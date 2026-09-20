# Laboratorio N.º 5 — Modelo OSI y TCP/IP con Docker

Tema: modelo OSI / TCP-IP · Semanas 4-5 · Unidad II
Combinado con el Lab 4 (análisis de trama); se resuelve en una clase.

> **Idea en 1 línea**: en una sola petición HTTP ves **todas las capas** del OSI
> caminando en vivo, comparas TCP vs UDP vs ICMP, y cada falla te dice **qué
> capa la detectó**. Todo con Docker.

## 1. Teoría mínima

### ¿Por qué capas?

La comunicación se divide en **capas**, cada una con una responsabilidad única
que solo habla con la de arriba y la de abajo. Como dev te sirve para:
- **Diagnóstico**: cuando falla algo, sabes qué capa mirar.
- **Modularidad**: cambias HTTP por WebSocket sin tocar TCP ni IP.
- **Reutilización**: no escribes control de errores — TCP ya lo hace.

### OSI (7) vs TCP/IP (4) vs tu código

```
OSI (7 capas)            TCP/IP (4 capas)      Tu código
─────────────────────    ──────────────────    ──────────────────
7 Aplicación        ┐
6 Presentación      ┤ →  4 Aplicación          Flask, HTTP, DNS, SMTP
5 Sesión            ┘
─────────────────────    ──────────────────    ──────────────────
4 Transporte              3 Transporte         TCP / UDP (sockets)
─────────────────────    ──────────────────    ──────────────────
3 Red                    2 Internet            IP (direcciones)
─────────────────────    ──────────────────    ──────────────────
2 Enlace                 1 Acceso a la red     Ethernet, Wi-Fi (MAC)
1 Física                (hardware / drivers)
─────────────────────    ──────────────────    ──────────────────
```

### PDU: lo que viaja en cada capa

| Capa | PDU |
|------|-----|
| Aplicación | mensaje / datos |
| Transporte | segmento |
| Red | paquete |
| Enlace | trama |

## 2. Escenario (todo en Docker)

Servidor web (Flask) en la red `lab5-red` + cliente con herramientas:

```bash
docker network create lab5-red

# Servidor web: capa 7 (HTTP) sobre capa 4 (TCP), capa 3 (IP) y 2 (MAC)
docker run -d --name web --network lab5-red -p 8080:5000 \
  python:3.11-slim sh -c \
  "pip install flask -q && python -c \"from flask import Flask; app=Flask(__name__); \
   app.add_url_rule('/', 'h', lambda: 'Hola desde la capa 7'); app.run(host='0.0.0.0',port=5000)\""

# Cliente con curl (capa 7), tcpdump (capa 2-4), nslookup (capa 7)
docker run -d --name client --network lab5-red alpine sleep 3600
docker exec client apk add --no-cache curl tcpdump bind-tools

docker exec client ping -c 1 web                                  # capa 3 → ICMP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web
```

> `web` tarda unos segundos en arrancar (instala Flask la primera vez). Si la
> captura no muestra nada, espera y vuelve a disparar el `curl`.

## 3. Una petición HTTP = TODAS las capas

**Terminal A** (captura en el servidor):
```bash
docker exec web sh -c "apt-get update -q && apt-get install -y -q tcpdump && tcpdump -i eth0 -nn -XX port 5000"
```
**Terminal B** (dispara la petición):
```bash
docker exec client curl http://web:5000/
```

Con `-XX` se ven los bytes crudos. Ubica cada campo en tu captura (guárdala
para el entregable):

| Bytes | Campo | Capa OSI | PDU |
|-------|-------|----------|-----|
| 0-5 | MAC destino | 2 · Enlace | Trama |
| 6-11 | MAC origen | 2 · Enlace | Trama |
| 12-13 | EtherType `0x0800` (IPv4) | 2 · Enlace | Trama |
| 14-17 | Versión + IHL | 3 · Red | Paquete |
| 18+ | IP origen / destino | 3 · Red | Paquete |
| … | puerto origen / destino (TCP) | 4 · Transporte | Segmento |
| … | `GET / HTTP/1.1` | 7 · Aplicación | Mensaje |

El viaje del dato (encapsulamiento):

```
"GET /"  →  segmento TCP  →  paquete IP  →  trama Ethernet  →  bits en el cable
```

**P1.** En tu captura, ¿qué campos distinguen la **capa 2** (enlace) y cuáles la
**capa 4** (transporte)? ¿Qué PDU tiene cada una?

## 4. TCP vs UDP vs ICMP

### TCP (conexión) — ya lo viste en la sección 3
Detén la captura en `Flags [S]` (SYN), `[S.]` (SYN-ACK) y `[.]` (ACK): TCP
**establece la conversación antes de enviar datos** (capa 4 confiable).

### UDP (sin conexión) — tu propio DNS
```bash
# Servidor DNS propio que traduce test.local → IP de web
docker run -d --name dns --network lab5-red \
  jpillora/dnsmasq --address=/test.local/<IP_DE_WEB>
# IP de dns →  docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dns
```
**Terminal A** (captura en el cliente):
```bash
docker exec client tcpdump -i eth0 -nn -XX udp port 53
```
**Terminal B** (dispara una consulta):
```bash
docker exec client nslookup test.local <IP_DE_DNS>
```
En la captura: **sin SYN/ACK** (no hay conexión — solo una pregunta y una
respuesta). La cabecera IP dice **protocolo 17 = UDP** (`... 4011 ...`). El
header UDP trae 2 puertos (`0x886b 0035` = origen → 53). La consulta viaja en el
payload (capa 7).

### ICMP (sin transporte) — ping
**Terminal A:**
```bash
docker exec web tcpdump -i eth0 -nn -XX icmp
```
**Terminal B:**
```bash
docker exec client ping -c 1 web
```
ICMP **no lleva puertos**: vive en la capa 3 (diagnóstico).

| Protocolo | Puerto | Transporte | Capa OSI |
|-----------|--------|------------|----------|
| HTTP | 80 | TCP | 7 (y 4, 3, 2, 1) |
| DNS | 53 | UDP / TCP | 7 (y 4, 3, 2, 1) |
| ICMP | — | ninguno | 3 |

**P2.** En la captura UDP, ¿cómo sabes que **no** es TCP? ¿En qué capa vive
ICMP? ¿Por qué DNS "se atreve" a usar UDP aunque pierda paquetes?

## 5. Falla = la capa que la detecta

Ejecuta y anota el mensaje de error:

```bash
# Capa 4 — puerto cerrado → TCP responde con RST
docker exec client curl -v http://web:9999/

# Capas 2-3 — IP que no existe: ARP pregunta "¿quién es?" y nadie responde
# Terminal A:  docker exec client tcpdump -i eth0 -nn -XX arp
# Terminal B:  docker exec client ping -c 1 <IP_DE_WEB_CON_OCTETO_CAMBIADO>   → 100% loss

# Capa 7 — recurso que no existe en la app
docker exec client curl http://web:5000/ruta-inventada

# Capa 7 — nombre DNS que no existe (fuera de tu zona test.local)
docker exec client nslookup noexiste.inventado <IP_DE_DNS>
```

En el tcpdump de ARP verás `who-has <IP> tell <IP>` y **ninguna respuesta**
(`0806` = EtherType ARP): hubo pregunta, nadie respondió, la capa 3 no pudo
entregar.

Traduce a capas:

| Error | Capa que avisa | Protocolo | El usuario ve |
|-------|----------------|-----------|---------------|
| Puerto cerrado | 4 · Transporte | TCP RST | `Connection refused` |
| Ningún host responde | 2 · Enlace (ARP) → 3 · Red | ARP / ICMP timeout | `100% packet loss` |
| Nombre DNS no existe | 7 · Aplicación | DNS | `NXDOMAIN` |
| Certificado inválido | 6 · Presentación | TLS alert | error SSL |
| Recurso no existe | 7 · Aplicación | HTTP | `404 Not Found` |

**P3.** Elige **un** fallo, ejecútalo y escribe: qué capa respondió, con qué
comando lo confirmaste y qué mensaje viste.

## 6. Capas 5 y 6 (invisibles, pero en tu código)

| Capa | Función | En tu código |
|------|---------|--------------|
| 5 · Sesión | mantiene la conversación | cookie, session-id, JWT (Flask/Django) |
| 6 · Presentación | formato, cifrado, compresión | `Content-Type`, `Accept`, `Content-Encoding`, TLS |

```bash
# Formato negociado (capa 6) y cifrado (capa 6)
docker exec client curl -H "Accept: application/json" http://web:5000/ -v
docker exec client curl -kv https://google.com 2>&1 | grep -i "SSL\|TLS" | head
```

**P4.** Nombra un header de **capa 6** y uno de **capa 5** que verías en una app
real tuya.

## 7. (Opcional) Wireshark en el host

En Wireshark elige la interfaz del bridge `lab5-red` (`br-xxx`), dispara el
`curl`, y por colores identifica: HTTP (7), TCP (4), IP (3), ARP (2). Nota cómo
Wireshark muestra el PDU de cada capa (`[TCP segment]`, `[IP packet]`,
`[Ethernet frame]`).

## Preguntas de verificación

1. Las 7 capas OSI en orden y su función en una línea.
2. Las 4 capas TCP/IP y su correspondencia con OSI.
3. ¿Qué es un PDU y por qué cada capa tiene uno diferente?
4. En HTTPS, ¿dónde se insertan las capas 5 y 6? ¿Qué aportan sobre HTTP?
5. Un contenedor comparte el kernel del host: ¿qué capas son del host y cuáles
   del contenedor?
6. Tu app falla con `Connection refused`: ¿qué capa consultas primero y con qué
   comando?
7. ¿Por qué el modelo en capas facilita la vida de un desarrollador?

## Entregable

1. Escenario Docker levantado (web + client) — foto de `docker ps`.
2. Tabla capa→campo de la sección 3 con tu captura `-XX`.
3. Las 3 capturas comparadas: HTTP/TCP (SYN-ACK), DNS/UDP (sin conexión), ICMP.
4. Exploración del fallo elegido (P3) y respuestas P1-P4 + 3 preguntas de
   verificación a elección.

## Rúbrica

| Criterio | Puntos |
|----------|--------|
| Escenario Docker montado (web + client + dns) | 15 |
| Tabla de capas sobre la captura HTTP | 25 |
| Capturas TCP vs UDP vs ICMP + tabla comparativa | 20 |
| Fallas → capa que la detecta (P3) | 20 |
| Capas 5-6 + preguntas | 20 |
| **Total** | **100** |

## Limpieza

```bash
docker rm -f web client dns
docker network rm lab5-red
```