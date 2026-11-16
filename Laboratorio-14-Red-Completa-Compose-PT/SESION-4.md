# Sesión 4 — Integración, respaldo y demo del stack

Laboratorio N.º 14 · Clase 4

## Objetivo de la sesión

Cerrar el ciclo: levantar **todo** el laboratorio con un solo comando,
demostrar que los **datos sobreviven** (respaldo y restauración de PostgreSQL),
simular la **caída y recuperación** de un servicio, y presentar el stack real.
Es el ensayo general del Proyecto Final.

> **Sesión independiente:** no requiere las anteriores. Si partes de cero, usa la
> carpeta ya orquestada:
>
> ```bash
> cp -r sesion-4 ~/lab14/sesion-4 && cd ~/lab14/sesion-4
> docker compose up -d --wait
> ```

## Paso 1: Reproducir todo desde cero

Borra todo y demuestra que el entorno es **reproducible** (esa es la promesa de
la orquestación):

```bash
cd ~/lab14/sesion-3          # o ~/lab14/sesion-4 si usaste la carpeta
docker compose down -v --remove-orphans   # -v borra también el volumen (a propósito)
docker compose up -d --wait
docker compose ps                          # todo (healthy)
```

```text
[Checkpoint] Todo levantado con 2 comandos · nadie tocó un `docker run`
```

## Paso 2: Respaldo y restauración de la base de datos

La DB es el activo más crítico; el respaldo es tan importante como el despliegue:

```bash
# 1. Meter algún dato
docker exec -i db-srv psql -U appuser -d postgres -c \
  "CREATE TABLE IF NOT EXISTS visitas(id serial primary key, ts timestamptz default now());
   INSERT INTO visitas DEFAULT VALUES;"

# 2. Respaldo lógico (pg_dump) al host
docker exec db-srv pg_dump -U appuser postgres > respaldo_lab14.sql
head -5 respaldo_lab14.sql ; ls -lh respaldo_lab14.sql

# 3. Simular desastre
docker compose down -v          # borra el volumen con los datos
docker compose up -d --wait
docker exec -i db-srv psql -U appuser -d postgres -c "SELECT count(*) FROM visitas;"
#  ↑ debe dar error: la tabla ya no existe

# 4. Restaurar
docker exec -i db-srv psql -U appuser -d postgres < respaldo_lab14.sql
docker exec -i db-srv psql -U appuser -d postgres -c "SELECT count(*) FROM visitas;"
#  ↑ debe devolver el conteo original
```

```text
[Checkpoint] count(*) antes = count(*) después de restaurar
```

## Paso 3: Auto-recuperación (self-healing)

Demuestra que la orquestación reacciona sola ante una falla:

```bash
# Con restart: unless-stopped, mata el proceso dentro de un contenedor
docker compose exec api pkill -f app.py
sleep 6
docker compose ps api        # debe estar (healthy) otra vez, solo
```

> Esta es la primera propiedad de un orquestador: **reconciliar el estado
> deseado**. Swarm y Kubernetes lo hacen igual, pero a escala multi-nodo.

## Paso 4: Demo integrada (10 min por equipo)

Presenta en orden, sin editar nada en vivo:

1. **Docker**: `docker compose ps` mostrando todo `(healthy)`, con la API en 2
   réplicas.
2. **Evidencia de segmentación**: `front` no alcanza `back`; `8080` es la única
   puerta abierta; la DB sin `ports:`.
3. **Monitoreo**: netdata o `tcpdump` mostrando tráfico de un servicio.
4. **Respaldo**: la restauración del Paso 2 funcionó.

## Paso 5: Del laboratorio al Proyecto Semestral

Checklist (marca el estado de tu proyecto real):

| # | Verificación | ¿Listo? |
|---|--------------|---------|
| 1 | La base de datos está en una red interna y **no** publica puertos | ☐ |
| 2 | El acceso al host es **solo por llave SSH** (probado sin password) | ☐ |
| 3 | Hay DNS interno resolviendo los nombres de los servicios | ☐ |
| 4 | La app está **escalada** (≥2 réplicas de front/back) | ☐ |
| 5 | Existe **evidencia de monitoreo** (capturas del stack, no de tu PC) | ☐ |
| 6 | **No hay credenciales** en el YAML ni en el código (`grep` limpio) | ☐ |
| 7 | El `docker compose up` reproduce todo **desde cero** | ☐ |
| 8 | El README del repo explica el despliegue paso a paso | ☐ |
| 9 | Hay un **diagrama de la red** coherente con el stack (opcional: Packet Tracer) | ☐ |
| 10 | El respaldo/restauración de la DB está probado | ☐ |

## Preguntas de la sesión

1. ¿Por qué `docker compose down` (sin `-v`) **no** pierde los datos pero
   `down -v` sí? ¿Qué implica eso para elegir `restart`/`volumes` en producción?
2. El self-healing de Compose reinicia contenedores, pero **no** reprograma
   tareas entre máquinas. Explica la diferencia con lo que haría Swarm con 3
   nodos.
3. Elabora la frase final del laboratorio con tus palabras: *¿por qué el
   bastión real es el host/VM y no un contenedor?* Susténtala con algo que
   rompiste y arreglaste hoy.

## Entregable de la sesión

- Salida de `docker compose ps` con todo `(healthy)`.
- `respaldo_lab14.sql` + evidencia de restauración (los dos `count(*)`).
- Resultado del self-healing (api volvió a `(healthy)` sola).
- Demo del Paso 4 y checklist del Paso 5 respondido.
