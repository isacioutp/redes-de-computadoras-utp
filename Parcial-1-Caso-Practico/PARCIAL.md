# PARCIAL ÚNICO — Redes de Computadoras (8410)

**Caso "RedTienda Panamá"** · **Individual** · **Entrega en 7 días**
Alcance: **Unidad I (1.1–1.3)** y **Unidad II hasta el Lab N.º 7**.
Enfoque: **futuros desarrolladores de software** — las preguntas se ven igual
que los Labs del curso (Docker/redes de tu app).
> No se resuelve en clase. Entrega en PDF: `Parcial1_Nombre_Apellido.pdf`.

| Nombre | |
|---|---|
| Grupo / Cédula | |
| Fecha | |

---

# El caso

Eres **desarrollador** en RedTienda Panamá. Tu equipo de 4 devs debe desplegar
una app web (frontend + API + base de datos) en los servidores de la empresa,
que hoy tiene:

1. **6 PCs en un hub** con `192.168.1.0/24` y la app queda **lenta** al subir
   fotos de productos al mediodía.
2. **Conflicto de IP**: dos PCs tienen `192.168.1.10` (se desconectan solos).
3. **Crecimiento**: deberás separar los servicios en *Frontend*, *API* y
   *Base de datos* y conectarlos a internet.

Como dev, no te toca instalar cableado: te toca **entender la red para que tu
app funcione bien y los clientes no se queden sin servicio**. Responde las 5
secciones (lo que ya viste en los Labs).

---

## Sección A — Comunicación de datos y Ethernet · Unidad I (20)

**A.1 (4)** Tu codebase vive en tu PC y el despliegue en un servidor de la
empresa. Al subir el código (git push), identifica los 5 componentes:
**Fuente / Transmisor / Sistema de transmisión / Receptor / Destino**.

**A.2 (6)** Elige el medio (par trenzado, fibra, Wi-Fi, satélite) para:
- tu PC → switch de la oficina
- servidores de RedTienda ↔ nube del ISP (3 km)
- respaldo de la sede en Isla Colón

**A.3 (6)**
- Da un ejemplo del día del desarrollador para LAN, WAN, MAN y PAN.
- El hub de la oficina: ¿qué **topología física** forma? ¿Hub o **switch**
  para la red nueva y por qué (lentitud/colisiones)?

**A.4 (4)**
- Un deploy sube un artefacto de **5 MB** por **Fast Ethernet (100 Mbps)**.
  ¿Cuántos segundos tarda?
- ¿Qué estándares **IEEE** son Ethernet por cable y Wi-Fi?

---

## Sección B — Modelo OSI / TCP-IP (20)

**B.1 (10)** Clasifica (capa OSI + capa TCP/IP + puerto si aplica):

| Protocolo | Capa OSI | Capa TCP/IP | Puerto |
|-----------|----------|-------------|--------|
| Ethernet | | | — |
| IP | | | — |
| TCP | | | — |
| UDP | | | — |
| HTTP | | | |
| DNS | | | |
| ICMP | | | — |

> Nota: en tus Labs usaste HTTP (navegar), TCP (Flask/Express), UDP y DNS
> (resolver `api-service` por nombre) — clasifícalos igual aquí.

**B.2 (10)** Cuando tu app (frontend, Flask) llama a tu API en el contenedor
`api`, un dato viaja por las capas. Nombra el **PDU** en cada una (mensaje,
segmento, paquete, trama) y responde: ¿cuál es el **SDU** y cuál el **PDU** de
la capa de red?

---

## Sección C — Análisis de trama (25)

Captura de `tcpdump` dentro de Docker cuando tu contenedor `frontend`
(`192.168.1.20`) hace `ping` al contenedor `api` (`192.168.1.10`):

```
02 42 c0 a8 01 0a | 02 42 c0 a8 01 14 | 08 00
45 00 00 54 | 12 34 00 00 | 40 01 5a 9b
c0 a8 01 14 | c0 a8 01 0a
(… datos ICMP …)
```

**C.1 (15)** Decodifica:

| Bytes | Campo | Valor |
|-------|-------|-------|
| 0–5 | MAC destino | |
| 6–11 | MAC origen | |
| 12–13 | EtherType | |
| 14–15 | Versión · IHL | |
| 22 | TTL | |
| 23 | Protocolo | |
| 26–29 | IP origen | |
| 30–33 | IP destino | |

Responde: ¿por qué `frontend` conoce la MAC de `api` (hint: **ARP**, como en el
Lab 6)? ¿En qué capa vive el protocolo `01` sin transporte? ¿Cuánto mide la
cabecera IP si IHL = 5?

**C.2 (10)**
- Nombra el PDU de los 3 bloques de la captura (trama/paquete/segmento).
- La trama mide **98 bytes** y el campo IP `Longitud total = 00 54` = 84.
  Explica la suma `14 (Ethernet) + 84 (IP)`. ¿Coincide con Wireshark?

---

## Sección D — Direccionamiento y subredes (20)

**D.1 (12)** Tu stack requiere 4 redes. Desde `192.168.10.0/24`, diseña VLSM
(de mayor a menor) — igual que hiciste en el Lab N.º 7:

| Servicio | Hosts | / | Subred | Rango útil | Broadcast |
|----------|-------|---|--------|-----------|-----------|
| Frontend (balanceado) | 30 | | | | |
| API | 14 | | | | |
| Base de datos | 6 | | | | |
| Enlace routers | 2 | | | | |

**D.2 (8)**
- Máscara decimal de la subred de Frontend.
- Gateway de Frontend (¿usa la `.0`? justifica).
- Broadcast de la subred de API.
- ¿Por qué RedTienda puede usar direcciones **privadas** RFC 1918 (y qué
  pasa cuando su app necesita llegar a internet)?

---

## Sección E — Evidencia práctica en TU equipo (15 + bonus 5)

Hazlo en tu máquina (Docker si lo tienes, si no con lo que tenías en los
Labs). Adjunta capturas:

**E.1 (5)** Levanta un contenedor y verifica su red (así lo hiciste en Labs
5-7):
```bash
docker network create parcial-red
docker run -d --name srv --network parcial-red alpine sleep 3600
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' srv
```
- ¿Qué IP te asignó Docker? ¿De qué `posible subred` viene (clase C? /24?)?
- ¿Qué MAC tiene el contenedor (pista: empieza con `02:42`)? ¿De dónde sale?

**E.2 (5)** Captura y explica **TTL** con `ping -c 4 8.8.8.8` (y si puedes,
`arp -a` de tu host). ¿TTL inicial (64/128)? ¿Por qué baja por salto?

**E.3 (bonus +5)** Una línea de **recomendación** para tu equipo de dev: cómo
organizar el despliegue con Docker (redes/subredes por servicio), evitar el
conflicto de IP y solucionar la lentitud del hub. *(Quien lo plantee bien ya
"resolvió el caso".)*

---

## Rúbrica

| Sección | Pts |
|---------|-----|
| A · Unidad I | 20 |
| B · Modelo OSI/TCP-IP | 20 |
| C · Análisis de trama | 25 |
| D · VLSM | 20 |
| E · Evidencia práctica | 15 (+5 bonus) |
| **Total** | **100** |

**Descuentos**: −2 pts/día de atraso · −10 pts si se detectan respuestas
idénticas entre estudiantes.

---

## Anexo — Portada

```
Universidad Tecnológica de Panamá
Redes de Computadoras (8410) — Parcial Único — Caso "RedTienda Panamá"
Nombre: __________  Grupo: ______  Fecha: ______
```