# Guía de estudio — Unidad III · 3.1 LAN y 3.2 Monitoreo

> **Material del estudiante.** Acompaña la clase de los temas **3.1
> (implementación de una LAN)** y **3.2 (herramientas de monitoreo)** y el
> `Laboratorio N.º 10`. Úsala para repasar antes de la práctica y antes del
> examen: primero la **chuleta** (secciones 1-4), luego el **banco de preguntas**
> (sección 5) y, al final, las **respuestas** (sección 7) para autocorregirte.
>
> Presentación de la clase: `Teoria-U3-Parte1-LAN-Monitoreo.pptx` · versión en
> texto: `TEORIA-U3-Parte1-LAN-Monitoreo.md`.

---

## 1. La idea de la clase en una frase

> **Segmentar** la red (para que sea medible y segura) y **medirla** (para poder
> diagnosticarla). Una LAN que no se segmenta se degrada; una LAN que no se mide
> está a ciegas.

---

## 2. Resumen de conceptos (lo que hay que recordar)

### 2.1 LAN y segmentación

- Una LAN es un **dominio de broadcast**: todos los equipos del mismo segmento se
  «ven» entre sí.
- Una **LAN plana** (una sola subred) se degrada al crecer: **tráfico de
  broadcast**, **un solo dominio de falla** y **exposición directa** (un usuario
  llega al puerto de la base de datos).
- Se segmenta en **dos capas**:

| | VLAN (802.1Q) | Subred IP |
|--|---------------|-----------|
| Capa | **2 · enlace** | **3 · red** |
| Se configura en | Switch (trunk/access) | Host o router |
| Aísla | El tráfico entre puertos | El tráfico L3 por diseño |
| Se rompe si… | El trunk no soporta el tag | Las rutas están mal |

- El **tag 802.1Q** son **4 bytes**; el **VLAN ID** va de **1 a 4094**.
- **Access** = un puerto, una VLAN · **Trunk** = un puerto, varias VLAN.
- **VLAN y subred no compiten:** VLAN segmenta en capa 2, la subred en capa 3.
  El router decide qué tráfico cruza. **Dos VLAN con la misma subred IP no
  funcionan** (se duplican rangos y se rompe el retorno).

### 2.2 Los tres servicios mínimos de una LAN

| Servicio | Qué resuelve | Clave para recordar |
|----------|--------------|---------------------|
| **DHCP** | Entrega direcciones | Flujo **DORA**: Discover → Offer → Request → Ack |
| **DNS** | Resuelve nombres | **Desacopla el nombre de la IP**; cambiar la IP no rompe la app |
| **NAT** | Traduce direcciones privadas | Las IP **RFC 1918** no se enrutan en internet |

> Por DHCP se entrega **también** el **gateway** y el **DNS**, no solo la IP.

### 2.3 El router de capa 3

Para que un host/contenedor haga de **router entre dos subredes**, hacen falta
**tres condiciones**:

1. **`net.ipv4.ip_forward=1`** (reenvío habilitado) — *el que más se olvida*.
2. **Una interfaz por subred** (una «pata» en cada red).
3. **Ruta en ambos sentidos** (ida **y vuelta**).

> **Síntoma clásico:** «el ping sale pero no vuelve» → falta la **ruta de vuelta**
> o el **gateway**. Es el error #1 de enrutamiento.

### 2.4 Las métricas de red (3.2)

| Métrica | Se mide con | Valor sano (LAN) | Si está mal, sospechar de… |
|---------|-------------|------------------|----------------------------|
| Ancho de banda | `iperf3` | >100 Mbps en Gigabit | Enlace saturado · cuello de botella |
| Latencia | `ping` / ICMP | <1 ms en la LAN | Congestión · ruta larga |
| Pérdida | `ping` · `iperf3 -u` | 0 % | Cable · switch · saturación |
| Jitter | `iperf3 -u` | <5 ms | Voz/video con cortes |
| Errores | `ip -s link` | 0 CRC / 0 drops | Cable · conector · duplex mismatch |

### 2.5 ¿Cada herramienta, qué pregunta responde?

| Herramienta | Responde a… |
|-------------|-------------|
| **`tcpdump`** | **qué** pasa (el contenido de la conversación) |
| **`iftop`** | **quién** consume la red (barras por host, en vivo) |
| **`iperf3`** | **cuánto** aguanta el enlace (ancho de banda, TCP vs UDP) |
| **`netdata`** | **cómo evoluciona** (gráficas e histórico) |

### 2.6 Medir con TCP y con UDP no es lo mismo

- **TCP se adapta:** retransmite lo perdido y baja el caudal. Mira el **`Retr`**
  (retransmisiones). Sirve para datos que no pueden perderse.
- **UDP pierde y no avisa:** no retransmite. Reporta **`jitter`** y **`Lost`**.
  Es lo que se parece a una **videollamada**: tolera algo de pérdida, pero no
  jitter alto.

### 2.7 Monitoreo por capas (método, no lista de comandos)

| Capa | Evidencia | Herramienta |
|------|-----------|-------------|
| 1 · Física | estado del enlace, CRC, drops | `ip -s link` |
| 2 · Enlace | tramas, MAC, ARP | `tcpdump` |
| 3 · Red | alcanzabilidad y ruta | `ping` · `traceroute` |
| 4 · Transporte | conexiones y throughput | `ss` · `iperf3` |
| 7 · Aplicación | nombres y respuestas de servicios | `dig` / `nslookup` |

> **Regla de oro:** monitorear **no es mirar**, es **hipótesis + verificación**.
> Si dos contenedores del **mismo host** marcan **40 ms**, el problema **no** es la
> red física: es el puente de Docker o un `netem` de otro laboratorio.

---

## 3. Chuleta de comandos (Laboratorio N.º 10)

```bash
# --- LAN: crear segmentos y el router dual-homed ---
docker network create publica --subnet 10.0.0.0/24 --gateway 10.0.0.1
docker network create interna --subnet 10.0.1.0/24 --gateway 10.0.1.1
docker run -d --name router-corp --cap-add=NET_ADMIN \
  --sysctl net.ipv4.ip_forward=1 alpine sleep 3600
docker network connect publica router-corp
docker network connect interna router-corp
docker exec router-corp ip addr show          # 2 interfaces

# --- Ruta explícita (ida y vuelta) ---
docker exec web-srv ip route add 10.0.1.0/24 via 10.0.0.2
docker exec web-srv ping -c 2 10.0.1.2

# --- tcpdump: ¿qué pasa? ---
docker exec web-srv sh -c "apk add --no-cache tcpdump -q"
docker exec web-srv tcpdump -i eth0 -nn -c 15 any port 80 or icmp

# --- iperf3: ¿cuánto aguanta? (TCP vs UDP) ---
docker run -d --name iperf-srv --network interna -p 5201:5201 mlabbe/iperf3 -s
docker run --rm --network interna mlabbe/iperf3 -c iperf-srv -t 5          # TCP
docker run --rm --network interna mlabbe/iperf3 -c iperf-srv -t 5 -u -b 100M  # UDP

# --- Errores de capa 1/2 ---
docker exec web-srv ip -s link                # CRC / drops

# --- DNS interno ---
nslookup web.local
```

---

## 4. Errores típicos (y su causa)

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| El router no reenvía | Falta `ip_forward=1` | `--sysctl net.ipv4.ip_forward=1` |
| `pool overlaps…` | Subred solapada | Revisar el VLSM y recrear la red |
| `app-srv` no resuelve `web-srv` | No está en `publica` | `docker network connect publica app-srv` |
| `tcpdump` vacío | Interfaz equivocada | Usar `-i eth0` y generar tráfico |
| `iperf3` no conecta | Cliente y servidor en redes distintas | Cliente con `--network interna` |
| `netdata` no abre en `:19999` | Faltan `SYS_PTRACE`/volúmenes | Usar el `docker run` completo del lab |
| `nslookup` no responde | Consulta al DNS del host | Pasar `--dns <ip-de-dns-corp>` |

---

## 5. Banco de preguntas (autoevaluación)

> Respóndelas sin mirar la sección 7. Las respuestas están al final.

**Concepto (3.1)**

1. ¿Por qué una **LAN plana** es un problema de **seguridad** además de
   rendimiento?
2. ¿Qué es un **dominio de broadcast** y por qué conviene dividirlo?
3. Diferencia **VLAN** de **subred**: ¿qué capa resuelve cada una?
4. ¿Qué significan **access** y **trunk** en una VLAN?
5. ¿Funcionarían **dos VLAN con la misma subred IP**? Justifica.
6. ¿Cuáles son las **tres condiciones** para que un contenedor haga de router
   entre dos redes?
7. Nombra los **tres servicios mínimos** de una LAN y qué resuelve cada uno.
8. ¿Qué se entrega por **DHCP** además de la dirección IP?
9. ¿Por qué el **DNS interno** es importante si ya sabemos las IP?
10. ¿Qué hace **NAT** y por qué las IP privadas (RFC 1918) no sirven en internet?

**Medición (3.2)**

11. Nombra las **cinco métricas** de red que importan.
12. ¿Qué herramienta usarías para demostrar que la red sostiene **100 Mbps**, y
    cuál para ver **quién** los consume?
13. Explica la diferencia entre **latencia**, **jitter** y **pérdida**.
14. En `iperf3`, ¿por qué **TCP** y **UDP** dan resultados distintos? ¿Qué es el
    `jitter` y con qué tipo de tráfico se relaciona?
15. Si dos contenedores del **mismo host** marcan **40 ms** de latencia, ¿cuál es
    la causa más probable?
16. ¿Qué comando usarías para detectar **errores de cable/conector**? ¿Qué
    valores serían sospechosos?
17. Relaciona cada capa OSI con una **evidencia** y su **comando** (capas 1, 2, 3,
    4 y 7).
18. ¿Cuál es la diferencia entre «mirar» y «monitorear»? Da un ejemplo.

**Aplicación**

19. Se te pide elegir **una herramienta** para demostrar en el proyecto que un
    servicio genera tráfico: ¿cuál eliges y por qué?
20. En **`netdata`**, ¿qué gráfica usarías para sospechar de un pico de tráfico
    anómalo (posible fuga o DDoS) y qué buscarías?

---

## 6. Glosario rápido

- **Broadcast:** trama que ven todos los equipos del segmento.
- **VLAN:** red lógica en capa 2 dentro de un switch (802.1Q).
- **Subred:** agrupación lógica en capa 3 (direcciones IP + máscara).
- **DORA:** secuencia de DHCP (Discover-Offer-Request-Ack).
- **NAT:** traducción de direcciones privadas ↔ públicas.
- **Ruta de vuelta:** camino de regreso de un paquete; sin él, «va pero no vuelve».
- **Jitter:** variación del retardo (clave en voz/video).
- **Throughput:** ancho de banda **real** medido (vs. el nominal del enlace).
- **CRC errors / drops:** errores de capa 1/2 en la interfaz.
- **trunk/access:** puerto que transporta varias VLAN / una sola.

---

## 7. Respuestas

1. Además de saturarse, deja a **cualquier equipo alcanzar directamente** los
   servicios internos (p. ej. el puerto de la **base de datos**).
2. Es el conjunto de equipos que reciben el mismo tráfico de broadcast; dividirlo
   **reduce el ruido** y el alcance de un fallo.
3. **VLAN = capa 2** (switch); **subred = capa 3** (IP/router). No compiten.
4. **Access** = un puerto con una sola VLAN; **trunk** = un puerto que transporta
   varias VLAN (tag 802.1Q).
5. **No:** duplicaría rangos, el host no sabría a qué VLAN ir y el retorno se
   rompe. Cada VLAN necesita su propia subred.
6. (1) `ip_forward=1`; (2) una interfaz por subred; (3) ruta en **ambos** sentidos.
7. **DHCP** (direcciones), **DNS** (nombres) y **NAT** (traducción a internet).
8. El **gateway** (puerta de enlace) y el **DNS**.
9. Desacopla el **nombre** de la **IP**: la app llama por nombre y cambiar la IP no
   rompe nada.
10. **NAT** traduce las IP privadas a una pública; las **RFC 1918** no son
    enrutables en internet, por eso se traducen.
11. **Ancho de banda, latencia, pérdida, jitter y errores.**
12. **`iperf3`** para demostrar el caudal; **`iftop`** (o `netdata`) para ver
    quién lo consume.
13. **Latencia** = retardo; **jitter** = variación del retardo; **pérdida** =
    paquetes que no llegan.
14. **TCP retransmite** y ajusta el caudal (mira `Retr`); **UDP no retransmite** y
    reporta `jitter`/`Lost`. El **jitter** es la variación del retardo, clave en
    **voz/video** (UDP).
15. El **puente de Docker** (o un `netem` de otro laboratorio), **no** la red
    física: 40 ms entre contenedores del mismo host es artificial.
16. **`ip -s link`**; sospechosos: **CRC > 0** o **drops > 0** (cable, conector o
    duplex mismatch).
17. (1) `ip -s link` · (2) `tcpdump` · (3) `ping`/`traceroute` · (4) `ss`/`iperf3`
    · (7) `dig`/`nslookup`.
18. **Mirar** es ver datos sueltos; **monitorear** es plantear una **hipótesis** y
    **verificarla** con la herramienta correcta. Ej.: «¿por qué va lento?» →
    `iperf3` (¿cuánto?) + `iftop` (¿quién?).
19. P. ej. **`tcpdump`** para probar que el servicio **genera** ese tráfico, o
    **`netdata`** si se busca evidencia continua; lo importante es justificar la
    elección con la **pregunta** que responde.
20. La de **throughput/tasa de segmentos** por interfaz; se buscaría un **pico
    anómalo** sostenido que no corresponde al uso normal.

---

## 8. Autochequeo final (¿puedo dar el examen?)

- [ ] Explico por qué se segmenta una LAN (broadcast + seguridad).
- [ ] Distingo VLAN (capa 2) de subred (capa 3) y sé cuándo usar cada una.
- [ ] Nombro los tres servicios (DHCP/DNS/NAT) y su rol.
- [ ] Enumero las **tres condiciones** del router de capa 3.
- [ ] Nombro las **cinco métricas** y la herramienta de cada una.
- [ ] Interpreto `iperf3` en **TCP y UDP** (incluido el `jitter`).
- [ ] Sé qué revisar si dos contenedores del **mismo host** dan 40 ms.
- [ ] Relaciono cada capa OSI con su evidencia y su comando.

> Si marco todo, estoy listo para la práctica del **Lab 10** y el **Avance N.º 2**
> del proyecto (LAN + monitoreo con evidencia).
