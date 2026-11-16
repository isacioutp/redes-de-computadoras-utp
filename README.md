# Redes de Computadoras — Asignatura 8410

Plan, guías y materiales de laboratorio de la asignatura **Redes de
Computadoras** (UTP · Facultad de Ingeniería de Sistemas Computacionales).

## Estructura del repositorio

Los documentos están agrupados por tipo y los laboratorios quedan en la raíz:

| Carpeta | Contenido |
|---------|-----------|
| `Teoria/` | Presentaciones de las unidades y su volcado en texto |
| `Guias/` | Guiones docentes, guías de clase y de estudio, demo y ejercicio de subneteo |
| `Administrativo/` | Analítico, planificación oficial, cronograma y guía del Proyecto 1 |
| `DevOps/` | Sesión de cierre: teoría, volcado y laboratorio del caso |
| `Laboratorio-*` · `Proyecto-Semestral/` · `Parcial-1-Caso-Practico/` | Laboratorios, proyecto final y parcial |
| `tools/` | Scripts que generan las presentaciones y sus volcados |

### Unidad I — Comunicación de datos y tecnologías Ethernet

| Carpeta | Laboratorio | Contenido | Herramienta | Estado |
|---------|-------------|-----------|-------------|--------|
| `Laboratorio-1-Comunicacion-Datos-PacketTracer` | N.º 1 — Introducción a la comunicación de datos | Componentes, tipos de red, topologías, hardware, bit/baudio | Packet Tracer | ✅ |
| `Laboratorio-2-Medios-Topologias-Hardware` | N.º 2 — Medios, topologías y hardware | Medios de transmisión, LAN, MAC, binario→decimal | Packet Tracer | ✅ |
| `Laboratorio-3-Tecnologias-Ethernet` | N.º 3 — Tecnologías Ethernet (IEEE 802) | 802.3/802.11/802.15/802.16, Fast/Gigabit, hub vs switch | Packet Tracer | ✅ |

### Unidad II — Modelos de comunicación y protocolos

| Carpeta | Laboratorio | Contenido | Herramienta | Estado |
|---------|-------------|-----------|-------------|--------|
| `Laboratorio-4-Analisis-Trama-Wireshark` | N.º 4 — Análisis de una trama (encapsulamiento) | Lectura de tramas, encapsulamiento, PDU/SDU | Wireshark | ✅ |
| `Laboratorio-5-Modelo-OSI-Docker` | N.º 5 — Modelo OSI y arquitectura de protocolos | Capas OSI vs TCP/IP, recorrido de un mensaje por capas, fallas | Docker | ✅ |
| `Laboratorio-6-Capa-Fisica-Enlace` | N.º 6 — Capa física y enlace (Semana 6) | **Solo teoría**: señal, trama Ethernet, MAC, switch, ARP. La práctica se aplica dentro de los casos | Lectura + quiz | ✅ |
| `Laboratorio-6-9-Casos-Ecosistema` | **Casos N.º 1-3 — "ECOSISTEMA" (Semanas 6-8)** | Reemplaza los Labs 6 (práctico), 7, 8 y 9 por **3 casos conectados entre sí**: ① TiendaYA (portal: HTTP/HTTPS/DNS) → ② PagosYA (API: TCP/UDP, handshake, router) → ③ DatosYA (VLSM, DB aislada, monitoreo). Cada caso reutiliza el anterior y **se evalúa en vivo** (documento + demo + prueba funcional). El Lab 6 queda solo como teoría | Docker | ✅ |

### Unidad III — Implementación de LAN y orquestación de aplicaciones

| Carpeta | Laboratorio | Contenido | Herramienta | Estado |
|---------|-------------|-----------|-------------|--------|
| `Laboratorio-10-LAN-Monitoreo-Docker` | N.º 10 — LAN y monitoreo (Semana 10) | **10A:** construir la LAN · **10B:** enrutamiento + monitoreo | Docker | ✅ |
| `Laboratorio-11-SSH-Servidores-Bastion` | N.º 11 — Claves SSH y servidores bastión (Semana 11) | **11A:** llaves + acceso · **11B:** bastión + producción | Docker | ✅ |
| `Laboratorio-12-Orquestacion-Docker-Swarm` | N.º 12 — Orquestación de servicios (Semana 11) | **12A:** Compose + Swarm · **12B:** secretos + stack | Docker Swarm | ✅ |
| `Laboratorio-14-Red-Completa-Compose-PT` | **N.º 14 — Integrador U3: red real → red virtual (4 sesiones)** | Fusiona los Labs 10-12 en una sola narrativa **sin Swarm** (Swarm solo como "qué sigue"), **arrancando con Docker Compose** y con el **hilo siempre de redes** (subredes, segmentación, DNS, puertos/NAT, monitoreo, seguridad): ① primer stack con Compose + segmentación/DNS · ② monitoreo + **el host como bastión** (SSH por llave) · ③ **orquestación con Compose** (escalado, healthchecks, secretos) · ④ integración, respaldo y demo. Incluye **archivos Docker listos por sesión** (`sesion-1/`…`sesion-4/`) y una **pista opcional de Packet Tracer** (`PACKET-TRACER.md`), autónoma y **sin efecto en la nota** | Docker (Docker Compose) · *opcional:* Packet Tracer | ✅ |
| `laboratorio-enruntamiento-vlan` | N.º 13 — VLSM, DHCP y enrutamiento (**tarea autónoma, semana 10**) | **A:** topología 3 sedes + VLSM + DHCP + rutas estáticas · **B:** OSPF área 0 / RIPv2 + diagnóstico | Packet Tracer | ✅ |
| `DevOps/Laboratorio-15-DevOps-Despliegue` | **N.º 15 — Caso: el despliegue del viernes (práctica de cierre, semana 14+)** | El caso de PagosYA reproducido **con Docker local**: tag explícito, build/push al registry, smoke test, `.last-good` y **rollback en dos comandos**. La red es el tema: **NAT 8080→8000**, loopback, `docker port` vs `ss`, y el `502` explicado como upstream sin listener | Docker · registry `:2` · `curl` | ✅ |

> **Repaso de subneteo:** `Guias/EJERCICIO-SUBNETEO.md` — un solo ejercicio de VLSM
> (subred, broadcast y rango por segmento), a lápiz y con la solución plegable.

> **Modelo de trabajo (Labs 6-12):** el Lab 6 es **solo teoría** (capa física y
> enlace, ver `Teoria/Teoria-Labs-6-9-Capas-Red.pptx`). Los antiguos Labs 7-8-9 fueron
> reemplazados por el **laboratorio de 3 Casos conectados entre sí** — "ECOSISTEMA"
> (`Laboratorio-6-9-Casos-Ecosistema`): ① TiendaYA (portal, HTTP/HTTPS/DNS) →
> ② PagosYA (API, TCP/UDP, router entre 2 subredes) → ③ DatosYA (VLSM, DB
> aislada, monitoreo). Cada caso **reutiliza el anterior** y se evalúa **en
> vivo** (documento + demo + prueba funcional). Los **Labs 10-12 se fusionan en
> el Laboratorio N.º 14** (`Laboratorio-14-Red-Completa-Compose-PT`, 4 sesiones
> `SESION-1..4.md`): red real → red virtual con **Docker Compose** (sin Swarm),
> con **archivos Docker listos por sesión** (`sesion-1/` … `sesion-4/`) y una
> **pista opcional de Packet Tracer** (`PACKET-TRACER.md`, autónoma y **sin
> efecto en la nota**). Enfoque **aprender haciendo**: se construye, se observa,
> se mide y se documenta en cada clase.

### Unidad III — Presentaciones, guías y guiones

La teoría de la unidad son **3 presentaciones** (55 min cada una; 2 h 45 min en
total) con **notas del orador**, más la guía de clase y los guiones docentes, y
una **Parte 4 de extensión** (almacenamiento compartido y HA) y una **sesión de
cierre de DevOps sobre la red** para las semanas de integración y el Proyecto
Final.

| Recurso | Contenido |
|---------|-----------|
| `Teoria/Teoria-U3-Parte1-LAN-Monitoreo.pptx` · `Teoria/TEORIA-U3-Parte1-LAN-Monitoreo.md` | **3.1** LAN · **3.2** Monitoreo (18 diapositivas) |
| `Teoria/Teoria-U3-Parte2-SSH-Bastion.pptx` · `Teoria/TEORIA-U3-Parte2-SSH-Bastion.md` | **3.3** Claves SSH · **3.4** Bastión (13) |
| `Teoria/Teoria-U3-Parte3-Orquestacion.pptx` · `Teoria/TEORIA-U3-Parte3-Orquestacion.md` | **3.5** Orquestación Compose/Swarm (12) |
| `Teoria/Teoria-U3-Parte4-Almacenamiento-Compartido.pptx` · `Teoria/TEORIA-U3-Parte4-Almacenamiento-Compartido.md` | **Extensión 3.5** Almacenamiento compartido para HA: NAS/SAN, quórum, volúmenes NFS/CSI (15) |
| `Guias/DEMO-CEPH.md` | **Demo en vivo de la Parte 4** (guion docente, ~25 min): clúster **MicroCeph de 2 VM sobre Tailscale** — CephFS compartido entre nodos, caída de nodo y pérdida de quórum, tercer voto, y export **NFS** que convierte el volumen `pgdata` del Lab 14 en storage distribuido |
| `Guias/GUIA-CLASE-UNIDAD-III.md` | Reparto de las 3 partes y notas de uso (diapositivas, tiempos, recortes) |
| `Guias/CLASE-U3-LAN-Monitoreo.md` | **Guion docente** de 3.1/3.2 (minuto a minuto + Lab 10) |
| `Guias/CLASE-U3-Parte2-SSH-Bastion.md` | **Guion docente** de 3.3/3.4 (minuto a minuto + Lab 11) |
| `Guias/CLASE-U3-Parte3-Orquestacion.md` | **Guion docente** de 3.5 (minuto a minuto + Lab 12) |
| `Guias/GUIA-ESTUDIO-U3-LAN-Monitoreo.md` | **Guía del estudiante** de 3.1/3.2 (repaso + banco de preguntas con respuestas) |

### Sesión de cierre — DevOps (`DevOps/`)

Todo el material de la sesión vive en `DevOps/`:

| Recurso | Contenido |
|---------|-----------|
| `DevOps/Teoria-DevOps-Despliegue.pptx` · `DevOps/TEORIA-DEVOPS-DESPLIEGUE.md` | **Sesión de cierre (55 min de teoría)**: qué es DevOps, el caso del viernes, el laboratorio, el pipeline y su tráfico (NAT, loopback, DNS), rollback y DORA (17) |
| `DevOps/Laboratorio-15-DevOps-Despliegue/` | **Práctica del caso**: la API, el `Dockerfile`, el `compose.yml` y la guía paso a paso con los 10 comandos |

> Los archivos `Teoria/TEORIA-U3-*.md` son el **volcado textual** de cada presentación
> (contenido + notas del orador); se regeneran con
> `python3 tools/dump_ppt_md.py <archivo.pptx> "<título>"` (ver `tools/README.md`).

## Proyecto Semestral

| Carpeta | Contenido |
|---------|-----------|
| `Administrativo/CRONOGRAMA.md` | **Calendario maestro del curso** (semana por semana + semanas sobrantes para presentaciones y caso con material adicional). Ver también README abajo. |
| `Administrativo/PROYECTO #1 - GUÍA Y RÚBRICA DE EVALUACIÓN.md` | Guía y rúbrica del Proyecto 1 |
| `Proyecto-Semestral/ENUNCIADO.md` | Banco de temas, avances (10, 10 y 15 %), rúbricas y cronograma ajustado por los feriados de noviembre |

## Evaluación

| Carpeta | Contenido |
|---------|-----------|
| `Parcial-1-Caso-Practico/PARCIAL.md` | Parcial único: caso "RedTienda Panamá" (Unidad I + Unidad II hasta Lab 7; práctico, individual, 1 semana) |
| `Parcial-1-Caso-Practico/GUIA-DOCENTE.md` | Soluciones + pautas de corrección (no publicar) |

## Mapa de la asignatura

> El calendario semana por semana está consolidado en **`Administrativo/CRONOGRAMA.md`**
> (único archivo de referencia). Allí se documenta la compresión de los Labs
> para cerrar las clases formales la última semana de octubre y liberar
> noviembre de los feriados.

## Pesos de evaluación del curso

| Criterio | % |
|----------|---|
| Exámenes parciales (3) | 30 |
| Examen/proyecto semestral | 35 |
| Proyectos (2) | 10 |
| Laboratorios, investigaciones, foros | 20 |
| Portafolio estudiantil | 5 |

## Referencias

- Comer, D. (2018). *The Internet Book*. 1.ª ed. CRC Press.
- Forouzan, B. (2020). *Transmisión de datos y redes de comunicación*. 1.ª ed. McGraw-Hill.
- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach*. 7.ª ed. Pearson.
- Tanenbaum, A. (2012). *Redes de computadoras*. 5.ª ed. Pearson.