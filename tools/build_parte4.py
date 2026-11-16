"""Unidad III · Parte 4 — Almacenamiento compartido para HA (extensión del 3.5) · 55 min."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ppt_kit import *  # noqa

PART = "Parte 4 · Almacenamiento HA"


def build(out):
    prs = new_deck()
    n = 0

    s = cover(prs, "UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES",
              "Unidad III — Parte 4",
              "Almacenamiento compartido para alta disponibilidad",
              ["Extensión del tema 3.5 · de un host con Compose a un clúster HA",
               "Dónde viven los datos cuando un nodo muere: NAS, SAN, quórum, réplicas",
               "Material de integración · semanas 12-13 · Proyecto Final"],
              "Extensión de la Parte 3", "55 min de profundización")
    notes(s, "⏱ 0-3 min · Apertura de la Parte 4 (extensión).\n\n"
             "Esta parte no es del programa original: es la pregunta que la Parte 3 dejó\n"
             "abierta y que todo el mundo encuentra en producción. Frase de apertura:\n"
             "'el orquestador mueve contenedores; el dato no se mueve solo'.\n"
             "Va después de las presentaciones del semestral y del Lab 14, como profundización.")

    n += 1
    s = content(prs, "Qué vamos a ver en esta parte", "La pregunta que quedó abierta al final de la Parte 3", PART, n + 1)
    table(s, [["#", "Tema", "Qué resuelve", "Min"],
              ["—", "Almacenamiento compartido (DAS/NAS/SAN/distribuido)", "Que el dato sobreviva al nodo caído", "20"],
              ["—", "Quórum y fencing", "Evitar el split-brain cuando la red se parte", "10"],
              ["—", "Volúmenes del orquestador (NFS/CSI)", "Declarar el almacenamiento como declaras los servicios", "15"],
              ["—", "Patrones y anti-patrones de datos", "Qué se replica, qué se comparte, qué no se toca", "10"]],
           0.45, 1.45, 12.4, col_w=[0.9, 4.6, 5.9, 1.0], size=12.5, row_h=0.44)
    callout(s, 0.45, 3.85, 6.1, 2.75, "La pregunta que quedó abierta", [
        "La Parte 3 cerró con: «Swarm mueve el contenedor al nodo sano».",
        "Pero el **volumen** era local al nodo: la réplica de la db levanta en otro host…",
        "…y no encuentra `/var/lib/postgresql/data`.",
        "**El contenedor es desechable; el dato, no.**"], ORANGE, 12.5)
    callout(s, 6.78, 3.85, 6.1, 2.75, "Lo que NO es esta parte", [
        "No es un curso de Kubernetes ni de Ceph.",
        "Es la capa **red + datos** que todo clúster HA necesita.",
        "En producción, la mayoría de caídas «del servidor» son de storage o de red:",
        "las dos cosas que este curso enseña."], TEAL, 12.5)
    notes(s, "⏱ 3-5 min · Agenda.\n\n"
             "Ancla la parte en algo que ya vieron: el `pgdata` del Lab 14. Ahí está el\n"
             "conflicto entero en un ejemplo. Si alguien preguntó '¿y si se cae la máquina'\n"
             "en la Sesión 4, esta presentación es la respuesta completa.")

    n += 1
    s = divider(prs, "3.5+", "El dato no es desechable",
                "De «el contenedor se reinicia solo» a «el dato sobrevive al nodo»",
                ["Repaso: dónde viven los datos en Compose",
                 "Los modelos: DAS, NAS, SAN — y el distribuido",
                 "Quórum: por qué 3 nodos y no 2"], "25 min")
    notes(s, "⏱ 5-6 min · Transición al bloque técnico.")

    n += 1
    s = content(prs, "Repaso: dónde viven los datos hoy", "El volumen del Lab 14, visto con lupa", PART, n + 1)
    code(s, 0.45, 1.35, 6.4, 2.4, [
        ("$ docker volume ls", ORANGE),
        "DRIVER    VOLUME NAME",
        "local     lab14-sesion-4_pgdata",
        "",
        ("$ docker compose down    # conserva pgdata", SUB),
        ("$ docker compose down -v # borra pgdata", RED)], size=11)
    callout(s, 7.15, 1.35, 5.7, 2.4, "En el Lab 14 (Sesiones 3-4)", [
        "La db escribe en el volumen `pgdata`.",
        "El contenedor se recrea; el dato sigue ahí.",
        "`down` sin `-v` = política de datos ya aprendida (Drill 6 del refuerzo)."], TEAL, 12.5)
    table(s, [["Mecanismo", "Qué es", "Quién lo gestiona", "¿Sobrevive a `down`?"],
              ["bind mount", "una carpeta del host (`./datos`)", "tú, a mano", "sí (es del host)"],
              ["volume", "`pgdata`, gestionado por Docker", "Docker", "sí (salvo `-v`)"],
              ["tmpfs", "RAM, nunca toca disco", "Docker", "no"]],
           0.45, 3.95, 12.4, col_w=[2.1, 4.3, 2.6, 3.4], size=12, row_h=0.42)
    callout(s, 0.45, 5.85, 12.4, 1.0, "El «pero» que motiva toda esta parte", [
        [("▸ ", {"color": RED, "bold": True, "size": 12.5}),
         ("Ese volumen vive en UN solo host: si el nodo muere, el dato muere con él. Escalar la db sin storage compartido = **dos bases divergentes**.",
          {"size": 12.5, "bold": True})]], RED, 12.5)
    notes(s, "⏱ 6-11 min · Repaso de volúmenes.\n\n"
             "No asumas que lo recuerdan: haz la pregunta '¿dónde quedó la base del Lab 14\n"
             "cuando hicimos down?' y deja que lo respondan.\n"
             "El paso de bind mount → volume ya lo vieron; aquí solo hace falta nombrarlo.\n"
             "El callout rojo es la bisagra: léelo en voz alta y no avances hasta que cale.")

    n += 1
    s = content(prs, "Qué significa alta disponibilidad (HA)", "No es tener réplicas: es seguir sirviendo cuando algo muere", PART, n + 1)
    kpi(s, [("99,9 %", "≈ 8,8 h/año caído"), ("99,99 %", "≈ 53 min/año caído"),
            ("RTO", "cuánto tarda en volver"), ("RPO", "cuánto dato se pierde")],
        0.45, 1.35, 12.4)
    callout(s, 0.45, 2.65, 6.1, 2.5, "SPOF: el punto único de falla", [
        "Cualquier componente sin respaldo: la fuente, el switch de salida,",
        "el nodo, el disco… **y la persona que solo ella sabe reiniciar**.",
        "HA = eliminar SPOF **capa por capa** (energía, red, nodo, dato)."], ORANGE, 12.5)
    callout(s, 6.78, 2.65, 6.1, 2.5, "Réplicas ≠ datos disponibles", [
        "3 réplicas de la api **sin estado** = HA fácil (Parte 3).",
        "La db **con estado** = el problema real de esta parte.",
        "**Stateless es barato; stateful es difícil.**"], TEAL, 12.5)
    callout(s, 0.45, 5.35, 12.4, 1.4, "La definición en una línea", [
        [("▸ ", {"color": NAVY, "bold": True, "size": 13}),
         ("Un sistema HA sigue sirviendo cuando falla un componente cualquiera — y no pierde los datos que ya había comprometido.",
          {"size": 13, "bold": True})],
        "RTO y RPO son los dos números que un jefe entiende: cuánto tiempo y cuánto dato."], NAVY, 12.5)
    notes(s, "⏱ 11-16 min · Qué es HA.\n\n"
             "Los porcentajes de disponibilidad suelen sorprender: 99,9 % son casi 9 horas\n"
             "al año. Pregunta cuántas 9 exige un banco y cuántas un blog.\n"
             "RTO/RPO en una frase cada uno; no hace más detalle hoy.")

    n += 1
    s = content(prs, "Dos filosofías: shared-everything vs shared-nothing", "Todo clúster de datos elige uno de estos dos caminos", PART, n + 1)
    table(s, [["", "Shared-everything", "Shared-nothing"],
              ["Idea", "todos los nodos ven el **mismo** almacenamiento", "cada nodo tiene su copia y se sincroniza"],
              ["Ejemplos", "Oracle RAC sobre SAN · VMs sobre NFS", "réplica de PostgreSQL · Ceph · Galera"],
              ["Si un nodo muere", "otro monta el mismo dato", "otro promueve su réplica"],
              ["Riesgo clásico", "dos escritores = corrupción (split-brain)", "lag de replicación (última transacción)"],
              ["Exigencia de red", "subred de storage muy estable y rápida", "ancho de banda para replicar"]],
           0.45, 1.35, 12.4, col_w=[2.4, 5.0, 5.0], size=12, row_h=0.5)
    callout(s, 0.45, 4.45, 6.1, 2.2, "Dónde vive cada cosa hoy", [
        "VMs y archivos → NFS/SAN sigue siendo el estándar.",
        "Bases de datos → hoy se prefiere **replicar** (shared-nothing).",
        "Ninguno es «mejor»: cambian el punto de falla y el costo."], ORANGE, 12.5)
    callout(s, 6.78, 4.45, 6.1, 2.2, "En contenedores", [
        "Swarm y Kubernetes **no replican volúmenes**: el dato sigue al nodo.",
        "El orquestador orquesta **procesos**; el dato lo orquesta el storage.",
        "Por eso el estado migra a servicios especializados (siguientes láminas)."], TEAL, 12.5)
    notes(s, "⏱ 16-21 min · Los dos modelos.\n\n"
             "La analogía que funciona: shared-everything es una pizarra común (todos ven\n"
             "lo mismo, pero pueden chocar al escribir); shared-nothing es que cada uno\n"
             "fotocopie la pizarra (chocan menos, pero la copia llega tarde).\n"
             "Insiste en la caja derecha: el orquestador NO resuelve esto por ti.")

    n += 1
    s = content(prs, "DAS, NAS y SAN: el mapa del almacenamiento", "Tres formas de conectar discos — y dónde entra cada protocolo", PART, n + 1)
    table(s, [["Nivel", "Qué es", "Protocolo típico", "El cliente ve"],
              ["DAS", "disco pegado al servidor", "SATA / SAS", "un disco local (`/dev/sdb`)"],
              ["NAS", "servidor de **archivos** en la LAN", "NFS / SMB", "una carpeta montada (`/mnt/datos`)"],
              ["SAN", "red **dedicada** de bloques", "iSCSI / Fibre Channel", "un disco (el formato lo pone el cliente)"],
              ["Objeto", "almacenamiento por API (nube)", "S3 sobre HTTP", "URLs con binarios"]],
           0.45, 1.35, 12.4, col_w=[1.5, 3.9, 3.3, 3.7], size=12, row_h=0.5)
    callout(s, 0.45, 3.95, 12.4, 1.7, "La diferencia que importa (y se pregunta en el examen)", [
        [("▸ ", {"color": RED, "bold": True, "size": 12.5}),
         ("NAS comparte **archivos**: el servidor coordina los accesos; varios clientes a la vez, sin peligro.", {"size": 12.5})],
        [("▸ ", {"color": RED, "bold": True, "size": 12.5}),
         ("SAN comparte **bloques**: si dos máquinas montan el mismo LUN sin coordinarse, **lo corrompen**.", {"size": 12.5})]], RED, 12.5)
    callout(s, 0.45, 5.85, 12.4, 1.0, "Traducción a contenedores", [
        [("▸ ", {"color": NAVY, "bold": True, "size": 12.5}),
         ("Un volumen NFS es **NAS**: varios nodos montan la misma carpeta. Un LUN iSCSI es **SAN**: un solo dueño a la vez.",
          {"size": 12.5})]], NAVY, 12.5)
    notes(s, "⏱ 21-26 min · DAS/NAS/SAN.\n\n"
             "Truco para que no se olviden: DAS = Directo, NAS = Archivos (Network **File**\n"
             "System), SAN = Bloques (Storage Area Network = red de **discos**).\n"
             "La fila «objeto» está para cerrar el mapa: S3/MinIO aparecen de nuevo en la\n"
             "lámina de patrones.")

    n += 1
    s = content(prs, "El storage compartido ES un problema de red", "Por esto el tema está en un curso de redes y no de sistemas", PART, n + 1)
    flow(s, [("Aplicación", "lee/escribe archivos"), ("Sistema de archivos", "NFS · iSCSI · SMB"),
             ("La red", "TCP/IP o Fibre Channel"), ("El array", "NAS / SAN")],
         0.45, 1.35, 12.4, h=0.95, colors=[BLUE, TEAL, ORANGE, GREEN], size=12)
    table(s, [["Protocolo", "Puerto", "Qué transporta"],
              ["NFS", "2049 TCP/UDP", "archivos sobre la LAN (Linux)"],
              ["SMB/CIFS", "445 TCP", "archivos (mundo Windows)"],
              ["iSCSI", "3260 TCP", "SCSI (bloques) dentro de TCP/IP"],
              ["Fibre Channel", "red propia, sin TCP", "bloques, latencia mínima"]],
           0.45, 2.5, 12.4, col_w=[2.4, 3.0, 7.0], size=12, row_h=0.44)
    callout(s, 0.45, 4.75, 6.1, 1.95, "Reglas de la subred de storage", [
        "VLAN/subred **dedicada** (como `back` en el Lab 14).",
        "Que no atraviese routers ni WAN.",
        "Jumbo frames (MTU 9000) para menos overhead."], ORANGE, 12.5)
    callout(s, 6.78, 4.75, 6.1, 1.95, "Por qué esto es de ESTE curso", [
        "Cada escritura = ida y vuelta: la latencia (3.2) se paga **dos veces**.",
        "Jitter en la red de storage = rendimiento errático en toda la app.",
        "Se diseña con VLSM y VLAN como cualquier otra red (3.1)."], TEAL, 12.5)
    notes(s, "⏱ 26-32 min · El ángulo de red.\n\n"
             "Esta es la lámina que justifica la presentación en el pénsum: el storage\n"
             "compartido no es un periférico, es TRÁFICO DE RED.\n"
             "iSCSI es literalmente SCSI encapsulado en TCP: puedes verlo en Wireshark\n"
             "(filtro `tcp.port == 3260`), igual que vieron la trama del Lab 4.\n"
             "Conecta con las 4 métricas del tema 3.2: latencia y jitter, de nuevo.")

    n += 1
    s = content(prs, "Quórum: evitar el split-brain", "El desastre clásico cuando la red falla a medias", PART, n + 1)
    kpi(s, [("2 nodos", "sin mayoría: peligro"), ("3 nodos", "toleran 1 caído"),
            ("5 nodos", "toleran 2 caídos"), ("N/2+1", "la mayoría que decide")],
        0.45, 1.35, 12.4)
    callout(s, 0.45, 2.65, 3.85, 2.9, "Split-brain", [
        "La red se parte en dos mitades.",
        "Cada mitad cree que la otra murió.",
        "Ambas escriben el mismo disco → **corrupción**.",
        "La falla no fue de discos: fue de **red**."], RED, 12)
    callout(s, 4.65, 2.65, 3.85, 2.9, "Fencing (exclusión)", [
        "Apartar **por la fuerza** al nodo sospechoso.",
        "Que no pueda volver a escribir («shoot the other node in the head»).",
        "Mejor un nodo sano apagado que un disco corrupto."], ORANGE, 12)
    callout(s, 8.85, 2.65, 3.85, 2.9, "Dónde ya lo viste", [
        "Los **managers** de Swarm sincronizan estado con **Raft**.",
        "3 managers toleran 1 caído: mismo quórum.",
        "Ojo: Raft protege los **metadatos** del cluster, no tus datos."], TEAL, 12)
    callout(s, 0.45, 5.75, 12.4, 1.0, "Moraleja de diseño", [
        [("▸ ", {"color": NAVY, "bold": True, "size": 12.5}),
         ("Los clústeres pares (2, 4) tienen el mismo problema: agrega nodos **impares** y deja un árbitro (witness) si el presupuesto no da.",
          {"size": 12.5})]], NAVY, 12.5)
    notes(s, "⏱ 32-37 min · Quórum.\n\n"
             "Ejemplo en vivo si quieres: con 3 personas votando a mano, pide que se tapen\n"
             "los ojos dos de tres: la mayoría no existe y nadie decide escribir.\n"
             "El detalle fino: Swarm elige 3 managers por la misma matemática.\n"
             "El error común que hay que desmontar: 'Raft ya replica, mis datos están\n"
             "seguros'. No: Raft replica el ESTADO DEL CLUSTER (servicios, secretos).")

    n += 1
    s = content(prs, "Almacenamiento distribuido: replicar por software", "La SAN es hardware; la alternativa moderna es software sobre Ethernet", PART, n + 1)
    callout(s, 0.45, 1.35, 6.1, 2.3, "La idea (Ceph, GlusterFS, Longhorn, MinIO)", [
        "N nodos con discos comunes, conectados por Ethernet.",
        "Cada dato se guarda en **≥ 2** de ellos.",
        "El conjunto expone **un** disco/cubo virtual al orquestador."], TEAL, 12.5)
    callout(s, 6.78, 1.35, 6.1, 2.3, "El precio", [
        "2-3× el espacio bruto en disco.",
        "Confirmar tras escribir en ≥ 2 réplicas: seguro, pero más lento.",
        "La red de replicación se dimensiona (3.1) y se vigila (3.2)."], ORANGE, 12.5)
    flow(s, [("Escritura", "la app escribe 1 dato"), ("Replicación", "se copia a otros nodos"),
             ("ACK", "confirman al cliente"), ("Listo", "consistente y tolerante")],
         0.45, 3.85, 12.4, h=0.95, colors=[BLUE, TEAL, ORANGE, GREEN], size=12)
    callout(s, 0.45, 5.0, 12.4, 1.7, "Conclusión del bloque técnico", [
        [("▸ ", {"color": NAVY, "bold": True, "size": 12.5}),
         ("NAS, SAN o distribuido — los tres son **tráfico de red**: elegir uno es un ejercicio de direccionamiento, aislamiento y presupuesto de ancho de banda.",
          {"size": 12.5, "bold": True})],
        "No hay que instalar ninguno en el curso: hay que saber qué elegiría y por qué."], NAVY, 12.5)
    notes(s, "⏱ 37-40 min · Distribuido.\n\n"
             "Ceph es el ejemplo canónico; no hace falta más nombre. Si alguien pregunta\n"
             "por cloud: EBS/S3 de AWS es esto administrado por otro (y cobrado por GB).\n"
             "Cierra el bloque aquí: hasta ahora el QUÉ; lo que sigue es el CÓMO se consume.")

    n += 1
    s = content(prs, "Cómo lo consume el orquestador", "El mismo giro declarativo de la Parte 3, ahora para el disco", PART, n + 1)
    table(s, [["Nivel", "Mecanismo", "Detalle"],
              ["Compose (1 host)", "`volumes:` + driver local", "el volumen vive en el host (Lab 14)"],
              ["Swarm (N nodos)", "el mismo YAML + driver externo (NFS)", "el volumen debe existir en **todos** los nodos"],
              ["Kubernetes", "PV / PVC + StorageClass (CSI)", "pides «10 Gi» y el cluster los consigue"]],
           0.45, 1.35, 12.4, col_w=[2.9, 4.4, 5.1], size=12.5, row_h=0.55)
    callout(s, 0.45, 3.6, 6.1, 2.9, "La idea declarativa, ahora para el disco", [
        "Igual que `DB_HOST=db` evitó las IP (Parte 3),",
        "el **PVC** evita «monta 172.28.30.20:/export».",
        "Declaras **qué** necesitas (10 Gi, un escritor),",
        "y el orquestador decide **dónde y cómo**."], ORANGE, 12.5)
    callout(s, 6.78, 3.6, 6.1, 2.9, "CSI: el estándar de la capa", [
        "**C**ontainer **S**torage **I**nterface.",
        "Cualquier storage (NFS, Ceph, nube) habla el mismo idioma",
        "con cualquier orquestador (Swarm, K8s, Nomad).",
        "Es para el storage lo que Ethernet es para la red:",
        "un estándar de **interfaz**, no un producto."], TEAL, 12.5)
    notes(s, "⏱ 40-43 min · Cómo lo consume el orquestador.\n\n"
             "El paralelo con `DB_HOST=db` es la llave: la Parte 3 ya les enseñó a no\n"
             "depender de la IP; esto es lo mismo un piso más abajo.\n"
             "CSI nómbralo y pasa: lo importante es el patrón declarativo.")

    n += 1
    s = content(prs, "El puente alcanzable: un volumen NFS en Compose", "El mismo YAML del Lab 14, cambiando una sola pieza", PART, n + 1)
    code(s, 0.45, 1.35, 6.4, 2.85, [
        ("services:", ORANGE),
        ("  db:", NAVY),
        "    volumes:",
        "      - pgdata:/var/lib/postgresql/data",
        "",
        ("volumes:", ORANGE),
        ("  pgdata:", NAVY),
        "    driver_opts:",
        ("      type: nfs", GREEN),
        ("      o: addr=172.28.30.20,rw,nfsvers=4", GREEN),
        ("      device: \":/export/pgdata\"", GREEN)], size=10.5)
    code(s, 0.45, 4.35, 6.4, 1.05, [
        ("$ docker volume create --driver local \\", ORANGE),
        ("    --opt type=nfs --opt o=addr=172.28.30.20,rw \\", ORANGE),
        ("    --opt device=:/export/pgdata  pgdata", ORANGE)], size=10)
    callout(s, 7.15, 1.35, 5.7, 1.35, "Qué cambia", [
        "El YAML es casi el del Lab 14.",
        "El volumen ya no vive en el host: vive en el NAS.",
        "Cualquier nodo que levante el stack ve el mismo dato."], ORANGE, 12)
    callout(s, 7.15, 2.85, 5.7, 1.35, "Cómo se verifica", [
        [("▸ ", {"color": TEAL, "bold": True, "size": 12}),
         ("`docker volume inspect pgdata`", {"size": 11, "font": "Consolas", "color": NAVY, "bold": True}),
         (" muestra el driver nfs.", {"size": 12})],
        "Dos contenedores leen el mismo archivo desde el mismo volumen.",
        "`down` sin `-v`: el dato sigue en el NAS."], TEAL, 12)
    callout(s, 0.45, 5.6, 12.4, 1.35, "La red de storage, ahora en el diseño", [
        [("▸ ", {"color": NAVY, "bold": True, "size": 12.5}),
         ("172.28.30.0/24 es la tercera subred, después de `front` y `back` (Lab 14): NFS/iSCSI viaja en su propia VLAN, lejos de la LAN de usuarios.",
          {"size": 12.5})]], NAVY, 12.5)
    notes(s, "⏱ 43-48 min · El puente alcanzable.\n\n"
             "Si hay docker a mano y un servidor NFS (o un contenedor `erichough/nfs-server`),\n"
             "la demo vale la pena: es literalmente cambiar el bloque `volumes:` del Lab 14.\n"
             "El comando de abajo es la versión imperativa, para crear el volumen a mano.\n"
             "Subraya la subred: están diseñando la VLAN de storage con VLSM, como el Caso 3.")

    n += 1
    s = content(prs, "Patrones: qué hacer con cada tipo de estado", "La decisión de diseño que el Proyecto Final te pide justificar", PART, n + 1)
    table(s, [["Pieza", "¿Tiene estado?", "Patrón HA recomendado"],
              ["web / api", "no", "N réplicas + balanceo (routing mesh, Parte 3)"],
              ["sesiones de usuario", "poco", "Redis/JWT fuera del contenedor"],
              ["base de datos", "sí", "réplica nativa o failover gestionado (1 escritor)"],
              ["archivos / imágenes", "sí", "objetos (S3/MinIO) o NFS compartido"],
              ["logs y métricas", "sí", "enviarlos fuera del nodo (remoto)"]],
           0.45, 1.35, 12.4, col_w=[2.7, 1.8, 7.9], size=12, row_h=0.5)
    callout(s, 0.45, 4.45, 12.4, 2.2, "Regla práctica", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("**Stateless primero**: cada byte de estado que quitas del contenedor es un SPOF menos.", {"size": 12.5})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("La escalera del REFUERZO llega a `--scale api=N`; esta parte añade el peldaño de los **datos**.", {"size": 12.5})],
        "La db del Proyecto no necesita SAN ni Ceph: necesita volumen nombrado + política de respaldo documentada."], ORANGE, 12.5)
    notes(s, "⏱ 48-50 min · Patrones.\n\n"
             "La tabla es la lámina que se llevan al Proyecto: léela por filas.\n"
             "Insiste en la última línea del callout: el curso no pide instalar HA real;\n"
             "pide entender qué haría falta y decirlo por escrito.")

    n += 1
    s = content(prs, "Anti-patrones: los que tumban producción", "Los cinco que se repiten en todos los incidentes", PART, n + 1)
    table(s, [["Síntoma", "Causa", "Arreglo"],
              ["el dato desaparece al reiniciar", "bind mount del host en un clúster", "volumen con driver NFS o distribuido"],
              ["dos réplicas de la db «divergen»", "escalar la db como si fuera stateless", "1 escritor + réplicas o failover gestionado"],
              ["disco corrupto tras caída de red", "clúster de 2 nodos sin quórum", "3 o 5 nodos + fencing"],
              ["se pierde todo tras mantenimiento", "`down -v` en producción", "`-v` solo en dev; respaldo + RPO definido"],
              ["secretos legibles en la red", "NFS sin cifrar comparte credenciales", "secrets cifrados (Parte 3) + VLAN interna"]],
           0.45, 1.35, 12.4, col_w=[3.9, 4.2, 4.3], size=12, row_h=0.55)
    callout(s, 0.45, 4.75, 12.4, 1.85, "El patrón detrás de los cinco", [
        [("▸ ", {"color": RED, "bold": True, "size": 12.5}),
         ("Casi todos son el mismo error: **tratar un servicio con estado como si no lo tuviera**.", {"size": 12.5, "bold": True})],
        "El orquestador escala lo que le das; distinguir lo escalable es trabajo tuyo."], RED, 12.5)
    notes(s, "⏱ 50-52 min · Anti-patrones.\n"
             "Cada fila es una historia real de guardia. La fila 2 es la más común en\n"
             "proyectos de estudiantes: `--scale db=2` y a correr.")

    n += 1
    s = content(prs, "Autoevaluación y cierre", "Si puedes responder esto en voz alta, la parte quedó", PART, n + 1)
    callout(s, 0.45, 1.4, 6.1, 4.9, "Responde en voz alta", [
        "¿Por qué el volumen de Compose no basta en un clúster multi-nodo?",
        "¿NAS vs SAN en una frase? (archivos vs bloques)",
        "¿Por qué un clúster de 2 nodos es más peligroso que uno de 3?",
        "iSCSI: ¿qué transporta y en qué puerto? (SCSI sobre TCP, 3260)",
        "¿Qué patrón HA eliges para la db del Proyecto y por qué?"], ORANGE, 12.5)
    callout(s, 6.78, 1.4, 6.1, 2.35, "Para el Proyecto Final", [
        "No se pide SAN ni Ceph: se pide **justificar la decisión**.",
        "«Nuestra db es stateful; elegimos volumen nombrado + respaldo, porque…».",
        "Documentar `down` sin `-v` ya es señal de madurez."], TEAL, 12.5)
    callout(s, 6.78, 3.95, 6.1, 2.35, "El hilo completo de la unidad", [
        "Red segmentada (3.1) → acceso por llave (3.3) →",
        "un solo punto de exposición (3.4) →",
        "orquestación (3.5) →",
        "**y el dato que sobrevive al nodo** (Parte 4)."], NAVY, 12.5)
    notes(s, "⏱ 52-55 min · Autoevaluación y cierre.\n\n"
             "Las cinco preguntas son el filtro de la parte; la segunda y la cuarta son\n"
             "las que separan quién entendió de quién memorizó.\n"
             "Cierra con el hilo de la caja azul: toda la unidad es una sola historia,\n"
             "y esta parte es su final honesto.")

    prs.save(out)
    return out


if __name__ == "__main__":
    p = build(sys.argv[1] if len(sys.argv) > 1 else "Teoria-U3-Parte4-Almacenamiento-Compartido.pptx")
    print("OK ->", p)
