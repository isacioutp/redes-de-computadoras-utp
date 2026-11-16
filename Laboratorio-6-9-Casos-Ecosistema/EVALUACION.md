# Evaluación del laboratorio de casos (guiado, por equipo)

**3 casos por equipo · equipos de 4-6 (32 estudiantes → 6-8 equipos) · 3-4 clases
de trabajo guiado**
· **Los casos 1-3 son iguales para todos**; lo que varía es el **escenario** de
cada equipo (`Escenarios/`) y el **diagrama** que acompaña el documento.

> Es un **laboratorio guiado**: la guía (`CASO-N.md`) se da paso a paso y cada
> equipo la ejecuta sobre **su escenario**. **No hay presentación ni demo**
> formal: lo que se evalúa es la **entrega (documento + evidencias + respuestas)**
> y que **cada integrante explique la evidencia que le tocó** al momento de
> revisarlo con el docente.

## 1. Nota por caso (100 puntos)

| Componente | Pts | Cómo se evalúa |
|-----------:|----:|----------------|
| **Evidencias pedidas por el caso** (capturas que coinciden con las IPs del escenario) | 50 | se cotejan con las listas de entregables de cada CASO-*.md |
| **Respuestas a las preguntas** del caso | 25 | coherencia de las preguntas 1-5 |
| **Diagrama** (según DIAGRAMAS.md) | 15 | coherencia con las evidencias, capas y flujo |
| **Rol individual** (trabajo en equipo) | 10 | cada integrante explica 1 evidencia suya en la revisión |

Revisión en clase guiada: el docente recorre contenedores/redes del equipo para
verificar que lo **entregado coincide con lo levantado** (las capturas no se
inventan). Nota final = promedio de los 3 casos.

## 2. Reparto de roles (para que los 4-6 trabajen)

Cada caso reparte el trabajo en roles (ver las tablas de cada `CASO-N.md`):
red, portal/TLS, DNS, transporte, DB/monitoreo, documentación/diagrama. En la
revisión, **cada miembro explica su evidencia** y responde una pregunta de su
rol. No se acepta que uno solo haga todo.

> Anti-copia: dos equipos con la **misma IP exacta** (mismo octeto), el mismo
> dominio o las mismas capturas → 0 en el caso.

## 3. Checklist por caso

- **Caso 1:** ☐ red `portal` /26 + gateway ☐ nginx 200 y 404 ☐ HTTPS falla sin `-k` / 200 con `-k` ☐ DNS del dominio desde un cliente ☐ trama `tcpdump -XX` etiquetada (MAC/EtherType/handshake) ☐ diagrama ☐ respuestas.
- **Caso 2:** ☐ subred `pagos` /26 sin solape ☐ API en 8088 (memoria) ☐ ping falla → rutas (ida+vuelta) → OK + `traceroute` ☐ handshake SYN/SYN-ACK/ACK ☐ `netstat` ☐ TCP vs UDP (`tc`) ☐ diagrama ☐ respuestas.
- **Caso 3:** ☐ VLSM completo calculado (tabla justificada + `ipcalc`) ☐ DB aislada (`docker port` vacío) ☐ API doble casa ☐ router + rutas ☐ DNS 3 nombres ☐ monitoreo `5432` ☐ prueba funcional POST→201→GET ☐ diagrama final ☐ respuestas.

## 4. Criterios de corte

- **Secuencia obligatoria**: el Caso 2 requiere el portal del Caso 1 y el Caso 3
  el esquema de los anteriores. Si no se puede montar el siguiente caso sobre lo
  entregado, se descuentan 15 pts en el flujo.
- Entregas idénticas entre equipos → 0 en el caso (ver anti-copia).

## 5. Escalas de la rúbrica

- **Logrado:** cumple el criterio y se demuestra con capturas.
- **Parcial:** cumple la mitad o evidencia débil.
- **No:** no cumple (0 en ese criterio).