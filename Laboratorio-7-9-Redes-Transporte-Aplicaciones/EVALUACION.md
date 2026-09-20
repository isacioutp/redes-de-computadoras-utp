# EVALUACIÓN — Casos N.º 7-9 (8 fichas en `casos/`)

Evaluación **simple** en 3 partes · Total **100 puntos** · Idéntica para las 8
fichas de caso (documento, demo y prueba funcional de la tuya).

| Parte | % | Qué se califica |
|-------|---|-----------------|
| **📄 Documento** | 40 | Informe técnico completo (diagrama, VLSM, tablas, capturas, respuestas) |
| **🎤 Presentación / Demo** | 30 | Demo **en vivo** del sistema funcionando, narrada capa por capa |
| **🔬 Prueba funcional** | 30 | Checklist de la sección 4 del caso ejecutado **en la presentación** |

---

## 1. Documento (40 pts)

| Criterio | Pts |
|----------|-----|
| Diagrama de la red (subredes, IPs, router, servicios, puertos) | 8 |
| Tabla VLSM completa y correcta + justificación | 8 |
| Tabla de servicios y puertos (TCP/UDP) | 6 |
| Capturas anotadas (ping→ruta→ping, traceroute, handshake, netem, dig, curl -k) | 12 |
| Respuestas a las 3 preguntas guía + conclusión | 6 |
| **Subtotal** | **40** |

## 2. Presentación / Demo (30 pts)

| Criterio | Pts |
|----------|-----|
| Demo en vivo funcionando (no solo capturas) | 10 |
| Narración del **viaje del mensaje** por las 3 capas al ejecutar la prueba | 10 |
| Claridad, dominio y respuestas a preguntas (máx. 10 min) | 10 |
| **Subtotal** | **30** |

## 3. Prueba funcional (30 pts) — los tópicos se DEMUESTRAN con pruebas

Checklist ejecutado **en vivo**, con Docker, sobre el caso asignado (sección 4
de `CASO.md`). **Cada prueba demuestra un tópico**; una entrega por **equipo
(4-6)**, incluye la mini-app funcional:

| # | Tópico | Prueba | Pts |
|---|--------|--------|-----|
| 1 | ICMP + enrutamiento | `ping` sin ruta FALLA | 2 |
| 2 | ICMP + enrutamiento | `ping` con ruta → 0 % pérdida | 4 |
| 3 | Routers / TTL | `traceroute` → 2-3 saltos (via router/es) | 3 |
| 4 | Aplicación (HTTP) | `curl` API → 200 + JSON | 4 |
| 5 | TCP (handshake) | `tcpdump` → SYN/SYN-ACK/ACK | 5 |
| 6 | DNS | `dig pagosya.local` → IP del portal | 3 |
| 7 | HTTPS | `curl -k https://…:8443/` → HTML | 3 |
| 8 | Aislamiento / seguridad | `docker port <db>` vacío (DB aislada) | 3 |
| 9 | Aplicación real (3 capas) | `POST /pagos` 201 + `GET /pagos` lo lista (persistido en DB) | 3 |
| **Subtotal** | | **30** |

---

## Penalidades

| Falta | Pena |
|-------|------|
| Base de datos expuesta al host o internet | −30 (violación de seguridad del caso) |
| Presentar solo capturas (sin demo en vivo) | −15 de la parte 2 |
| Entrega tarde | −2 pts/día (regla del curso) |
| Solución idéntica a otro equipo | −100 (regla de integridad) |