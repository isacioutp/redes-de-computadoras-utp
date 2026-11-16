# CASO 1 — "El portal" (capa aplicación + enlace) — **Laboratorio guiado**

**Enlace + HTTP/HTTPS/DNS · una subred simple · captura de una trama**

> Laboratorio **guiado**: seguí los pasos y capturá cada evidencia. Trabajás en
> tu escenario (`Escenarios/Grupo-N-*.md`): la guía es la misma para todos, solo
> cambian la base IP, el dominio y los nombres.

## Tus datos de escenario

| Dato | Valor |
|------|-------|
| Base IP | `192.168.<X>.0/24` (ver tu hoja de escenario: Grupo 1 → `88`, Grupo 2 → `89`, …) |
| Dominio | `<tu-escenario>.local` (ej. `feria.local`) |
| Subred del portal | `portal` → `192.168.<X>.0/26` · gateway `192.168.<X>.1` |
| Puerto HTTP / HTTPS | `8081` / `8443` |

> **Por qué `/26`:** la guía empieza simple (una sola subred de una base `/24`).
> El subnetting VLSM completo llega en el Caso 3.

## Paso 1 · Crear la subred del portal

```bash
docker network create portal --subnet 192.168.<X>.0/26 --gateway 192.168.<X>.1
```

Verificá con `docker network ls` y `docker network inspect portal` (guardá la
captura). El portal tendrá la primera IP libre: `192.168.<X>.2`.

## Paso 2 · Portal web (nginx, HTTP)

```bash
mkdir -p web
cat > web/index.html << 'EOF'
<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Mi escenario</title></head>
<body><h1>Portal de mi empresa</h1></body></html>
EOF

# IMPORTANTE: --cap-add NET_ADMIN (lo necesitarás para tcpdump y para las rutas del Caso 2)
docker run -d --name tienda-web --network portal --cap-add NET_ADMIN \
  -p 8081:80 -v "$(pwd)/web:/usr/share/nginx/html:ro" nginx:alpine

docker inspect -f 'PORTAL_IP={{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' tienda-web
# → PORTAL_IP=192.168.<X>.2   (guardá este valor, lo usás en el Paso 4)
```

Evidencia: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8081/` → **200**.
Y una página inexistente → **404**.

## Paso 3 · HTTPS (certificado autofirmado)

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout privkey.pem -out server.crt \
  -subj "/CN=<tu-dominio>"

cat > nginx-ssl.conf << 'EOF'
server {
    listen 443 ssl;
    server_name <tu-dominio>;
    ssl_certificate     /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    location / { root /usr/share/nginx/html; index index.html; }
}
EOF

docker run -d --name tienda-https --network portal -p 8443:443 \
  -v "$(pwd)/server.crt:/etc/nginx/ssl/server.crt:ro" \
  -v "$(pwd)/privkey.pem:/etc/nginx/ssl/privkey.pem:ro" \
  -v "$(pwd)/web:/usr/share/nginx/html:ro" \
  -v "$(pwd)/nginx-ssl.conf:/etc/nginx/conf.d/default.conf:ro" nginx:alpine
```

Evidencias (ambas):

```bash
curl -s -o /dev/null -w "%{http_code}" https://localhost:8443/        # falla (autofirmado)
curl -sk -o /dev/null -w "%{http_code}" https://localhost:8443/       # 200
```

## Paso 4 · DNS propio (dnsmasq)

```bash
# 1) creá el DNS **en la red portal**, apuntando tu dominio a la IP del portal
#    (<IP_DEL_PORTAL> = 192.168.<X>.2 que guardaste en el Paso 2)
docker run -d --name tienda-dns --network portal -p 8053:53/udp \
  jpillora/dnsmasq --address=/<tu-dominio>/<IP_DEL_PORTAL>

# 2) recién AHORA que el contenedor existe, capturá su IP en la red portal:
DNS_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' tienda-dns)
echo "DNS_IP=$DNS_IP"   # ej. 192.168.<X>.4
```

> dnsmasq escucha en la IP de su interfaz, no en `localhost` del contenedor; y
> esa imagen no trae `dig`. Consultá desde un **cliente de la red**:

```bash
docker run --rm --network portal alpine sh -c \
  "apk add --no-cache bind-tools >/dev/null 2>&1; dig <tu-dominio> @$DNS_IP +short"
# → tiene que salir la IP del portal (192.168.<X>.2)
```

## Paso 5 · Ver la trama (capa de enlace, teoría del Lab 6)

```bash
docker exec tienda-web sh -c "apk add --no-cache tcpdump >/dev/null 2>&1"
docker exec tienda-web tcpdump -i eth0 -nn -XX port 80 -c 5
```

En otra terminal pedile al portal:

```bash
curl -s -o /dev/null http://localhost:8081/
```

En la captura buscá y **marcá**: MAC destino, MAC origen, `EtherType` (`0800` =
IPv4) y el handshake TCP (`Flags [S]`, `[S.]`, `[.]`). Guardá la captura.

## Paso 6 · Tabla de puertos (completala en el documento)

| Servicio | Protocolo | Puerto interno | Puerto host |
|----------|-----------|----------------|-------------|
| HTTP (portal) | TCP | 80 | 8081 |
| HTTPS (portal) | TCP | 443 | 8443 |
| DNS | UDP | 53 | 8053 |

## Entregables del Caso 1 (documento)

1. `docker network ls` + `inspect` de `portal` y justificación del `/26`.
2. Capturas: HTTP 200, 404, HTTPS sin `-k` (falla) y con `-k` (200).
3. `dig <dominio> +short` desde el cliente (resuelve a la IP del portal).
4. Captura `tcpdump -XX` con MAC/EtherType/handshake **marcados**.
5. Tabla de puertos.
6. **Diagrama del Caso 1** (ver DIAGRAMAS.md).
7. Respuestas a las preguntas.

## Preguntas de verificación

1. ¿Qué campos de la trama cambian entre emisor y receptor? (switch/router)
2. ¿Por qué un navegador rechaza el certificado autofirmado del DNS propio?
3. Al abrir `<tu-dominio>`: ¿en qué orden actúan DNS, TCP y HTTP?
4. ¿Cuántos hosts útiles tiene una `/26`?
5. ¿Qué evidencia confirma que el mensaje viaja dentro de una trama Ethernet?