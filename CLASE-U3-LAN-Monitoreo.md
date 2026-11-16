# Clase — Unidad III · 3.1 LAN y 3.2 Monitoreo (guion docente)

> **Punto del módulo:** arranque de la **Unidad III**. Cubre los **temas 3.1
> (implementación de una LAN)** y **3.2 (herramientas de monitoreo)** del
> programa analítico — semana 10 del `CRONOGRAMA.md`.
>
> **Materiales que acompaña:** presentación `Teoria-U3-Parte1-LAN-Monitoreo.pptx`
> (generada por `tools/build_parte1.py`; versión en texto en
> `TEORIA-U3-Parte1-LAN-Monitoreo.md`), laboratorio
> `Laboratorio-10-LAN-Monitoreo-Docker` (`SESION-A.md` y `SESION-B.md`),
> `GUIA-CLASE-UNIDAD-III.md` y la guía del estudiante
> `GUIA-ESTUDIO-U3-LAN-Monitoreo.md`.
>
> **Objetivo en una frase:** que el estudiante pase de «una red que anda» a
> **una LAN segmentada, con servicios, que se puede medir y diagnosticar**.

---

## 1. Ficha de la clase

| Campo | Valor |
|-------|-------|
| Unidad | III — Implementación de LAN y orquestación de aplicaciones |
| Temas | 3.1 Implementación de una LAN · 3.2 Herramientas de monitoreo |
| Semana | 10 (dos clases) |
| Laboratorio | N.º 10 — Clase 1: 10A (LAN) · Clase 2: 10B (enrutamiento + monitoreo) |
| Duración | Teoría 55 min + 2 sesiones prácticas (≈2 h 45 min cada una) |
| Entregable del lab | 100 pts (Sesión A 50 + Sesión B 50) |
| Insumo para el proyecto | **Avance N.º 2** (LAN + monitoreo, 10 %) |

### Objetivos de aprendizaje

Al terminar el punto, el estudiante debe poder:

1. **Explicar** por qué una LAN plana se degrada (broadcast, seguridad, un solo
   dominio de falla) y qué cambia al **segmentarla** en subredes/VLAN.
2. **Identificar** los tres servicios mínimos de una LAN (**DHCP, DNS, NAT**) y
   su rol dentro de la red.
3. **Describir** el patrón del **router dual-homed** (dos interfaces, una por
   subred) y las **tres condiciones** para que reenvíe tráfico.
4. **Elegir** la métrica correcta (**ancho de banda, latencia, pérdida,
   errores**) y la herramienta correcta (**tcpdump, iftop, iperf3, netdata**)
   para responder una pregunta concreta.
5. **Construir y medir** una LAN segmentada en Docker con evidencia reproducible.

### Requisitos previos (lo que ya vieron)

| Ya visto en… | Concepto que se reutiliza |
|--------------|---------------------------|
| Unidad I | LAN, switch, estrella, Ethernet |
| Caso 1 (ECOSISTEMA) | DNS interno (`dnsmasq`), HTTP/HTTPS, trama |
| Caso 2 | TCP/UDP, `tc netem`, router entre 2 subredes, ruta de vuelta |
| Caso 3 | VLSM, base de datos aislada, monitoreo básico |

> **Regla de oro del docente:** de todo lo anterior, **no reexplicar**. Esta
> clase no repite VLSM ni DORA; los **usa como vocabulario** para hablar de una
> LAN real. Si se repiten temas viejos, no alcanza el tiempo.

---

## 2. Materiales y preparación previa (30 min antes)

### En el host (docente)

```bash
# Imágenes que conviene tener ya descargadas (evita perder clase esperando red)
docker pull nginx:alpine
docker pull postgres:15-alpine
docker pull alpine
docker pull netdata/netdata:latest
docker pull mlabbe/iperf3
docker pull jpillora/dnsmasq

# Verificar Docker y limpiar restos de pruebas anteriores
docker ps
docker network prune -f
```

### En la pizarra / pantalla

- Un **diagrama de LAN plana** (un solo 10.0.0.0/24) y, al lado, la **LAN
  segmentada** (pública / interna / datos / administración).
- La tabla de **métricas vs. herramientas** (sección 4) — dejarla visible durante
  toda la parte de monitoreo.

### Puntos de control (checkpoints) que se van a pedir

1. `docker network ls` con `publica` e `interna`.
2. `docker exec router-corp ip addr` con **dos interfaces**.
3. `nslookup web.local` / `nslookup app.local` resolviendo.
4. Captura de `tcpdump` + resultado de `iperf3` (TCP y UDP).
5. Panel de `netdata` con una gráfica actualizándose.

---

## 3. Estructura de la clase (dos formas de dictarla)

El punto de LAN y monitoreo se puede dar como **una clase teórica de 55 min** y
luego **dos prácticas**, o todo integrado. Ambas formas usan el mismo material.

### Opción 1 — Clase teórica (55 min) + prácticas aparte

| Bloque | Min | Qué se hace |
|--------|-----|-------------|
| Teoría 3.1 + 3.2 | 55 | Presentación `Teoria-U3-Parte1-LAN-Monitoreo.pptx` (diapositivas 1-18) |
| Sesión A | ≈120-165 | Lab 10A: construir la LAN (Docker) |
| Sesión B | ≈120-165 | Lab 10B: enrutar + monitorear |

### Opción 2 — Bloque semanal (2 clases de 2 h 45 min)

| Clase | Min | Qué se hace |
|-------|-----|-------------|
| **Clase 1** | 55 + 110 | Teoría 3.1 (LAN) + **Sesión A** (construir la LAN) |
| **Clase 2** | 55 + 110 | Teoría 3.2 (monitoreo) + **Sesión B** (enrutar + medir) |

> El resto de este documento se lee **bloque por bloque**, así que sirve para
> cualquiera de las dos opciones.

---

## 4. Guion teoría — Tema 3.1 y 3.2 (55 min)

> Alineado con las **notas del presentador** del PPT (que ya traen el minuto de
> cada diapositiva). Aquí está el *cómo contarlo*, no el texto de cada
> diapositiva.

### Encuadre (0-5 min)

- Presentar que la Unidad III tiene **5 temas** y que hoy son los **dos
  primeros**: la LAN (3.1) y el monitoreo (3.2).
- Frase para abrir: *«En los Casos 1-3 ya hicieron una red que funciona. Hoy la
  volvemos una red de oficina de verdad: segmentada, con servicios, y medida.»*
- Aclarar el **contrato de tiempo**: son 55 min; si nos pasamos, se recorta la
  práctica, no el concepto.

### 3.1 · La LAN corporativa (5-37 min)

| Min | Diapositiva / tema | Cómo contarlo |
|-----|--------------------|---------------|
| 5-6 | Transición a 3.1 | Anunciar el hilo: qué es una LAN → por qué segmentar → cómo se segmenta (VLAN y subredes) → servicios → router. |
| 6-9 | **Qué es una LAN** | Repaso de 3 min de Unidad I (medios, hardware, topología estrella). Idea clave: una LAN es un **dominio de broadcast**. No extenderse. |
| 9-12 | **Una LAN plana se degrada sola** | Preguntar *«200 equipos en una sola subred, ¿qué pasa si alguien hace ping broadcast?»*. Dejar que la clase responda: se llena la red. Gancho de seguridad: en red plana el usuario llega **directo al puerto de la DB**. |
| **12-20** | **VLAN (802.1Q)** | Aclarar con honestidad: VLAN **no** es tema propio del analítico (802.1Q ≠ 802.3/802.11), se incluye porque es el tema exacto de *segmentación* y **puente** hacia las redes bridge del laboratorio. Idea: un switch reparte sus puertos en grupos lógicos independientes. Pregunta: *¿dos VLAN con la misma subred IP funcionarían?* (No: rompe el retorno). |
| 20-23 | **Subredes (capa 3)** | **No rehacer el VLSM** (ya está en la Unidad II / Caso 3). Mostrar la tabla como «presupuesto de direcciones» de 4 segmentos. Presentar el **/28 de gestión**: la red por la que se monitorea y se entra por SSH. |
| 23-26 | **VLAN vs subred** | Responder la duda que suele quedar: VLAN = capa 2 (switch), subred = capa 3 (IP/router); no compiten, se complementan. El router decide qué tráfico cruza. |
| 26-28 | DHCP (DORA) | Conectar con el Caso 1 (ya usaron `dnsmasq`). DORA ya lo saben: solo confirmar el orden. Lo clave: **el gateway y el DNS también se entregan por DHCP**. |
| 28-31 | DNS y NAT | Argumento fuerte del DNS interno: **desacopla el nombre de la IP**. NAT: las IP privadas (RFC 1918) no se enrutan en internet; el router las traduce. |
| 31-35 | **El router de capa 3** | Es el mismo patrón del router del Caso 2, ahora como diseño de la LAN. Los **3 requisitos**: `ip_forward=1`, una interfaz por subred, ruta en ambos sentidos. El que más olvidan es `ip_forward`. |
| 35-37 | **Ruta de ida y vuelta** | Error clásico: «el ping no responde aunque la red está bien» → casi siempre falta la ruta de vuelta o el gateway. Ya se nombró en el Caso 2; aquí se deja el concepto y las herramientas de capa 3. |

### 3.2 · El monitoreo (37-55 min)

| Min | Diapositiva / tema | Cómo contarlo |
|-----|--------------------|---------------|
| 37-38 | Transición a 3.2 | *«Ya construimos y entendimos la LAN; ahora la miramos. Sin esto, estás a ciegas.»* |
| 38-41 | **Las cinco métricas** | Ancho de banda, latencia, pérdida, jitter y errores. Dejar claro que monitorear **no es mirar**: es *hipótesis + verificación*. Ejemplo: 40 ms entre dos contenedores del **mismo host** no es la red física. Mencionar que el **ENUNCIADO** exige tcpdump/iftop/iperf3/netdata (mínimo 1). |
| 41-45 | **Las herramientas** | tcpdump ya la conocen (no gastar tiempo). Enfocarse en **iperf3** y **netdata**, que son nuevas. Cerrar con la combinación: tcpdump **qué**, iperf3 **cuánto**, netdata **cómo evoluciona**. |
| 45-49 | **iperf3: TCP vs UDP** | Si hay Docker levantado, **correrlo en vivo** (es rápido y convence). Mensaje clave: **TCP se adapta** (retransmite y baja el caudal); **UDP pierde y no avisa** (`Lost`, `jitter`). |
| 49-52 | **Monitoreo por capas (OSI)** | Síntesis: cada capa tiene su evidencia (1 `ip -s link`, 2 `tcpdump`, 3 `ping`/`traceroute`, 4 `ss`/`iperf3`, 7 `dig`). Que se lleven el **método**, no la lista de comandos. |
| 52-55 | Cierre y autoevaluación | Hacer 2 de las 5 preguntas en voz alta (sección 7) antes de pasar a la práctica. |

### Tabla de referencia para pizarra (métricas ↔ herramientas)

| Métrica | Se mide con | Valor sano (LAN) | Si está mal, sospechar de… |
|---------|-------------|------------------|----------------------------|
| Ancho de banda | `iperf3` | >100 Mbps en Gigabit | Enlace saturado · cuello de botella |
| Latencia | `ping` / ICMP | <1 ms en la LAN | Congestión · ruta larga |
| Pérdida | `ping` · `iperf3 -u` | 0 % | Cable · switch · saturación |
| Jitter | `iperf3 -u` | <5 ms | Voz/video con cortes |
| Errores | `ip -s link` | 0 CRC / 0 drops | Cable · conector · duplex mismatch |

---

## 5. Guion práctica — Sesión A: construir la LAN (10A)

**Meta:** dejar la red funcionando y **capturar los checkpoints 1-3**.
**Tiempo sugerido:** 15 min demo guiada + 60-90 min trabajo + 15 min cierre.

| Min | Etapa | Qué hace el docente / el estudiante |
|-----|-------|-------------------------------------|
| 0-10 | Encuadre + paso 1-2 en vivo | Crear `publica` e `interna`, levantar `router-corp` y sus dos `network connect`. Proyectar `ip addr` para mostrar las 2 interfaces. |
| 10-25 | Paso 3-4 guiados | Publicar `web-srv` (nginx) en `publica` y `db-srv` (postgres) en `interna`. Verificar `curl` y `docker logs … ready`. |
| 25-55 | Paso 5 (app flask) | Construir la app que llama a `web-srv` y `db-srv` **por nombre**. Es el momento donde "la red" se vuelve útil. |
| 55-75 | Paso 6 (DNS dnsmasq) | Levantar `dns-corp` y validar `nslookup web.local` / `app.local`. |
| 75-90 | Pregunta 3 + evidencias | `app-srv` alcanza `web-srv` y `db-srv` por nombre. Cerrar con las capturas del entregable. |

### Comandos núcleo (Si el estudiante se pierde, dictarlos)

```bash
# Segmentos de la LAN
docker network create publica --subnet 10.0.0.0/24 --gateway 10.0.0.1
docker network create interna --subnet 10.0.1.0/24 --gateway 10.0.1.1

# Router dual-homed
docker run -d --name router-corp --cap-add=NET_ADMIN alpine sleep 3600
docker network connect publica router-corp
docker network connect interna router-corp
docker exec router-corp ip addr show
```

### Preguntas de la Sesión A (con la respuesta esperada)

1. ¿Cuántas interfaces tiene `router-corp`? ¿Qué IP tiene en cada red?
   → **Dos**: una en `10.0.0.0/24` (pública) y otra en `10.0.1.0/24` (interna).
2. ¿Qué registros creaste (`A`)? ¿Cómo resolvería `app.local`?
   → Registros **A** en `dnsmasq`; `app.local` apunta a la IP de `app-srv`.
3. ¿Por qué se puede llamar a `web-srv`/`db-srv` **por nombre**?
   → Por el **DNS interno** (en el lab, `dnsmasq`); el nombre desacopla la IP.

> **Error típico a vigilar:** `app-srv` solo queda en `interna` si se omite el
> `docker network connect publica app-srv` después de levantarlo. Sin eso, no
> resuelve por el DNS que vive en la red pública.

---

## 6. Guion práctica — Sesión B: enrutar y monitorear (10B)

**Meta:** hacer **explícito** el enrutamiento y **medir** con las 4 herramientas.
**Tiempo sugerido:** 15 min paso 1-2 + 75 min pasos 3-6 + 15 min integración.

| Min | Etapa | Qué demuestra |
|-----|-------|---------------|
| 0-15 | Pasos 1-2: conectividad + ruta explícita | `app→web` funciona, `web→app` no; añadir `ip route add 10.0.1.0/24 via 10.0.0.2` y comprobar con `ping`. |
| 15-35 | Paso 3: `tcpdump` | Capturar tráfico real y **clasificarlo por capa** (TCP/80, ICMP, etc.). |
| 35-50 | Paso 4: `iftop` | Ver **quién** consume la red **en vivo** (barras por host). |
| 50-75 | Paso 5: `iperf3` | Ancho de banda **TCP vs UDP**: `Mbits/sec`, `Retr`, `jitter`, `Lost`. |
| 75-90 | Paso 6-7: `netdata` + integración | Gráficas históricas + el flujo completo `/`, `/web`, `/db` de `app-srv`. |

### Comandos núcleo

```bash
# Ruta explícita (lo que Docker ya hacía por debajo)
docker exec web-srv ip route add 10.0.1.0/24 via 10.0.0.2 2>/dev/null
docker exec web-srv ping -c 2 10.0.1.2

# tcpdump
docker exec web-srv sh -c "apk add --no-cache tcpdump -q"
docker exec web-srv tcpdump -i eth0 -nn -c 15 any port 80 or icmp

# iperf3 (servidor en interna, cliente para medir)
docker run -d --name iperf-srv --network interna -p 5201:5201 mlabbe/iperf3 -s
docker run --rm --network interna mlabbe/iperf3 -c iperf-srv -t 5
docker run --rm --network interna mlabbe/iperf3 -c iperf-srv -t 5 -u -b 100M
```

### Preguntas de la Sesión B (con la respuesta esperada)

1. ¿Qué peticiones funcionan y cuáles no? → `app→web` sí (comparte red);
   `web→app` no hasta añadir la ruta.
2. ¿Qué muestra `ip route` y qué rol cumple la **ruta de vuelta**? → La ruta
   hacia `10.0.1.0/24`; sin ella el paquete va pero **no regresa**.
3. ¿Qué protocolos/puertos ves en `tcpdump`? → TCP/80 (aplicación), ICMP (red).
4. ¿Par IP:puerto con más tráfico en `iftop`? ¿Ancho de banda máximo?
5. `iperf3` TCP vs UDP: ¿qué es el `jitter`? → Variación del retardo; clave para
   **videollamadas** (UDP tolera algo de pérdida, pero no jitter alto).
6. En `netdata`, ¿qué gráfica muestra la tasa de segmentos? ¿Cómo ayudaría a
   detectar una fuga o un DDoS?
7. Completar el diagrama del flujo de la petición.
8. Diseño: proponer el esquema de la app de inventarios y justificar **qué
   herramienta** de monitoreo elegirían.

> **Error típico a vigilar:** `iperf3` necesita el binario en el contenedor. Con
> `mlabbe/iperf3` ya viene; si se usa `alpine`, hay que `apk add --no-cache iperf3`.
> Y el `iperf-srv` debe estar en la **misma red** que el cliente para medir sin NAT.

---

## 7. Autoevaluación / salida de clase

Preguntas que el estudiante debe poder responder **antes de irse**:

1. ¿Por qué una red plana es un problema de **seguridad** además de rendimiento?
2. ¿Qué **tres condiciones** debe cumplir un contenedor para hacer de router
   entre dos redes?
3. Diferencia entre **VLAN** y **subred**: ¿qué capa resuelve cada una?
4. La red local marca **40 ms** de latencia entre dos contenedores del **mismo
   host**. ¿Qué revisas primero?
5. ¿Qué herramienta usarías para demostrar que la red sostiene **100 Mbps**, y
   cuál para ver **quién los consume**?

**Respuestas guía:** (1) exposición directa a servicios internos como la DB;
(2) `ip_forward=1`, una interfaz por subred, ruta en ambos sentidos; (3) VLAN =
capa 2 (switch), subred = capa 3 (IP/router); (4) el puente de Docker o un
`netem` de otro lab, no la red física; (5) `iperf3` y `iftop`/`netdata`.

---

## 8. Errores frecuentes y cómo resolverlos en clase

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| El router no reenvía entre redes | Falta `net.ipv4.ip_forward=1` | Recrear con `--sysctl net.ipv4.ip_forward=1` (o `docker exec … sysctl -w`) |
| `pool overlaps with other one on this address space` | Subred mal calculada / solapada | Revisar el VLSM; cambiar el rango y recrear la red |
| `app-srv` no resuelve `web-srv` | No está conectado a `publica` | `docker network connect publica app-srv` |
| `tcpdump` vacío | Se captura en la interfaz equivocada | Usar `-i eth0` y generar tráfico en la otra terminal |
| `iperf3` no conecta | Cliente y servidor en redes distintas | Levantar el cliente con `--network interna` |
| `netdata` no abre en `:19999` | Faltan `SYS_PTRACE` o volúmenes `/proc` `/sys` | Usar el `docker run` completo de `SESION-B.md` |
| `nslookup` no responde | Se consulta al DNS del host | Pasar `--dns <ip-de-dns-corp>` al contenedor de prueba |

---

## 9. Conexión con el resto del curso

- **Hacia atrás (lo que ya saben):** Casos 1-3 del ECOSISTEMA (DNS interno,
  TCP/UDP, VLSM, DB aislada) son el vocabulario de esta clase.
- **Hacia adelante (Parte 2 de la unidad):** administrar esta LAN exige **entrar
  a los servidores**; y con contraseña no se escala ni es seguro → **claves SSH
  (3.3) y servidor bastión (3.4)**. El bastión es, conceptualmente, **el segmento
  de administración** que ya se mencionó aquí.
- **Hacia el proyecto:** lo construido hoy es exactamente el **Avance N.º 2**
  (LAN en Docker + DNS + monitoreo con evidencia). Recordar que el ENUNCIADO
  exige **evidencia de tcpdump/iftop/netdata (mínimo 1)**.

---

## 10. Checklist rápido antes de salir del aula

- [ ] Redes `publica` e `interna` creadas y visibles en `docker network ls`.
- [ ] `router-corp` con **dos** interfaces.
- [ ] `web-srv`, `db-srv`, `app-srv` funcionando.
- [ ] DNS interno resolviendo `web.local` y `app.local`.
- [ ] Ruta explícita entre subredes probada con `ping`.
- [ ] Capturas de `tcpdump` y `iftop`.
- [ ] Resultados de `iperf3` en **TCP y UDP** con interpretación.
- [ ] Panel de `netdata` con al menos una gráfica.
- [ ] Respuestas a las preguntas de Sesión A (1-3) y Sesión B (1-8).

---

## 11. Limpieza (recordar al cierre)

```bash
docker rm -f router-corp web-srv db-srv app-srv dns-corp iperf-srv monit
docker network rm publica interna
```

---

## 12. Recursos externos recomendados (lecturas de apoyo)

> Lecturas **opcionales** para el estudiante que quiera profundizar, del blog
> [DevOpsCube](https://devopscube.com/blog/). Se listan solo las que se relacionan
> **directamente** con los temas 3.1 y 3.2, con el **momento exacto de la clase**
> donde conviene mencionarlas.

| # | Recurso | Se conecta con… | Momento de la clase |
|---|---------|-----------------|---------------------|
| 1 | [Linux networking troubleshooting commands](https://devopscube.com/list-linux-networking-troubleshooting-and-commands-beginners/) | Comandos por capa de la 3.2 | **Monitoreo por capas OSI** (49-52 min) |
| 2 | [Best open-source monitoring tools](https://devopscube.com/best-opensource-monitoring-tools/) | Panorama más allá de `netdata` | **Las herramientas** (41-45 min) |
| 3 | [Monitor Docker containers](https://devopscube.com/monitor-docker-containers-guide/) | Observabilidad del laboratorio en Docker | Cierre / práctica de la **Sesión B** |
| 4 | [iptables tutorial for beginners](https://devopscube.com/iptables-tutorial-beginners/) | Firewall entre segmentos (contexto de la 3.1) | Bloque de **segmentación** (12-26 min) |

**Cierre sugerido (1 min al final del tema 3.2):** *«Si quieren seguir, el blog de
DevOpsCube tiene la lista de herramientas de monitoreo y el tutorial de `iptables`
que vimos por encima; son el paso natural después de esta clase.»*

**Para las Partes 2 y 3 de la unidad** (mismo blog, apoyo opcional):

- Claves SSH y bastión → [Generate SSH key pair](https://devopscube.com/generate-ssh-key-pair/).
- Orquestación (3.5) → [Docker Swarm cluster](https://devopscube.com/how-to-setup-and-configure-docker-swarm-cluster/)
  y [container clustering tools](https://devopscube.com/docker-container-clustering-tools/).
- Proxy y red multi-host → [Setup a proxy server](https://devopscube.com/setup-and-configure-proxy-server/)
  y [Docker multi-host networking](https://devopscube.com/docker-multi-host-networking-tutorial/).

---

**Referencias**

- `Teoria-U3-Parte1-LAN-Monitoreo.pptx` — presentación de la clase (Parte 1).
- `TEORIA-U3-Parte1-LAN-Monitoreo.md` — versión en texto (con notas del orador).
- `GUIA-ESTUDIO-U3-LAN-Monitoreo.md` — guía de estudio del estudiante (repaso + banco de preguntas).
- `GUIA-CLASE-UNIDAD-III.md` — reparto de las 3 partes y notas de uso.
- `Laboratorio-10-LAN-Monitoreo-Docker/` — prácticas (`SESION-A.md`, `SESION-B.md`).
- `Proyecto-Semestral/ENUNCIADO.md` — Avance N.º 2 (LAN + monitoreo).
- Forouzan, B. *Transmisión de datos y redes de comunicación* · Kurose & Ross,
  *Computer Networking: A Top-Down Approach*.
