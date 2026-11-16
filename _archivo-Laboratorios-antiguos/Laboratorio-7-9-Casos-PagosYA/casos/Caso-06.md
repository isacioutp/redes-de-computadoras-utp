# CASO 06 — EnvíosYa: logística y rastreo

Laboratorio N.º 7-9 · equipo de 4-6 · **presentas la siguiente clase**.

> Tu trabajo: la **red completa** del rastreo de envíos en tiempo real. Marco
> general en [CASO.md](../CASO.md); aquí van **tus parámetros y tu giro**.

## Tu red (3 segmentos · VLSM sobre `192.168.20.0/24`)

| Segmento | Función | Hosts |
|----------|---------|-------|
| API de tracking | Backend que recibe posiciones | 28 |
| Portal web | Países/clientes consultan el envío | 10 |
| Base de datos | Rutas y paquetes (sensible) | 12 |

## Giro de tu caso

- El tracking usa **TCP** para consulta y puedes demostrar el **handshake**
  (`tcpdump` SYN/SYN-ACK/ACK) en cada consulta de un paquete.
- La **DB NO se expone**; `docker port` vacío.
- Tu `POST /pagos` equivale a **registrar un paquete en ruta** (prueba 9) y debe
  persistir por la subred interna.

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