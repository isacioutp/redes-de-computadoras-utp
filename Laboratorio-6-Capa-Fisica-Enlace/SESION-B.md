# Laboratorio N.° 6 — Capa Física y Capa de Enlace de Datos · Sesión B: El switch, el aislamiento y la salida a internet

Semana 8 · Clase 2 · El switch, el aislamiento y la salida a internet

Cubre: Parte 3 (Aislamiento — dominios de colisión/broadcast), Parte 5 (El host Docker como router), Actividad de refuerzo de Wireshark y preguntas de verificación del guion original. Preguntas originales 7, 8, 11, 12 y preguntas de verificación 1, 2, 3.

## Objetivo de la sesión

Comprobar que cada red Docker es un **dominio de colisión/broadcast separado**
(qué aisla el switch y por qué se necesita la capa 3 para salir de la red),
para luego seguir el camino real del tráfico hacia internet a través del host y
confirmar lo observado con Wireshark.

## Retoma la sesión A

Esta sesión reutiliza `c1`, `c2`, `c3` y la red `lab6-red` de la Sesión A.
**Verifica** que siguen corriendo:

```bash
docker ps
docker network ls
```

Si no existieran, vuelve a ejecutar el Paso 1.2 de la Sesión A para recrear la
red y los tres contenedores antes de continuar.

## Parte 3: Aislamiento — cada red es un dominio de colisión/broadcast separado

### Paso 3.1: Redes diferentes NO se ven

**Construye** una segunda red, levanta `c4` en ella y **prueba** la
comunicación entre redes:

```bash
# Crear segunda red
docker network create lab6-red2

# Levantar c4 en la red 2
docker run -d --name c4 --network lab6-red2 alpine sleep 3600

# Intentar comunicar c1 (red1) con c4 (red2)
docker exec c1 ping -c 2 c4
```

**Pregunta 1**: ¿Funciona el ping? ¿Por qué la capa 2 (enlace) aísla las redes?
¿Qué dispositivo de capa 3 se necesitaría para comunicarlas? (Pista: lo verás
en el Laboratorio N.º 7.)

### Paso 3.2: Simular un switch creando un hub

Un **switch** aprende y filtra; un **hub** reenvía todo (flooding siempre).
Con tcpdump podemos ver que Docker aísla la difusión dentro de cada red.
**Observa** el dominio de broadcast:

```bash
# Listo: c4 está en otra red
docker exec c2 tcpdump -i eth0 -nn ether broadcast
# Desde c1 hacer un ping a c2 -> c3 (que tambien esta en red1) no esta en broadcast capturado de c2
docker exec c1 ping -c 1 c3
```

**Pregunta 2**: ¿c2 ve el broadcast de c1 aunque el ping iba hacia c3? ¿Qué
significa que c2 esté en el mismo dominio de colisión/broadcast que c1?

## Parte 5: Aplicación práctica — Internet desde adentro

### Paso 5.1: El host Docker como router (enlace → red)

Cuando los contenedores salen a internet, el tráfico pasa:

```
Container (MAC c1) ──bridge──> docker0 ──NAT──> host NIC (MAC real) ──> router
     Capa 2                                        Capa 2
```

**Sigue** la ruta de salida del contenedor y **observa** qué MAC actúa como
destino:

```bash
# Ver la ruta de salida del contenedor
docker exec c1 sh -c "ip route"
docker exec c1 sh -c "cat /etc/resolv.conf"

# ping al gateway del bridge
docker exec c1 ping -c 2 172.18.0.1

# salir a internet
docker exec c1 ping -c 2 google.com
```

**Pregunta 3**: ¿Qué MAC aparece como "destino" cuando el contenedor se
comunica con internet? ¿Es la del router real o la del gateway de Docker?
¿Por qué?

## Actividad de refuerzo — trama de Wireshark

**Captura** y **desglosa** las tramas de capa 2 con Wireshark:

1. En el host, abre **Wireshark** seleccionando la interfaz `docker0` o
   `br-xxxx`.
2. Genera tráfico:`docker exec c1 ping -c 2 c2`.
3. Filtra `arp` y observa la trama:
   - ¿Cuál es la dirección MAC destino? (`ff:ff:ff:ff:ff:ff` en el ARP request)
   - ¿Cuál es la dirección IP origen y destino dentro del ARP?
4. Filtra `icmp` y desglosa la trama:
   - Capa 2: MAC destino = MAC de c2.
   - Capa 3: IP destino = IP de c2.
   - Capa 4: protocolo ICMP (capa de red, sin transporte).

**Pregunta 4**: La trama ICMP ¿tiene puertos origen/destino de TCP/UDP?
¿Y el ARP? ¿Qué capa del modelo OSI les corresponde entonces?

## Preguntas de verificación

**Documenta** tus conclusiones de toda la semana:

**Pregunta 5**: ¿Cuál es la diferencia entre una dirección **MAC** y una
dirección **IP**?

**Pregunta 6**: ¿Por qué el switch mantiene una tabla de aprendizaje MAC→puerto?
¿Qué sucede si no encuentra la MAC destino?

**Pregunta 7**: ¿Qué protocolo traduce IP→MAC y en qué capa se encuentra?

## Entregable de la sesión

Sube a la tarea:

1. Captura del ping fallido entre `c1` y `c4` (Paso 3.1).
2. Captura del broadcast capturado por `c2` (Paso 3.2).
3. Capturas del Paso 5.1: `ip route`, ping al gateway y ping a `google.com`.
4. Captura o análisis de Wireshark: trama ARP e trama ICMP.
5. Respuestas a las **7 preguntas** de la sesión.
6. Tabla resumen: MAC, IP, red y puerta de enlace de `c1`, `c2`, `c3` y `c4`
   (completa la iniciada en la Sesión A).
7. Conclusión (3-5 líneas) sobre cómo la capa 2 logra reenviar una trama en
   una LAN y qué necesita para salir de ella.

## Rúbrica de la sesión

| Criterio | Puntos |
|----------|--------|
| Aislamiento y dominios de colisión/broadcast (Parte 3) | 20 |
| Router host y direcciones de salida a internet (Parte 5) | 15 |
| Wireshark + preguntas de verificación | 15 |
| **Total** | **50** |