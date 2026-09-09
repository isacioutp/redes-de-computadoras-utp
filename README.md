# Redes de Computadoras — Asignatura 8410

Plan, guías y materiales de laboratorio de la asignatura **Redes de
Computadoras** (UTP · Facultad de Ingeniería de Sistemas Computacionales).

## Estructura del repositorio

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
| `Laboratorio-6-Capa-Fisica-Enlace` | N.º 6 — Capa física y enlace (Semana 8) | **6A:** bits→trama Ethernet · **6B:** switch, aislamiento, internet | Docker | ✅ |
| `Laboratorio-7-Direccionamiento-Subredes` | N.º 7 — Direccionamiento y subredes (Semana 9) | **7A:** IP + VLSM · **7B:** ICMP, enrutamiento, DHCP | Docker | ✅ |
| `Laboratorio-8-Capa-Transporte-Docker` | N.º 8 — Capa de transporte (Semana 10) | **8A:** TCP vs UDP · **8B:** puertos, congestión, microservicios | Docker | ✅ |
| `Laboratorio-9-Capa-Aplicacion-Servicios` | N.º 9 — Servicios de aplicación (Semana 11) | **9A:** HTTP/HTTPS/DNS · **9B:** SMTP/FTP/SNMP | Docker | ✅ |

### Unidad III — Implementación de LAN y orquestación de aplicaciones

| Carpeta | Laboratorio | Contenido | Herramienta | Estado |
|---------|-------------|-----------|-------------|--------|
| `Laboratorio-10-LAN-Monitoreo-Docker` | N.º 10 — LAN y monitoreo (Semana 12) | **10A:** construir la LAN · **10B:** enrutamiento + monitoreo | Docker | ✅ |
| `Laboratorio-11-SSH-Servidores-Bastion` | N.º 11 — Claves SSH y servidores bastión (Semana 13) | **11A:** llaves + acceso · **11B:** bastión + producción | Docker | ✅ |
| `Laboratorio-12-Orquestacion-Docker-Swarm` | N.º 12 — Orquestación de servicios (Semana 14) | **12A:** Compose + Swarm · **12B:** secretos + stack | Docker Swarm | ✅ |

> **Modelo de trabajo (Labs 6-12):** cada lab está dividido en **dos sesiones**
> (`SESION-A.md` y `SESION-B.md` dentro de la carpeta), una por clase de la
> semana. Cada sesión tiene su objetivo, pasos, preguntas, entregable y rúbrica
> (50 + 50 = 100). Enfoque **aprender haciendo**: se construye, se observa, se
> mide y se documenta en cada clase.

## Proyecto Semestral

| Carpeta | Contenido |
|---------|-----------|
| `CRONOGRAMA.md` | **Calendario maestro del curso** (semana por semana + semanas sobrantes para presentaciones y caso con material adicional). Ver también README abajo. |
| `Proyecto-Semestral/ENUNCIADO.md` | Banco de temas, avances (10, 10 y 15 %), rúbricas y cronograma ajustado por los feriados de noviembre |

## Evaluación

| Carpeta | Contenido |
|---------|-----------|
| `Parcial-1-Caso-Practico/PARCIAL.md` | Parcial único: caso "RedTienda Panamá" (Unidad I + Unidad II hasta Lab 7; práctico, individual, 1 semana) |
| `Parcial-1-Caso-Practico/GUIA-DOCENTE.md` | Soluciones + pautas de corrección (no publicar) |

## Mapa de la asignatura (según sílabo 8410)

> ⚠️ La numeración por semana de este mapa **fue consolidada y adelantada** en
> `CRONOGRAMA.md` para librar los feriados de noviembre. Si hay diferencia, manda
> el `CRONOGRAMA.md`.

### Unidad I — Comunicación de datos y tecnologías Ethernet (10 h)

| Semana | Tema del sílabo | Laboratorio |
|--------|-----------------|-------------|
| 1 | 1.1 Componentes, bit/baudio, modos de transmisión | **Lab N.º 1** — introducción a la comunicación de datos |
| 2–3 | 1.2 Medios de transmisión, tipos de red, topologías, hardware, intranet/extranet | **Lab N.º 2** — medios, topologías y hardware |
| 4 | 1.3 Estándares IEEE 802.3/802.11/802.15/802.16, Fast/Gigabit | **Lab N.º 3** — tecnologías Ethernet |

### Unidad II — Modelos de comunicación y protocolos (40 h)

| Semana | Tema del sílabo | Laboratorio |
|--------|-----------------|-------------|
| 5–7 | 2.1–2.4: Arquitectura de protocolos, modelo OSI, TCP/IP | **Lab N.º 4** — análisis de trama · **Lab N.º 5** — modelo OSI y arquitectura de protocolos |
| 8 | 2.5–2.6: Capa física y enlace de datos | **Lab N.º 6** — Clase 1 (6A) · Clase 2 (6B) |
| 9 | 2.7: Capa de red — IP, máscaras, subredes, ARP, DHCP, ICMP | **Lab N.º 7** — Clase 1 (7A) · Clase 2 (7B) |
| 10 | Avance N.º 1 del Proyecto Semestral (diagrama + direccionamiento IP) | Se apoya en Lab N.º 7 (7B) |
| 10 | 2.8: Capa de transporte — TCP, UDP, puertos/sockets | **Lab N.º 8** — Clase 1 (8A) · Clase 2 (8B) |
| 11 | 2.9: Capa de aplicación — HTTP, FTP, SMTP, POP3/IMAP, DNS, SNMP | **Lab N.º 9** — Clase 1 (9A) · Clase 2 (9B) |

### Unidad III — Implementación de una LAN y orquestación de aplicaciones (25 h)

| Semana | Tema del sílabo | Laboratorio |
|--------|-----------------|-------------|
| 12 | 3.1–3.2: LAN + herramientas de monitoreo | **Lab N.º 10** — Clase 1 (10A) · Clase 2 (10B) |
| 13 | 3.3–3.4: Claves SSH + servidores bastión | **Lab N.º 11** — Clase 1 (11A) · Clase 2 (11B) |
| 14 | 3.5: Orquestación de servicios | **Lab N.º 12** — Clase 1 (12A) · Clase 2 (12B) |
| 15 | Cierre: integración + caso de estudio + portafolio | Aplicación de Labs 10–12 al proyecto semestral |

## Evaluación

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