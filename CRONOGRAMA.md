# CRONOGRAMA MAESTRO — Redes de Computadoras (8410) · Semestre 2026-II

> **Único archivo de referencia del calendario.** Reemplaza los números de
> semana sueltos de otros archivos (README, ENUNCIADO y carpetas de
> laboratorio), que ya están alineados con este documento.
>
> Semestre iniciado el **lunes 17 de agosto de 2026** · **2 clases por semana**
> · los laboratorios se comprimen para cerrar la **última semana de octubre**.

## 1. Regla general (compresión por noviembre)

Noviembre concentra varios **días libres** (3, 4, 5, 10 y 28), así que para no
arriesgar entregas:

1. **Todos los laboratorios terminan la semana 11 (26–30 de octubre)**, dejando
   noviembre libre para el Parcial 1, el Proyecto Final y las presentaciones.
2. Los **Labs 4+5** y **11+12** se **combinan** (una sesión por clase; el
   detalle está en la sección 3), y los **Labs 7+8+9 se reemplazan por 8
   fichas de caso** (red + transporte + aplicación en una mini-app funcional).
3. La última entrega grande es el **Proyecto Final (semana 13)**.
4. Las **semanas 14 en adelante son sobrantes**: presentar el semestral,
   socializar el caso práctico, portafolio y reposición de clases perdidas.

## 2. Calendario maestro por semana

> **Modelo de trabajo (Labs 6-12):** cada laboratorio se divide en **sesiones**
> (`SESION-X.md`), una por clase. Con **2 clases por semana**, cada clase
> resuelve una sesión: entregable y rúbrica por sesión. Excepción: los **Labs
> N.º 7-9** se reemplazan por **8 fichas de caso** ("PagosYA" y variantes) que
> cubren red, transporte y aplicación con una mini-app funcional; se evalúan en
> 3 partes: **documento + presentación/demo + prueba funcional**
> (`CASO.md` + `EVALUACION.md`).

| Semana | Fechas | Unidad | Laboratorio / Tema (2 clases/semana) | Proyecto Semestral | Evaluación / uso |
|--------|--------|--------|--------------------------------------|--------------------|------------------|
| 1 | Ago 17–21 | I | Lab N.º 1 — comunicación de datos | — | — |
| 2–3 | Ago 24–Sep 4 | I | Lab N.º 2 — medios, topologías y hardware | — | — |
| 4 | Sep 7–11 | I | Lab N.º 3 — tecnologías Ethernet (IEEE 802) · **se publica el Lab N.º 5** como tarea autónoma | — | — |
| 5 | Sep 14–18 | II | **Labs N.º 4-5 combinados** — análisis de trama · OSI/TCP-IP (Clase 1: Lab 4 · Clase 2: Lab 5) | — | — |
| 6 | Sep 21–25 | II | Lab N.º 6 — **Clase 1:** 6A (bits→trama) · **Clase 2:** 6B (switch, internet) | — | — |
| 7 | Sep 28–Oct 2 | II | **Casos N.º 7-9** — **Clase 1:** **DEMO intro (60 min)** y **sorteo de las 8 fichas** de caso · **Clase 2:** implementación con acompañamiento/consultas | — | — |
| 8 | Oct 5–9 | II | **Casos N.º 7-9** — **Clase 1:** presentaciones (equipos 1-4) · **Clase 2:** presentaciones (equipos 5-8): documento + demo en vivo + prueba funcional | — | **Publicar Parcial 1** (caso "RedTienda", 7 días) |
| 9 | Oct 12–16 | II | **Integración/consultas** (post-casos) · se resuelven presentaciones pendientes si no alcanzó | — | Parcial 1: vence esta semana |
| 10 | Oct 19–23 | II-III | Lab N.º 10 — **Clase 1:** 10A (LAN) · **Clase 2:** 10B (monitoreo) | Entrega **Avance N.º 1** (10 %, insumo: tabla VLSM del Lab 7-9) | — |
| 11 | Oct 26–30 | III | **Labs N.º 11-12 combinados** — **Clase 1:** 11A (llaves) + 11B (bastión, tarea) · **Clase 2:** 12A (Swarm) + 12B (secretos, tarea) | Entrega **Avance N.º 2** (10 %) | Devolver/socializar Parcial 1 |
| 12 | Nov 2–6 | III | Sin labs · integración (Labs 10-11 aplicados al semestral) | preparación Proyecto Final | — |
| 13 | Nov 9–13 | III | Sin labs · integración (Lab 12) | Entrega **Proyecto Final** (15 %) | Presentaciones del semestral |
| 14 | Nov 16–20 | — | Sin labs | — | Presentaciones del semestral · caso práctico |
| 15 | Nov 23–27 | — | Sin labs | — | Presentaciones restantes · portafolio · correcciones por atrasos |
| 16+ | Dic | — | **Semanas sobrantes** | — | Solo reposición de sesiones perdidas |

## 3. Cómo se combinan los laboratorios

Para cerrar en la semana 11 se fusionan dos pares de labs. La sesión que no se
ve en clase se resuelve como **trabajo autónomo** (los pasos ya están guiados
en cada `SESION-B.md`):

| Combinación | En clase | Trabajo autónomo |
|-------------|----------|------------------|
| **Labs 4 + 5** (semana 5) | Clase 1: Lab 4 (Wireshark) · Clase 2: Lab 5 (OSI) | Ambos labs se entregan completos el viernes de esa semana |
| **Labs 7 + 8 + 9** (semanas 7-8) | Clase 1: DEMO intro + sorteo de las 8 fichas · Clase 2: implementación/consultas | Los **8 casos** (documento + mini-app funcional + demo) se presentan en las clases 2 de la semana 8 (equipos 1-4 y 5-8) |
| **Labs 11 + 12** (semana 11) | Clase 1: 11A (llaves SSH) · Clase 2: 12A (Compose/Swarm) | 11B (bastión) y 12B (secretos/stack) se resuelven con los pasos de cada `SESION-B.md` |

Ambas combinaciones conservan sus **100 puntos** (entregable + rúbrica por
sesión); se empaquetan como **una sola entrega por semana**.

## 4. Feriados que ya quedan fuera de las clases formales

| Fecha (noviembre) | Día conmemorativo | Cae en |
|-------------------|-------------------|--------|
| 3, 4, 5 | Separación de Panamá de Colombia · Día de la Bandera · Consolidación | Semana 12 (sin labs) |
| 10 | Primer Grito de Independencia (Villa de Los Santos) | Semana 13 (presentaciones) |
| 28 | Independencia de España | Sábado, fuera del calendario lectivo |

> Los días libres están sujetos a lo que disponga el Ejecutivo (posibles
> puentes adicionales). Al no haber laboratorios en noviembre, no afectan las
> entregas; solo pueden pausar presentaciones.

## 5. Reglas operativas

1. Todos los laboratorios se dictan y entregan **hasta la semana 11**.
2. La última entrega grande es el **Proyecto Final, en la semana 13**; después
   de esa semana no se programan entregas nuevas.
3. Las semanas 12 en adelante se dedican al **Proyecto Final**, a las
   **presentaciones** (semestral y caso) y al **cierre** (portafolio,
   correcciones por atrasos: −2 pts/día); nunca a contenido nuevo obligatorio.
4. Si un equipo no alcanza a presentar en una sesión sobrante, pasa a la
   siguiente; el orden de presentación se sortea al terminar la semana 13.
5. Los avances/final se entregan como indica `Proyecto-Semestral/ENUNCIADO.md`.