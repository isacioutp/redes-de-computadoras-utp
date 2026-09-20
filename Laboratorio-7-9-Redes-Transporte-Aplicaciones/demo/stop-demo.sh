#!/usr/bin/env bash
# Baja el stack de la demo y elimina todo (contenedores, redes, imágenes).
cd "$(dirname "$0")"
set -euo pipefail

docker compose down --remove-orphans
docker rm -f demo-router demo-web demo-web-https demo-api demo-db demo-dns 2>/dev/null || true
echo ">>> Stack de la demo detenido."