# Sesión 2 — archivos Docker

Archivos que necesita la **Sesión 2** (monitoreo y acceso seguro). Guía:
[../SESION-2.md](../SESION-2.md).

| Archivo | Para qué |
|---------|----------|
| `docker-compose.yml` | El stack **ya segmentado** (`front`/`back` + `internal: true`). Es el punto de partida; la sesión no lo rehace. |
| `dnsmasq.conf` | Zonas DNS internas ya resueltas. |
| `api/` | Código y `Dockerfile` de la API (Flask). |

## Uso

```bash
docker compose up -d
docker compose ps

# Monitoreo (Sesión 2): captura en la interfaz del contenedor web
docker compose exec web sh -c "apk add -q tcpdump && tcpdump -ni eth0 -c 20 port 80"
# en otra terminal: genera tráfico
curl -s -o /dev/null http://localhost:8080
```

> Es el **resultado final de la Sesión 1**. Si vienes de esa sesión, este stack ya
> lo tienes; este folder es el punto de partida para hacer la Sesión 2 **sola**.