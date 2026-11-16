# Laboratorio N.° 4 — Análisis de una trama (encapsulamiento en Wireshark)

## Objetivo

Comprobar que la trama capturada por Wireshark es el **resultado del
encapsulamiento**: cada capa agrega su cabecera al dato de la capa superior,
produciendo un paquete final con todas las cabeceras anidadas.

## Materiales

- Computadora con Wireshark instalado.
- Conexión a internet (o archivo `.pcap` capturado previamente).

## Procedimiento

1. Abrir Wireshark e iniciar captura en la interfaz de red activa.
2. Generar tráfico (por ejemplo, `ping google.com` o navegar a un sitio web).
3. Detener la captura y seleccionar un paquete TCP u otro protocolo de interés.
4. En el panel de detalles, desplegar cada capa y anotar los campos.

## Análisis de la trama (encapsulamiento)

Una trama capturada se lee de afuera hacia adentro. Cada capa envuelve al dato
anterior agregando su cabecera:

```
┌────────────────────────────────────────────────────────────┐
│ Cabecera Ethernet (14 bytes)                  ← Capa de Enlace │
│   MAC destino | MAC origen | EtherType                     │
├────────────────────────────────────────────────────────────┤
│ Cabecera IP (20+ bytes)                       ← Capa de Red   │
│   Versión | TTL | IP origen | IP destino                   │
├────────────────────────────────────────────────────────────┤
│ Cabecera TCP (20+ bytes)                       ← Capa de Transporte│
│   Puerto origen | puerto destino | ACK/SEQ                  │
├────────────────────────────────────────────────────────────┤
│ Datos (payload)                              ← Capa de Aplicación │
└────────────────────────────────────────────────────────────┘
```

### Campos a identificar en Wireshark

| Capa | Cabecera en Wireshark | Campos clave |
|------|----------------------|--------------|
| Enlace | `Ethernet II` | Direcciones MAC origen/destino, EtherType (`0x0800` = IPv4) |
| Red | `Internet Protocol Version 4` | IP origen/destino, TTL, protocolo (`6` = TCP, `17` = UDP) |
| Transporte | `Transmission Control Protocol` o `UDP` | Puertos origen/destino, flags, números de secuencia |
| Aplicación | `Data` (bytes del payload) | Datos enviados por la aplicación |

### Terminología (PDU y SDU)

- **SDU** (Service Data Unit): los datos que una capa recibe de la superior.
- **PDU** (Protocol Data Unit): los datos + la cabecera que la capa agrega.
- El PDU de una capa es el SDU de la capa inferior.

| Capa | PDU |
|------|-----|
| Aplicación | Datos |
| Transporte | Segmento |
| Red | Paquete |
| Enlace | Trama (frame) |

## Verificación numérica del encapsulamiento

En la columna `Length` de Wireshark, cada trama muestra su **longitud total en
bytes**. Comprobar manualmente que esa cifra es la suma de cada capa:

```
Longitud total ≈ 14 (Ethernet) + IHL × 4 (IP) + Header Length (TCP) + payload
```

Para ello:

1. En la ventana `Ethernet II` anotar el campo **Frame Check Sequence / length**.
2. En `Internet Protocol Version 4` leer el campo **Header Length (IHL)** (por
   lo general `20 bytes` = 5 filas de 32 bits).
3. En `Transmission Control Protocol` leer **Header Length** (normalmente 20 bytes
   = 5 filas de 32 bits; aumenta si hay opciones TCP como timestamps).
4. Calcular el payload con la fórmula y compararlo con el campo que Wireshark
   muestra en `[TCP segment data]` o en `Data (…) bytes`.

El resultado debe coincidir. Si no coincide, revisar si la capa IP tiene
opciones (`IHL` mayor que 20) o si la trama tiene bytes de relleno y Preamble.

## Filtros de captura y de visualización

Repetir la captura usando filtros para seleccionar tráfico específico.

| Filtro | Tipo | Efecto |
|--------|------|--------|
| `icmp` | Visualización | Muestra solo paquetes de ping |
| `tcp.port == 443` | Visualización | Solo tráfico HTTPS |
| `udp` | Visualización | Solo tráfico UDP (ej. DNS) |
| `ip.addr == <tu-IP>` | Visualización | Solo tráfico de tu equipo |
| `port 53` | Captura | Guarda solo tráfico DNS desde el inicio |

1. Aplicar un filtro de visualización en la barra de Wireshark y verificar el
   color de la barra (verde = filtro válido).
2. Capturar un paquete **ICMP** (`ping`) y un paquete **DNS** (UDP). Comparar
   las cabeceras de ambos: ¿qué capas se repiten? ¿qué capa de transporte usa
   cada uno?

## Actividad complementaria

1. Buscar en la captura un paquete TCP **sin datos** (solo ACK o SYN).
   ¿Cuántas capas tiene? ¿La capa de aplicación existe en ese caso?
2. En el panel de bits de Wireshark (parte inferior), resaltar los primeros
   **14 bytes** de la trama: corresponden a la cabecera Ethernet. Confirmar
   visualmente cuántos bytes ocupan exactamente las direcciones MAC (6 + 6) y
   el EtherType (2).
3. Usar una captura HTTPS y contestar: ¿por qué la capa de aplicación aparece
   como `Encrypted Application Data` y no como texto legible?

## Preguntas de verificación

1. ¿Qué campo de la cabecera Ethernet indica qué protocolo llega después, TCP
   o UDP? *(Pista: un valor en la tabla de campos clave.)*
2. ¿Por qué la longitud del payload no aparece en la cabecera TCP pero sí se
   puede deducir de la longitud IP?
3. ¿Qué sucede con la trama si el `IHL` indica 24 bytes en vez de 20? ¿Qué
   datos extra contiene?
4. En el diagrama del encapsulamiento, ¿cuál es el SDU de la capa de red y
   cuál su PDU?

## Entregable

- Captura `.pcap`.
- Para un paquete: captura de pantalla desplegando las 4 capas.
- Tabla con los campos de cada capa del paquete elegido.
- La **verificación numérica** del punto anterior: cálculo a mano de la
  longitud total y comparación con el valor de Wireshark.
- Tabla comparativa de las cabeceras del paquete **ICMP** vs **DNS** (UDP) de
  la sección de filtros.
- Respuestas a las **preguntas de verificación**.
- Conclusión de 3-5 líneas explicando por qué la trama es el resultado del
  encapsulamiento.