# Sesión 3 — Orquestación con Docker Compose

Laboratorio N.º 14 · Clase 3

## Objetivo de la sesión

Convertir el stack "a mano" en un stack **orquestado con Compose**: reproducir
todo con un solo `up`, escalar réplicas, declarar **dependencias y healthchecks**,
manejar **secretos** (sin contraseñas en texto plano) y usar **perfiles** para
arrancar la app en modo desarrollo vs. producción. **Sin Docker Swarm**: Swarm
es multi-nodo y aquí trabajamos en un host; se verá teóricamente al final.

> **Sesión independiente:** no requiere las anteriores. Si partes de cero, usa la
> carpeta ya segmentada:
>
> ```bash
> cp -r sesion-3 ~/lab14/sesion-3 && cd ~/lab14/sesion-3
> docker compose up -d
> ```
>
> Esa carpeta ya trae `api/`, `dnsmasq.conf` y `db_pass.txt`; aquí **solo
> reescribirás el `docker-compose.yml`**.
>
> Packet Tracer **no** se usa en esta sesión.

## Contexto: ¿qué es orquestar?

Ejecutar *un* contenedor es fácil. La orquestación aparece cuando hay varios
servicios, réplicas, dependencias, actualizaciones y secretos. Compose declara
**el estado deseado** y el motor lo reconcilia: crea, escala, reinicia lo que
falla y respeta el orden de arranque.

| | Hacerlo a mano (`docker run`) | Orquestado (`docker compose`) |
|--|-------------------------------|-------------------------------|
| Reproducir el entorno | 8 comandos que se olvidan | 1 archivo + `up` |
| Escalar | copiar/pegar comandos | `--scale api=2` |
| Dependencias | arrancar en el orden correcto tú | `depends_on` + `healthcheck` |
| Secretos | `-e PASSWORD=...` visible | archivo `secrets:` montado en `/run/secrets` |
| Estado de salud | preguntar manualmente | `docker compose ps` con `(healthy)` |

## Paso 1: El `docker-compose.yml` completo y orquestado

La carpeta [`sesion-3/`](sesion-3/README.md) ya trae `api/` (código + Dockerfile),
`dnsmasq.conf` y `db_pass.txt`. Aquí **solo reescribirás el `docker-compose.yml`**
por esta versión declarativa (todo reproducido con un comando):

```yaml
# docker-compose.yml
services:
  dns:
    image: strm/dnsmasq
    container_name: dns-corp
    volumes: [ ./dnsmasq.conf:/etc/dnsmasq.conf:ro ]
    networks:
      front: { ipv4_address: 172.28.10.53 }
    command: ["-k", "--log-facility=-", "-u", "root"]   # -u root evita el fallo "setting capabilities"
    healthcheck:
      test: ["CMD", "nslookup", "web.local", "127.0.0.1"]
      interval: 5s
      timeout: 3s
      retries: 5
    restart: unless-stopped

  web:
    image: nginx:alpine
    container_name: web-srv
    ports: ["8080:80"]
    depends_on:
      api:
        condition: service_healthy     # no arranca hasta que la API esté sana
    networks:
      front: { ipv4_address: 172.28.10.10 }
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost/"]
      interval: 5s
      timeout: 3s
      retries: 5
    restart: unless-stopped

  api:
    build: ./api
    environment:
      DB_HOST: db.local
      DB_USER: appuser
    networks: [front, back]            # el puente front↔back
    expose: ["8000"]                   # visible SOLO dentro de la red
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request as u;u.urlopen('http://localhost:8000/ping')"]
      interval: 5s
      timeout: 3s
      retries: 5
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: db-srv
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD_FILE: /run/secrets/db_pass   # ← lee del secreto
    secrets: [db_pass]
    volumes: [pgdata:/var/lib/postgresql/data]
    networks:
      back: { ipv4_address: 172.28.20.20 }   # NUNCA publica puertos
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser"]
      interval: 5s
      retries: 5
    restart: unless-stopped

secrets:
  db_pass:
    file: ./db_pass.txt

networks:
  front:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.10.0/24
  back:
    driver: bridge
    internal: true
    ipam:
      config:
        - subnet: 172.28.20.0/24

volumes:
  pgdata: {}
```

```bash
docker compose up -d --wait      # --wait = espera a que los healthchecks pasen
docker compose ps                # dns, web, api y db deben decir (healthy)
```

> **Ajusta `dnsmasq.conf`:** como la API ya no tiene IP fija (para poder escalar),
> quita la línea `address=/api.local/...`. El servicio `api` se resuelve con el
> DNS de Docker; dnsmasq solo publica `web.local` y `db.local`.

## Paso 2: Escala la API (réplicas + balanceo por DNS)

```bash
docker compose up -d --scale api=2
docker compose ps api

# Compose crea N réplicas con el mismo nombre DNS; el DNS de Docker las devuelve todas.
# (El punto final de `api.` evita el dominio de búsqueda del host.)
docker compose exec web nslookup api.
```

```text
[Checkpoint] nslookup api → devuelve 2+ direcciones (balanceo básico por DNS)
```

> **Comparación honesta:** Compose balancea "en el DNS" (round-robin de
> nombres), no con un proxy. Docker Swarm sí tiene ingress mesh y balanceo
> real — por eso Swarm se ve como teoría, no con `docker run`.

## Paso 3: El secreto NO está en el código

```bash
# La contraseña vive en el archivo, se monta en el contenedor y NO aparece en el YAML
docker exec db-srv cat /run/secrets/db_pass       # muestra el secreto
docker inspect db-srv | grep -i POSTGRES_PASSWORD # NO debe mostrar la clave
grep -n "una-clave" docker-compose.yml            # no debe haber coincidencias
```

```text
[Checkpoint] /run/secrets/db_pass existe · el YAML no contiene la contraseña
```

## Paso 4: Ciclo de vida orquestado (update, escala y down)

```bash
docker compose logs api --tail 20      # decide si un servicio está sano o no
docker compose restart api
docker compose up -d --scale api=1     # desescala
docker compose stop && docker compose start   # conserva contenedores y volúmenes
docker compose down                    # apaga (los datos SOBREVIVEN en pgdata)
```

> **Nota sobre Swarm (solo teoría):** cuando el despliegue pasa a **varios
> hosts**, Compose ya no alcanza: se necesita un orquestador multi-nodo.
> Docker Swarm añade cluster (`manager`/`worker`), red **overlay** entre nodos,
> balanceo ingress mesh, *rolling update* y *secretos gestionados por el
> clúster*. `docker stack deploy` usa el **mismo** YAML de Compose, así que lo
> aprendido hoy migra directo. Se verá en la siguiente unidad o en el Proyecto
> Final como profundización.

## Paso 5: Puente con el Proyecto Semestral

Este `docker-compose.yml` **es** la plantilla del Proyecto Final. Adáptalo:

- [ ] Cambiar imágenes genéricas por las de la app de tu equipo.
- [ ] Añadir `secrets:` para *todas* las credenciales (nada en `environment:`).
- [ ] Confirmar que la DB está solo en `back` sin `ports:`.
- [ ] Definir `healthcheck` en web y api (no solo db).
- [ ] Añadir un servicio de monitoreo (netdata/cAdvisor) en `front`.

## Preguntas de la sesión

1. ¿Por qué `db` no tiene `ports:` pero la web **sí**? Relaciona con la
   pregunta 1 de la Sesión 1 (¿qué protege `internal: true` y qué no?).
2. `depends_on: condition: service_healthy` espera a que la API esté sana antes
   de arrancar la web. ¿Qué problema evita respecto a solo usar `depends_on` sin
   condición? Piensa en la secuencia de arranque de web y API.
3. `docker inspect db-srv | grep PASSWORD` no revela la clave pero
   `docker exec db-srv cat /run/secrets/db_pass` sí. ¿Por qué la primera es una
   fuga inaceptable y la segunda no? ¿Qué principio de seguridad se aplica?
4. Si mañana el stack debe correr en 3 máquinas, enumera **3 cosas** que
   Compose no puede hacer y Swarm sí. (Revisa el README del Lab 12 para validar.)

## Entregable de la sesión

- `docker-compose.yml` completo (con `secrets:` y `healthchecks`).
- Captura de `--scale api=2` + `nslookup api` devolviendo varias IPs.
- Captura del secreto en `/run/secrets` y del `grep` sin coincidencias.
- Respuestas a las preguntas 1-4.
