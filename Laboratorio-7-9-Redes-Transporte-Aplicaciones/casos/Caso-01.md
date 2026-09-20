# CASO 01 — PagosYA: la fintech de pagos

Laboratorio N.º 7-9 · equipo de 4-6 · **presentas la siguiente clase**.

> Tu trabajo: la **red completa** que hace funcionar una app de pagos de 3 capas
> (portal → API → base de datos). El marco general está en
> [CASO.md](../CASO.md); aquí tienes **tus parámetros y tu giro**.

## Tu red (3 segmentos · VLSM sobre `192.168.88.0/24`)

| Segmento | Función | Hosts |
|----------|---------|-------|
| API de pagos | Backend que procesa transacciones | 30 |
| Portal web | Frontend que atiende al usuario | 8 |
| Base de datos | Almacena transacciones (sensible) | 10 |

## Giro de tu caso

- La **base de datos NO se expone** (ni al host ni a internet); confírmalo con
  `docker port`.
- El flujo de un pago debe quedar **funcional**: `POST /pagos` → 201 y al
  `GET /pagos` el pago aparece (persistido en la DB a través de la subred
  interna).

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