# Grupo 3 · RutaYA — logística

**Sector:** logística y mensajería · **Base IP:** `192.168.90.0/24` · **Dominio:** `ruta.local`

## Contexto

**RutaYA** mueve paquetes entre ciudades: clientes registran envíos y pagan el
flete. Tu equipo monta la red de su centro de distribución.

- **Portal** (nginx, público): seguimiento de envíos → puertos `8081`/`8443`.
- **API** (plantilla): registra el **cobro del flete** → puerto `8088`.
- **DB** (postgres): envíos y estados → **aislada**.

## Transacción del ecosistema (la demo final)

Un cliente abre `ruta.local`, genera su envío y **paga el flete**: la API lo
registra y **persiste en la base**. El diagrama final muestra el envío cruzando
las subredes hasta la DB.

## Red esperada (misma estructura para todos)

| Caso | Subredes | Puertos |
|------|----------|---------|
| 1 | `portal` `/26` (subred simple) | 8081 / 8443 |
| 2 | + `pagos` `/26` contigua + router | 8088 |
| 3 | VLSM completo: pagos `/26` · portal `/28` · datos `/28` · admin `/29` (+ enlace `/30` en el diagrama) | 8081 / 8443 / 8088 |

## Servicios y nombres (Caso 3)

| Subred | Servicio | Nombre DNS |
|--------|----------|-----------|
| pagos | API | `api.ruta.local` |
| portal | portal | `ruta.local` |
| datos | DB | `db.ruta.local` |

## Lo que demuestra de la Unidad 1 (capas)

1. **Aplicación (7):** HTTP/HTTPS, DNS.
2. **Transporte (4):** handshake TCP, puertos, TCP vs UDP, latencia.
3. **Red (3):** IP, máscara, subredes, VLSM (Caso 3), router y rutas.
4. **Enlace (2):** trama Ethernet capturada (MAC, EtherType) en el Caso 1.

## Entregable

Seguí los Casos 1-3 y los **DIAGRAMAS.md**; tu escenario solo cambia estos
nombres e IPs respecto de la guía.