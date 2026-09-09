# Laboratorio N.° 10 — Implementación de una LAN y Herramientas de Monitoreo

Semana 12 · Unidad III · 2 clases

- **Clase 1:** Construir la LAN corporativa → [Sesión A](SESION-A.md)
- **Clase 2:** Enrutamiento entre subredes y monitoreo → [Sesión B](SESION-B.md)

## Objetivo general

Implementar una red de área local (LAN) completa con **Docker** como si fuera
una oficina de desarrollo: segmentada en subredes, con DNS interno, enrutador
propio, NAT y servicios. Luego monitorear el tráfico con herramientas reales
(`tcpdump`, `iftop`, `iperf3`, `netdata`) para medir ancho de banda, latencia
y paquetes.

Al terminar, tendrás las bases para el **Proyecto Semestral** (sin tener la
solución única, sino la metodología).

## Contexto teórico

Una LAN moderna (oficina/Data Center) necesita:

- **Segmentación** en subredes (VLADNet / VLANs → en Docker: redes bridge).
- **DHCP** para asignar IPs (visto en Lab N.º 7).
- **DNS** interno para resolver nombres (visto en Lab N.º 9).
- **Enrutamiento** entre subredes + salida a internet (NAT).
- **Monitoreo**: conocer ancho de banda, latencia, errores y uso.

Docker cubre casi todo el "switch + router + DNS" con sus *bridges* integrados.
Aquí lo haremos **explícito**: un contenedor hará de router y otro de servidor
DNS, igual que harías en una oficina.

### Arquitectura de la LAN de la semana

```
                  ┌───────────────────────────────┐
                  │        INTERNET (host)        │
                  └──────────────┬────────────────┘
                                 │ NAT + router del host
                  ┌──────────────▼────────────────┐
                  │        router-corp (contenedor)│  dual-homed
                  └──┬───────────────────────┬─────┘
              redPública(10.0.0.0/24)   redInterna(10.0.1.0/24)
                     │                       │
          ┌──────────▼──────┐    ┌───────────▼──────────┐
          │ web-srv (nginx) │    │ app-srv (flask)      │
          │ db-srv (postgres)│   │ monit (netdata)      │
          └─────────────────┘    └──────────────────────┘
```

## Materiales

- Docker Engine (verificado con `docker ps`).
- Host Linux recomendado (para `ip`, `iptables` y `netdata` por puerto).

## Cómo se trabaja esta semana

| Sesión | Qué haces | Entregable breve | Guía |
|--------|-----------|------------------|------|
| **Sesión A — Construir la LAN corporativa** | Diseño de la LAN: subredes `publica`/`interna`, router `router-corp` dual-homed (Parte 1) y servicios web nginx, db postgres, app flask y DNS interno dnsmasq (Parte 2). Preguntas 1–3. | `docker network ls`, captura de `router-corp` con 2 interfaces, `nslookup web.local/app.local` funcionando. | [Sesión A](SESION-A.md) |
| **Sesión B — Enrutamiento entre subredes y monitoreo** | Enrutamiento explícito con tablas (Parte 3), monitoreo con `tcpdump`, `iftop`, `iperf3`, `netdata` (Parte 4) e integración con diagrama de flujo y propuesta de diseño (Parte 5). Preguntas del original 3–10 (renumeradas 1–8). | Capturas de `tcpdump`/`iftop`, resultados `iperf3` TCP/UDP, captura de `netdata`, diagrama de la LAN propuesta. | [Sesión B](SESION-B.md) |

## Rúbrica global

100 puntos (Sesión A 50 + Sesión B 50).

| Sesión | Criterio | Puntos |
|--------|----------|--------|
| A | Redes `publica`/`interna` creadas (`docker network ls`) | 10 |
| A | `router-corp` dual-homed con 2 interfaces | 10 |
| A | Servicios `web-srv`, `db-srv`, `app-srv` funcionando | 10 |
| A | DNS interno (`nslookup web.local` y `app.local`) | 10 |
| A | Preguntas 1–3 | 10 |
| B | Enrutamiento entre subredes (rutas explícitas) | 10 |
| B | Evidencias de `tcpdump` + `iftop` | 15 |
| B | Resultados `iperf3` TCP/UDP con interpretación | 10 |
| B | `netdata` funcionando | 10 |
| B | Preguntas 1–8 + diagrama de LAN propuesta | 5 |
| | **Total** | **100** |

## Limpieza

Al terminar la semana, elimina los recursos:

```bash
docker rm -f router-corp web-srv db-srv app-srv dns-corp iperf-srv monit
docker network rm publica interna
```