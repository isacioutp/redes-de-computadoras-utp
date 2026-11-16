# RESOLUCIÓN — Caso 1 (guía de verificación del docente)

> La guía paso a paso (`CASO-1.md`) es la misma que reciben los equipos; aquí
> está la **versión verificada** (comandos probados en Docker 29.x) y, sobre
> todo, los **errores típicos a chequear** en las entregas. Se usa para guiarlos
> y para confirmar lo que aprendieron de la Unidad 1.
>
> Base de ejemplo: Grupo 1 · `BASE=192.168.88.0/24` · dominio `feria.local`.
> Para otro grupo cambiar el tercer octeto (88→8X) y el dominio.

## Red

```bash
docker network create portal --subnet 192.168.88.0/26 --gateway 192.168.88.1
```

> Gateway `.1`, portal obtiene `.2`. No solapa con `pagos` (`192.168.88.64/26`),
> que llega en el Caso 2 — usar `/24` aquí provoca `Pool overlaps` después.

## Portal + HTTPS

```bash
mkdir -p web
printf '<!DOCTYPE html><html><head><meta charset="utf-8"><title>FeriaYA</title></head><body><h1>FeriaYA portal</h1></body></html>\n' > web/index.html

docker run -d --name tienda-web --network portal --cap-add NET_ADMIN \
  -p 8081:80 -v "$(pwd)/web:/usr/share/nginx/html:ro" nginx:alpine

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout privkey.pem -out server.crt \
  -subj "/C=PA/ST=Panama/L=Cd de Panama/O=FeriaYA/CN=feria.local"
cat > nginx-ssl.conf <<'EOF'
server {
    listen 443 ssl;
    server_name feria.local;
    ssl_certificate     /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    location / { root /usr/share/nginx/html; index index.html; }
}
EOF
docker run -d --name tienda-https -p 8443:443 \
  -v "$(pwd)/server.crt:/etc/nginx/ssl/server.crt:ro" \
  -v "$(pwd)/privkey.pem:/etc/nginx/ssl/privkey.pem:ro" \
  -v "$(pwd)/web:/usr/share/nginx/html:ro" \
  -v "$(pwd)/nginx-ssl.conf:/etc/nginx/conf.d/default.conf:ro" nginx:alpine
```

> `--cap-add NET_ADMIN`: imprescindible para `ip route add` (Caso 2) y
> `tcpdump`. Docker por defecto da CAP_NET_RAW (por eso tcpdump sí anda solo),
> pero NO NET_ADMIN.

## DNS

```bash
DNS_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' tienda-dns)
docker run -d --name tienda-dns --network portal -p 8053:53/udp \
  jpillora/dnsmasq --address=/feria.local/192.168.88.2
```

**Trampa conocida:** dnsmasq escucha en la IP de su interfaz, NO en `@localhost`
del contenedor, y la imagen jpillora no trae `dig`. Consultar desde un cliente:

```bash
docker run --rm --network portal alpine sh -c \
  "apk add --no-cache bind-tools >/dev/null 2>&1; dig feria.local @$DNS_IP +short"
# → 192.168.88.2
```

Desde el HOST (si tiene bind-utils): `dig feria.local -p 8053 @127.0.0.1 +short`.

## Captura de la trama

```bash
docker exec tienda-web sh -c "apk add --no-cache tcpdump >/dev/null 2>&1"
docker exec tienda-web tcpdump -i eth0 -nn -XX port 80 -c 5
# otra terminal:
curl -s -o /dev/null http://localhost:8081/
```

Esperada (verificado):

```
IP 192.168.88.1.x > 192.168.88.2.80: Flags [S] ...      # SYN
IP 192.168.88.2.80 > 192.168.88.1.x: Flags [S.] ...     # SYN-ACK
IP 192.168.88.1.x > 192.168.88.2.80: Flags [.] ...      # ACK
0x0000: <MAC dest> <MAC orig> 0800 45 00 ...            # EtherType 0800 = IPv4
```

## Probar el caso

```bash
curl -s -o /dev/null -w 'HTTP  %{http_code}\n' localhost:8081   # 200
curl -s -o /dev/null -w 'HTTP  %{http_code}\n' localhost:8081/xx # 404
curl -s -o /dev/null -w 'HTTPS %{http_code}\n' https://localhost:8443/   # (curl sin -k) error de cert
curl -sk -o /dev/null -w 'HTTPS %{http_code}\n' https://localhost:8443/  # 200
```

## Errores típicos a verificar en las entregas

1. Red `/24` + plan de agregar `/26` → se solapan → falla Docker (o llega plano).
2. `ip route add` dentro del contenedor → `RTNETLINK ... Operation not permitted` (falta NET_ADMIN).
3. Consultar `dig @localhost` dentro del DNS → no responde.
4. Con `curl -k` funciona pero no lo explican (autofirmado rechazado).