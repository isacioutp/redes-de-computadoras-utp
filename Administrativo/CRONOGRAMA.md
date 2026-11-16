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
2. Los **Labs 4+5** se **combinan** (una sesión por clase), el **Lab 6 pasa a
   ser solo teoría**, los **Labs 7+8+9 se reemplazan por 3 casos conectados
   entre sí** ("ECOSISTEMA": ① portal → ② API → ③ datos) sobre una mini-app
   funcional, y los **Labs 10-12 se fusionan en el Laboratorio N.º 14**
   ("red real → red virtual": PT + **Docker Compose**, sin Swarm).
3. La última entrega grande es el **Proyecto Final (semana 13)**.
4. Las **semanas 14 en adelante son sobrantes**: presentar el semestral,
   socializar el caso práctico, portafolio y reposición de clases perdidas.

## 2. Calendario maestro por semana

> **Modelo de trabajo (Labs 6-12):** el **Lab 6 es solo teoría** (capa física y
> enlace; presentación `Teoria-Labs-6-9-Capas-Red.pptx`). Los Labs 10-12 se
> **fusionan en el Laboratorio N.º 14** ("red real → red virtual"), un lab
> integrador de **4 sesiones** con **Docker Compose** (sin Swarm) y un **lab
> paralelo de Packet Tracer** que hace visible lo que Docker abstrae; ver
> `Laboratorio-14-Red-Completa-Compose-PT/`, con **archivos Docker por sesión**
> (`sesion-1/` … `sesion-4/`). Además, una **pista opcional de Packet Tracer**
> (autónoma, **sin efecto en la nota**) hace visible lo que Docker abstrae; ver
> `Laboratorio-14-Red-Completa-Compose-PT/PACKET-TRACER.md`. Excepción: los
> **Labs N.º 7-9** se
> reemplazan por **3 casos conectados entre sí** ("ECOSISTEMA" — TiendaYA →
> PagosYA → DatosYA) sobre una mini-app funcional; cada caso **reutiliza el
> anterior** y se evalúa en 3 partes: **documento + presentación/demo + prueba
> funcional** (`CASO-1/2/3.md` + `EVALUACION.md`).

| Semana | Fechas | Unidad | Laboratorio / Tema (2 clases/semana) | Proyecto Semestral | Evaluación / uso |
|--------|--------|--------|--------------------------------------|--------------------|------------------|
| 1 | Ago 17–21 | I | Lab N.º 1 — comunicación de datos | — | — |
| 2–3 | Ago 24–Sep 4 | I | Lab N.º 2 — medios, topologías y hardware | — | — |
| 4 | Sep 7–11 | I | Lab N.º 3 — tecnologías Ethernet (IEEE 802) · **se publica el Lab N.º 5** como tarea autónoma | — | — |
| 5 | Sep 14–18 | II | **Labs N.º 4-5 combinados** — análisis de trama · OSI/TCP-IP (Clase 1: Lab 4 · Clase 2: Lab 5) | — | — |
| 6 | Sep 21–25 | II | **Lab N.º 6 — solo teoría** (capa física/enlace) · Clase corta: **se publica el Caso 1 (ECOSISTEMA)** para el resto de la semana + fin de semana | — | — |
| 7 | Sep 28–Oct 2 | II | **ECOSISTEMA — Casos N.º 1-3** · **Clase 1:** teoría Lab 6-9 + arranque **Caso 2** (PagosYA) · **Clase 2:** presentación Caso 2 (documento + demo + prueba) | — | — |
| 8 | Oct 5–9 | II | **ECOSISTEMA** · **Clase 1:** **Caso 3** (DatosYA: VLSM + DB aislada + integración TiendaYA→PagosYA→DatosYA) · **Clase 2:** integración final + presentación Caso 3 | — | **Publicar Parcial 1** (caso "RedTienda", 7 días) |
| 9 | Oct 12–16 | II | **Integración/consultas** (post-casos) · se resuelven presentaciones pendientes si no alcanzó | — | Parcial 1: vence esta semana |
| 10 | Oct 19–23 | II-III | **Lab N.º 14** — red real → red virtual · **Clase 1:** Sesión 1 (primer Compose + segmentación/DNS) · **Clase 2:** Sesión 2 (monitoreo + acceso SSH) | Entrega **Avance N.º 1** (10 %, insumo: tabla VLSM del Caso 3) · **Se publica el Lab N.º 13 (VLSM/PT) como tarea autónoma** | — |
| 11 | Oct 26–30 | III | **Lab N.º 14** (continúa) · **Clase 1:** Sesión 3 (**orquestación con Compose**) · **Clase 2:** Sesión 4 (integración + respaldo + demo) | Entrega **Avance N.º 2** (10 %) | Devolver/socializar Parcial 1 |
| 12 | Nov 2–6 | III | Sin labs · integración (Labs 10-11 aplicados al semestral) | preparación Proyecto Final | — |
| 13 | Nov 9–13 | III | Sin labs · integración (Lab 12) | Entrega **Proyecto Final** (15 %) | Presentaciones del semestral |
| 14 | Nov 16–20 | — | Sin labs | — | Presentaciones del semestral · caso práctico |
| 15 | Nov 23–27 | — | Sin labs | — | Presentaciones restantes · portafolio · correcciones por atrasos |
| 16+ | Dic | — | **Semanas sobrantes** | — | Solo reposición de sesiones perdidas |

## 3. Cómo se combinan los laboratorios

Para cerrar en la semana 11, los Labs 10-12 se fusionan en el **Laboratorio
N.º 14** (4 sesiones, una por clase) y el par 4+5 se combina en la semana 5. Lo
que no alcanza en clase se resuelve como **trabajo autónomo** (los pasos ya están
guiados en cada `SESION-N.md`):

| Combinación | En clase | Trabajo autónomo |
|-------------|----------|------------------|
| **Labs 4 + 5** (semana 5) | Clase 1: Lab 4 (Wireshark) · Clase 2: Lab 5 (OSI) | Ambos labs se entregan completos el viernes de esa semana |
| **Labs 6-9 → ECOSISTEMA** (semanas 6-8) | Clase 6: teoría Lab 6 + Caso 1 (finde) · Clase 7: Caso 2 · Clase 8: Caso 3 | Cada caso se construye fuera de clase y se presenta en vivo (documento + demo + prueba funcional) |
| **Labs 10-12 → Lab N.º 14** (semanas 10-11) | Clase 10.1: Sesión 1 (primer Compose + segmentación/DNS) · Clase 10.2: Sesión 2 (monitoreo + acceso SSH) · Clase 11.1: Sesión 3 (Compose: réplicas/secretos) · Clase 11.2: Sesión 4 (integración) | Cada `SESION-N.md` trae su entregable y su carpeta con los archivos Docker (`sesion-1/` … `sesion-4/`); la **pista de Packet Tracer** (`PACKET-TRACER.md`) es **opcional y autónoma** (no influye en la nota). El **Lab N.º 13 (VLSM/DHCP en PT)** se publica como **tarea autónoma en la semana 10** para reforzar el direccionamiento del Avance N.º 1 |

Cada caso del ECOSISTEMA conserva su **100 puntos** (documento + demo + prueba
funcional, ver `Laboratorio-6-9-Casos-Ecosistema/EVALUACION.md`).

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