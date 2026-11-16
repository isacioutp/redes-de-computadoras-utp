# RESOLUCIÓN — Caso 2 (guía de verificación del docente)

> La guía paso a paso es `CASO-2.md`; aquí está la **versión verificada**
> (comandos probados en Docker 29.x) y los **errores típicos a chequear** en las
> entregas. Base de ejemplo Grupo 1: `192.168.88.0/24`, portal en
> `192.168.88.0/26`.

## Segunda subred

```bash
docker network create pagos --subnet 192.168.88.64/26 --gateway 192.168.88.65
```

> Contigua al `/26` del portal: NO se solapan (`.0/26` y `.64/26`). API obtiene
> `.66` (primer host libre tras el gateway `.65`).

## API (plantilla, modo memoria)

```bash
docker build -t pagosya-api plantilla/api
# NET_ADMIN: para la ruta de retorno (ver abajo)
docker run -d --name pagosya-api --network pagos --cap-add NET_ADMIN \
  -p 8088:5000 pagosya-api
curl -s http://localhost:8088/health        # almacenado: "memoria"
curl -s -X POST http://localhost:8088/pagos \
  -H 'Content-Type: application/json' -d '{"monto":99.99,"cliente":"EquipoX"}'
# 201 {"estado":"registrado","id_pago":1,...}
```

## Router + rutas (el patrón falla → ruta → OK)

```bash
docker run -d --name router-eco --cap-add=NET_ADMIN \
  --sysctl net.ipv4.ip_forward=1 --network portal alpine sleep 7200
docker network connect pagos router-eco
sudo sysctl -w net.ipv4.ip_forward=1
docker exec router-eco ip addr   # cara portal y cara pagos
```

**Punto que casi nadie ve**: el ping, además de la ruta de ida en el portal,
necesita la **ruta de vuelta** en la API (el host NO actúa de ruta de retorno
pese a `ip_forward`; se pierde por ruteo asimétrico/conntrack). Verificado: sin
la ruta de vuelta → 100% pérdida; con ella → 0%.

```bash
# ida (portal → pagos)
docker exec tienda-web ip route add 192.168.88.64/26 via <IP_ROUTER_EN_PORTAL>
# vuelta (API → portal)
docker exec pagosya-api ip route add 192.168.88.0/26 via <IP_ROUTER_EN_PAGOS>

docker exec tienda-web ping -c 3 192.168.88.66   # 0% pérdida
docker exec tienda-web sh -c "apk add --no-cache traceroute >/dev/null 2>&1; \
  traceroute -m 5 192.168.88.66"                 # salto por el router
```

## Handshake + puertos

```bash
# terminal A
docker exec pagosya-api tcpdump -i eth0 -nn port 5000 -c 10
# terminal B
curl -s http://localhost:8088/ > /dev/null
# → Flags [S], [S.], [.] (SYN → SYN-ACK → ACK) y puertos origen/destino

netstat -tlnp | grep 8088   (o con sudo)
```

## TCP vs UDP + latencia

```bash
# latencia simulada sobre la cara de la API
docker exec pagosya-api tc qdisc add dev eth0 root netem delay 100ms
docker exec pagosya-api ping -c 4 192.168.88.65   # RTT ≈ 100ms (verificado)
docker exec pagosya-api tc qdisc del dev eth0 root
# (variantte con pérdida: `tc qdisc add ... root netem loss 30%`)

# UDP mínimo (sin conexión, no hay handshake) — ejemplo verificable en un script:
# socket(AF_INET, SOCK_DGRAM) → envia "hola" → recibe "echo:hola"
```

## Errores típicos a verificar en las entregas

1. Ruta solo de ida → ping nunca responde (falta la ruta de vuelta).
2. Portal sin `--cap-add NET_ADMIN` → no puede `ip route add`.
3. `traceroute` no muestra el salto (no hay ruta por el router o pasan por el host).
4. Confunden el handshake con todo el flujo: en la captura deben **marcar** SYN, SYN-ACK y ACK.