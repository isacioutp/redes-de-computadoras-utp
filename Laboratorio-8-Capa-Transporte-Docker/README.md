# Laboratorio N.° 8 — Capa de Transporte con Docker

Semana 10 · Unidad II · 2 clases

**Sesión A:** TCP vs UDP — sockets, handshake y puertos
**Sesión B:** Puertos, congestión y arquitectura de microservicios

## Objetivo general

Comprender el funcionamiento de la **capa de transporte** (TCP y UDP) a través
de Docker, observando cómo los contenedores se comunican mediante puertos,
segmentación de datos y control de flujo. Los estudiantes aprenderán a
orquestar aplicaciones de red y analizar el tráfico entre contenedores.

## Contexto teórico

### Capa de Transporte

La capa de transporte proporciona comunicación extremo a extremo entre
aplicaciones. Sus protocolos principales son:

| Característica | TCP | UDP |
|----------------|-----|-----|
| Conexión | Orientado a conexión (handshake 3 vías) | Sin conexión |
| Confiable | Sí (retransmite paquetes perdidos) | No (best-effort) |
| Orden | Garantiza orden de llegada | No garantiza orden |
| Velocidad | Mayor latencia (overhead) | Menor latencia |
| Uso típico | HTTP, SSH, FTP, bases de datos | DNS, streaming, VoIP, juegos |

### TCP: El Three-Way Handshake

```
Cliente                    Servidor
   │                          │
   │──── SYN ────────────────>│  1. Cliente solicita conexión
   │<─── SYN-ACK ─────────────│  2. Servidor confirma
   │──── ACK ────────────────>│  3. Cliente confirma
   │                          │
   │    Conexión establecida  │
```

### Puertos y Segmentación

- **Puertos**: Identifican aplicaciones (0-65535)
  - Puertos bien conocidos: 0-1023 (HTTP=80, HTTPS=443, SSH=22)
  - Puertos registrados: 1024-49151
  - Puertos dinámicos: 49152-65535
- **Segmentación**: TCP divide los datos en segmentos, cada uno con número de secuencia

### Docker y la Capa de Transporte

Docker utiliza la capa de transporte para:
- **Port mapping**: `docker run -p 8080:80` mapea puertos del host al contenedor
- **Container networking**: contenedores en la misma red se comunican vía IPs internas
- **DNS interno**: Docker resuelve nombres de servicio a IPs de contenedor

## Materiales

- Computadora con Docker Desktop instalado (Windows/Mac) o Docker Engine (Linux)
- Conexión a internet (para descargar imágenes)
- Wireshark (opcional, para análisis de tráfico)

## Requisitos previos

```bash
# Verificar instalación de Docker
docker --version
docker-compose --version

# Verificar que Docker está corriendo
docker ps
```

---

## Cómo se trabaja esta semana

| Sesión | Qué harás | Entregable |
|--------|-----------|------------|
| **Sesión A — TCP vs UDP: sockets, handshake y puertos** | Construirás una red Docker, escribirás un servidor TCP (Flask) y su cliente, capturarás con tcpdump el handshake `SYN / SYN-ACK / ACK`, y compararás el comportamiento con un servidor UDP. | Captura del handshake, tabla comparativa TCP vs UDP con evidencia y respuestas a 5 preguntas. — [Sesión A](SESION-A.md) |
| **Sesión B — Puertos, congestión y arquitectura de microservicios** | Mapearás puertos al host, inspeccionarás `netstat` e `iptables` (regla DOCKER), simularás latencia y pérdida con `tc netem` y definirás una arquitectura de microservicios (gateway, APIs, cola UDP) con docker-compose. | Capturas de mapeo y de netem, diagrama de arquitectura de microservicios y respuestas a 6 preguntas. — [Sesión B](SESION-B.md) |

## Rúbrica global

| Sesión | Puntos |
|--------|--------|
| Sesión A — TCP vs UDP: sockets, handshake y puertos | 50 |
| Sesión B — Puertos, congestión y arquitectura de microservicios | 50 |
| **Total** | **100** |

## Limpieza

Ejecuta estos comandos al terminar la **Sesión B**, cuando ya no necesites los
servicios:

```bash
# Eliminar contenedores y la red de trabajo
docker rm -f servidor-web servidor-1 servidor-2 servidor-3 servidor-4 udp-server 2>/dev/null || true
docker network rm laboratorio-red 2>/dev/null || true

# Eliminar las imágenes construidas en las dos sesiones
docker rmi servidor-tcp servidor-udp 2>/dev/null || true

# Opcional: eliminar el directorio de trabajo
rm -rf ~/laboratorio-transporte
```

## Recursos adicionales

- [Docker Documentation - Networking](https://docs.docker.com/engine/reference/commandline/network/)
- [TCP/IP Illustrated, Vol. 1 - W. Richard Stevens](https://www.oreilly.com/library/view/tcpip-illustrated-volume/9780132808231/)
- [Wireshark Display Filters](https://wiki.wireshark.org/DisplayFilters)