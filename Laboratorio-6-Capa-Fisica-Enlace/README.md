# Laboratorio N.° 6 — Capa Física y Capa de Enlace de Datos

Tema 2.5–2.6 · Semana 8 · Unidad II · 2 clases

## Objetivo general

Comprender cómo los datos se convierten en **señales físicas** (capa 1) y se
organizan en **tramas con direcciones MAC** (capa 2), observando el trabajo del
switch y el protocolo ARP dentro de una red local, usando Docker como entorno
de laboratorio.

## Contexto teórico

### Capa Física (capa 1 del modelo OSI)

- Transmite **bits** como señales físicas: voltaje (cable), luz (fibra), ondas
  de radio (Wi-Fi).
- No entiende direcciones ni datos — solo transporta señal cruda.
- Define: voltaje, frecuencia, velocidad de transmisión, tipo de conector.

### Capa de Enlace de Datos (capa 2)

Organiza los bits en **tramas** y agrega **direcciones MAC**:

```
┌─────────────┬─────────────┬──────────┬──────────┬─────────┬──────────┐
│ MAC destino │ MAC origen  │ EtherType│ Datos    │ FCS / CRC │           │
│ 6 bytes     │ 6 bytes     │ 2 bytes  │ 46-1500  │ 4 bytes  │           │
└─────────────┴─────────────┴──────────┴──────────┴─────────┴──────────┘
                              ← Cabecera Ethernet →
```

### Dirección MAC (Media Access Control)

- Identificador **físico y único** del NIC (tarjeta de red).
- Formato: `AA:BB:CC:DD:EE:FF` → 12 dígitos hexadecimales (48 bits).
- Los primeros 3 octetos identifican al **fabricante** (OUI).
- Ejemplo: `02:42:c0:a8:01:02` (los `02:42` los asigna Docker).

### El Switch y la Tabla de Direcciones MAC

- El switch vive en la **capa 2**.
- Lee la MAC destino y decide a qué puerto enviar la trama.
- Mantiene una **tabla MAC↔puerto** (aprender = flooding inicial, luego filtrado).
- Difunde (flood) una trama a todos los puertos cuando no conoce al destino.

### ARP — Address Resolution Protocol

- Problema: la capa de red conoce la **IP** del destino, pero la capa 2 solo
  reenvía por **MAC**.
- ARP **traduce IP → MAC** dentro de la misma red.
- Envía un **broadcast** preguntando "¿quién tiene la IP X?" y guarda la
  respuesta en su caché ARP.

| Protocolo | Capa | Función |
|-----------|------|---------|
| Ethernet (IEEE 802.3) | Enlace | Formato de tramas, acceso al medio |
| ARP | Enlace/Red | Traduce IP → MAC |
| Switch | Enlace | Reenvío de tramas por MAC |

## Materiales y requisitos

- Computadora con Docker instalado.
- Conexión a internet (descargar imágenes).
- Cliente Wireshark (para el entregable opcional de la Sesión B).

```bash
docker --version
docker ps
```

## Cómo se trabaja esta semana

Dos clases en la misma semana. La **Sesión A** construye la infraestructura
(red y contenedores `c1`, `c2`, `c3`) que la **Sesión B** reutiliza para
probar aislamiento y salida a internet.

| Sesión | Contenido | Entregable breve | Guía |
|--------|-----------|------------------|------|
| Sesión A — De los bits a la trama Ethernet | Parte 1 (MAC en contenedores), Parte 2 (Tramas Ethernet con tcpdump y `-XX`) y Parte 4 (Capa física: latencia y CSMA/CD). | Capturas de MAC y de tramas ARP/ICMP, análisis `-XX`, respuestas 1–8. | [Sesión A](SESION-A.md) |
| Sesión B — El switch, el aislamiento y la salida a internet | Parte 3 (aislamiento y dominios), Parte 5 (host Docker como router/internet), refuerzo Wireshark y verificación. | Capturas de aislamiento e internet, análisis Wireshark, respuestas 1–7. | [Sesión B](SESION-B.md) |

## Rúbrica global

Cada sesión suma **50 puntos**; ambas juntas conforman la calificación total de
la semana (**100 puntos**).

| Criterio | Puntos |
|----------|--------|
| Sesión A — De los bits a la trama Ethernet | 50 |
| Sesión B — El switch, el aislamiento y la salida a internet | 50 |
| **Total** | **100** |

## Limpieza

```bash
docker rm -f c1 c2 c3 c4 test-phys
docker network rm lab6-red lab6-red2
```