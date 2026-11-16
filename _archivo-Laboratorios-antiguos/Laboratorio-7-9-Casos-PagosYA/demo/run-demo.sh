#!/usr/bin/env bash
# Demo Lab 7-9: levanta el stack completo y prepara las rutas.
# EJECUTAR ANTES DE LA CLASE. Requiere Docker.
set -euo pipefail
cd "$(dirname "$0")"

echo ">>> [1/5] Generando certificado autofirmado (HTTPS)..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout privkey.pem -out server.crt \
  -subj "/C=PA/ST=Panama/L=CD/L=UTP/O=Redes/CN=localhost" 2>/dev/null

echo ">>> [2/5] Contenido web de prueba..."
mkdir -p html
echo "<h1>Demo Lab 7-9 · El viaje de un mensaje</h1>" > html/index.html

echo ">>> [3/5] Habilitando reenvío de paquetes en el host..."
sudo sysctl -w net.ipv4.ip_forward=1 || true

echo ">>> [4/5] Levantando el stack (red + transporte + aplicación)..."
docker compose up -d --build

echo ">>> [5/5] Montando rutas entre subredes (via router)..."
docker exec demo-web ip route add 192.168.60.32/27 via 192.168.60.2 || true
docker exec demo-api sh -c "ip route add 192.168.60.0/27 via 192.168.60.34" || true

echo
echo ">>> Listo. Panel de servicios:"
docker compose ps --format 'table {{.Name}}\t{{.Status}}\t{{.Ports}}'
echo
echo ">>> IPs por contenedor:"
for c in demo-router demo-web demo-web-https demo-api demo-db demo-dns; do
  ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}  {{end}}' "$c" 2>/dev/null)
  echo "  $c -> $ip"
done
echo
echo ">>> Comando rápido para la demo:  bash demo/quick-checks.sh"