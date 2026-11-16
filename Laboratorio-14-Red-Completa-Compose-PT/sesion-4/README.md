# Sesión 4 — archivos Docker

Archivos que necesita la **Sesión 4** (integración, respaldo y demo). Guía:
[../SESION-4.md](../SESION-4.md).

| Archivo | Para qué |
|---------|----------|
| `docker-compose.yml` | El stack **ya orquestado** (healthchecks, secreto, `restart`). |
| `dnsmasq.conf` | Zonas DNS internas (`web.local`, `db.local`). |
| `api/` | Código y `Dockerfile` de la API (Flask). |
| `db_pass.txt` | Contraseña de Postgres montada como secreto (`/run/secrets/db_pass`). |

## Uso

```bash
# Reproducir todo desde cero
docker compose down -v --remove-orphans
docker compose up -d --wait
docker compose ps                       # todo (healthy)

# Respaldo / restauración
docker exec db-srv pg_dump -U appuser postgres > respaldo_lab14.sql

# Self-healing (la API se reinicia sola)
docker compose exec api pkill -f app.py
sleep 6 && docker compose ps api        # vuelve a (healthy)
```

> Es el **resultado final de la pista A** y el ensayo general del Proyecto
> Semestral. El checklist de cierre está en
> [../SESION-4.md](../SESION-4.md#paso-5-del-laboratorio-al-proyecto-semestral).
