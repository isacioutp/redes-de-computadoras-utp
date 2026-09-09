# Laboratorio N.° 5 — Modelo OSI y arquitectura de protocolos con Docker

Temas 2.1–2.4 · Semana 6 · Unidad II

## Objetivo

Comprender la **arquitectura en capas** de los protocolos de red: qué hace cada
capa del modelo OSI y cómo se relaciona con el modelo TCP/IP que realmente
usan tus aplicaciones. Lo verás "en vivo": un mensaje viajará de tu código
(capa de aplicación) hasta los bits en el medio, y de vuelta, capturando cada
capa con contenedores Docker.

## Contexto teórico

### ¿Por qué capas?

Un protocolo es un conjunto de reglas de comunicación. En vez de un solo
protocolo gigante, la comunicación se divide en **capas**; cada una tiene una
responsabilidad única y solo habla con la capa de arriba y la de abajo.

Ventajas clave para ti como desarrollador:

- **Modularidad**: cambias HTTP por WebSocket sin tocar TCP ni IP.
- **Reutilización**: no escribes control de errores — TCP ya lo hace.
- **Diagnóstico**: cuando algo falla, sabes qué capa revisar.

### Modelo OSI (7 capas) vs TCP/IP (4 capas)

```
OSI (7 capas)            TCP/IP (4 capas)        Tu código
─────────────────────    ─────────────────────   ─────────────────
7. Aplicación       ┐
6. Presentación     ┤ →  4. Aplicación           Flask, Express, Django
5. Sesión           ┘                            (HTTP, DNS, SMTP)
─────────────────────    ─────────────────────   ─────────────────
4. Transporte            3. Transporte           TCP / UDP
                          (headers de sockets)
─────────────────────    ─────────────────────   ─────────────────
3. Red                  2. Internet              IP (direcciones)
─────────────────────    ─────────────────────   ─────────────────
2. Enlace de datos      1. Acceso a la red       Ethernet, Wi-Fi
1. Física                (hardware, drivers)
─────────────────────    ─────────────────────   ─────────────────
```

### PDU/SDU en cada capa

| Capa | PDU (lo que se transmite) |
|------|---------------------------|
| Aplicación | Datos / mensaje |
| Transporte | Segmento |
| Red | Paquete |
| Enlace | Trama (frame) |

## Materiales

- Docker instalado.
- Wireshark en el host (o usar tcpdump dentro de los contenedores).
- No necesitas Packet Tracer: la simulación será real con contenedores.

## Requisitos previos

```bash
docker --version
docker ps
```

### Instalación de Docker (recomendado: Linux / Ubuntu Server)

Para este laboratorio (y toda la unidad) es mucho más práctico usar
**Linux**, idealmente un **Ubuntu Server** (real o VM): Docker es nativo,
no requiere WSL ni Hyper-V, y los contenedores de red (tcpdump, bridges,
iptables) se comportan igual que en producción. En Windows tendrías que
lidiar con WSL 2 o Docker Desktop, que ocultan capas del OSI que aquí sí
queremos observar.

```bash
# Ubuntu Server (llévelo LTS: 22.04/24.04)
sudo apt update && sudo apt install -y docker.io
sudo usermod -aG docker $USER   # evita usar sudo en cada comando
newgrp docker                   # activa el grupo en la sesión actual

# O apt oficial del proyecto Docker
curl -fsSL https://get.docker.com | sudo sh

# Verificar
docker --version
docker run --rm hello-world
```

> Si usas Windows, la alternativa es instalar WSL 2 con Ubuntu y seguir los
> mismos pasos dentro de la distribución.

---

## Parte 1: La pila de red de tu máquina

### Paso 1.1: Listar las capas de la pila local

```bash
# Capa 2 (enlace): interfaces y direcciones MAC
ip link
# Capa 3 (red): direcciones IP y rutas
ip addr show
ip route
# Capa 4 (transporte): puertos en escucha
ss -tlnp
# Capa 7 (aplicación): procesos que usan la red
lsof -i
```

**Pregunta 1**: Para la interfaz activa, anota: dirección MAC (capa 2),
dirección IP y gateway (capa 3). ¿Qué procesos ves escuchando en puertos
(capa 4→7)?

### Paso 1.2: Un solo servicio usa varias capas

```bash
# Detrás de "docker run -p" hay red (capa 4) y procesos (capa 7)
docker ps --format 'table {{.Names}}\t{{.Ports}}'
ps aux | grep docker | grep -v grep | head
```

**Pregunta 2**: ¿Dónde encaja un "contenedor" en el modelo OSI? Una pista: el
contenedor comparte el kernel del host. ¿Qué capas son las del host y cuáles
las del contenedor?

---

## Parte 2: Montar el escenario de simulación

### Paso 2.1: Red y servidor

```bash
docker network create lab5-red

# Servidor web (capa 7 = HTTP, sobre capa 4 = TCP)
docker run -d --name web --network lab5-red -p 8080:5000 \
  -e FLASK_PORT=5000 \
  python:3.11-slim sh -c \
  "pip install flask -q && python -c \"from flask import Flask; app=Flask(__name__); \
   @app.route('/'); def h(): return 'Hola desde la capa 7'; app.run(host='0.0.0.0',port=5000)\""
```

### Paso 2.2: Cliente con herramientas de capa 7

```bash
# Contenedor "cliente" con curl (capa 7)
docker run -d --name client --network lab5-red alpine sleep 3600
docker exec client sh -c "apk add --no-cache curl tcpdump bind-tools"

# Verificar red
docker exec client ping -c 1 web
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' client
```

---

## Parte 3: Recorrer las capas con una petición HTTP

### Paso 3.1: Capturar TODAS las capas a la vez

```bash
# Terminal A — captura en el contenedor del servidor
docker exec web sh -c "apt-get update >/dev/null && apt-get install -y tcpdump >/dev/null && tcpdump -i eth0 -nn -XX port 5000" &
sleep 2
# Terminal B — disparar la petición
docker exec client curl http://web:5000/
```

Verás algo como:

```
... IP 172.x.x.a > 172.x.x.b.5000: Flags [P.] ... : HTTP: GET / HTTP/1.1

0x0000:  0242 ac11000b 0242 ac11000a 0800 4500 003c  .....
         └─order in trama: MACdst MACsrc EtherType | IPv4
```

### Paso 3.2: Identificar cada capa en la captura

Completa esta tabla usando la salida `-XX` de tcpdump (y Wireshark en el host
si quieres verlo más claro):

| Bytes en la trama | Campo | Capa OSI | PDU |
|-------------------|-------|----------|-----|
| 0–5 | MAC destino | 2 · Enlace | Trama |
| 6–11 | MAC origen | 2 · Enlace | Trama |
| 12–13 | EtherType (`0x0800`) | 2 · Enlace | Trama |
| 14–17 | Versión + IHL | 3 · Red | Paquete |
| 18+ | IP origen/destino | 3 · Red | Paquete |
| … | Puerto origen/destino (TCP) | 4 · Transporte | Segmento |
| … | `GET / HTTP/1.1` | 7 · Aplicación | Mensaje/Datos |

**Pregunta 3**: ¿Qué capa del modelo OSI se repite en las capas 5 y 6
(sesión/presentación) cuando usa HTTP sin cifrado? ¿Dónde aparecería una capa
5/6 si usarás HTTPS?

### Paso 3.3: Simular el viaje completo

El recorrido del dato por las capas (encapsulamiento):

```
 cliente                                   servidor web
─────────────────                         ─────────────────
 application: "GET /"        →                    application: HTTP recibido
 transport:   SYNC/SEQ=0  →  segmento            transport:   ACK/SEQ_ok
 network:     IP origen/dest → paquete           network:     IP recibida
 link:        MAC src/dst  →  trama              link:        MAC leída
 physical:    bits en cable                       physical:    señal
```

**Pregunta 4**: Escribe en una sola línea el "viaje" de la palabra `Hola`
desde el cliente hasta el servidor nombrando el PDU de cada capa (mensaje →
segmento → paquete → trama → bits).

---

## Parte 4: Distintos protocolos, distintas capas

### Paso 4.1: UDP — DNS (capa 4 sin conexión + capa 7)

```bash
# Capturar DNS (UDP, puerto 53)
docker exec web tcpdump -i eth0 -nn -XX udp port 53 &

# Disparar una consulta DNS desde el cliente
docker exec client nslookup google.com
sleep 1 && docker exec web pkill tcpdump
```

**Pregunta 5**: El DNS viaja sobre **UDP**, no TCP. En la captura, ¿qué header
de transporte ves? ¿Cómo sabes que es UDP (protocolo `17` en IP)?

### Paso 4.2: ICMP — sin capa de transporte

```bash
# Capturar ICMP (directo entre capa 3 y 7)
docker exec web tcpdump -i eth0 -nn -XX icmp &

# Disparar ping
docker exec client ping -c 1 web
sleep 1 && docker exec web pkill tcpdump
```

**Pregunta 6**: ¿El ICMP tiene puertos origen/destino? ¿En qué capa se
encuentra? Compara con DNS: ¿qué capa de transporte usa cada uno?

### Paso 4.3: Tabla comparativa

| Protocolo | Puerto | Transporte | Capa OSI | Uso |
|-----------|--------|------------|----------|-----|
| HTTP | 80 | TCP | 7 (y 4,3,2,1) | Navegación |
| DNS | 53 | UDP/TCP | 7 (y 4,3,2,1) | Resolución de nombres |
| ICMP | — | ninguno | 3 | Diagnóstico (ping) |
| ARP | — | ninguno | 2 | IP→MAC |

**Pregunta 7**: Completa la columna "Transporte" de la tabla con lo que
observaste en las capturas. ¿Por qué DNS puede usar UDP si "pierde" paquetes?

---

## Parte 5: Simular fallas y ver qué capa la detecta

### Paso 5.1: Falla en capa 4 — puerto cerrado

```bash
# El puerto 9999 no está abierto en web
docker exec client curl -v http://web:9999/
```

Verás: `Connection refused` — lo reporta la **capa 4** (TCP RST).

**Pregunta 8**: ¿Qué capa detectó el fallo? ¿Qué significa `Connection refused`
a nivel TCP (paquete RST)?

### Paso 5.2: Falla en capa 3 — destino inalcanzable

```bash
# IP que no existe en la red
docker exec client ping -c 2 172.28.0.99
docker exec client ping -c 2 8.8.8.8
```

Verás: `Destination Host Unreachable` (ICMP reportado por la **capa 3**).

**Pregunta 9**: ¿Qué protocolo reporta este error y en qué capa se encuentra?

### Paso 5.3: Falla en capa 2 — red aislada (dominio de colisión)

```bash
# Red totalmente aislada (sin conexión a otras)
docker network create -o com.docker.network.bridge.enable_ip_masquerade=false aislada
docker run -d --name netweb --network aislada python:3.11-slim sh -c "pip install flask -q && python -c \"from flask import Flask; app=Flask(__name__); @app.route('/'); def h(): return 'ok'; app.run(host='0.0.0.0',port=5000)\"" 
docker run -d --name netcli --network aislada alpine sleep 3600
docker exec netcli curl -s http://netweb:5000/ && echo " OK-en-capa-2" || echo " falla"
```

**Pregunta 10**: Si `curl` falla, ¿qué capa lo está impidiendo? Piensa en el
aislamiento de red de Docker (capa 2, bridges) vs el DNS/naming (capa 7).

### Paso 5.4: Tabla — errores y sus capas

| Error | Capa que lo detecta | Protocolo | El usuario ve |
|-------|---------------------|-----------|---------------|
| Puerto cerrado | 4 · Transporte | TCP RST | Connection refused |
| IP inalcanzable | 3 · Red | ICMP | Host unreachable |
| Red aislada | 3 · Red (+2) | ICMP/NAT | Timeout / unreachable |
| Certificado SSL | 6 · Presentación | TLS alert | SSL error |
| HTTP 404 | 7 · Aplicación | HTTP | 404 Not Found |

**Pregunta 11**: Escribe las 5 situaciones en tu entregable y explica cuál
capa del modelo OSI "habla" primero cuando algo falla.

---

## Parte 6: Capas invisibles (5 y 6) en tu código

Como desarrollador usas la 5 y la 6 sin darte cuenta:

| Capa OSI | Lo que hace | Ejemplo en dev |
|----------|-------------|----------------|
| 5 · Sesión | Mantiene la conversación | Sesiones de Flask/Django, cookies, JWT |
| 6 · Presentación | Formato, cifrado, compresión | JSON, TLS/SSL, gzip, base64 |

```bash
# Ver qué formato negocia HTTP (capa 6: representación)
docker exec client curl -H "Accept: application/json" http://web:5000/ -v

# Ver el cifrado con HTTPS (capa 6)
docker exec client curl -kv https://google.com 2>&1 | grep -E "SSL|TLS|certificate" | head
```

**Pregunta 12**: ¿Qué headers de HTTP viste que correspondan a la capa 6
(`Content-Type`, `Accept`, `Content-Encoding`)? ¿Y a la capa 5 (`Cookie`,
`Session-ID`)?

---

## Actividad de refuerzo — Wireshark en el host

1. En Wireshark del host, elige la interfaz del bridge de `lab5-red`
   (se llama `br-xxxx`).
2. Dispara la petición del Paso 3.1.
3. En **Vista → Colores**, identifica: protocolos de la capa 7 (HTTP), 4
   (TCP), 3 (IP), 2 (ARP/Ethernet).
4. Actualiza la tabla del Paso 3.2 con las capas 5/6 (si las vieras) y anota
   los nombres de PDU en el detalle: `[TCP segment]`, `[IP packet]`,
   `[Ethernet frame]`.

**Pregunta 13**: ¿Cómo distingue Wireshark la "capa" de un protocolo? Usa lo
que leíste en la cabecera (EtherType, protocolo IP, puerto TCP).

---

## Preguntas de verificación

1. ¿Cuáles son las 7 capas del modelo OSI y cuál es la función principal de
   cada una?
2. ¿Cuáles son las 4 capas del modelo TCP/IP? Haz la correspondencia con OSI.
3. ¿Qué es un PDU y por qué cada capa tiene uno diferente?
4. En una petición HTTPS, ¿dónde se insertan las capas 5 y 6 (sesión y
   presentación)? ¿Qué aportan a la conversación HTTP?
5. ¿Por qué un contenedor Docker puede abstraer varias capas del OSI?
6. Tu aplicación falla con `Connection refused`. ¿Qué capa consultarías
   primero y con qué comando?
7. ¿Por qué es útil el modelo en capas para un desarrollador de software?

## Entregable

1. Captura de la Tabla del Paso 3.2 completada con tu análisis `-XX`.
2. Capturas de las 4 capturas (HTTP, DNS, ICMP, ARP) mostrando cada capa.
3. Tabla de "errores y capas" del Paso 5.4.
4. Respuestas a las **13 preguntas**.
5. Diagrama de capas dibujado sobre tu stack de desarrollo (por ejemplo: tu
   app Flask → TCP → IP → Ethernet de Docker).

## Rúbrica

| Criterio | Puntos |
|----------|--------|
| Partes 1-2 (pila local + escenario) | 15 |
| Parte 3 (recorrido de HTTP por capas) | 25 |
| Parte 4 (TCP vs UDP vs ICMP) | 20 |
| Parte 5 (simular fallas) | 20 |
| Parte 6 + refuerzo (capas 5/6, Wireshark) | 10 |
| Preguntas de verificación | 10 |
| **Total** | **100** |

## Limpieza

```bash
docker rm -f web client netweb netcli
docker network rm lab5-red aislada
```