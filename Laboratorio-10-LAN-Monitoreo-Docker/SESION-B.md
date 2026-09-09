# Laboratorio N.° 10 — Implementación de una LAN y Herramientas de Monitoreo · Sesión B: Enrutamiento entre subredes y monitoreo

Semana 12 · Clase 2

Cubre las **Partes 3, 4 y 5** del laboratorio original: enrutamiento explícito
entre subredes, herramientas de monitoreo (`tcpdump`, `iftop`, `iperf3`,
`netdata`) e integración del escenario completo con diagrama de flujo y
propuesta de diseño.

## Objetivo de la sesión

Enrutar la LAN entre subredes de forma explícita (con tablas de ruta) y luego
monitorear y medir el tráfico real con herramientas de producción. Al final
integras todo el stack de la Sesión A y propones el esquema para una app de
inventarios usando las piezas que ya construiste.

## Pasos

### Paso 1: Prueba la conectividad NAT natural del host

Observa qué peticiones funcionan y cuáles no entre subredes:

```bash
docker exec app-srv curl -s http://web-srv/ 2>/dev/null | head -1        # web-srv alcanzable?
docker exec web-srv ping -c 2 app-srv   # web-srv intentando alcanzar app-srv
```

### Paso 2: Agrega el enrutamiento explícito con tablas

Haz explícito lo que Docker ya entrega con red y gateway: agrega la ruta al
final de la red interna vía el router y verifica con ping:

```bash
# Ruta al final de la red interna vía el router
docker exec web-srv ip route add 10.0.1.0/24 via 10.0.0.2 2>/dev/null
docker exec web-srv ping -c 2 10.0.1.2
```

### Paso 3: Captura tráfico en vivo con tcpdump

Instala `tcpdump` en `web-srv`, captura en la Terminal A y genera tráfico en la
Terminal B:

```bash
docker exec web-srv sh -c "apk add --no-cache tcpdump -q"

# Terminal A: capturar en web-srv
docker exec web-srv tcpdump -i eth0 -nn -c 15 any port 80 or icmp
# Terminal B: generar tráfico
for i in 1 2 3 4; do curl -s http://localhost:8080/ >/dev/null; done
docker exec web-srv ping -c 3 10.0.0.1
```

> **Checkpoint:** guarda la salida de `tcpdump`; ahí se ven los flujos TCP
> (puerto 80) e ICMP que analiza la Pregunta 3.

### Paso 4: Mide el ancho de banda en tiempo real con iftop

Instala `iftop` y ejecútalo 10 segundos mientras otra terminal genera carga:

```bash
docker exec web-srv sh -c "apk add --no-cache iftop -q"
# Terminal A (interactiva, 10s):
docker exec -it web-srv iftop -t -s 10 -n -N
# Terminal B: generar carga
ab -n 2000 -c 50 http://localhost:80/ 2>/dev/null || \
curl -s http://localhost:8080/ >/dev/null
```

### Paso 5: Mide ancho de banda entre extremos con iperf3

Levanta el servidor de prueba en la red interna y ejecuta un cliente TCP y otro
UDP:

```bash
# Servidor iperf (escucha en la red interna)
docker run -d --name iperf-srv --network interna -p 5201:5201 mlabbe/iperf3 -s

# Cliente iperf desde host
docker run --rm --network interna mlabbe/iperf3 -c iperf-srv -t 5
docker run --rm --network interna mlabbe/iperf3 -c iperf-srv -t 5 -u -b 100M
```

### Paso 6: Abre el panel web de netdata

Dimensiona el contenedor de monitoreo y abre el panel en el navegador:

```bash
# Dimensionar el contenedor (necesario en algunos kernels)
docker run -d --name monit \
  --network interna -p 19999:19999 \
  --cap-add SYS_PTRACE -v /proc:/host/proc:ro \
  -v /sys:/host/sys:ro \
  netdata/netdata:latest
```

Abre `http://localhost:19999` y revisa los paneles de **TCP**, **UDP**,
**interfaces** y **procesos**. Genera tráfico (ab o iperf) y observa las
gráficas actualizarse.

### Paso 7: Integra el escenario completo

Lanza el stack completo y verifica el flujo completo:

```bash
# ¿La aplicación alcanza web y db?
docker exec app-srv curl -s http://localhost:5000/
docker exec app-srv curl -s http://localhost:5000/web
docker exec app-srv curl -s http://localhost:5000/db
```

> **Checkpoint:** la aplicación de la Sesión A debe responder `/`, `/web` y
> `/db`; esa es la evidencia de que la LAN completa funciona.

## Preguntas de la sesión

1. ¿Qué peticiones funcionan (app→web) y cuáles no (web→app)? Piensa en el DNS
   interno y en si ambos contenedores comparten red.
2. ¿Qué tabla de enrutamiento muestra `docker exec web-srv ip route`? ¿Qué rol
   cumplen las rutas para que el paquete regrese (ruta de vuelta)?
3. ¿Qué protocolos y puertos ves en la captura de `tcpdump`? Clasifica cada
   flujo por capa: transporte (TCP/UDP), red (ICMP), aplicación.
4. ¿Cuál es el par IP:puerto con más tráfico durante la prueba de `iftop`? ¿Qué
   ancho de banda máximo observaste (Mbps)?
5. Compara los resultados de `iperf3` en modo TCP y UDP. ¿Qué significa el
   `jitter` en UDP? ¿Qué utilidad tiene para una videollamada?
6. En el panel de TCP de `netdata`: ¿qué gráfica muestra la tasa de
   segmentos/paquetes? ¿Cómo te ayudaría esta herramienta a detectar una fuga
   de memoria o un DDoS en tu app?
7. Completa el diagrama del flujo de una petición:

   ```
   Usuario ──:8080──> ?(?):8080 ──DNS──> ? ──:5000──> app-srv ──> web-srv
                                                 └─────> db-srv
   ```

8. **Pregunta de diseño**: tu grupo de desarrollo despliega una app de
   inventarios. Propón el esquema (subredes, servicios, qué monitorearías) SIN
   necesidad de resolver el proyecto completo — solo las piezas de esta LAN:
   webserver, API, DB, monitoreo. ¿Qué herramienta de monitoreo elegirías de
   las vistas y por qué?

## Entregable de la sesión

1. Captura de `tcpdump` (Paso 3) y de `iftop` (Paso 4).
2. Resultados de `iperf3` TCP y UDP con la interpretación (`jitter` en UDP).
3. Captura de pantalla del panel web de `netdata` con alguna gráfica.
4. Evidencia del flujo app→web y app→db funcionando (Paso 7).
5. Diagrama de tu LAN propuesta (Pregunta 8) y respuestas a las preguntas 1–8.

## Rúbrica de la sesión (50 puntos)

| Criterio | Puntos |
|----------|--------|
| Enrutamiento entre subredes (rutas explícitas) | 10 |
| Evidencias de `tcpdump` + `iftop` | 15 |
| Resultados `iperf3` TCP/UDP con interpretación | 10 |
| `netdata` funcionando | 10 |
| Preguntas 1–8 + diagrama de LAN propuesta | 5 |
| **Total** | **50** |