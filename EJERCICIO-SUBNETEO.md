# Ejercicio de subneteo (VLSM)

Una sola práctica, a **lápiz y sin calculadora**. Es la misma habilidad que
pide el Caso 3 (DatosYA), el Lab N.º 13 y el Avance N.º 1.

## Enunciado

Diseña el direccionamiento de una sede sobre `192.168.20.0/24` con estos
segmentos y arma la tabla: **subred, máscara, broadcast y rango utilizable**
de cada uno.

| Segmento | Hosts necesarios |
|----------|------------------|
| Ventas | 100 |
| Soporte | 50 |
| Servidores | 25 |
| Enlace WAN (router–router) | 2 |

> **Recordatorio:** ordena **del más grande al más pequeño**, asigna desde el
> inicio del bloque libre, y cada subred empieza en un **múltiplo de su
> bloque** (hosts útiles = 2^h − 2):
>
> `/25` = 128 · `/26` = 64 · `/27` = 32 · `/28` = 16 · `/30` = 4

<details><summary><b>Solución</b></summary>

| Segmento | Subred | Broadcast | Rango utilizable | Hosts útiles |
|----------|--------|-----------|------------------|--------------|
| Ventas (100) | `192.168.20.0/25` | `.127` | `.1` – `.126` | 126 |
| Soporte (50) | `192.168.20.128/26` | `.191` | `.129` – `.190` | 62 |
| Servidores (25) | `192.168.20.192/27` | `.223` | `.193` – `.222` | 30 |
| WAN (2) | `192.168.20.224/30` | `.227` | `.225` – `.226` | 2 |

**Cómo se llega:** 100 hosts → 2⁷−2 = 126 → `/25` desde `.0`. El siguiente
bloque libre es `.128`: 50 → 2⁶−2 = 62 → `/26`. Siguiente libre `.192`:
25 → 2⁵−2 = 30 → `/27`. Siguiente libre `.224`: 2 hosts → `/30` (`.224–.227`).
Queda libre `.228`–`.255` para crecimiento.

</details>
