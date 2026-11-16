# Proyecto Semestral — Redes de Computadoras (8410)

**Semestre:** II · **Carrera:** Desarrollo de Software
**Peso en el curso:** 35 % (Proyecto Semestral) + 10 % (Proyecto N.º 2 / Trabajo Grupal N.º 4)

## 1. Descripción general

Cada equipo de **4 a 6 estudiantes** desarrollará una **aplicación de software**
(de un banco de temas) y será responsable de **diseñar, implementar y orquestar
su propia infraestructura de red** usando las herramientas y conceptos vistos
en clase: direccionamiento IP, contenedores Docker, DNS interno, autenticación
SSH, servidores bastión, monitoreo y orquestación.

No se evalúa solo "que funcione": se evalúa **cómo se diseñó la red**, **cómo
se protegió el acceso** y **cómo se orquesta el despliegue**, igual que se
hace en una empresa de desarrollo real.

> El docente no entrega una solución tipo; el ejercicio es precisamente que
> cada equipo tome decisiones de arquitectura y las justifique.

## 2. Objetivos

1. Aplicar el **modelo OSI/TCP/IP** al diseño de la infraestructura de una
   aplicación real.
2. Diseñar un **esquema de direccionamiento** (subredes, VLSM, IP privadas).
3. Implementar una **LAN segmentada** con contenedores (frontend, backend,
   datos) con DNS interno propio.
4. Asegurar el acceso con **claves SSH** y un **servidor bastión**.
5. **Monitorear** el tráfico y el rendimiento de los servicios.
6. **Orquestar** el despliegue final (Docker Compose / Docker Swarm).

## 3. Restricciones y herramientas permitidas

| Aspecto | Herramienta obligatoria/sugerida |
|---------|-----------------------------------|
| App (web + API + DB) | Cualquier lenguaje: Python/Flask, Node/Express, PHP, Java… |
| Contenedores | Docker (`docker network`, `docker compose`) |
| Orquestación | Docker Compose y/o Docker Swarm (`docker stack`) |
| DNS interno | `dnsmasq` / inventario de Compose |
| Monitoreo | `tcpdump`, `iftop`, `iperf3`, `netdata` (mínimo 1) |
| Acceso seguro | `ssh-keygen` + `authorized_keys` + bastión |
| Diseño de red | Cisco Packet Tracer (Avance 1) y diagramas (draw.io/Mermaid) |
| Simulación final | Docker Engine (host) — no se requiere nube pagada |
| **No permitido** | Exponer la base de datos a internet; contraseñas en código; un solo contenedor "monolito" |

## 4. Banco de temas (elegir uno por equipo)

> 32 estudiantes · grupos de 4-6 → se forman **6-8 equipos**. Tres equipos como
> máximo pueden elegir el mismo tema; el docente asigna al inicio.

1. **PYME en línea** — tienda e-commerce con catálogo, carrito, pedidos e
   inventario (web + API + DB).
2. **Logística de almacén** — control de stock, entradas/salidas, reportes y
   alertas de stock mínimo.
3. **Biblioteca digital** — préstamos, catálogo, reservas y multas para una
   sede de la UTP.
4. **Agenda médica** — reserva de citas, historial de pacientes y recordatorios.
5. **Plataforma de cursos** — LMS con usuarios, cursos, matrículas y avances
   de nota.
6. **Restaurante en línea** — menús, pedidos, estado de cocina y entrega.
7. **Gestión inmobiliaria** — propiedades, inquilinos, contratos y pagos.
8. **Seguimiento de transporte** — rutas, unidades, estado de envíos y
   reporte en tiempo real (simulado).

**Requisito arquitectural común**: la app debe separarse en **al menos 3
servicios** (frontend web, API/backend, base de datos) y opcionalmente un
cuarto (cache, cola de mensajes, servidor de archivos). Esto permite que la
red real (subredes front/back/data) exista de verdad y no sea decorativa.

## 5. Entregables y cronograma

> **Nota sobre el calendario (ajuste):** para librar los feriados de noviembre
> (3, 4, 5, 10 y 28), los **laboratorios se comprimen y terminan en la semana 11**
> (última semana de octubre). Por eso el **Avance N.º 2 se adelanta a la
> semana 11** y el **Proyecto Final a la semana 13**; las semanas siguientes
> quedan como colchón de presentaciones/correcciones, sin trabajo nuevo
> obligatorio. Ver `../Administrativo/CRONOGRAMA.md`.

### A. Avance N.º 1 — Diseño de red (semana 10) — 10 % *(Proyecto N.º 2 / Trabajo Grupal N.º 4)*

Entregar:
1. **Diagrama de red** (Packet Tracer + imagen PNG del diagrama lógico) con
   los servicios propuestos y su ubicación en subredes.
2. **Esquema de direccionamiento** completo usando **VLSM** sobre una red base
   privada (RFC 1918) elegida por el equipo, con tabla de:
   subred → rango → broadcast → gateway → hosts necesarios.
3. Justificación breve (máx. 1 página) de las decisiones de segmentación.
4. Lista de los puertos que se expondrán públicamente y cuáles quedarán
   internos.

*Se apoya en el **Caso 3 del laboratorio de casos ECOSISTEMA** (tabla VLSM y diagrama de red completo, `Laboratorio-6-9-Casos-Ecosistema/`).*

### B. Avance N.º 2 — LAN, acceso seguro y monitoreo (semana 11) — 10 %

Entregar:
1. **Implementación en Docker** de la LAN diseñada en el Avance 1:
   contenedores en sus subredes (`docker network`), DNS interno funcionando.
2. **Claves SSH**: `ssh-keygen`, llave pública en servidores, acceso **sin
   contraseña** demostrado (captura).
3. **Servidor bastión**: mínimo *dual-homed* (o multi) protegiendo la red
   interna; la aplicación interna NO tiene exposición directa.
4. **Monitoreo** funcionando: evidencia de `tcpdump`, `iftop` o `netdata`
   capturando el tráfico de al menos un servicio.

*Se apoya en los **Labs N.º 10 y 11**.*

### C. Proyecto Final (semana 13) — 15 %

Entregar:
1. **Stack orquestado** completo: el frontend y el backend **escalados** (≥2
   réplicas) con balanceo, usando Docker Compose (y opcional Swarm) con
   secretos para credenciales.
2. **Manual de despliegue** (documento paso a paso: clonar repositorio,
   variables de entorno, `docker compose up`, cómo se conecta el bastión).
3. **Documentación técnica**:
   - Arquitectura (diagrama actualizado con redes, puertos, flujos).
   - Decisiones y justificación (segmentación, bastión, orquestación).
   - Presupuesto lógico de direcciones (resumen del Avance 1).
4. **Presentación oral** (10-12 min) + demo en vivo del stack.
5. **Anexo**: código fuente, `docker-compose.yml`, capturas de monitoreo.
6. **Repositorio** (GitHub/GitLab) con README y commit limpio.

*Se apoya en el **Lab N.º 12**.*

### Resumen de pesos

| Entregable | Semana | Peso |
|------------|--------|------|
| Avance N.º 1 — Diseño de red | 10 | 10 % |
| Avance N.º 2 — LAN + SSH/bastión + monitoreo | 11 | 10 % |
| Proyecto Final — orquestación + doc + demo | 13 | 15 % |
| **Total Proyecto Semestral** | | **35 %** |

## 6. Rúbrica de evaluación

### Avance N.º 1 (10 puntos)

| Criterio | Pts | Logrado (100 %) | Parcial | No (0) |
|----------|-----|-----------------|---------|--------|
| Diagrama Packet Tracer | 3 | Red dibujada y coherente con 3+ servicios | Diagrama incompleto | No hay |
| Esquema VLSM (tabla subred→rango→broadcast) | 5 | Correcto, sin superposición | Errores menores | Incorrecto |
| Justificación de segmentación + puertos | 2 | Clara y justificada | Superficial | No |

### Avance N.º 2 (10 puntos)

| Criterio | Pts | Logrado | Parcial | No |
|----------|-----|---------|---------|-----|
| LAN en Docker según Avance 1 | 4 | Subredes reales + DNS funcionando | Faltan piezas | No |
| SSH sin contraseña (captura) | 2 | Autenticación por llave probada | Solo password | No |
| Bastión (dual/multi-homed) | 2 | Aísla red interna de verdad | Solo single | No |
| Monitoreo (evidencia) | 2 | 1+ herramienta capturando tráfico | Evidencia débil | No |

### Proyecto Final (15 puntos)

| Criterio | Pts | Logrado | Parcial | No |
|----------|-----|---------|---------|-----|
| Stack orquestado con réplicas y balanceo | 4 | ≥2 réplicas front/back | Solo 1 réplica | No |
| Secretos configurados | 2 | No hay credenciales en código | Parcial | No |
| Manual de despliegue | 2 | Paso a paso reproducible | Incompleto | No |
| Documentación técnica (arquitectura + justificación) | 3 | Completa y coherente | Superficial | No |
| Presentación + demo en vivo | 2 | Funciona sin caos | Solo slides | No |
| Repositorio (GitHub) | 2 | README + commits claros | Básico | No |

## 7. Formato de entrega

- **Avance 1 y 2**: PDF (carpeta `Anexos/` con capturas) entregado en la
  plataforma del curso (Canvas/Moodle) + **enlace a rama/commit** del repo.
- **Proyecto final**: repositorio en línea + PDF + presentación (slides + demo).
- Documentos con carátula oficial de la UTP: universidad, Facultad, nombre del
  curso, integrantes, tema elegido.

## 8. Cronograma detallado (semanas)

> Ver la compresión de labs en `../Administrativo/CRONOGRAMA.md`: los laboratorios terminan en
> la **semana 11** (26-30 de octubre). Las semanas 12-13 resuelven el
> **Proyecto Final** y las semanas 14+ quedan como colchón de
> presentaciones/correcciones, NO para entregas nuevas.

| Semana | Actividad | Apoyo |
|--------|-----------|-------|
| 8 | Confirmar equipos + tema | Banco de temas |
| 9-10 | **Avance N.º 1**: diseño de red | Caso 3 del ECOSISTEMA (tabla VLSM y diagrama final) |
| 10-11 | Implementación LAN + SSH + bastión + monitoreo | Labs N.º 10-11 |
| 11 | **Avance N.º 2**: LAN + bastión + monitoreo (adelantado) | Labs N.º 10-11 |
| 11 | Orquestación del stack | Lab N.º 12 |
| 12 | Integración y ajustes del stack | Todo el curso |
| 13 | **Proyecto Final**: doc + presentación (adelantado) | Todo el curso |
| 14+ | Presentaciones del semestral + caso práctico · colchón de correcciones. Sin trabajo nuevo | — |

## 9. Lista de verificación final (antes de entregar)

- [ ] ¿La **base de datos** está en una red interna (no expuesta)?
- [ ] ¿El **SSH** por llave funciona **sin contraseña**?
- [ ] ¿Existe un **bastión** que protege el acceso?
- [ ] ¿Hay **DNS interno** resolviendo los nombres de los servicios?
- [ ] ¿La app está **escalada** (≥2 réplicas) y **balanceada**?
- [ ] ¿Hay **evidencia de monitoreo** (capturas, gráficas)?
- [ ] ¿No hay **credenciales** en el código?
- [ ] ¿El **README** explica cómo desplegar el proyecto?

## 10. Aviso académico

- La entrega es en equipo; el **portafolio estudiantil (5 %)** recoge la
  aportación individual de cada integrante (README personal, commits,
  reflexiones por lab).
- Se aplica el reglamento antiplagio de la UTP; todo repositorio debe ser
  público o con acceso del docente.
- El incumplimiento de una fecha entrega descuenta 2 puntos por cada día de
  atraso (sujeto al reglamento del curso).