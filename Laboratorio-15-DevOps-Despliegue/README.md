# Laboratorio N.º 15 — El despliegue y su red: pipeline a mano con Docker

Semana 14+ · Unidad III · **1 sesión** (práctica de cierre)

> **Sigue siendo un curso de redes.** El pipeline es el escenario: lo que se
> estudia es el **tráfico** que hace posible un despliegue — qué puerto, en qué
> dirección, por qué subred y qué se rompe cuando un flujo falla. El guion
> docente completo (caso, tiempos y preguntas) está en
> [`../CLASE-DEVOPS.md`](../CLASE-DEVOPS.md); la teoría, en
> [`../Teoria-DevOps-Despliegue.pptx`](../Teoria-DevOps-Despliegue.pptx).

## 🧭 La red que se mide

| # | Flujo | Origen → destino | Puerto | Si se bloquea |
|---|-------|------------------|--------|----------------|
| 1 | Código | tu host → servidor Git | 22/443 | no hay commit |
| 2 | Push | daemon → registry | 5000/TCP | el artefacto no sale |
| 3 | Pull | servidor → registry | 5000/TCP | no encuentra la imagen |
| 4 | Servicio | cliente → app publicada | 8080 → 8000 (**NAT**) | `RST` / sin respuesta |
| 5 | Interno | app → base de datos | 5432/TCP · DNS `db` | arranca y falla al conectar |

En esta práctica se ejercitan los flujos **2, 3 y 4**. El 1 y el 5 ya se
trabajaron en el Laboratorio N.º 14.

## 📁 Archivos

| Archivo | Qué es |
|---------|--------|
| `app/app.py` | API de 17 líneas: responde `/` con la versión y `/health` con `ok` |
| `app/Dockerfile` | Mete la versión en `/app/VERSION` con `ARG APP_VERSION` |
| `compose.yml` | Publica `8080` del host → `8000` del contenedor, usa `TAG` y `init: true` |
| `.gitignore` | Ignora `.last-good` (se genera en clase) |

## 🚀 Práctica (10 comandos)

> **Importante:** el laboratorio se trabaja en **tu propio repo**, no dentro del
> repo del curso. Cópialo fuera antes de empezar.

```bash
# 0 · Preparar el repo y el registry local
cp -r Laboratorio-15-DevOps-Despliegue ~/pagosya-devops
cd ~/pagosya-devops
git init && git config user.email "estudiante@utp.ac.pa" && git config user.name "Estudiante"
git add -A && git commit -m "PagosYA api inicial"
docker run -d --name registry -p 127.0.0.1:5000:5000 registry:2

# 1 · La versión tiene nombre (el tag es el commit)
TAG=$(git rev-parse --short HEAD)

# 2 · Build desde el repo, no desde la laptop
docker build --build-arg APP_VERSION="$TAG" -t localhost:5000/pagosya-api:$TAG app/

# 3 · El artefacto es el que dice ser
docker run --rm localhost:5000/pagosya-api:$TAG cat /app/VERSION

# 4 · Publicar el artefacto (inmutable)
docker push localhost:5000/pagosya-api:$TAG
curl -s localhost:5000/v2/_catalog

# 5 · Desplegar un tag explícito
TAG="$TAG" docker compose up -d

# 6 · Smoke test: la puerta es la respuesta, no el proceso
curl localhost:8080/
# → PagosYA api <TAG>

# 7 · Registrar la última versión buena
echo "$TAG" > .last-good
```

> Si el `curl` sale vacío, espera 2 segundos y repite: la app tarda en arrancar.
> Si el tag que responde **no** es el que desplegaste, el despliegue no pasó,
> aunque `docker ps` diga `Up`.

### Romperlo y volver (el corazón del laboratorio)

```bash
# 8 · Romper: la app escucha en 9000, pero el DNAT apunta a 8000
sed -i 's/8000/9000/' app/app.py
git commit -am "cambio de puerto"
TAG=$(git rev-parse --short HEAD)
docker build --build-arg APP_VERSION="$TAG" -t localhost:5000/pagosya-api:$TAG app/
docker push localhost:5000/pagosya-api:$TAG
TAG="$TAG" docker compose up -d
curl localhost:8080/        # falla: el puerto existe, nadie escucha
docker port pagosya-devops-api-1

# 9 · Volver: se elige una imagen que ya existe, no se reconstruye
TAG=$(cat .last-good) docker compose up -d
curl localhost:8080/        # → PagosYA api <tag bueno> · menos de 1 s

# 10 · Evidencia: las dos versiones siguen en el registry
curl -s localhost:5000/v2/pagosya-api/tags/list
```

## 🔍 Diagnóstico de red

```bash
docker port pagosya-devops-api-1
# 8000/tcp -> 0.0.0.0:8080        ← la regla que programó Docker

docker network inspect pagosya-devops_default \
  --format '{{range .IPAM.Config}}{{.Subnet}} gw {{.Gateway}}{{end}}'
# 172.22.0.0/16 gw 172.22.0.1

ss -ltnp | grep -E ':(5000|8080)'
# 0.0.0.0:8080 (app) · 127.0.0.1:5000 (registry)

curl -v localhost:8080/ 2>&1 | grep -E 'Connected|HTTP'
```

> `localhost` es la **loopback** de cada máquina: no pasa por la tarjeta de red
> y no se alcanza desde otra. Para que otro equipo use tu registry habría que
> publicarlo con `-p 5000:5000`, abrir 5000/TCP y declararlo `insecure-registry`
> (o ponerle TLS).

## 📝 Entregable

| Ítem | Pts | Qué se entrega |
|------|-----|----------------|
| Bitácora + mapa de flujos | 40 | Los 10 comandos con el tag real, y los 5 flujos (origen → destino, puerto, cifrado, qué se rompe) |
| Evidencia | 30 | `_catalog`, tag en `curl`, `docker port`/`ss`, smoke en rojo y rollback cronometrado |
| Postmortem del caso | 20 | Una página: línea de tiempo, 5 porqués, las 3 piezas que faltaban |
| Métricas | 10 | Tabla antes/después (DORA) y MTTR medido |

> Se evalúa la **explicación de red**, no la memorización: quien pega los
> comandos pero no sabe qué puerto abrió, no aprobó.

## 🧹 Limpieza

```bash
docker compose down
docker rm -f registry
```
