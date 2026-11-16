# CASO 03 — UniTEC: campus universitario

Laboratorio N.º 7-9 · equipo de 4-6 · **presentas la siguiente clase**.

> Tu trabajo: la **red completa** de un campus con subredes para estudiantes,
> staff, sistemas y monitoreo. Marco general en [CASO.md](../CASO.md); aquí van
> **tus parámetros y tu giro**.

## Tu red (3 segmentos · VLSM sobre `192.168.40.0/24`)

| Segmento | Función | Hosts |
|----------|---------|-------|
| Portal de estudiantes | Frontend de matrícula y notas | 30 |
| API académica | Backend de inscripciones | 14 |
| Base de datos | Notas y expediente (sensible) | 10 |

## Giro de tu caso

- El **portal quedó "dinámico"**: además de IP fija, demuestra **DHCP** en una
  subred usando IPs de tu rango (te sirve de captura extra).
- La **DB NO se expone** (seguridad de Calificaciones); `docker port` vacío.
- Tu `POST /pagos` equivale a **registrar una matrícula** que debe persistir
  (prueba 9).

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