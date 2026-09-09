# Laboratorio N.° 1 — Introducción a la Comunicación de Datos

Unidad I · Temas 1.1–1.2 · **Cisco Packet Tracer**

## Objetivo

Identificar los componentes de un sistema de comunicación de datos y montar la
primera red en Cisco Packet Tracer, reconociendo tipos de red, topologías y
hardware básico. Este laboratorio refresca los conceptos de la Unidad I antes
de entrar a las capas del modelo de comunicación.

## Materiales

- Cisco Packet Tracer instalado (cuenta de estudiante Cisco NetAcad).
- Este instructivo.

## Parte 1: Componentes de la comunicación de datos

El modelo genérico de comunicación es:

```
Fuente → Transmisor → Sistema de transmisión (medio) → Receptor → Destino
```

Completa la tabla con un ejemplo real de tu vida diaria:

| Componente | Descripción | Ejemplo: mensaje por WhatsApp |
|------------|-------------|------------------------------|
| Fuente | Genera los datos | ... |
| Transmisor | Convierte dato en señal | ... |
| Sistema de transmisión | El medio que transporta la señal | ... |
| Receptor | Convierte señal en dato | ... |
| Destino | Consume el dato | ... |

**Actividad**: En Packet Tracer, dibuja este modelo con un diagrama: usa un
`PC`, un `Router`, un `cloud` (nube) y otro `PC`.

**Pregunta 1**: ¿Qué dispositivo actúa como "transmisor" y cuál como "receptor"
en el envío de un mensaje de texto?

## Parte 2: Tipos de red y topologías

### Paso 2.1: Clasifica los tipos de red

Completa según el sílabo:

| Sigla | Nombre | Tamaño/alcance | Ejemplo real |
|-------|--------|----------------|--------------|
| PAN | Personal Area Network | ~10m | ... |
| LAN | Local Area Network | Un edificio/campus | ... |
| CAN | Campus | Campus universitario | ... |
| MAN | Metropolitan | Ciudad | ... |
| WAN | Wide | País/global | ... |

**Pregunta 2**: ¿En qué tipo de red está conectado tu celular a tu casa?
¿Y tu laptop de la universidad a los servidores de la UTP?

### Paso 2.2: Topologías en Packet Tracer

Construye las siguientes topologías (usa `PC`, `switch` y cableado recto):

1. **Estrella**: 4 PCs → 1 Switch.
2. **Bus**: 3 PCs conectados en línea (usa `Hub` para simular bus en PT).
3. **Anillo**: 3 PCs con tráfico circular (PT no tiene anillo real; usa un
   `Hub` con conexiones físicas en círculo).
4. **Malla**: 3 switches interconectados entre sí.

**Pregunta 3**: Rellena la tabla de topologías:

| Topología | Ventaja | Desventaja | ¿La uso actual ISPs? |
|-----------|---------|------------|----------------------|
| Estrella | ... | ... | Sí |
| Bus | ... | ... | No |
| Anillo | ... | ... | No |
| Malla | ... | ... | Routers de internet |

## Parte 3: Hardware de comunicación

### Paso 3.1: Reconoce los dispositivos

En Packet Tracer, agrega al área estos componentes y escribe su función:

| Dispositivo | Función | Capa OSI (si la recuerdas) |
|-------------|---------|----------------------------|
| PC / estación de trabajo | | |
| Server | | |
| Switch | | 2 |
| Hub | | 1 |
| Router | | 3 |
| Access Point (AP) | | 1/2 |
| Cable de cobre (directo) | | 1 |
| Cable de fibra | | 1 |

**Pregunta 4**: ¿Qué diferencia hay entre un `Hub` y un `Switch`? ¿Por qué los
`Hubs` ya no se usan en redes modernas?

### Paso 3.2: Intranet, extranet e internet

**Pregunta 5**: Clasifica cada acceso de texto:
- Red interna de la UTP a la que solo accede personal de la FISC.
- Red de la UTP a la que pueden acceder estudiantes con VPN.
- El sitio web público www.utp.edu.pa.

## Parte 4: Primera comunicación de extremo a extremo

### Paso 4.1: Construir la red

1. Arrastra **2 PCs** (`PC-PT`) y **1 Switch** (`Switch-2960`).
2. Conéctalos con cable **Copper Straight-Through**.
3. Asigna IPs (icono PC → `Config` → `FastEthernet0`):

```
PC1: IP 192.168.1.10   Mask 255.255.255.0
PC2: IP 192.168.1.20   Mask 255.255.255.0
```

### Paso 4.2: Verificar

```text
PC1 > ping 192.168.1.20
```

Cambia a **modo Simulation** y dispara el ping. Observa el sobre de datos
moverse por cada cable.

**Pregunta 6**: ¿El ping llega sin un router? ¿Por qué? ¿Qué capa del modelo
OSI necesitó únicamente?

### Paso 4.3: Fallos — detener la comunicación

```text
# Desconecta el cable de PC1
# En modo real:
PC1 > ping 192.168.1.20   → ¿qué pasa?
```

**Pregunta 7**: ¿Qué componente del modelo fuente→transmisor→medio→receptor
falló al desconectar el cable? ¿Cómo lo detectarías en la vida real?

## Parte 5: Bit y baudio

**Pregunta 8**: Calcula:
- Un archivo de 1 MB se transfiere a 1 Mbps. ¿Cuántos segundos tarda?
- ¿Qué significa que una línea sea de 9600 **baudios** si cada símbolo
  transporta 4 bits? (pista: baudios × bits/símbolo = bits/s)

## Entregable

1. Diagrama final de la Parte 4 (captura de pantalla del router+switch+PCs).
2. Tablas completadas en las Partes 1, 2 y 3.
3. Respuestas a las 8 preguntas.
4. Conclusión (3-5 líneas): para qué sirve conocer los componentes antes de
   estudiar protocolos.

## Rúbrica (10 pts)

| Ítem | Pts |
|------|-----|
| Diagrama y topologías | 3 |
| Tablas | 3 |
| Preguntas | 3 |
| Conclusión | 1 |