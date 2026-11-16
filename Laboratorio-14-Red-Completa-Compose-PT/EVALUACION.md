# Evaluación del Laboratorio N.º 14

**4 sesiones · trabajo individual o en parejas · 100 puntos (25 por sesión)**
· Se evalúa **en vivo** (el docente recorre los contenedores y coteja las
capturas) y con el **entregable de cada sesión**.

> El laboratorio es el **ensayo general del Proyecto Semestral**: lo que se
> aprueba aquí es exactamente la columna vertebral del Avance N.º 2 y del
> Proyecto Final.

## 0. Enfoque: red primero, Compose como medio

Es un laboratorio de **Redes**: se evalúan conceptos de red (segmentación,
subredes, DNS, puertos/NAT, monitoreo, acceso seguro). **Docker Compose es el
medio** para que esa red sea real y observable, y su orquestación es el eje de
ejecución. Por eso:

- Se evalúa como resultado final un **stack reproducible con un solo comando**
  (`docker compose up -d --wait`).
- El material [REFUERZO-ORQUESTACION.md](REFUERZO-ORQUESTACION.md) contiene los
  drills que se califican indirectamente en las Sesiones 3-4.
- **Regla de corte:** si el equipo termina con `docker run` sueltos (sin un
  `docker-compose.yml` que reproduzca todo), la nota máxima del laboratorio es
  **50/100**, aunque las Sesiones 1-2 estén perfectas.

## 1. Reparto por sesión

| Sesión | Tema | Entregable | Pts |
|--------|------|-----------|----:|
| **1** | Primer stack con Compose + segmentación/DNS | `docker-compose.yml` + pruebas `web↛db`/`api→db` + 3 `nslookup` | 25 |
| **2** | Monitoreo + acceso seguro | `tcpdump`/netdata + SSH por llave sin password | 25 |
| **3** | Orquestación con Compose | `docker-compose.yml` + `--scale api=2` + secreto + healthchecks | 25 |
| **4** | Integración y respaldo | Stack `up --wait` + dump/restore DB + self-healing + demo | 25 |

## 2. Rúbrica detallada

### Sesión 1 — Primer stack y segmentación (25)

| Criterio | Pts | Logrado | Parcial | No |
|----------|----:|---------|---------|----|
| Primer stack con Compose (`up` levanta web/api/db) | 8 | Un archivo = stack corriendo | Requiere `docker run` | No |
| Segmentación (`front`/`back` + `internal` + pruebas `web↛db`, `api→db`) | 12 | Ambas pruebas OK | Una sola o red plana | No |
| DNS interno resuelve `web.local`/`api.local`/`db.local` | 3 | Los 3 nombres | 1-2 nombres | No |
| Preguntas 1-4 | 2 | Correctas | Incompletas | No |

### Sesión 2 — Monitoreo y acceso (25)

| Criterio | Pts | Logrado | Parcial | No |
|----------|----:|---------|---------|----|
| Monitoreo (`tcpdump` + netdata o `iftop`) | 12 | Tráfico de un servicio capturado | Evidencia débil | No |
| SSH por llave al host + rechazo de password | 9 | Sin contraseña, password bloqueado | Solo funciona con password | No |
| Preguntas 1-4 | 4 | Correctas | Incompletas | No |

### Sesión 3 — Orquestación (25)

| Criterio | Pts | Logrado | Parcial | No |
|----------|----:|---------|---------|----|
| `docker-compose.yml` con redes, healthchecks, secretos y `depends_on` sano | 10 | Declarativo y reproducible | Faltan piezas | No |
| `--scale api=2` + balanceo por DNS demostrado | 8 | Evidencia clara | Solo escalado | No |
| Secreto fuera del YAML (`/run/secrets` + `grep` limpio) | 4 | No hay credenciales en código | Parcial | No |
| Preguntas 1-4 | 3 | Correctas | Incompletas | No |

### Sesión 4 — Integración (25)

| Criterio | Pts | Logrado | Parcial | No |
|----------|----:|---------|---------|----|
| Reproducción total (`down` + `up --wait`, todo `healthy`) | 8 | Sin pasos manuales | Requiere retoques | No |
| Respaldo y restauración de la DB | 8 | `count(*)` coincide | Solo dump | No |
| Self-healing demostrado | 5 | El servicio se recupera solo | No se recupera | No |
| Demo integrada (Docker, sin editar en vivo) | 4 | Coherente y en vivo | Solo slides | No |

## 3. Escalas de la rúbrica

- **Logrado (100 %):** cumple el criterio y se demuestra **en vivo** con capturas
  o comandos reproducibles.
- **Parcial (50 %):** cumple a medias o la evidencia es débil.
- **No (0):** no cumple.

### Pista B (opcional) — Packet Tracer, independiente

La **pista B** se evalúa **por separado** y **no influye** en los 100 puntos de
la pista A. Ver [PACKET-TRACER.md](PACKET-TRACER.md).

| Criterio | Pts | Logrado | Parcial | No |
|----------|----:|---------|---------|----|
| Topología completa (router, bastión dual-homed, red interna, host admin) | 3 | Completa y coherente | Incompleta | No |
| Direccionamiento (subredes + gateways) correcto | 3 | Sin solapes ni errores | Errores menores | No |
| ACL aplicada y paquete denegado en Simulation mode | 2 | Denegación visible | Solo configurada | No |
| Diagrama entregable + preguntas 1-5 | 2 | Completo | Superficial | No |
| **Total** | **10** | | | |

> Se puede aprobar la pista A sin hacer la pista B, y viceversa.

## 4. Política anti-copia

- Dos equipos con la **misma dirección IP exacta**, el **mismo nombre de dominio**
  o **capturas idénticas** → **0 en la sesión**.
- Las capturas deben corresponder a lo que está **levantado** en el equipo al
  revisar: si el contenedor no existe, la captura no vale.
- Se aplica el reglamento antiplagio de la UTP.

## 5. Revisión en clase (procedimiento del docente)

1. El equipo levanta su stack al inicio de la sesión (`docker compose ps`).
2. El docente ejecuta **una prueba funcional** aleatoria (p. ej. `curl` a la web,
   `nslookup` de un nombre, `pg_isready`).
3. Cada integrante **explica una evidencia suya** (rol asignado).
4. Se coteja la captura con lo levantado; si difieren, se descuenta.

## 6. Relación con el Proyecto Semestral

| Entregable del curso | Cubierto por |
|----------------------|--------------|
| Avance N.º 1 (10 %): diagrama + VLSM + segmentación + puertos | Sesión 1 (la **pista PT opcional** ayuda con el diagrama) |
| Avance N.º 2 (10 %): LAN Docker + SSH + bastión + monitoreo | Sesiones 1-2 |
| Proyecto Final (15 %): orquestación + secretos + manual + demo | Sesiones 3-4 |

## 7. Lista de verificación final (antes de la nota)

- [ ] La base de datos está en `back` (interna) y **no** publica puertos.
- [ ] El SSH por llave funciona **sin contraseña**.
- [ ] El acceso al host es la **única** entrada (password deshabilitado).
- [ ] Hay DNS interno resolviendo los nombres.
- [ ] La app está escalada (≥2 réplicas) y balanceada por DNS.
- [ ] Hay evidencia de monitoreo del stack.
- [ ] No hay credenciales en el YAML ni en el código.
- [ ] `docker compose up -d --wait` reproduce todo desde cero.
- [ ] El README del equipo explica cómo desplegar.
