# Laboratorio N.º 15 — El despliegue y su red: pipeline a mano con Docker

Semana 14+ · Unidad III · **1 sesión**

Vas a desplegar una API en tu máquina, romperla a propósito y volver a la
versión anterior en segundos. Todo es **local**: no necesitas Git, ni GitHub,
ni internet. Lo que se estudia es la **red** que hace posible el despliegue.

> La teoría de la sesión está en
> [`../Teoria-DevOps-Despliegue.pptx`](../Teoria-DevOps-Despliegue.pptx) (o en
> texto: [`../TEORIA-DEVOPS-DESPLIEGUE.md`](../TEORIA-DEVOPS-DESPLIEGUE.md)).

## 🧭 Los cinco flujos (el mapa)

| # | Flujo | Origen → destino | Puerto | Si se bloquea | ¿Lo haces aquí? |
|---|-------|------------------|--------|----------------|-----------------|
| 1 | Código | tu host → servidor Git | 22/443 | no hay commit | contexto |
| 2 | Push | daemon → registry | 5000/TCP | el artefacto no sale | **sí** |
| 3 | Pull | servidor → registry | 5000/TCP | no encuentra la imagen | **sí** |
| 4 | Servicio | cliente → app publicada | 8080 → 8000 (**NAT**) | `RST` / sin respuesta | **sí** |
| 5 | Interno | app → base de datos | 5432/TCP · DNS `db` | arranca y falla al conectar | contexto |

Los flujos 2, 3 y 4 los ejecutas tú. El 1 y el 5 se explican en clase: en este
laboratorio no hay servidor Git ni base de datos.

## ✅ Lo que necesitas

- Docker Engine con el plugin **Compose v2** (`docker compose version`).
- `curl`.
- Linux, macOS o WSL. En Windows nativo los comandos cambian.

## 📁 Lo que trae la carpeta

| Archivo | Qué es |
|---------|--------|
| `app/app.py` | La API: responde `/` con la versión y `/health` con `ok` |
| `app/Dockerfile` | Mete la versión en `/app/VERSION` con `ARG APP_VERSION` |
| `compose.yml` | Publica `8080` del host → `8000` del contenedor, usa `TAG` e `init: true` |

No hay scripts: **cada comando lo escribes tú**.

---

# Guía paso a paso

## Paso 0 · Prepara la carpeta y el registry

Copia la carpeta fuera del repo del curso y arranca un registry local:

```bash
cp -r Laboratorio-15-DevOps-Despliegue ~/pagosya-devops
cd ~/pagosya-devops
docker run -d --name registry -p 127.0.0.1:5000:5000 registry:2
```

**Debes ver** un ID de contenedor y, al comprobarlo:

```bash
docker ps --filter name=registry
# registry  Up ...  127.0.0.1:5000->5000/tcp
```

> `127.0.0.1` es la **loopback**: el registry solo es alcanzable desde tu
> máquina. Con `-p 5000:5000` quedaría publicado en todas las interfaces.

## Paso 1 · Ponle nombre a la versión

```bash
TAG=v1
echo "$TAG"
# v1
```

> En un equipo real el tag sale del commit (`git rev-parse --short HEAD`). Aquí
> lo eliges tú para que el laboratorio no dependa de Git.

## Paso 2 · Construye la imagen

```bash
docker build --build-arg APP_VERSION="$TAG" \
  -t localhost:5000/pagosya-api:$TAG app/
```

**Debes ver** al final líneas como:

```
#9 naming to localhost:5000/pagosya-api:v1 done
#9 DONE 0.1s
```

> El `ARG` se **hornea** en la imagen: cambiar el tag cambia el contenido de
> `/app/VERSION`. Por eso el smoke test puede comparar lo que sirve con lo que
> se desplegó.

## Paso 3 · Comprueba el artefacto

```bash
docker run --rm localhost:5000/pagosya-api:$TAG cat /app/VERSION
# v1
```

Si responde otra cosa, la imagen no es la que crees: no sigas.

## Paso 4 · Publícala en el registry

```bash
docker push localhost:5000/pagosya-api:$TAG
curl -s localhost:5000/v2/_catalog
# {"repositories":["pagosya-api"]}
```

**Debes ver** el digest de la imagen y el catálogo con `pagosya-api`.

## Paso 5 · Despliega ese tag explícito

```bash
TAG="$TAG" docker compose up -d
# Container pagosya-devops-api-1  Started
```

Comprueba la traducción de puertos:

```bash
docker port pagosya-devops-api-1
# 8000/tcp -> 0.0.0.0:8080
```

> El contenedor se llama `<nombre-de-la-carpeta>-api-1`. Si copiaste la carpeta
> con otro nombre, usa ese (`docker compose ps` lo muestra).

> `8080 → 8000` es **DNAT**: el puerto del host se traduce al del contenedor.

## Paso 6 · Smoke test (la puerta)

```bash
curl localhost:8080/
# PagosYA api v1
```

Si sale vacío, espera 2 segundos y repite: la app tarda en arrancar.

> `docker ps` solo prueba que el proceso existe. Este `curl` prueba el
> **camino**: host:8080 → DNAT → contenedor:8000 → proceso → HTTP.

## Paso 7 · Registra la última versión buena

```bash
echo "$TAG" > .last-good
cat .last-good
# v1
```

## Paso 8 · Rompe el despliegue

Cambia el puerto interno de la app y despliega como `v2`:

```bash
sed -i 's/8000/9000/' app/app.py
# En macOS: sed -i '' 's/8000/9000/' app/app.py
TAG=v2
docker build --build-arg APP_VERSION="$TAG" \
  -t localhost:5000/pagosya-api:$TAG app/
docker push localhost:5000/pagosya-api:$TAG
TAG="$TAG" docker compose up -d
```

Ahora el smoke falla:

```bash
curl localhost:8080/
# curl: (56) Recv failure: Conexión reinicializada por la máquina remota
```

Y la red te dice por qué:

```bash
docker port pagosya-devops-api-1
# 8000/tcp -> 0.0.0.0:8080      ← la regla sigue apuntando a 8000

docker network inspect pagosya-devops_default \
  --format '{{range .IPAM.Config}}{{.Subnet}} gw {{.Gateway}}{{end}}'
# 172.23.0.0/16 gw 172.23.0.1   ← tu subred puede variar

ss -ltnp | grep -E ':(5000|8080)'
# 0.0.0.0:8080 (app) · 127.0.0.1:5000 (registry)
```

> `docker ps` dirá `Up`, pero el DNAT apunta a `8000` y la app escucha en
> `9000`. El kernel cierra con `RST` una conexión a un puerto sin listener: es
> un problema de **puerto**, no de ruta ni de DNS.

## Paso 9 · Vuelve a la versión anterior

```bash
TAG=$(cat .last-good) docker compose up -d
curl localhost:8080/
# PagosYA api v1
```

Tarda **menos de 2 segundos**: no se reconstruye nada, se elige una imagen que
ya está en el registry.

> El `init: true` del `compose.yml` es lo que hace que sea así de rápido: sin
> él, Python queda como PID 1, ignora el `SIGTERM` y `docker stop` espera 10 s.

## Paso 10 · Deja la evidencia

```bash
curl -s localhost:5000/v2/pagosya-api/tags/list
# {"name":"pagosya-api","tags":["v2","v1"]}
```

La versión mala **no se borra**: queda en el registry como evidencia. Volver
atrás fue elegir `v1`, no reconstruirla.

---

## 🧹 Limpieza

```bash
docker compose down
docker rm -f registry
```

## 🔧 Si algo falla

| Síntoma | Causa | Solución |
|---------|-------|----------|
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | Otro contenedor usa 8080 | `docker ps`, y detén el que lo ocupa |
| `Bind for 127.0.0.1:5000 failed` | Ya hay un registry corriendo | `docker rm -f registry` y repite el paso 0 |
| `pull access denied` al hacer `compose up` | La imagen no está en el registry | Repite el paso 4 y revisa el tag |
| El smoke responde un tag viejo | El contenedor no se recreó | `TAG="$TAG" docker compose up -d --force-recreate` |
| `curl: (56) Recv failure` | El puerto interno no coincide con el DNAT | `docker port` y revisa el puerto en `app.py` |
| `cat: .last-good: No such file` | Nunca hubo un despliegue verde | Completa los pasos 5-7 antes de romper |
| `permission denied` al usar Docker | Tu usuario no está en el grupo `docker` | Usa `sudo` o agrega el usuario al grupo |

## 📝 Qué entregas

1. **Bitácora** de los 10 pasos con el tag real en cada uno.
2. **Mapa de los 5 flujos**: origen → destino, puerto y qué se rompe si se bloquea.
3. **Evidencia**: salida de `_catalog`, el tag en `curl`, `docker port`/`ss`, el
   smoke en rojo y el tiempo del rollback.
4. **Explicación de red**: por qué falló el paso 8 y por qué el paso 9 fue inmediato.

> Se evalúa la **explicación de red**, no la memorización: quien pega los
> comandos pero no sabe qué puerto abrió, no aprobó.

## 🌐 Contexto (no se ejecuta)

| Se ejecuta en tu máquina | Solo se explica |
|--------------------------|-----------------|
| `docker build`, `push`, `compose up -d`, `curl` | Git remoto / GitHub (flujo 1, 22/443) |
| Registry `registry:2` en `localhost:5000` | CI/CD del equipo |
| Smoke, `.last-good` y rollback | Ciclo DevOps completo y métricas DORA |

El laboratorio no necesita internet ni un servidor: todo pasa en **loopback** y
en la **red bridge** del compose.
