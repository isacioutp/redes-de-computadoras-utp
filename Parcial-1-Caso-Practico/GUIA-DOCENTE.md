# GUÍA DOCENTE — Parcial Único (Caso "RedTienda Panamá")

> ⚠️ **Solo para el docente. NO publicar.**
> Soluciones + pautas de corrección. Parcial orientado a futuros desarrolladores
> de software (misma teoría, contexto de deploy de apps), 100 pts.

## 1. Propósito

Único examen del curso, individual, práctico, asignado a mitad de la Unidad II
(tras el Lab N.º 7), entrega en 7 días. Cubre **Unidad I + Unidad II (hasta Lab
7)** con escenarios que un dev enfrenta (desplegar su app, redes de Docker).

## 2. Respuestas esperadas

### Sección A — Unidad I (20)

**A.1 (4)** Al subir código (git push) al servidor:
Fuente = tu PC/dev (genera los datos) · Transmisor = NIC del PC ·
Sistema de transmisión = cable/red · Receptor = NIC del servidor ·
Destino = repositorio/servidor (da servicio).

**A.2 (6)** PC→switch: **par trenzado** · servidores↔ISP 3 km: **fibra óptica**
· sede Isla Colón: **satélite**.

**A.3 (6)** Tipo de red: LAN = red de oficina (switches), WAN = internet/entre
sedes distantes, MAN = ciudad, PAN = Bluetooth de tu teclado/auriculares.
Topología actual: **estrella con hub**; recomendar **switch** (estrella
conmutada, full duplex, sin colisiones). (3+3)

**A.4 (4)** 5 MB → 40 Mb → **0.4 s** a 100 Mbps. Ethernet = **802.3**, Wi-Fi =
**802.11**.

### Sección B — Modelo OSI/TCP-IP (20)

**B.1 (10)** Ethernet=Enlace/Acceso-a-red(—) · IP=Red/Internet(—) ·
TCP=Transporte/Transporte(—) · UDP=Transporte/Transporte(—) · HTTP=Aplicación/
Aplicación(**80**) · DNS=Aplicación/Aplicación(**53**) · ICMP=Red/Internet(—,
sin transporte). (≈1.4/ítem)

**B.2 (10)** Frontend→API: **mensaje** (app) → **segmento** (TCP) →
**paquete** (IP) → **trama** (Ethernet). SDU de red = **segmento**; PDU de red
= **paquete**.

### Sección C — Análisis de trama (25)

**C.1 (15)**
| Bytes | Campo | Valor |
|-------|-------|-------|
| 0–5 | MAC dst | `02:42:c0:a8:01:0a` |
| 6–11 | MAC src | `02:42:c0:a8:01:14` |
| 12–13 | EtherType | `0x0800` = IPv4 |
| 14–15 | Versión 4 · IHL 5 | cabecera IP = **20 bytes** |
| 22 | TTL | `64` (`0x40`) |
| 23 | Protocolo | `1` = ICMP |
| 26–29 | IP src | `192.168.1.20` (frontend) |
| 30–33 | IP dst | `192.168.1.10` (api) |

ARP → `frontend` preguntó "¿quién tiene .10?" por broadcast (Lab 6). ICMP vive
en capa **3**, sin TCP/UDP. IHL=5 → **20 bytes**.
(10 tabla + 5 preguntas.)

**C.2 (10)** PDU: **trama** (Ethernet) → **paquete IP** → ICMP (sin segmento;
"datagrama ICMP"). Suma: **14 + 84 = 98**; el 84 = IP(20) + ICMP(8+56).
Coincide con Wireshark.

### Sección D — VLSM (20)

**D.1 (12)** — base 192.168.10.0/24:

| Servicio | Hosts | / | Subred | Rango | Broadcast |
|----------|-------|---|--------|-------|-----------|
| Frontend | 30 | /27 | 192.168.10.0/27 | .1–.30 | 192.168.10.31 |
| API | 14 | /28 | 192.168.10.32/28 | .33–.46 | 192.168.10.47 |
| Base de datos | 6 | /29 | 192.168.10.48/29 | .49–.54 | 192.168.10.55 |
| Enlace | 2 | /30 | 192.168.10.56/30 | .57–.58 | 192.168.10.59 |

**D.2 (8)** Máscara Frontend = **255.255.255.224** · Gateway = **.1** (primera
utilizable; la `.0` es dirección de red, no se usa) · Broadcast API =
**192.168.10.47** · RFC 1918: no se enruta en internet; para llegar a internet
el gateway hace **NAT** (y es por eso que unos contenedores "salen" y otros no).

### Sección E — Evidencia práctica (15 + 5)

**E.1 (5)** El contenedor recibe IP del rango de la red creada (auhorizamos
cualquiera de la clase C /24). La MAC **02:42** es asignada por Docker (OUI
local de bridges de contenedores). Respuesta esperada: IP como `172.x.0.x/24`
o la de la red creada y MAC `02:42:...`.

**E.2 (5)** TTL inicial: **64** (Linux) o **128** (Windows/macOS clase);
baja 1 por cada router ("Time exceeded" de ICMP en traceroute). `arp -a` único
por máquina → anti-copia.

**E.3 (bonus 5)** Recomendación coherente: usar **Docker networks** por
servicio (front/back/db como en Labs 7 y 12), **DHCP** (o asignación única)
para IPs, **switch** en lugar de hub, monitoreo. Premiar lógica, no exactitud.

## 3. Notas de aplicación

- Publicar tras el Lab N.º 7 (semana 9-10). Plazo 7 días.
- E surge de los Labs 5-7 (Docker): se siente como "continuar el lab", no como
  examen de teoría.
- Gente sin Docker puede responder E.1 describiendo el resultado que se vio en
  clase/lab y E.2 con ping/arp del propio SO.
- Peso sugerido: reemplaza los parciales del sílabo (30 %); usar 15 % y
  reasignar el resto a proyecto/labs según tu plan.

## 4. Errores comunes a vigilar

- ARP (IP→MAC, capa 2) vs DNS (nombre→IP, capa 7) — aquí DNS ahora está en la
  tabla B.1 a propósito.
- 5 MB → no olvidar ×8 a megabits.
- Hosts = 2^(32−n) − 2.
- IHL=5 → 20 bytes (no 5).
- ICMP no usa UDP/TCP.