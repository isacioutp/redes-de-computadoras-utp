# Laboratorio N.° 6 — Capa Física y Capa de Enlace de Datos · Sesión A: De los bits a la trama Ethernet

Semana 8 · Clase 1 · De los bits a la trama Ethernet

Cubre: Parte 1 (Direcciones MAC en contenedores), Parte 2 (Tramas Ethernet con tcpdump) y Parte 4 (Capa física: latencia y CSMA/CD) del guion original. Preguntas originales 1, 2, 3, 4, 5, 6, 9 y 10.

## Objetivo de la sesión

Construir una red local con contenedores Docker y capturar en vivo las tramas
Ethernet (capa 2) que la cruzan, identificando **MAC origen/destino**,
**EtherType** y el papel de **ARP**; luego experimentar con la capa física
(latencia y método de acceso al medio).

## Hazlo

Vas a **construir**, **observar**, **capturar**, **medir** y **documentar**
todo lo que pase en la terminal. Cada evidencia que generes alimenta tu
entregable.

## Parte 1: Direcciones MAC en contenedores

### Paso 1.1: Ver las interfaces de red del sistema

**Observa** las interfaces del host. Desde el host:

```bash
# Ver las interfaces de red del host (capa 2)
ip link

# Ver las direcciones MAC de cada interfaz
cat /sys/class/net/*/address

# En Windows (PowerShell):
# getmac /v
```

**Pregunta 1**: ¿Cuántas interfaces tiene tu equipo? ¿Qué MAC tiene la interfaz
de red principal? ¿En qué formato viene escrita?

### Paso 1.2: las MAC que Docker crea

**Construye** una red y tres contenedores, y luego **observa** las MAC que
Docker asigna:

```bash
# Crear red y levantar un contenedor
docker network create lab6-red

docker run -d --name c1 --network lab6-red alpine sleep 3600
docker run -d --name c2 --network lab6-red alpine sleep 3600
docker run -d --name c3 --network lab6-red alpine sleep 3600

# Ver las MAC de cada contenedor
docker inspect -f '{{.Name}} → {{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' c1
docker inspect -f '{{.Name}} → {{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' c2
docker inspect -f '{{.Name}} → {{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' c3
```

> Nota: si la MAC sale vacía, puede también verse con el comando `ip link`
> dentro del contenedor:

```bash
docker exec c1 ip link
docker exec c1 cat /sys/class/net/eth0/address
```

**Pregunta 2**: ¿Qué prefijo de MAC usan todos los contenedores? ¿Crees que
identifica a Docker como "fabricante"? (Pista: busca `02:42:` en internet.)

### Paso 1.3: La tabla MAC del switch virtual de Docker

Docker usa un **bridge virtual** (`br-xxx`) que se comporta como un switch.
**Observa** su tabla de aprendizaje:

```bash
# Ver el "switch" bridge que Docker creó
ip link show type bridge

# Tabla de aprendizaje MAC del bridge (el corazón del switch)
bridge fdb show | grep -A1 lab6-red
```

**Pregunta 3**: ¿Tienes puerta de enlace (gateway) en el bridge de Docker? ¿Qué
MAC tiene el gateway de la red `lab6-red`?

## Parte 2: Tramas Ethernet — observación con tcpdump

### Paso 2.1: Capturar la trama

Instalamos `tcpdump` en un contenedor para ver las tramas en vivo. **Captura**
el intercambio ARP + ICMP de un ping:

```bash
docker exec c1 sh -c "apk add --no-cache tcpdump" 
docker exec c2 sh -c "apk add --no-cache tcpdump"

# Terminal A: capturar en c1
docker exec c1 tcpdump -i eth0 -nn

# Terminal B: ping de c1 a c2
docker exec c1 ping -c 3 c2
```

Observar la salida. Debe verse similar a:

```
11:22:33.44... ARP, Request who-has 172.18.0.3 tell 172.18.0.2, length 28
11:22:33.44... ARP, Reply 172.18.0.3 is-at 02:42:ac:12:00:03, length 28
11:22:33.44... IP 172.18.0.2 > 172.18.0.3: ICMP echo request, id 1, seq 1, length 64
11:22:33.44... IP 172.18.0.3 > 172.18.0.2: ICMP echo reply, id 1, seq 1, length 64
```

**Pregunta 4**: ¿Qué protocolo aparece ANTES que el ICMP? ¿Por qué es necesario
ese intercambio antes de poder enviar el ping?

### Paso 2.2: Ver la trama completa en hexadecimal

Docker crea un puente que se ve como un switch normal. Para ver la trama
Ethernet "de verdad" (con MAC origen/destino), usamos verbose. **Captura** la
trama y **analiza** su estructura:

```bash
docker exec c1 tcpdump -i eth0 -nn -XX src host 172.18.0.3
# en otra terminal
docker exec c1 ping -c 1 c2
```

Datos (comentar la estructura):

```
0x0000:  0242 ac12 0003 0242 ac12 0002 0800 4500  .B.._...B....E.
          ^MAC dst^  ^MAC src^ ^Etype  ^IPv4 header
```

**Pregunta 5**: Localiza en la salida `-XX` las **6+6 bytes de las MAC** y los
**2 bytes del EtherType** (`0800` = IPv4). ¿Coinciden con la MAC de `c2`
(destino) y `c1` (origen)?

### Paso 2.3: Broadcast y flooding

El ARP se envía a la dirección MAC de broadcast `ff:ff:ff:ff:ff:ff`. **Captura**
el broadcast:

```bash
docker exec c1 tcpdump -i eth0 -nn ether broadcast
# en otra terminal
docker exec c1 ping -c 1 c2
```

**Pregunta 6**: ¿Qué dirección MAC destino tienen los paquetes ARP Request?
¿Por qué no pueden enviarse directamente al destinatario si aún no se conoce
su MAC?

## Parte 4: Capa física — simulando medios y velocidad

### Paso 4.1: Latencia y velocidad del medio

**Mide** la latencia dentro del "medio" del bridge y luego **simula** un cable
más largo o un satélite:

```bash
# Crear contenedor con herramientas de red
docker run -d --name test-phys --network lab6-red -e PING_COUNT=10 alpine sleep 3600

# Medir latencia dentro del "medio" del bridge
docker exec test-phys ping -c 10 c1

# Límites de la velocidad de transmisión (rate), mts en mbit
docker exec test-phys sh -c "which tc || apk add --no-cache iproute2"

# Agregar latencia artificial (simula cable más largo / satélite)
docker exec test-phys tc qdisc add dev eth0 root netem delay 100ms
docker exec test-phys ping -c 3 c1

# Eliminar latencia
docker exec test-phys tc qdisc del dev eth0 root
```

| Medio | Velocidad típica | Latencia típica |
|-------|------------------|-----------------|
| Par trenzado (Cat6) | 1–10 Gbps | <0.5 ms/salto |
| Fibra óptica | 10–400 Gbps | ~1 ms/100km |
| Wi-Fi 6 | 1–9 Gbps | 2–10 ms |
| Satélite | 25–100 Mbps | 250-600 ms |

**Pregunta 7**: Compara las latencias de la tabla con la que mediste en el lab
¿cómo se relaciona la "velocidad" del medio con la latencia de la aplicación?

### Paso 4.2: Método de acceso al medio (CSMA/CD en Ethernet)

Ethernet usa **CSMA/CD**: escucha antes de transmitir y detecta colisiones.
Para observar "colisiones" simuladas — si bien en Docker los bridges modernos
son full-duplex — **genera** tráfico simultáneo:

```bash
# Generar tráfico simultáneo (varios contenedores a la vez)
for i in {1..5}; do
  docker exec test-phys ping -c 5 c1 > /dev/null &
done
wait

# Contar pérdidas con -f (flood) y observar que el host reporta paquetes
docker exec test-phys ping -c 20 -f c1
```

**Pregunta 8**: ¿Qué diferencia observaste entre CSMA/CD (en los medios
compartidos antiguos) y la conmutación full-duplex de los switches modernos?

## Entregable de la sesión

Sube a la tarea:

1. Captura de pantalla del Paso 1.2 con la red `lab6-red` creada, los
   contenedores `c1`, `c2`, `c3` corriendo y sus direcciones MAC.
2. Captura del tcpdump del Paso 2.1 mostrando **ARP + ICMP**.
3. Análisis de la salida `-XX` del Paso 2.2 marcando MAC destino, MAC origen
   y EtherType.
4. Respuestas a las **8 preguntas** de la sesión.
5. Tabla resumen: MAC, IP, red y puerta de enlace de `c1`, `c2` y `c3`.

## Rúbrica de la sesión

| Criterio | Puntos |
|----------|--------|
| Paso: creación de la red/contenedores y direcciones MAC (Parte 1) | 20 |
| Análisis de la trama `-XX` (MAC y EtherType) (Parte 2) | 15 |
| Capa física: latencia y CSMA/CD (Parte 4) | 15 |
| **Total** | **50** |