"""Unidad III · Parte 1 — La LAN y el monitoreo (temas 3.1 y 3.2) · 55 min.

Presentación ENFOCADA EN REDES DE COMPUTADORAS: capas, direccionamiento,
segmentación (VLAN y subredes), servicios (DHCP/DNS/NAT), el router de capa 3
y las métricas/herramientas de monitoreo. El laboratorio (Docker) se menciona
solo como práctica, no es el eje del contenido.

Genera: Teoria/Teoria-U3-Parte1-LAN-Monitoreo.pptx
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ppt_kit import *  # noqa

PART = "Parte 1 · LAN y monitoreo"
MIN = "55 min"


def build(out):
    prs = new_deck()
    n = 0

    # ------------------------------------------------------------- 1 portada
    s = cover(prs, "UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES",
              "Unidad III — Parte 1",
              "Implementación de una LAN y herramientas de monitoreo",
              ["Tema 3.1 · Implementación de una red de área local (LAN)",
               "Tema 3.2 · Herramientas de monitoreo de red",
               "Laboratorio N.º 10 · Semana 10 · 2 sesiones"],
              "Parte 1 de 3", "2 h 45 min de clase (3 partes de 55 min)")
    notes(s, "⏱ 0-3 min · Apertura.\n\n"
             "Presentamos la Unidad III: 5 temas (3.1 LAN, 3.2 monitoreo, 3.3 SSH,\n"
             "3.4 bastión, 3.5 orquestación). La clase son 2 h 45 y se divide en 3\n"
             "bloques de 55 min:\n"
             "  · Parte 1 (esta): LAN + monitoreo        → Lab 10\n"
             "  · Parte 2: claves SSH + bastión          → Lab 11\n"
             "  · Parte 3: orquestación (Compose/Swarm)  → Lab 12\n"
             "Esta parte es teoría; la práctica es el Laboratorio N.º 10 (Sesiones A y B).")

    # ------------------------------------------------------------- 2 agenda
    n += 1
    s = content(prs, "Qué vamos a ver en esta parte", "Dos temas del programa y un objetivo: una LAN que se puede medir", PART, n + 1)
    table(s, [["#", "Tema del programa", "Pregunta que responde", "Min"],
              ["3.1", "Implementación de una LAN", "¿Cómo diseño una red de oficina segmentada y que funcione?", "30"],
              ["3.2", "Herramientas de monitoreo", "¿Cómo sé si la red está sana o se está degradando?", "15"],
              ["—", "Cierre y repaso", "Autoevaluación y puente al Laboratorio N.º 10", "5"]],
          0.45, 1.45, 12.4, col_w=[0.8, 3.6, 7.0, 1.0], size=13, row_h=0.5)
    callout(s, 0.45, 3.75, 6.1, 1.7, "Idea rectora", [
        "Una LAN no es «un switch y todos juntos».",
        "Es segmentación + servicios (DHCP, DNS, NAT) + enrutamiento.",
        "Un segmento que nadie mide es un segmento que se cae en silencio."], ORANGE, 12.5)
    callout(s, 6.78, 3.75, 6.1, 1.7, "Qué NO es esta clase", [
        "No configuramos switches ni cableado físico.",
        "No repetimos VLSM: ya se vio en la Unidad II (Caso 3).",
        "No configuramos SNMP: lo veremos como siguiente paso."], TEAL, 12.5)
    callout(s, 0.45, 5.65, 12.4, 1.05, "Conexión con lo que ya saben", [
        "Subredes, router entre dos redes, DNS y handshake TCP ya se usaron en los Casos 1-3.",
        "Hoy se integran en una LAN segmentada de verdad, y se añade la medición."],
        ORANGE, 12.5)
    notes(s, "⏱ 3-5 min · Agenda.\n\n"
             "Objetivo 3.1/3.2 del programa (literal): 'Implementar una red de área local\n"
             "funcional' y 'Aplicar herramientas de monitoreo de red'. Son estos dos bloques.\n"
             "Insiste en el tiempo: si nos pasamos, se recorta la práctica, no el concepto.")

    # ------------------------------------------------------------- 3 divider 3.1
    n += 1
    s = divider(prs, "3.1", "La LAN corporativa", "De la red plana a la red segmentada que aguanta el trabajo diario",
                ["Qué es una LAN y por qué hay que segmentarla",
                 "VLAN (capa 2) y subredes (capa 3)",
                 "Servicios: DHCP, DNS y NAT",
                 "El router de capa 3 y el enrutamiento"], "30 min")
    notes(s, "⏱ 5-6 min · Transición a 3.1.\n\n"
             "Anuncia el hilo: primero qué es una LAN y por qué segmentar; después cómo\n"
             "se segmenta (VLAN y subredes); luego los servicios; y al final el router.")

    # ------------------------------------------------------------- 4 qué es una LAN
    n += 1
    s = content(prs, "Qué es una LAN (y dónde encaja entre los tipos de red)", "Tema 3.1 · red de un edificio o campus, con Ethernet o Wi-Fi", PART, n + 1)
    table(s, [["Tipo", "Alcance", "Tecnología típica", "Capa de la LAN que usa"],
              ["PAN", "Personal (~10 m)", "Bluetooth", "—"],
              ["LAN", "Edificio / campus", "Ethernet 802.3 · Wi-Fi 802.11", "1–2"],
              ["CAN", "Vehículos / industria", "CAN bus", "—"],
              ["MAN", "Ciudad", "Metro Ethernet · fibra óptica", "1–3"],
              ["WAN", "País / mundo", "MPLS · SD-WAN · internet", "3"]],
          0.45, 1.45, 12.4, col_w=[1.3, 3.0, 4.9, 3.2], size=12.5, row_h=0.42)
    callout(s, 0.45, 4.35, 6.1, 2.15, "Elementos de toda LAN", [
        "Medios: par trenzado (Cat6) y fibra · Wi-Fi en el móvil.",
        "Hardware: switch, punto de acceso, router, servidor.",
        "Topología: **estrella** (la única que se usa hoy).",
        "Alcance: un edificio o campus (a diferencia de MAN/WAN)."], ORANGE, 12.5)
    callout(s, 6.78, 4.35, 6.1, 2.15, "Lo que la define técnicamente", [
        "Es un **dominio de broadcast** propio (capa 2).",
        "Los equipos se identifican por **MAC** dentro del segmento.",
        "Al crecer, un solo dominio de broadcast se **degrada**.",
        "Por eso se **segmenta** en varias LAN lógicas."], TEAL, 12.5)
    notes(s, "⏱ 6-9 min · Qué es una LAN. Recapitulación de Unidad I.\n\n"
             "Es un repaso corto. La idea clave es 'dominio de broadcast': una LAN es\n"
             "un dominio de broadcast, y ese es el punto que después obliga a segmentar.\n"
             "No extender: solo conectar con el siguiente tema.")

    # ------------------------------------------------------------- 5 LAN plana
    n += 1
    s = content(prs, "Una LAN plana se degrada sola", "El mismo segmento para usuarios, servidores y datos", PART, n + 1)
    text(s, 0.45, 1.35, 5.9, 0.3, "Red plana (un solo segmento)", size=14, color=NAVY, bold=True)
    rect(s, 0.45, 1.75, 5.9, 1.0, LIGHT)
    text(s, 0.6, 1.87, 5.6, 0.85, "LAN  10.0.0.0/24  ·  254 hosts  ·  un solo dominio de broadcast",
         size=12.5, color=TEXT, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 0.45, 3.0, 5.9, 0.3, "LAN segmentada (lo que se hace)", size=14, color=NAVY, bold=True)
    rect(s, 0.45, 3.4, 5.9, 1.6, LIGHT)
    text(s, 0.6, 3.53, 5.6, 1.45,
         [[("LAN  10.0.0.0/24", {"size": 12.5, "bold": True, "color": NAVY})],
          [("   usuarios y servicios publicados", {"size": 11.5, "color": TEXT})],
          [("LAN  10.0.1.0/24", {"size": 12.5, "bold": True, "color": NAVY})],
          [("   aplicación y base de datos", {"size": 11.5, "color": TEXT})]], space=2)
    bullets(s, ["Un solo segmento = todo se ve entre sí: la base de datos queda expuesta.",
                "El broadcast crece con cada host y consume ancho de banda.",
                "Un error de configuración afecta a los 254 equipos.",
                "Un solo dominio de falla: si algo se cae, se cae todo."],
            6.75, 1.75, 6.1, size=13.5, gap=11, h=2.6)
    kpi(s, [("1", "dominio de\nbroadcast"), ("254", "hosts\npor segmento"), ("0", "aislamiento\nreal")],
        6.75, 4.6, 6.1, h=1.2)
    notes(s, "⏱ 9-12 min · Por qué segmentar.\n\n"
             "Pregunta a la clase: '200 equipos en una sola subred, ¿qué pasa si alguien\n"
             "hace un ping broadcast?' (se llena la red). Que la respuesta salga de ellos.\n"
             "El punto de SEGURIDAD es el que más se recuerda: en una red plana el usuario\n"
             "llega directo al puerto de la base de datos. Segmentar es seguridad y rendimiento.")

    # ------------------------------------------------------------- 6 VLAN
    n += 1
    s = content(prs, "Segmentación en capa 2: VLAN (IEEE 802.1Q)", "Un switch, varias redes lógicas independientes", PART, n + 1)
    text(s, 0.45, 1.3, 12.4, 0.35,
         [[("La idea: ", {"size": 14, "bold": True, "color": NAVY}),
           ("un switch físico reparte sus puertos en grupos lógicos independientes, cada uno con su propia VLAN ID.", {"size": 14, "color": TEXT})]])
    flow(s, [("VLAN 10", "Usuarios\n192.168.10.0/24"), ("VLAN 20", "Servidores\n192.168.20.0/24"),
             ("VLAN 30", "Datos\n192.168.30.0/24")],
         0.9, 1.8, 8.0, h=0.95, colors=[BLUE, TEAL, GREEN], size=12.5)
    text(s, 0.9, 2.85, 8.0, 0.3, "▲  un solo switch 802.1Q  ·  las tres VLAN están aisladas entre sí",
         size=11.5, color=GRAY, align=PP_ALIGN.CENTER)
    callout(s, 9.2, 1.75, 3.65, 2.6, "Cómo viaja una trama", [
        "El switch marca la trama con un **tag de 4 bytes** (802.1Q).",
        "El tag lleva la **VLAN ID** (1 a 4094).",
        "Un puerto **trunk** transporta varias VLAN; un puerto **access** una sola."], ORANGE, 12)
    table(s, [["", "VLAN (802.1Q)", "Subred IP", "Red bridge del laboratorio"],
              ["Capa", "2 · enlace", "3 · red", "3 · red (virtual)"],
              ["Se configura en", "Switch (trunk/access)", "Host o router", "docker network create"],
              ["Aísla", "El tráfico entre puertos", "El tráfico L3 por diseño", "Contenedores de esa red"],
              ["Se rompe si…", "El trunk no soporta el tag", "Las rutas están mal", "Se conecta a otra red"]],
          0.45, 4.55, 12.4, col_w=[2.2, 2.9, 3.0, 4.3], size=11.5, row_h=0.36, header_h=0.4)
    notes(s, "⏱ 12-20 min · VLAN. ★ BLOQUE CENTRAL\n\n"
             "Aclaración honesta: VLAN NO es tema propio del analítico (que lista 802.3/802.11/\n"
             "802.15/802.16). VLAN es 802.1Q (bridging). Se incluye porque es el tema exacto de\n"
             "'segmentación' del 3.1 y da la clave mental de lo que hacen las redes bridge.\n\n"
             "Resumen de una frase: 'separar un switch en varias redes lógicas sin comprar más switches'.\n"
             "Pregunta: si dos VLAN usaran la misma subred IP, ¿funcionaría? (No: duplicar rangos\n"
             "rompe el retorno; por eso nunca se superponen.)")

    # ------------------------------------------------------------- 7 subredes
    n += 1
    s = content(prs, "Segmentación en capa 3: las subredes", "Cada segmento recibe su propio rango de direcciones IP", PART, n + 1)
    table(s, [["Segmento", "Subred", "Máscara", "Gateway", "Hosts útiles", "Qué vive ahí"],
              ["Usuarios", "10.0.0.0/24", "255.255.255.0", "10.0.0.1", "254", "Equipos de usuario"],
              ["Servicios", "10.0.1.0/24", "255.255.255.0", "10.0.1.1", "254", "Web y API"],
              ["Datos", "10.0.2.0/25", "255.255.255.128", "10.0.2.1", "126", "Base de datos aislada"],
              ["Gestión", "10.0.3.0/28", "255.255.255.240", "10.0.3.1", "14", "Monitoreo y administración"]],
          0.45, 1.45, 12.4, col_w=[1.7, 1.9, 2.3, 1.6, 1.6, 3.3], size=11.5, row_h=0.5)
    callout(s, 0.45, 3.95, 6.1, 2.0, "Reglas del direccionamiento", [
        "Se reparten del **mayor al menor**: la subred más grande primero.",
        "Nunca se superponen: un rango duplicado rompe el retorno.",
        "Se reserva un rango de **gestión** para monitoreo y acceso."], ORANGE, 12.5)
    callout(s, 6.78, 3.95, 6.1, 2.0, "Ventaja de segmentar en capa 3", [
        "El tráfico entre segmentos **pasa por el router** y se puede filtrar.",
        "Un problema en un segmento **no** inunda a los demás.",
        "La base de datos deja de ser alcanzable desde los usuarios."], TEAL, 12.5)
    kpi(s, [("4", "segmentos"), ("10.0.0.0/16", "espacio privado (RFC 1918)"), ("0", "solapes")],
        0.45, 6.05, 12.4, h=0.95)
    notes(s, "⏱ 20-23 min · Direccionamiento.\n\n"
             "NO rehacer el cálculo VLSM: ya se hizo en la Unidad II (Caso 3) y en el Avance 1.\n"
             "Mostrar la tabla como ejemplo de 'presupuesto de direcciones' de una LAN de 4 segmentos.\n"
             "Insistir: segmentar en capa 3 es lo que permite FILTRAR entre segmentos — ahí\n"
             "está la seguridad que se busca para la base de datos. El rango de gestión conecta\n"
             "con el servidor bastión de la Parte 2.")

    # ------------------------------------------------------------- 8 VLAN vs subred
    n += 1
    s = content(prs, "VLAN y subred no son lo mismo", "Una segmenta en capa 2 (switch) y la otra en capa 3 (IP/router)", PART, n + 1)
    table(s, [["Aspecto", "VLAN (802.1Q)", "Subred IP"],
              ["Capa del modelo", "Enlace (2)", "Red (3)"],
              ["Se define en", "El switch", "El direccionamiento (IP + máscara)"],
              ["Aísla por", "Puertos del switch", "Rangos de direcciones"],
              ["Para comunicarlas se necesita", "Un router (router-on-a-stick)", "Un router (una interfaz por red)"],
              ["Lo ve el usuario final", "No (es transparente)", "Sí (su IP y su máscara)"],
              ["Ejemplo del laboratorio", "Switch 802.1Q", "docker network (red bridge)"]],
          0.45, 1.5, 12.4, col_w=[3.4, 4.5, 4.5], size=12.5, row_h=0.52)
    callout(s, 0.45, 5.55, 12.4, 1.25, "Cómo se combinan en la práctica", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Normalmente una VLAN corresponde a una subred: se aísla en capa 2 **y** en capa 3. ", {"size": 12.5}),
         ("El router es el que las une y decide qué tráfico puede cruzar.", {"size": 12.5, "bold": True})]],
        ORANGE, 12.5)
    notes(s, "⏱ 23-26 min · VLAN vs subred.\n\n"
             "Esta tabla responde la duda que suele quedar: VLAN (capa 2) y subred (capa 3) no\n"
             "compiten, se complementan. Una VLAN por subred es el diseño típico.\n"
             "Mensaje: 'la seguridad no está en aislar, sino en decidir qué cruza el router'.")

    # ------------------------------------------------------------- 9 DHCP
    n += 1
    s = content(prs, "Servicio 1: DHCP (entrega de direcciones)", "El equipo arranca sin saber nada y la red le da su configuración", PART, n + 1)
    flow(s, [("Cliente", "arranca sin IP"), ("DISCOVER", "busca servidor\n(broadcast)"),
             ("OFFER", "el servidor\npropone"), ("REQUEST", "el cliente\npide"), ("ACK", "queda\nasignada")],
         0.5, 1.45, 12.3, h=1.0, colors=[BLUE, TEAL, GREEN, ORANGE, NAVY], size=11.5)
    table(s, [["Dato que entrega", "Ejemplo", "Por qué importa"],
              ["Dirección IP", "10.0.0.50", "Identifica al equipo en la subred"],
              ["Máscara de subred", "255.255.255.0 (/24)", "Define qué es local y qué no"],
              ["Puerta de enlace (gateway)", "10.0.0.1", "Por dónde sale hacia otras redes"],
              ["Servidor DNS", "10.0.0.53", "Cómo resuelve los nombres"]],
          0.45, 2.85, 12.4, col_w=[3.6, 3.2, 5.6], size=12, row_h=0.44)
    callout(s, 0.45, 5.25, 6.1, 1.4, "Detalle clave: DORA", [
        "DISCOVER → OFFER → REQUEST → ACK.",
        "El primer paquete va por **broadcast**: el cliente aún no tiene IP."], ORANGE, 12)
    callout(s, 6.78, 5.25, 6.1, 1.4, "UDP 67 (servidor) / 68 (cliente)", [
        "La dirección se entrega con un **lease** (préstamo).",
        "Al expirar, el cliente la renueva o recibe otra."], TEAL, 12)
    notes(s, "⏱ 26-28 min · Servicios, parte 1 (DHCP).\n\n"
             "Ya se vio DORA en el Caso 1: no reexplicar, solo confirmar el orden y el porqué\n"
             "del broadcast inicial. Lo importante para la LAN: el gateway y el DNS también se\n"
             "entregan por DHCP, no solo la IP.")

    # ------------------------------------------------------------- 10 DNS y NAT
    n += 1
    s = content(prs, "Servicios 2 y 3: DNS y NAT", "Resolver nombres y salir a internet con direcciones privadas", PART, n + 1)
    flow(s, [("Cliente", "escribe un nombre\n«app.local»"), ("DNS", "resuelve:\nnombre → IP"),
             ("NAT", "traduce IP privada\n→ IP pública")],
         0.9, 1.5, 8.6, h=1.05, colors=[BLUE, TEAL, ORANGE], size=12.5)
    table(s, [["Servicio", "Protocolo / puerto", "Qué resuelve"],
              ["DNS", "UDP/TCP 53", "Nombre → IP (registros A, CNAME, MX)"],
              ["NAT", "Tabla del router", "Traduce la IP privada al salir a internet"],
              ["NAT (DNAT)", "Tabla del router", "Publica un servicio interno en un puerto"]],
          0.45, 2.9, 12.4, col_w=[2.4, 3.0, 7.0], size=12.5, row_h=0.46)
    callout(s, 0.45, 5.35, 6.1, 1.4, "Por qué DNS y no IPs sueltas", [
        "Si la IP cambia, el cliente no se entera: el **nombre no cambia**.",
        "Desacopla el nombre del servicio de la IP que tenga."], ORANGE, 12)
    callout(s, 6.78, 5.35, 6.1, 1.4, "NAT y las direcciones privadas", [
        "RFC 1918: 10/8, 172.16/12, 192.168/16 no se enrutan en internet.",
        "El router las traduce al salir (SNAT) y de vuelta."], TEAL, 12)
    notes(s, "⏱ 28-31 min · Servicios, partes 2 y 3 (DNS y NAT).\n\n"
             "El argumento fuerte del DNS interno: desacoplar nombre de IP. Eso es lo que más\n"
             "tarde permite mover servicios sin tocar la configuración.\n"
             "NAT: recordar que las IP privadas (RFC 1918) no se enrutan en internet; el router\n"
             "las traduce. Conectar con 'por qué una LAN usa direcciones privadas'.")

    # ------------------------------------------------------------- 11 router
    n += 1
    s = content(prs, "El router de capa 3: une los segmentos", "Dos interfaces, una en cada subred — el patrón de la LAN segmentada", PART, n + 1)
    text(s, 0.45, 1.3, 6.2, 0.35, "Un dispositivo con una interfaz por subred:", size=14, color=NAVY, bold=True)
    code(s, 0.45, 1.75, 6.2, 1.95, [
        ("$ ip -4 -o addr show", SUB),
        "eth0  10.0.0.1/24   ← red de usuarios",
        "eth1  10.0.1.1/24   ← red de servicios",
        "",
        ("$ ip route", SUB),
        "10.0.0.0/24 dev eth0",
        "10.0.1.0/24 dev eth1",
        ("default via <proveedor>", ORANGE),
    ], size=11)
    text(s, 0.45, 3.85, 6.2, 0.35, "Verificación del reenvío", size=14, color=NAVY, bold=True)
    code(s, 0.45, 4.3, 6.2, 1.55, [
        ("$ cat /proc/sys/net/ipv4/ip_forward", SUB),
        ("1        # sin esto NO reenvía entre interfaces", ORANGE),
        "",
        ("$ ip -s link show eth0   # errores y drops", SUB),
    ], size=11)
    callout(s, 6.95, 1.55, 5.9, 2.5, "El switch no une redes; el router sí", [
        "Un switch (capa 2) solo mueve tramas dentro del mismo segmento.",
        "El router (capa 3) decide, con su tabla de rutas, a qué red va el paquete.",
        "Conseguir una LAN segmentada **obliga** a tener un router entre segmentos."], ORANGE, 12.5)
    callout(s, 6.95, 4.25, 5.9, 1.9, "Los 3 requisitos del router", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Reenvío IPv4 habilitado", {"size": 12.5, "bold": True}),
         (" (ip_forward=1).", {"size": 12.5})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Una interfaz por subred", {"size": 12.5, "bold": True}),
         (" (dos o más).", {"size": 12.5})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Ruta por destino", {"size": 12.5, "bold": True}),
         (" en ambos sentidos.", {"size": 12.5})]], TEAL, 12.5)
    notes(s, "⏱ 31-35 min · El router.\n\n"
             "Idea que debe quedar: segmentar en capa 3 obliga a enrutar. El switch no cruza\n"
             "segmentos; el router sí, con su tabla de rutas. Es el mismo patrón del router del\n"
             "Caso 2, ahora como diseño de la LAN real.\n"
             "El requisito que más se olvida es el reenvío (ip_forward). Sin él, el paquete\n"
             "llega a una interfaz y no sale por la otra. La tabla de rutas (ip route) es la\n"
             "herramienta de diagnóstico.")

    # ------------------------------------------------------------- 12 ruta ida y vuelta
    n += 1
    s = content(prs, "Ruta de ida y ruta de vuelta", "El paquete tiene que poder regresar: si no hay ruta de vuelta, no hay respuesta", PART, n + 1)
    flow(s, [("Origen", "10.0.0.10"), ("Gateway", "10.0.0.1\n(ruta de ida)"),
             ("Router", "decide\ndestino"), ("Destino", "10.0.1.20"),
             ("Vuelta", "10.0.1.1 → 10.0.0.0/24\n(ruta de vuelta)")],
         0.4, 1.5, 12.5, h=1.15, colors=[BLUE, TEAL, NAVY, GREEN, ORANGE], size=11)
    callout(s, 0.45, 3.0, 6.1, 2.5, "Qué significa «no hay ruta de vuelta»", [
        "El paquete llega al destino, pero el destino **no sabe cómo responder**.",
        "Se ve como un ping que se pierde aunque la ruta de ida exista.",
        "Por eso el router necesita rutas (o un default) **en los dos sentidos**."], ORANGE, 12.5)
    callout(s, 6.78, 3.0, 6.1, 2.5, "Cómo se diagnostica en capa 3", [
        "ip route → ver la tabla de rutas del equipo o router.",
        "ping → comprobar ida y vuelta (ICMP echo / echo reply).",
        "traceroute → ver por qué saltos (hops) pasa el paquete.",
        "arp → ver el mapeo IP ↔ MAC dentro del segmento."], TEAL, 12.5)
    kpi(s, [("ICMP", "diagnóstico\nde capa 3"), ("TTL", "limita los saltos\ny evita bucles"), ("0", "solapes de red")],
        0.45, 5.7, 12.4, h=1.0)
    notes(s, "⏱ 35-37 min · Ruta de ida y vuelta.\n\n"
             "Este es el error clásico de laboratorio: 'el ping no responde aunque la red\n"
             "está bien'. Casi siempre falta la ruta de vuelta o el gateway. Ya se nombró en\n"
             "el Caso 2; aquí se deja el concepto y las herramientas de capa 3.")

    # ------------------------------------------------------------- 13 divider 3.2
    n += 1
    s = divider(prs, "3.2", "El monitoreo de red", "La parte que separa una red que «anda» de una red que se puede operar",
                ["Qué se mide: ancho de banda, latencia, pérdida, jitter, errores",
                 "Herramientas: tcpdump · iftop · iperf3 · netdata",
                 "Cómo leer un resultado y sacar una conclusión"], "15 min")
    notes(s, "⏱ 37-38 min · Transición a 3.2.\n\n"
             "Frase de entrada: 'ya construimos y entendimos la LAN; ahora la miramos.\n"
             "Sin medición, estás a ciegas.'")

    # ------------------------------------------------------------- 14 métricas
    n += 1
    s = content(prs, "Las métricas de red que importan", "Si solo vas a mirar cinco cosas, que sean estas", PART, n + 1)
    kpi(s, [("Mbps", "Ancho de banda\ncuánto pasa"), ("ms", "Latencia\ncuánto tarda"),
            ("%", "Pérdida\ncuánto se pierde"), ("ms", "Jitter\ncuánto varía")],
        0.45, 1.5, 12.4, h=1.1, gap=0.25)
    table(s, [["Métrica", "Qué mide", "Valor sano en LAN", "Si está mal, sospechar de…"],
              ["Ancho de banda", "Bits por segundo", "> 100 Mbps en Gigabit", "Enlace saturado · cuello de botella"],
              ["Latencia", "Tiempo de ida y vuelta", "< 1 ms en la LAN", "Congestión · ruta larga"],
              ["Pérdida", "Paquetes que no llegan", "0 %", "Cable · switch · saturación"],
              ["Jitter", "Variación de la latencia", "< 5 ms", "Voz/video con cortes"],
              ["Errores", "Frames con error (CRC) o drops", "0", "Cable · conector · duplex mismatch"]],
          0.45, 2.9, 12.4, col_w=[2.3, 3.0, 2.9, 4.2], size=12, row_h=0.42)
    callout(s, 0.45, 5.5, 12.4, 1.25, "El criterio del programa (3.2)", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("«Aplicar herramientas de monitoreo de red»", {"size": 12.5, "bold": True, "color": NAVY}),
         (": el entregable no es la herramienta, es la evidencia de que la red responde. ", {"size": 12.5}),
         ("El ENUNCIADO del proyecto exige tcpdump, iftop, iperf3 o netdata (mínimo 1).", {"size": 12.5, "bold": True})]],
        ORANGE, 12.5)
    notes(s, "⏱ 38-41 min · Métricas de red.\n\n"
             "Cinco métricas: ancho de banda (¿cuánto pasa?), latencia (¿cuánto tarda?),\n"
             "pérdida (¿qué se cae?), jitter (¿varía?) y errores (¿la interfaz falla?).\n"
             "Insistir en la última columna: cada síntoma apunta a una causa probable.\n"
             "Ejemplo: 40 ms entre dos equipos del mismo host casi siempre es virtualización,\n"
             "no la red física. Monitorear es hipótesis + verificación, no solo mirar gráficas.")

    # ------------------------------------------------------------- 15 herramientas
    n += 1
    s = content(prs, "Las herramientas y la pregunta que responde cada una", "Cada una ataca una métrica distinta — no compiten", PART, n + 1)
    table(s, [["Herramienta", "Pregunta que responde", "Capa", "Métrica"],
              ["tcpdump", "¿Qué paquetes exactos están pasando?", "2-4", "Contenido, errores"],
              ["iftop", "¿Quién está usando la red ahora mismo?", "3-4", "Ancho de banda"],
              ["iperf3", "¿Cuánto ancho de banda aguanta de verdad?", "4", "Banda, jitter, pérdida"],
              ["netdata", "¿Cómo se comporta el sistema con el tiempo?", "—", "Histórico (panel web)"]],
          0.45, 1.45, 12.4, col_w=[1.9, 5.4, 1.6, 3.5], size=12, row_h=0.55)
    callout(s, 0.45, 4.15, 6.1, 2.2, "Herramientas de línea de comandos", [
        "tcpdump captura y muestra paquetes (con -nn sin resolver nombres).",
        "iftop muestra el tráfico por host en tiempo real (barras).",
        "iperf3 abre una conexión y mide la tasa real (TCP o UDP).",
        "Todas se ejecutan en un equipo o servidor de la LAN."], ORANGE, 12)
    callout(s, 6.78, 4.15, 6.1, 2.2, "Además, sin instalar nada", [
        "ping → latencia y pérdida (ICMP).",
        "ip -s link → contadores de errores y drops por interfaz.",
        "ss → conexiones y puertos en escucha.",
        "dig / nslookup → verificar el DNS."], TEAL, 12)
    notes(s, "⏱ 41-45 min · Herramientas.\n\n"
             "No son competencia: cada una responde una pregunta distinta.\n"
             "La combinación que da evidencia: tcpdump (QUÉ pasa) + iperf3 (CUÁNTO pasa) +\n"
             "netdata (CÓMO evoluciona). Esa combinación es la que pide el Avance 2 del proyecto.\n"
             "netdata es lo más visual: mostrar la URL :19999 en el navegador si hay tiempo.")

    # ------------------------------------------------------------- 16 TCP vs UDP
    n += 1
    s = content(prs, "Medir con TCP y con UDP no es lo mismo", "El mismo enlace se comporta distinto según el transporte", PART, n + 1)
    table(s, [["Aspecto", "TCP", "UDP"],
              ["Conexión", "Orientado (handshake)", "Sin conexión"],
              ["Ante la pérdida", "Retransmite y baja el caudal", "Pierde y no avisa"],
              ["Qué mide mejor", "Rendimiento real", "Jitter y pérdida"],
              ["Dato clave en la salida", "Mbits/sec y retransmisiones", "Jitter y Lost/Total"],
              ["Ejemplo de uso", "Web, SSH, base de datos", "DNS, voz, video, juegos"]],
          0.45, 1.5, 12.4, col_w=[2.6, 5.0, 4.8], size=12.5, row_h=0.48)
    callout(s, 0.45, 5.0, 6.1, 1.75, "Lo que enseña el resultado", [
        "Si suben las retransmisiones en TCP → hay pérdida (y el caudal baja).",
        "Si sube el jitter en UDP → la voz/video se corta aunque no haya pérdida."], ORANGE, 12)
    callout(s, 6.78, 5.0, 6.1, 1.75, "Por qué importa para la LAN", [
        "Mismo medio, distinto resultado: el transporte cambia la medición.",
        "Por eso una métrica sola no basta para decir «la red está bien»."], TEAL, 12)
    notes(s, "⏱ 45-49 min · TCP vs UDP (iperf3).\n\n"
             "Enlaza con la teoría de transporte de la Unidad II. Mensaje clave: TCP se adapta\n"
             "(retransmite, baja el caudal); UDP pierde y no avisa.\n"
             "Si hay laboratorio levantado, correr iperf3 en vivo es lo que más convence.\n"
             "El jitter es la métrica que decide si una videollamada se oye bien.")

    # ------------------------------------------------------------- 17 OSI y monitoreo
    n += 1
    s = content(prs, "Qué se observa en cada capa del modelo OSI", "El monitoreo no es solo «paquetes»: cada capa tiene su evidencia", PART, n + 1)
    table(s, [["Capa", "Qué se observa", "Con qué"],
              ["1 · Física", "Señal, errores de transmisión, drops", "ip -s link"],
              ["2 · Enlace", "Tramas, direcciones MAC, FCS", "tcpdump, arp"],
              ["3 · Red", "IP, rutas, ICMP (ping/traceroute)", "ping, ip route, traceroute"],
              ["4 · Transporte", "Puertos, TCP/UDP, retransmisiones, jitter", "ss, tcpdump, iperf3"],
              ["7 · Aplicación", "HTTP/HTTPS, DNS, tiempos de respuesta", "curl, dig, panel web"]],
          0.45, 1.5, 12.4, col_w=[2.3, 6.1, 4.0], size=12.5, row_h=0.5)
    callout(s, 0.45, 4.6, 12.4, 2.15, "El método (no la herramienta) es lo importante", [
        "1. Definir el síntoma: ¿lento, intermitente, no conecta?",
        "2. Formular una hipótesis de capa: ¿física, enlace, red, transporte o aplicación?",
        "3. Medir con la herramienta de esa capa y comparar contra el valor sano.",
        "4. Concluir y, si aplica, corregir; volver a medir para confirmar."], ORANGE, 12.5)
    notes(s, "⏱ 49-52 min · Monitoreo por capas.\n\n"
             "Este cuadro es la síntesis de la clase de monitoreo: conecta el modelo OSI con\n"
             "las herramientas. Que el estudiante se lleve el MÉTODO, no una lista de comandos.\n"
             "Ejemplo de hipótesis: 'no resuelve nombres' → capa 7 (DNS); 'no conecta a un\n"
             "puerto' → capa 4 (ss/telnet); 'todo lento' → capa 1/3.")

    # ------------------------------------------------------------- 18 cierre
    n += 1
    s = content(prs, "Resumen y cierre de la Parte 1", "Qué debe quedar claro antes de ir al Laboratorio N.º 10", PART, n + 1)
    callout(s, 0.45, 1.4, 6.1, 2.5, "Ideas clave (3.1 + 3.2)", [
        "Una LAN es un dominio de broadcast: se **segmenta** para escalar y asegurar.",
        "Se segmenta en capa 2 (**VLAN**) y en capa 3 (**subredes**).",
        "DHCP, DNS y NAT son los servicios mínimos.",
        "El **router** une los segmentos y decide qué tráfico cruza.",
        "Se monitorea para **actuar**: banda, latencia, pérdida, jitter, errores."], ORANGE, 12)
    callout(s, 6.78, 1.4, 6.1, 2.5, "Puente hacia la Parte 2", [
        "Administrar la LAN exige entrar a esos servidores…",
        "…pero **con contraseña no se escala y no es seguro**.",
        "Parte 2: claves SSH (3.3) + servidor bastión (3.4).",
        "El bastión vive en el segmento de administración."], TEAL, 12)
    callout(s, 0.45, 4.15, 12.4, 2.55, "Preguntas de autoevaluación (sal de clase sabiendo responderlas)", [
        [("1. ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("¿Por qué una red plana es un problema de seguridad además de rendimiento?", {"size": 12.5})],
        [("2. ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("¿Qué tres condiciones debe cumplir un equipo para hacer de router entre dos redes?", {"size": 12.5})],
        [("3. ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Diferencia entre VLAN y subred: ¿qué capa resuelve cada una?", {"size": 12.5})],
        [("4. ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Si ves 40 ms de latencia entre dos equipos del mismo host, ¿qué revisas primero?", {"size": 12.5})],
        [("5. ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("¿Qué herramienta usarías para demostrar que la red sostiene 100 Mbps y cuál para ver quién los consume?", {"size": 12.5})]],
        NAVY, 12.5)
    notes(s, "⏱ 52-55 min · Cierre de la Parte 1.\n\n"
             "Las 5 preguntas son el pretexto del parcial y del Laboratorio N.º 10.\n"
             "Respuestas guía: (1) exposición directa a servicios internos como la base de datos;\n"
             "(2) reenvío habilitado, una interfaz por subred, ruta en ambos sentidos;\n"
             "(3) VLAN = capa 2, subred = capa 3; (4) el jitter; (5) TCP se adapta (retransmite),\n"
             "UDP pierde y no avisa.\n"
             "Pedir 2 respuestas en voz alta y anunciar el puente a la Parte 2 (SSH y bastión).")

    prs.save(out)
    return out


if __name__ == "__main__":
    p = build(sys.argv[1] if len(sys.argv) > 1 else "Teoria/Teoria-U3-Parte1-LAN-Monitoreo.pptx")
    print("OK ->", p)
