# Laboratorio N.° 6 — Capa Física y Capa de Enlace de Datos · TEORÍA

Tema 2.5–2.6 · Semana 6 · Unidad II

> **Este laboratorio es SOLO teórico.** La práctica de capa física y enlace no
> se hace como laboratorio aparte: su aplicación práctica queda integrada en
> los **Casos N.º 1-3** (carpeta `Laboratorio-6-9-Casos-Ecosistema`), donde se
> capturan tramas y se observa el enlace dentro del flujo completo.
>
> Presentación con toda la teoría (Labs 6-9): `Teoria-Labs-6-9-Capas-Red.pptx`.

## Objetivo

Comprender cómo los datos se convierten en **señales físicas** (capa 1) y se
organizan en **tramas con direcciones MAC** (capa 2), para poder leer una trama
capturada con tcpdump y entender qué aísla un switch.

---

## 1. Capa Física (capa 1 del modelo OSI)

- Transmite **bits** como señales físicas: voltaje (cable), luz (fibra), ondas
  de radio (Wi-Fi).
- No entiende direcciones ni datos — solo transporta señal cruda.
- Define: tipo de medio y conector, voltaje, frecuencia, velocidad (bps) y
  modo dúplex (half/full).

| Medio | Velocidad típica | Latencia típica |
|-------|------------------|-----------------|
| Par trenzado (Cat6) | 1–10 Gbps | < 0.5 ms/salto |
| Fibra óptica | 10–400 Gbps | ~1 ms / 100 km |
| Wi-Fi 6 | 1–9 Gbps | 2–10 ms |
| Satélite | 25–100 Mbps | 250–600 ms |

- **Latencia (propagation delay)**: tiempo de viaje de la señal; depende de la
  distancia, no de la velocidad del enlace (un satélite siempre será ~0.5 s).
- **CSMA/CD** (Ethernet clásica): escuchar antes de transmitir y detectar
  colisiones. Los switches modernos son **full-duplex**: no hay colisiones.

## 2. Capa de Enlace de Datos (capa 2)

Organiza los bits en **tramas** y agrega **direcciones MAC**:

```
┌─────────────┬─────────────┬──────────┬──────────┬─────────┬──────────┐
│ MAC destino │ MAC origen  │ EtherType│ Datos    │ FCS/CRC │          │
│ 6 bytes     │ 6 bytes     │ 2 bytes  │ 46-1500  │ 4 bytes │          │
└─────────────┴─────────────┴──────────┴──────────┴─────────┴──────────┘
              ← Cabecera Ethernet (IEEE 802.3) →
```

- **MAC destino**: a quién llega (o `ff:ff:ff:ff:ff:ff` = broadcast).
- **MAC origen**: quién envía (única por NIC).
- **EtherType**: protocolo del payload — `0x0800`=IPv4, `0x0806`=ARP, `0x86DD`=IPv6.
- **FCS/CRC**: suma de comprobación; si falla, la trama se descarta.

### Dirección MAC (Media Access Control)

- Identificador **físico y único** del NIC; 12 dígitos hexadecimales (48 bits).
- Primeros 3 octetos = **OUI** del fabricante. Ej. `02:42:c0:a8:01:02` (el
  prefijo `02:42` lo asigna **Docker**).
- **MAC vs IP**: la MAC dice *quién es físicamente* (solo vale en la LAN, cambia
  en cada salto de enrutador); la IP dice *dónde está lógicamente* (vale de
  punta a punta).

### El Switch y su tabla MAC

- Vive en la **capa 2**: reenvía por MAC destino.
- **Aprende** MAC↔puerto observando el MAC origen.
- Conoce el destino → **filtra** (solo a ese puerto). No lo conoce → **flooding**
  (a todos). Broadcast → flooding siempre.
- Hub = un solo dominio de colisión (reenvía todo); switch = un dominio de
  colisión por puerto.
- El **bridge de Docker** (`br-xxx` = `docker network`) se comporta como un
  switch: cada red Docker es un **dominio de broadcast separado**.

### ARP — Address Resolution Protocol

- La capa 3 sabe la **IP** del destino, pero la capa 2 reenvía por **MAC**.
- ARP **traduce IP → MAC** dentro de la misma red: envía un broadcast
  `who-has 192.168.1.2?`, el dueño responde `is-at <MAC>`, y el par se guarda en
  la **caché ARP**.
- El primer ping siempre va precedido de ARP (evidencia en tcpdump).

## 3. Tabla-resumen Lab 6

| Concepto | Capa | Función |
|----------|------|---------|
| Medios (cobre/fibra/radio) | 1 | Transportar señal |
| Ethernet (IEEE 802.3) | 2 | Formato de tramas, acceso al medio |
| Dirección MAC | 2 | Identificar físicamente la tarjeta |
| Switch / bridge | 2 | Reenvío por MAC + aprendizaje |
| ARP | 2/3 | Traducir IP → MAC |

## 4. Para cerrar (preguntas de verificación)

1. ¿Qué campos tiene una trama Ethernet y para qué sirve el EtherType?
2. ¿Cómo aprende el switch su tabla MAC y qué hace si no conoce al destino?
3. ¿Qué traduce ARP, en qué capa vive y por qué se envía por broadcast?
4. ¿Qué diferencia hay entre una MAC y una IP? ¿Cuál cambia al cruzar un router?
5. ¿Qué separa una red Docker de otra y qué dispositivo se necesita para unirlas?

## Referencia

- Presentación completa (teoría Labs 6-9): `Teoria-Labs-6-9-Capas-Red.pptx`.
- Los Casos N.º 1-3 aplican esta teoría dentro del flujo portal→API→datos:
  `Laboratorio-6-9-Casos-Ecosistema/`.
- Guías prácticas históricas (material docente): `_archivo-Laboratorios-antiguos/`.