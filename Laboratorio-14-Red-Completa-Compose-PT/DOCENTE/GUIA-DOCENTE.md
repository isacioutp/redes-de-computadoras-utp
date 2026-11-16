# Guía docente — Laboratorio N.º 14 (4 sesiones)

Documento **interno** (no publicar al estudiante). Reúne el guion de las 4
sesiones, la logística, los errores frecuentes y las respuestas de referencia.
Los comandos exactos y el Compose de referencia están en
[SOLUCIONES.md](SOLUCIONES.md); el diagrama del `.pkt` (pista B opcional), en
[../DIAGRAMAS.md](../DIAGRAMAS.md).

> **Materiales del estudiante:** [../README.md](../README.md),
> [../SESION-1..4.md], [../TEORIA.md](../TEORIA.md),
> [../GUIA-ESTUDIO.md](../GUIA-ESTUDIO.md), [../EVALUACION.md](../EVALUACION.md),
> y los archivos Docker de cada sesión:
> [../sesion-1/](../sesion-1/README.md), [../sesion-2/](../sesion-2/README.md),
> [../sesion-3/](../sesion-3/README.md), [../sesion-4/](../sesion-4/README.md).
> La **pista B opcional** es [../PACKET-TRACER.md](../PACKET-TRACER.md).

## 0. Encuadre general

| Aspecto | Detalle |
|---------|---------|
| Duración | 4 clases × ~120 min |
| Modalidad | Individual o parejas (informe por equipo) |
| Herramientas | **Pista A:** Docker Engine + `docker compose` (obligatoria) · **Pista B:** Packet Tracer (opcional, independiente) |
| Requisito previo | Labs 10-12 cursados (o al menos 10) |
| Hilo | Compose = **ejecución/red del data center** · PT (pista B opcional) = **diseño/perímetro** |
| Cierre | Ensayo general del Proyecto Semestral |

**Mensaje que debe quedar (repetirlo cada sesión):** *en producción el bastión
es un host/VM, no un contenedor; el bastión real de tu proyecto es el host.*

**Eje del laboratorio:** la **orquestación con Compose**. Las Sesiones 1-2
habilitan el stack; las 3-4 lo orquestan. El material
[../REFUERZO-ORQUESTACION.md](../REFUERZO-ORQUESTACION.md) (drills de
imperativo→declarativo, depuración de un Compose roto, secretos, escalado) se
asigna **después de la Sesión 2** y se repasa antes de la Sesión 4. Si se atrasa,
se recorta la demo, **no** la orquestación.

### Preparación previa del entorno

```bash
docker --version && docker compose version
docker network create prueba && docker network rm prueba   # prueba rápida
# Solo si se dicta la pista B (opcional): Packet Tracer instalado y funcionando
```

Si el aula no tiene Docker, se puede dictar la Sesión 3 en modalidad demostración
(el docente proyecta) y pedir el resto como tarea con capturas.

---

## Sesión 1 — Primer stack con Compose + segmentación (~120 min)

| Min | Actividad | Nota docente |
|----:|-----------|--------------|
| 0-10 | Encuadre: **es un curso de redes**; Compose es el *medio*, la red es el *tema* | Presentar la tabla "anclaje de redes" del README |
| 10-35 | **Paso 1:** primer `docker compose up` (web/api/db en una red) | El "wow": un archivo = un stack. No se escribió `docker run` |
| 35-50 | **Paso 2:** el problema de la red plana (`web → db`) | Que ellos descubran: "¿debería la web hablar con la DB?" |
| 50-90 | **Paso 3:** refactor a `front`/`back` + `internal` + DNS | Leer juntos el YAML; explicar `ipam` y `expose` vs `ports` |
| 90-105 | **Paso 4:** puente conceptual (tabla red física ↔ Docker) | Aclarar que PT es la pista B opcional, no requisito |
| 105-120 | Preguntas 1-4 + entregable | Insistir: `internal: true` = "subred sin salida" |

**Checkpoints de la sesión:** stack levantado con `up` · `web↛db` y `api→db` ·
`nslookup` de los 3 nombres.

---

## Sesión 2 — Monitoreo y acceso seguro (~120 min)

| Min | Actividad | Nota docente |
|----:|-----------|--------------|
| 0-10 | Repaso de segmentación (`docker compose ps` + pruebas) | No se reconstruye nada |
| 10-55 | Monitoreo: `tcpdump`, `iftop`, netdata | Hablar de métricas de red: ancho de banda, latencia, capas |
| 55-95 | **SSH por llave al host** + deshabilitar password | El momento "el bastión es el host" |
| 95-110 | Seguridad de acceso: qué dejar abierto y por qué | El host es el bastión; la DB no se publica nunca |
| 110-120 | Preguntas 1-4 y entregable | Reforzar: `internal: true` ≠ no publicar puertos |

**Riesgos técnicos y planes B:**

- `apt-get`/`apk` sin internet en el aula → usar imágenes que ya traen la
  herramienta o la captura del docente.
- netdata no arranca → basta `tcpdump` como evidencia mínima.
- Windows sin `sshd` → usar WSL o una VM ligera; documentar el paso.

---

## Sesión 3 — Orquestación con Compose (~120 min)

| Min | Actividad | Nota docente |
|----:|-----------|--------------|
| 0-15 | Concepto de orquestación y tabla Compose vs `docker run` | De [../TEORIA.md](../TEORIA.md) §5 |
| 15-50 | Construir el `docker-compose.yml` completo (redes, secretos, healthchecks) | El secreto nunca en el YAML |
| 50-75 | `up --wait` + `docker compose ps` en `(healthy)` | Explicar `depends_on: condition` |
| 75-95 | `--scale api=2` y balanceo por DNS | Aclarar que es balanceo por DNS, no proxy |
| 95-110 | Inspección del secreto y `grep` limpio | Principio de mínima exposición |
| 110-120 | **Swarm solo teoría** (5 min) + preguntas 1-4 | No ejecutar Swarm |

**Refuerzo del eje:** si hay tiempo en la Sesión 3, intercalar los drills 1-2 de
[../REFUERZO-ORQUESTACION.md](../REFUERZO-ORQUESTACION.md) (convertir `docker run`
a Compose y depurar el YAML roto). El resto de drills queda como trabajo
autónomo antes de la Sesión 4.

**Mensaje clave de la sesión:** el mismo YAML migra a Swarm/Kubernetes.

---

## Sesión 4 — Integración y respaldo (~120 min)

| Min | Actividad | Nota docente |
|----:|-----------|--------------|
| 0-20 | `down -v` + `up --wait`: demostrar reproducibilidad | "Nadie toca `docker run`" |
| 20-55 | Respaldo y restauración de PostgreSQL | El activo más crítico |
| 55-75 | Self-healing (matar el proceso del API) | Reconciliación del estado deseado |
| 75-110 | **Demo integrada por equipo** (10 min c/u) | Stack Docker en vivo; la pista B (PT) se presenta aparte si se hizo |
| 110-120 | Checklist del Proyecto Semestral + cierre | De [../SESION-4.md](../SESION-4.md) |

**Evaluación:** usar [../EVALUACION.md](../EVALUACION.md). Cotejar en vivo; no
aceptar capturas de contenedores que no existen al momento de revisar.

---

## Errores frecuentes en clase

| Síntoma | Causa | Indicación |
|---------|-------|-----------|
| La red `back` tiene internet | falta `internal: true` | editar y `docker compose up -d` |
| `front` alcanza la DB | la DB publica puertos | quitar `ports:` |
| DNS no resuelve | IP del contenedor ≠ `dnsmasq.conf` | sincronizar IPs |
| El stack arranca antes de tiempo | `depends_on` sin `condition` | usar `service_healthy` |
| La clave aparece en `docker inspect` | se usó `environment:` | migrar a `secrets:` |
| `up` no espera | falta `--wait` | agregar el flag |
| Perdieron los datos | `down -v` | respaldar antes; usar `down` |

## Reparto sugerido (si es en parejas)

- **Rol A (red):** Sesión 1 (redes, DNS, segmentación).
- **Rol B (servicios/seguridad):** Sesión 2 (SSH, segmentación, monitoreo).
- **Ambos:** Sesión 3 (Compose) y Sesión 4 (integración/demo).
- **Pista B (opcional, aparte):** quien quiera refuerza el diseño en Packet Tracer.

## Autoevaluación del docente

- [ ] ¿Quedó claro por qué el bastión real es el host?
- [ ] ¿Se ejecutó la prueba de segmentación en vivo?
- [ ] ¿Se migró todo a `docker compose` (sin `docker run` sueltos)?
- [ ] ¿Se dejó claro que Swarm es el siguiente paso, no el de hoy?
- [ ] ¿El estudiante puede reproducir su stack con un comando?
