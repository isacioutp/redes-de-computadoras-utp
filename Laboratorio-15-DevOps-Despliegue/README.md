# Laboratorio N.º 15 — El despliegue y su red: pipeline a mano con Docker

Semana 14+ · Unidad III · **1 sesión** (práctica de cierre)

> **Sigue siendo un curso de redes.** El pipeline es el escenario: lo que se
> estudia es el **tráfico** que hace posible un despliegue — qué puerto, en qué
> dirección, por qué subred y qué se rompe cuando un flujo falla. El guion
> docente completo (caso, tiempos y preguntas) está en
> [`../CLASE-DEVOPS.md`](../CLASE-DEVOPS.md); la teoría, en
> [`../Teoria-DevOps-Despliegue.pptx`](../Teoria-DevOps-Despliegue.pptx).

## 🧭 La red que se mide

| # | Flujo | Origen → destino | Puerto | Si se bloquea | ¿Se ejecuta? |
|---|-------|------------------|--------|----------------|--------------|
| 1 | Código | tu host → servidor Git | 22/443 | no hay commit | **contexto** |
| 2 | Push | daemon → registry | 5000/TCP | el artefacto no sale | sí |
| 3 | Pull | servidor → registry | 5000/TCP | no encuentra la imagen | sí |
| 4 | Servicio | cliente → app publicada | 8080 → 8000 (**NAT**) | `RST` / sin respuesta | sí |
| 5 | Interno | app → base de datos | 5432/TCP · DNS `db` | arranca y falla al conectar | **contexto** |

En esta práctica se ejercitan los flujos **2, 3 y 4**. El 1 y el 5 ya se
trabajaron en el Laboratorio N.º 14.

## 🧪 Qué es local y qué es contexto

Todo el laboratorio corre **en tu máquina, sin internet**: la app, el registry,
la red del compose, el smoke y el rollback. No hay servidor remoto que
configurar.

| Se ejecuta (local, con Docker) | Es solo contexto (no se ejecuta) |
|--------------------------------|----------------------------------|
| `docker build`, `docker push`, `docker compose up -d` | Git remoto / GitHub (22 o 443/TCP) |
| Registry `registry:2` en `localhost:5000` | CI/CD: el pipeline automático del equipo |
| `curl` al `8080` y el rollback con `.last-good` | Ciclo DevOps completo: planear, operar, medir, aprender |
| El tag `v1`/`v2` que eliges tú | En producción, el tag sale del commit (`git rev-parse`) |
| — | Métricas DORA y los roles del equipo |

> **Git no es un requisito.** Aquí el tag lo pones tú (`v1`, `v2`). En un equipo
> real lo pone el commit, y ese flujo remoto es exactamente el **flujo 1** de la
> tabla de arriba: se explica, no se ejecuta.

## 📁 Archivos

| Archivo | Qué es |
|---------|--------|
| `app/app.py` | API de 17 líneas: responde `/` con la versión y `/health` con `ok` |
| `app/Dockerfile` | Mete la versión en `/app/VERSION` con `ARG APP_VERSION` |
| `compose.yml` | Publica `8080` del host → `8000` del contenedor, usa `TAG` e `init: true` |
| `.gitignore` | Ignora `.last-good` (se genera en clase) |

## 🚀 Práctica (10 comandos)

> El laboratorio se trabaja en **tu propia carpeta**, no dentro del repo del
> curso. Cópiala fuera antes de empezar.

```bash
# 0 · Preparar la carpeta y el registry local
cp -r Laboratorio-15-DevOps-Despliegue ~/pagosya-devops
cd ~/pagosya-devops
docker run -d --name registry -p 127.0.0.1:5000:5000 registry:2

# 1 · La versión tiene nombre (tú eliges el tag)
TAG=v1

# 2 · Build desde la carpeta, no desde otra máquina
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
# → PagosYA api v1

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
TAG=v2
docker build --build-arg APP_VERSION="$TAG" -t localhost:5000/pagosya-api:$TAG app/
docker push localhost:5000/pagosya-api:$TAG
TAG="$TAG" docker compose up -d
curl localhost:8080/        # falla: el puerto existe, nadie escucha
docker port pagosya-devops-api-1

# 9 · Volver: se elige una imagen que ya existe, no se reconstruye
TAG=$(cat .last-good) docker compose up -d
curl localhost:8080/        # → PagosYA api v1 · menos de 1 s

# 10 · Evidencia: las dos versiones siguen en el registry
curl -s localhost:5000/v2/pagosya-api/tags/list
```

> El `init: true` del `compose.yml` es lo que hace que ese «menos de 1 s» sea
> real: sin él, Python queda como PID 1, ignora el `SIGTERM` y `docker stop`
> espera 10 s antes de matar el contenedor.

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
> (o ponerle TLS) — eso sí es el flujo 1, y es contexto.

## 📝 Entregable

| Ítem | Pts | Qué se entrega |
|------|-----|----------------|
| Bitácora + mapa de flujos | 40 | Los 10 comandos con el tag real, y los 5 flujos (origen → destino, puerto, cifrado, qué se rompe) |
| Evidencia | 30 | `_catalog`, tag en `curl`, `docker port`/`ss`, smoke en rojo y rollback cronometrado |
| Postmortem del caso | 20 | Una página: línea de tiempo, 5 porqués, las 3 piezas que faltaban |
| Métricas | 10 | MTTR medido del rollback; las otras 3 DORA se explican como contexto |

> Se evalúa la **explicación de red**, no la memorización: quien pega los
> comandos pero no sabe qué puerto abrió, no aprobó.

## 🧹 Limpieza

```bash
docker compose down
docker rm -f registry
```
