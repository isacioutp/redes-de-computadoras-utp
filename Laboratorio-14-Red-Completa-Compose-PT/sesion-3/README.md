# Sesión 3 — archivos Docker

Archivos que necesita la **Sesión 3** (orquestación con Compose). Guía:
[../SESION-3.md](../SESION-3.md).

| Archivo | Para qué |
|---------|----------|
| `docker-compose.yml` | **Punto de partida:** el stack segmentado (front/back + DNS). |
| `dnsmasq.conf` | Zonas DNS internas. |
| `api/` | Código y `Dockerfile` de la API (Flask). |
| `db_pass.txt` | El valor que se montará como **secreto** (`secrets:` → `/run/secrets/db_pass`). |

## Uso

Esta sesión **reescribe** el `docker-compose.yml` para dejarlo orquestado
(healthchecks, `depends_on` con `condition`, `secrets`, `restart`). El resultado
final está en [../sesion-4/docker-compose.yml](../sesion-4/docker-compose.yml)
como referencia.

```bash
# 1. Punto de partida
docker compose up -d

# 2. Reescribe docker-compose.yml (ver SESION-3.md, Paso 1) y arranca:
docker compose up -d --wait
docker compose ps                       # web y db deben decir (healthy)

# 3. Escala la API (réplicas + balanceo por DNS de Docker)
docker compose up -d --scale api=2
docker compose exec web nslookup api.    # devuelve 2+ direcciones
```

> La carpeta `sesion-4/` contiene el resultado ya orquestado de esta sesión;
> úsala para comparar, no para saltarte los pasos.
