# Laboratorio N.° 8 — Capa de Transporte con Docker · Sesión B: Puertos, congestión y arquitectura de microservicios

Semana 8 · Clase 2

Cubre las **Partes 3, 6 y 7** del laboratorio original: port mapping hacia el
host con `netstat`/`iptables`, simulación de latencia y pérdida con
`tc netem`, y el escenario final de microservicios con `docker-compose`. Las
Partes 4 y 5 (compose multi-servicio y análisis con Wireshark) se omiten porque
Docker Compose se trabaja a fondo en el **Laboratorio N.° 12**.

> **Antes de empezar** verifica que conservas de la **Sesión A** la imagen
> `servidor-tcp` y el contenedor `servidor-web`:
>
> ```bash
> docker images | grep servidor-tcp
> docker ps | grep servidor-web
> ```

## Objetivo de la sesión

Vas a exponer servicios hacia el host por puertos, a observar cómo Docker
erige sus reglas de NAT en iptables, a degradar la red de un contenedor con
latencia y pérdida artificiales (`tc netem`) para ver cómo reacciona TCP, y a
definir la arquitectura de un sistema de microservicios (gateway público, APIs
internas y una cola UDP en una red aislada).

---

## Paso 1. Mapea puertos del host a múltiples contenedores

```bash
# Ejecutar servidor en múltiples puertos
docker run -d --name servidor-1 -p 8081:5000 --network laboratorio-red servidor-tcp
docker run -d --name servidor-2 -p 8082:5000 --network laboratorio-red servidor-tcp
docker run -d --name servidor-3 -p 8083:5000 --network laboratorio-red servidor-tcp

# Verificar mapeo
docker port servidor-1
docker port servidor-2
docker port servidor-3

# Probar cada servidor desde el host
curl http://localhost:8081/
curl http://localhost:8082/
curl http://localhost:8083/
```

**Pregunta 1**: ¿Qué sucede si intentas ejecutar otro contenedor mapeado al puerto 8081?

> **Hazlo**: compruébalo en vivo. Lanza `docker run -d --name servidor-4 -p
> 8081:5000 --network laboratorio-red servidor-tcp` y documenta el error de
> Docker (conflicto de puerto). Luego elimínalo si quedó creado:
> `docker rm -f servidor-4`.

## Paso 2. Expón servicios y observa la regla DOCKER de iptables

```bash
# Verificar puertos en escucha
netstat -tlnp | grep -E '808[1-3]'

# Inspeccionar las reglas de iptables de Docker
sudo iptables -t nat -L DOCKER -n
```

**Pregunta 2**: ¿Cómo resuelve Docker el tráfico cuando múltiples contenedores mapean al mismo puerto del host?

## Paso 3. Simula latencia con `tc netem`

`tc netem` (emulador de red) añade retardos y pérdidas al tráfico que sale por
la interfaz `eth0`. El comando del original operaba sobre el stack compose
(omitido); aquí se aplica directamente al contenedor `servidor-web` de la
Sesión A.

```bash
# Instalar herramientas de red dentro del contenedor
docker exec servidor-web apt-get update
docker exec servidor-web apt-get install -y iproute2

# Agregar 100ms de latencia al tráfico saliente
docker exec servidor-web tc qdisc add dev eth0 root netem delay 100ms

# Medir tiempo de respuesta (debe crecer ~100ms por trayecto)
time curl http://localhost:8080/

# Remover latencia
docker exec servidor-web tc qdisc del dev eth0 root
```

## Paso 4. Simula pérdida de paquetes con `tc netem`

```bash
# Agregar 10% de pérdida de paquetes
docker exec servidor-web tc qdisc add dev eth0 root netem loss 10%

# Hacer múltiples peticiones (observa si alguna falla o se ralentiza)
for i in {1..10}; do
  curl -s http://localhost:8080/ | python3 -m json.tool
done

# Remover pérdida
docker exec servidor-web tc qdisc del dev eth0 root
```

**Pregunta 3**: ¿Cómo reacciona TCP ante la pérdida de paquetes? ¿Y UDP?

**Pregunta 4**: ¿Por qué es importante el control de congestión en redes reales?

## Paso 5. Define la arquitectura de microservicios

```bash
cd ~/laboratorio-transporte

# Crear estructura de proyecto
mkdir -p microservicios/{gateway,user-service,order-service}

# Crear docker-compose.yml completo
cat > microservicios/docker-compose.yml << 'YAML'
version: '3.8'

services:
  # API Gateway - expone puerto 80
  gateway:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - public
    depends_on:
      - user-api
      - order-api

  # Servicio de usuarios
  user-api:
    build: ./user-service
    networks:
      - public
      - internal
    expose:
      - "3001"  # Solo accesible desde otras redes Docker

  # Servicio de pedidos
  order-api:
    build: ./order-service
    networks:
      - public
      - internal
    expose:
      - "3002"

  # Cola de mensajes UDP
  message-queue:
    build: .
    networks:
      - internal
    expose:
      - "9000/udp"

networks:
  public:
    driver: bridge
  internal:
    driver: bridge
    internal: true  # Sin acceso a internet
YAML
```

**Pregunta 5**: ¿Cuál es la diferencia entre `ports`, `expose` y `networks` en docker-compose?

**Pregunta 6**: ¿Por qué se crea una red `internal: true`? ¿Qué casos de uso tiene?

## Paso 6. Valida la arquitectura

```bash
# El despliegue completo con Compose se trabaja en el Lab N.° 12.
# Aquí validas que la definición de la arquitectura es correcta:
cd ~/laboratorio-transporte/microservicios
docker-compose config -q && echo "compose valido"

# Dibuja (a mano o con la herramienta que prefieras) el diagrama:
#   Host ->[puerto 80] gateway -> user-api:3001 / order-api:3002 (red public)
#                                     \-> message-queue:9000/udp (red internal)
```

---

## Entregable de la sesión

1. **Capturas de pantalla** del mapeo de puertos (`docker port` + `curl` a los tres puertos) y de la salida de `netstat` e `iptables`.
2. **Evidencia** del experimento de congestión: salida de `time curl` con 100 ms de latencia y de las 10 peticiones con 10 % de pérdida.
3. **Diagrama de arquitectura** del sistema de microservicios indicando puertos, protocolos y redes (público vs interna).
4. **Respuestas** a las preguntas 1 a 6.

## Rúbrica de la sesión

| Criterio | Puntos |
|----------|--------|
| Mapeo de puertos (8081-8083) y verificación con netstat/iptables | 12 |
| Simulación de latencia y pérdida con `tc netem` (aplicar, medir, remover) | 10 |
| Arquitectura de microservicios: estructura, compose y diagrama | 12 |
| Evidencias y capturas | 6 |
| Respuestas a las preguntas 1-6 (análisis y comprensión) | 10 |
| **Total** | **50** |