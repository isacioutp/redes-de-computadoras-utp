# Laboratorio N.° 12 — Orquestación de Servicios y Despliegue de Aplicaciones · Sesión B: Secretos, overlay, actualizaciones y stack

Semana 11 · Clase 2

Cubre las **Partes 3, 4, 5, 6 y 7** del laboratorio original: secretos en
swarm, red overlay, rolling update y rollback, `stack deploy` a partir del
Compose, la tabla comparativa de orquestación (VMs, nube, contenedores) y la
práctica integradora de tu proyecto semestral.

## Objetivo de la sesión

Operar el Swarm en modo producción: gestionar secretos que las apps montan en
`/run/secrets`, crear redes overlay, actualizar un servicio sin caída (rolling
update) y revertirlo (rollback), desplegar un stack completo y cerrar con una
reflexión comparativa y la metodología aplicada a tu proyecto.

## Pasos

### Paso 1: Crea secretos de forma segura

Crea los secretos y un servicio de base de datos que los usa:

```bash
printf "labpass123" | docker secret create db_pass -
printf "admin"     | docker secret create db_user -

# servicio de base de datos que usa los secretos (montados en /run/secrets)
docker service create --name db-swarm \
  --secret db_pass \
  --secret db_user \
  --network ingress \
  postgres:15-alpine sleep 3600   # demostración (POSTGRES_PASSWORD en K8s usa secrets)

docker exec $(docker ps -qf name=db-swarm) bash -c 'cat /run/secrets/db_pass; echo'
```

> **Checkpoint:** el comando debe imprimir `labpass123`; el secreto está montado
> en `/run/secrets/db_pass`. Captúralo.

### Paso 2: Reflexiona sobre la gestión de secretos

Los secretos NO van en el código. Revisa las opciones para gestionarlos y
decide cuál usarías en tu proyecto (Pregunta 2).

### Paso 3: Crea una red overlay segura

Crea la red overlay y un servicio de 2 réplicas que se resuelve por nombre:

```bash
docker network create --driver overlay backoverlay 2>/dev/null
docker service create --name api-overlay \
  --network backoverlay \
  --replicas 2 \
  python:3.11-slim sleep 3600

# Verificar resolución del servicio en la red overlay
docker exec $(docker ps -qf name=api-overlay) \
  sh -c "apk add --no-cache bind-tools -q 2>/dev/null; nslookup api-overlay"
```

### Paso 4: Actualiza y revierte el servicio (rolling update + rollback)

Publica una nueva versión de la imagen de `web-mesh` de a una, y si fallara,
revierte:

```bash
#-publicar varias versiones
docker service update --image nginx:1.25 web-mesh --update-delay 5s
docker service ps web-mesh
```

```bash
# si fallara: rollback
docker service rollback web-mesh
```

> **Checkpoint:** captura `docker service ps web-mesh` donde se ve la imagen
> antigua y la nueva (rolling update). Si lanzas el rollback, la imagen vuelve a
> `nginx:alpine`.

### Paso 5: Despliega el stack con `docker stack deploy`

Convierte el Compose de la Sesión A en un stack de Swarm creando `stack.yml`:

```yaml
services:
  web:
    image: nginx:alpine
    ports: ["8090:80"]
    networks: [meshnet]
    deploy:
      replicas: 2
      update_config:
        order: start-first
  api:
    image: python:3.11-slim
    command: python -c "import time; print('API cluster'); time.sleep(3600)"
    networks: [meshnet]
    deploy:
      replicas: 3
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: labpass123
    networks: [meshnet]
    deploy:
      placement:
        constraints: [node.role == manager]
    volumes: [pgdata:/var/lib/postgresql/data]

networks:
  meshnet:
    driver: overlay
volumes:
  pgdata: {}
```

```bash
docker stack deploy -c stack.yml appfinal
docker stack services appfinal
docker stack ps appfinal
curl http://localhost:8090/
```

> **Checkpoint:** `docker stack ps appfinal` debe mostrar todas las tareas en
> estado *Running* y `curl http://localhost:8090/` debe responder.

### Paso 6: Completa la tabla comparativa de orquestación

Completa y explica CON TUS PALABRAS:

| Aspecto | Orquestación VMs | Nube (EC2/EKS) | Contenedores (Swarm/K8s) |
|---------|------------------|----------------|---------------------------|
| Start time | minutos | minutos/seg | segundos |
| Aislamiento | kernel completo | virtualization | kernel compartido |
| Migración | lenta (VMotion) | rápida | instantánea |
| Escalado | manual/plantillas | automático (ASG) | automático (replicas) |
| Costo | alto (licencias, host) | por uso | bajo |
| Autocuras | require | SI | SI |
| Red entre servicios | VLAN + firewall | VPC + SG | overlay / docker networks |

### Paso 7: Aplica la práctica integradora a tu proyecto

No te daremos la solución del proyecto; aquí tienes la **metodología** con las
piezas que ya dominaste en los Labs 10-12:

**Guion sugerido para tu equipo:**
1. **Diseña la LAN**: segmentos (web/API/db) → `docker network create`.
2. **Publica servicios**: Compose con red front/back (Lab 12 P1).
3. **Asegura el acceso**: llaves SSH + bastion (Lab 11) sobre la red privada.
4. **Monitorea**: netdata/iperf3/tcpdump (Lab 10) midiendo la app.
5. **Escala**: Swarm con réplicas y secrets (Lab 12 P2–P5).
6. **Documenta**: arquitectura + selección de orquestación (P6).

Realiza esta **autoevaluación** de tu stack final:
- ¿Cuántas réplicas necesita la API? ¿El web? ¿La DB?
- ¿Qué secretos expones (passwords de DB, API keys)?
- ¿Qué metricas de monitoreo mostrarías al director del proyecto?

## Preguntas de la sesión

1. ¿Dónde ve la app el secreto? ¿Por qué es mejor que inyectar la contraseña en
   variables de entorno?
2. Nombra 3 opciones para gestionar secretos (secreto de Swarm, .env local,
   vault/cloud). Compara cuál usarías en tu proyecto.
3. ¿Qué IP resuelve `api-overlay`? ¿En qué se diferencia una red **overlay**
   (swarm) de una **bridge** (compose) para un cluster multi-nodo?
4. Describe el proceso del rolling update: ¿actualiza todas a la vez o de a
   una? ¿Qué hace el `--update-delay`? ¿Y si la nueva imagen falla (rollback)?
5. ¿Qué comando despliega el stack completo? Detalla `docker stack ps`:
   ¿cuántas tareas y en qué estado?
6. ¿Qué significa la restricción `node.role == manager` para el DB (en sistemas
   con un solo nodo)? En multi-nodo, ¿por qué conviene poner DB/datos en un
   manager y no en cualquier worker?
7. ¿Cuándo elegirías Docker Compose, Swarm o Kubernetes aunque sean del
   proyecto? (En tu respuesta considera: complejidad del equipo, número de
   servicios, alta disponibilidad.)
8. En la nube real, ¿qué servicios de orquestación usarías para implementar la
   app de tu proyecto (ej. AWS ECS/EKS, Azure AKS, GCP GKE)? ¿qué role jugaría
   Docker en CI/CD?
9. **Reflexión**: lista las 3 ventajas más importantes de la orquestación que
   usarías en tu proyecto de software y cómo se conectan con los 3 labs
   anteriores (10, 11, 12).

## Entregable de la sesión

1. Evidencia del secreto montado en `/run/secrets/db_pass`.
2. Evidencia del rolling update y del rollback de `web-mesh`.
3. `stack.yml` creado y desplegado con `docker stack ps appfinal`.
4. Tabla comparativa de orquestación completa + reflexión integradora.
5. Respuestas a las preguntas 1–9.

## Rúbrica de la sesión (50 puntos)

| Criterio | Puntos |
|----------|--------|
| Secretos montados en `/run/secrets` | 10 |
| Red overlay + rolling update/rollback | 10 |
| `stack deploy` de `stack.yml` | 10 |
| Tabla comparativa de orquestación | 5 |
| Reflexión integradora (práctica del proyecto) | 5 |
| Preguntas 1–9 respondidas | 10 |
| **Total** | **50** |