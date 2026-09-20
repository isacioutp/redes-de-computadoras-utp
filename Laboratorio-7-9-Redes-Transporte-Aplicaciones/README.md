# Casos N.º 7-9 — red + transporte + aplicación (8 fichas)

Unidad II · Semanas 7-9
**Reemplazan los antiguos Labs N.º 7, 8 y 9 por 8 casos prácticos**, uno por
equipo, que cubren los mismos temas pero aplicados a empresas distintas.
Alimentan el Avance N.º 1 del Proyecto Semestral (diagrama + direccionamiento IP).

## Qué es esto

En lugar de tres laboratorios pequeños, **8 fichas de caso de implementación**
con una **mini-aplicación real** (portal + API + base de datos). Cada equipo
(4-6) recibe su ficha (`casos/Caso-01.md` .. `Caso-08.md`), despliega **la red
completa de su empresa con Docker** y **presenta con una demo funcional** cómo
un mensaje viaja de punta a punta y cómo un registro (pago, matrícula, viaje…)
se guarda de verdad en la base de datos a través de la red segmentada.

> **Red simplificada: 3 segmentos (uno por capa).** `sub-web` (portal, pública),
> `sub-api` (API, aplicación) y `sub-db` (DB, aislada), unidas por un router.
> Cada equipo hace **3 subredes VLSM** sobre su `/24` y demuestra los conceptos
> con pruebas.

> **Conceptos = pruebas.** Cada tópico del curso (VLSM, enrutamiento, TCP,
> HTTP/HTTPS, DNS…) se **demuestra con una prueba en vivo** sobre su red Docker
> (`CASO.md` sección 4). No se evalúan diapositivas: se evalúa que el concepto
> **se ve** corriendo.

**Evaluación simple** (ver [EVALUACION.md](EVALUACION.md)):

```
Documento (40) + Presentación/Demo (30) + Prueba funcional en vivo (30) = 100
```

## La app (compartida por las 8 fichas)

```
Navegador → [portal  nginx :8081]  →  [API  Flask :8088]  →  [DB Postgres]
             sub-web (pública)         sub-api (app)            sub-db (aislada)
```

La plantilla funcional está en `plantilla/` (API Flask con Postgres + `init.sql`
+ portal). El trabajo del equipo es la **red y las configuraciones** (3 subredes,
router, rutas, puertos, DNS, HTTPS) que la hacen funcionar en **su** empresa.

## El viaje del mensaje (lo que los casos demuestran)

```
USUARIO                  SERVIDOR
  │                        │
  │ ① https://pagosya.local│
  │   DNS → IP del portal  │  ← CAPA DE APLICACIÓN (HTTP/HTTPS/DNS)
  │                        │
  │ ② TCP SYN→SYN-ACK→ACK │  ← CAPA DE TRANSPORTE (handshake, puertos)
  │   (puerto 5000)        │
  │ ③ IP → subred → router │  ← CAPA DE RED (VLSM, rutas, ICMP/traceroute)
  │   (TTL decrece)        │
  │ ④ Trama Ethernet (MAC) │  ← Enlace (Lab 6)
  └────────────────────────┘
```

## Archivos de este caso

| Ruta | Contenido |
|------|-----------|
| `CASO.md` | **Procedimiento común** de los 8 casos (escenario base, requisitos por capa, prueba funcional, reglas) |
| `casos/` | **Las 8 fichas de caso** (`Caso-01.md` .. `Caso-08.md`): una por equipo |
| `EVALUACION.md` | **Rúbrica** (documento + presentación/demo + prueba funcional) |
| `DEMO-DOCENTE.md` | Guion del docente (60 min): demo intro + entrega de las 8 fichas |
| `plantilla/` | **App funcional de regalo** (API Flask + Postgres `init.sql` + portal HTML) |
| `demo/` | Stack Docker del docente: ejemplo FUNCIONAL de referencia |

## Cómo se trabaja

| Momento | Actividad |
|---------|-----------|
| Clase 1 (demo) | Docente presenta la demo intro (`DEMO-DOCENTE.md`) y **sortea una ficha de caso por equipo** (`casos/`) |
| Tras la clase | Cada equipo implementa su ficha: red + mini-app funcional (con los hints de `CASO.md`) |
| **Siguiente clase** | **Presentaciones**: documento + demo en vivo + prueba funcional (máx. 10 min) |

> El stack `demo/` es la **referencia funcional** del docente. Los estudiantes
> construyen el suyo con base en su ficha (cada empresa tiene su propia base y
> su tabla VLSM).

## Base teórica en 1 tabla

| Capa | Qué resuelve | Protocolos / herramientas |
|------|--------------|---------------------------|
| Red | ¿Dónde está el destino? Subredes, rutas | IP, VLSM, ICMP, ARP, DHCP, router |
| Transporte | ¿Cómo se entrega intacto? Confiabilidad | TCP (handshake), UDP, puertos, netem |
| Aplicación | ¿Quién lo entiende? El servicio | HTTP/HTTPS, DNS, SMTP, FTP, SNMP |

## Archivo de las versiones guiadas

Las guías por sesión de los antiguos Labs 7, 8 y 9 se conservan en
`../_archivo-Laboratorios-7-8-9/` como material de referencia del docente.

## Limpieza

```bash
docker compose -f demo/docker-compose.yml down --remove-orphans
docker rm -f $(docker ps -aq --filter name=lab79) 2>/dev/null || true
docker network rm $(docker network ls -q --filter name=sub-) 2>/dev/null || true
```