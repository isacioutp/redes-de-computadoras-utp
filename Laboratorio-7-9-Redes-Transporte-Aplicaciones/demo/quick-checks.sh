#!/usr/bin/env bash
# Una pantalla con TODAS las comprobaciones de la demo para mostrarla rápida.
cd "$(dirname "$0")"
set -euo pipefail

echo "================ CAPA DE RED ================"
echo "--- subneteo: dos subredes (192.168.60.0/27 y 192.168.60.32/27) ---"
docker network inspect demo-lab79_public-front demo-lab79_back \
  --format '{{.Name}}  ->  {{range .IPAM.Config}}{{.Subnet}} (gw {{.Gateway}}){{end}}'

echo "--- IP del router (una por subred) ---"
docker exec demo-router ip addr show | grep -E "inet 172"

echo "--- ping FAIL (sin ruta): demo-web -> api-back ---"
docker exec demo-web ping -c 1 192.168.60.35 || true

echo "--- ruta agregada via router ---"
docker exec demo-web ip route 2>/dev/null | grep 192.168.60.32 || true

echo "--- ping OK (con ruta) ---"
docker exec demo-web ping -c 2 192.168.60.35

echo "--- traceroute: web -> api (2 saltos) ---"
docker exec demo-web traceroute -n -m 5 192.168.60.35 2>/dev/null || true

echo
echo "================ CAPA DE TRANSPORTE ================"
echo "--- curl al API por IP interna (puerto 5000) ---"
curl -s http://192.168.60.11:5000/health
echo
echo "--- handshake: ver SYN/SYN-ACK/ACK (tcpdump en otra terminal) ---"
echo "    docker exec -it demo-api tcpdump -i eth0 -nn port 5000"
echo "    curl -s http://192.168.60.11:5000/"

echo
echo "================ CAPA DE APLICACIÓN ================"
echo "--- HTTP localhost:8081 ---"
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8081/
echo "--- HTTPS localhost:8443 (curl -k) ---"
curl -sk https://localhost:8443/
echo "--- DNS propio: dig app.lab -----------"
docker exec demo-web sh -c "apk add --no-cache -q bind-tools && dig app.lab @192.168.60.12 +short" 2>/dev/null || \
  dig app.lab @localhost -p 8053 +short