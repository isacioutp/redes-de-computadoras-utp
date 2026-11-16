# Grupo 8 · RefuYA — energía

**Sector:** estaciones de servicio · **Base IP:** `192.168.95.0/24` · **Dominio:** `refu.local`

## Contexto

**RefuYA** opera estaciones de servicio: el conductor registra su repostaje y
paga el combustible. Tu equipo monta la red de la estación.

- **Portal** (nginx, público): precios y reporte → puertos `8081`/`8443`.
- **API** (plantilla): registra el **pago del repostaje** → puerto `8088`.
- **DB** (postgres): consumos y tanquadas → **aislada**.

## Transacción del ecosistema (la demo final)

Un conductor abre `refu.local`, registra su repostaje y **paga el combustible**:
la API lo registra y **persiste en la base**. El diagrama final muestra el
repostaje cruzando las subredes hasta la DB.

## Red esperada (misma estructura para todos)

| Caso | Subredes | Puertos |
|------|----------|---------|
| 1 | `portal` `/26` (subred simple) | 8081 / 8443 |
| 2 | + `pagos` `/26` contigua + router | 8088 |
| 3 | VLSM completo: pagos `/26` · portal `/28` · datos `/28` · admin `/29` (+ enlace `/30` en el diagrama) | 8081 / 8443 / 8088 |

## Servicios y nombres (Caso 3)

| Subred | Servicio | Nombre DNS |
|--------|----------|-----------|
| pagos | API | `api.refu.local` |
| portal | portal | `refu.local` |
| datos | DB | `db.refu.local` |

## Lo que demuestra de la Unidad 1 (capas)

1. **Aplicación (7):** HTTP/HTTPS, DNS.
2. **Transporte (4):** handshake TCP, puertos, TCP vs UDP, latencia.
3. **Red (3):** IP, máscara, subredes, VLSM (Caso 3), router y rutas.
4. **Enlace (2):** trama Ethernet capturada (MAC, EtherType) en el Caso 1.

## Entregable

Seguí los Casos 1-3 y los **DIAGRAMAS.md**; tu escenario solo cambia estos
nombres e IPs respecto de la guía.