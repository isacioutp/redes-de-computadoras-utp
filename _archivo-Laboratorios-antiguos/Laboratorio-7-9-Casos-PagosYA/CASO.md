# CASO — "PagosYA": el viaje de un mensaje por las tres capas

Laboratorio N.º 7-9 (reemplaza los antiguos Labs N.º 7, 8 y 9) · Trabajo en
**equipos de 4-6** (se recomienda el mismo equipo del Proyecto Semestral) ·
**Se presenta con demo funcional en clase**.

> **Este es el caso base / de referencia.** Cada equipo recibe **una de las 8
> fichas** de [casos/](casos/) (`Caso-01.md` .. `Caso-08.md`): misma
> metodología, empresa, parámetros y "giro" propios. Este archivo describe el
> **procedimiento común** a los 8 (el ejemplo aquí es la demo docente).

> **Evaluación simple**: documento + presentación/demo + prueba funcional en
> vivo. Detalle en [EVALUACION.md](EVALUACION.md).

---

## 1. Contexto

La fintech **PagosYA** te contrata para desplegar su plataforma de pagos. Es
**tu responsabilidad** la red completa que la hace funcionar: que cuando un
usuario escriba `https://pagosya.local` en el navegador, el mensaje **llegue y
vuelva** atravesando las tres capas de la red.

**Solo tienes que demostrar una cosa**: que el mensaje **viaja completo** de
punta a punta (ver sección 4 → *La prueba*).

### Qué se necesita — **3 segmentos de red (uno por capa)**

| Segmento | Función | Hosts |
|----------|---------|-------|
| Portal web | Frontend que atiende al usuario (subred pública) | 8 |
| API de pagos | Backend que procesa transacciones (subred de aplicación) | 30 |
| Base de datos | Almacena transacciones — **sensible, aislada** | 10 |

- Red base: **`192.168.88.0/24`** — debe partirse en **3 subredes** (VLSM).
- Reglas de seguridad de PagosYA:
  - La **base de datos NO se expone** al host ni a internet.
  - **Cada capa de la app vive en su propia subred**: no todo en una sola.

> **Todo se construye y se demuestra con Docker.** Tu entorno son contenedores y
> redes Docker; los conceptos del lab los vas a **ver** ejecutando las pruebas de
> la sección 4 (cada tópico → su prueba).

---

## 2. Qué debes construir

### La app: PagosYA (una aplicación simple pero FUNCIONAL)

No es solo infraestructura: la red debe sostener una **mini-aplicación de 3
capas que funcione de verdad** y registrar un pago.

```
Navegador → [portal  nginx :8081]  →  [API  Flask :8088]  →  [DB Postgres]
             sub-web (pública)         sub-api (app)            sub-db (aislada)
                       └──────── por el router ─────────┘
```

- **3 subredes, una por capa**: `sub-web` (portal), `sub-api` (API) y `sub-db`
  (DB, sin puerto al host).
- La **API tiene "doble casa"**: una cara en `sub-api` (para el portal / el
  usuario) y una cara en `sub-db` (la única que toca la base de datos).
- El **router** une las subredes: sin él (sin rutas) el portal no llega ni a la
  API ni a la DB — lo demuestras en las pruebas 1-3.

El flujo real de "un pago": el usuario (o `curl`) llama a la API, esta escribe
en la base de datos **a través de la subred interna**, y la respuesta vuelve.
Entrega la plantilla lista en `plantilla/`:

| Archivo | Contenido |
|---------|-----------|
| `plantilla/api/` | API Flask: `POST /pagos` y `GET /pagos` (guardan en Postgres) |
| `plantilla/init.sql` | Crea la tabla `pagos` (se monta en el Postgres) |
| `plantilla/web/index.html` | Portal simple con formulario que llama a la API |

> Tu trabajo real es la **red y las configuraciones** (subredes, router, rutas,
> puertos, DNS, HTTPS, aislamiento). La app es el instrumento que demuestra que
> la red funciona: si la red está mal, el pago **no** se registra.

Prueba funcional mínima de la app (parte de la demo):

```bash
curl -s -X POST http://localhost:8088/pagos -H 'Content-Type: application/json' \
  -d '{"monto": 99.99, "cliente": "Prueba"}'     # → 201 {"id_pago":1}
curl -s http://localhost:8088/pagos               # → listado que incluye el pago
```

### A. Capa de red — subredes, router y diagnóstico

1. Diseña el **VLSM** de `192.168.88.0/24` (de mayor a menor) y completa:

   | Segmento | Prefijo | Subred | Broadcast | Gateway | Hosts útiles |
   |----------|---------|--------|-----------|---------|--------------|
   | API de pagos | `/27` | | | | 30 |
   | Portal web | `/28` | | | | 14 |
   | Base de datos | `/28` | | | | 14 |

2. **Crea las 3 subredes reales** con Docker (`docker network create`) con esos
   rangos y levanta portal, api y db.
3. Añade un **router contenedor** que conecte las subredes y haz que
   `192.168.88.X` (api y db) sea alcanzable desde otra subred solo cargando
   **rutas**. Debes mostrar: ping que **falla** → ruta agregada → ping que
   **responde** → `traceroute` mostrando el salto por el router (TTL).

### B. Capa de transporte — TCP, handshake y puertos

4. Levanta un servidor TCP (Flask, `python:3.11-slim`) como **API de pagos**
   dentro de tu red y **mapea** un puerto al host (p. ej. `-p 8088:5000`).
5. Captura el **three-way handshake** con `tcpdump -nn port 5000` al hacer un
   `curl`. Marca `SYN`, `SYN-ACK`, `ACK` y los **puertos origen/destino**.
6. (Recomendado) Aplica **100 ms de latencia** con `tc netem` y compara
   `time curl` antes/después. Explica qué pasaría con UDP (no confiable).

### C. Capa de aplicación — HTTP/HTTPS, DNS y aislamiento

7. Sirve el **portal** con `nginx` por HTTP y **HTTPS autofirmado**
   (`openssl` + `curl -k`, puerto 8443). Verifica códigos 200 y 404.
8. Monta tu **DNS propio** (`jpillora/dnsmasq`) que traduzca
   `pagosya.local → <IP del portal>` y consúltalo con `dig`.
9. Deja la **base de datos aislada** en su subred (sin puerto al host).
   Confirma con `docker port <db>` que no publica nada.

**Hints (comandos clave de los labs 7-9)**:

```bash
# 1) Las 3 subredes de tu VLSM (una por capa; ajusta a tu tabla)
docker network create sub-api  --subnet 192.168.88.0/27  --gateway 192.168.88.1
docker network create sub-web  --subnet 192.168.88.32/28 --gateway 192.168.88.33
docker network create sub-db   --subnet 192.168.88.48/28 --gateway 192.168.88.49

# 2) Router que une las 3 (con una interfaz en cada subred) + rutas
docker run -d --name router --cap-add=NET_ADMIN \
  --sysctl net.ipv4.ip_forward=1 --network sub-web alpine sleep 3600
docker network connect sub-api router
docker network connect sub-db router
sudo sysctl -w net.ipv4.ip_forward=1            # reenvío en el host
docker exec router ip addr                        # IP del router en cada subred
# Rutas en el portal para alcanzar api y db vía router:
docker exec portal ip route add 192.168.88.0/27  via <IP_ROUTER_SUB_WEB>
docker exec portal ip route add 192.168.88.48/28 via <IP_ROUTER_SUB_WEB>

# 3) LA APP (3 capas): DB aislada + API "doble casa" + portal
docker run -d --name pagosya-db --network sub-db \
  -e POSTGRES_USER=pagosya -e POSTGRES_PASSWORD=pagosya123 -e POSTGRES_DB=pagosya \
  -v $(pwd)/plantilla/init.sql:/docker-entrypoint-initdb.d/init.sql:ro \
  postgres:15-alpine

docker build -t pagosya-api plantilla/api
docker run -d --name pagosya-api --network sub-api \
  -p 8088:5000 -e DB_HOST=pagosya-db \
  -e DB_USER=pagosya -e DB_PASS=pagosya123 pagosya-api
docker network connect sub-db pagosya-api         # su cara privada: la única que toca la DB

mkdir -p web && cp plantilla/web/index.html web/
docker run -d --name portal --network sub-web -p 8081:80 \
  -v $(pwd)/web:/usr/share/nginx/html:ro nginx:alpine

# 4) Handshake sobre la app (transporte)
docker exec pagosya-api tcpdump -i eth0 -nn -c 10 port 5000   # terminal A
curl -s http://localhost:8088/                                  # terminal B

# 5) HTTPS + DNS (aplicación)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout privkey.pem -out server.crt \
  -subj "/C=PA/ST=Panama/L=CD/L=UTP/O=Redes/CN=pagosya.local"
docker run -d --name dns --network sub-web -p 8053:53/udp \
  jpillora/dnsmasq --address=/pagosya.local/<IP_PORTAL>

# 6) Prueba de la app (debe registrar y listar el pago)
curl -s -X POST http://localhost:8088/pagos -H 'Content-Type: application/json' -d '{"monto":99.99,"cliente":"Prueba"}'
curl -s http://localhost:8088/pagos
```

---

## 3. El documento (entregable escrito)

Un informe claro (PDF o Markdown) que contenga:

1. **Diagrama** de la red (Packet Tracer, draw.io o a mano): subredes, IPs,
   router, servicios y puertos.
2. **Tabla VLSM** completa + justificación (por qué `/30` en el enlace y `/27`
   en la API).
3. **Tabla de servicios y puertos** (servicio, puerto host, puerto interno,
   protocolo TCP/UDP).
4. **Capturas** con anotaciones: ping fallido→exitoso, `traceroute`, handshake
   (`SYN/SYN-ACK/ACK`), `time curl` con netem, `dig pagosya.local`, `curl -k`.
5. Respuesta breve a **3 preguntas guía**:
   1. ¿Qué capa "resolvió" el ping fallido y cómo?
   2. ¿Por qué el puerto origen del cliente cambia en cada conexión TCP?
   3. ¿Por qué la base de datos no se expone al host?

---

## 4. La prueba funcional: **demuestra los conceptos con Docker**

Los **tópicos** de los antiguos Labs 7-9 **no se explican con diapositivas**: se
**verifican con una prueba** ejecutada sobre tu red Docker. **La presentación ES
la prueba.** Cada tópico → su prueba:

| Tópico (concepto) | Prueba en Docker (en vivo) | Qué demuestra |
|---|---|---|
| Subredes / VLSM | `docker network create --subnet/--gateway` + `docker network inspect` | Rangos IP reales: red, broadcast, hosts útiles |
| ICMP + enrutamiento | `ping` sin ruta → FALLA · con ruta → 0 % pérdida | Solo llega lo que **sabe** qué ruta tomar |
| Routers / TTL | `traceroute` entre subredes | El paquete salta router por router (TTL decrece) |
| TCP (confiabilidad) | `tcpdump -nn port` al hacer un `curl` | SYN → SYN-ACK → ACK antes de los datos |
| Puertos | destino fijo `:5000` vs origen alto y variable | La conversación se identifica por puerto |
| Latencia / congestión | `tc netem delay 100ms` + `time curl` antes/después | El RTT impacta la app (y por qué UDP no asegura) |
| HTTP | `curl -w '%{http_code}'` al portal | Códigos de estado: el servicio responde |
| HTTPS | `curl -k https://…` (autofirmado) | La conversación viaja cifrada (TLS) |
| DNS | `dig pagosya.local @<tu-dns> +short` | El nombre resuelve a una IP antes de conectar |
| Aislamiento del dato sensible | `docker port <db>` → vacío | La DB no se expone (seguridad del caso) |
| Aplicación real (3 capas) | `POST /pagos` → 201 y `GET /pagos` → listado | El mensaje cruza red+transporte+aplicación y **persiste** |

En la presentación ejecutas **en vivo** el checklist de abajo (es exactamente la
tabla anterior, con la evidencia esperada por tópico):

| # | Tópico | Prueba | Salida esperada |
|---|--------|--------|-----------------|
| 1 | ICMP + enrutamiento | `ping` entre subredes **sin** ruta | FALLA (`Destination Host Unreachable`) |
| 2 | ICMP + enrutamiento | `ping` entre subredes **con** ruta | 0 % pérdida |
| 3 | Routers / TTL | `traceroute` entre subredes | 2-3 saltos (intermediario = router/es) |
| 4 | Aplicación (HTTP) | `curl` a tu API | HTTP 200 + JSON |
| 5 | TCP (handshake) | `tcpdump` de un `curl` | paquetes `SYN`, `SYN-ACK`, `ACK` |
| 6 | DNS | `dig pagosya.local` | la IP de tu portal |
| 7 | HTTPS | `curl -k https://localhost:8443/` | HTML (HTTP 200) |
| 8 | Aislamiento / seguridad | `docker port <db>` | vacío (DB NO publicada) |
| 9 | Aplicación real (3 capas) | `POST /pagos` y luego `GET /pagos` | 201 `{id_pago}` y el pago listado (persistió en la DB) |

> Cada prueba debe **narrar el tópico** que está viendo: al ejecutar la prueba 4,
> di "aquí el mensaje cruzó las subredes por el router (red), hizo el handshake
> TCP (transporte) y el servidor respondió (aplicación)".

---

## 5. Reglas y plazos

- **Equipos de 4-6 personas** (una entrega por equipo; se recomienda el mismo
  equipo del Proyecto Semestral).
- **Cada equipo recibe una ficha de caso** (`casos/Caso-01.md` .. `Caso-08.md`)
  sorteada en la clase de la demo; se **presenta la siguiente clase**.
- Presentación **máx. 10 minutos** + 3 min de preguntas.
- Si no se alcanza a presentar, pasa a la siguiente (sorteo), con penalidad de
  entrega tarde (−2 pts/día, regla del curso).
- Está prohibido: exponer la base de datos, copiar la solución de otro equipo
  o presentar capturas sin el sistema funcionando.

👉 **Calificación**: ver [EVALUACION.md](EVALUACION.md).