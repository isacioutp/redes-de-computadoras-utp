# Laboratorio N.º 14 — De la red real a la red virtual: LAN completa + orquestación con Compose

Semana 10-11 · Unidad III · **4 sesiones** (1 clase cada una)

> **Laboratorio integrador** que fusiona los Labs N.º 10, 11 y 12. Se organiza
> en **dos pistas que no se afectan entre sí**:
>
> | Pista | Carácter | Documentos |
> |-------|----------|------------|
> | **A · Docker Compose** | **Obligatoria** (es la nota del laboratorio) | [SESION-1.md](SESION-1.md) · [2](SESION-2.md) · [3](SESION-3.md) · [4](SESION-4.md) |
> | **B · Packet Tracer** | **Opcional e independiente** (no influye en la pista A) | [PACKET-TRACER.md](PACKET-TRACER.md) |
>
> **Sesiones de la pista A** (cada una con su propio entregable):
>
> | Sesión | Tema | Guía |
> |--------|------|------|
> | 1 | Primer stack con Compose + segmentación y DNS | [SESION-1.md](SESION-1.md) |
> | 2 | Monitoreo de la red y acceso seguro | [SESION-2.md](SESION-2.md) |
> | 3 | Orquestación con Docker Compose (escalado, secretos, healthchecks) | [SESION-3.md](SESION-3.md) |
> | 4 | Integración, respaldo de datos y demo del stack | [SESION-4.md](SESION-4.md) |

## 🧭 Es un curso de redes: la red del data center, orquestada

Este es un laboratorio de **Redes de Computadoras**, no de DevOps. El objeto de
estudio sigue siendo **la red**: direccionamiento y subredes, segmentación,
enrutamiento, DNS, puertos/NAT, monitoreo y seguridad de borde. Lo que cambia es
el **medio**: en lugar de *dibujar* los hosts, los **ejecutamos** con Docker
Compose para poder **ver la red funcionando de verdad**.

> **Docker Compose es el medio; la red es el tema.** Cada línea del YAML existe
> para demostrar un concepto de red: las `networks` son **segmentación**
> (VLAN ↔ red bridge), `internal: true` es **subred sin salida**, `expose` vs
> `ports` es **puertos y NAT**, el DNS interno es **resolución de nombres**, el
> escalado es **balanceo de capa 4/7** y el bastión es **seguridad de borde**.

### Anclaje de redes por sesión (el hilo del curso)

| Sesión | Concepto de RED (lo que se aprende) | Capa OSI | Cómo se ve en Compose | Evidencia |
|--------|-------------------------------------|:--------:|------------------------|-----------|
| 1 | Segmentación, subredes, DNS, puertos vs NAT | 2-3-7 | `networks`, `internal`, `ports`/`expose` | `web↛db`, `nslookup` |
| 2 | Monitoreo (ancho de banda, latencia) y acceso seguro | 1-4 | `tcpdump`, `iftop`, SSH por llave | captura + login sin password |
| 3 | Descubrimiento de servicios, balanceo, aislamiento de credenciales | 4-7 | `--scale`, DNS embebido, `secrets` | `nslookup` + `/run/secrets` |
| 4 | Red en operación: disponibilidad, respaldo, diagnóstico | todas | `up --wait`, self-healing | `ps (healthy)` + dump/restore |

### Eje de ejecución (el medio): orquestar con Compose

El laboratorio **arranca con Compose** y lo usa como hilo: cada sesión agrega un
peldaño a la misma escalera.

| Sesión | Aporte al eje | Piso de la escalera |
|--------|---------------|---------------------|
| 1 | Primer `docker compose up` + segmentación + DNS | declarar el entorno |
| 2 | Verificación de segmentación + monitoreo + acceso | operar los servicios |
| 3 | **Orquestación**: réplicas, secretos, healthchecks, dependencias | reconciliar el estado deseado |
| 4 | Reproducir, respaldar y recuperar con un comando | operar el stack |

**Material de refuerzo del medio:** [REFUERZO-ORQUESTACION.md](REFUERZO-ORQUESTACION.md)
(se hace tras la Sesión 2 y se repasa antes de la Sesión 4).

> **Swarm queda fuera de ejecución** (solo 5 min de teoría al cerrar la Sesión 3):
> es el siguiente peldaño, no el de hoy.

## 🔀 Pista B (opcional) — Packet Tracer, independiente

La pista de **Packet Tracer** es **autónoma**: tiene su propio objetivo, sus
propios pasos, su propio entregable y su propia evaluación. **No influye en la
nota de las sesiones de Compose**, y estas **no la requieren** para nada.

- Se puede hacer **antes, después o sin** la pista A.
- Si el docente la asigna, se califica **por separado** (ver
  [EVALUACION.md](EVALUACION.md) §"Pista B").
- Su valor es didáctico: **ver** la red que Compose abstrae (subredes, bastión,
  ACL, Simulation mode). Es una *lupa*, no un requisito.

| Pista A (Compose, obligatoria) | Pista B (PT, opcional) |
|--------------------------------|------------------------|
| Se evalúa con la nota del lab | No afecta la nota del lab |
| Requiere Docker | Requiere Packet Tracer |
| Entregables por sesión | Un único entregable propio |

## Documentación del laboratorio

| Documento | Para quién | Contenido |
|-----------|-----------|-----------|
| [REPARTO-SESIONES.md](REPARTO-SESIONES.md) | Ambos | **Plan de reparto**: qué va en cada sesión, tiempos, entregables y balance |
| [SESION-1.md](SESION-1.md) · [2](SESION-2.md) · [3](SESION-3.md) · [4](SESION-4.md) | Estudiante | Pasos, comandos y entregable de cada clase (**independientes**) |
| [sesion-1/](sesion-1/README.md) · [2](sesion-2/README.md) · [3](sesion-3/README.md) · [4](sesion-4/README.md) | Estudiante | **Archivos Docker de cada sesión** (punto de partida listo para `up`) |
| [PACKET-TRACER.md](PACKET-TRACER.md) | Estudiante | **Pista B** (opcional/independiente): topología, bastión, ACL y preguntas |
| [TEORIA.md](TEORIA.md) | Estudiante | Teoría consolidada (LAN, monitoreo, SSH/bastión, Compose) |
| [REFUERZO-ORQUESTACION.md](REFUERZO-ORQUESTACION.md) | Estudiante | **Eje del lab**: entrenamiento focalizado en Compose (drills + depuración) |
| [DIAGRAMAS.md](DIAGRAMAS.md) | Estudiante | Diagramas Mermaid (Compose, flujos y —opcional— PT) para draw.io |
| [GUIA-ESTUDIO.md](GUIA-ESTUDIO.md) | Estudiante | Repaso + banco de preguntas con respuestas |
| [EVALUACION.md](EVALUACION.md) | Ambos | Rúbrica por sesión, pista B aparte, anti-copia y checklist |
| [DOCENTE/GUIA-DOCENTE.md](DOCENTE/GUIA-DOCENTE.md) | **Docente** | Guion minuto a minuto de las 4 sesiones y errores frecuentes |
| [DOCENTE/SOLUCIONES.md](DOCENTE/SOLUCIONES.md) | **Docente** | Compose de referencia, respuestas y (opcional) configuración del `.pkt` |

> Los documentos de `DOCENTE/` **no se publican** al estudiante.

## 📁 Archivos Docker por sesión (cómo arrancar)

Cada sesión tiene su **carpeta con los archivos Docker que necesita**, lista para
`docker compose up` y **sin depender** de las otras:

| Carpeta | Punto de partida | Arranque |
|---------|------------------|----------|
| [`sesion-1/`](sesion-1/README.md) | Red plana → segmentada | `docker compose up -d` |
| [`sesion-2/`](sesion-2/README.md) | Stack ya segmentado | `docker compose up -d` |
| [`sesion-3/`](sesion-3/README.md) | Stack segmentado (+ `db_pass.txt`) | `docker compose up -d` |
| [`sesion-4/`](sesion-4/README.md) | Stack ya orquestado | `docker compose up -d --wait` |

```bash
# Ejemplo: hacer la Sesión 2 de forma aislada
cp -r sesion-2 ~/lab14/sesion-2 && cd ~/lab14/sesion-2
docker compose up -d
```

> **Subredes fijas:** este lab usa `172.28.10.0/24` (front) y `172.28.20.0/24`
> (back). Baja una sesión (`docker compose down -v`) antes de levantar otra para
> evitar el solapamiento de subredes.


## Idea central del laboratorio

Durante todo el curso los estudiantes montaron redes con `docker network`,
bastiones con contenedores, DNS interno… pero **nunca vieron la red**. Las
"subredes" eran líneas de un archivo YAML y el "bastión" era un contenedor que
comparte kernel con todo lo demás.

Este laboratorio resuelve eso con **dos pistas independientes**:

| Pista | Qué modela | Por qué |
|-------|-----------|---------|
| **A · Docker Compose** (Sesiones 1-4, **obligatoria**) | El **data center**: frontend, API y base de datos en subredes propias, DNS interno, monitoreo y orquestación | Docker modela la app real multi-servicio, la escalada y el ciclo de vida automatizado |
| **Packet Tracer** ([PACKET-TRACER.md](PACKET-TRACER.md)) — **pista B, opcional** | El **perímetro visible**: router con ACL, bastión dual-homed con SSH, IPs fijas y tráfico paquete a paquete | Donde Docker abstrae, PT *muestra*. **No influye** en la pista A. |

> La pista B no es requisito de la pista A: se puede hacer por separado y no
> afecta la nota del laboratorio de Compose.

**La frase que debe quedarse con el estudiante:**

> En producción el bastión es un host o VM endurecido, **no un contenedor**.
> Tu bastión de verdad en este laboratorio (y en el Proyecto Semestral) es el
> **host**: la única entrada es SSH con llave, y las redes internas de Docker
> no son alcanzables desde fuera. Si alguien rompe el host, ya no hay red
> interna que proteger — por eso el acceso se endurece donde se ejecuta (el host).

## Arquitectura: dos pistas que no se cruzan

```
 PISTA A · DOCKER COMPOSE (obligatoria)          PISTA B · PACKET TRACER (opcional)
 ┌────────────────────────────────────────┐      ┌──────────────────────────────────┐
 │  HOST = bastión real (SSH por llave)   │      │  Internet ── R1 (router + ACL)   │
 │  red front 172.28.10.0/24 ── nginx     │      │      └─ SW ── srv-bastion        │
 │  red back  172.28.20.0/24 ── api ×2    │      │   (dual-homed) ── red interna    │
 │            └── db (NUNCA expuesta)     │      │                                  │
 │  DNS: web.local / api.local / db.local │      │  Se hace por separado; no        │
 │  Monitoreo: tcpdump + iftop + netdata  │      │  requiere Docker ni afecta la    │
 │  Secretos: db_pass                     │      │  pista A.  Ver PACKET-TRACER.md  │
 └────────────────────────────────────────┘      └──────────────────────────────────┘
```

> **Independencia:** ninguna pista necesita a la otra para completarse. La
> comparación PT↔Compose que aparece en algunos textos es **opcional** y solo
> sirve para *entender*, nunca para *aprobar*.

## Materiales

- **Docker Engine** con plugin `docker compose` (verificar: `docker compose version`).
  → **Todo lo que se necesita para la pista A (obligatoria).**
- Cliente SSH del host (`ssh`, `ssh-keygen`). En Windows: OpenSSH incluido o Git Bash.
- **Packet Tracer** (≥ 8.x) — **solo si** se quiere hacer la pista B (opcional).
  No es requisito para la pista A ni se usa en sus pasos.

## Qué se entrega por sesión

| Sesión | Entregable breve |
|--------|------------------|
| 1 | `docker-compose.yml` con `front`/`back` + pruebas de segmentación (`web↛db`, `api→db`) + `nslookup` de los 3 nombres |
| 2 | Capturas de `tcpdump`/`iftop`/netdata + demo de acceso SSH por llave y de rechazo de puertos |
| 3 | `docker-compose.yml` completo + captura de `--scale api=2` + evidencia del secreto en `/run/secrets` + prueba de `healthcheck` |
| 4 | Demo final del stack + dump de la DB + respaldo restaurado + `README.md` del repo del estudiante |

## Rúbrica global

100 puntos (25 por sesión).

| Sesión | Criterio | Puntos |
|--------|----------|--------|
| 1 | Primer stack con Compose (web/api/db) levantado con `up` | 8 |
| 1 | Segmentación demostrada (`web↛db`, `api→db`) + `internal: true` | 12 |
| 1 | DNS interno resuelve los 3 nombres | 3 |
| 1 | Preguntas 1-4 | 2 |
| 2 | Evidencia de monitoreo (`tcpdump` + netdata o iftop) | 12 |
| 2 | SSH por llave al host + rechazo de password (el host como bastión) | 9 |
| 2 | Preguntas 1-4 | 4 |
| 3 | `docker-compose.yml` con redes, healthchecks, secretos y escalado | 10 |
| 3 | `--scale api=2` + evidencia del secreto montado | 8 |
| 3 | Preguntas 1-4 | 7 |
| 4 | Stack completo levantado con `up --wait` sin intervención manual | 8 |
| 4 | Respaldo + restauración de la DB demostrados | 8 |
| 4 | Demo + preguntas 1-3 | 9 |
| | **Total** | **100** |

> **Pista B (opcional):** la evaluación de Packet Tracer es **independiente** y
> **no influye** en estos 100 puntos (ver [EVALUACION.md](EVALUACION.md) §"Pista B").

> **Puente con el Proyecto Semestral:** lo construido aquí es exactamente la
> columna vertebral del Avance N.º 2 (LAN + acceso + monitoreo) y base del
> Proyecto Final (orquestación). La Sesión 4 incluye un checklist explícito.

> **Regla del eje de orquestación:** el resultado que se califica es el **stack
> orquestado con Compose**. Si el equipo termina con `docker run` sueltos (sin
> un `docker-compose.yml` que reproduzca todo), la nota máxima del laboratorio
> es **50/100**, aunque las Sesiones 1-2 estén perfectas.

## Limpieza

```bash
cd Laboratorio-14-Red-Completa-Compose-PT/sesion-3
docker compose down -v --remove-orphans
rm -rf ~/lab14-ssh   # llaves del ejercicio
```
