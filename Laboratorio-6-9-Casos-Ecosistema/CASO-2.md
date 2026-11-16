# CASO 2 — "La transacción" (capa transporte + red) — **guía guiada**

**API interna · TCP vs UDP · puertos · handshake · router entre 2 subredes**

> Réutiliza el portal del Caso 1. Agregás la **API interna** (`plantilla/`) en su
> propia subred `pagos`, y una **router** las comunica.

## Tus datos de escenario

| Dato | Valor |
|------|-------|
| Subred del portal (Caso 1) | `portal` → `192.168.<X>.0/26` · gateway `.1` |
| Subred nueva `pagos` | `192.168.<X>.64/26` · gateway `192.168.<X>.65` |
| API | `plantilla/` · puerto host `8088` |

> Las dos `/26` (`.0/26` y `.64/26`) **no se solapan** — Docker rechaza
> subredes que se pisan (si da `Pool overlaps`, revisá el cálculo).

## Paso 1 · Crear la subred y levantar la API

```bash
docker network create pagos --subnet 192.168.<X>.64/26 --gateway 192.168.<X>.65

docker build -t pagosya-api plantilla/api
# NET_ADMIN: para la ruta de vuelta (paso 3)
docker run -d --name pagosya-api --network pagos --cap-add NET_ADMIN \
  -p 8088:5000 pagosya-api
```

Probalo (evidencia):

```bash
curl -s http://localhost:8088/health        # almacenado: "memoria" (sin DB aún)
curl -s -X POST http://localhost:8088/pagos \
  -H 'Content-Type: application/json' -d '{"monto":99.99,"cliente":"EquipoX"}'
# → 201, id_pago 1 (aún NO persiste: espera la DB del Caso 3)
```

## Paso 2 · El router que une las dos subredes

```bash
docker run -d --name router-eco --cap-add=NET_ADMIN \
  --sysctl net.ipv4.ip_forward=1 --network portal alpine sleep 7200
docker network connect pagos router-eco
docker exec router-eco ip addr   # anotá la IP del router en cada subred
```

> **El router tiene 2 interfaces** (una por subred) y eso es lo que lo convierte
> en router:
>
> | Interfaz | Subred | IP del router |
> |----------|--------|---------------|
> | `eth0` (red `portal`) | `192.168.<X>.0/26` | `192.168.<X>.3` |
> | `eth1` (red `pagos`) | `192.168.<X>.64/26` | `192.168.<X>.67` |
>
> Verificá que el reenvío quedó activo (es lo que hace de router al router):
>
> ```bash
> docker exec router-eco cat /proc/sys/net/ipv4/ip_forward   # → 1
> ```

## Paso 3 · Rutas (¡en ambos sentidos!)

> La API necesita la ruta de **vuelta**: sin ella el ping se pierde aunque la ida
> esté bien (el host no devuelve el tráfico).

```bash
docker exec tienda-web sh -c "apk add --no-cache iputils-ping iproute2 >/dev/null 2>&1"

# (a) SIN rutas → ping FALLA
docker exec tienda-web ping -c 1 <IP_API>

# (b) ruta de ida (portal → pagos)
docker exec tienda-web ip route add 192.168.<X>.64/26 via <IP_ROUTER_EN_PORTAL>
# (c) ruta de vuelta (API → portal)
docker exec pagosya-api ip route add 192.168.<X>.0/26 via <IP_ROUTER_EN_PAGOS>

# (d) ping RESPONDE
docker exec tienda-web ping -c 3 <IP_API>
# (e) traceroute muestra el salto por el router
docker exec tienda-web sh -c "apk add --no-cache traceroute >/dev/null 2>&1; \
  traceroute -m 5 <IP_API>"
```

Guardá las capturas de (a), (d) y (e).

### (f) La transacción que cruza el router  ← evidencia clave del caso

El objetivo del Caso 2: que el **portal (subred `portal`) le cobre a la API
(subred `pagos`)**. Ese pedido tiene que **cruzar el router**:

```bash
# desde el portal, por IP interna de la API (NO por localhost:8088)
docker exec tienda-web sh -c "apk add --no-cache curl >/dev/null 2>&1"
docker exec tienda-web curl -s -w '\nHTTP=%{http_code}\n' \
  -X POST http://<IP_API>:5000/pagos \
  -H 'Content-Type: application/json' -d '{"monto":150.50,"cliente":"EquipoX"}'
# → {"...","estado":"registrado","id_pago":1,...}
# → HTTP=201
```

> **Ojo:** `http://localhost:8088` (lo que usaste en el Paso 1) recorre el
> `docker-proxy` del host y **no pasa por el router**. Para demostrar el
> enrutamiento tenés que llamar a la **IP de la API dentro de la red**.

## Paso 4 · Handshake TCP y puertos

```bash
# Terminal A: capturar
docker exec pagosya-api tcpdump -i eth0 -nn port 5000 -c 10
# Terminal B: pedirle a la API
curl -s http://localhost:8088/ > /dev/null
```

En la captura marcá **SYN (`[S]`) → SYN-ACK (`[S.]`) → ACK (`[.]`)** y los
puertos origen/destino. Además:

```bash
netstat -tlnp | grep 8088    # en el HOST: el puerto publicado (docker-proxy)

docker exec pagosya-api ss -tlnp | grep 5000   # DENTRO: el puerto real de Flask
# LISTEN 0 128 0.0.0.0:5000 0.0.0.0:*  users:(("python",pid=1,fd=3))
```

## Paso 5 · TCP vs UDP y latencia

```bash
# en la API, simulá 100ms de latencia en su interfaz
docker exec pagosya-api tc qdisc add dev eth0 root netem delay 100ms
docker exec pagosya-api ping -c 4 192.168.<X>.65   # RTT ≈ 100ms
docker exec pagosya-api tc qdisc del dev eth0 root

# (variante: pérdida con `tc qdisc ... netem loss 30%`)
```

> La imagen de la API ya trae `ping`, `tc`, `traceroute` y `tcpdump` (los
> instala su `Dockerfile`), así que no necesitás `apk add` en este paso.

### Servidor UDP (sin conexión, no hay handshake)

Levantá un servidor UDP mínimo **dentro de la API** y comprobá que responde
**sin ningún SYN/ACK**:

```bash
docker exec -d pagosya-api sh -c 'cat > /tmp/udp.py << "PY"
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 5001))
print("UDP server en 5001", flush=True)
while True:
    data, addr = s.recvfrom(1024)
    print("recibido:", data.decode(), "de", addr, flush=True)
    s.sendto(b"respuesta-udp: " + data, addr)
PY
python3 /tmp/udp.py > /tmp/udp.log 2>&1'
sleep 2

# cliente UDP: envía "hola" y recibe la respuesta
docker exec pagosya-api python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.settimeout(3)
s.sendto(b'hola', ('127.0.0.1', 5001))
print('resp:', s.recvfrom(1024)[0].decode())
"
# → resp: respuesta-udp: hola
```

**Capturá los dos protocolos y compará.** Para UDP:

```bash
docker exec pagosya-api sh -c 'timeout 6 tcpdump -i lo -nn -S "udp port 5001" -c 3 \
  > /tmp/udp-cap.txt 2>&1 &
sleep 2
python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.settimeout(3)
s.sendto(b\"hola\", (\"127.0.0.1\", 5001)); s.recvfrom(1024)
"
wait'
docker exec pagosya-api cat /tmp/udp-cap.txt
# → solo 2 líneas: "UDP, length 4" y "UDP, length 19"   (¡NADA de Flags [S]!)
```

**Conclusión esperada:** con TCP la conexión se establece con 3 paquetes
(`[S]` → `[S.]` → `[.]`) **antes** de los datos; con UDP los datos viajan de
inmediato, sin handshake, sin confirmar recepción y sin reintentos. Por eso UDP
se usa para streaming/DNS y TCP para HTTP/pagos.

## Entregables del Caso 2 (documento)

1. `docker network ls` + `inspect` de `portal` y `pagos` (sin solape).
2. Ping **sin ruta** (falla) → **con rutas** (0%) + `traceroute`.
3. **La transacción portal → API cruzando el router** (`HTTP=201`).
4. Captura del **handshake** con SYN/SYN-ACK/ACK y puertos anotados.
5. `netstat`/`ss` con el `8088` (host) y el `5000` (API).
6. Comparación **TCP vs UDP** (servidor UDP + `tc`) y conclusión.
7. **Diagrama del Caso 2** (2 subredes + router + flujo del pedido).
8. Respuestas a las preguntas.

## Preguntas de verificación

1. Al cruzar el router: ¿qué cambia y qué no en el paquete? (MAC, IP, TTL)
2. ¿Por qué la API necesita la ruta de **vuelta**?
3. En el handshake, ¿qué puerto es origen y cuál destino? ¿Quién los decide?
4. Con tu simulación de pérdida: ¿qué hace TCP que UDP no haga?
5. ¿Dos `/26` alcanzan para aislar la base de datos del usuario? (gancho al Caso 3)