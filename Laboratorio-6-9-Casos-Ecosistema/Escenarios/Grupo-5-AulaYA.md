# Grupo 5 · AulaYA — educación

**Sector:** educación virtual · **Base IP:** `192.168.92.0/24` · **Dominio:** `aula.local`

## Contexto

**AulaYA** gestiona matrículas de cursos: estudiantes eligen curso y pagan su
matrícula. Tu equipo monta la red del campus virtual.

- **Portal** (nginx, público): catálogo de cursos → puertos `8081`/`8443`.
- **API** (plantilla): registra el **pago de la matrícula** → puerto `8088`.
- **DB** (postgres): estudiantes y matrículas → **aislada**.

## Transacción del ecosistema (la demo final)

Un estudiante abre `aula.local`, elige su curso y **paga la matrícula**: la API
lo registra y **persiste en la base**. El diagrama final muestra la matrícula
cruzando las subredes hasta la DB.

## Red esperada (misma estructura para todos)

| Caso | Subredes | Puertos |
|------|----------|---------|
| 1 | `portal` `/26` (subred simple) | 8081 / 8443 |
| 2 | + `pagos` `/26` contigua + router | 8088 |
| 3 | VLSM completo: pagos `/26` · portal `/28` · datos `/28` · admin `/29` (+ enlace `/30` en el diagrama) | 8081 / 8443 / 8088 |

## Servicios y nombres (Caso 3)

| Subred | Servicio | Nombre DNS |
|--------|----------|-----------|
| pagos | API | `api.aula.local` |
| portal | portal | `aula.local` |
| datos | DB | `db.aula.local` |

## Lo que demuestra de la Unidad 1 (capas)

1. **Aplicación (7):** HTTP/HTTPS, DNS.
2. **Transporte (4):** handshake TCP, puertos, TCP vs UDP, latencia.
3. **Red (3):** IP, máscara, subredes, VLSM (Caso 3), router y rutas.
4. **Enlace (2):** trama Ethernet capturada (MAC, EtherType) en el Caso 1.

## Entregable

Seguí los Casos 1-3 y los **DIAGRAMAS.md**; tu escenario solo cambia estos
nombres e IPs respecto de la guía.