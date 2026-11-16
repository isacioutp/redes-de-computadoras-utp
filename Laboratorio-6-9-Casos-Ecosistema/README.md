# LABORATORIO N.º 6-9 — CASOS DE ESTUDIO "ECOSISTEMA"

**Red + Transporte + Aplicación + Teoría de capa física/enlace, en 3 casos
conectados entre sí.**

Semestres 2026-II · Semanas 6-8 · Unidad II · **32 estudiantes · 6-8 equipos de
4-6 · 3-4 clases**

> **Reemplaza a los antiguos Labs N.º 6 (práctico), 7, 8 y 9.** El Lab N.º 6
> queda **solo como teoría** (`Laboratorio-6-Capa-Fisica-Enlace/README.md` + el
> PPT `Teoria-Labs-6-9-Capas-Red.pptx`). En su lugar, **un solo laboratorio de
> casos de estudio**: cada caso cubre **varias capas a la vez sin saturarse**, y
> los tres se encadenan formando un ecosistema que **prueba lo que se vio de la
> Unidad 1 (capas 1-4)** en clase.

---

## 1. Qué es esto

Un laboratorio en **3 casos progresivos** por equipo. **Los 3 casos son iguales
para todos**; lo que cambia por equipo es su **escenario** (`Escenarios/`):
empresa, dominio y base IP. Cada equipo construye su ecosistema con Docker,
avanzando caso por caso:

```
            ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
            │  CASO 1         │      │  CASO 2         │      │  CASO 3         │
   usuario →│  el portal      │ ───► │  la API interna │ ───► │  la base de     │
 (navegador)│  HTTP/HTTPS/DNS │ http │  TCP/UDP,       │ SQL  │  datos aislada  │
            │  + trama (enl.) │      │  router, 2 subs │      │  + VLSM + DNS   │
            └─────────────────┘      └─────────────────┘      └─────────────────┘
               aplicar + enlace        transporte + red          red VLSM + datos
               (HTTP/HTTPS/DNS)        (TCP, puertos, router)    (VLSM, DB interna)
```

- **Caso 1 — el portal** que ve el usuario (capa 7: HTTP, HTTPS, DNS) apoyado en
  la teórica del Lab 6 (capa 2: se captura la trama Ethernet).
- **Caso 2 — la API** (capa 4: TCP/UDP, handshake, puertos, latencia) y la
  primera segmentación: 2 subredes + router con rutas.
- **Caso 3 — los datos** (capa 3 a fondo: **VLSM completo calculado por ellos**),
  base **aislada**, API doble casa, DNS interno y monitoreo. Cierra el flujo:
  **una transacción nace en el portal, cruza las subredes y persiste en la DB**.

> **Es un laboratorio guiado**: cada equipo recibe las guías paso a paso
> (`CASO-N.md`) y las ejecuta sobre **su escenario** (empresa, dominio, base IP).
> Se guía de a poco en clase y se **verifica qué aprendieron de la Unidad 1** con
> las evidencias, las respuestas y el diagrama. **No hay presentación ni demo
> formal.** La verificación del docente está en `DOCENTE/`.

## 2. Cómo se trabaja (3-4 clases guiadas)

| Clase | Actividad | Entregable |
|-------|-----------|------------|
| Clase 1 | Armado de equipos + asignación de **escenario** + guía del **Caso 1** | Documento del Caso 1 (resto de la semana + finde) |
| Clase 2 | Guía y soporte del **Caso 2** (aplica el portal) | Documento del Caso 2 |
| Clase 3 | Guía del **Caso 3** (VLSM, DB aislada, monitoreo) | Documento del Caso 3 |
| Clase 4 | **Revisión con el docente** (verificación de evidencias y respuestas por rol) | Ajustes y cierre de las entregas |

> Cada caso suma **100 puntos** (evidencias + respuestas + diagrama + rol
> individual). Detalle en `EVALUACION.md`.

## 3. Escenarios por equipo (solo cambia aquí)

| Grupo | Escenario | Base IP | Dominio |
|------:|-----------|---------|---------|
| 1 | FeriaYA · retail | `192.168.88.0/24` | `feria.local` |
| 2 | MediYA · salud | `192.168.89.0/24` | `medi.local` |
| 3 | RutaYA · logística | `192.168.90.0/24` | `ruta.local` |
| 4 | CineYA · entretenimiento | `192.168.91.0/24` | `cine.local` |
| 5 | AulaYA · educación | `192.168.92.0/24` | `aula.local` |
| 6 | GymYA · fitness | `192.168.93.0/24` | `gym.local` |
| 7 | HotelYA · hotelería | `192.168.94.0/24` | `hotel.local` |
| 8 | RefuYA · energía | `192.168.95.0/24` | `refu.local` |

Ver `Escenarios.md` y las hojas `Escenarios/Grupo-N-*.md`. Con 6 equipos se usan
los grupos 1-6; con 8, todos.

## 4. Esquema de red (idéntico en todos; cambia octeto y nombres)

| Caso | Subredes que se crean | Rol |
|------|-----------------------|-----|
| 1 | **1 subred** `portal` (`/26`, simple) | Portal público |
| 2 | + **`pagos` `/26`** contigua + router que une ambas | API interna comunicada |
| 3 | **VLSM completo**: `pagos /26` · `portal /28` · `datos /28` · `admin /29` (+ enlace `/30` en el diagrama) | 3 subredes + DB aislada |

> En el Caso 3 la base se **re-parte con VLSM** (de mayor a menor) † y se
> demuestra el aislamiento de la DB. La partición **la calcula cada equipo**:
> la guía no la da.

## 5. La plantilla (recurso compartido — la aplicación es el "termómetro")

```
Navegador → [portal nginx] → [API Flask :5000/:8088] → [Postgres aislado]
```

`plantilla/` (API Flask reutilizable + `init.sql` + portal HTML) se entrega para
que el trabajo sea la **red, los contenedores y las configuraciones**; la
aplicación solo demuestra que la red funciona (el POST→201→GET del Caso 3).

## 6. Archivos

| Ruta | Contenido |
|------|-----------|
| `CASO-1.md` | Guía paso a paso del Caso 1 (portal: HTTP/HTTPS/DNS + trama) |
| `CASO-2.md` | Guía paso a paso del Caso 2 (transporte + router entre 2 subredes) |
| `CASO-3.md` | Guía paso a paso del Caso 3 (VLSM calculado, DB aislada, monitoreo, integración) |
| `DIAGRAMAS.md` | Requisitos de los **diagramas** por caso + herramientas + plantilla |
| `EVALUACION.md` | Rúbrica (evidencias/respuestas/diagrama/rol) y reglas anti-copia |
| `Escenarios.md` | Asignación base IP + dominio por grupo |
| `Escenarios/Grupo-N-*.md` | Hoja de escenario de cada equipo (contexto + servicios + transacción) |
| `TEORIA.md` | Repaso equilibrado de las capas (capa física/enlace = Lab 6) |
| `plantilla/` | API Flask + `init.sql` + portal HTML reutilizables |
| `DOCENTE/` | **Guía de verificación del docente** (lo que deben lograr + errores típicos a chequear) |

## 7. Limpieza general

```bash
docker rm -f $(docker ps -aq --filter name=tienda-web) 2>/dev/null || true
docker rm -f $(docker ps -aq --filter name=pagosya) 2>/dev/null || true
docker rm -f $(docker ps -aq --filter name=datosya) 2>/dev/null || true
docker rm -f $(docker ps -aq --filter name=router-eco) 2>/dev/null || true
docker network rm $(docker network ls -q --filter name=portal) 2>/dev/null || true
docker network rm $(docker network ls -q --filter name=pagos) 2>/dev/null || true
docker network rm $(docker network ls -q --filter name=datos) 2>/dev/null || true
docker network rm $(docker network ls -q --filter name=admin) 2>/dev/null || true
```

## 8. Referencias

- Teoría completa (PPT): `Teoria-Labs-6-9-Capas-Red.pptx`
- Teoría Lab 6 (capa física y enlace): `Laboratorio-6-Capa-Fisica-Enlace/README.md`
- Guías prácticas históricas de los Labs 7-9: `_archivo-Laboratorios-antiguos/`