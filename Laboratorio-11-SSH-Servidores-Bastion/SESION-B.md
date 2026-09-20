# Laboratorio N.° 11 — Claves SSH y Servidores Bastión · Sesión B: Servidores bastión en producción

Semana 11 · Clase 2

Cubre las **Partes 4, 5 y 6** del laboratorio original: bastión dual-homed con
red `--internal`, SSH ProxyJump, bastión web con nginx como proxy inverso,
endurecimiento con iptables (deep-secure) y la puesta en producción con
`~/.ssh/config`.

## Objetivo de la sesión

Llevar el concepto de bastión a producción: construir un bastión *dual-homed*
que es el único punto de entrada entre la red pública y la privada, saltar a
los servidores internos con ProxyJump, publicar una API interna detrás de un
bastión web con nginx y dejar la configuración persistente en `~/.ssh/config`.

## Pasos

### Paso 1: Crea las redes pública y privada

Crea la red pública y la red privada sin salida a internet:

```bash
docker network create red-publica   --subnet 172.20.0.0/24
docker network create red-privada   --subnet 172.20.1.0/24 --internal  # sin internet
```

### Paso 2: Construye el bastión dual-homed

Despliega el servidor SSH bastión con 2 interfaces (una en cada red):

```bash
# Servidor SSH bastion en las DOS redes
docker run -d --name bastion \
  -p 2200:2222 \
  -e PUBLIC_KEY_FILE=/authorized_keys \
  -e USER_NAME=alumno \
  -v $(pwd)/llave_lab11.pub:/authorized_keys:ro \
  linuxserver/openssh-server

docker network connect red-publica bastion
docker network connect red-privada bastion

# Ver las 2 interfaces
docker exec bastion ip addr show | grep inet
```

> **Checkpoint:** anota las 2 IP del bastión (una en `172.20.0.0/24` y otra en
> `172.20.1.0/24`); las necesitas para la Pregunta 1 y el diagrama.

### Paso 3: Aisla los servidores internos en la red privada

Levanta un contenedor interno SOLO en `red-privada` y verifica que no tiene
salida a internet:

```bash
docker run -d --name app-interno --network red-privada --cap-add=NET_ADMIN \
  alpine sleep 3600

# Verificación: app-interno NO tiene salida a internet
docker exec app-interno ping -c 1 8.8.8.8  # ¿funciona? ¿por qué?
```

### Paso 4: Salta al servidor interno con SSH ProxyJump

Copia tu llave al interno (simulando la puerta trasera de admin) y salta desde
el host a través del bastión:

```bash
# Copiar la llave al app-interno (simulamos puerta trasera de admin)
docker exec app-interno sh -c "apk add --no-cache openssh >/dev/null; \
  mkdir -p ~/.ssh && cp /dev/stdin ~/.ssh/authorized_keys && chmod 700 ~/.ssh" < llave_lab11.pub

# Desde el host, entrar en red privada saltando por bastion
ssh -J alumno@localhost:2200 \
    -i llave_lab11 \
    root@172.20.1.2 2>/dev/null || echo "ejemplo conceptual"
```

> En producción, `ProxyJump` (`-J`) es la forma estándar de llegar a servidores
> internos a través del bastión. Docker aquí no ejecuta SSH real en el
> `app-interno` por defecto, pero el concepto es el mismo que en una oficina
> real con VMs.

### Paso 5: Publica una API interna detrás de un bastión web

Crea el servicio interno (no expuesto) y el bastión web que hace proxy hacia
él:

```bash
# Servicio interno (no expuesto)
docker run -d --name internal-api --network red-privada --cap-add=NET_ADMIN \
  python:3.11-slim sh -c "pip install flask -q; python -c \"from flask import Flask; \
  app=Flask(__name__); @app.route('/'); def h(): return 'API interna'; \
  app.run(host='0.0.0.0',port=5000)\""

# Bastión web: expone 80 y hace proxy al interno (sin exponer la API)
mkdir -p basweb
cat > basweb/nginx.conf << 'EOF'
worker_processes 1;
events { worker_connections 1024; }
http {
    server {
        listen 80;
        location /api/ {
            proxy_pass http://internal-api:5000/;
        }
        location / {
            return 200 'Bastion web - inverso';
        }
    }
}
EOF

docker run -d --name bastion-web -p 8085:80 \
  -v $(pwd)/basweb/nginx.conf:/etc/nginx/nginx.conf:ro \
  --network red-publica nginx:alpine
docker network connect red-privada bastion-web

# Probar: el puerto 80 expone al interno SIN exposicion directa
curl http://localhost:8085/
curl http://localhost:8085/api/
```

> **Checkpoint:** si `curl http://localhost:8085/api/` devuelve `API interna`,
> el bastión web está publicando la API sin exponerla directamente. Captúralo.

### Paso 6: Endurece el bastión con iptables (deep-secure)

Aplica la política de firewall: solo entra por el puerto 2222 desde el host:

```bash
# iptables en bastion: Solo permitir entrada por el puerto 2222 desde el host
docker exec bastion sh -c "apk add --no-cache iptables -q; \
  iptables -A INPUT -p tcp --dport 2222 -j ACCEPT; \
  iptables -P INPUT DROP" 2>/dev/null || echo "requiere host supports; verificar"
```

### Paso 7: Deja la configuración persistente en `~/.ssh/config`

Crea la config SSH del host (o en el workspace `ssh.config`) y prueba el acceso
con ProxyJump automático:

```text
Host bastion-lab
    HostName localhost
    Port 2200
    User alumno
    IdentityFile /home/tu-usuario/lab11/llave_lab11

Host app-interno
    HostName 172.20.1.2
    ProxyJump bastion-lab
    IdentityFile /home/tu-usuario/lab11/llave_lab11
```

```bash
# Probar
ssh -F ssh.config app-interno 'echo GRANDE - sin password y sin exponer nada'
```

## Preguntas de la sesión

1. ¿Cuántas direcciones IP tiene el bastión? Menciona la IP en cada red. ¿Es
   "dual-homed" porque tiene dos NIC?
2. ¿La red `--internal` permite acceso a internet? Verifica que `ping 8.8.8.8`
   falle. ¿Qué capa lo corta (el NAT del host)?
3. Explica con un diagrama la ruta: `TuPC → [bastion:2200] → app-interno`.
   ¿Qué ganas de seguridad al NO exponer `app-interno` a internet?
4. ¿Qué servicio está realmente expuesto (`bastion-web`) y cuál no
   (`internal-api`)? ¿Qué rol juega nginx (proxy inverso) y qué lo hace un
   "bastión de aplicación"?
5. ¿Qué política de firewall aplicaste (INPUT)? ¿Qué implicación tiene para los
   demás puertos del bastión? ¿Por qué se llama *deep-secure*?
6. ¿Qué ventaja da centralizar la configuración en `~/.ssh/config` para un
   equipo de desarrollo (SSO, portales de acceso, rotación de llaves)?
   Relaciona con el concepto de *bastion* en la nube (AWS Systems Manager
   Session Manager, Azure Bastion).

## Entregable de la sesión

1. Diagrama del bastión dual-homed con sus 2 IPs (Pregunta 3).
2. Evidencia de `bastion-web` proxy funcionando (puerto 8085, Pregunta 4).
3. `~/.ssh/config` (o `ssh.config`) creado y usado con `ssh -F`.
4. Respuestas a las preguntas 1–6.

## Rúbrica de la sesión (50 puntos)

| Criterio | Puntos |
|----------|--------|
| Bastión dual-homed + red `--internal` verificada | 10 |
| ProxyJump + diagrama de ruta | 10 |
| Bastión web (proxy inverso) + deep-secure iptables | 15 |
| `~/.ssh/config` + flujo completo | 10 |
| Preguntas 1–6 respondidas | 5 |
| **Total** | **50** |