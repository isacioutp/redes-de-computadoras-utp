# Sesión 2 — Monitoreo de la red y acceso seguro

Laboratorio N.º 14 · Clase 2 · **Pista A (Docker Compose)**

## Objetivo de la sesión

**Medir** la red (ancho de banda, latencia, tráfico por capa) y **asegurar su
acceso**: la única entrada al host será SSH autenticado por llave — el **bastión
real**.

> **Contexto de redes:** esta sesión cubre dos temas del curso — **monitoreo de
> red** (métricas y herramientas) y **seguridad de acceso** (SSH, bastión).
> Compose solo ejecuta la red; lo que se aprende son las métricas y el control
> de acceso.

> **Sesión independiente:** no requiere la Sesión 1. Si empiezas aquí, usa la
> plantilla ya segmentada:
>
> ```bash
> cp -r sesion-2 ~/lab14/sesion-2 && cd ~/lab14/sesion-2
> docker compose up -d
> ```

> **Pista opcional:** [PACKET-TRACER.md](PACKET-TRACER.md) es **autónomo** y
> **no influye** en esta sesión ni en su nota.

## Paso 1: Verifica la segmentación

No se reconstruye nada: se **comprueba** que la red está aislada.

```bash
cd ~/lab14/sesion-2        # o tu carpeta de trabajo
docker compose ps

# front → db debe fallar (la red interna solo la ve el API)
docker compose exec web sh -c "nc -zv db 5432" 2>&1 | tail -1

# api → db debe funcionar (el único puente)
docker compose exec api python -c \
  "import socket as s; s.create_connection(('172.28.20.20',5432),3); print('API → DB OK')"
```

```text
[Checkpoint] web ↛ db · api → db OK
```

## Paso 1b: Monitorea el tráfico (métricas de red)

Genera tráfico y obsérvalo por capa, igual que medirías una LAN real.

```bash
# Capa 4/7: captura tráfico HTTP en la interfaz del contenedor web
docker exec -d web-srv apk add -q tcpdump; sleep 3
docker exec web-srv tcpdump -i eth0 -c 20 -n port 80 > tcpdump-web.txt &
sleep 1
curl -s http://localhost:8080/ >/dev/null     # genera el tráfico
wait; cat tcpdump-web.txt

# Capa 3/4: ancho de banda por conexión (si el host lo tiene)
sudo iftop -i br-<red> -t -s 10

# Panel de métricas por contenedor (red, CPU, disco)
# (usa el nombre real de la red: `docker network ls` → busca la red *front)
FRONT=$(docker network ls --format '{{.Name}}' | grep '_front' | head -1)
docker run -d --name monit --network "$FRONT" \
  -p 19999:19999 \
  -v /proc:/host/proc:ro -v /sys:/host/sys:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  netdata/netdata
# abrir http://localhost:19999
```

> **Sin Packet Tracer:** esta sesión no requiere Simulation mode ni `.pkt`. Si
> además haces la pista opcional, comparar `tcpdump` con Simulation mode es un
> buen ejercicio, pero **no cuenta** para esta nota.

## Paso 2: El host como bastión — SSH por llave, sin contraseña

**Por qué aquí y no un contenedor:** un bastión real es un host endurecido cuyo
compromiso derriba *todo* lo que protege. Ese host eres tú. **Seguridad de
borde:** la única entrada será SSH por llave.

```bash
mkdir -p ~/lab14-ssh && cd ~/lab14-ssh

# 1. Par de llaves (una vez para todo el semestre)
ssh-keygen -t ed25519 -f id_lab14 -C "alumno@lab14" -N ""
chmod 600 id_lab14

# 2. Endurece tu sshd (en /etc/ssh/sshd_config):
#    PasswordAuthentication no
#    PermitRootLogin no
#    (recarga: sudo systemctl reload sshd)

# 3. Instala tu llave pública
cat id_lab14.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 4. Acceso SIN contraseña (el host como bastión)
ssh -i id_lab14 usuario@localhost 'echo "Entré al bastión sin password"'

# 5. La contraseña ya no sirve
ssh -o PubkeyAuthentication=no -o PreferredAuthentications=password \
    usuario@localhost true ; echo "exit=$?"
```

```text
[Checkpoint] Entro por llave · la autenticación por contraseña está bloqueada.
```

> **Recuerda:** desde el bastión (el host) alcanzas las redes Docker; desde
> fuera, lo único abierto es el 22 endurecido y el 8080 (web) — nada más.

## Preguntas de la sesión

1. ¿Qué mecanismo del host Linux (puentes, `iptables`) implementa en Docker el
   aislamiento de la red `back`, y por qué es "menos visible" que una ACL en un
   router?
2. `front` no alcanza `back` (Paso 1). ¿Qué pasa exactamente si quitas
   `internal: true` de `back`? Ejecútalo y descríbelo.
3. Tu API tiene interfaces en `front` y `back` (es el "puente"). ¿Por qué en
   Docker es aceptable para una API pero **no** para una base de datos?
4. Con la llave instalada, explica por qué el **host** es un bastión más seguro
   que intentar "hacer de bastión" con un contenedor.

## Entregable de la sesión

- Capturas de monitoreo (`tcpdump` y netdata o `iftop`) con tráfico real.
- Prueba de segmentación (`web ↛ db`, `api → db`).
- SSH por llave funcionando **y** rechazo de la autenticación por contraseña.
- Respuestas a las preguntas 1-4.
