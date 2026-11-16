# Teoría — Unidad III · Sesión de cierre: DevOps sobre la red

> Contenido completo de [`Teoria-DevOps-Despliegue.pptx`](Teoria-DevOps-Despliegue.pptx) (17 diapositivas, 16:9).
> Volcado textual de la presentación: mismo contenido y mismo orden de
> lectura, sin depender de PowerPoint.
>
> Se regenera con:
> `python3 tools/dump_ppt_md.py Teoria-DevOps-Despliegue.pptx "Unidad III · Sesión de cierre: DevOps sobre la red"`
>
> Cada diapositiva conserva sus **notas del orador** al final, en bloques
> plegables: en GitHub y en la mayoría de editores se despliegan con un clic.

## Índice

- **1.** Unidad III — Sesión de cierre
- **2.** Qué vamos a ver
- **3.** ¿Qué es DevOps, en serio?
- **4.** DevOps no es una herramienta
- **5.** La prueba de fuego
- **6.** El despliegue del viernes
- **7.** PagosYA: el sistema y la costumbre
- **8.** La bitácora
- **9.** Lo que la bitácora revela
- **10.** Del commit a producción
- **11.** Las 7 etapas
- **12.** El laboratorio, en tu máquina
- **13.** El mapa de tráfico del despliegue
- **14.** La red detrás del despliegue
- **15.** El rollback: dos comandos
- **16.** Medir: las 4 claves DORA
- **17.** Qué se lleva de la sesión

---

## 1. Unidad III — Sesión de cierre

**UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES**

DevOps sobre la red: el despliegue del viernes

- Qué es DevOps: una definición que no nombra herramientas
- El caso: un despliegue manual que costó 3 h 50 min de servicio
- El laboratorio local: pipeline, puertos, NAT y rollback en dos comandos

<details><summary>Notas del orador</summary>

⏱ 0-2 min · Portada.

Abrir con la promesa: 'hoy no hay herramienta nueva; hoy el sistema que ya
construyeron recorre el camino hasta producción y aprende a volver atrás'.
Aclarar de entrada que sigue siendo una clase de redes: lo que se va a mirar
es el tráfico del despliegue, no una moda de la industria.

</details>

---

## 2. Qué vamos a ver

> Un caso real, una definición y el camino del código a producción

| # | Bloque | La pregunta que responde | Min |
|---|---|---|---|
| 1 | ¿Qué es DevOps? | ¿Por qué el mismo deploy sale distinto cada vez? | 14 |
| 2 | El caso del viernes | ¿Qué le faltaba al despliegue de PagosYA? | 14 |
| 3 | El pipeline y su red | ¿Qué puerto, en qué dirección, y cómo se vuelve atrás? | 22 |
| 4 | Medir y cerrar | ¿Cómo sabemos que mejoró? | 5 |

**La regla de esta sesión**
- **Sigue siendo un curso de redes.** El pipeline es el escenario; el tema es el tráfico.
- Cada etapa es un flujo con **origen, destino, puerto y cifrado**.
- Cada falla del caso es una **decisión de red** mal tomada: un puerto, una ruta, una versión.
- El **Laboratorio 15** corre entero en tu máquina con Docker: sin Git remoto y sin internet.
- **No se evalúa** memorizar comandos: se evalúa saber qué se abrió y por qué.

<details><summary>Notas del orador</summary>

⏱ 2-4 min · Agenda.

Enuncia los cuatro bloques y el peso: el caso ocupa tanto como la definición
porque el caso ES la clase. Si el tiempo aprieta, el bloque 4 se recorta a
una frase: 'se mide con DORA'.

</details>

---

## 3. ¿Qué es DevOps, en serio?

Antes de pipeline, registry y métricas: el acuerdo

- Las 3 vías: flujo, retroalimentación, aprendizaje
- La prueba de fuego del martes a las 4 de la tarde
- Lo que DevOps NO es

14 min

<details><summary>Notas del orador</summary>

⏱ 4-5 min · Transición al bloque 1.

</details>

---

## 4. DevOps no es una herramienta

> Es un acuerdo sobre cómo se cambia un sistema en producción

**Planear**
qué cambia

**Construir**
build

**Probar**
test

**Desplegar**
deploy

**Operar**
corre

**Medir**
DORA

**La definición que sirve**
- El **mismo cambio** se despliega **igual** todas las veces.
- Se **mide**: hay una prueba que dice si sirve.
- Se puede **revertir** sin drama.
- Si depende de una persona o de una laptop, no es DevOps.

**Las 3 vías (la parte cultural)**
- **Flujo:** cambios pequeños y frecuentes.
- **Retroalimentación:** cada etapa avisa en segundos.
- **Aprendizaje:** el fallo se documenta y se automatiza la lección.
- Nada de esto se compra: se acuerda.

**Lo que DevOps NO es**
- No es Kubernetes, ni una herramienta de moda, ni «el equipo de DevOps».
- En esta clase se hace **a mano y con Docker**, que ya saben: `build`, `push`, `compose`, `curl`.
- El ciclo completo y el **Git remoto** son **contexto**: el laboratorio solo ejecuta el tramo local.

<details><summary>Notas del orador</summary>

⏱ 5-13 min · Qué es DevOps.

Empieza por el ciclo de arriba, pero sin software: 'planear, construir, probar,
desplegar, operar, medir' es lo que hace un restaurante todas las noches.
La definición hay que leerla despacio; la frase que más discusión genera es
la última: 'si depende de una persona, no es DevOps'.
Las 3 vías en versión de clase, sin nombres de libros.
Cierra con el NO: desmonta la idea de que DevOps es un puesto de trabajo.
Deja claro qué se ejecuta y qué no: el laboratorio es Docker local; el ciclo
completo y el Git remoto se explican como contexto, no se montan.

</details>

---

## 5. La prueba de fuego

> ¿Puedes desplegar un martes a las 4 de la tarde y salir tranquilo?

| Pregunta | Viernes (manual) | Con pipeline |
|---|---|---|
| ¿Qué versión corre? | No se sabe | El tag del commit |
| ¿Quién detecta el fallo? | El cliente | El smoke test |
| ¿Cuánto tarda el rollback? | 3 h 50 min | ≈ 2 s |
| ¿Se pierde dato al volver? | Sí: 8 horas | No |
| ¿Se repite igual? | Depende de quién | Es una lista de comandos |

**La idea que ordena todo lo demás**
- **DevOps no se nota cuando todo va bien: se nota cuando hay que volver atrás.**
- Y volver atrás rápido no es suerte: es tener la versión anterior a un `pull` de distancia.

<details><summary>Notas del orador</summary>

⏱ 13-18 min · La prueba de fuego.

Esta tabla es el resumen del caso que viene; úsala como promesa, no como
respuesta. Pregunta al grupo: '¿alguno desplegó algo un viernes?'.
La caja azul es la frase que se llevan.

</details>

---

## 6. El despliegue del viernes

PagosYA · tres personas · un servidor · ningún pipeline

- 15:30 merge · 16:10 despliegue · 16:20 primer 502
- 17:00 «volver atrás» sin versión anterior
- 20:10 estable: 3 h 50 min caído

14 min

<details><summary>Notas del orador</summary>

⏱ 18-19 min · Transición al caso.

Decir que el caso es real en su forma: no importa la empresa, importa la
secuencia. Si alguien reconoce su propio trabajo, mejor.

</details>

---

## 7. PagosYA: el sistema y la costumbre

> La API de pagos del Caso 2, ahora con clientes de verdad

personas en el equipo

servidor con Docker

pipelines

meses funcionando así

**El sistema**
- `nginx` delante, la API de pagos detrás.
- PostgreSQL con su volumen `pgdata`.
- Un `compose.yml` y un servidor: nada más.

**La costumbre (8 meses)**
- Ana entra por SSH.
- `git pull` y `docker compose up -d --build`.
- «Si funciona en mi máquina, funciona».
- El despliegue **es** la persona.

**La deuda invisible**
- Funciona mientras nadie tenga prisa. El día que falla no hay versión anterior, ni prueba automática, ni registro de lo que corría.

<details><summary>Notas del orador</summary>

⏱ 19-22 min · Contexto.

Subraya los dos KPIs que importan: 1 servidor (no hay redundancia) y 0
pipelines (todo pasa por manos). Los otros dos son contexto.
La deuda invisible es el concepto: el costo no se paga hasta el incidente.

</details>

---

## 8. La bitácora

> Viernes 8 de noviembre · de 15:30 a 20:10

| Hora | Qué pasó |
|---|---|
| 15:30 | Se fusiona el PR «descuentos de temporada» a `main`. |
| 15:45 | Ana construye la imagen en su laptop y copia el `compose.yml`. |
| 16:10 | Servidor: `git pull` + `compose up -d --build`. La app arranca y se cae. |
| 16:20 | Primer cliente: 502 al pagar. `nginx` no tiene a quién reenviar. |
| 16:35 | La app reinicia en bucle: dependencias no fijadas. |
| 17:00 | «Volver atrás»: no hay versión anterior, todo era `latest`. |
| 17:40 | Reconstruir el commit viejo falla: no compila con las deps de hoy. |
| 18:30 | Restauran el backup de las 2:00 a. m.: 8 horas de pagos perdidas. |

**20:10 · servicio estable**
- **Tiempo total caído:** **3 h 50 min****. El código del PR no era el problema.**
- El problema fue que el despliegue no era una operación repetible.

<details><summary>Notas del orador</summary>

⏱ 22-28 min · La bitácora.

Léela como una historia, no como una tabla: 15:30 es una decisión normal;
16:20 es el cliente enterándose primero; 17:00 es el momento en que se dan
cuenta de que no tienen a dónde volver.
Pausa en 17:40: 'no compila' es la prueba de que construir desde el código no
es lo mismo que desplegar un artefacto.
No avances sin que alguien diga en voz alta qué pieza faltaba.

</details>

---

## 9. Lo que la bitácora revela

> Tres piezas que faltaban — y una consecuencia que se paga con datos

**Faltaba un tag inmutable**
- Todo se publicaba como `latest`.
- «La versión que corre» era una suposición.
- Un tag por commit la vuelve un hecho.

**Faltaba un smoke test**
- Lo detectó un cliente, no el sistema.
- `docker ps` decía `Up` mientras nadie pagaba.
- La puerta es la respuesta, no el proceso.

**Faltaba el registro**
- Nadie sabía cuál era la última buena.
- Sin registro no hay rollback: hay arqueología.
- Un archivo `.last-good` lo resuelve.

**Y la consecuencia que sí se paga**
- **Sin rollback de la aplicación, «volver atrás» fue restaurar la base:** **8 horas de pagos****. El dato no es desechable (Parte 4).**

<details><summary>Notas del orador</summary>

⏱ 28-33 min · El diagnóstico.

Pide las tres piezas antes de mostrarlas: casi siempre sale 'un backup' o
'probar mejor', que son síntomas, no la causa.
Aquí se enlaza con la Parte 4: el respaldo existe para desastres, no para
cada despliegue. Si el plan de vuelta es un backup, el diseño está mal.

</details>

---

## 10. Del commit a producción

Siete etapas, diez comandos y cinco flujos de red

- Build once, deploy everywhere
- El smoke test es la puerta
- El rollback elige una imagen que ya existe

22 min

<details><summary>Notas del orador</summary>

⏱ 33-34 min · Transición al bloque técnico.

</details>

---

## 11. Las 7 etapas

> Cada etapa deja una evidencia que se puede comprobar

| # | Etapa | Qué garantiza | Evidencia |
|---|---|---|---|
| 1 | Commit | El cambio está identificado | `TAG=v1` · en producción, `git rev-parse` |
| 2 | Build | La imagen sale del repo, no de una laptop | `docker build -t ...:$TAG` |
| 3 | Test | El artefacto es el que dice ser | `docker run ... cat /app/VERSION` |
| 4 | Registry | El artefacto es inmutable y reutilizable | `docker push` · `v2/_catalog` |
| 5 | Deploy | Se despliega un tag explícito, no `latest` | `TAG=$TAG compose up -d` |
| 6 | Smoke | Responde como usuario, no solo «arrancó» | `curl localhost:8080/` |
| 7 | Registro | Hay una versión anterior conocida | `echo $TAG > .last-good` |

**El pipeline no es magia**
- Son estos comandos, pegados en orden. Lo que agrega es que corren **igual** a las 3 de la mañana, sin depender de quién esté despierto.
- El flujo remoto de Git queda como **contexto**: aquí el tag lo eliges tú.

<details><summary>Notas del orador</summary>

⏱ 34-39 min · Las 7 etapas.

Recorre la columna 'Evidencia': cada etapa se puede comprobar sin creerle a
nadie. Ese es el punto de la clase.
La 3 es la que suele faltar en los proyectos: 'probé en mi máquina' no es test
del artefacto.
Aclara que la etapa 1 se hace con un tag elegido (v1, v2) para que el
laboratorio no dependa de Git; en producción el tag sale del commit.
Si hay tiempo, muestra el comando 1 y el 7 en pantalla: son una línea cada uno.

</details>

---

## 12. El laboratorio, en tu máquina

> Todo local con Docker: sin Git remoto y sin internet

```text
$ cp -r Laboratorio-15-DevOps-Despliegue ~/pagosya-devops
$ cd ~/pagosya-devops
$ docker run -d --name registry -p 127.0.0.1:5000:5000 registry:2
$ TAG=v1
```

**Local (se ejecuta)**
- `docker build`, `push`, `compose up -d`.
- Registry `registry:2` en `localhost:5000`.
- Smoke y rollback con `.last-good`.
- El tag lo eliges tú: `v1`, `v2`.

**Contexto (se explica, no se ejecuta)**
- **Git remoto / GitHub** (22 o 443/TCP) · **CI/CD** del equipo.
- El **ciclo DevOps completo** (planear, operar, medir, aprender) y las **métricas DORA**.
- Son el flujo 1 del mapa: existen en producción, no en esta práctica.

**Por qué es reproducible**
- Todo pasa en **loopback** y en la **red bridge** del compose: no hace falta internet ni un servidor.
- El `init: true` del `compose.yml` es lo que hace que el rollback tarde **menos de 1 s**.

<details><summary>Notas del orador</summary>

⏱ 39-41 min · El laboratorio.

Esta lámina es el puente entre la teoría y la práctica: muestra la carpeta,
el registry y separa lo que se ejecuta de lo que solo se explica.
Insiste en que no hay Git remoto: el tag es v1 y luego v2. Si alguien
pregunta por CI/CD, remítelo al flujo 1 del mapa y sigue.
El detalle de init:true se justifica al cronometrar el rollback: sin él,
docker stop espera 10 s porque Python es PID 1 e ignora SIGTERM.

</details>

---

## 13. El mapa de tráfico del despliegue

> Cinco flujos: si uno se bloquea, el pipeline se cae en esa etapa

| Flujo | Origen → destino | Puerto / protocolo | Si se bloquea |
|---|---|---|---|
| Código | tu host → servidor Git | 22 o 443/TCP | no hay commit |
| Push | daemon → registry | 5000/TCP | el artefacto no sale |
| Pull | servidor → registry | 5000/TCP | no encuentra la imagen |
| Servicio | cliente → app publicada | 8080 → 8000 · NAT | RST; con proxy, 502 |
| Interno | app → db | 5432/TCP · DNS `db` | arranca y falla al conectar |

**Los errores también son de red**
- `connection refused` = nadie escucha · `timeout` = algo descarta · `502` = el proxy no tiene upstream sano.
- **El flujo 1 (Git remoto) es contexto; aquí se ejercitan el 2, 3 y 4. El 5 (app → db) ya lo vieron en el Lab 14.**

<details><summary>Notas del orador</summary>

⏱ 41-46 min · El mapa de tráfico.

Esta es la lámina que justifica la sesión en el pénsum. Lee la fila 4 dos
veces: es el mismo NAT de la Unidad II, con otra tabla.
Pregunta: '¿quién inicia cada conexión?'. Ningún servicio empuja: alguien abre
la conexión. Por eso un firewall que bloquea la salida rompe el deploy igual
que uno que bloquea la entrada.
La fila 1 se nombra como contexto: en el laboratorio no hay servidor Git.

</details>

---

## 14. La red detrás del despliegue

> Donde el pipeline deja de ser DevOps y vuelve a ser el curso

**8080 → 8000 es DNAT**
- El puerto del host se traduce al del contenedor.
- Se ve con `docker port`.
- Es el NAT de la Unidad II: otra tabla, otro comando.

**`localhost` es loopback**
- `127.0.0.1`: no pasa por la tarjeta de red.
- No se alcanza desde otra máquina.
- Por eso el registry de clase no necesita DNS.

```text
$ docker port pagosya-devops-api-1
8000/tcp -> 0.0.0.0:8080
$ ss -ltnp | grep :8080
LISTEN 0.0.0.0:8080
```

**Pregunta que ordena todo**
- **¿Quién inicia la conexión?**
- Push y pull: el daemon. Smoke: el cliente.
- Hacia la db: la app.
- Sin conexión abierta no hay tráfico.

**Regla y hecho**
- `docker port` muestra la **regla**; `ss` muestra el **hecho**. Si no coinciden, el despliegue miente.

<details><summary>Notas del orador</summary>

⏱ 46-50 min · La red.

La caja de la pregunta es la evaluación: si el estudiante no sabe quién
inicia la conexión, no entendió el flujo.
Menciona el `-p 127.0.0.1:5000:5000`: el registry de clase queda solo local;
con `-p 5000:5000` queda expuesto en toda la máquina. Es segmentación (3.1).
No te detengas en TLS: se nombra y se sigue.

</details>

---

## 15. El rollback: dos comandos

> La versión anterior ya existe en el registry: no se reconstruye

```text
$ cat .last-good
0311133
$ TAG=$(cat .last-good)
$ TAG=$TAG docker compose up -d
Container pagosya-devops-api-1 Started
# menos de 1 s después
$ curl localhost:8080/
PagosYA api 0311133
```

```text
$ curl -s localhost:5000/v2/pagosya-api/tags/list
{"name":"pagosya-api","tags":
["0311133","faf2193"]}
```

**La versión mala no se borra**
- Queda en el registry como evidencia.
- Auditar es listar tags, no adivinar.

**Volver atrás es elegir, no reconstruir**
- **Por eso tarda segundos y no 3 h 50 min: el artefacto ya está a un `pull` de distancia.**
- `rollback.sh` no consulta al sistema roto: lee un archivo. Si el sistema caído dictara cómo volver, el rollback caería con él.

<details><summary>Notas del orador</summary>

⏱ 50-53 min · El rollback.

Si hay proyector y Docker, ejecuta los comandos: el 'Started' en segundos es
más elocuente que cualquier lámina.
El detalle del archivo es intencional: un rollback no debe depender de la
disponibilidad del sistema que está fallando.
La lista de tags cierra el argumento: la versión mala sigue ahí, pero no
está sirviendo.
El 'menos de 1 s' depende de init:true; sin él son ~12 s por el SIGTERM
ignorado por el PID 1. Es una línea del compose, no magia.

</details>

---

## 16. Medir: las 4 claves DORA

> Lo que no se mide no se mejora — el laboratorio deja medir el MTTR

**Frecuencia**
cada despliegue

**Lead time**
minutos

**Tasa de fallo**
la decide el smoke

**MTTR**
< 1 s

**Qué mide cada una**
- **Frecuencia:** cada cuánto se pone algo en producción.
- **Lead time:** del commit al usuario.
- **Tasa de fallo:** % de despliegues que no pasan la puerta.
- **MTTR:** de la falla al servicio sano.
- Antes: 1 al mes · días · 1 de 1 · 3 h 50 min.

**El hilo de redes**
- El **lead time** es, en buena parte, **tiempo de red**: subir y bajar la imagen.
- El **smoke test** es una medición de 3.2 aplicada a un despliegue.
- El **MTTR** bajo es tener el artefacto anterior a un `pull`.
- En el laboratorio solo se **cronometra el MTTR**; las otras tres son contexto.
- Las cuatro se mejoran acortando el camino, no comprando herramientas.

<details><summary>Notas del orador</summary>

⏱ 53-56 min · DORA.

No nombres el libro si no hace falta: las cuatro se explican solas.
La comparación 'antes/después' es la que se lleva al Proyecto: no se pide
número exacto, se pide tendencia y por qué.
Cierra el enlace con 3.2: el smoke es monitoreo aplicado a un despliegue.

</details>

---

## 17. Qué se lleva de la sesión

> Tres ideas, un entregable y una práctica

**El despliegue es una operación**
- Si depende de una persona o de una laptop, no es repetible.
- El tag `v1`/`v2` le pone nombre a lo que corre.
- Y ese nombre viaja: **build once**.

**La puerta es la respuesta**
- `docker ps` dice que el proceso existe.
- El smoke dice que el sistema sirve.
- Solo el segundo decide si el despliegue pasó.

**Volver es elegir**
- La versión anterior está en el registry.
- `.last-good` dice cuál es.
- Dos comandos; cero reconstrucción.

**Entregable y siguiente paso**
- **Bitácora del Laboratorio 15** (los 10 comandos) + mapa de los 5 flujos + postmortem de una página.
- Es, literalmente, el **manual de despliegue** que pide la rúbrica del Proyecto Final.
- Siguiente: `Laboratorio-15-DevOps-Despliegue/` — todo local con Docker, sin Git remoto.

<details><summary>Notas del orador</summary>

⏱ 56-57 min · Cierre.

Lee las tres cajas como las tres frases que deben poder repetir.
El entregable se explica en una línea: la bitácora es el manual.
Cierra con la práctica y el primer comando; recuerda que la carpeta del
laboratorio ya trae los archivos y no necesita internet.

</details>

---

