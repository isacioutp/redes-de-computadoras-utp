# DEMO DOCENTE — "El viaje de un mensaje" (60 minutos)

Siguiente clase · 1 hora · Caso N.º 7-9
**Objetivo**: que los estudiantes **vean** en una sola demostración cómo un mensaje
recorre las tres capas (red → transporte → aplicación) **a través de Docker**,
que **entiendan que cada tópico del curso se demuestra con una prueba**, y al
finalizar se les entreguen las **8 fichas de caso** para presentar la siguiente
clase.

> ## Antes de la clase (30 min previos)
>
> 1. Ejecutar `bash demo/run-demo.sh` (levanta todo el stack).
> 2. Tener **3 terminales abiertas** en el folder `demo/`.
> 3. Abrir/proyectar el diagrama del README.
> 4. Tener las **8 fichas de caso** (`casos/Caso-01.md` ... `Caso-08.md`)
>    listas para sortear y entregar en el minuto 52.

---

## Minuto 0–5 · La historia del mensaje

Proyecta el diagrama. Cuenta la historia en 2 frases:

> "Cuando un usuario escribe `http://app` en el navegador, el mensaje **no puede
> llegar solo**: primero necesita una **red** que lo enrute (capa de red), luego un
> **canal de transporte** que lo entregue entero y ordenado (capa de transporte), y
> solo al final alguien que **entienda su lenguaje** y responda (capa de aplicación).
> Hoy vamos a verlo vivo: un mensaje de punta a punta."

👋 **Pregunta a la clase**: *"¿Qué capa creen que falla si el ping entre dos redes
falla pero las máquinas están encendidas?"* (respuesta esperada: red/ruteo → error TTL).

## Minuto 5–12 · Capa de red: subredes VLSM

Muestra la red construida. Aclarar en voz alta: la demo usa el mínimo (2
subredes: una "pública" y una "interna"); **cada caso exige 3 subredes**, una
por capa (`sub-web` portal, `sub-api` API, `sub-db` DB aislada):

```bash
# Terminal 1
docker network ls | grep demo
docker network inspect demo-lab79_public-front --format '{{range .IPAM.Config}}{{.Subnet}} gw {{.Gateway}}{{end}}'
docker network inspect demo-lab79_back          --format '{{range .IPAM.Config}}{{.Subnet}} gw {{.Gateway}}{{end}}'
```

Explica con las 2 líneas del diagrama: `192.168.60.0/27` (pública: `web`, `api`,
`dns`) y `192.168.60.32/27` (interna: `api`, `db`). Señala que **un contenedor
(`api`) tiene 2 IPs**: una en cada subred → es un **router** potencial.

Muestra las IPs:

```bash
for c in demo-router demo-web demo-api demo-db; do
  echo "$c -> $(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{end}}' $c)"
done
```

**Momento clave — el fallo.** Pide a la clase que prediga antes de ejecutar:

```bash
docker exec demo-web ping -c 1 192.168.60.35     # IP interna del API → FALLA
```

> ⌛ Toma 20 segundos aquí para que **la clase** explique por qué falla (no hay ruta;
> `Destination Host Unreachable`).

## Minuto 12–20 · Capa de red: router + rutas + traceroute

```bash
docker exec demo-router ip addr show | grep "inet 172"        # 1 IP por subred
docker exec demo-web ip route add 192.168.60.32/27 via 192.168.60.2   # ruta via router
docker exec demo-web ping -c 2 192.168.60.35                   # → AHORA SÍ responde
docker exec demo-web traceroute -n -m 5 192.168.60.35          # 2 saltos: web → router → api
```

**Explica**: la **tabla de enrutamiento** decide la salida, el **TTL** decrece en cada
salto y es la base del traceroute (y del mensaje `time exceeded` de ICMP).

## Minuto 20–32 · Capa de transporte: TCP handshake y puertos

Levanta la pestaña 2 (captura) y la pestaña 3 (petición):

```bash
# Terminal 2: captura en vivo (mete port 5000)
docker exec -it demo-api tcpdump -i eth0 -nn -c 10 port 5000
```

```bash
# Terminal 3: dispara la petición
curl -s http://192.168.60.11:5000/ | python3 -m json.tool
```

Marca con el puntero los paquetes:
1. `SYN` (cliente → servidor) — quiero hablar
2. `SYN-ACK` (servidor → cliente) — ok, hablemos
3. `ACK` (cliente → servidor) — acuerdo

**Explica los puertos**: el `5000` es fijo (servidor); el origen es **dinámico**
(49152–65535) y cambia en cada conexión → por eso decimos "conversación por
puertos, no por IP".

> ⌛ Si el tiempo aprieta: menciona UDP con el RTT del caso y sigue; la comparación
> detallada queda para tu caso asignado (ver ficha en `casos/`).

## Minuto 32–45 · Capa de aplicación: HTTP, DNS y HTTPS

```bash
# HTTP: dialogamos con el navegador "mini" (curl) y leemos códigos
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8081/
curl -v http://localhost:8081/ 2>&1 | head -20        # request + response headers

# DNS: nuestro propio servidor de nombres traduce
dig app.lab @localhost -p 8053 +short                 # → 192.168.60.10 (web)
dig google.com +short trendia                          # → IP pública de Internet

# HTTPS: certificado autofirmado
curl -k https://localhost:8443/
```

Conecta con el diagrama: el navegador pidió a **DNS** la IP de `app` **(aplicación)**
y luego la conversación viajó por el canal de transporte **(red/transporte)**.

## Minuto 45–52 · El momento "aha": el mensaje completo

Vuelve a la pestaña 2 (captura del API) y ahora dispara desde el **host** hacia la
**web**:

```bash
# Terminal 2
docker exec -it demo-web ash -c "apk add -q iproute2 tcpdump; tcpdump -i eth0 -nn port 80"
```

```bash
# Terminal 3
curl -s http://localhost:8081/
```

Muestra en la captura **dos capas en el mismo paquete**: handshake TCP (transporte)
y `GET / HTTP/1.1` (aplicación), viajando por la subred (red). Señala el **header de
la trama** (Ethernet/MAC, Lab 6) al inicio de la línea.

**Cierre visual**: repite el diagrama y enumera — "este mensaje pasó por: DNS →
handshake TCP → IP → ruta → trama Ethernet → y volvió. Eso es todo el lab."

## Minuto 52–60 · Entrega de las 8 fichas de caso

1. Sortea o asigna **una ficha de caso por equipo** (`casos/Caso-01.md` ...
   `Caso-08.md`). Cada ficha tiene: empresa, tabla VLSM propia, giro particular
   y los mismos 9 pruebas que acabas de ver en la demo.
2. Lee en 60 segundos la consigna: el mismo camino que acabas de demostrar
   (subredes → router → TCP → HTTP/DNS) pero con **sus propios números** y su
   empresa.
3. Explica la **evaluación en 3 partes**: Documento (40) + Presentación/Demo
   (30) + Prueba funcional en vivo (30). La tabla de pruebas es la misma para
   los 8 casos y **cada prueba demuestra un tópico** del curso (ver la tabla
   "tópico → prueba" de `CASO.md` sección 4); la demo que acaban de ver es
   exactamente lo que cada equipo presentará con sus números.
4. Reglas: **equipos de 4-6**, presentación **máx. 10 min**, **la siguiente
   clase** se presentan todos los casos. La mini-app debe quedar funcional
   (POST/GET).
5. Señala la **plantilla** (`plantilla/`) como punto de partida: API Flask +
   Postgres + portal HTML, lista para levantar.
6. Resuelve dudas. Anota en la pizarra: **VLSM (tabla), ping fallido→rutas,
   handshake tcpdump, HTTPS + DNS, DB aislada.**

---

## Checklist de la demo (marca lo que salió)

- [ ] Stack levantado (`bash demo/run-demo.sh`)
- [ ] Subredes mostradas (`docker network inspect`)
- [ ] Ping fallido explicado por la clase
- [ ] Ruta agregada + ping OK + traceroute (2 saltos)
- [ ] Handshake SYN/SYN-ACK/ACK capturado en vivo
- [ ] HTTP + códigos de estado
- [ ] DNS `dig app.lab` respondiendo
- [ ] HTTPS `curl -k`
- [ ] Mensaje completo (handshake + GET en una captura)
- [ ] **8 fichas de caso** sorteadas/entregadas (`casos/`) y fecha confirmada
      (la siguiente clase)