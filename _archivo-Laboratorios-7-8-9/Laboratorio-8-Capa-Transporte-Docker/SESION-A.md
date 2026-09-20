# Laboratorio N.° 8 — Capa de Transporte con Docker · Sesión A: TCP vs UDP — sockets, handshake y puertos

Semana 8 · Clase 1

Cubre las **Partes 1 y 2** del laboratorio original: comunicación básica entre
contenedores (red Docker, servidor TCP con Flask, cliente con curl y captura del
three-way handshake con tcpdump) y la comparación UDP vs TCP.

## Objetivo de la sesión

Vas a levantar con tus propias manos una aplicación TCP dentro de contenedores:
crearás la red, escribirás el servidor Flask, construirás la imagen, la
ejecutarás, la consumirás con curl y observarás los paquetes `SYN`, `SYN-ACK` y
`ACK` en vivo con tcpdump. Después montarás un servidor UDP y compararás su
comportamiento con el de TCP.

---

## Paso 1. Crea la red Docker personalizada

```bash
# Crear red bridge personalizada
docker network create laboratorio-red

# Verificar la red creada
docker network ls
docker network inspect laboratorio-red
```

**Pregunta 1**: ¿Qué rango de IPs asigna Docker a los contenedores en esta red?

## Paso 2. Escribe y compila el servidor TCP (Flask)

Este es el único archivo que construyes hoy; la imagen `servidor-tcp` se
reutilizará en la Sesión B.

```bash
# Crear directorio de trabajo
mkdir -p ~/laboratorio-transporte && cd ~/laboratorio-transporte

# Crear archivo Dockerfile para el servidor
cat > Dockerfile.server << 'EOF'
FROM python:3.11-slim
RUN pip install --no-cache-dir flask
COPY server.py /app/server.py
WORKDIR /app
EXPOSE 5000
CMD ["python", "server.py"]
EOF

# Crear servidor Flask
cat > server.py << 'EOF'
from flask import Flask, request
import socket
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    client_ip = request.remote_addr
    server_ip = socket.gethostbyname(socket.gethostname())
    return {
        "mensaje": "Hola desde el servidor TCP",
        "servidor_ip": server_ip,
        "cliente_ip": client_ip,
        "protocolo": "TCP",
        "puerto_servidor": 5000,
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.route('/datos', methods=['POST'])
def recibir_datos():
    datos = request.get_json()
    return {
        "recibido": datos,
        "servidor": socket.gethostbyname(socket.gethostname()),
        "status": "ok"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

# Construir imagen
docker build -f Dockerfile.server -t servidor-tcp .
```

## Paso 3. Levanta el servidor y pruébalo con un cliente

```bash
# Ejecutar servidor en background
docker run -d --name servidor-web --network laboratorio-red -p 8080:5000 servidor-tcp

# Verificar que el servidor está corriendo
docker ps

# Obtener IP del contenedor servidor
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' servidor-web

# Ejecutar cliente (contenedor temporal)
docker run --rm --network laboratorio-red curlimages/curl \
  curl http://servidor-web:5000/
```

**Pregunta 2**: ¿Qué diferencia hay entre acceder a `http://localhost:8080` desde el host vs `http://servidor-web:5000` desde dentro de la red Docker?

## Paso 4. Observa el handshake TCP con tcpdump

Usa **tres terminales**: en la primera instalas tcpdump, en la segunda inicias
la captura y en la tercera haces la petición.

```bash
# Terminal 1: instalar tcpdump dentro del contenedor servidor
docker exec -it servidor-web bash -c "apt-get update && apt-get install -y tcpdump"
```

```bash
# Terminal 2: iniciar captura (queda escuchando)
docker exec -it servidor-web tcpdump -i eth0 -c 10 port 5000
```

```bash
# Terminal 3: hacer una petición
docker run --rm --network laboratorio-red curlimages/curl \
  curl http://servidor-web:5000/
```

**Pregunta 3**: En la captura de tcpdump, ¿puedes identificar los paquetes SYN, SYN-ACK y ACK? ¿Cuántos bytes tiene cada uno?

## Paso 5. Crea y ejecuta el servidor UDP

```bash
cat > Dockerfile.udp << 'EOF'
FROM python:3.11-slim
COPY udp_server.py /app/udp_server.py
WORKDIR /app
EXPOSE 9000/udp
CMD ["python", "udp_server.py"]
EOF

cat > udp_server.py << 'EOF'
import socket
import json
import datetime

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 9000))
    print("Servidor UDP escuchando en puerto 9000...")

    while True:
        data, addr = sock.recvfrom(1024)
        mensaje = data.decode('utf-8')
        respuesta = json.dumps({
            "recibido": mensaje,
            "origen": f"{addr[0]}:{addr[1]}",
            "servidor": "udp-server",
            "timestamp": datetime.datetime.now().isoformat()
        })
        sock.sendto(respuesta.encode('utf-8'), addr)
        print(f"Mensaje de {addr}: {mensaje}")

if __name__ == '__main__':
    main()
EOF

# Construir y ejecutar
docker build -f Dockerfile.udp -t servidor-udp .
docker run -d --name udp-server --network laboratorio-red servidor-udp
```

## Paso 6. Compara TCP y UDP con un cliente de prueba

```bash
# Crear script de prueba UDP
cat > udp_client.py << 'EOF'
import socket
import json
import time
import sys

def test_udp(message, server_host, port=9000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)

    start = time.time()
    sock.sendto(message.encode('utf-8'), (server_host, port))

    try:
        data, addr = sock.recvfrom(1024)
        elapsed = time.time() - start
        response = json.loads(data.decode('utf-8'))
        print(f"Mensaje: {message}")
        print(f"Respuesta: {response}")
        print(f"RTT: {elapsed*1000:.2f} ms")
        print(f"{'='*50}")
    except socket.timeout:
        print(f"Timeout para mensaje: {message}")
    finally:
        sock.close()

if __name__ == '__main__':
    server = sys.argv[1] if len(sys.argv) > 1 else "udp-server"
    messages = ["Hola UDP 1", "Hola UDP 2", "Hola UDP 3"]
    for msg in messages:
        test_udp(msg, server)
EOF

# Ejecutar cliente UDP (mide el RTT de cada datagrama)
docker run --rm --network laboratorio-red -v $(pwd)/udp_client.py:/app/udp_client.py \
  python:3.11-slim python /app/udp_client.py udp-server
```

**Pregunta 4**: ¿Qué sucede si el servidor UDP no está disponible cuando se envía un mensaje? Compara con el comportamiento de TCP.

**Pregunta 5**: ¿Por qué UDP es preferido para streaming de video en tiempo real?

---

## Entregable de la sesión

1. **Captura de pantalla** de la red `laboratorio-red` creada y del contenedor `servidor-web` corriendo (`docker ps`).
2. **Captura de tcpdump** mostrando los paquetes `SYN`, `SYN-ACK` y `ACK` del handshake.
3. **Tabla comparativa TCP vs UDP** con evidencia de laboratorio (salida del cliente UDP con los RTT medidos y la respuesta del servidor TCP por curl).
4. **Respuestas** a las preguntas 1 a 5.

## Rúbrica de la sesión

| Criterio | Puntos |
|----------|--------|
| Red Docker creada y servidor TCP levantado y respondiendo | 10 |
| Cliente curl funcionando y captura del handshake (SYN / SYN-ACK / ACK) | 10 |
| Servidor UDP funcionando y comparación TCP/UDP con evidencia | 10 |
| Tabla comparativa y calidad de las capturas | 10 |
| Respuestas a las preguntas 1-5 (análisis y comprensión) | 10 |
| **Total** | **50** |