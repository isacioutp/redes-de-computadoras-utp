# Laboratorio N.° 2 — Medios de Transmisión, Topologías y Hardware de Red

Unidad I · Temas 1.2.2–1.2.7 · **Cisco Packet Tracer**

## Objetivo

Seleccionar el **medio de transmisión** correcto, comparar **topologías** y
verificar el comportamiento de **switch, router y punto de acceso**, midiendo
cómo se transmite un bit a través de distintos medios en Packet Tracer.

## Materiales

- Packet Tracer.
- Calculadora (para conversiones binarias de la Parte 3).

## Parte 1: Medios de transmisión

### Paso 1.1: Elegir el cable correcto

Packet Tracer ofrece tres tipos de cable físicos. Identifícalos:

| Cable en PT | Medio real | Velocidad típica | Cuándo se usa |
|-------------|------------|------------------|---------------|
| Copper Straight-Through | Par trenzado (Cat5e/6) | 100 Mbps–10 Gbps | PC ↔ Switch |
| Copper Cross-Over | Par trenzado cruzado | Ídem | PC ↔ PC directo |
| Fiber Optic | Fibra óptica | 1–400 Gbps | Switch ↔ Router / largas distancias |

**Paso práctico**: Conecta 2 PCs con **crossover** directamente (sin switch).
Asigna IPs `10.0.0.1` y `10.0.0.2` y haz `ping`.

**Pregunta 1**: ¿El cable usado es correcto? ¿Qué sucedería si usarás un cable
directo entre dos PCs (sin switch)?

### Paso 1.2: Fibra óptica vs cobre

- Monta: `Router` → **fibra** → `Switch` → **cobre** → `PC`.
- Configura IP en el PC.

**Pregunta 2**: ¿Dónde conviene usar fibra y dónde cobre? (alcance, inmune a
interferencias, costo)

### Paso 1.3: Inalámbrico (radio)

1. Agrega un `Access Point-PT` y un `Laptop` (con adaptador Wi-Fi).
2. Usa el cable **crossover** (o "Coaxial" en algunos PT) para conectar el AP
   al switch.
3. En la `Laptop`, `Wireless0` → SSID del AP, asigna IP misma subred.

**Pregunta 3**: ¿Qué estándar IEEE maneja la Wi-Fi en PT (802.11a/b/g/n/ac)?
¿Qué frecuencia y velocidad máxima?

## Parte 2: Construcción de una LAN completa (intranet)

Monta la siguiente red (es la base de todo el curso):

```
PC1 ─┐
PC2 ─┤
PC3 ─┴─ Switch ── Server
         │
      Router ── Internet (Cloud)
```

1. **Switch-2960** central. 3 PCs + 1 Server conectados en estrella.
2. **Router-2811/2911** conectado al switch y a un `Cloud` (internet).
3. Asigna IPs en **red privada** `192.168.1.0/24`:
   - Server: `192.168.1.100`
   - PCs: `192.168.1.10-30`

**Pregunta 4**: ¿Qué sucede si dos equipos usan la misma IP? Simúlalo: pon la
misma IP a PC1 y PC2 y haz ping a la IP duplicada. Qué observas (la tabla ARP
del switch / el conflicto).

### Paso 2.1: El rol del switch y del router con dirección MAC

1. Con `ping` funcionando, selecciona el switch y ve con **`MAC Address Table`**
   (mejor en modo Simulation).
2. Anota las **direcciones MAC** de PC1, PC2, PC3 y Server.

**Pregunta 5**: La tabla MAC del switch, ¿se llenó al ser encendido o tras el
primer tráfico? ¿Qué implica "aprender" para el switch?

### Paso 2.2: Intranet vs Internet

**Pregunta 6**: En la red montada, ¿qué dispositivo separa la "intranet" de la
"internet"? ¿Cómo llamarías a una red empresarial que se accede por VPN
(extranet)?

## Parte 3: Conversión de direcciones (repaso binario → decimal)

Para la Unidad II (direccionamiento IP) necesitarás convertir entre binario y
decimal. Resuelve:

1. `11000000 10101000 00000001 00011110` = ?
2. `192.168.10.150` → binario
3. `255.255.255.0` → binario (¿qué promedio tiene de 1s?)
4. ¿Cuántos bits tiene una dirección IP? ¿Cuántos valores distintos acepta
   cada octeto?

## Parte 4: Hardware — función de cada equipo

Usando la red de la Parte 2, responde:

| Equipo | Lo que hace en esta red | ¿Podría la red funcionar sin él? |
|--------|-------------------------|----------------------------------|
| Switch | Comunica PCs dentro de la misma red (capa 2) | No |
| Router | Conecta la LAN con internet (capa 3) | Sí, pero sin internet |
| Server | Provee servicios (capa 7) | Sí, PCs hablan entre sí |
| Access Point | Extiende la red a Wi-Fi | Sí |

**Pregunta 7**: Si quitamos el switch y conectamos PC1↔PC2 en crossover, ¿qué
tipo de "red" (topología) queda? ¿Y si agregamos un tercero sin hub?

**Pregunta 8**: ¿Por qué un Home Office típico usa un solo equipo que es
"router + switch + AP + firewall" integrados? ¿Qué capas cubre ese todo-en-uno?

## Entregable

1. Captura de la red LAN de la Parte 2 con las IPs visibles.
2. Captura de la tabla MAC del switch con las 4 MAC.
3. Conversiones de la Parte 3 anotadas.
4. Respuestas a las 8 preguntas.

## Rúbrica (10 pts)

| Ítem | Pts |
|------|-----|
| LAN montada y funcionando (ping) | 3 |
| Tabla MAC capturada | 2 |
| Conversiones | 2 |
| Preguntas | 3 |