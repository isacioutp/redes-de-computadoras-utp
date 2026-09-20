# CASO 04 — SuperRed: retail con puntos de venta (POS)

Laboratorio N.º 7-9 · equipo de 4-6 · **presentas la siguiente clase**.

> Tu trabajo: la **red completa** de una cadena de supermercados con sistema de
> facturación. Marco general en [CASO.md](../CASO.md); aquí van **tus parámetros
> y tu giro**.

## Tu red (3 segmentos · VLSM sobre `192.168.10.0/24`)

| Segmento | Función | Hosts |
|----------|---------|-------|
| API de facturación | Backend de ventas | 25 |
| Portal web | Tienda en línea | 8 |
| Base de datos | Inventario y ventas (sensible) | 12 |

## Giro de tu caso

- El tráfico **no debe ser "limpio" solo por defecto**: aplica **latencia
  artificial** (`tc netem`, ~100 ms) y compara `time curl` antes/después en la
  captura; explica qué pasaría con UDP (no confiable) en tu facturación.
- La **DB NO se expone** al host; `docker port` vacío.
- Tu `POST /pagos` equivale a **registrar una venta** (prueba 9).

## Entregables (igual para los 8 casos)

1. **Documento (40)** — sección 3 de `CASO.md`: diagrama, tabla VLSM, tabla
   puertos, capturas anotadas, 3 preguntas guía.
2. **Presentación / demo en vivo (30)** — ejecuta **en vivo, con Docker** las
   **9 pruebas** de `CASO.md` sección 4: **cada prueba demuestra un tópico**
   (tabla tópico→prueba), narrada capa por capa.
3. **Prueba funcional (30)** — checklist de `EVALUACION.md` sección 3, con la
   mini-app funcionando (prueba 9).

## Reglas

Ver `CASO.md` sección 5: equipos de 4-6, máx. 10 min, se presenta la siguiente
clase. Rúbrica en `EVALUACION.md`.