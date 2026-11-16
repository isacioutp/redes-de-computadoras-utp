# CASO 3 — "Los datos": el cierre (VLSM + DB aislada + DNS + monitoreo) — **guía guiada**

**VLSM completo · base de datos aislada · DNS interno · integración portal→API→DB**

> Cierres el ecosistema: la base completa se re-particiona con **VLSM**, la
> **DB queda aislada** (sin puerto al host) y se **muestrea** el tráfico hasta
> ella. La evidencia: **una transacción nace en el portal, cruza las subredes y
> persiste en la DB**.

## La partición VLSM (calculada por tu equipo)

Sobre tu base `192.168.<X>.0/24`, cada servicio necesita un número de hosts;
se parte **de mayor a menor** tomando bloques **consecutivos**:

| Subred | Servicio | Hosts | Prefijo sugerido |
|--------|----------|------:|------------------|
| 1 | API `pagos` | 30 | `/26` |
| 2 | Portal `portal` | 8 | `/28` |
| 3 | DB `datos` | 8 | `/28` |
| 4 | Admin / monitoreo | 5 | `/29` |
| 5 | Enlace routers (diagrama) | 2 | `/30` |

> Completá (en tu documento) para cada bloque: **subred, broadcast, gateway y
> hosts útiles** — verificá cada uno con `ipcalc`. El gateway de cada subred va
> en el **primer host útil** de su bloque.
>
> *Ejemplo de arranque* (Grupo 1): `pagos` en `.0/26` → gateway `.1`; `portal`
> en `.64/28` → gateway `.65`; `datos` en `.80/28` → gateway `.81`; `admin` en
> `.96/29` → gateway `.97`; enlace en `.104/30`.

## Paso 1 · Rediseño: redes y contenedores del esquema VLSM

> El Caso 3 cambia los prefijos de los Casos 1-2 → se eliminan y se reconstruyen.

```bash
docker rm -f tienda-web pagosya-api router-eco eco-dns datosya-db 2>/dev/null || true
docker network rm portal pagos 2>/dev/null || true

docker network create pagos  --subnet 192.168.<X>.0/26  --gateway 192.168.<X>.1
docker network create portal --subnet 192.168.<X>.64/28 --gateway 192.168.<X>.65
docker network create datos  --subnet 192.168.<X>.80/28 --gateway 192.168.<X>.81
docker network create admin  --subnet 192.168.<X>.96/29 --gateway 192.168.<X>.97

# portal (recreado en la nueva subred)
printf '<h1>Mi empresa</h1>\n' > web/index.html
docker run -d --name tienda-web --network portal --cap-add NET_ADMIN \
  -p 8081:80 -v "$(pwd)/web:/usr/share/nginx/html:ro" nginx:alpine
```

## Paso 2 · Router multi-cara

```bash
docker run -d --name router-eco --cap-add=NET_ADMIN \
  --sysctl net.ipv4.ip_forward=1 --network pagos alpine sleep 7200
docker network connect portal router-eco
docker network connect datos  router-eco
docker network connect admin  router-eco
sudo sysctl -w net.ipv4.ip_forward=1
docker exec router-eco ip addr   # anotá la IP del router en cada subred
```

## Paso 3 · Base de datos AISLADA + API "doble casa"

```bash
docker run -d --name datosya-db --network datos \
  -e POSTGRES_USER=pagosya -e POSTGRES_PASSWORD=pagosya123 -e POSTGRES_DB=pagosya \
  -v "$(pwd)/plantilla/init.sql:/docker-entrypoint-initdb.d/init.sql:ro" \
  postgres:15-alpine

docker port datosya-db        # → debe estar VACÍO (la DB NO tiene -p: aislada)

docker build -t pagosya-api plantilla/api
docker run -d --name pagosya-api --network pagos --cap-add NET_ADMIN -p 8088:5000 \
  -e DB_HOST=datosya-db -e DB_USER=pagosya -e DB_PASS=pagosya123 pagosya-api
docker network connect datos pagosya-api      # su cara privada: única vía a la DB

curl -s http://localhost:8088/health          # almcenado: "postgres"
```

## Paso 4 · Rutas (ambos sentidos)

```bash
docker exec tienda-web sh -c "apk add --no-cache iproute2 iputils-ping >/dev/null 2>&1"

# portal → api y → datos, vía el router
docker exec tienda-web ip route add 192.168.<X>.0/26  via <ROUTER_EN_PORTAL>
docker exec tienda-web ip route add 192.168.<X>.80/28 via <ROUTER_EN_PORTAL>
# API → portal (vuelta)
docker exec pagosya-api ip route add 192.168.<X>.64/28 via <ROUTER_EN_PAGOS>

docker exec tienda-web ping -c 3 <IP_API>                 # 0% pérdida
docker exec tienda-web sh -c "apk add --no-cache traceroute >/dev/null 2>&1; \
  traceroute -m 4 <IP_API>"                               # salto por el router
```

## Paso 5 · DNS interno (3 nombres)

```bash
DNS_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' eco-dns)
docker run -d --name eco-dns --network portal -p 8053:53/udp jpillora/dnsmasq \
  --address=/<portal>.local/<IP_PORTAL> \
  --address=/<api>.local/<IP_API> \
  --address=/<db>.local/<IP_DB>

docker run --rm --network portal alpine sh -c \
  "apk add --no-cache bind-tools >/dev/null 2>&1; \
   dig <portal>.local @$DNS_IP +short; dig <api>.local @$DNS_IP +short; dig <db>.local @$DNS_IP +short"
```

## Paso 6 · Monitoreo + prueba funcional (el cierre)

```bash
# cara privada de la API (la que toca datos) — ver la consulta ir a la DB
docker exec pagosya-api tcpdump -i eth1 -nn port 5432

# en otra terminal: el flujo completo
curl -s -o /dev/null -w "portal %{http_code}\n" http://localhost:8081/          # 200
curl -s -X POST http://localhost:8088/pagos \
  -H 'Content-Type: application/json' -d '{"monto":99.99,"cliente":"EquipoX"}' # 201
curl -s http://localhost:8088/pagos        # el listado incluye el pedido (persistió)
docker port datosya-db                     # sigue vacío
```

En el tcpdump debe verse el tráfico hacia `5432` (INSERT/SELECT) → **monitoreo**.

## Entregables del Caso 3 (documento final del ecosistema)

1. Tabla VLSM completa **calculada por tu equipo** (subred/broadcast/gateway) + `ipcalc`.
2. Captura de las 4 subredes (`docker network ls` + `inspect`).
3. Prueba funcional: portal 200 → POST → **201** → GET con el pedido.
4. `docker port datosya-db` **vacío** (aislamiento).
5. Monitoreo: `tcpdump port 5432` (o `iftop`) con el INSERT visible.
6. `dig` de los 3 nombres del DNS interno.
7. **Diagrama final** (subredes, IPs, router, puertos, **flujo del pedido**).
8. Respuestas a las preguntas.

## Preguntas de verificación

1. ¿Por qué el enlace entre subredes se dimensiona `/30` (2 hosts)?
2. ¿Qué significa la "doble casa" de la API? ¿Por qué la DB solo se alcanza desde ahí?
3. En la prueba final, ¿qué capas cruzó el mensaje del navegador a la DB? Nombrá cada una.
4. ¿Cómo garantiza el aislamiento (`docker port` vacío) que ni el host ni internet vean la DB?
5. ¿Qué consecuencia tendría empezar la segunda subred en el gateway equivocado? (orden VLSM)