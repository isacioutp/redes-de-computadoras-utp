# Laboratorio N.° 10 — Implementación de una LAN y Herramientas de Monitoreo · Sesión A: Construir la LAN corporativa

Semana 12 · Clase 1

Cubre las **Partes 1 y 2** del laboratorio original: el diseño de la LAN
(subredes `publica` e `interna`, router corporativo dual-homed) y el despliegue
de los servicios de la oficina (web nginx, base de datos postgres, aplicación
flask y DNS interno con dnsmasq).

## Objetivo de la sesión

Construir, con comandos y desde cero, una LAN corporativa funcional en Docker:
crea dos subredes, levanta un contenedor que hace de router, publica los
servicios de la oficina y valida que todos se resuelven por nombre gracias al
DNS interno. Al terminar tendrás la red real que en la Clase 2 enrutarás de
forma explícita y monitorearás.

## Pasos

### Paso 1: Crea los segmentos de la LAN

Crea la red "pública" de la oficina (donde se publican los servicios) y la red
"interna" (servidores de aplicación y datos):

```bash
# Red "pública" de la oficina (donde se publican servicios)
docker network create publica --subnet 10.0.0.0/24 --gateway 10.0.0.1

# Red "interna" (servidores de aplicación y datos)
docker network create interna --subnet 10.0.1.0/24 --gateway 10.0.1.1
```

### Paso 2: Levanta el router corporativo

Construye el contenedor que actuará de router entre ambas redes y conéctalo a
las dos subredes (queda *dual-homed*):

```bash
# Contenedor que actuará de router entre ambas redes
docker run -d --name router-corp --cap-add=NET_ADMIN alpine sleep 3600
docker network connect publica router-corp
docker network connect interna router-corp

# Interfaces del router
docker exec router-corp ip addr show
```

Observa la salida: el router debe mostrar **dos interfaces**, una dentro de
`10.0.0.0/24` y otra dentro de `10.0.1.0/24`.

> **Checkpoint:** registra las dos IP que Docker asignó a `router-corp`; las
> usarás para responder la Pregunta 1.

### Paso 3: Publica el servidor web (red pública)

Levanta nginx en la red pública y verifica que responde:

```bash
docker run -d --name web-srv --network publica -p 8080:80 nginx:alpine
docker exec web-srv curl -s http://localhost/ -o /dev/null -w 'HTTP %{http_code}\n'
```

### Paso 4: Publica la base de datos (red interna)

Levanta postgres en la red interna y confirma que el puerto 5432 queda en
escucha:

```bash
docker run -d --name db-srv --network interna -e POSTGRES_PASSWORD=labpass123 postgres:15-alpine

# Verificar puerto 5432 en escucha
docker logs db-srv 2>&1 | grep -i "ready" | head
```

### Paso 5: Construye el servidor de aplicación (interno)

Crea y compila la aplicación flask que llama a web y a db por nombre, y
conéctala a las dos redes:

```bash
mkdir -p lab10-app
cat > lab10-app/app.py << 'EOF'
from flask import Flask, jsonify
import socket, requests, time

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/')
def home():
    return jsonify(nodo=socket.gethostname(),
                   mensaje="Hola desde la LAN corporativa")

@app.route('/web')
def check_web():
    try:
        r = requests.get('http://web-srv/', timeout=3)
        return jsonify(web=r.status_code)
    except Exception as e:
        return jsonify(web=f"error: {e}")

@app.route('/db')
def check_db():
    try:
        import psycopg2
        conn = psycopg2.connect(host='db-srv', dbname='postgres',
                                user='postgres', password='labpass123', connect_timeout=3)
        cur = conn.cursor()
        cur.execute('SELECT version()')
        v = cur.fetchone()[0].split()[0]
        conn.close()
        return jsonify(db=f"postgres {v}")
    except Exception as e:
        return jsonify(db=f"error: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

cat > lab10-app/Dockerfile << 'EOF'
FROM python:3.11-slim
RUN pip install --no-cache-dir flask requests psycopg2-binary
COPY app.py /app/app.py
WORKDIR /app
EXPOSE 5000
CMD ["python", "app.py"]
EOF

docker build -t app-corp lab10-app

# Conectado a las dos redes (accede a web-srv por name DNS y a db-srv)
docker run -d --name app-srv --network interna -p 5001:5000 app-corp
docker network connect publica app-srv
```

### Paso 6: Instala el DNS interno de la oficina (dnsmasq)

Levanta dnsmasq para resolver los nombres de la oficina:

```bash
docker run -d --name dns-corp --network publica \
  -p 53:53/udp \
  -e PORTS="53" \
  jpillora/dnsmasq \
  --address=/web.local/10.0.0.3 \
  --address=/app.local/10.0.1.2 \
  --server=8.8.8.8 \
  --no-resolv
```

Verifica las resoluciones (usa la IP real de `dns-corp`):

```bash
host_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dns-corp)
echo "DNS en: $host_ip"
docker run --rm --dns $host_ip alpine sh -c \
  "apk add --no-cache bind-tools -q && nslookup web.local $host_ip && nslookup app.local $host_ip"
```

> **Checkpoint:** si las dos `nslookup` devuelven las IP correctas (10.0.0.3 y
> 10.0.1.2), tu DNS interno de oficina está funcionando. Captura esa salida.

## Preguntas de la sesión

1. ¿Cuántas interfaces tiene `router-corp`? ¿Qué IP le asignó Docker en cada
   red?
2. ¿Qué registros creaste (`A`)? ¿Cómo se resolvería `app.local`? ¿Qué ventaja
   tiene el DNS interno para microservicios?
3. **Pregunta de construcción**: verifica que `app-srv` alcanza a `web-srv` y
   a `db-srv` por nombre, sin usar IPs:

   ```bash
   docker exec app-srv curl -s http://web-srv/ -o /dev/null -w 'web: HTTP %{http_code}\n'
   docker exec app-srv ping -c 2 db-srv
   ```

   Documenta qué responde cada verificación y explica por qué es posible usar
   los nombres de los contenedores sin conocer sus IPs.

## Entregable de la sesión

1. Captura de `docker network ls` mostrando las redes `publica` e `interna`.
2. Salida de `docker exec router-corp ip addr show` con las 2 interfaces.
3. `nslookup web.local` y `nslookup app.local` funcionando contra `dns-corp`.
4. Respuestas a las preguntas 1–3.

## Rúbrica de la sesión (50 puntos)

| Criterio | Puntos |
|----------|--------|
| Redes `publica`/`interna` creadas y visibles en `docker network ls` | 10 |
| `router-corp` con 2 interfaces (dual-homed) | 10 |
| Servicios `web-srv`, `db-srv` y `app-srv` funcionando | 10 |
| DNS interno resolviendo `web.local` y `app.local` | 10 |
| Preguntas 1–3 respondidas | 10 |
| **Total** | **50** |