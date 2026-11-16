# RESOLUCIÓN — Caso 3 (guía de verificación del docente)

> La guía paso a paso es `CASO-3.md` (con la VLSM a calcular por el equipo);
> aquí está la **partición esperada**, la **versión verificada** de los comandos
> (Docker 29.x) y los **errores típicos a chequear** en las entregas. Base de
> ejemplo Grupo 1: `192.168.88.0/24` (en los demás grupos, tercer octeto `8X`).

## La partición VLSM (la "respuesta")

| # | Prefijo | Subred | Broadcast | Gateway | Hosts útiles | Servicio |
|---|---------|--------|-----------|---------|--------------|----------|
| 1 | /26 | 192.168.88.0/26 | .63 | .1 | 62 | API `pagos` |
| 2 | /28 | 192.168.88.64/28 | .79 | .65 | 14 | Portal `portal` |
| 3 | /28 | 192.168.88.80/28 | .95 | .81 | 14 | DB `datos` |
| 4 | /29 | 192.168.88.96/29 | .103 | .97 | 6 | Admin |
| 5 | /30 | 192.168.88.104/30 | .107 | .105 | 2 | Enlace routers |

> Se parte de mayor a menor (30→8→8→5→2) y se toman bloques consecutivos.
> El `/30` suele quedar solo en el diagrama (los routers se montan con
> `docker network connect`, no con un enlace punto a punto real).

## Redes + router

```bash
# rediseño: quitar lo previo del equipo
docker rm -f tienda-web pagosya-api router-eco eco-dns datosya-db 2>/dev/null || true
docker network rm portal pagos 2>/dev/null || true

docker network create pagos  --subnet 192.168.88.0/26  --gateway 192.168.88.1
docker network create portal --subnet 192.168.88.64/28 --gateway 192.168.88.65
docker network create datos  --subnet 192.168.88.80/28 --gateway 192.168.88.81
docker network create admin  --subnet 192.168.88.96/29 --gateway 192.168.88.97

docker run -d --name router-eco --cap-add=NET_ADMIN \
  --sysctl net.ipv4.ip_forward=1 --network pagos alpine sleep 7200
docker network connect portal router-eco
docker network connect datos  router-eco
docker network connect admin  router-eco
sudo sysctl -w net.ipv4.ip_forward=1
```

Verificado: router en `.66` (pagos… ejemplo) … las IPs concretas dependen del
orden de creación; usar `docker exec router-eco ip addr`.

## Portal, DB aislada y API "doble casa"

```bash
printf '<h1>FeriaYA</h1>\n' > web/index.html
docker run -d --name tienda-web --network portal --cap-add NET_ADMIN \
  -p 8081:80 -v "$(pwd)/web:/usr/share/nginx/html:ro" nginx:alpine

docker run -d --name datosya-db --network datos \
  -e POSTGRES_USER=pagosya -e POSTGRES_PASSWORD=pagosya123 -e POSTGRES_DB=pagosya \
  -v "$(pwd)/plantilla/init.sql:/docker-entrypoint-initdb.d/init.sql:ro" \
  postgres:15-alpine
docker port datosya-db        # → vacío  (el aislamiento)

docker build -t pagosya-api plantilla/api
docker run -d --name pagosya-api --network pagos --cap-add NET_ADMIN -p 8088:5000 \
  -e DB_HOST=datosya-db -e DB_USER=pagosya -e DB_PASS=pagosya123 pagosya-api
docker network connect datos pagosya-api   # cara privada → única vía a la DB
curl -s http://localhost:8088/health       # almacenado: "postgres"
```

## Rutas (ambos sentidos)

```bash
RT=$(docker exec router-eco sh -c "ip route show | grep portal | awk '{print \$NF}'")
docker exec tienda-web ip route add 192.168.88.0/26  via <ROUTER_EN_PORTAL>
docker exec tienda-web ip route add 192.168.88.80/28 via <ROUTER_EN_PORTAL>
docker exec pagosya-api ip route add 192.168.88.64/28 via <ROUTER_EN_PAGOS>
docker exec tienda-web ping -c 3 192.168.88.3     # verificado 0% pérdida
docker exec tienda-web sh -c "apk add --no-cache traceroute >/dev/null 2>&1; traceroute -m 4 192.168.88.3"
# → salto por router (verificado: 2 hops)
```

## DNS de los 3 servicios

```bash
DNS_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' eco-dns)
docker run -d --name eco-dns --network portal -p 8053:53/udp jpillora/dnsmasq \
  --address=/feria.local/192.168.88.67 \
  --address=/api.feria.local/192.168.88.3 \
  --address=/db.feria.local/192.168.88.83
docker run --rm --network portal alpine sh -c \
  "apk add --no-cache bind-tools >/dev/null 2>&1; \
   dig feria.local @$DNS_IP +short; dig api.feria.local @$DNS_IP +short; dig db.feria.local @$DNS_IP +short"
```

(IPs de ejemplo según el orden de creación.)

## Monitoreo + prueba funcional (verificado)

```bash
# cara privada de la API (eth1 = datos): ver el INSERT hacia la DB
docker exec pagosya-api tcpdump -i eth1 -nn port 5432

curl -s -o /dev/null -w 'portal %{http_code}\n' http://localhost:8081/      # 200
curl -s -X POST http://localhost:8088/pagos -H 'Content-Type: application/json' \
  -d '{"monto": 99.99, "cliente": "EquipoX"}'                               # 201
# {"almacenado":"postgres","estado":"registrado","id_pago":1}
curl -s http://localhost:8088/pagos        # listado incluye el pedido (persistió)
# y en tcpdump: 25+ paquetes port 5432 (INSERT/SELECT)
```

## Errores típicos a verificar en las entregas

1. **Solape VLSM** — la tabla "con los prefijos ya puestos" pero con bloque mal
   ubicados (comenzar la 2.ª subred en `.1` en vez de `.64`).
2. DB con `-p` publicada al host (rompe el aislamiento).
3. API sin `DB_HOST`/sin cara `datos` → /health dice "memoria" (no probaron la API).
4. Ruta de vuelta olvidada → ping cruzado 100% pérdida.
5. DNS consultado con `dig @localhost` dentro del propio DB.
6. Diagrama con IPs que no coinciden con las capturas o sin el flujo del pedido (ver DIAGRAMAS.md).