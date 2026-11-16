# TEORÍA — Repaso equilibrado de las capas (Labs 6-9)

> Lectura recomendada antes del **Caso 1**. Cada caso de este laboratorio apoya
> una parte de esta teoría en su red Docker. Presentación completa:
> `../Teoria/Teoria-Labs-6-9-Capas-Red.pptx`.

---

## 1. El modelo y el encadenamiento de capas

```
  Datos  →  Segmento/datagrama  →  Datagrama IP  →  Trama Ethernet  →  Bits
  (app)      (transporte 4)        (red 3)            (enlace 2)       (física 1)
```

Cada capa envuelve el dato con su cabecera (encapsulamiento); al recibir, cada
capa quita su cabecera (desencapsulamiento). Los **3 casos** recorren ese camino:
el navegador escribe un nombre (aplicación), se abre TCP (transporte), el
datagrama cruza subredes (red), viaja en una trama (enlace) y se serializa en
bits (física).

| Capa | Problema que resuelve | Protocolos / elementos clave |
|------|-----------------------|------------------------------|
| 1 · Física | ¿Cómo viaja el bit? | Medios, señales, latencia, CSMA/CD |
| 2 · Enlace | ¿A quién le paso la trama? | Ethernet, MAC, switch, ARP, FCS |
| 3 · Red | ¿Dónde está el destino? | IP, máscara, VLSM, ICMP, DHCP, router |
| 4 · Transporte | ¿Llega intacto y a qué app? | TCP (handshake), UDP, puertos |
| 7 · Aplicación | ¿Qué servicio es? | HTTP/HTTPS, DNS, SMTP, FTP, SNMP |

## 2. Capa física y enlace (Lab 6 — teoría, una clase)

- **Física**: los bits viajan como voltaje (cobre), luz (fibra) o radio
  (Wi-Fi). Define medio, conector, velocidad y **latencia** (el tiempo de viaje
  depende de la distancia, no del ancho de banda).
- **Trama Ethernet**: MAC destino (6) + MAC origen (6) + EtherType (2) + datos
  (46-1500) + FCS (4). `0x0800` = IPv4, `0x0806` = ARP.
- **MAC**: 48 bits en hexa; identifica físicamente la tarjeta. Prefijo = OUI del
  fabricante (`02:42:` de Docker). La MAC **cambia en cada salto**; la IP no.
- **Switch/bridge**: vive en capa 2, **aprende** MAC↔puerto y reenvía
  (no conoce destino → flooding). Cada red Docker es un dominio de broadcast.
- **ARP**: traduce IP → MAC en la misma red (broadcast + caché). Siempre precede
  a un ping.

## 3. Capa de red (Casos 1-3)

- **IPv4**: 32 bits, 4 octetos. Máscara separa red de host; `/24` =
  `255.255.255.0`.
- **Privadas RFC 1918**: `10/8`, `172.16/12`, `192.168/16` (solo LAN; NAT al salir).
- **Subneteo/VLSM**: partir la red en el tamaño justo; ordenar de mayor a menor;
  sin superposiciones. Para cada subred: **red**, **broadcast**, **gateway** y
  **hosts útiles = 2^(32-pref) − 2**.
- **ICMP**: diagnóstico de capa 3 — `ping` (echo), `traceroute` (salta con TTL),
  errores (*Destination Unreachable*).
- **DHCP**: UDP 67/68, mensajes DISCOVER → OFFER → REQUEST → ACK, entregas IP +
  máscara + gateway + DNS con lease.
- **Router** = dispositivo de capa 3 que une subredes con su **tabla de rutas**;
  requiere `ip_forward` y resuelve *default via <next hop>*.

## 4. Capa de transporte (Caso 2)

| Característica | TCP | UDP |
|----------------|-----|-----|
| Conexión | Orientado (handshake) | Sin conexión |
| Confiable | Sí (retransmite) | No (best-effort) |
| Orden | Garantiza | No garantiza |
| Latencia | Mayor (overhead) | Menor |
| Uso | HTTP, SSH, SMTP, DB | DNS, streaming, VoIP, juegos |

- **Handshake 3 vías**: SYN → SYN-ACK → ACK; cierre con FIN.
- **Puertos**: 0-1023 conocidos · 1024-49151 registrados · 49152-65535
  dinámicos. El par (IP, puerto) identifica la conversación.
- **Congestión/pérdida**: TCP reduce la ventana y retransmite; UDP pierde y no
  avisa. Se simula con `tc netem delay/loss`.

## 5. Capa de aplicación (Caso 1 y 3)

| Protocolo | Puerto | TCP/UDP | Función |
|-----------|--------|---------|---------|
| HTTP | 80 | TCP | Navegación web / APIs |
| HTTPS | 443 | TCP | Web cifrada (TLS) |
| DNS | 53 | UDP (y TCP) | Nombre → IP |
| SMTP | 25 / 465 / 587 | TCP | Enviar correo |
| POP3 / IMAP | 110 / 143 | TCP | Recibir correo |
| FTP | 20-21 | TCP | Transferencia de archivos |
| SNMP | 161 | UDP | Monitoreo (MIB/OID) |

- **HTTP**: métodos GET/POST/PUT/DELETE, encabezados, **códigos de estado**
  (200 OK, 301 redirect, 400/401/404, 500). Se consume con `curl -v`.
- **HTTPS**: HTTP dentro de **TLS** (certificados X.509); `curl -k` acepta
  autofirmados (solo desarrollo).
- **DNS**: jerarquía raíz→TLD→autoritativos; registros A/AAAA, CNAME, MX, TXT,
  NS; `dig` y `nslookup` para consultar.

## 6. Cuadro resumen "qué se ve en cada caso"

| Concepto | Caso 1 | Caso 2 | Caso 3 |
|----------|:------:|:------:|:------:|
| HTTP / HTTPS / DNS | ✅ | | ✅ |
| Teoría de trama/enlace (tcpdump -XX) | ✅ | | |
| IP / máscara / subred simple | ✅ | ✅ | ✅ |
| TCP handshake / puertos | ✅ | ✅ | ✅ |
| TCP vs UDP / netem | | ✅ | |
| 2 subredes + router + rutas | | ✅ | |
| VLSM completo / 3 subredes | | | ✅ |
| DB aislada + DNS interno + monitoreo | | | ✅ |
| Flujo completo tienda→API→datos | | | ✅ |

## 7. Preguntas de repaso

1. ¿Qué campos tiene la trama Ethernet y para qué sirve el EtherType?
2. ¿Qué cambia y qué no al cruzar un router: MAC, IP, TTL?
3. Para 30 hosts, ¿qué prefijo usás y qué tendrías que calcular (red,
   broadcast, gateway, hosts útiles)?
4. ¿Qué 3 paquetes establecen una conexión TCP?
5. ¿Qué código de estado responde una URL inexistente y qué puerto usa DNS?
6. ¿Por qué la base de datos no debe publicar puertos al host?