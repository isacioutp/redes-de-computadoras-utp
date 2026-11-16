# Pista B — Packet Tracer: el perímetro que Docker no puede mostrar

**Laboratorio autónomo y opcional.** No depende de las sesiones de Docker
Compose (pista A) y **no influye** en su nota. Se puede hacer antes, durante o
después, o no hacer.

> **Para qué sirve:** donde Docker abstrae, Packet Tracer *muestra*. Aquí el
> bastión es un host de verdad, las interfaces existen, las subredes se ven y el
> tráfico se inspecciona paquete a paquete. Es la lupa de la red física.

> **Independencia:** ningún paso de este documento requiere haber hecho la pista
> A, y ningún paso de la pista A requiere este documento. Las comparaciones
> "gemelo Docker" que aparecen abajo son **opcionales**: sirven para entender,
> nunca para aprobar.

## Objetivo

Diseñar y justificar, en Packet Tracer, una **LAN segmentada** con un **bastión
dual-homed** que media entre una subred pública y una red interna sin salida,
protegida por una **ACL**. Al terminar sabrás *por qué* la segmentación y el
control de acceso importan, con la red dibujada y funcionando.

## Entregable y evaluación (independiente)

| Criterio | Pts |
|----------|----:|
| Topología completa (R1, switch, bastión dual-homed, PC-admin, srv-interno) | 3 |
| Direccionamiento correcto (subred pública + interna, gateways) | 3 |
| ACL `SOLO-ADMIN` en R1 aplicada y funcional | 2 |
| Captura de Simulation mode con el paquete denegado | 1 |
| Diagrama (PNG) anotado + respuestas a las preguntas | 4 |
| **Total** | **10** |

> Esta nota es **independiente** de los 100 puntos de la pista A (Docker Compose).

---

## Paso 1 — Construye la topología

1. Coloca un **router** (R1), un **switch** (SW), **srv-bastion**, **PC-admin**
   y **srv-interno**.
2. Cablea según el diagrama: R1 ↔ SW; SW ↔ srv-bastion (pública) y ↔ PC-admin;
   **srv-bastion ↔ srv-interno directo** (la interfaz interna del bastión).
3. Enciende todas las interfaces (`no shutdown` en el router).

```text
 Internet ── R1 (router + ACL) ── SW ── srv-bastion (dual-homed)
                                          └─ PC-admin
                              srv-interno ── (interfaz interna del bastión)
```

| Dispositivo | Interfaz | IP | Máscara | Gateway |
|-------------|----------|----|---------|---------|
| R1 | G0/0 (WAN) | 200.200.200.1 | 255.255.255.252 | — |
| R1 | G0/1 (LAN) | 10.10.10.1 | 255.255.255.0 | — |
| srv-bastion | Fa0 (pública) | 10.10.10.2 | 255.255.255.0 | 10.10.10.1 |
| srv-bastion | Fa1 (interna) | 10.20.20.2 | 255.255.255.0 | — |
| srv-interno | Fa0 | 10.20.20.10 | 255.255.255.0 | 10.20.20.2 |
| PC-admin | Fa0 | 10.10.10.10 | 255.255.255.0 | 10.10.10.1 |

```text
[Checkpoint] PC-admin hace ping a 10.10.10.2 (bastión) y 10.10.10.1 (R1) OK,
pero NO alcanza 10.20.20.10 (la red interna no tiene ruta desde R1).
```

## Paso 2 — El bastión: SSH y por qué no enruta

En `srv-bastion`, habilita SSH:

```
# Servicios → SSH
enable secret clase
username admin secret admin123
ip domain-name lab14.local
crypto key generate rsa   ! 1024
line vty 0 4
 login local
 transport input ssh
```

**Regla de oro del bastión:** en `srv-bastion` **NO hay forwarding de paquetes**
(`ip routing` apagado). No es un router: es una estación a la que se llega y
desde la que se trabaja. La comunicación hacia lo interno pasa por **túneles
SSH**:

```
PC-admin>   ssh -l admin 10.10.10.2
srv-bastion> ssh -l interno 10.20.20.10     # segundo salto (ProxyJump manual)
```

```text
[Checkpoint] Llegas a 10.20.20.10 SOLO a través del bastión, nunca directo.
```

## Paso 3 — La ACL: el firewall del perímetro

En `R1`, interfaz G0/1:

```
ip access-list extended SOLO-ADMIN
  permit tcp host 10.10.10.10 host 10.10.10.2 eq 22
  deny   ip any host 10.20.20.10
  permit ip 10.10.10.0 0.0.0.255 any
interface G0/1
  ip access-group SOLO-ADMIN in
```

**Pruébalo en Simulation mode:** haz un ping de PC-admin a 10.20.20.10 y observa
el paquete detenerse en R1 con el ícono de "denegado". Ese paquete gris es el
perímetro haciendo su trabajo.

```text
[Checkpoint] PC-admin → 10.20.20.10 se detiene en R1 (denegado).
```

## Paso 4 — Observa el tráfico (Simulation mode)

PT no tiene `tcpdump`, pero tiene **Simulation mode**: avanza evento a evento y
inspecciona el PDU en cada salto. Observa el doble salto
`PC-admin → bastión → srv-interno` y responde la pregunta 3.

## Paso 5 — Entrega el diagrama

Exporta el `.pkt` y un PNG del diagrama lógico con estas anotaciones:

- [ ] Subred pública (10.10.10.0/24) y subred interna (10.20.20.0/24) rotuladas.
- [ ] Bastión dual-homed con sus 2 interfaces marcadas.
- [ ] ACL aplicada en R1 indicada en el diagrama.
- [ ] Nota: "srv-interno sin ruta a Internet".

> Si además haces la pista A, este diagrama es un buen insumo para el Proyecto
> Semestral. No es requisito de la pista A.

## Preguntas (independientes)

1. ¿Por qué `srv-interno` tiene como gateway al bastión y **no** a R1? ¿Qué se
   logra con eso?
2. En la ACL `SOLO-ADMIN`, ¿qué pasaría si intercambias el orden del `permit` y
   el `deny`? ¿Por qué?
3. En Simulation mode, observa el doble salto PC → bastión → srv-interno. ¿En qué
   dispositivo cambia la IP de destino del paquete? ¿Y la de origen?
4. Busca "forwarding" en la configuración del bastión. ¿Está habilitado? Justifica
   por qué un bastión real **no** debe enrutar.
5. ¿Cuál de los dos modelos de segmentación (una ruta que no existe + ACL aquí,
   o `internal: true` en Docker) es más fácil de auditar y por qué?

## Entregable

- Archivo `.pkt` funcional (topología completa y direccionada).
- PNG del diagrama con las anotaciones del Paso 5.
- Captura del paquete denegado en Simulation mode.
- Respuestas a las preguntas 1-5.

## Puente opcional con Docker (solo para *entender*, no para aprobar)

| En esta pista (PT) | En la pista A (Docker Compose) |
|--------------------|-------------------------------|
| Subredes 10.10.10.0/24 y 10.20.20.0/24 | `front` (172.28.10.0/24) y `back` (172.28.20.0/24) |
| srv-interno sin ruta a Internet | red `back` con `internal: true` |
| Bastión dual-homed | API en las dos redes (el "puente") |
| ACL en R1 | puertos publicados vs `expose` |
| Simulation mode: paquete hop a hop | `tcpdump` en la interfaz |
| Table → routing table | `docker network inspect` |
