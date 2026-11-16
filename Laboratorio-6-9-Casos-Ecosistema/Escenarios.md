# Escenarios por equipo

Cada equipo recibe **una** hoja de escenario (`Escenarios/Grupo-N-*.md`). El
contenido de los Casos 1-3 es el mismo para todos; **solo cambia el escenario**:
empresa, dominio, base IP y la "transacción" del negocio. Eso es lo que hace que
cada demo sea distinta.

## Asignación según el número de equipos

32 estudiantes · equipos de 4-6 → **6-8 equipos**:

| Equipos | Escenarios usados |
|---------|-------------------|
| 6 | Grupo 1 … Grupo 6 |
| 7 | Grupo 1 … Grupo 7 |
| 8 | Grupo 1 … Grupo 8 |

Elegí la base 88 como tercer octeto del Grupo 1 para que quede "cerca" del
clásico `192.168.88.0/24` de Cisco que ya conocen.

## Base IP por grupo

| Grupo | Escenario | Base IP (0/24) | Dominio |
|------:|-----------|----------------|---------|
| 1 | FeriaYA — retail | `192.168.88.0/24` | `feria.local` |
| 2 | MediYA — salud | `192.168.89.0/24` | `medi.local` |
| 3 | RutaYA — logística | `192.168.90.0/24` | `ruta.local` |
| 4 | CineYA — entretenimiento | `192.168.91.0/24` | `cine.local` |
| 5 | AulaYA — educación | `192.168.92.0/24` | `aula.local` |
| 6 | GymYA — fitness | `192.168.93.0/24` | `gym.local` |
| 7 | HotelYA — hotelería | `192.168.94.0/24` | `hotel.local` |
| 8 | RefuYA — energía | `192.168.95.0/24` | `refu.local` |

> La estructura de la red es idéntica en todos: Caso 1 portal `/26` + Caso 2
> `pagos` `/26` + Caso 3 VLSM completo. Lo único que cambia el octeto y los
> nombres (servicios, DNS, base de datos).

## Recursos comunes (iguales para todos)

- Plantilla de la API: `plantilla/` (Dockerfile + `app.py` + `init.sql`).
- Los puertos host son los mismos para todos (cada equipo trabaja en su máquina):
  portal HTTP `8081`, portal HTTPS `8443`, API `8088`, DNS `8053/UDP`.
- Los nombres internos en el Caso 3 siguen el patrón `<servicio>.local` de tu
  escenario (portal, API, DB).

## Regla anti-plagio entre grupos

Las entregas con la **misma IP exacta** (mismo octeto) o el **mismo dominio**
que otro grupo se consideran copia. Cada escenario tiene el suyo.