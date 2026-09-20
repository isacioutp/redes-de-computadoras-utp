# CASO 07 — RutaX: transporte y movilidad urbana

Laboratorio N.º 7-9 · equipo de 4-6 · **presentas la siguiente clase**.

> Tu trabajo: la **red completa** que conecta taxis/coches con la plataforma.
> Marco general en [CASO.md](../CASO.md); aquí van **tus parámetros y tu giro**.

## Tu red (3 segmentos · VLSM sobre `192.168.200.0/24`)

| Segmento | Función | Hosts |
|----------|---------|-------|
| API de conductores | Backend de ubicaciones | 30 |
| Portal web | App del pasajero | 8 |
| Base de datos | Viajes y pagos (sensible) | 12 |

## Giro de tu caso

- Utiliza **dos routers en cadena** (router-A une `sub-web` y `sub-api`;
  router-B une `sub-api` y `sub-db`) para que el `traceroute` muestre **3
  saltos** en lugar de 2: portal → router-A → router-B → API/DB. Esto demuestra
  el concepto de **TTL** decreciendo en cada salto y la importancia de cada
  router en la cadena.
- La **DB NO se expone**; `docker port` vacío.
- Tu `POST /pagos` equivale a **registrar un viaje completo** (prueba 9).

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