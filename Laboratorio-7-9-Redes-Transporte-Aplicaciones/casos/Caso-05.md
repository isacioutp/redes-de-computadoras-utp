# CASO 05 — AgroScan: agricultura de precisión (IoT)

Laboratorio N.º 7-9 · equipo de 4-6 · **presentas la siguiente clase**.

> Tu trabajo: la **red completa** que conecta sensores de cosechas con el panel
> del agrónomo. Marco general en [CASO.md](../CASO.md); aquí van **tus parámetros
> y tu giro**.

## Tu red (3 segmentos · VLSM sobre `192.168.100.0/24`)

| Segmento | Función | Hosts |
|----------|---------|-------|
| API de sensores | Backend que recibe lecturas | 30 |
| Portal web | Panel del agrónomo | 8 |
| Base de datos | Historial de lecturas (sensible) | 12 |

## Giro de tu caso

- El **DNS es clave**: tus sensores se apuntan por nombre
  (`sensor1.agroscan.local`…) y tu `pagosya.local` debe resolver a la IP del
  portal (`dig`). Muestra el **traceroute** que cruza por el router (2 saltos).
- La **DB NO se expone**; `docker port` vacío.
- Tu `POST /pagos` equivale a **enviar una lectura de sensores** que persiste a
  través de la subred interna (prueba 9).

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