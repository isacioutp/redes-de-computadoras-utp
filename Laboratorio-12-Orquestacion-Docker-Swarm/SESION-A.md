# Laboratorio N.° 12 — Orquestación de Servicios y Despliegue de Aplicaciones · Sesión A: Compose y Swarm: réplicas y balanceo

Semana 11 · Clase 1

Cubre las **Partes 1 y 2** del laboratorio original: el stack multi-servicio
con Docker Compose (web/api/db/redis), el escalado con réplicas y balanceo por
DNS, y el cluster Docker Swarm con el servicio replicado `web-mesh` y su
routing mesh.

## Objetivo de la sesión

Levantar una aplicación multi-servicio con Docker Compose, escalar la API a 3
réplicas y observar cómo Compose las balancea por DNS. Luego inicializas un
cluster Swarm con un nodo manager y creas un servicio replicado de 3 tareas que
responde detrás de un solo puerto gracias al routing mesh.

## Pasos

### Paso 1: Crea el stack base (web + api + db + redis)

Crea la carpeta y el archivo de Compose:

```bash
mkdir -p lab12 && cd lab12

cat > docker-compose.yml << 'YAML'
services:
  web:
    image: nginx:alpine
    ports: ["8080:80"]
    depends_on: [api]
    networks: [front]

  api:
    image: python:3.11-slim
    command: python -c "import time; print('API lista'); time.sleep(3600)"
    networks: [front, back]

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: labpass123
    networks: [back]
    volumes: [pgdata:/var/lib/postgresql/data]

  cache:
    image: redis:7-alpine
    networks: [back]

networks:
  front: {}
  back: {}

volumes:
  pgdata: {}
YAML

docker compose up -d
docker compose ps
```

### Paso 2: Escala el servicio api (réplicas)

Escala la API a 3 réplicas y observa el balanceo por DNS:

```bash
docker compose up -d --scale api=3
docker compose ps api

# DNS + balanceo básico: los 3 se llaman igual ("api")
docker compose exec web getent hosts api
```

> **Checkpoint:** `getent hosts api` debe devolver las 3 IPs de las réplicas.
> Ese es tu balanceo básico por DNS. Captúralo.

### Paso 3: Observa logs y dependencias

Monitorea la secuencia de arranque y las dependencias:

```bash
docker compose logs -f --tail=10 api &
docker compose start db && docker compose logs db | tail -3
kill %1
```

### Paso 4: Inicializa el Swarm (un nodo manager)

Activa el modo cluster con un nodo manager y verifica los roles:

```bash
docker swarm init --advertise-addr 127.0.0.1
docker node ls
```

### Paso 5: Crea un servicio replicado con balanceo

Crea el servicio web replicado (balanceado por routing mesh en puerto 9090):

```bash
# Servicio web replicado (balanceado por routing mesh en puerto 9090)
docker service create --name web-mesh \
  --replicas 3 \
  --network ingress \
  -p 9090:80 \
  nginx:alpine

docker service ls
docker service ps web-mesh
```

### Paso 6: Prueba el routing mesh

Verifica las IPs de las 3 tareas y prueba el puerto único:

```bash
# Ver las IPs de las 3 tareas
docker service ps web-mesh --format '{{.Name}}  {{.CurrentState}}  {{.Node}}'

# Desde el host, todas las réplicas responden en el mismo 9090
for i in 1 2 3; do curl -s http://localhost:9090/ -o /dev/null -w "%{http_code} "; done; echo ""
```

> **Checkpoint:** los 3 `curl` a `localhost:9090` deben responder `200`; el
> servicio está balanceado aunque solo veas un puerto.

## Preguntas de la sesión

1. ¿Cuántos servicios y cuántas redes hay? ¿Qué servicio está en ambas (front y
   back) y por qué?
2. ¿Cuántas IPs devuelve `getent hosts api` con las 3 réplicas? ¿Qué hace
   Compose para balancear? Compáralo con lo que haría un load balancer
   (nginx/haproxy).
3. ¿Qué orden de arranque impone `depends_on`? ¿El DB inició antes que la API?
   ¿Qué pasa si una réplica de api falla?
4. ¿Qué roles tiene el nodo (`MANAGER`/`WORKER`/`ACTIVE`)? ¿Cuál es la IP que
   usa el plano de control?
5. ¿Cuántas tareas (tasks) corrió Swarm para `web-mesh`? Prueba
   `curl http://localhost:9090/` varias veces. ¿Notas la IP que responde?
6. Si Swarm tiene 3 réplicas en el puerto 9090, ¿cuántas conexiones simultáneas
   puede atender? ¿Qué comportamiento esperarías si uno de los contenedores
   muere?

## Entregable de la sesión

1. `docker-compose.yml` creado (stack web/api/db/redis).
2. `docker compose ps api` con 3 réplicas y salida de `getent hosts api`.
3. `docker service ls` con `web-mesh` en 3/3 réplicas.
4. `curl http://localhost:9090/` respondiendo (routing mesh).
5. Respuestas a las preguntas 1–6.

## Rúbrica de la sesión (50 puntos)

| Criterio | Puntos |
|----------|--------|
| Stack Compose (web/api/db/redis) funcionando | 15 |
| `scale api=3` + `getent hosts api` | 10 |
| Swarm init + servicio `web-mesh` (3 réplicas) | 10 |
| Routing mesh respondiendo en el puerto 9090 | 5 |
| Preguntas 1–6 respondidas | 10 |
| **Total** | **50** |