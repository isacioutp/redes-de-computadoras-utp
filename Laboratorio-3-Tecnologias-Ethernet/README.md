# Laboratorio N.° 3 — Tecnologías Ethernet: IEEE 802

Unidad I · Tema 1.3 · **Cisco Packet Tracer**

## Objetivo

Comprender la familia de estándares **IEEE 802** (Ethernet, Wi-Fi, Bluetooth,
WiMAX), diferenciar **Ethernet/Fast Ethernet/Gigabit** por velocidad, y
distinguir **dominio de colisión** (hub) frente a **dominio de broadcast**
(switch) observando el tráfico en Packet Tracer.

## Materiales

- Packet Tracer.
- Wireshark (opcional, para ver las tramas).

## Parte 1: La familia IEEE 802

Completa la tabla (usa internet si hace falta):

| Estándar | Nombre comercial | Velocidad | Uso |
|----------|------------------|-----------|-----|
| 802.3 | Ethernet (cable) | 10 Mbps → 400 Gbps | LAN cableada |
| 802.11 | Wi-Fi | 11–9.6 Mbps... | LAN inalámbrica |
| 802.15 | Bluetooth / WPAN | | PAN |
| 802.16 | WiMAX | | MAN |

**Pregunta 1**: ¿Cuál es la diferencia entre 802.3, 802.11 y 802.15 en cuanto
al medio de transmisión que cada uno utiliza?

## Parte 2: Ethernet, Fast Ethernet y Gigabit

### Paso 2.1: Velocidades de puertos del switch

1. Agrega un **Switch-2960** y 3 PCs.
2. En `CLI` del switch ejecuta:

```
en
conf t
interface FastEthernet0/1
speed 100
duplex full
interface GigabitEthernet0/1
speed 1000
```

*(Un 2960 tiene puertos Fast y Gigabit; observa la etiqueta de los puertos.)*

### Paso 2.2: Medir el "ancho de banda" en PT

En **modo Simulation**:

1. Filtra por `ICMP`.
2. PC1 hace `ping` a PC2.
3. Anota el tiempo que tarda el paquete con puerto Fast vs puerto Gigabit.

**Pregunta 2**: Un archivo de 500 MB se transfiere por:
- 10BASE-T (10 Mbps): ? segundos.
- 100BASE-TX (Fast Ethernet): ? segundos.
- 1000BASE-T (Gigabit): ? segundos.

Muestra tus cálculos.

### Paso 2.3: Full duplex vs half duplex

1. En el switch, pon la interfaz de PC1 en **half duplex** (`duplex half`).
2. Compara con PC2 en **full duplex**.

**Pregunta 3**: ¿Qué diferencia hay entre half y full duplex? ¿En qué medio
moderno ya no existen colisiones? Relaciónalo con el switch (full duplex =
una conversación en cada dirección a la vez).

## Parte 3: Colisiones vs broadcast — hub contra switch

### Paso 3.1: Escena con HUB

1. Monta **4 PCs → 1 Hub** (misma subred `192.168.1.0/24`).
2. En simulación, PC1 hace ping a PC4.
3. Observa en la **LAN del hub** quiénes reciben las tramas.

### Paso 3.2: Escena con SWITCH

1. Monta **4 PCs → 1 Switch** (misma subred).
2. Repite el ping PC1→PC4.
3. Observa en la captura de Simulation quién recibe la trama.

**Pregunta 4**: Rellena:

| | Hub | Switch |
|---|-----|--------|
| Recibe la trama PC1→PC4 | Todos los puertos | Solo el puerto destino (tras aprender) |
| Dominio de colisión | Uno solo (todas las PC) | Uno por puerto (full duplex) |
| Colisiones cuando 2 envián | Sí | No |
| Capa | 1 | 2 |

### Paso 3.3: Dominio de broadcast

Mete en la misma red del switch:
- PC1, PC2, PC3 (192.168.1.10/20/30) y un **Server DHCP** opcional.

**Pregunta 5**: Si un equipo hace una consulta DNS con destino `255.255.255.255`
(broadcast), ¿quién la recibe en el switch? ¿Y si estuvieran en dos redes
distintas con un router, qué pasaría con el broadcast?

## Parte 4: Ethernet en la vida real de un desarrollador

**Pregunta 6**: Cuando haces `docker run -p 8080:80`, ¿qué estándar Ethernet
está usando el host para llegar al switch de tu red? ¿Suficiente para tu
servidor web de producción (tráfico de usuarios)?

## Entregable

1. Captura de los puertos Fast/Gigabit del switch con su velocidad.
2. Captura de la escena Hub (broadcast hacia todos) y Switch (solo fue
   reenviado al destino correcto).
3. Cálculos de la Pregunta 2.
4. Respuestas a las 6 preguntas.

## Rúbrica (10 pts)

| Ítem | Pts |
|------|-----|
| Parte 1 (tabla 802) | 2 |
| Parte 2 (velocidades y duplex) | 3 |
| Parte 3 (hub vs switch) | 3 |
| Parte 4 + preguntas | 2 |