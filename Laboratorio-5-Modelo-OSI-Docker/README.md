# Laboratorio N.º 5 — Modelo OSI y TCP/IP con Docker

Tema: modelo OSI / TCP-IP · Semanas 4-5 · Unidad II
Combinado con el Lab 4 (análisis de trama); se resuelve en una clase.

> **Idea en 1 línea**: en una sola petición HTTP ves **todas las capas** del OSI
> en vivo, comparas TCP vs UDP vs ICMP, y cada falla te dice **qué capa la
> detectó**. De paso, exploras Docker por primera vez: imagen, contenedor y red.

## 0. Docker desde cero (si es tu primera vez)

### ¿Qué es Docker?

- **Imagen**: una *receta* congelada (`nginx:alpine`, `python:3.11-slim`). No
  "corre", es un archivo de solo lectura con todo lo necesario (Linux mínimo +
  programas).
- **Contenedor**: un proceso que corre a partir de una imagen, **como un mini-PC
  con su propia tarjeta de red, su propia IP y su propio disco**. No es una
  máquina virtual: comparte el kernel y el hardware de tu computadora.

Piénsalo como: **imagen = plantilla / ISO**, **contenedor = PC encendido**.

### Por qué Docker es perfecto para ver el OSI

Cada contenedor tiene su propio mundo de capas:

| Lo que tiene | Capa OSI |
|--------------|----------|
| su dirección **MAC** | 2 · Enlace |
| su **eth0** (tarjeta de red virtual) y su **IP** | 3 · Red |
| su **puerta de enlace** dentro de la red | 3 · Red |
| su **DNS** (docker responde nombres como `web`) | 7 · Aplicación |

Tú decides qué contenedores "hablan" entre sí **creando redes**: la red es un
segmento aislado (capa 2-3), por eso al ver las capas, Docker es tu juguete.

### Los 7 comandos de este lab (son los de siempre)

| Comando | Qué hace |
|---------|----------|
| `docker network create <red>` | crea una red aislada entre contenedores |
| `docker run -d --name <n> --network <red> <imagen>` | levanta un contenedor conectado a esa red |
| `-p 8080:80` (flag de `run`) | publica el puerto 80 del contenedor en el 8080 de tu PC |
| `docker exec <n> <comando>` | ejecuta un comando **dentro** del contenedor |
| `docker ps` | lista los contenedores encendidos |
| `docker inspect <n>` | datos técnicos del contenedor (IP, red…) |
| `docker rm -f <n>` · `docker network rm <red>` | limpieza |

### Comprueba que Docker funcione

```bash
docker version        # o: docker info
# en Linux, si no tienes permisos: sudo usermod -aG docker $USER (cerrar sesión),
# o ejecuta los comandos con sudo delante.
```

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
6 Presentación      ┤ →  4 Aplicación          HTTP, DNS, SMTP, Flask
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

## 2. Escenario (tu primer Docker real)

Vas a levantar **2 contenedores** en una red propia: un servidor web
(`web`) y un cliente de exploración (`client`).

```bash
# 1) Crea una red aislada: los contenedores de la red se ven entre sí por
#    nombre; los de afuera, no.
docker network create lab5-red

# 2) Servidor web nginx:
#    -d              → fondo (no te bloquea la terminal)
#    --name web      → nombre del contenedor
#    --network lab5-red → conectado a tu red
#    -p 8080:80      → puerto 80 del contenedor se ve en tu PC como 8080
docker run -d --name web --network lab5-red -p 8080:80 nginx:alpine

# 3) Cliente: un Linux mínimo para explorar la red desde adentro.
#    sleep 3600 → se queda encendido una hora mientras exploras.
docker run -d --name client --network lab5-red alpine sleep 3600

# 4) El cliente nace sin herramientas; se las instalas con apk (Alpine):
#    curl (capa 7) · tcpdump (capas 2-4) · nslookup/bind-tools (capa 7 DNS)
docker exec client apk add --no-cache curl tcpdump bind-tools

# 5) Prueba rápida: el cliente 'ping' al web POR NOMBRE.
#    docker resuelve 'web' por DNS (capa 7) → lo traduce a IP (capa 3)
#    → ICMP de ida y vuelta.
docker exec client ping -c 1 web

# 6) ¿Qué IP le tocó a web? La anotas, la usarás en las secciones 4 y 5.
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web
```

> nginx arranca al instante (mucho más rápido que una imagen con Python).
> También puedes abrir tu navegador en http://localhost:8080: ese `8080` es el
> puerto `-p` del contenedor publicado en tu computadora.

## 3. Una petición HTTP = TODAS las capas

**Terminal A** (captura en el servidor; `apk` instala con el instalador de
Alpine, `eth0` es la tarjeta de red del contenedor):
```bash
docker exec web sh -c "apk add --no-cache tcpdump && tcpdump -i eth0 -nn -XX port 80"
```
**Terminal B** (dispara la petición):
```bash
docker exec client curl http://web/
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
| … | puerto origen / destino (TCP, destino `80`) | 4 · Transporte | Segmento |
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
# Servidor DNS propio que traduce test.local → IP de web (la de la sección 2)
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
docker exec client curl http://web/ruta-inventada

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
# Formato negociado (capa 6) — fíjate en los headers (Accept / Content-Type)
docker exec client curl -H "Accept: application/json" http://web/ -v
# Cifrado (capa 6) — TLS handshake contra un sitio HTTPS
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
5. ¿Qué diferencia hay entre una **imagen** y un **contenedor** en Docker?
6. Un contenedor comparte el kernel del host: ¿qué capas son del host y cuáles
   del contenedor?
7. Tu app falla con `Connection refused`: ¿qué capa consultas primero y con qué
   comando?
8. ¿Por qué el modelo en capas facilita la vida de un desarrollador?

## Entregable

1. Escenario Docker levantado (web + client) — foto de `docker ps`.
2. Tabla capa→campo de la sección 3 con tu captura `-XX`.
3. Las 3 capturas comparadas: HTTP/TCP (SYN-ACK), DNS/UDP (sin conexión), ICMP.
4. Exploración del fallo elegido (P3) y respuestas P1-P4 + 3 preguntas de
   verificación a elección.

## Rúbrica

| Criterio | Puntos |
|----------|--------|
| Escenario Docker explorado (web + client + dns) | 15 |
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