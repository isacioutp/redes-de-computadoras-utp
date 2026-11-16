# Grupo 1 · FeriaYA — retail (marketplace)

**Sector:** comercio electrónico · **Base IP:** `192.168.88.0/24` · **Dominio:** `feria.local`

## Contexto

**FeriaYA** es un marketplace: miles de vendedores ofrecen productos y los
compradores pagan en línea. Tu equipo monta la red de su centro de operaciones.

- **Portal** (nginx, público): catálogo de productos → puertos `8081`/`8443`.
- **API** (plantilla): registra el **pago de cada pedido** → puerto `8088`.
- **DB** (postgres): catálogo e historial de pedidos → **aislada**.

## Transacción del ecosistema (la demo final)

Un comprador abre `feria.local`, elige un producto y **paga el pedido**: la API
lo registra y **persiste en la base**. El diagrama final muestra ese flujo del
pedido cruzando las subredes.

## Red esperada (misma estructura para todos)

| Caso | Subredes | Puertos |
|------|----------|---------|
| 1 | `portal` `/26` (subred simple) | 8081 / 8443 |
| 2 | + `pagos` `/26` contigua + router | 8088 |
| 3 | VLSM completo: pagos `/26` · portal `/28` · datos `/28` · admin `/29` (+ enlace `/30` en el diagrama) | 8081 / 8443 / 8088 |

## Servicios y nombres (Caso 3)

| Subred | Servicio | Nombre DNS |
|--------|----------|-----------|
| pagos | API | `api.feria.local` |
| portal | portal | `feria.local` |
| datos | DB | `db.feria.local` |

## Lo que demuestra de la Unidad 1 (capas)

1. **Aplicación (7):** HTTP/HTTPS, DNS.
2. **Transporte (4):** handshake TCP, puertos, TCP vs UDP, latencia.
3. **Red (3):** IP, máscara, subredes, VLSM (Caso 3), router y rutas.
4. **Enlace (2):** trama Ethernet capturada (MAC, EtherType) en el Caso 1.

## Entregable

Seguí los Casos 1-3 y los **DIAGRAMAS.md**; tu escenario solo cambia estos
nombres e IPs respecto de la guía.