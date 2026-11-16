# Teoría — Unidad III · Parte 1: LAN y monitoreo

> Contenido completo de [`Teoria-U3-Parte1-LAN-Monitoreo.pptx`](Teoria-U3-Parte1-LAN-Monitoreo.pptx) (18 diapositivas, 16:9).
> Volcado textual de la presentación: mismo contenido y mismo orden de
> lectura, sin depender de PowerPoint.
>
> Se regenera con:
> `python3 tools/dump_ppt_md.py Teoria-U3-Parte1-LAN-Monitoreo.pptx "Unidad III · Parte 1: LAN y monitoreo"`
>
> Cada diapositiva conserva sus **notas del orador** al final, en bloques
> plegables: en GitHub y en la mayoría de editores se despliegan con un clic.

## Índice

- **1.** Unidad III — Parte 1
- **2.** Qué vamos a ver en esta parte
- **3.** La LAN corporativa
- **4.** Qué es una LAN (y dónde encaja entre los tipos de red)
- **5.** Una LAN plana se degrada sola
- **6.** Segmentación en capa 2: VLAN (IEEE 802.1Q)
- **7.** Segmentación en capa 3: las subredes
- **8.** VLAN y subred no son lo mismo
- **9.** Servicio 1: DHCP (entrega de direcciones)
- **10.** Servicios 2 y 3: DNS y NAT
- **11.** El router de capa 3: une los segmentos
- **12.** Ruta de ida y ruta de vuelta
- **13.** El monitoreo de red
- **14.** Las métricas de red que importan
- **15.** Las herramientas y la pregunta que responde cada una
- **16.** Medir con TCP y con UDP no es lo mismo
- **17.** Qué se observa en cada capa del modelo OSI
- **18.** Resumen y cierre de la Parte 1

---

## 1. Unidad III — Parte 1

**UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES**

Implementación de una LAN y herramientas de monitoreo

- Tema 3.1 · Implementación de una red de área local (LAN)
- Tema 3.2 · Herramientas de monitoreo de red
- Laboratorio N.º 10 · Semana 10 · 2 sesiones

<details><summary>Notas del orador</summary>

⏱ 0-3 min · Apertura.

Presentamos la Unidad III: 5 temas (3.1 LAN, 3.2 monitoreo, 3.3 SSH,
3.4 bastión, 3.5 orquestación). La clase son 2 h 45 y se divide en 3
bloques de 55 min:
  · Parte 1 (esta): LAN + monitoreo        → Lab 10
  · Parte 2: claves SSH + bastión          → Lab 11
  · Parte 3: orquestación (Compose/Swarm)  → Lab 12
Esta parte es teoría; la práctica es el Laboratorio N.º 10 (Sesiones A y B).

</details>

---

## 2. Qué vamos a ver en esta parte

> Dos temas del programa y un objetivo: una LAN que se puede medir

| # | Tema del programa | Pregunta que responde | Min |
|---|---|---|---|
| 3.1 | Implementación de una LAN | ¿Cómo diseño una red de oficina segmentada y que funcione? | 30 |
| 3.2 | Herramientas de monitoreo | ¿Cómo sé si la red está sana o se está degradando? | 15 |
| — | Cierre y repaso | Autoevaluación y puente al Laboratorio N.º 10 | 5 |

**Idea rectora**
- Una LAN no es «un switch y todos juntos».
- Es segmentación + servicios (DHCP, DNS, NAT) + enrutamiento.
- Un segmento que nadie mide es un segmento que se cae en silencio.

**Qué NO es esta clase**
- No configuramos switches ni cableado físico.
- No repetimos VLSM: ya se vio en la Unidad II (Caso 3).
- No configuramos SNMP: lo veremos como siguiente paso.

**Conexión con lo que ya saben**
- Subredes, router entre dos redes, DNS y handshake TCP ya se usaron en los Casos 1-3.
- Hoy se integran en una LAN segmentada de verdad, y se añade la medición.

<details><summary>Notas del orador</summary>

⏱ 3-5 min · Agenda.

Objetivo 3.1/3.2 del programa (literal): 'Implementar una red de área local
funcional' y 'Aplicar herramientas de monitoreo de red'. Son estos dos bloques.
Insiste en el tiempo: si nos pasamos, se recorta la práctica, no el concepto.

</details>

---

## 3. La LAN corporativa

De la red plana a la red segmentada que aguanta el trabajo diario

- Qué es una LAN y por qué hay que segmentarla
- VLAN (capa 2) y subredes (capa 3)
- Servicios: DHCP, DNS y NAT
- El router de capa 3 y el enrutamiento

30 min

<details><summary>Notas del orador</summary>

⏱ 5-6 min · Transición a 3.1.

Anuncia el hilo: primero qué es una LAN y por qué segmentar; después cómo
se segmenta (VLAN y subredes); luego los servicios; y al final el router.

</details>

---

## 4. Qué es una LAN (y dónde encaja entre los tipos de red)

> Tema 3.1 · red de un edificio o campus, con Ethernet o Wi-Fi

| Tipo | Alcance | Tecnología típica | Capa de la LAN que usa |
|---|---|---|---|
| PAN | Personal (~10 m) | Bluetooth | — |
| LAN | Edificio / campus | Ethernet 802.3 · Wi-Fi 802.11 | 1–2 |
| CAN | Vehículos / industria | CAN bus | — |
| MAN | Ciudad | Metro Ethernet · fibra óptica | 1–3 |
| WAN | País / mundo | MPLS · SD-WAN · internet | 3 |

**Elementos de toda LAN**
- Medios: par trenzado (Cat6) y fibra · Wi-Fi en el móvil.
- Hardware: switch, punto de acceso, router, servidor.
- Topología: **estrella** (la única que se usa hoy).
- Alcance: un edificio o campus (a diferencia de MAN/WAN).

**Lo que la define técnicamente**
- Es un **dominio de broadcast** propio (capa 2).
- Los equipos se identifican por **MAC** dentro del segmento.
- Al crecer, un solo dominio de broadcast se **degrada**.
- Por eso se **segmenta** en varias LAN lógicas.

<details><summary>Notas del orador</summary>

⏱ 6-9 min · Qué es una LAN. Recapitulación de Unidad I.

Es un repaso corto. La idea clave es 'dominio de broadcast': una LAN es
un dominio de broadcast, y ese es el punto que después obliga a segmentar.
No extender: solo conectar con el siguiente tema.

</details>

---

## 5. Una LAN plana se degrada sola

> El mismo segmento para usuarios, servidores y datos

**Red plana (un solo segmento)**

- Un solo segmento = todo se ve entre sí: la base de datos queda expuesta.
- El broadcast crece con cada host y consume ancho de banda.
- Un error de configuración afecta a los 254 equipos.
- Un solo dominio de falla: si algo se cae, se cae todo.

LAN  10.0.0.0/24  ·  254 hosts  ·  un solo dominio de broadcast

**LAN segmentada (lo que se hace)**

**LAN  10.0.0.0/24**
usuarios y servicios publicados
**LAN  10.0.1.0/24**
aplicación y base de datos

dominio de
broadcast

hosts
por segmento

aislamiento
real

<details><summary>Notas del orador</summary>

⏱ 9-12 min · Por qué segmentar.

Pregunta a la clase: '200 equipos en una sola subred, ¿qué pasa si alguien
hace un ping broadcast?' (se llena la red). Que la respuesta salga de ellos.
El punto de SEGURIDAD es el que más se recuerda: en una red plana el usuario
llega directo al puerto de la base de datos. Segmentar es seguridad y rendimiento.

</details>

---

## 6. Segmentación en capa 2: VLAN (IEEE 802.1Q)

> Un switch, varias redes lógicas independientes

**La idea:** un switch físico reparte sus puertos en grupos lógicos independientes, cada uno con su propia VLAN ID.

**Cómo viaja una trama**
- El switch marca la trama con un **tag de 4 bytes** (802.1Q).
- El tag lleva la **VLAN ID** (1 a 4094).
- Un puerto **trunk** transporta varias VLAN; un puerto **access** una sola.

**VLAN 10**
Usuarios
192.168.10.0/24

**VLAN 20**
Servidores
192.168.20.0/24

**VLAN 30**
Datos
192.168.30.0/24

▲  un solo switch 802.1Q  ·  las tres VLAN están aisladas entre sí

|  | VLAN (802.1Q) | Subred IP | Red bridge del laboratorio |
|---|---|---|---|
| Capa | 2 · enlace | 3 · red | 3 · red (virtual) |
| Se configura en | Switch (trunk/access) | Host o router | docker network create |
| Aísla | El tráfico entre puertos | El tráfico L3 por diseño | Contenedores de esa red |
| Se rompe si… | El trunk no soporta el tag | Las rutas están mal | Se conecta a otra red |

<details><summary>Notas del orador</summary>

⏱ 12-20 min · VLAN. ★ BLOQUE CENTRAL

Aclaración honesta: VLAN NO es tema propio del analítico (que lista 802.3/802.11/
802.15/802.16). VLAN es 802.1Q (bridging). Se incluye porque es el tema exacto de
'segmentación' del 3.1 y da la clave mental de lo que hacen las redes bridge.

Resumen de una frase: 'separar un switch en varias redes lógicas sin comprar más switches'.
Pregunta: si dos VLAN usaran la misma subred IP, ¿funcionaría? (No: duplicar rangos
rompe el retorno; por eso nunca se superponen.)

</details>

---

## 7. Segmentación en capa 3: las subredes

> Cada segmento recibe su propio rango de direcciones IP

| Segmento | Subred | Máscara | Gateway | Hosts útiles | Qué vive ahí |
|---|---|---|---|---|---|
| Usuarios | 10.0.0.0/24 | 255.255.255.0 | 10.0.0.1 | 254 | Equipos de usuario |
| Servicios | 10.0.1.0/24 | 255.255.255.0 | 10.0.1.1 | 254 | Web y API |
| Datos | 10.0.2.0/25 | 255.255.255.128 | 10.0.2.1 | 126 | Base de datos aislada |
| Gestión | 10.0.3.0/28 | 255.255.255.240 | 10.0.3.1 | 14 | Monitoreo y administración |

**Reglas del direccionamiento**
- Se reparten del **mayor al menor**: la subred más grande primero.
- Nunca se superponen: un rango duplicado rompe el retorno.
- Se reserva un rango de **gestión** para monitoreo y acceso.

**Ventaja de segmentar en capa 3**
- El tráfico entre segmentos **pasa por el router** y se puede filtrar.
- Un problema en un segmento **no** inunda a los demás.
- La base de datos deja de ser alcanzable desde los usuarios.

segmentos

**10.0.0.0/16**
espacio privado (RFC 1918)

solapes

<details><summary>Notas del orador</summary>

⏱ 20-23 min · Direccionamiento.

NO rehacer el cálculo VLSM: ya se hizo en la Unidad II (Caso 3) y en el Avance 1.
Mostrar la tabla como ejemplo de 'presupuesto de direcciones' de una LAN de 4 segmentos.
Insistir: segmentar en capa 3 es lo que permite FILTRAR entre segmentos — ahí
está la seguridad que se busca para la base de datos. El rango de gestión conecta
con el servidor bastión de la Parte 2.

</details>

---

## 8. VLAN y subred no son lo mismo

> Una segmenta en capa 2 (switch) y la otra en capa 3 (IP/router)

| Aspecto | VLAN (802.1Q) | Subred IP |
|---|---|---|
| Capa del modelo | Enlace (2) | Red (3) |
| Se define en | El switch | El direccionamiento (IP + máscara) |
| Aísla por | Puertos del switch | Rangos de direcciones |
| Para comunicarlas se necesita | Un router (router-on-a-stick) | Un router (una interfaz por red) |
| Lo ve el usuario final | No (es transparente) | Sí (su IP y su máscara) |
| Ejemplo del laboratorio | Switch 802.1Q | docker network (red bridge) |

**Cómo se combinan en la práctica**
- Normalmente una VLAN corresponde a una subred: se aísla en capa 2 **y** en capa 3. **El router es el que las une y decide qué tráfico puede cruzar.**

<details><summary>Notas del orador</summary>

⏱ 23-26 min · VLAN vs subred.

Esta tabla responde la duda que suele quedar: VLAN (capa 2) y subred (capa 3) no
compiten, se complementan. Una VLAN por subred es el diseño típico.
Mensaje: 'la seguridad no está en aislar, sino en decidir qué cruza el router'.

</details>

---

## 9. Servicio 1: DHCP (entrega de direcciones)

> El equipo arranca sin saber nada y la red le da su configuración

**Cliente**
arranca sin IP

**DISCOVER**
busca servidor
(broadcast)

**OFFER**
el servidor
propone

**REQUEST**
el cliente
pide

**ACK**
queda
asignada

| Dato que entrega | Ejemplo | Por qué importa |
|---|---|---|
| Dirección IP | 10.0.0.50 | Identifica al equipo en la subred |
| Máscara de subred | 255.255.255.0 (/24) | Define qué es local y qué no |
| Puerta de enlace (gateway) | 10.0.0.1 | Por dónde sale hacia otras redes |
| Servidor DNS | 10.0.0.53 | Cómo resuelve los nombres |

**Detalle clave: DORA**
- DISCOVER → OFFER → REQUEST → ACK.
- El primer paquete va por **broadcast**: el cliente aún no tiene IP.

**UDP 67 (servidor) / 68 (cliente)**
- La dirección se entrega con un **lease** (préstamo).
- Al expirar, el cliente la renueva o recibe otra.

<details><summary>Notas del orador</summary>

⏱ 26-28 min · Servicios, parte 1 (DHCP).

Ya se vio DORA en el Caso 1: no reexplicar, solo confirmar el orden y el porqué
del broadcast inicial. Lo importante para la LAN: el gateway y el DNS también se
entregan por DHCP, no solo la IP.

</details>

---

## 10. Servicios 2 y 3: DNS y NAT

> Resolver nombres y salir a internet con direcciones privadas

**Cliente**
escribe un nombre
«app.local»

**DNS**
resuelve:
nombre → IP

**NAT**
traduce IP privada
→ IP pública

| Servicio | Protocolo / puerto | Qué resuelve |
|---|---|---|
| DNS | UDP/TCP 53 | Nombre → IP (registros A, CNAME, MX) |
| NAT | Tabla del router | Traduce la IP privada al salir a internet |
| NAT (DNAT) | Tabla del router | Publica un servicio interno en un puerto |

**Por qué DNS y no IPs sueltas**
- Si la IP cambia, el cliente no se entera: el **nombre no cambia**.
- Desacopla el nombre del servicio de la IP que tenga.

**NAT y las direcciones privadas**
- RFC 1918: 10/8, 172.16/12, 192.168/16 no se enrutan en internet.
- El router las traduce al salir (SNAT) y de vuelta.

<details><summary>Notas del orador</summary>

⏱ 28-31 min · Servicios, partes 2 y 3 (DNS y NAT).

El argumento fuerte del DNS interno: desacoplar nombre de IP. Eso es lo que más
tarde permite mover servicios sin tocar la configuración.
NAT: recordar que las IP privadas (RFC 1918) no se enrutan en internet; el router
las traduce. Conectar con 'por qué una LAN usa direcciones privadas'.

</details>

---

## 11. El router de capa 3: une los segmentos

> Dos interfaces, una en cada subred — el patrón de la LAN segmentada

**Un dispositivo con una interfaz por subred:**

```text
$ ip -4 -o addr show
eth0  10.0.0.1/24   ← red de usuarios
eth1  10.0.1.1/24   ← red de servicios
$ ip route
10.0.0.0/24 dev eth0
10.0.1.0/24 dev eth1
default via <proveedor>
```

**El switch no une redes; el router sí**
- Un switch (capa 2) solo mueve tramas dentro del mismo segmento.
- El router (capa 3) decide, con su tabla de rutas, a qué red va el paquete.
- Conseguir una LAN segmentada **obliga** a tener un router entre segmentos.

**Verificación del reenvío**

```text
$ cat /proc/sys/net/ipv4/ip_forward
1        # sin esto NO reenvía entre interfaces
$ ip -s link show eth0   # errores y drops
```

**Los 3 requisitos del router**
- **Reenvío IPv4 habilitado** (ip_forward=1).
- **Una interfaz por subred** (dos o más).
- **Ruta por destino** en ambos sentidos.

<details><summary>Notas del orador</summary>

⏱ 31-35 min · El router.

Idea que debe quedar: segmentar en capa 3 obliga a enrutar. El switch no cruza
segmentos; el router sí, con su tabla de rutas. Es el mismo patrón del router del
Caso 2, ahora como diseño de la LAN real.
El requisito que más se olvida es el reenvío (ip_forward). Sin él, el paquete
llega a una interfaz y no sale por la otra. La tabla de rutas (ip route) es la
herramienta de diagnóstico.

</details>

---

## 12. Ruta de ida y ruta de vuelta

> El paquete tiene que poder regresar: si no hay ruta de vuelta, no hay respuesta

**Origen**
10.0.0.10

**Gateway**
10.0.0.1
(ruta de ida)

**Router**
decide
destino

**Destino**
10.0.1.20

**Vuelta**
10.0.1.1 → 10.0.0.0/24
(ruta de vuelta)

**Qué significa «no hay ruta de vuelta»**
- El paquete llega al destino, pero el destino **no sabe cómo responder**.
- Se ve como un ping que se pierde aunque la ruta de ida exista.
- Por eso el router necesita rutas (o un default) **en los dos sentidos**.

**Cómo se diagnostica en capa 3**
- ip route → ver la tabla de rutas del equipo o router.
- ping → comprobar ida y vuelta (ICMP echo / echo reply).
- traceroute → ver por qué saltos (hops) pasa el paquete.
- arp → ver el mapeo IP ↔ MAC dentro del segmento.

**ICMP**
diagnóstico
de capa 3

**TTL**
limita los saltos
y evita bucles

solapes de red

<details><summary>Notas del orador</summary>

⏱ 35-37 min · Ruta de ida y vuelta.

Este es el error clásico de laboratorio: 'el ping no responde aunque la red
está bien'. Casi siempre falta la ruta de vuelta o el gateway. Ya se nombró en
el Caso 2; aquí se deja el concepto y las herramientas de capa 3.

</details>

---

## 13. El monitoreo de red

La parte que separa una red que «anda» de una red que se puede operar

- Qué se mide: ancho de banda, latencia, pérdida, jitter, errores
- Herramientas: tcpdump · iftop · iperf3 · netdata
- Cómo leer un resultado y sacar una conclusión

15 min

<details><summary>Notas del orador</summary>

⏱ 37-38 min · Transición a 3.2.

Frase de entrada: 'ya construimos y entendimos la LAN; ahora la miramos.
Sin medición, estás a ciegas.'

</details>

---

## 14. Las métricas de red que importan

> Si solo vas a mirar cinco cosas, que sean estas

**Mbps**
Ancho de banda
cuánto pasa

**ms**
Latencia
cuánto tarda

**%**
Pérdida
cuánto se pierde

**ms**
Jitter
cuánto varía

| Métrica | Qué mide | Valor sano en LAN | Si está mal, sospechar de… |
|---|---|---|---|
| Ancho de banda | Bits por segundo | > 100 Mbps en Gigabit | Enlace saturado · cuello de botella |
| Latencia | Tiempo de ida y vuelta | < 1 ms en la LAN | Congestión · ruta larga |
| Pérdida | Paquetes que no llegan | 0 % | Cable · switch · saturación |
| Jitter | Variación de la latencia | < 5 ms | Voz/video con cortes |
| Errores | Frames con error (CRC) o drops | 0 | Cable · conector · duplex mismatch |

**El criterio del programa (3.2)**
- **«Aplicar herramientas de monitoreo de red»**: el entregable no es la herramienta, es la evidencia de que la red responde. **El ENUNCIADO del proyecto exige tcpdump, iftop, iperf3 o netdata (mínimo 1).**

<details><summary>Notas del orador</summary>

⏱ 38-41 min · Métricas de red.

Cinco métricas: ancho de banda (¿cuánto pasa?), latencia (¿cuánto tarda?),
pérdida (¿qué se cae?), jitter (¿varía?) y errores (¿la interfaz falla?).
Insistir en la última columna: cada síntoma apunta a una causa probable.
Ejemplo: 40 ms entre dos equipos del mismo host casi siempre es virtualización,
no la red física. Monitorear es hipótesis + verificación, no solo mirar gráficas.

</details>

---

## 15. Las herramientas y la pregunta que responde cada una

> Cada una ataca una métrica distinta — no compiten

| Herramienta | Pregunta que responde | Capa | Métrica |
|---|---|---|---|
| tcpdump | ¿Qué paquetes exactos están pasando? | 2-4 | Contenido, errores |
| iftop | ¿Quién está usando la red ahora mismo? | 3-4 | Ancho de banda |
| iperf3 | ¿Cuánto ancho de banda aguanta de verdad? | 4 | Banda, jitter, pérdida |
| netdata | ¿Cómo se comporta el sistema con el tiempo? | — | Histórico (panel web) |

**Herramientas de línea de comandos**
- tcpdump captura y muestra paquetes (con -nn sin resolver nombres).
- iftop muestra el tráfico por host en tiempo real (barras).
- iperf3 abre una conexión y mide la tasa real (TCP o UDP).
- Todas se ejecutan en un equipo o servidor de la LAN.

**Además, sin instalar nada**
- ping → latencia y pérdida (ICMP).
- ip -s link → contadores de errores y drops por interfaz.
- ss → conexiones y puertos en escucha.
- dig / nslookup → verificar el DNS.

<details><summary>Notas del orador</summary>

⏱ 41-45 min · Herramientas.

No son competencia: cada una responde una pregunta distinta.
La combinación que da evidencia: tcpdump (QUÉ pasa) + iperf3 (CUÁNTO pasa) +
netdata (CÓMO evoluciona). Esa combinación es la que pide el Avance 2 del proyecto.
netdata es lo más visual: mostrar la URL :19999 en el navegador si hay tiempo.

</details>

---

## 16. Medir con TCP y con UDP no es lo mismo

> El mismo enlace se comporta distinto según el transporte

| Aspecto | TCP | UDP |
|---|---|---|
| Conexión | Orientado (handshake) | Sin conexión |
| Ante la pérdida | Retransmite y baja el caudal | Pierde y no avisa |
| Qué mide mejor | Rendimiento real | Jitter y pérdida |
| Dato clave en la salida | Mbits/sec y retransmisiones | Jitter y Lost/Total |
| Ejemplo de uso | Web, SSH, base de datos | DNS, voz, video, juegos |

**Lo que enseña el resultado**
- Si suben las retransmisiones en TCP → hay pérdida (y el caudal baja).
- Si sube el jitter en UDP → la voz/video se corta aunque no haya pérdida.

**Por qué importa para la LAN**
- Mismo medio, distinto resultado: el transporte cambia la medición.
- Por eso una métrica sola no basta para decir «la red está bien».

<details><summary>Notas del orador</summary>

⏱ 45-49 min · TCP vs UDP (iperf3).

Enlaza con la teoría de transporte de la Unidad II. Mensaje clave: TCP se adapta
(retransmite, baja el caudal); UDP pierde y no avisa.
Si hay laboratorio levantado, correr iperf3 en vivo es lo que más convence.
El jitter es la métrica que decide si una videollamada se oye bien.

</details>

---

## 17. Qué se observa en cada capa del modelo OSI

> El monitoreo no es solo «paquetes»: cada capa tiene su evidencia

| Capa | Qué se observa | Con qué |
|---|---|---|
| 1 · Física | Señal, errores de transmisión, drops | ip -s link |
| 2 · Enlace | Tramas, direcciones MAC, FCS | tcpdump, arp |
| 3 · Red | IP, rutas, ICMP (ping/traceroute) | ping, ip route, traceroute |
| 4 · Transporte | Puertos, TCP/UDP, retransmisiones, jitter | ss, tcpdump, iperf3 |
| 7 · Aplicación | HTTP/HTTPS, DNS, tiempos de respuesta | curl, dig, panel web |

**El método (no la herramienta) es lo importante**
- 1. Definir el síntoma: ¿lento, intermitente, no conecta?
- 2. Formular una hipótesis de capa: ¿física, enlace, red, transporte o aplicación?
- 3. Medir con la herramienta de esa capa y comparar contra el valor sano.
- 4. Concluir y, si aplica, corregir; volver a medir para confirmar.

<details><summary>Notas del orador</summary>

⏱ 49-52 min · Monitoreo por capas.

Este cuadro es la síntesis de la clase de monitoreo: conecta el modelo OSI con
las herramientas. Que el estudiante se lleve el MÉTODO, no una lista de comandos.
Ejemplo de hipótesis: 'no resuelve nombres' → capa 7 (DNS); 'no conecta a un
puerto' → capa 4 (ss/telnet); 'todo lento' → capa 1/3.

</details>

---

## 18. Resumen y cierre de la Parte 1

> Qué debe quedar claro antes de ir al Laboratorio N.º 10

**Ideas clave (3.1 + 3.2)**
- Una LAN es un dominio de broadcast: se **segmenta** para escalar y asegurar.
- Se segmenta en capa 2 (**VLAN**) y en capa 3 (**subredes**).
- DHCP, DNS y NAT son los servicios mínimos.
- El **router** une los segmentos y decide qué tráfico cruza.
- Se monitorea para **actuar**: banda, latencia, pérdida, jitter, errores.

**Puente hacia la Parte 2**
- Administrar la LAN exige entrar a esos servidores…
- …pero **con contraseña no se escala y no es seguro**.
- Parte 2: claves SSH (3.3) + servidor bastión (3.4).
- El bastión vive en el segmento de administración.

**Preguntas de autoevaluación (sal de clase sabiendo responderlas)**
1. ¿Por qué una red plana es un problema de seguridad además de rendimiento?
2. ¿Qué tres condiciones debe cumplir un equipo para hacer de router entre dos redes?
3. Diferencia entre VLAN y subred: ¿qué capa resuelve cada una?
4. Si ves 40 ms de latencia entre dos equipos del mismo host, ¿qué revisas primero?
5. ¿Qué herramienta usarías para demostrar que la red sostiene 100 Mbps y cuál para ver quién los consume?

<details><summary>Notas del orador</summary>

⏱ 52-55 min · Cierre de la Parte 1.

Las 5 preguntas son el pretexto del parcial y del Laboratorio N.º 10.
Respuestas guía: (1) exposición directa a servicios internos como la base de datos;
(2) reenvío habilitado, una interfaz por subred, ruta en ambos sentidos;
(3) VLAN = capa 2, subred = capa 3; (4) el jitter; (5) TCP se adapta (retransmite),
UDP pierde y no avisa.
Pedir 2 respuestas en voz alta y anunciar el puente a la Parte 2 (SSH y bastión).

</details>

---

