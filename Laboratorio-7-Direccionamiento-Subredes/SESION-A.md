# Laboratorio N.° 7 — Direccionamiento IP y Subredes · Sesión A: Direcciones IP y subneteo VLSM con Docker

Semana 9 · Clase 1 · Direcciones IP y subneteo VLSM con Docker

Cubre: Parte 1 (Direccionamiento IP básico) y Parte 2 (Subneteo — crear múltiples subredes reales en Docker) del guion original. Preguntas originales 1, 2, 3, 4 y 5.

## Objetivo de la sesión

Verificar cómo se asigna una **dirección IP**, su **máscara** y su **gateway**
en un contenedor Docker, y luego **construir** cinco subredes reales con
subneteo **VLSM**, comprobando con Docker que cada una recibe las direcciones
del rango diseñado.

## Hazlo

Vas a **construir**, **verificar** y **documentar** cada subred: todo lo que
observes se completa en las tablas y preguntas del entregable.

## Parte 1: Direccionamiento IP básico

### Paso 1.1: Ver la dirección de tu equipo

**Observa** la configuración IP de tu equipo:

```bash
# Linux/macOS
ip addr show
# o Windows
# ipconfig /all
```

**Pregunta 1**: Escribe la IP, la máscara y el gateway de tu equipo. ¿A qué
red pertenece? ¿Cuántos hosts puede tener?

### Paso 1.2: Direccionamiento automático que Docker aplica

**Construye** una red Docker con un rango fijo y dos servidores, y **verifica**
las IP asignadas:

```bash
docker network create lab7-red --subnet 192.168.50.0/24 --gateway 192.168.50.1

docker run -d --name srv1 --network lab7-red alpine sleep 3600
docker run -d --name srv2 --network lab7-red alpine sleep 3600

# Ver IP asignadas
docker inspect -f '{{.Name}}: {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' srv1 srv2

# Dentro del contenedor, ver la configuración IP
docker exec srv1 ip addr show eth0
docker exec srv1 ip route
```

**Pregunta 2**: ¿Qué IPs asignó Docker? ¿Coinciden con el rango `/24`? ¿Qué
función crees que cumple el gateway `192.168.50.1`?

### Paso 1.3: Cálculo de red y hosts

**Calcula** la red, los hosts y el broadcast con `ipcalc`:

```bash
# ipcalc (instalar localmente si se quiere, o usar calculadora web)
sudo apt install -y ipcalc 2>/dev/null || true
ipcalc 192.168.50.0/24
```

| Campo | Valor |
|-------|-------|
| Dirección de red | 192.168.50.0 |
| Primer IP utilizable | 192.168.50.1 |
| Última IP utilizable | 192.168.50.254 |
| Broadcast | 192.168.50.255 |
| Total hosts | 254 |

**Pregunta 3**: Docker asigna IPs sucesivas (`10`, `11`, etc.). Si se usaran
todas las 254 IPs, ¿qué sucedería con el siguiente contenedor? Verifica la
resistencia con un contenedor más.

## Parte 2: Subneteo — crear múltiples subredes reales

### Paso 2.1: Diseñar el esquema

Vas a implementar la red de una empresa de software con 3 departamentos:

| Departamento | Hosts necesarios | Prefijo sugerido | Subred |
|--------------|------------------|------------------|--------|
| Frontend (dev) | 20 | /27 | 192.168.60.0/27 |
| Backend/API | 30 | /27 | 192.168.60.32/27 |
| Base de datos | 10 | /28 | 192.168.60.64/28 |
| Administración | 5 | /29 | 192.168.60.80/29 |
| Enlace routers | 2 hosts | /30 | 192.168.60.96/30 |

Cálculo VLSM (de mayor a menor), la tabla completada:

```
192.168.60.0/27   → red 192.168.60.0   broadcast .31  hosts 1-30
192.168.60.32/27  → red 192.168.60.32  broadcast .63  hosts 33-62
192.168.60.64/28  → red 192.168.60.64  broadcast .79  hosts 65-78
192.168.60.80/29  → red 192.168.60.80  broadcast .87  hosts 81-86
192.168.60.96/30  → red 192.168.60.96  broadcast .99  hosts 97-98
```

### Paso 2.2: Implementar cada subred en Docker

**Construye** las cinco subredes y levanta un servicio en cada una:

```bash
# Subred Frontend
docker network create frontend --subnet 192.168.60.0/27 --gateway 192.168.60.1
# Subred Backend
docker network create backend  --subnet 192.168.60.32/27 --gateway 192.168.60.33
# Subred Base de datos
docker network create dbsub    --subnet 192.168.60.64/28 --gateway 192.168.60.65
# Subred Administración
docker network create admin    --subnet 192.168.60.80/29 --gateway 192.168.60.81
# Subred enlace (2 hosts)
docker network create linknet  --subnet 192.168.60.96/30 --gateway 192.168.60.97

# Levantar servicio en cada subred
docker run -d --name web-front   --network frontend alpine sleep 3600
docker run -d --name api-backend --network backend  alpine sleep 3600
docker run -d --name db-main     --network dbsub    alpine sleep 3600
docker run -d --name admin-pc    --network admin    alpine sleep 3600
```

### Paso 2.3: Verificar asignación en cada subred

**Verifica** qué IP le tocó a cada contenedor:

```bash
docker inspect -f '{{.Name}}: IP={{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}} Red={{range .NetworkSettings.Networks}}{{.NetworkID}}{{end}}' web-front api-backend db-main admin-pc

docker network inspect frontend --format '{{range .Containers}}{{.IPv4Address}}{{end}}'
docker network inspect backend  --format '{{range .Containers}}{{.IPv4Address}}{{end}}'
```

**Pregunta 4**: Completa la tabla con lo que observaste:

| Contenedor | Subred | IP asignada | Gateway |
|------------|--------|-------------|---------|
| web-front | 192.168.60.0/27 | | |
| api-backend | 192.168.60.32/27 | | |
| db-main | 192.168.60.64/28 | | |
| admin-pc | 192.168.60.80/29 | | |

**Pregunta 5**: ¿Por qué es necesario usar una subred `/30` para el enlace
entre dos routers? ¿Concuerdas con el uso eficiente de direcciones?

## Entregable de la sesión

Sube a la tarea:

1. Tabla de tu equipo: IP, máscara, gateway y red (Pregunta 1).
2. Captura de las IPs asignadas a `srv1` y `srv2` (Paso 1.2).
3. Captura de la salida de `ipcalc` (Paso 1.3).
4. Evidencia de las subredes creadas: `docker network ls` y las IPs del
   Paso 2.3 con `frontend`, `backend`, `dbsub`, `admin` y `linknet`.
5. Tabla de asignación de los 4 contenedores completada (Pregunta 4).
6. Respuestas a las **5 preguntas** de la sesión.

## Rúbrica de la sesión

| Criterio | Puntos |
|----------|--------|
| Direccionamiento IP básico (Parte 1: IP, máscara, gateway, ipcalc) | 15 |
| Subneteo VLSM y subredes reales en Docker (Parte 2) | 20 |
| Respuestas a las preguntas 1–5 | 15 |
| **Total** | **50** |