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
| `Laboratorio-6-Capa-Fisica-Enlace` | N.º 6 — Capa física y enlace (Semana 6) | **6A:** bits→trama Ethernet · **6B:** switch, aislamiento, internet | Docker | ✅ |
| `Laboratorio-7-9-Redes-Transporte-Aplicaciones` | **Casos N.º 7-9 — "PagosYA" y 7 variantes (Semanas 7-9)** | 8 fichas de caso (red + transporte + aplicación) con una mini-app funcional: VLSM + router + ICMP, TCP/UDP + handshake, HTTP/HTTPS + DNS, DB aislada. Se presentan con demo funcional la siguiente clase. **Evaluación**: documento + demo + prueba funcional | Docker | ✅ |

### Unidad III — Implementación de LAN y orquestación de aplicaciones

| Carpeta | Laboratorio | Contenido | Herramienta | Estado |
|---------|-------------|-----------|-------------|--------|
| `Laboratorio-10-LAN-Monitoreo-Docker` | N.º 10 — LAN y monitoreo (Semana 10) | **10A:** construir la LAN · **10B:** enrutamiento + monitoreo | Docker | ✅ |
| `Laboratorio-11-SSH-Servidores-Bastion` | N.º 11 — Claves SSH y servidores bastión (Semana 11) | **11A:** llaves + acceso · **11B:** bastión + producción | Docker | ✅ |
| `Laboratorio-12-Orquestacion-Docker-Swarm` | N.º 12 — Orquestación de servicios (Semana 11) | **12A:** Compose + Swarm · **12B:** secretos + stack | Docker Swarm | ✅ |

> **Modelo de trabajo (Labs 6-12):** cada lab está dividido en **sesiones**
> (`SESION-X.md` dentro de la carpeta), una por clase de la semana. Cada sesión
> tiene su objetivo, pasos, preguntas, entregable y rúbrica (50 + 50 = 100).
> Nota: los Labs **7-9 se reemplazaron por 8 fichas de caso** ("PagosYA" y
> variantes, carpeta `Laboratorio-7-9-…`) que cubren red+transporte+aplicación
> con una mini-app funcional, y se **evalúan en 3 partes**: documento +
> presentación/demo + prueba funcional en vivo (`CASO.md` + `EVALUACION.md`). El
> docente introduce la clase con una **demo de 60 min** (`DEMO-DOCENTE.md` +
> stack `demo/`) y sortea las fichas (`casos/`); los equipos presentan la
> siguiente clase. Enfoque **aprender haciendo**: se construye, se observa, se
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

## Mapa de la asignatura

> El calendario semana por semana está consolidado en **`CRONOGRAMA.md`**
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