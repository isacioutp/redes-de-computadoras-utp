# Laboratorio N.° 12 — Orquestación de Servicios y Despliegue de Aplicaciones

Semana 11 · Unidad III · 2 clases

- **Clase 1:** Compose y Swarm: réplicas y balanceo → [Sesión A](SESION-A.md)
- **Clase 2:** Secretos, overlay, actualizaciones y stack → [Sesión B](SESION-B.md)

## Objetivo general

Comprender qué es la **orquestación de servicios**, compararla entre
**máquinas virtuales**, **nube** y **contenedores**, y desplegar una
aplicación multi-servicio con **Docker Compose** y **Docker Swarm**
(servicios, réplicas, balanceo, secretos y actualizaciones continuas).

Este es el **laboratorio final de la unidad**: conecta todas las nociones de
red tridimensionales (LAN, DNS, SSH, monitoreo) con la operación real de un
stack de software.

## Contexto teórico

### ¿Qué es orquestar?

Ejecutar **una** app con **un** contenedor es fácil. La complejidad crece
cuando tienes varios servicios (web + api + db + cache + worker), necesitas
**réplicas**, **actualizaciones**, **secretos** y **redes** entre ellos. La
orquestación automatiza: despliegue, escalado, descubrimiento de servicios,
balanceo de carga, auto-curación y secretos.

| Herramienta | Modelo | Ejemplos |
|-------------|--------|----------|
| Orchestrator de VMs | Máquina virtual | VMware vCenter, Proxmox |
| Cloud orchestration | Infraestructura como servicio | AWS EC2/ECS, Azure, GCP |
| Container orchestration | Contenedores | Docker Compose, Docker Swarm, Kubernetes |

### Docker Compose vs Docker Swarm

| | Docker Compose | Docker Swarm |
|--|----------------|---------------|
| Alcance | Un solo host (dev/pruebas) | Múltiples nodos (cluster) |
| Réplicas | `scale` | `docker service scale` |
| Redes | Bridge por proyecto | **Overlay** entre nodos |
| Alta disponibilidad | No | Sí (rol manager/worker) |
| Balanceo | No (por capacidades) | Sí (ingress mesh) |
| Uso típico | Desarrollo local | Producción simple / on-prem |

## Materiales

- Docker Engine (debe incluir `docker compose` y `docker swarm`).
- Configuraciones copiadas de los Labs N.º 8 y 10.

## Cómo se trabaja esta semana

| Sesión | Qué haces | Entregable breve | Guía |
|--------|-----------|------------------|------|
| **Sesión A — Compose y Swarm: réplicas y balanceo** | Stack Compose web/api/db/redis con `scale api=3` y `getent` (Parte 1) e inicialización del Swarm con el servicio `web-mesh` replicado y su routing mesh (Parte 2). Preguntas 1–6. | `compose.yml`, `docker service ls` con réplicas, `curl` al mesh. | [Sesión A](SESION-A.md) |
| **Sesión B — Secretos, overlay, actualizaciones y stack** | Secretos en `/run/secrets` (Parte 3), red overlay + rolling update/rollback (Parte 4), `stack deploy` (Parte 5), tabla comparativa de orquestación (Parte 6) y práctica integradora del proyecto (Parte 7). Preguntas del original 7–15 (renumeradas 1–9). | Secreto montado en `/run/secrets`, evidencia de update/rollback, `stack.yml` desplegado, tabla comparativa, reflexión integradora. | [Sesión B](SESION-B.md) |

## Rúbrica global

100 puntos (Sesión A 50 + Sesión B 50).

| Sesión | Criterio | Puntos |
|--------|----------|--------|
| A | Stack Compose (web/api/db/redis) funcionando | 15 |
| A | `scale api=3` + `getent hosts api` | 10 |
| A | Swarm init + servicio `web-mesh` (3 réplicas) con routing mesh | 15 |
| A | Preguntas 1–6 | 10 |
| B | Secretos montados en `/run/secrets` | 10 |
| B | Red overlay + rolling update/rollback | 10 |
| B | `stack deploy` de `stack.yml` | 10 |
| B | Tabla comparativa de orquestación | 5 |
| B | Reflexión integradora (práctica del proyecto) | 5 |
| B | Preguntas 7–15 (renumeradas 1–9) | 10 |
| | **Total** | **100** |

## Limpieza

Al terminar la semana, elimina los recursos:

```bash
docker service rm web-mesh db-swarm api-overlay 2>/dev/null
docker stack rm appfinal 2>/dev/null
docker secret rm db_pass db_user 2>/dev/null
docker compose down --remove-orphans -v
docker swarm leave --force
```