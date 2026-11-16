# Grupo 6 · GymYA — fitness

**Sector:** gimnasios y membresías · **Base IP:** `192.168.93.0/24` · **Dominio:** `gym.local`

## Contexto

**GymYA** vende membresías de gimnasio: el socio elige plan y paga su cuota
mensual. Tu equipo monta la red de la sede.

- **Portal** (nginx, público): planes y suscripción → puertos `8081`/`8443`.
- **API** (plantilla): registra el **pago de la membresía** → puerto `8088`.
- **DB** (postgres): socios y membresías → **aislada**.

## Transacción del ecosistema (la demo final)

Un socio abre `gym.local`, elige su plan y **paga la membresía**: la API lo
registra y **persiste en la base**. El diagrama final muestra la membresía
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
| pagos | API | `api.gym.local` |
| portal | portal | `gym.local` |
| datos | DB | `db.gym.local` |

## Lo que demuestra de la Unidad 1 (capas)

1. **Aplicación (7):** HTTP/HTTPS, DNS.
2. **Transporte (4):** handshake TCP, puertos, TCP vs UDP, latencia.
3. **Red (3):** IP, máscara, subredes, VLSM (Caso 3), router y rutas.
4. **Enlace (2):** trama Ethernet capturada (MAC, EtherType) en el Caso 1.

## Entregable

Seguí los Casos 1-3 y los **DIAGRAMAS.md**; tu escenario solo cambia estos
nombres e IPs respecto de la guía.