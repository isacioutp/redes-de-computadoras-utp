# Teoría — Unidad III · Parte 3: Orquestación de servicios con Docker

> Contenido completo de [`Teoria-U3-Parte3-Orquestacion.pptx`](Teoria-U3-Parte3-Orquestacion.pptx) (12 diapositivas, 16:9).
> Volcado textual de la presentación: mismo contenido y mismo orden de
> lectura, sin depender de PowerPoint.
>
> Se regenera con:
> `python3 tools/dump_ppt_md.py Teoria/Teoria-U3-Parte3-Orquestacion.pptx "Unidad III · Parte 3: Orquestación de servicios con Docker"`
>
> Cada diapositiva conserva sus **notas del orador** al final, en bloques
> plegables: en GitHub y en la mayoría de editores se despliegan con un clic.

## Índice

- **1.** Unidad III — Parte 3
- **2.** Qué vamos a ver en esta parte
- **3.** Orquestación de servicios
- **4.** Qué significa orquestar
- **5.** Compose vs Swarm: no compiten entre sí
- **6.** compose.yml: el sistema entero en un archivo
- **7.** Los nodos de Swarm: manager y worker
- **8.** Réplicas, routing mesh y auto-curación
- **9.** Secretos: la contraseña fuera del código
- **10.** Actualizaciones continuas: rolling update y rollback
- **11.** Cierre de la unidad y del proyecto
- **12.** Autoevaluación y cierre

---

## 1. Unidad III — Parte 3

**UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES**

Orquestación de servicios con Docker

- Tema 3.5 · Docker Compose y Docker Swarm: réplicas, balanceo y secretos
- Laboratorio N.º 12 · Semana 11 · 2 sesiones
- Cierre de la unidad y del Proyecto Semestral

<details><summary>Notas del orador</summary>

⏱ 0-3 min · Apertura de la Parte 3.

Esta parte cierra la unidad y el proyecto. Todo lo anterior converge acá:
la red (Parte 1), el acceso seguro (Parte 2) y ahora el despliegue a escala.
Frase de apertura: 'hasta ahora vimos cómo se protege una máquina; hoy, cómo se despliega
un sistema completo que se mantiene solo'.

</details>

---

## 2. Qué vamos a ver en esta parte

> Un tema del programa, pero el que más se parece al trabajo real

| # | Tema del programa | Qué resuelve | Min |
|---|---|---|---|
| 3.5 | Orquestación: Compose y Swarm | Levantar y mantener un sistema de varios servicios | 40 |
| — | Cierre de la unidad | Repaso final, autoevaluación y rúbrica del proyecto | 15 |

**El problema que ataca**
- Una app real = web + api + db + cache + worker.
- 5 contenedores, 5 comandos, 5 redes… y algo falla a las 3 a.m.
- Un orquestador lo describe **una vez** y lo levanta siempre igual.

**Qué aporta (las 6 cosas del enunciado)**
- despliegue · escalado · descubrimiento de servicios
- balanceo de carga · auto-curación · **secretos**
- Las dos primeras son las que más se notan en la rúbrica.

**Dónde encaja este laboratorio en la unidad**
- Parte 1 (LAN y monitoreo) le da la red · **Parte 2 (SSH y bastión) le da el acceso seguro** · y la Parte 3 le da la forma de producción. Es el último laboratorio de la unidad.
- El Proyecto Semestral se evalúa **con esta misma rúbrica**: 100 puntos entre las dos sesiones del Lab 12.

<details><summary>Notas del orador</summary>

⏱ 3-5 min · Agenda.

Deja claro que esta es la parte con más peso en el proyecto: la rúbrica del Lab 12
y la del Proyecto Semestral se parecen mucho.
Las preguntas del Proyecto se responden con estos tres entregables en la mano.

</details>

---

## 3. Orquestación de servicios

De «un contenedor que corro a mano» a «un sistema que se despliega solo»

- Qué es orquestar y por qué dejó de ser opcional
- Compose: un archivo que describe el sistema entero
- Swarm: réplicas, balanceo, overlay y secretos

40 min

<details><summary>Notas del orador</summary>

⏱ 5-6 min · Transición a 3.5.

</details>

---

## 4. Qué significa orquestar

> Un contenedor es fácil; un sistema con varios, no

**Un solo contenedor:** `docker run` y listo. **Cinco contenedores con dependencias:** el orden importa, las redes importan, un reinicio a medias lo rompe todo.

| Herramienta | Modelo | Ejemplos |
|---|---|---|
| Orquestador de VMs | Máquina virtual | VMware vCenter, Proxmox |
| Orquestación en nube | Infraestructura como servicio | AWS EC2/ECS, Azure, GCP |
| Orquestación de contenedores | Contenedores | Docker Compose, Docker Swarm, Kubernetes |

**Las 6 capacidades del orquestador**
**Despliegue**  ·  una definición, muchos hosts
**Escalado**  ·  más réplicas sin tocar el código
**Descubrimiento**  ·  «api» resuelve a la IP del contenedor
**Balanceo**  ·  reparte tráfico entre réplicas
**Auto-curación**  ·  reinicia el que muere
**Secretos**  ·  contraseñas fuera del código y de la imagen

**Por qué Docker NO es solo «un contenedor»**
- El enunciado del Proyecto pide **replicación de contenedores**.
- Y la rúbrica del Lab 12 califica `docker service scale` y el routing mesh.
- Es decir: **se evalúa orquestación, no solo ejecución**.
- Un `docker compose up` bien hecho ya es una parte; el resto es Swarm.

**Idea ancla de toda la parte**
- **Compose responde «¿cómo levanto mi sistema?»  ·  Swarm responde «¿cómo lo mantengo funcionando si un nodo o un contenedor muere?».**

<details><summary>Notas del orador</summary>

⏱ 6-11 min · Qué es orquestar.

Pide un ejemplo de la vida real: un restaurante. Si un mesero cae, alguien más
toma su mesa. Eso es auto-curación. Si el restaurante tiene que cerrar porque
cayó el mesero, no hay orquestación.
Las 6 capacidades de la caja izquierda son literalmente los ítems de la rúbrica.
Merece la pena leerlas en voz alta: la evaluación las pide una por una.

</details>

---

## 5. Compose vs Swarm: no compiten entre sí

> Mismo archivo, distinto alcance

|  | Docker Compose | Docker Swarm |
|---|---|---|
| Alcance | Un solo host (dev / pruebas) | Múltiples nodos (cluster) |
| Réplicas | `docker compose up --scale api=3` | `docker service scale api=3` |
| Redes | Bridge por proyecto | Overlay entre nodos |
| Alta disponibilidad | No | Sí (roles manager / worker) |
| Balanceo | No (reparte por capacidades) | Sí (ingress mesh) |
| Secretos | Archivo `.env` (simple) | `docker secret` → `/run/secrets` |
| Uso típico | Desarrollo local | Producción simple / on-prem |

**La frase que resume la diferencia**
- Compose = **un** host que se sabe de memoria todo.
- Swarm = **varios** hosts que se descubren solos por la red overlay.
- El archivo es casi el mismo; el alcance es el que cambia.

**Cómo se usa en el Lab 12**
- Sesión A: stack `compose.yml` con `scale api=3` + `getent hosts api`.
- Sesión A: `swarm init` + servicio `web-mesh` con 3 réplicas.
- Sesión B: secretos, overlay, rolling update y `stack deploy`.

<details><summary>Notas del orador</summary>

⏱ 11-16 min · Compose vs Swarm.

Error clásico que conviene anticipar: 'Compose no sirve para producción'.
La respuesta honesta: para una producción pequeña, on-prem, Swarm es suficiente.
No es Kubernetes, y no pretende serlo; está en el programa porque es alcanzable.
La tabla de arriba es la que hay que saber rellenar de memoria.

</details>

---

## 6. compose.yml: el sistema entero en un archivo

> Servicios, redes, volúmenes y dependencias — declarado una vez

```text
services:
api:
image: feria/api:1.0
deploy:
replicas: 3          # ← escalado
environment:
- DB_HOST=db
depends_on:
- db
db:
image: postgres:16
environment:
- POSTGRES_PASSWORD_FILE=/run/secrets/db_pass
secrets:
- db_pass
secrets:
db_pass:
external: true
```

**Lo que declara un compose**
- **`services`** — qué corre y con qué imagen
- **`depends_on`** — el orden de arranque
- **`networks` / `volumes`** — aislamiento y datos
- **`secrets`****— contraseñas fuera del YAML**

**Por qué `DB_HOST=db` funciona**
- Compose crea una red propia del proyecto.
- El nombre del servicio es el **DNS** del otro contenedor.
- `api` no necesita saber la IP: escribe `db` y ya está.

**Escalado en una línea**
**$ docker compose up -d --scale api=3**
**$ getent hosts api**   # devuelve 3 IPs
- Las 3 IPs son las 3 réplicas. Eso es la prueba del ítem de rúbrica.

<details><summary>Notas del orador</summary>

⏱ 16-22 min · compose.yml.

Este es el archivo que van a escribir en la Sesión A. Recórrelo línea por línea.
Lo importante no es memorizar sintaxis: es entender que el archivo es la FUENTE
de verdad del sistema. Si está en el archivo, se puede repetir.
El descubrimiento por DNS (caja naranja) es el punto 'oh': no hay IP fijas.
Advertencia técnica: `--scale` falla si el servicio declara `container_name`.

</details>

---

## 7. Los nodos de Swarm: manager y worker

> El cluster se administra desde los managers y ejecuta en los workers

```text
$ docker swarm init --advertise-addr 10.0.1.5
Swarm initialized: current node is a manager.
$ docker node ls
ID       HOST   STATUS   ROLES
x7f2a*   node1  Ready    manager
b31c9    node2  Ready    worker
```

**El rol worker**
- Solo ejecuta lo que el manager le ordena.
- No decide nada; no acepta despliegues.
- Un worker que muere: el manager pone la réplica en otro.
- Un manager que muere: otro manager lo puede promover.

| Comparación | Compose | Swarm |
|---|---|---|
| Alcance | 1 host | N nodos |
| Alta disponibilidad | No | Sí |
| Balanceo | No | Ingress mesh |
| Secretos | `.env` | `/run/secrets` |
| Ideal para | Desarrollo | Producción simple |

**El rol manager**
- Recibe y guarda el **estado deseado** del cluster.
- Decide qué servicios corren y dónde.
- Es el que responde `docker service create`.
- Todos los managers se sincronizan entre sí.

<details><summary>Notas del orador</summary>

⏱ 22-27 min · Nodos Swarm.

La analogía que funciona: el manager es el jefe de sala (dice qué pasa),
el worker es el mesero (obedece). Si muere un mesero, otro toma su mesa.
Un dato útil: en Docker Desktop el nodo único es manager y worker a la vez.
En el laboratorio probablemente sea un solo nodo, pero el concepto es el que se evalúa.
Si hay tiempo, muestra `docker node ls` en vivo aunque sea un solo nodo.

</details>

---

## 8. Réplicas, routing mesh y auto-curación

> El corazón del tema 3.5: qué pasa cuando algo se muere

```text
$ docker service create --name web-mesh \
--replicas 3 -p 8080:80 feria/web:1.0
$ docker service ls
web-mesh  replicated  3/3  Running  1 minute ago
$ docker service ps web-mesh
ID  NODE   IMAGE         STATE
..  node1  feria/web:1.0  Running
..  node2  feria/web:1.0  Running
..  node3  feria/web:1.0  Running
```

**Cliente**
pide :8080

**Ingress mesh**
ruta virtual :8080

**Balanceo**
elige una réplica

**Respuesta**
convierte a la IP real

**Qué es el routing mesh**
- Un puerto publicado **una sola vez** en el nodo.
- La red interna reparte entre las réplicas sin que tú lo configures.
- El balanceo ocurre en la capa de red, no en el código.

**Auto-curación: la demostración que impresiona**
- Baja el número de réplicas: docker service scale web-mesh=2
- Mata un contenedor a la fuerza: docker kill <id>
- El manager detecta la falta y crea otra: vuelve a 3/3 en segundos.

<details><summary>Notas del orador</summary>

⏱ 27-33 min · Réplicas y routing mesh.

Esta es la diapositiva que más impresiona si la demuestras en vivo:
   curl -s localhost:8080 | grep server   (repite 5 veces, cambia el nodo)
   docker service rm web-mesh.3            (y al rato, 3/3 otra vez)
La analogía del ingress mesh: un número único en la puerta que tiene un portero
que reparte a las mesas. Tú no llamas a cada mesa.
Sin la demo en vivo, explica al menos qué hace el manager al detectar la baja.

</details>

---

## 9. Secretos: la contraseña fuera del código

> El ítem que más se olvida y más se pide

| Dónde NO va la contraseña | Por qué |
|---|---|
| En el `Dockerfile` (`ENV`) | Queda en la imagen; cualquiera que la use la ve |
| En `compose.yml` en claro | El archivo se versiona y termina en el repo |
| En el comando de ejecución | Queda en el historial de shell |
| En una variable de build | Se imprime en los logs de construcción |

```text
$ docker secret create db_pass /ruta/credencial
$ docker service create --name db-swarm \
--secret db_pass \
-e POSTGRES_PASSWORD_FILE=/run/secrets/db_pass \
postgres:16
$ docker service exec db-srv cat /run/secrets/db_pass
```

**Cómo funciona el secreto en Swarm**
1. Se crea una vez y queda cifrado en el raft.
2. El manager lo envía solo a quien lo pide.
3. En el contenedor aparece como archivo en **`/run/secrets/`**
4. La app lo lee con la variable **`_FILE`**, no con la contraseña.
- Se puede rotar sin reconstruir la imagen.

<details><summary>Notas del orador</summary>

⏱ 33-37 min · Secretos.

Este ítem vale 10 puntos solo en el Lab 12 y aparece en el proyecto.
La idea que hay que transmitir: la contraseña NUNCA está en un archivo que se
versiona. Un `git grep admin123` en el repo ya es un incidente de seguridad.
El detalle técnico `_FILE` es lo que hace limpio el patrón: la app no recibe la
contraseña por variable de entorno, la lee de un archivo montado.
El detalle técnico `_FILE` es lo que hace limpio el patrón.

</details>

---

## 10. Actualizaciones continuas: rolling update y rollback

> Cambiar la versión sin caída, y volver atrás si algo sale mal

```text
$ docker service update --image feria/web:2.0 \
--update-parallelism 1 \
--update-order start-first web-mesh
#Swap automático: 1 antigua, 1 nueva, a la vez
$ docker service ps web-mesh
web-mesh.1  web:2.0  Running  0 seconds ago
web-mesh.2  web:2.0  Running  0 seconds ago
web-mesh.3  web:1.0  Running  1 minute ago
# Si la 2.0 sale mal:
$ docker service rollback web-mesh
```

**Actualización progresiva (rolling)**
- Nunca se tiran las 3 réplicas a la vez.
- Se reemplaza de a una; el servicio nunca se cae.
- Si una falla, el despliegue se detiene solo.

**Rollback: una orden, al estado anterior**
- Swarm guarda el estado previo de cada servicio.
- Volver atrás es tan simple como avanzar.
- Es la diferencia entre operar y administrar.

**`stack deploy`: el archivo completo, a producción**
**$ docker stack deploy -c compose.yml appfinal**
- Levanta el **sistema entero** (servicios + redes + secretos) con un comando.
- `docker stack ls` lo muestra como un solo conjunto.
- Es el entregable de la Sesión B del Lab 12.
- `docker stack rm appfinal` lo deshace completo.

<details><summary>Notas del orador</summary>

⏱ 37-40 min · Rolling update y stack.

Termina el tema 3.5 con la promesa que justify Swarm: se puede cambiar y volver atrás.
La analogía: es un hotel con varias habitaciones; puedes remodelingar una a la vez
y, si el resultado no gusta, volver a la habitación anterior.
Si el tiempo está corto, prioriza `stack deploy` y el rollback; el rolling es el detalle.
El rolling update es lo que evita la caída durante el cambio de versión.

</details>

---

## 11. Cierre de la unidad y del proyecto

> Repaso final de las tres partes y qué se entrega

| Parte | Tema | Concepto ancla | Lab |
|---|---|---|---|
| 1 | 3.1 · LAN | Segmentar: la red se mide y se aísla | Lab 10 |
| 1 | 3.2 · Monitoreo | Mbits, latencia, jitter, pérdida | Lab 10 |
| 2 | 3.3 · Claves SSH | La privada no sale; la pública autoriza | Lab 11 |
| 2 | 3.4 · Bastión | Una sola puerta; interna sin salida | Lab 11 |
| 3 | 3.5 · Orquestación | Un archivo, N réplicas, auto-curación | Lab 12 |

**Los 4 entregables del proyecto (Avances 1-4)**
- **Avance 1:** LAN, subredes VLSM, DHCP/DNS/NAT
- **Avance 2:** Bastión dual-homed + app interna sin exposición
- **Avance 3:** Claves SSH funcionando (sin contraseñas)
- **Avance 4:** Orquestación: réplicas, secretos y stack

**El hilo que lo cose todo**
- **Segmentar** (3.1) para que la red sea medible y segura.
- **Proteger el acceso** (3.3) con llaves, no con secretos.
- **Exponer solo lo necesario** (3.4) detrás de un bastión.
- **Escalar sin rehacer** (3.5) con réplicas y secretos.
- Todo lo anterior, medido (3.2) con las cuatro métricas.

<details><summary>Notas del orador</summary>

⏱ 40-48 min · Cierre de la unidad.

Diapositiva de consolidación: vuelve a las 5 ideas y las amarra.
Si tienes que resumir la unidad en una frase: 'una red que se segmenta, se protege,
se expone por un solo punto y se mantiene sola'.
La tabla de la izquierda es un buen resumen para el examen.
Repasa que el hilo narrativo sea: se segmenta, se protege, se expone poco, se escala.

</details>

---

## 12. Autoevaluación y cierre

> Diez preguntas para comprobar que la unidad quedó

**Repaso por tema (responde en voz alta)**
**3.1 ·** ¿Por qué una LAN plana se degrada al crecer?
**3.2 ·** Diferencia latencia, jitter y pérdida.
**3.3 ·** ¿Por qué el servidor nunca guarda la contraseña?
**3.4 ·** ¿Qué gana un dual-homed frente a uno single-homed?
**3.5 ·** ¿Qué problema resuelve el routing mesh?
**3.5 ·** Diferencia entre `scale` de Compose y de Swarm.
**3.5 ·** ¿Por qué la contraseña va en `/run/secrets/` y no en el YAML?
**— ·** Nombra las 4 métricas de red del tema 3.2.

**Cómo se evalúa (para que no haya sorpresas)**
- Unidad III = Lab 10 + Lab 11 + Lab 12 (100 pts c/u).
- El Proyecto Semestral usa rúbrica aparte, **por avances**.
- Se entrega: compose.yml, stack.yml, evidencias de réplicas,
- capturas de SSH por llave, tabla de comparación y reflexión.

**Para la próxima clase**
- Trae **compose.yml** y **stack.yml** funcionando.
- Trae las dos capturas de SSH (con y sin llave autorizada).
- Repasa los comandos: `scale`, `service update`, `rollback`, `stack deploy`
- Dudas antes de empezar: es más barato que reprobar.

<details><summary>Notas del orador</summary>

⏱ 48-55 min · Autoevaluación y cierre.

Deja que respondan en voz alta: la pregunta de 'difference entre scale de Compose y
de Swarm' es la que mejor separa a quien entendió de quien memorizó.
Lee la caja de abajo con calma: es la lista de tareas para la próxima clase y
evita que el cierre termine en un 'nos vemos' sin rumbo.

</details>

---

