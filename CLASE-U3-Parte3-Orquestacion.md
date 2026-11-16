# Clase — Unidad III · 3.5 Orquestación de servicios (guion docente)

> **Punto del módulo:** cierre de la **Unidad III**. Cubre el tema **3.5
> (orquestación de servicios: Docker Compose y Docker Swarm)** y la **síntesis de
> toda la unidad** — semana 11 del `CRONOGRAMA.md`.
>
> **Materiales que acompaña:** presentación `Teoria-U3-Parte3-Orquestacion.pptx`
> (generada por `tools/build_parte3.py`; versión en texto en
> `TEORIA-U3-Parte3-Orquestacion.md`), laboratorio
> `Laboratorio-12-Orquestacion-Docker-Swarm` (`SESION-A.md` y `SESION-B.md`) y
> `GUIA-CLASE-UNIDAD-III.md`.
>
> **Objetivo en una frase:** que el estudiante pase de «corro un contenedor a
> mano» a **describir un sistema completo y mantenerlo funcionando solo**.

---

## 1. Ficha de la clase

| Campo | Valor |
|-------|-------|
| Unidad | III — Implementación de LAN y orquestación de aplicaciones |
| Tema | 3.5 Orquestación: Compose y Swarm (réplicas, balanceo y secretos) |
| Semana | 11 (dos clases) |
| Laboratorio | N.º 12 — Clase 1: 12A (Compose + Swarm) · Clase 2: 12B (secretos + stack) |
| Duración | Teoría 55 min + 2 sesiones prácticas (≈2 h 45 min cada una) |
| Entregable del lab | 100 pts (Sesión A 50 + Sesión B 50) |
| Insumo para el proyecto | **Proyecto Final** (stack orquestado + secretos + demo) |

### Objetivos de aprendizaje

Al terminar el punto, el estudiante debe poder:

1. **Definir** orquestación y nombrar sus **6 capacidades** (despliegue, escalado,
   descubrimiento, balanceo, auto-curación y secretos).
2. **Distinguir** Compose de Swarm y elegir la herramienta correcta según el
   alcance (un host vs. clúster).
3. **Escribir** un `compose.yml` que describa servicios, redes y dependencias, y
   **escalar** con `--scale` comprobando el balanceo por DNS.
4. **Desplegar** un servicio replicado en Swarm y explicar el **routing mesh** y
   la **auto-curación**.
5. **Gestionar secretos** fuera del código (`docker secret` → `/run/secrets`) y
   **actualizar sin caída** (rolling update / rollback / `stack deploy`).

### Requisitos previos (lo que ya vieron)

| Ya visto en… | Concepto que se reutiliza |
|--------------|---------------------------|
| Parte 1 (3.1/3.2) | La red segmentada y las métricas de monitoreo |
| Parte 2 (3.3/3.4) | Acceso por llave y bastión; secretos ≈ llaves, no contraseñas |
| Casos 1-3 | `docker network`, servicios por nombre, DB aislada |

> **Regla de oro del docente:** el objetivo **no** es memorizar sintaxis de YAML,
> sino entender que **el archivo es la fuente de verdad** del sistema y que el
> orquestador lo **mantiene** funcionando sin intervención manual.

---

## 2. Materiales y preparación previa (30 min antes)

### En el host (docente)

```bash
# Imágenes que conviene tener ya descargadas (evita perder clase esperando red)
docker pull nginx:alpine
docker pull postgres:15-alpine
docker pull redis:7-alpine
docker pull python:3.11-slim

# Verificar Docker, Compose y que el host no esté ya en un Swarm
docker version
docker compose version
docker info | grep -i swarm

# Limpiar restos de pruebas anteriores
docker service rm $(docker service ls -q) 2>/dev/null
docker swarm leave --force 2>/dev/null
```

### En la pizarra / pantalla

- El **diagrama Compose vs. Swarm**: un host que «se sabe todo» vs. varios nodos
  que «se descubren solos» por la red overlay.
- La tabla de las **6 capacidades del orquestador** (sección 4) — es casi literal
  el enunciado del proyecto.

### Puntos de control (checkpoints) que se van a pedir

1. `getent hosts api` devolviendo **3 IP** (balanceo por DNS de Compose).
2. `docker service ls` con `web-mesh` en **3/3**.
3. `curl http://localhost:9090/` respondiendo por el routing mesh.
4. Secreto montado: `cat /run/secrets/db_pass` dentro del contenedor.
5. `docker stack ps appfinal` con todas las tareas en *Running*.

---

## 3. Estructura de la clase (dos formas de dictarla)

### Opción 1 — Clase teórica (55 min) + prácticas aparte

| Bloque | Min | Qué se hace |
|--------|-----|-------------|
| Teoría 3.5 | 55 | Presentación `Teoria-U3-Parte3-Orquestacion.pptx` (diapositivas 1-12) |
| Sesión A | ≈120-165 | Lab 12A: Compose + Swarm (réplicas y balanceo) |
| Sesión B | ≈120-165 | Lab 12B: secretos + overlay + stack |

### Opción 2 — Bloque semanal (2 clases de 2 h 45 min)

| Clase | Min | Qué se hace |
|-------|-----|-------------|
| **Clase 1** | 55 + 110 | Teoría 3.5 + **Sesión A** (Compose y Swarm) |
| **Clase 2** | 55 + 110 | Repaso + **Sesión B** (secretos y stack) y cierre de la unidad |

> El resto de este documento se lee **bloque por bloque**, así que sirve para
> cualquiera de las dos opciones.

---

## 4. Guion teoría — Tema 3.5 (55 min)

> Alineado con las **notas del presentador** del PPT (que ya traen el minuto de
> cada diapositiva). Aquí está el *cómo contarlo*, no el texto de cada diapositiva.

### Encuadre (0-5 min)

- Abrir con la frase de convergencia: *«la Parte 1 dio la red, la Parte 2 el
  acceso seguro; hoy desplegamos a escala un sistema que se mantiene solo»*.
- Advertir el peso en el proyecto: la rúbrica del **Lab 12** se parece mucho a la
  del **Proyecto Final**.

### 3.5 · Orquestación (5-40 min)

| Min | Diapositiva / tema | Cómo contarlo |
|-----|--------------------|---------------|
| 5-6 | Transición a 3.5 | Hilo: qué es orquestar → Compose vs Swarm → `compose.yml` → nodos → réplicas → secretos → actualizaciones. |
| 6-11 | **Qué significa orquestar** | Pide un ejemplo real (un **restaurante**: si cae un mesero, otro toma la mesa → auto-curación). Leer en voz alta las **6 capacidades**: son los ítems de la rúbrica. Idea ancla: Compose responde *cómo levanto*; Swarm, *cómo lo mantengo*. |
| 11-16 | **Compose vs Swarm** | Anticipar el error «Compose no sirve para producción»: para una producción pequeña on-prem, **Swarm es suficiente**. No es Kubernetes ni pretende serlo. La tabla hay que saber rellenarla de memoria. |
| 16-22 | **`compose.yml`: el sistema en un archivo** | Recorrer el archivo línea por línea. El punto «oh» es que **`DB_HOST=db` funciona** por el DNS interno del proyecto. Advertencia: `--scale` falla si el servicio declara `container_name`. |
| 22-27 | **Nodos manager y worker** | Analogía: el manager es el **jefe de sala**, el worker el **mesero**. En Docker Desktop el nodo único es manager y worker a la vez. |
| 27-33 | **Réplicas, routing mesh y auto-curación** | La diapositiva que más impresiona: si se puede, demostrar en vivo (`curl` repetido cambia de nodo; matar una tarea y ver el 3/3 volver). Analogía del portero que reparte a las mesas con un solo número en la puerta. |
| 33-37 | **Secretos: fuera del código** | Vale 10 puntos solo en el Lab 12. Idea: la contraseña **nunca** en un archivo versionado. Detalle técnico clave: la app recibe `_FILE` y lee `/run/secrets/`, no la contraseña por variable. |
| 37-40 | **Rolling update, rollback y `stack deploy`** | Promesa que justifica Swarm: **cambiar y volver atrás**. Priorizar `stack deploy` y `rollback` si el tiempo aprieta; el detalle del rolling es secundario. |

### Cierre de la unidad (40-55 min)

| Min | Diapositiva / tema | Cómo contarlo |
|-----|--------------------|---------------|
| 40-48 | **Cierre de la unidad y del proyecto** | Volver a las **5 ideas** y amarrarlas: segmentar → proteger → exponer poco → escalar → medir. Repasar los **4 avances** del proyecto y decir dónde encaja cada uno. |
| 48-55 | **Autoevaluación y cierre** | Responder en voz alta 2-3 de las 10 preguntas. Leer la lista de tareas para la próxima clase (traer `compose.yml` y las capturas). |

---

## 5. Guion práctica — Sesión A: Compose y Swarm (12A)

**Meta:** levantar el stack, **escalar** y ver el **balanceo**; luego el routing mesh.
**Tiempo sugerido:** 15 min demo guiada + 60-90 min trabajo + 15 min cierre.

| Min | Etapa | Qué hace el docente / el estudiante |
|-----|-------|-------------------------------------|
| 0-20 | Pasos 1-2 en vivo | Stack `web/api/db/redis` con Compose; `up -d --scale api=3` y `getent hosts api`. |
| 20-35 | Paso 3 guiado | Logs y dependencias (`depends_on`); observar el arranque. |
| 35-55 | Pasos 4-5 | `swarm init`, `node ls` y servicio replicado `web-mesh` (3 réplicas, puerto 9090). |
| 55-75 | Paso 6 | Probar el **routing mesh** con `curl` repetido; observar la IP que responde. |
| 75-90 | Evidencias y preguntas | Capturas de `getent`, `docker service ls` y `curl`; preguntas 1-6. |

### Comandos núcleo (si el estudiante se pierde, dictarlos)

```bash
mkdir -p lab12 && cd lab12

cat > docker-compose.yml << 'YAML'
services:
  web:
    image: nginx:alpine
    ports: ["8080:80"]
    depends_on: [api]
    networks: [front]
  api:
    image: python:3.11-slim
    command: python -c "import time; print('API lista'); time.sleep(3600)"
    networks: [front, back]
  db:
    image: postgres:15-alpine
    environment: { POSTGRES_PASSWORD: labpass123 }
    networks: [back]
    volumes: [pgdata:/var/lib/postgresql/data]
  cache:
    image: redis:7-alpine
    networks: [back]
networks: { front: {}, back: {} }
volumes: { pgdata: {} }
YAML

docker compose up -d
docker compose up -d --scale api=3
docker compose exec web getent hosts api          # 3 IP → balanceo por DNS

# Swarm
docker swarm init --advertise-addr 127.0.0.1
docker node ls
docker service create --name web-mesh --replicas 3 --network ingress -p 9090:80 nginx:alpine
docker service ls                                 # web-mesh 3/3
for i in 1 2 3; do curl -s http://localhost:9090/ -o /dev/null -w "%{http_code} "; done; echo
```

### Preguntas de la Sesión A (con la respuesta esperada)

1. ¿Cuántos servicios y redes hay? ¿Cuál está en ambas redes?
   → Cuatro servicios (`web`, `api`, `db`, `cache`) y dos redes (`front`, `back`);
   `api` está en las dos porque es el puente entre frontend y backend.
2. ¿Cuántas IP devuelve `getent hosts api` con 3 réplicas? ¿Qué hace Compose?
   → Tres: el **DNS interno** resuelve el nombre `api` a las IP de las réplicas
   (balanceo básico; un load balancer dedicado sería nginx/haproxy).
3. ¿Qué orden impone `depends_on`? ¿Qué pasa si falla una réplica de `api`?
   → Arranca primero `db`; `depends_on` no reinicia por sí solo, pero Compose
   recrea las réplicas si se relanzan.
4. ¿Qué rol tiene el nodo? ¿Qué IP usa el plano de control?
   → `MANAGER` (y `ACTIVE`); la del `--advertise-addr`.
5. ¿Cuántas tareas corrió Swarm? Al hacer `curl`, ¿notas la IP?
   → Tres tareas; el **routing mesh** reparte y responde siempre por el 9090.
6. ¿Qué pasa si un contenedor de `web-mesh` muere?
   → El manager lo **recrea** (auto-curación) y vuelve a 3/3.

> **Error típico a vigilar:** `--scale` falla si un servicio declara
> `container_name`; y `docker compose` no administra un servicio de Swarm (para
> eso se usa `docker service`).

---

## 6. Guion práctica — Sesión B: secretos y stack (12B)

**Meta:** operar el Swarm en modo producción: **secretos, overlay, updates y stack**.
**Tiempo sugerido:** 15 min pasos 1-2 + 60 min pasos 3-5 + 15 min pasos 6-7.

| Min | Etapa | Qué demuestra |
|-----|-------|---------------|
| 0-15 | Pasos 1-2: secretos | `docker secret` montado en `/run/secrets/db_pass`; por qué no va en el YAML. |
| 15-30 | Paso 3: red overlay | `api-overlay` con 2 réplicas resolviéndose por nombre. |
| 30-50 | Paso 4: rolling update / rollback | Cambiar la imagen de a una y revertir sin caída. |
| 50-70 | Paso 5: `stack deploy` | Levantar el sistema completo con un comando (`appfinal`). |
| 70-90 | Pasos 6-7: comparativa + proyecto | Tabla de orquestación y metodología integradora. |

### Comandos núcleo

```bash
# 1 · Secretos (nunca en el YAML)
printf "labpass123" | docker secret create db_pass -
printf "admin"     | docker secret create db_user -
docker service create --name db-swarm --secret db_pass --secret db_user \
  --network ingress postgres:15-alpine sleep 3600
docker exec $(docker ps -qf name=db-swarm) sh -c 'cat /run/secrets/db_pass; echo'

# 2 · Red overlay + resolución por nombre
docker network create --driver overlay backoverlay
docker service create --name api-overlay --network backoverlay --replicas 2 \
  python:3.11-slim sleep 3600
docker exec $(docker ps -qf name=api-overlay) nslookup api-overlay

# 3 · Rolling update y rollback
docker service update --image nginx:1.25 web-mesh --update-delay 5s
docker service ps web-mesh
docker service rollback web-mesh

# 4 · Stack completo
docker stack deploy -c stack.yml appfinal
docker stack ps appfinal
curl http://localhost:8090/
```

> El `stack.yml` de la Sesión B es el Compose de la Sesión A con bloque `deploy:`
> (`replicas`, `update_config.order: start-first`, `placement.constraints`).

### Preguntas de la Sesión B (con la respuesta esperada)

1. ¿Dónde ve la app el secreto y por qué es mejor que una variable de entorno?
   → En `/run/secrets/`; no queda en la imagen ni en el YAML versionado.
2. Nombra 3 opciones para gestionar secretos.
   → Secreto de Swarm, `.env` local, vault/nube; justificar cuál usarían.
3. ¿Qué IP resuelve `api-overlay`? Diferencia overlay vs. bridge.
   → La de las réplicas en la red overlay; overlay cubre **varios nodos**, bridge
   es de un host.
4. Describe el rolling update: ¿de a una o todas a la vez?
   → De a una (`--update-parallelism`/`--update-delay`); si falla, se detiene y
   `rollback` vuelve a la versión anterior.
5. ¿Qué comando despliega el stack completo? ¿Qué muestra `docker stack ps`?
   → `docker stack deploy`; las tareas y su estado (`Running`).
6. ¿Qué significa `node.role == manager` para la DB?
   → Fijarla al manager (en multi-nodo, para datos/volúmenes persistentes).
7. ¿Cuándo elegirías Compose, Swarm o Kubernetes?
   → Según complejidad, número de servicios y necesidad de alta disponibilidad.
8. En la nube, ¿qué usarías (ECS/EKS/AKS/GKE) y qué rol juega Docker en CI/CD?
   → Orquestación administrada; Docker construye/publica las imágenes.
9. **Reflexión:** las 3 ventajas de orquestar y cómo se conectan con los Labs 10-12.
   → Respuesta abierta; se espera que ligue red (10), acceso (11) y escala (12).

> **Error típico a vigilar:** dejar la contraseña en `compose.yml` o en el
> `Dockerfile` (un `git grep admin123` en el repo ya es un incidente) y olvidar
> que la app debe leer `_FILE` desde `/run/secrets/`.

---

## 7. Autoevaluación / salida de clase

Preguntas que el estudiante debe poder responder **antes de irse**:

1. ¿Por qué una LAN plana se degrada al crecer? *(repaso 3.1)*
2. Diferencia **latencia**, **jitter** y **pérdida**. *(repaso 3.2)*
3. ¿Por qué el servidor nunca guarda la contraseña? *(repaso 3.3)*
4. ¿Qué gana un **dual-homed** frente a uno **single-homed**? *(repaso 3.4)*
5. ¿Qué problema resuelve el **routing mesh**?
6. Diferencia el **`scale` de Compose** del de **Swarm**.
7. ¿Por qué la contraseña va en `/run/secrets/` y no en el YAML?

**Respuestas guía:** (1) un único dominio de broadcast colapsa por tráfico y
expone servicios; (2) latencia = retardo, jitter = su variación, pérdida =
paquetes que no llegan; (3) solo usa la llave pública, que verifica firmas;
(4) dual-homed separa red pública e interna (puente de acceso), el single vive en
una sola red; (5) publica un solo puerto y reparte entre réplicas sin configurar
el código; (6) `docker compose --scale` es de un host, `docker service scale` es
de un clúster; (7) para no versionarla ni dejarla en la imagen.

---

## 8. Errores frecuentes y cómo resolverlos en clase

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| `--scale` da error | El servicio declara `container_name` | Quitar `container_name` y volver a escalar |
| `docker compose` no escala un servicio de Swarm | Compose ≠ Swarm | Usar `docker service scale web-mesh=3` |
| `getent hosts api` devuelve 1 IP | No se escaló / servicio en otra red | `--scale api=3` y mismo proyecto Compose |
| `docker swarm init` falla | El host ya está en un Swarm | `docker swarm leave --force` y reintentar |
| El puerto 9090 no responde | Servicio sin `-p` o no listo | Revisar `docker service ls` y esperar el 3/3 |
| El secreto no está en `/run/secrets` | No se pasó `--secret` al servicio | Recrear el servicio con `--secret db_pass` |
| `stack deploy` falla | El YAML usa claves de Compose no soportadas | Mover lo específico a `deploy:` |
| La app no conecta a la DB | Se puso la contraseña en una variable | Usar `_FILE=/run/secrets/...` |

---

## 9. Conexión con el resto del curso

- **Hacia atrás (lo que ya saben):** la Parte 1 dejó la red segmentada y medida; la
  Parte 2, el acceso seguro por llave y el bastión.
- **Es el cierre de la unidad:** las **5 ideas ancla** — segmentar (3.1), medir
  (3.2), proteger con llaves (3.3), exponer una sola puerta (3.4), escalar sin
  rehacer (3.5).
- **Hacia el proyecto:** esto es el **Proyecto Final** (semana 13, 15 %). La
  rúbrica pide **stack con ≥2 réplicas front/back y balanceo**, **secretos**,
  **manual de despliegue**, **documentación** (arquitectura + justificación),
  **demo en vivo** y **repositorio** con README.

---

## 10. Checklist rápido antes de salir del aula

- [ ] `compose.yml` con `web`, `api`, `db`, `cache` en `front`/`back`.
- [ ] `--scale api=3` y `getent hosts api` con **3 IP**.
- [ ] `docker swarm init` + `docker node ls`.
- [ ] `web-mesh` en **3/3** y `curl :9090` respondiendo (routing mesh).
- [ ] Secreto visible con `cat /run/secrets/db_pass`.
- [ ] Red **overlay** y `nslookup` del servicio resolviendo.
- [ ] Rolling update **y** rollback evidenciados.
- [ ] `stack.yml` desplegado (`docker stack ps appfinal` en *Running*, `curl :8090`).
- [ ] Tabla comparativa de orquestación + reflexión integradora.
- [ ] Respuestas a las preguntas de Sesión A (1-6) y Sesión B (1-9).

---

## 11. Limpieza (recordar al cierre)

```bash
docker service rm web-mesh db-swarm api-overlay 2>/dev/null
docker stack rm appfinal 2>/dev/null
docker secret rm db_pass db_user 2>/dev/null
docker compose down --remove-orphans -v
docker swarm leave --force
```

---

**Referencias**

- `Teoria-U3-Parte3-Orquestacion.pptx` — presentación de la clase (Parte 3).
- `TEORIA-U3-Parte3-Orquestacion.md` — versión en texto (con notas del orador).
- `GUIA-CLASE-UNIDAD-III.md` — reparto de las 3 partes, notas de uso y cierre.
- `Laboratorio-12-Orquestacion-Docker-Swarm/` — prácticas (`SESION-A.md`, `SESION-B.md`).
- `Proyecto-Semestral/ENUNCIADO.md` — Proyecto Final (stack orquestado + secretos).
- Documentación oficial de Docker: *Compose file reference*, *Swarm mode* y
  *Manage sensitive data with Docker secrets*.
- Recursos externos opcionales: [Docker Swarm cluster](https://devopscube.com/how-to-setup-and-configure-docker-swarm-cluster/)
  y [container clustering tools](https://devopscube.com/docker-container-clustering-tools/)
  (ver también `CLASE-U3-LAN-Monitoreo.md`, sección 12).
