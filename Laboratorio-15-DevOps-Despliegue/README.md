# Laboratorio N.º 15 — Caso: el despliegue del viernes de PagosYA

Semana 14+ · Unidad III · **1 sesión**

Este laboratorio es un **caso**. El caso completo es el despliegue que PagosYA
hizo un viernes y que dejó el servicio caído **3 h 50 min**: incluye un equipo,
un servidor en producción, un Git remoto y ocho meses de costumbre. Nada de eso
se puede reproducir en un salón, así que se entrega como **contexto**.

Lo que sí vas a reproducir es el **tramo de red donde el caso falló**: el
artefacto, el registry, el puerto publicado y el rollback. Eso corre con **tu
Docker local**, sin Git remoto ni servidores.

> La teoría de la sesión está en
> [`../Teoria-DevOps-Despliegue.pptx`](../Teoria-DevOps-Despliegue.pptx) (o en
> texto: [`../TEORIA-DEVOPS-DESPLIEGUE.md`](../TEORIA-DEVOPS-DESPLIEGUE.md)).
> El caso completo, con preguntas de diagnóstico, está en
> [`../CLASE-DEVOPS.md`](../CLASE-DEVOPS.md).

## 1. El caso

**PagosYA** es la API de pagos del Caso 2. La empresa es pequeña: tres personas,
un servidor con Docker y Compose, y ningún pipeline. Desplegar consistía en que
**Ana** entrara por SSH, hiciera `git pull` y ejecutara
`docker compose up -d --build`. Funcionó ocho meses.

| Hora | Qué pasó |
|------|----------|
| 15:30 | Se aprueba el PR «descuentos de temporada» y se fusiona a `main`. |
| 15:45 | Ana construye la imagen **en su laptop** y copia el `compose.yml` al servidor. |
| 16:10 | En el servidor: `git pull` + `compose up -d --build`. La app nueva arranca y **se cae** a los segundos. |
| 16:20 | Un cliente reporta **error 502** al pagar: el `nginx` de adelante no tiene a quién reenviar. |
| 16:35 | El contenedor **reinicia en bucle**. En la laptop de Ana funcionaba. |
| 17:00 | Deciden «volver atrás». Nadie sabe qué imagen corría: todo se publicó como `latest`. |
| 17:40 | Reconstruir desde el commit anterior **no compila**: las dependencias no están fijadas. |
| 18:30 | Restauran el respaldo de la base de datos de las 2:00 a. m.: se pierden **8 horas de pagos**. |
| 20:10 | El servicio queda estable. **Tiempo total caído: 3 h 50 min.** |

No falló el código del PR. Faltaban **tres piezas**:

1. Una **imagen versionada** (hoy todo es `latest`).
2. Un **tag explícito** en el `compose.yml`, para desplegar un artefacto concreto.
3. Un **registro de la última versión buena**, para volver sin reconstruir.

## 2. Lo que el caso entrega como contexto

Estas partes **se leen y se discuten; no se ejecutan** aquí:

| Del caso | Por qué no se reproduce | Dónde se explica |
|----------|--------------------------|------------------|
| Git remoto / PR a `main` (22/443/TCP) | Hace falta un servidor Git y un equipo | Flujo 1 del mapa |
| Servidor de producción con `nginx` | Hace falta un host aparte | El `502` = upstream sin listener |
| CI/CD del equipo | Depende de la plataforma del equipo | Etapas 2-5 automatizadas |
| Ana, los clientes y el turno de guardia | Hace falta gente | El smoke como detector |
| Base de datos y respaldo | Fuera del alcance de esta práctica | Flujo 5 (se vio en el Lab 14) |
| Ciclo DevOps completo y métricas DORA | Se miden en semanas, no en una sesión | Frecuencia, lead time, tasa de fallo, MTTR |

**El tag lo eliges tú** (`v1`, `v2`). En el caso lo ponía el commit
(`git rev-parse --short HEAD`); aquí ese flujo remoto es exactamente el flujo 1,
y es contexto.

## 3. Lo que sí reproduces

| En el caso | En tu Docker local |
|------------|--------------------|
| Ana construye en su laptop | `docker build` en tu máquina, con el mismo `Dockerfile` |
| Todo se publica como `latest` | Tags inmutables: `v1`, `v2` |
| Copia el `compose.yml` al servidor | `TAG=$TAG docker compose up -d` |
| `nginx` 8080 → app 8000 | El mismo **DNAT** `8080:8000` |
| El cliente reporta el `502` | `curl localhost:8080/` falla antes de dar el visto bueno |
| Nadie sabe qué versión corría | `cat .last-good` |
| Rollback en 3 h 50 min | Dos comandos, menos de 2 segundos |
| Se pierden 8 horas de pagos | El rollback no toca datos: no hay base de datos |

## 4. Los cinco flujos (el mapa)

| # | Flujo | Origen → destino | Puerto | Si se bloquea | ¿Dónde? |
|---|-------|------------------|--------|----------------|---------|
| 1 | Código | tu host → servidor Git | 22/443 | no hay commit | caso (contexto) |
| 2 | Push | daemon → registry | 5000/TCP | el artefacto no sale | **aquí** |
| 3 | Pull | servidor → registry | 5000/TCP | no encuentra la imagen | **aquí** |
| 4 | Servicio | cliente → app publicada | 8080 → 8000 (**NAT**) | `RST` / sin respuesta | **aquí** |
| 5 | Interno | app → base de datos | 5432/TCP · DNS `db` | arranca y falla al conectar | caso (Lab 14) |

## ✅ Lo que necesitas

- Docker Engine con el plugin **Compose v2** (`docker compose version`).
- `curl`.
- Linux, macOS o WSL. En Windows nativo los comandos cambian.

> La primera vez, Docker descarga las dos imágenes base (`python:3.11-slim` y
> `registry:2`), así que necesitas conexión para eso. Después el laboratorio no
> sale de tu máquina: la app, el registry y el tráfico son locales.

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

En el caso el «registry» eran las imágenes sueltas del servidor. Aquí es un
registry de verdad, en tu máquina:

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

> En el caso el tag salía del commit (`git rev-parse --short HEAD`). Aquí lo
> eliges tú para que el laboratorio no dependa de Git.

## Paso 2 · Construye la imagen

En el caso la imagen se construía en la laptop de Ana. Aquí se construye desde
la carpeta, para que salga del mismo sitio todas las veces:

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

## Paso 6 · Smoke test (la puerta que el caso no tuvo)

```bash
curl localhost:8080/
# PagosYA api v1
```

Si sale vacío, espera 2 segundos y repite: la app tarda en arrancar.

> En el caso lo detectó un **cliente** a los 10 minutos. Este `curl` prueba el
> **camino**: host:8080 → DNAT → contenedor:8000 → proceso → HTTP, y decide si
> el despliegue pasó.

## Paso 7 · Registra la última versión buena

```bash
echo "$TAG" > .last-good
cat .last-good
# v1
```

> Esto es lo que nadie tenía a las 17:00 del viernes: una respuesta escrita a
> «¿qué versión funcionaba?».

## Paso 8 · Rompe el despliegue (como el viernes)

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
ya está en el registry. En el caso eso tomó 3 h 50 min y costó 8 horas de pagos.

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
   Marca cuáles son del caso y cuáles ejecutaste.
3. **Evidencia**: salida de `_catalog`, el tag en `curl`, `docker port`/`ss`, el
   smoke en rojo y el tiempo del rollback.
4. **Postmortem del caso** (una página): línea de tiempo, los 5 porqués y las tres
   piezas que faltaban. Cierra comparando el caso con tu práctica: 3 h 50 min
   frente a tu rollback medido, y **qué flujo de red** falló en cada uno.

> Se evalúa la **explicación de red**, no la memorización: quien pega los
> comandos pero no sabe qué puerto abrió, no aprobó.
