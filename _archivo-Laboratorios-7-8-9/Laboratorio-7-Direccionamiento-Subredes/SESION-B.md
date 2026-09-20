# Laboratorio N.° 7 — Direccionamiento IP y Subredes · Sesión B: ICMP, enrutamiento, DHCP y el esquema del proyecto

Semana 7 · Clase 2 · ICMP, enrutamiento, DHCP y el esquema del proyecto

Cubre: Parte 3 (ICMP, router contenedor, rutas y traceroute), Parte 4 (DHCP con dnsmasq y ARP) y Parte 5 (esquema VLSM del proyecto + `docker-compose.yml`) del guion original. Preguntas originales 6 a 14.

## Objetivo de la sesión

Diagnosticar la red con **ICMP**, habilitar la comunicación entre subredes con
un **router contenedor** y tablas de enrutamiento, levantar un **DHCP real**
con dnsmasq, y terminar diseñando el **esquema VLSM** que alimenta el
Avance N.º 1 del Proyecto Semestral.

## Retoma la sesión A

Esta sesión reutiliza las subredes `frontend`, `backend`, `dbsub`, `admin`,
`linknet` y los contenedores `web-front`, `api-backend`, `db-main`,
`admin-pc` de la Sesión A. **Verifica** que siguen en pie:

```bash
docker ps
docker network ls
```

Si no existieran, vuelve a ejecutar el Paso 2.2 de la Sesión A para recrearlas
antes de continuar.

## Parte 3: ICMP — diagnóstico de la red

### Paso 3.1: ping entre subredes — la barrera del router

**Prueba** comunicar dos subredes distintas y **observa** el error ICMP:

```bash
docker exec web-front ping -c 2 api-backend   # Mismo host? No → falla (sin router)
docker exec web-front ping -c 2 192.168.60.34 # IP real de api-backend
```

**Pregunta 1**: ¿Por qué falla el ping entre `web-front` y `api-backend` si
están en distintas subredes? ¿Qué paquete ICMP de error devuelve Docker?
(Entrega la salida de tcpdump si puedes.)

### Paso 3.2: Comunicación inter-subred usando un router (contenedor)

Muchas veces un contenedor puede actuar como router si habilitamos el reenvío.
**Construye** el router y **agrega** las rutas:

```bash
# Crear contenedor "router" conectado a ambas subredes
docker run -d --name router-lab7 --network frontend alpine sh -c "sleep 3600"
docker network connect backend router-lab7

# Habilitar reenvío de IP en el router
docker exec router-lab7 sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

# Ver ambos interfaces del router
docker exec router-lab7 ip addr show
```

**Pregunta 2**: Observa las IPs del router en ambas subredes. ¿Qué tendrías que
agregar en las tablas de enrutamiento de `web-front` y `api-backend` para que se
comuniquen a través del router? (Pista: `ip route add default via <neigh>`)

```bash
# Agregar ruta default en web-front hacia el router (IP en su subred)
docker exec web-front ip route add default via 192.168.60.2

# Agregar ruta default en api-backend hacia el router (IP en su subred)
docker exec api-backend ip route add default via 192.168.60.34

# Probar de nuevo
docker exec web-front ping -c 2 192.168.60.34
```

> Nota: por el aislamiento NAT del bridge, puede requerir habilitar ip_forward
> en el host con `sudo sysctl -w net.ipv4.ip_forward=1`. En un entorno real
> con Packet Tracer se usaría un router físico/lógico.

**Pregunta 3**: Luego de agregar la ruta, ¿se comunican ahora las subredes?
¿Qué rol cumple la tabla de enrutamiento en la capa de red?

### Paso 3.3: traceroute — ruta paquete a paquete

**Mide** los saltos necesarios para salir de la red:

```bash
# Desde el host hacia el gateway de docker
traceroute 192.168.60.1 2>/dev/null || tracepath 192.168.60.1

# Dentro del contenedor hacia internet
docker exec web-front sh -c "apk add --no-cache traceroute 2>/dev/null;\
  traceroute -m 10 google.com"
```

**Pregunta 4**: ¿Cuántos saltos (TTL) se necesitan para llegar a internet desde
el contenedor? ¿Qué relación tienen el TTL con ICMP?

## Parte 4: DHCP — asignación automática de IPs

### Paso 4.1: Levantar un DHCP real (dnsmasq)

**Construye** un servidor DHCP con dnsmasq en una subred:

```bash
# Red con DHCP automático
docker network create dhcp-lab --subnet 10.99.0.0/24 --gateway 10.99.0.1

# Servidor DHCP (dnsmasq) en la subred, rango de 50-100
docker run -d --name dhcp-srv --network dhcp-lab \
  --cap-add=NET_ADMIN \
  jpillora/dnsmasq \
  --dhcp-range=10.99.0.50,10.99.0.100,255.255.255.0,12h \
  --dhcp-option=3,10.99.0.1

docker logs dhcp-srv | tail -20
```

### Paso 4.2: Cliente DHCP (sin IP fija)

**Levanta** un cliente sin IP fija y **observa** el intercambio DHCP:

```bash
# Crear un contenedor sin IP asignada manualmente (se pide por DHCP)
docker run -d --name dhcp-client --network dhcp-lab --cap-add=NET_ADMIN \
  alpine sleep 3600

docker exec dhcp-client rm /etc/resolv.conf 2>/dev/null || true

# Ejecutar cliente DHCP (udhcpc)
docker exec dhcp-client sh -c "apk add --no-cache dhclient 2>/dev/null;\
  udhcpc -i eth0 -f" | head -20
```

Si prefieres usar la herramienta nativa de DHCP en Docker, muchos bridges
tipos `macvlan` hacen asignación automática con `docker-proxy`. También se
puede ver la **firma del DHCP** observando los paquetes:

```bash
# Espiar los paquetes DHCP (broadcast UDP 68)
docker exec dhcp-srv tcpdump -i eth0 udp port 67 -nn
# en otra terminal ejecutar udhcpc
```

**Pregunta 5**: ¿Qué mensajes intercambia el cliente con el servidor DHCP:
`DISCOVER`, `OFFER`, `REQUEST`, `ACK`? ¿En qué capa y puertos viajan?

**Pregunta 6**: El DHCP asigna una IP **temporalmente** (lease). ¿Para qué
sirve el TTL/lease? ¿Qué pasa cuando se vence?

### Paso 4.3: Ver el ARP generado por DHCP

**Captura** el ARP que dispara la primera comunicación:

```bash
docker exec dhcp-srv tcpdump -i eth0 -nn arp
# en otra terminal: forzar una petición
docker exec dhcp-client ping -c 1 10.99.0.1
```

**Pregunta 7**: ¿Cómo arranca la comunicación sin conocer la MAC del otro?
¿Qué papel juega la caché ARP después del primer intercambio?

## Parte 5: Aplicación al proyecto semestral (Avance N.º 1)

### Paso 5.1: Diseñar la red de tu proyecto

Tu equipo de desarrollo desplegará una aplicación web completa. **Diseña** el
esquema de direccionamiento para los siguientes servicios (en un futuro
Laboratorio N.º 9-10 lo levantarás con Docker Compose):

| Servicio | Hosts | Subred sugerida | Rango utilizable | Broadcast |
|----------|-------|-----------------|------------------|-----------|
| Balanceador/web (nginx) | 3 | | | |
| API (Node/Python) | 5 | | | |
| Base de datos | 2 | | | |
| Servidor de archivos | 1 | | | |
| Monitoreo | 2 | | | |
| Enlace a internet | 2 hosts | | | |

Usa la red base `172.20.30.0/24` y haz **VLSM** (de mayor a menor). Completa:

```
172.20.30.0/24
├── ...
```

> Importante: esta tabla VLSM es el **insumo del Avance N.º 1** del Proyecto
> Semestral (diagrama + direccionamiento IP). Guárdala y enumérala en tu
> avance.

**Pregunta 8**: ¿Cuántas IPs se desperdician al usar `/24` completo si solo
requieres 10 hosts? ¿Cómo mejora VLSM el uso del espacio de direcciones?

### Paso 5.2: Implementar el esquema en Docker Compose

**Implementa** el esquema en `docker-compose.yml`. Crea el archivo:

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    networks:
      public-subnet:
        ipv4_address: 172.20.30.10
    ports:
      - "8080:80"

  api:
    image: python:3.11-slim
    command: python -c "import time; time.sleep(3600)"
    networks:
      public-subnet:
        ipv4_address: 172.20.30.20
      db-subnet:
        ipv4_address: 172.20.30.130

  db:
    image: postgres:15-alpine
    networks:
      db-subnet:
        ipv4_address: 172.20.30.140
    environment:
      POSTGRES_PASSWORD: labpass123

networks:
  public-subnet:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.30.0/27
          gateway: 172.20.30.1
  db-subnet:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.30.128/28
          gateway: 172.20.30.129
```

**Levanta** la composición y **verifica** las subredes:

```bash
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yml ps
docker network inspect $(docker network ls -q --filter name=default) 2>/dev/null | grep -E '"Name"|"IPv4Address"'
```

**Pregunta 9**: ¿Qué subredes definiste? ¿La `api` puede alcanzar a `db` y a
`web` a la vez? ¿Eso es deseable para una arquitectura segura?

## Entregable de la sesión

Sube a la tarea:

1. Captura del ping fallido (Paso 3.1) y del ping exitoso con rutas (Paso 3.2).
2. Salida del `traceroute` (Paso 3.3).
3. Captura del DHCP (`DISCOVER`/`OFFER`/`REQUEST`/`ACK`) y del ARP (Parte 4).
4. Tabla VLSM del Paso 5.1 completada (**insumo del Avance N.º 1**).
5. `docker-compose.yml` final del Paso 5.2.
6. Respuestas a las **9 preguntas** de la sesión.
7. Conclusión (3-5 líneas): cómo aplicarías este diseño al proyecto del curso.

## Rúbrica de la sesión

| Criterio | Puntos |
|----------|--------|
| ICMP y enrutamiento (Parte 3: router contenedor y rutas) | 15 |
| DHCP y ARP (Parte 4) | 15 |
| Esquema VLSM del proyecto + `docker-compose.yml` (Parte 5) | 15 |
| Respuestas a las preguntas 1–9 | 5 |
| **Total** | **50** |