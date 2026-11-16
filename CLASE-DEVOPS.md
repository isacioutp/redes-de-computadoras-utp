# Clase — DevOps sobre la red: el caso del despliegue del viernes (guion docente)

> **Punto del módulo:** sesión de **cierre e integración** (después de la Parte 4).
> No introduce herramientas nuevas ni scripts: se usa **Git + Docker + Compose**
> comando por comando, lo que ya se dictó en la Unidad III, y se le agrega lo que
> faltaba: **el camino del código hasta producción**.
>
> **Materiales que acompaña:** `Teoria-DevOps-Despliegue.pptx` (la teoría de esta
> sesión, 55 min · versión en texto `TEORIA-DEVOPS-DESPLIEGUE.md`),
> `Teoria-U3-Parte3-Orquestacion.pptx` (3.5),
> `Teoria-U3-Parte4-Almacenamiento-Compartido.pptx` (extensión 3.5) y el
> `Laboratorio-14-Red-Completa-Compose-PT` (stack con Compose y secretos).
>
> **Objetivo en una frase:** que el estudiante **haga a mano, paso por paso, el
> despliegue completo** y pueda **volver atrás en segundos** — entendiendo cada
> comando antes de que nadie lo meta en un script.
>
> **Sigue siendo una clase de redes.** El pipeline es el **escenario**, no el
> tema: lo que se estudia es el **tráfico** que hace posible un despliegue —
> qué puerto, en qué dirección, con qué cifrado, por qué subred — y qué se rompe
> cuando uno de esos flujos falla. El 502 del caso no es «un bug de DevOps»: es
> un proxy (o un puerto publicado) que no encuentra a nadie sano del otro lado.

---

## 1. Ficha de la clase

| Campo | Valor |
|-------|-------|
| Unidad | III — cierre / extensión (DevOps como operación de lo ya construido) |
| Tema | Pipeline de despliegue hecho a mano: artefacto inmutable, smoke test y rollback |
| Enfoque | **Redes**: los flujos del despliegue (puertos, NAT, subredes, DNS, cifrado). DevOps es el vehículo |
| Semana | 14+ (encaja en el bloque «caso práctico» del `CRONOGRAMA.md`) |
| Duración | **Una sesión de 165 min** (2 h 45 min) · recorte a 55 min en la sección 3 |
| Caso de estudio | **PagosYA en producción**: «el despliegue del viernes» (sección 4) |
| Entregable | Bitácora de los 10 comandos + evidencia del rollback + postmortem de una página |
| Insumo para el proyecto | **Manual de despliegue del Proyecto Final** (rúbrica de documentación) |

> Esta es una sesión **de cierre**, no contenido obligatorio nuevo: se ofrece como
> práctica para el Proyecto Final y para quien quiera llevar su stack del Lab 14
> a «producción».

### Objetivos de aprendizaje

Al terminar la sesión, el estudiante debe poder:

1. **Explicar** qué es DevOps sin nombrar una herramienta: un acuerdo de que el
   **mismo cambio** se despliega **igual** todas las veces, y se puede **revertir**.
2. **Diagnosticar** un despliegue manual a partir de su bitácora: qué versión
   corría, quién se enteró del fallo y cuánto tardó el rollback.
3. **Ejecutar a mano** el pipeline de 7 etapas con `git`, `docker build`,
   `docker push`, `docker compose` y **verificar por la red** con un smoke test
   que decide si el despliegue pasó o no.
4. **Provocar** un despliegue fallido y **volver a la versión anterior** con dos
   comandos, usando un tag inmutable, y medir el tiempo.
5. **Medir** el antes/después con las **4 claves DORA** (frecuencia, lead time,
   tasa de fallo y tiempo de recuperación) y conectarlas con la red.
6. **Trazar** los flujos del despliegue (origen → destino, puerto, protocolo,
   cifrado) y explicar qué se cae si se bloquea uno — con `ss`, `docker port` y
   `curl -v`, no de memoria.

### Requisitos previos (lo que ya vieron)

| Ya visto en… | Concepto que se reutiliza |
|--------------|---------------------------|
| 3.5 / Lab 14 | `compose.yml`, servicios, puertos, healthchecks |
| Lab 14 · Sesión 3 | Secretos fuera del código (`/run/secrets`) |
| Parte 4 | El dato no es desechable: volúmenes, respaldo y réplica |
| 3.1/3.2 | Puertos, NAT y monitoreo: el smoke test **es** una medición |
| Caso 2 (PagosYA) | El sistema del caso de estudio ya es conocido por el curso |

> **Regla de oro del docente:** DevOps **no** es una lista de herramientas ni un
> puesto de trabajo. Es la respuesta a una pregunta concreta: *«¿cómo hago este
> despliegue otra vez, igual, a las 4 de la tarde de un martes, sin que nadie
> rece?»*. Todo lo demás (registry, pipeline, métricas) existe para responderla.
>
> **Por qué a mano y sin script:** si el estudiante no ejecutó la secuencia con
> sus dedos, no sabe **qué** automatizar. El script no es magia: es esta misma
> lista de comandos, pegada. Primero se entiende; después se automatiza.

---

## 2. Materiales y preparación previa (30 min antes)

### En el host (docente)

```bash
# Imágenes que conviene tener ya descargadas
docker pull python:3.11-slim
docker pull registry:2

# Registro local para la clase (queda en localhost:5000)
docker run -d --name registro-clase -p 5000:5000 registry:2
curl -s localhost:5000/v2/_catalog      # {"repositories":[]} al inicio

# Verificar que hay git
git --version
```

> `localhost:5000` es el único caso en que Docker acepta un registry **sin TLS**
> sin configuración extra (`insecure-registries`). Por eso el registro de clase
> vive en `localhost` y no en una IP del tailnet.
>
> **Ojo con el `-p`:** `-p 5000:5000` publica en **todas** las interfaces. Para
> que solo tu máquina lo alcance, `-p 127.0.0.1:5000:5000` — comprobado: por la
> IP del host la respuesta es `000` (sin conexión). Es la segmentación de 3.1
> aplicada a un servicio: el registry no necesita estar en la LAN.

### En la pizarra / pantalla

- La **lista de los 10 pasos** de la sección 7, numerada (es el guion completo de
  la parte práctica; conviene dejarla proyectada).
- La **bitácora del incidente** de la sección 4, impresa o proyectada — es el
  caso de estudio completo; no hace falta otro material.

### Puntos de control (checkpoints) que se van a pedir

1. `curl -s localhost:5000/v2/_catalog` mostrando `pagosya-api`.
2. `curl localhost:8080/` devolviendo **el tag del commit** que se acaba de construir.
3. `cat .last-good` con ese mismo tag.
4. Un cambio roto que hace **fallar el smoke** (`curl` con error o con otro tag).
5. Volver al tag anterior con dos comandos, en **menos de 30 segundos**.

---

## 3. Estructura de la sesión (dos formas de dictarla)

### Opción 1 — Sesión completa (165 min)

| Bloque | Min | Qué se hace |
|--------|-----|-------------|
| 1 · Encuadre | 0-15 | Qué es DevOps y la prueba de fuego del despliegue |
| 2 · Caso de estudio | 15-40 | «El despliegue del viernes»: lectura y diagnóstico en parejas |
| 3 · Anatomía | 40-65 | Las 7 etapas y los 10 comandos que las ejecutan |
| 4 · Demo guiada | 65-95 | El docente hace los 10 pasos en vivo, sin prisa |
| 5 · Práctica | 95-130 | Cada estudiante repite los pasos en su terminal |
| 6 · El caso, resuelto | 130-150 | Despliegue roto → smoke falla → **rollback cronometrado** |
| 7 · Medición | 150-160 | Las 4 claves DORA antes/después del caso |
| 8 · Cierre | 160-165 | Entregable, checklist y conexión con el Proyecto Final |

### Opción 2 — Recorte a 55 min

| Bloque | Min | Qué se hace |
|--------|-----|-------------|
| 1 · Encuadre | 0-10 | Qué es DevOps (versión corta) |
| 2 · Caso de estudio | 10-30 | Bitácora + 3 preguntas de diagnóstico |
| 3 · Anatomía | 30-45 | Los 7 pasos esenciales, en pantalla |
| 4 · Demo | 45-52 | Un despliegue y un rollback ya ejecutados |
| 5 · Cierre | 52-55 | El entregable y la regla de las 4 claves |

> El resto del documento se lee **bloque por bloque**; sirve para cualquiera de
> las dos opciones.

---

## 4. Caso de estudio — «El despliegue del viernes»

> **Cómo usarlo:** se entrega la bitácora tal cual (impresa o proyectada) y se
> pide a las parejas que respondan las 6 preguntas **antes** de explicar nada.
> El objetivo no es adivinar el final, es encontrar **las piezas que faltaban**.

### Contexto

**PagosYA** es la API de pagos del Caso 2 del curso. La empresa es pequeña: tres
personas, un servidor con Docker y Compose, y ningún pipeline. Hasta hoy el
despliegue consiste en que **Ana** entre por SSH, haga `git pull` y ejecute
`docker compose up -d --build`. Funciona desde hace ocho meses.

### Bitácora del incidente (viernes 8 de noviembre)

| Hora | Qué pasó |
|------|----------|
| 15:30 | Se aprueba el PR «descuentos de temporada» y se fusiona a `main`. |
| 15:45 | Ana construye la imagen **en su laptop** y copia el `compose.yml` al servidor. |
| 16:10 | En el servidor: `git pull` + `docker compose up -d --build`. El build termina; la app nueva **arranca y se cae** a los segundos. |
| 16:20 | Primer reporte de un cliente: **error 502** al pagar. El `nginx` de adelante no tiene a quién reenviar. |
| 16:35 | Revisan el servidor: el contenedor **reinicia en bucle**. En la laptop de Ana funcionaba porque ahí las dependencias ya estaban; en el servidor el build no las fija. |
| 17:00 | Deciden «volver atrás». Nadie sabe qué imagen corría antes: todo se publicó como `latest` y ya se sobrescribió. |
| 17:40 | Intentan reconstruir desde el commit anterior. **No compila**: las dependencias no están fijadas y una versión nueva rompe la app. |
| 18:30 | Restauran el respaldo de la base de datos de las **2:00 a. m.**: se pierden **8 horas de pagos**. |
| 20:10 | El servicio queda estable. **Tiempo total caído: 3 h 50 min.** |

### Preguntas de diagnóstico (en parejas · 15 min)

1. **¿Qué versión estaba en producción a las 16:20?** ¿Cómo lo sabrían?
2. ¿Por qué la prueba de Ana pasó y la de los clientes no? ¿Qué **no** se probó?
3. ¿Quién detectó el fallo y cuándo? ¿Quién **debió** detectarlo?
4. ¿Por qué el rollback tardó 3 h 50 min? Nombra **dos** razones distintas.
5. ¿Por qué se perdió **dato** en un problema que empezó como un despliegue?
6. Nombra los **tres artefactos** que faltaban y en qué etapa vive cada uno.

### Respuestas guía

1. **No se sabe.** Esa es la respuesta. Sin un tag inmutable y un registro de lo
   desplegado, la versión en producción es una suposición.
2. Porque probó **su** build en **su** máquina. No se probó el artefacto que iba
   a correr en el servidor (otra arquitectura, otra base de imagen, otras
   dependencias) ni el sistema ya desplegado por el puerto real.
3. Lo detectó un **cliente**, 10 minutos después del despliegue. Debió detectarlo
   el **smoke test** del paso 6, antes de dar el despliegue por bueno.
4. (a) No había **tag anterior** al cual volver (`latest` lo pisó todo);
   (b) el «rollback» se intentó **reconstruyendo** desde el código, que no era
   reproducible. Volver atrás debe ser **elegir otra imagen que ya existe**, no
   volver a construir.
5. Porque el respaldo de la base de datos era el **único** plan de vuelta. Al no
   haber rollback de la aplicación, se pagó con datos. La Parte 4 lo dijo: el
   dato no es desechable.
6. **Imagen versionada** (build → registry), **`compose.yml` con el tag explícito**
   (deploy) y **registro de la última versión buena** (smoke → `.last-good`).

> **Cierre del caso (frase para dejar escrita):** el problema no fue el código
> del PR. Fue que **el despliegue no era una operación repetible**.

---

## 5. Encuadre — qué es DevOps (0-15 min)

Tres ideas, en este orden:

1. **La prueba de fuego:** *«¿puedes desplegar un martes a las 4 de la tarde y
   salir tranquilo?»*. Si la respuesta depende de **una persona** o de **una
   laptop**, no hay DevOps: hay una persona con un ritual.
2. **De qué se compone** (las 3 vías, en versión de clase):
   - **Flujo:** cambios pequeños y frecuentes, no un lanzamiento trimestral.
   - **Retroalimentación:** cada etapa dice en segundos si el cambio sirve
     (test, smoke test, monitoreo).
   - **Aprendizaje:** cuando falla, se documenta y se automatiza la lección
     (postmortem), no se busca culpable.
3. **Lo que NO es:** no es Kubernetes, ni una herramienta de moda, ni «el equipo
   de DevOps». En esta clase se hace **a mano, con Docker**, que ya saben.

> **Gancho con la red:** un despliegue es tráfico: `git` (22/443), el **push** al
> registry (5000/TCP), el **pull** de la imagen en el servidor, y el **smoke
> test** golpeando el mismo puerto que usan los clientes (8080 → 8000). Si la red
> está mal, el pipeline miente.

---

## 6. Anatomía del pipeline (40-65 min)

### Las 7 etapas y el comando que las hace

| # | Etapa | Qué garantiza | Comando de la clase |
|---|-------|---------------|---------------------|
| 1 | **Commit** | El cambio está identificado y versionado | `git rev-parse --short HEAD` |
| 2 | **Build** | La imagen se construye **desde el repo**, no desde una laptop | `docker build --build-arg APP_VERSION=$TAG -t ...` |
| 3 | **Test** | El artefacto es el que dice ser | `docker run --rm IMAGEN cat /app/VERSION` |
| 4 | **Registry** | El artefacto es **inmutable** y reutilizable | `docker push` + `v2/_catalog` |
| 5 | **Deploy** | Se despliega **un tag explícito**, no `latest` | `TAG=$TAG docker compose up -d` |
| 6 | **Smoke** | El sistema **responde como usuario**, no solo «arrancó» | `curl localhost:8080/` |
| 7 | **Registro / rollback** | Hay una versión anterior **conocida** a la cual volver | `echo $TAG > .last-good` |

### El mapa de tráfico del despliegue (el corazón de la clase)

Un despliegue son **cinco flujos**. Si uno se bloquea, el pipeline se cae **en esa
etapa**, y el mensaje de error lo delata: `connection refused` (nadie escucha),
`timeout` (algo descarta en el camino) o `502` (con un proxy delante: hay puerto,
pero no servicio detrás).

| # | Flujo | Origen → destino | Puerto / protocolo | Cifrado | Si se bloquea |
|---|-------|------------------|--------------------|---------|----------------|
| 1 | Código | tu host → servidor Git | 22/TCP (SSH) o 443/TCP | sí | no hay commit que desplegar |
| 2 | Push | Docker daemon → registry | 5000/TCP | no en clase (loopback) | el artefacto no sale de la laptop |
| 3 | Pull | servidor → registry | 5000/TCP | no en clase | compose no encuentra la imagen |
| 4 | Servicio | cliente → app publicada | 8080/TCP → 8000/TCP (**NAT**) | no (HTTP) | **RST / sin respuesta**: hay puerto, nadie escucha (con proxy delante: 502) |
| 5 | Interno | app → db (si el stack tiene base de datos, como el Lab 14) | 5432/TCP por la red del compose, DNS `db` | no | la app arranca y falla al conectar |

```
  tu host                         servidor (Docker)
┌────────────┐  22/443   ┌──────────────────────────────────────┐
│ git commit │──────────▶│ repo                                 │
│ build      │           │                                      │
│ push       │──5000────▶│ registry :5000 ──pull──▶ api :8000   │
└────────────┘           └───────────────────────────┬──────────┘
                                                     │ NAT 8080→8000
   usuario ────────────── 8080/TCP ─────────────────▶┘
```

> `8080 → 8000` es **DNAT**: el puerto del host se traduce al del contenedor. Es
> el mismo NAT de la Unidad II, con otra tabla (`iptables`/`nftables`) y otro
> comando para verla (`docker port`). Y `localhost` no es una dirección de red:
> es la **loopback**, por eso el registry de clase no necesita DNS y no se
> alcanza desde otra máquina.
>
> En la demo de esta clase se ejercitan los flujos **2, 3 y 4**; el 1 (git
> remoto) y el 5 (app → DB) ya los vieron en el Lab 14 — aquí se nombran para
> que el mapa quede completo.

### Las dos reglas que valen toda la clase

1. **Build once, deploy everywhere.** Se construye **una** imagen y esa imagen
   viaja; no se reconstruye en cada host. Un tag por commit (`0311133`) hace que
   «la versión que corre» tenga nombre y apellido.
2. **El smoke test es la puerta.** El despliegue **no** termina cuando el
   contenedor arranca: termina cuando el sistema responde por el puerto y con la
   versión correcta. Si el smoke falla, el despliegue **no** pasó, aunque
   `docker ps` diga `Up`.

### El diagrama (para la pizarra)

```
git commit ──▶ build ──▶ test ──▶ push ──▶ deploy ──▶ smoke ──▶ .last-good
    │            │         │        │         │          │            │
  versión     imagen    artefacto  registry  compose   ¿responde?   versión
  con nombre  desde     correcto   inmutable  con TAG   por 8080     anterior
              repo                                                       │
                    ┌──────────────────────────────────────────────────┘
                    ▼
        rollback (2 comandos): TAG=$(cat .last-good) + compose up -d
```

---

## 7. Paso a paso con Docker (65-95 min)

> **Cómo usarlo:** cada bloque se pega **tal cual** en la misma terminal. Cada
> paso empieza recalculando `TAG`, así que nunca se queda «viejo» aunque se
> equivoquen. Lo que se espera ver está en la línea `→`.
>
> **Atajo:** los tres archivos ya están en
> [`Laboratorio-15-DevOps-Despliegue/`](Laboratorio-15-DevOps-Despliegue/README.md).
> Se puede copiar (`cp -r Laboratorio-15-DevOps-Despliegue ~/pagosya-devops`) en
> vez de teclearlos; aquí se muestran para explicar cada línea.

### Paso 0 — El repo y el registry (10 min)

```bash
mkdir -p pagosya-devops/app && cd pagosya-devops
git init && git config user.email "estudiante@utp.ac.pa" && git config user.name "Estudiante"
```

`app/app.py` — la aplicación (17 líneas, sin dependencias):

```python
import http.server, pathlib
VERSION = pathlib.Path("/app/VERSION").read_text().strip()

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b"ok\n"
        else:
            body = f"PagosYA api {VERSION}\n".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *args):
        pass

http.server.HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
```

`app/Dockerfile` — el artefacto lleva su versión **horneada** dentro:

```dockerfile
FROM python:3.11-slim
ARG APP_VERSION=dev
WORKDIR /app
COPY app.py .
RUN echo "$APP_VERSION" > VERSION
EXPOSE 8000
CMD ["python", "app.py"]
```

`compose.yml` — el tag es explícito:

```yaml
services:
  api:
    image: localhost:5000/pagosya-api:${TAG:-dev}
    ports: ["8080:8000"]
    init: true
```

> `init: true` no es adorno: sin él, Python queda como **PID 1** y el kernel le
> ignora el `SIGTERM` del PID 1, así que `docker stop` espera **10 s** y mata a
> la fuerza. Con `init`, el rollback baja de ~12 s a **menos de 1 s** — el
> «volver en segundos» se sostiene en una línea del `compose.yml`.

```bash
git add -A && git commit -m "pagosya: pipeline inicial"
```

> `ARG APP_VERSION` se **hornea** en la imagen: cambiar el tag cambia el
> contenido. Por eso el smoke test puede comparar «lo que sirve» con «lo que se
> desplegó» y no hay forma de mentir. `${TAG:-dev}` permite arrancar sin pipeline,
> pero **en producción el tag siempre se pasa**. Nunca `latest`.

### Paso 1 — La versión tiene nombre (1 min)

```bash
TAG=$(git rev-parse --short HEAD); echo "$TAG"
```
→ `0311133` (el hash corto del commit; en su repo será otro)

### Paso 2 — Build desde el repo, no desde la laptop (3 min)

```bash
TAG=$(git rev-parse --short HEAD)
docker build --build-arg APP_VERSION="$TAG" -t "localhost:5000/pagosya-api:$TAG" app/
```
→ termina en `naming to localhost:5000/pagosya-api:0311133`

### Paso 3 — Test: el artefacto es el que dice ser (1 min)

```bash
TAG=$(git rev-parse --short HEAD)
docker run --rm "localhost:5000/pagosya-api:$TAG" cat /app/VERSION
```
→ `0311133` — **el mismo** tag. Si no coincide, se para aquí.

### Paso 4 — Push al registry: el artefacto ya no vive en la laptop (2 min)

```bash
TAG=$(git rev-parse --short HEAD)
docker push "localhost:5000/pagosya-api:$TAG"
curl -s localhost:5000/v2/_catalog
```
→ `{"repositories":["pagosya-api"]}`

> **Red:** un flujo **saliente** hacia `localhost:5000` — loopback, no pasa por la
> tarjeta de red. En producción sería `registry.empresa.com:443`: DNS + TLS +
> firewall. El comando es el mismo; lo que cambia es el camino.

### Paso 5 — Deploy con tag explícito (2 min)

```bash
TAG=$(git rev-parse --short HEAD)
TAG="$TAG" docker compose up -d
```
→ `Container pagosya-devops-api-1 Started`

> **Red:** Compose crea la red `pagosya-devops_default` (una `/16`, p. ej.
> `172.22.0.0/16`), le da IP al contenedor y **traduce** el 8080 del host al 8000
> del contenedor. El `TAG` viaja en la variable de entorno; si no se pasa, sube
> `dev` (y el smoke lo va a cantar).

### Paso 6 — Smoke test: la puerta (2 min)

```bash
curl -s localhost:8080/health
curl -s localhost:8080/
```
→ `ok` y `PagosYA api 0311133`

> Si el `curl` sale vacío, esperar 2 segundos y repetir (la app tarda en
> arrancar). **Si el tag que responde no es el que se desplegó, el despliegue no
> pasó** — aunque `docker ps` diga `Up`.
>
> **Red:** ese `curl` recorre el flujo 4 completo — `host:8080` → DNAT → `contenedor:8000`
> → proceso → HTTP. `docker ps` solo prueba que el proceso existe; el `curl`
> prueba el **camino**.

### Paso 7 — Registrar la versión buena (1 min)

```bash
TAG=$(git rev-parse --short HEAD)
echo "$TAG" > .last-good
cat .last-good
```
→ `0311133`

> Esto no es un script: es **un archivo de texto** con un tag. Es el «cartel en la
> puerta» que dice cuál era la última versión que pasó la puerta.

### Paso 8 — El cambio del viernes (5 min)

```bash
# la app ahora escucha en 9000, pero el compose sigue publicando 8000
sed -i 's/("0.0.0.0", 8000)/("0.0.0.0", 9000)/' app/app.py
git commit -am "viernes: cambio de puerto"
```

Y se repiten los pasos **2, 4 y 5** (build, push, deploy) con el tag nuevo:

```bash
TAG=$(git rev-parse --short HEAD)
docker build --build-arg APP_VERSION="$TAG" -t "localhost:5000/pagosya-api:$TAG" app/
docker push "localhost:5000/pagosya-api:$TAG"
TAG="$TAG" docker compose up -d
curl -sS --max-time 3 localhost:8080/
```
→ `curl: (56) Recv failure: ...` — **el smoke falla**

> Build OK, test OK, push OK, deploy OK… y aun así **no pasó**: la puerta es el
> paso 6, no el `docker ps`. Nada se escribió en `.last-good`.

### Paso 9 — Rollback: dos comandos, cero reconstrucción (1 min)

```bash
TAG=$(cat .last-good); echo "volver a $TAG"
TAG="$TAG" docker compose up -d
sleep 2; curl -s localhost:8080/
```
→ `PagosYA api 0311133` — la versión buena, de vuelta.

```bash
curl -s localhost:5000/v2/pagosya-api/tags/list
```
→ `{"name":"pagosya-api","tags":["0311133","faf2193"]}`

> Las dos versiones siguen en el registry: volver atrás es **elegir** una imagen
> que ya existe, no reconstruir desde el código. Por eso tarda segundos.

### Diagnóstico de red del despliegue (5 min)

Antes de tocar nada, mirar la red — estos cuatro comandos son la evidencia:

```bash
docker port pagosya-devops-api-1
# 8000/tcp -> 0.0.0.0:8080        ← la regla: 8080 del host, 8000 del contenedor

docker network inspect pagosya-devops_default \
  --format '{{range .IPAM.Config}}{{.Subnet}} gw {{.Gateway}}{{end}}'
# 172.22.0.0/16 gw 172.22.0.1

ss -ltnp | grep -E ':(5000|8080)'
# 0.0.0.0:8080 (app)  ·  127.0.0.1:5000 (registry, si se ató bien)

curl -v localhost:8080/ 2>&1 | grep -E 'Connected|HTTP'
# Connected to localhost port 8080 ... HTTP/1.0 200 OK
```

Y la pregunta que ordena todo: **¿quién inicia cada conexión?** El push y el pull,
tu daemon; el smoke, el cliente; hacia la base, la app. Ningún servicio «empuja»
datos sin que alguien abra la conexión: por eso un firewall que bloquea la
**salida** rompe un despliegue igual que uno que bloquea la **entrada**.

### Resumen de los 10 comandos (la lista que se lleva el estudiante)

| # | Comando | Etapa |
|---|---------|-------|
| 1 | `TAG=$(git rev-parse --short HEAD)` | commit |
| 2 | `docker build --build-arg APP_VERSION=$TAG -t IMAGEN app/` | build |
| 3 | `docker run --rm IMAGEN cat /app/VERSION` | test |
| 4 | `docker push IMAGEN` | registry |
| 5 | `TAG=$TAG docker compose up -d` | deploy |
| 6 | `curl localhost:8080/` | smoke |
| 7 | `echo $TAG > .last-good` | registro |
| 8 | `git commit -am "cambio"` | cambio nuevo |
| 9 | `TAG=$(cat .last-good) docker compose up -d` | rollback |
| 10 | `curl localhost:5000/v2/pagosya-api/tags/list` | auditoría |

---

## 8. Práctica de los estudiantes (95-130 min)

**Meta:** cada estudiante (o pareja) termina con el pipeline ejecutado **a mano**
y con la **evidencia** de un despliegue rojo y su rollback.

| Paso | Min | Qué hace |
|------|-----|----------|
| 1 | 15 | Repo, registry y los 3 archivos; primer commit |
| 2 | 15 | Pasos 1-4: tag, build, test y push (verificar el `_catalog`) |
| 3 | 10 | Pasos 5-7: deploy, smoke y `.last-good` |
| 4 | 20 | Paso 8: **romper a propósito** y ver el smoke fallar |
| 5 | 10 | Paso 9: rollback **cronometrado** (`time` opcional) |
| 6 | 10 | Llenar la tabla antes/después, **trazar los 5 flujos** (puerto y cifrado) y responder la sección 9 |

> **Reto de red (si sobra tiempo):** volver a levantar el registry con
> `-p 127.0.0.1:5000:5000` y comprobar con `ss -ltnp` y un `curl` por la IP del
> host que ya no responde. Explicar en una línea **por qué** y qué habría que
> abrir para compartirlo con un compañero.

### Tabla antes/después (la evidencia del entregable)

| Pregunta | Viernes (manual) | Con los 10 pasos |
|----------|------------------|------------------|
| ¿Qué versión corre? | No se sabe | El tag del commit |
| ¿Quién detecta el fallo? | El cliente | El smoke test |
| ¿Cuánto tarda el rollback? | 3 h 50 min | ≈ 2–5 s |
| ¿Se pierde dato al volver? | Sí (8 h) | No |
| ¿Se puede repetir igual? | Depende de quién | Sí: es una lista de comandos |

---

## 9. El caso, resuelto (130-150 min)

Con el pipeline ya roto y restaurado en la práctica, se vuelve a la bitácora y se
responde **con evidencia**, no de memoria:

1. **¿Dónde habría fallado el pipeline del viernes?**
   → En el **paso 6** (smoke): la app no responde por 8080. El despliegue se
   detiene **antes** de escribir `.last-good`.
2. **¿Qué se habría desplegado a las 16:20?**
   → Una imagen con tag del commit (`0311133`), guardada en el registry. Nada de
   `latest`.
3. **¿Qué habría hecho el rollback?**
   → Leer `.last-good`, cambiar el `TAG` del compose y volver a subir. Sin
   reconstruir, sin tocar la base de datos.
4. **¿Por qué no se pierde dato?**
   → Porque volver atrás es **cambiar de imagen**, no restaurar un respaldo. El
   respaldo sigue existiendo para desastres, no para cada despliegue (Parte 4).
5. **¿Qué automatiza un pipeline, entonces?**
   → **Exactamente esta lista.** Nada más. Un `deploy.sh` no sabe hacer magia: es
   estos comandos pegados en orden. Lo que agrega es que los corre **igual** a
   las 3 de la mañana, sin depender de quién esté despierto.

> **Para discutir:** si el rollback son dos comandos, ¿por qué el viernes tardó
> 3 h 50 min? Porque nadie sabía **cuál** era el tag bueno ni **dónde** estaba la
> imagen. El pipeline no arregla la falta de registro; la hace visible.

### Preguntas de red del despliegue (con respuestas)

Estas son las que se evalúan: no «qué comando», sino **qué pasa en la red**.

1. **¿Por qué desde otra máquina no funciona `push` a `localhost:5000`?**
   → Porque `localhost` es la loopback de **cada** máquina: la otra hablaría con
   su propio puerto 5000. Para compartirlo: publicar en la IP del host, abrir
   5000/TCP y declararlo `insecure-registry` (o ponerle TLS).
2. **El smoke da `Connection reset` y `docker ps` dice `Up`. ¿Qué capa falló?**
   → Ni DNS ni ruta: el proceso vive, pero escucha en 9000 mientras el DNAT
   apunta a 8000. El kernel del contenedor cierra con RST una conexión a un
   puerto sin listener. Es un problema de **puerto**, no de red lógica.
3. **¿Qué diferencia hay entre `docker port` y `ss -ltnp`?**
   → `docker port` muestra la **regla** que Docker programó (host → contenedor);
   `ss` muestra el **hecho**: qué escucha en el host y en qué interfaz. Si no
   coinciden, el despliegue miente.
4. **¿Por qué la app necesita DNS para `db` y no para el registry?**
   → `localhost` está en la loopback (no se resuelve); `db` lo resuelve el DNS
   embebido de Docker (127.0.0.11) dentro de la red del compose. Sin red
   compartida, `db` no existe como nombre — igual que un host sin DNS.
5. **Si el registry estuviera en otra VLAN, ¿qué habría que tocar?**
   → Dirección o DNS, regla de firewall (5000/TCP de salida desde el servidor) y
   **TLS** (Docker no habla HTTP plano salvo loopback o `insecure-registries`).
   Y la ruta entre subredes, que es el tema de toda la unidad.

---

## 10. Medición — las 4 claves DORA (150-160 min)

| Clave | Qué mide | Viernes | Con los 10 pasos |
|-------|----------|---------|------------------|
| **Frecuencia de despliegue** | Cada cuánto se pone algo en producción | 1 vez al mes | Cada commit |
| **Lead time** | Del commit a producción | Días (o semanas) | Minutos |
| **Tasa de fallo** | % de despliegues que fallan | 1 de 1 ese día | Se **mide** (el smoke lo decide) |
| **Tiempo de recuperación (MTTR)** | De la falla al servicio sano | 3 h 50 min | Segundos |

**Cómo se conecta con la red (el hilo del curso):**

- El **lead time** es, en buena parte, **tiempo de red**: construir, subir la
  imagen al registry y que el servidor la baje. Un registry lejano se paga en
  cada despliegue.
- El **smoke test** es una medición de 3.2 aplicada a un despliegue: latencia,
  código HTTP y contenido. Si el healthcheck tarda 4 s, el pipeline espera 4 s.
- El **MTTR** bajo no viene de la suerte: viene de tener el artefacto anterior
  **a un `pull` de distancia**, en el mismo registry.

> **Para la reflexión:** las 4 claves no se «mejoran» con una herramienta. Se
> mejoran **acortando el camino** entre el commit y el usuario, y haciendo que
> cada etapa avise sola. Es la misma idea de monitoreo de la Parte 1: medir para
> decidir, no para adornar el informe.

---

## 11. Cierre y entregable (160-165 min)

### Entregable (práctica de cierre, 100 pts sugeridos)

| Ítem | Pts | Qué se entrega |
|------|-----|----------------|
| Bitácora + mapa de flujos | 40 | Los 10 comandos con el tag real del repo, **y los 5 flujos** (origen → destino, puerto, cifrado, qué se rompe si se bloquea) |
| Evidencia | 30 | Capturas: `_catalog`, tag en `curl`, `docker port`/`ss`, deploy rojo en el smoke y rollback cronometrado |
| Postmortem del caso | 20 | Una página: línea de tiempo, **5 porqués**, las 3 piezas que faltaban |
| Métricas | 10 | Tabla antes/después de la sección 8 + el MTTR medido |

> Se evalúa **la explicación de red**, no la memorización de comandos: un
> estudiante que pega los comandos pero no sabe qué puerto abrió, no aprobó.

> El postmortem es **sin culpables**: se evalúa el **sistema**, no a Ana. Un buen
> postmortem nombra la pieza que faltaba, no a la persona que la olvidó.

### Checklist rápido antes de salir del aula

- [ ] `curl -s localhost:5000/v2/_catalog` muestra `pagosya-api`.
- [ ] `curl localhost:8080/` devuelve el **mismo tag** que se construyó.
- [ ] `cat .last-good` tiene ese tag.
- [ ] Un cambio roto hace **fallar el smoke**, no el build.
- [ ] El rollback (dos comandos) vuelve al tag anterior en **menos de 30 s**.
- [ ] Tabla antes/después completa y MTTR medido.
- [ ] Los **5 flujos** trazados con puerto, protocolo y cifrado.
- [ ] `docker port` y `ss -ltnp` mostrando la traducción 8080 → 8000.
- [ ] Postmortem con las 3 piezas faltantes: tag inmutable, smoke test, `.last-good`.

---

## 12. Errores frecuentes y cómo resolverlos en clase

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| `docker push` da `connection refused` | El registry no está corriendo | `docker run -d -p 5000:5000 --name registro-clase registry:2` |
| `docker push` da `denied` o `http` | Se usó una IP en vez de `localhost` | El registry de clase se usa como `localhost:5000` |
| El compose sube con la imagen `dev` | No se pasó `TAG` en la misma línea | `TAG="$TAG" docker compose up -d` |
| El smoke responde **otro** tag | El contenedor no se recreó | Repetir el paso 5; si persiste, `docker compose up -d --force-recreate` |
| El smoke no responde nada | La app aún arranca | Esperar 2 s y repetir el `curl` |
| `git rev-parse` falla | El repo no tiene commits | `git add -A && git commit -m inicial` |
| El rollback no cambia nada | Se pidió el mismo tag que ya corría | Es correcto: no había nada que revertir |
| `cat: .last-good: No such file` | Nunca hubo un despliegue verde | Completar los pasos 5-7 antes de romper nada |
| El puerto 5000 está ocupado | Otro servicio local (AirPlay, etc.) | Cambiar `-p 5001:5000` y el prefijo de la imagen a `localhost:5001` |
| El pipeline espera y falla | La app escucha en otro puerto | Comparar `EXPOSE`/puerto del compose con el `HTTPServer(...)` |
| La app arranca pero el smoke da 502 | El mapeo `8080:8000` no coincide con el puerto interno | Corregir el puerto en `compose.yml` |
| `localhost:5000` responde pero la IP del host no | El registry se publicó solo en `127.0.0.1` | `ss -ltnp`; para compartirlo, publicar en `0.0.0.0` y abrir 5000/TCP |
| `push` funciona y el `pull` desde otra máquina no | Registry en loopback o firewall | Misma red/VLAN, regla 5000/TCP y `insecure-registries` en el cliente |
| `Connection reset` en el smoke | La app escucha en un puerto que el DNAT no traduce | `docker port` + puerto del `HTTPServer` |

---

## 13. Conexión con el resto del curso

Esta clase **no enseña DevOps**: usa el despliegue como excusa para recorrer la
red que ya estudiaron. Cada etapa del pipeline es un flujo con dirección, puerto
y cifrado; cada falla del caso es una decisión de red mal tomada.

- **Hacia atrás:** la Parte 1 dio la red y la medición; la Parte 2, el acceso por
  llave y el bastión (el pipeline entra al servidor **por SSH con llave**, no con
  contraseña); la Parte 3, el sistema declarado en un archivo; la Parte 4, el dato
  que no es desechable.
- **Lo nuevo:** el **camino** entre el código y el usuario, y la capacidad de
  **volver atrás**. Nada de eso es una herramienta nueva: es orden.
- **Hacia el Proyecto Final:** la rúbrica pide **manual de despliegue** y **demo en
  vivo**. Esta bitácora de 10 comandos **es** ese manual: se entrega tal cual, con
  los tags reales del repo.
- **Límite consciente:** migraciones de base de datos y configuración (IaC). Se
  nombran; no se dictan en esta sesión.

---

## 14. Limpieza (recordar al cierre)

```bash
TAG=$(cat .last-good 2>/dev/null) docker compose down -v
docker rm -f registro-clase
docker rmi $(docker images 'localhost:5000/pagosya-api' -q) 2>/dev/null
```

---

**Referencias**

- `CLASE-U3-Parte3-Orquestacion.md` — Compose/Swarm, secretos y `stack deploy`
  (el despliegue antes de este pipeline).
- `Teoria-U3-Parte4-Almacenamiento-Compartido.pptx` — el dato y el respaldo.
- `Laboratorio-14-Red-Completa-Compose-PT/` — el stack que este pipeline despliega.
- `Proyecto-Semestral/ENUNCIADO.md` — rúbrica del manual de despliegue y la demo.
- Documentación oficial de Docker: *Registry*, *Compose file reference* y
  *docker build --build-arg*.
- Las 4 claves DORA: *Accelerate* (Forsgren, Humble, Kim) — resumen de las
  métricas de entrega de software.
