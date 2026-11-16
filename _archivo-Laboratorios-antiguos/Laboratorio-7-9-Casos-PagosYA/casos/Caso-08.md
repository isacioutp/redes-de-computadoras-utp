# CASO 08 — PlayZone: plataforma de gaming online

Laboratorio N.º 7-9 · equipo de 4-6 · **presentas la siguiente clase**.

> Tu trabajo: la **red completa** que conecta jugadores con servidores de
> partidas en tiempo real. Marco general en [CASO.md](../CASO.md); aquí van
> **tus parámetros y tu giro**.

## Tu red (3 segmentos · VLSM sobre `192.168.50.0/24`)

| Segmento | Función | Hosts |
|----------|---------|-------|
| API de partidas | Backend en tiempo real | 30 |
| Portal web | Tienda y lobby | 8 |
| Base de datos | Estadísticas de jugadores (sensible) | 10 |

## Giro de tu caso

- En gaming el **tiempo importa**: aplica **latencia artificial** (~50 ms) con
  `tc netem` a la interfaz del contenedor, compara `time curl` antes/después, y
  explica por qué **UDP** se usa en partes del juego (sin garantía) vs **TCP**
  para login y compras (con garantía).
- La **DB NO se expone** (estadísticas privadas de jugadores); `docker port`
  vacío.
- Tu `POST /pagos` equivale a **registrar una partida/partida terminada** (prueba
  9) y debe persistir a través de la subred interna.

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