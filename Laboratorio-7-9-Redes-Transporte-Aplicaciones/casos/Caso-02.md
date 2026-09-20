# CASO 02 — MediSalud: historia clínica digital

Laboratorio N.º 7-9 · equipo de 4-6 · **presentas la siguiente clase**.

> Tu trabajo: la **red completa** que sostiene el registro clínico de una clínica.
> Marco general en [CASO.md](../CASO.md); aquí van **tus parámetros y tu giro**.

## Tu red (3 segmentos · VLSM sobre `192.168.5.0/24`)

| Segmento | Función | Hosts |
|----------|---------|-------|
| API de pacientes | Backend de citas e historial | 20 |
| Portal web | Portal del paciente | 12 |
| Base de datos | Historial clínico (sensible) | 14 |

## Giro de tu caso

- La información clínica es sensible: la **DB va aislada en su subred** (el
  historial no puede salir sin autorización; `docker port` debe mostrar nada).
- **HTTPS obligatorio en todo el trayecto** hacia el usuario: el portal se sirve
  por HTTPS (autofirmado, `curl -k` 200) y puedes **redirigir 303** del 80 al 443.
- El `POST` que registra un pago equivale a **registrar una consulta/cita** que
  debe persistir (prueba 9).

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