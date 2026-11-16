"""Unidad III · Parte 3 — Orquestación con Compose y Swarm (tema 3.5) · 55 min."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ppt_kit import *  # noqa

PART = "Parte 3 · Orquestación"


def build(out):
    prs = new_deck()
    n = 0

    s = cover(prs, "UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES",
              "Unidad III — Parte 3",
              "Orquestación de servicios con Docker",
              ["Tema 3.5 · Docker Compose y Docker Swarm: réplicas, balanceo y secretos",
               "Laboratorio N.º 12 · Semana 11 · 2 sesiones",
               "Cierre de la unidad y del Proyecto Semestral"],
              "Parte 3 de 3", "2 h 45 min de clase (3 partes de 55 min)")
    notes(s, "⏱ 0-3 min · Apertura de la Parte 3.\n\n"
             "Esta parte cierra la unidad y el proyecto. Todo lo anterior converge acá:\n"
             "la red (Parte 1), el acceso seguro (Parte 2) y ahora el despliegue a escala.\n"
             "Frase de apertura: 'hasta ahora vimos cómo se protege una máquina; hoy, cómo se despliega\n"
             "un sistema completo que se mantiene solo'.")

    n += 1
    s = content(prs, "Qué vamos a ver en esta parte", "Un tema del programa, pero el que más se parece al trabajo real", PART, n + 1)
    table(s, [["#", "Tema del programa", "Qué resuelve", "Min"],
              ["3.5", "Orquestación: Compose y Swarm", "Levantar y mantener un sistema de varios servicios", "40"],
              ["—", "Cierre de la unidad", "Repaso final, autoevaluación y rúbrica del proyecto", "15"]],
          0.45, 1.45, 12.4, col_w=[0.9, 4.6, 5.9, 1.0], size=13, row_h=0.5)
    callout(s, 0.45, 2.75, 6.1, 2.0, "El problema que ataca", [
        "Una app real = web + api + db + cache + worker.",
        "5 contenedores, 5 comandos, 5 redes… y algo falla a las 3 a.m.",
        "Un orquestador lo describe **una vez** y lo levanta siempre igual."], ORANGE, 12.5)
    callout(s, 6.78, 2.75, 6.1, 2.0, "Qué aporta (las 6 cosas del enunciado)", [
        "despliegue · escalado · descubrimiento de servicios",
        "balanceo de carga · auto-curación · **secretos**",
        "Las dos primeras son las que más se notan en la rúbrica."], TEAL, 12.5)
    callout(s, 0.45, 5.0, 12.4, 1.65, "Dónde encaja este laboratorio en la unidad", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Parte 1 (LAN y monitoreo) le da la red · ", {"size": 12.5}),
         ("Parte 2 (SSH y bastión) le da el acceso seguro", {"size": 12.5, "bold": True}),
         (" · y la Parte 3 le da la forma de producción. Es el último laboratorio de la unidad.", {"size": 12.5})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("El Proyecto Semestral se evalúa ", {"size": 12.5}),
         ("con esta misma rúbrica", {"size": 12.5, "bold": True}),
         (": 100 puntos entre las dos sesiones del Lab 12.", {"size": 12.5})]], NAVY, 12.5)
    notes(s, "⏱ 3-5 min · Agenda.\n\n"
             "Deja claro que esta es la parte con más peso en el proyecto: la rúbrica del Lab 12\n"
             "y la del Proyecto Semestral se parecen mucho.\n"
             "Las preguntas del Proyecto se responden con estos tres entregables en la mano.")

    n += 1
    s = divider(prs, "3.5", "Orquestación de servicios",
                "De «un contenedor que corro a mano» a «un sistema que se despliega solo»",
                ["Qué es orquestar y por qué dejó de ser opcional",
                 "Compose: un archivo que describe el sistema entero",
                 "Swarm: réplicas, balanceo, overlay y secretos"], "40 min")
    notes(s, "⏱ 5-6 min · Transición a 3.5.")

    n += 1
    s = content(prs, "Qué significa orquestar", "Un contenedor es fácil; un sistema con varios, no", PART, n + 1)
    text(s, 0.45, 1.3, 12.4, 0.35,
         [[("Un solo contenedor: ", {"size": 14, "bold": True, "color": GREEN}),
           ("`docker run` y listo. ", {"size": 14, "font": "Consolas"}),
           ("Cinco contenedores con dependencias: ", {"size": 14, "bold": True, "color": RED}),
           ("el orden importa, las redes importan, un reinicio a medias lo rompe todo.", {"size": 14, "color": TEXT})]])
    table(s, [["Herramienta", "Modelo", "Ejemplos"],
              ["Orquestador de VMs", "Máquina virtual", "VMware vCenter, Proxmox"],
              ["Orquestación en nube", "Infraestructura como servicio", "AWS EC2/ECS, Azure, GCP"],
              ["Orquestación de contenedores", "Contenedores", "Docker Compose, Docker Swarm, Kubernetes"]],
          0.45, 1.85, 12.4, col_w=[3.4, 3.4, 5.6], size=12.5, row_h=0.44)
    callout(s, 0.45, 3.6, 6.1, 2.4, "Las 6 capacidades del orquestador", [
        [("Despliegue", {"size": 12.5, "bold": True, "color": NAVY}), ("  ·  una definición, muchos hosts", {"size": 12.5})],
        [("Escalado", {"size": 12.5, "bold": True, "color": NAVY}), ("  ·  más réplicas sin tocar el código", {"size": 12.5})],
        [("Descubrimiento", {"size": 12.5, "bold": True, "color": NAVY}), ("  ·  «api» resuelve a la IP del contenedor", {"size": 12.5})],
        [("Balanceo", {"size": 12.5, "bold": True, "color": NAVY}), ("  ·  reparte tráfico entre réplicas", {"size": 12.5})],
        [("Auto-curación", {"size": 12.5, "bold": True, "color": NAVY}), ("  ·  reinicia el que muere", {"size": 12.5})],
        [("Secretos", {"size": 12.5, "bold": True, "color": NAVY}), ("  ·  contraseñas fuera del código y de la imagen", {"size": 12.5})]],
         ORANGE, 12.5)
    callout(s, 6.78, 3.6, 6.1, 2.4, "Por qué Docker NO es solo «un contenedor»", [
        "El enunciado del Proyecto pide **replicación de contenedores**.",
        "Y la rúbrica del Lab 12 califica `docker service scale` y el routing mesh.",
        "Es decir: **se evalúa orquestación, no solo ejecución**.",
        "Un `docker compose up` bien hecho ya es una parte; el resto es Swarm."], TEAL, 12.5)
    callout(s, 0.45, 6.15, 12.4, 1.05, "Idea ancla de toda la parte", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Compose responde «¿cómo levanto mi sistema?»  ·  Swarm responde «¿cómo lo mantengo "
          "funcionando si un nodo o un contenedor muere?».", {"size": 12.5, "bold": True})]], RED, 12.5)
    notes(s, "⏱ 6-11 min · Qué es orquestar.\n\n"
             "Pide un ejemplo de la vida real: un restaurante. Si un mesero cae, alguien más\n"
             "toma su mesa. Eso es auto-curación. Si el restaurante tiene que cerrar porque\n"
             "cayó el mesero, no hay orquestación.\n"
             "Las 6 capacidades de la caja izquierda son literalmente los ítems de la rúbrica.\n"
             "Merece la pena leerlas en voz alta: la evaluación las pide una por una.")

    n += 1
    s = content(prs, "Compose vs Swarm: no compiten entre sí", "Mismo archivo, distinto alcance", PART, n + 1)
    table(s, [["", "Docker Compose", "Docker Swarm"],
              ["Alcance", "Un solo host (dev / pruebas)", "Múltiples nodos (cluster)"],
              ["Réplicas", "`docker compose up --scale api=3`", "`docker service scale api=3`"],
              ["Redes", "Bridge por proyecto", "**Overlay** entre nodos"],
              ["Alta disponibilidad", "No", "Sí (roles manager / worker)"],
              ["Balanceo", "No (reparte por capacidades)", "Sí (**ingress mesh**)"],
              ["Secretos", "Archivo `.env` (simple)", "`docker secret` → `/run/secrets`"],
              ["Uso típico", "Desarrollo local", "Producción simple / on-prem"]],
          0.45, 1.35, 12.4, col_w=[2.6, 4.9, 4.9], size=12.5, row_h=0.42)
    callout(s, 0.45, 4.75, 6.1, 2.1, "La frase que resume la diferencia", [
        "Compose = **un** host que se sabe de memoria todo.",
        "Swarm = **varios** hosts que se descubren solos por la red overlay.",
        "El archivo es casi el mismo; el alcance es el que cambia."], ORANGE, 12.5)
    callout(s, 6.78, 4.75, 6.1, 2.1, "Cómo se usa en el Lab 12", [
        "Sesión A: stack `compose.yml` con `scale api=3` + `getent hosts api`.",
        "Sesión A: `swarm init` + servicio `web-mesh` con 3 réplicas.",
        "Sesión B: secretos, overlay, rolling update y `stack deploy`."], TEAL, 12.5)
    notes(s, "⏱ 11-16 min · Compose vs Swarm.\n\n"
             "Error clásico que conviene anticipar: 'Compose no sirve para producción'.\n"
             "La respuesta honesta: para una producción pequeña, on-prem, Swarm es suficiente.\n"
             "No es Kubernetes, y no pretende serlo; está en el programa porque es alcanzable.\n"
             "La tabla de arriba es la que hay que saber rellenar de memoria.")

    n += 1
    s = content(prs, "compose.yml: el sistema entero en un archivo", "Servicios, redes, volúmenes y dependencias — declarado una vez", PART, n + 1)
    code(s, 0.45, 1.35, 6.4, 4.2, [
        ("services:", ORANGE),
        ("  api:", NAVY),
        "    image: feria/api:1.0",
        ("    deploy:", NAVY),
        "      replicas: 3          # ← escalado",
        "    environment:",
        "      - DB_HOST=db",
        "    depends_on:",
        "      - db",
        "",
        ("  db:", NAVY),
        "    image: postgres:16",
        "    environment:",
        ("      - POSTGRES_PASSWORD_FILE=/run/secrets/db_pass", GREEN),
        "    secrets:",
        ("      - db_pass", GREEN),
        "",
        ("secrets:", ORANGE),
        ("  db_pass:", NAVY),
        ("    external: true", GREEN)], size=10.5)
    callout(s, 7.15, 1.35, 5.7, 1.95, "Lo que declara un compose", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("`services`", {"size": 12, "font": "Consolas", "color": NAVY, "bold": True}),
         (" — qué corre y con qué imagen", {"size": 12})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("`depends_on`", {"size": 12, "font": "Consolas", "color": NAVY, "bold": True}),
         (" — el orden de arranque", {"size": 12})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("`networks` / `volumes`", {"size": 12, "font": "Consolas", "color": NAVY, "bold": True}),
         (" — aislamiento y datos", {"size": 12})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("`secrets`", {"size": 12, "font": "Consolas", "color": NAVY, "bold": True}),
         (" — contraseñas fuera del YAML", {"size": 12, "bold": True})]], TEAL, 12)
    callout(s, 7.15, 3.55, 5.7, 1.6, "Por qué `DB_HOST=db` funciona", [
        "Compose crea una red propia del proyecto.",
        "El nombre del servicio es el **DNS** del otro contenedor.",
        "`api` no necesita saber la IP: escribe `db` y ya está."], ORANGE, 12.5)
    callout(s, 7.15, 5.4, 5.7, 1.6, "Escalado en una línea", [
        [("$ docker compose up -d --scale api=3", {"font": "Consolas", "size": 11, "color": NAVY, "bold": True})],
        [("$ getent hosts api", {"font": "Consolas", "size": 11, "color": NAVY, "bold": True}),
         ("   # devuelve 3 IPs", {"font": "Consolas", "size": 10.5, "color": SUB})],
        "Las 3 IPs son las 3 réplicas. Eso es la prueba del ítem de rúbrica."], TEAL, 12)
    notes(s, "⏱ 16-22 min · compose.yml.\n\n"
             "Este es el archivo que van a escribir en la Sesión A. Recórrelo línea por línea.\n"
             "Lo importante no es memorizar sintaxis: es entender que el archivo es la FUENTE\n"
             "de verdad del sistema. Si está en el archivo, se puede repetir.\n"
             "El descubrimiento por DNS (caja naranja) es el punto 'oh': no hay IP fijas.\n"
             "Advertencia técnica: `--scale` falla si el servicio declara `container_name`.")

    n += 1
    s = content(prs, "Los nodos de Swarm: manager y worker", "El cluster se administra desde los managers y ejecuta en los workers", PART, n + 1)
    code(s, 0.45, 1.4, 6.1, 1.9, [
        ("$ docker swarm init --advertise-addr 10.0.1.5", ORANGE),
        "  Swarm initialized: current node is a manager.",
        "",
        ("$ docker node ls", SUB),
        "  ID       HOST   STATUS   ROLES",
        "  x7f2a*   node1  Ready    manager",
        "  b31c9    node2  Ready    worker"], size=10.5)
    callout(s, 0.45, 3.55, 6.1, 2.9, "El rol manager", [
        "Recibe y guarda el **estado deseado** del cluster.",
        "Decide qué servicios corren y dónde.",
        "Es el que responde `docker service create`.",
        "Todos los managers se sincronizan entre sí."], ORANGE, 12.5)
    callout(s, 6.78, 1.4, 6.1, 2.2, "El rol worker", [
        "Solo ejecuta lo que el manager le ordena.",
        "No decide nada; no acepta despliegues.",
        "Un worker que muere: el manager pone la réplica en otro.",
        "Un manager que muere: otro manager lo puede promover."], TEAL, 12.5)
    table(s, [["Comparación", "Compose", "Swarm"],
              ["Alcance", "1 host", "N nodos"],
              ["Alta disponibilidad", "No", "Sí"],
              ["Balanceo", "No", "Ingress mesh"],
              ["Secretos", "`.env`", "`/run/secrets`"],
              ["Ideal para", "Desarrollo", "Producción simple"]],
          6.78, 3.85, 5.9, col_w=[2.3, 1.8, 1.8], size=11, row_h=0.42, header_h=0.4)
    notes(s, "⏱ 22-27 min · Nodos Swarm.\n\n"
             "La analogía que funciona: el manager es el jefe de sala (dice qué pasa),\n"
             "el worker es el mesero (obedece). Si muere un mesero, otro toma su mesa.\n"
             "Un dato útil: en Docker Desktop el nodo único es manager y worker a la vez.\n"
             "En el laboratorio probablemente sea un solo nodo, pero el concepto es el que se evalúa.\n"
             "Si hay tiempo, muestra `docker node ls` en vivo aunque sea un solo nodo.")

    n += 1
    s = content(prs, "Réplicas, routing mesh y auto-curación", "El corazón del tema 3.5: qué pasa cuando algo se muere", PART, n + 1)
    code(s, 0.45, 1.35, 6.4, 2.25, [
        ("$ docker service create --name web-mesh \\", ORANGE),
        ("    --replicas 3 -p 8080:80 feria/web:1.0", ORANGE),
        "",
        ("$ docker service ls", SUB),
        "  web-mesh  replicated  3/3  Running  1 minute ago",
        "",
        ("$ docker service ps web-mesh", SUB),
        ("  ID  NODE   IMAGE         STATE", NAVY),
        "  ..  node1  feria/web:1.0  Running",
        "  ..  node2  feria/web:1.0  Running",
        "  ..  node3  feria/web:1.0  Running"], size=10)
    flow(s, [("Cliente", "pide :8080"), ("Ingress mesh", "ruta virtual :8080"),
             ("Balanceo", "elige una réplica"), ("Respuesta", "convierte a la IP real")],
         0.45, 3.85, 12.4, h=0.95, colors=[BLUE, TEAL, ORANGE, GREEN], size=12)
    callout(s, 0.45, 5.0, 6.1, 1.85, "Qué es el routing mesh", [
        "Un puerto publicado **una sola vez** en el nodo.",
        "La red interna reparte entre las réplicas sin que tú lo configures.",
        "El balanceo ocurre en la capa de red, no en el código."], ORANGE, 12.5)
    callout(s, 6.78, 5.0, 6.1, 1.85, "Auto-curación: la demostración que impresiona", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Baja el número de réplicas: ", {"size": 12}),
         ("docker service scale web-mesh=2", {"size": 10.5, "font": "Consolas", "color": NAVY})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Mata un contenedor a la fuerza: ", {"size": 12}),
         ("docker kill <id>", {"size": 10.5, "font": "Consolas", "color": NAVY})],
        "El manager detecta la falta y crea otra: vuelve a 3/3 en segundos."], RED, 12)
    notes(s, "⏱ 27-33 min · Réplicas y routing mesh.\n\n"
             "Esta es la diapositiva que más impresiona si la demuestras en vivo:\n"
             "   curl -s localhost:8080 | grep server   (repite 5 veces, cambia el nodo)\n"
             "   docker service rm web-mesh.3            (y al rato, 3/3 otra vez)\n"
             "La analogía del ingress mesh: un número único en la puerta que tiene un portero\n"
             "que reparte a las mesas. Tú no llamas a cada mesa.\n"
             "Sin la demo en vivo, explica al menos qué hace el manager al detectar la baja.")

    n += 1
    s = content(prs, "Secretos: la contraseña fuera del código", "El ítem que más se olvida y más se pide", PART, n + 1)
    code(s, 0.45, 1.35, 6.1, 2.35, [
        ("$ docker secret create db_pass /ruta/credencial", ORANGE),
        "",
        ("$ docker service create --name db-swarm \\", ORANGE),
        ("    --secret db_pass \\", ORANGE),
        "    -e POSTGRES_PASSWORD_FILE=/run/secrets/db_pass \\",
        "    postgres:16",
        "",
        ("$ docker service exec db-srv cat /run/secrets/db_pass", SUB)], size=10)
    table(s, [["Dónde NO va la contraseña", "Por qué"],
              ["En el `Dockerfile` (`ENV`)", "Queda en la imagen; cualquiera que la use la ve"],
              ["En `compose.yml` en claro", "El archivo se versiona y termina en el repo"],
              ["En el comando de ejecución", "Queda en el historial de shell"],
              ["En una variable de build", "Se imprime en los logs de construcción"]],
          6.78, 1.35, 5.9, col_w=[2.5, 3.4], size=11, row_h=0.55, header_h=0.44)
    callout(s, 6.78, 4.15, 5.9, 2.65, "Cómo funciona el secreto en Swarm", [
        [("1. ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Se crea una vez y queda cifrado en el raft.", {"size": 12})],
        [("2. ", {"color": ORANGE, "bold": True, "size": 12}),
         ("El manager lo envía solo a quien lo pide.", {"size": 12})],
        [("3. ", {"color": ORANGE, "bold": True, "size": 12}),
         ("En el contenedor aparece como archivo en ", {"size": 12}),
         ("`/run/secrets/`", {"size": 11, "font": "Consolas", "color": NAVY, "bold": True})],
        [("4. ", {"color": ORANGE, "bold": True, "size": 12}),
         ("La app lo lee con la variable ", {"size": 12}),
         ("`_FILE`", {"size": 11, "font": "Consolas", "color": NAVY, "bold": True}),
         (", no con la contraseña.", {"size": 12})],
        "Se puede rotar sin reconstruir la imagen."], TEAL, 12)
    notes(s, "⏱ 33-37 min · Secretos.\n\n"
             "Este ítem vale 10 puntos solo en el Lab 12 y aparece en el proyecto.\n"
             "La idea que hay que transmitir: la contraseña NUNCA está en un archivo que se\n"
             "versiona. Un `git grep admin123` en el repo ya es un incidente de seguridad.\n"
             "El detalle técnico `_FILE` es lo que hace limpio el patrón: la app no recibe la\n"
             "contraseña por variable de entorno, la lee de un archivo montado.\n"
             "El detalle técnico `_FILE` es lo que hace limpio el patrón.")

    n += 1
    s = content(prs, "Actualizaciones continuas: rolling update y rollback", "Cambiar la versión sin caída, y volver atrás si algo sale mal", PART, n + 1)
    code(s, 0.45, 1.4, 6.4, 2.5, [
        ("$ docker service update --image feria/web:2.0 \\", ORANGE),
        ("    --update-parallelism 1 \\", ORANGE),
        "    --update-order start-first web-mesh",
        "",
        "#Swap automático: 1 antigua, 1 nueva, a la vez",
        "",
        ("$ docker service ps web-mesh", SUB),
        "  web-mesh.1  web:2.0  Running  0 seconds ago",
        "  web-mesh.2  web:2.0  Running  0 seconds ago",
        "  web-mesh.3  web:1.0  Running  1 minute ago",
        "",
        ("# Si la 2.0 sale mal:", GREEN),
        ("$ docker service rollback web-mesh", GREEN)], size=10)
    callout(s, 7.15, 1.4, 5.7, 1.95, "Actualización progresiva (rolling)", [
        "Nunca se tiran las 3 réplicas a la vez.",
        "Se reemplaza de a una; el servicio nunca se cae.",
        "Si una falla, el despliegue se detiene solo."], ORANGE, 12.5)
    callout(s, 7.15, 3.6, 5.7, 1.9, "Rollback: una orden, al estado anterior", [
        "Swarm guarda el estado previo de cada servicio.",
        "Volver atrás es tan simple como avanzar.",
        "Es la diferencia entre operar y administrar."], TEAL, 12.5)
    callout(s, 0.45, 4.2, 6.4, 2.6, "`stack deploy`: el archivo completo, a producción", [
        [("$ docker stack deploy -c compose.yml appfinal", {"font": "Consolas", "size": 11, "color": NAVY, "bold": True})],
        "Levanta el **sistema entero** (servicios + redes + secretos) con un comando.",
        "`docker stack ls` lo muestra como un solo conjunto.",
        "Es el entregable de la Sesión B del Lab 12.",
        "`docker stack rm appfinal` lo deshace completo."], NAVY, 12)
    notes(s, "⏱ 37-40 min · Rolling update y stack.\n\n"
             "Termina el tema 3.5 con la promesa que justify Swarm: se puede cambiar y volver atrás.\n"
             "La analogía: es un hotel con varias habitaciones; puedes remodelingar una a la vez\n"
             "y, si el resultado no gusta, volver a la habitación anterior.\n"
             "Si el tiempo está corto, prioriza `stack deploy` y el rollback; el rolling es el detalle.\n"
             "El rolling update es lo que evita la caída durante el cambio de versión.")

    # ---------------------------------------------------------------- cierre
    n += 1
    s = content(prs, "Cierre de la unidad y del proyecto", "Repaso final de las tres partes y qué se entrega", PART, n + 1)
    table(s, [["Parte", "Tema", "Concepto ancla", "Lab"],
              ["1", "3.1 · LAN", "Segmentar: la red se mide y se aísla", "Lab 10"],
              ["1", "3.2 · Monitoreo", "Mbits, latencia, jitter, pérdida", "Lab 10"],
              ["2", "3.3 · Claves SSH", "La privada no sale; la pública autoriza", "Lab 11"],
              ["2", "3.4 · Bastión", "Una sola puerta; interna sin salida", "Lab 11"],
              ["3", "3.5 · Orquestación", "Un archivo, N réplicas, auto-curación", "Lab 12"]],
          0.45, 1.4, 12.4, col_w=[0.9, 2.9, 6.1, 1.5], size=12.5, row_h=0.44)
    callout(s, 0.45, 4.35, 6.1, 2.5, "Los 4 entregables del proyecto (Avances 1-4)", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Avance 1: ", {"size": 12, "bold": True}),
         ("LAN, subredes VLSM, DHCP/DNS/NAT", {"size": 12})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Avance 2: ", {"size": 12, "bold": True}),
         ("Bastión dual-homed + app interna sin exposición", {"size": 12})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Avance 3: ", {"size": 12, "bold": True}),
         ("Claves SSH funcionando (sin contraseñas)", {"size": 12})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Avance 4: ", {"size": 12, "bold": True}),
         ("Orquestación: réplicas, secretos y stack", {"size": 12})]], NAVY, 12)
    callout(s, 6.78, 4.35, 6.1, 2.5, "El hilo que lo cose todo", [
        "**Segmentar** (3.1) para que la red sea medible y segura.",
        "**Proteger el acceso** (3.3) con llaves, no con secretos.",
        "**Exponer solo lo necesario** (3.4) detrás de un bastión.",
        "**Escalar sin rehacer** (3.5) con réplicas y secretos.",
        "Todo lo anterior, medido (3.2) con las cuatro métricas."], TEAL, 12.5)
    notes(s, "⏱ 40-48 min · Cierre de la unidad.\n\n"
             "Diapositiva de consolidación: vuelve a las 5 ideas y las amarra.\n"
             "Si tienes que resumir la unidad en una frase: 'una red que se segmenta, se protege,\n"
             "se expone por un solo punto y se mantiene sola'.\n"
             "La tabla de la izquierda es un buen resumen para el examen.\n"
             "Repasa que el hilo narrativo sea: se segmenta, se protege, se expone poco, se escala.")

    n += 1
    s = content(prs, "Autoevaluación y cierre", "Diez preguntas para comprobar que la unidad quedó", PART, n + 1)
    callout(s, 0.45, 1.4, 6.1, 4.0, "Repaso por tema (responde en voz alta)", [
        [("3.1 · ", {"color": ORANGE, "bold": True, "size": 12}),
         ("¿Por qué una LAN plana se degrada al crecer?", {"size": 12})],
        [("3.2 · ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Diferencia latencia, jitter y pérdida.", {"size": 12})],
        [("3.3 · ", {"color": ORANGE, "bold": True, "size": 12}),
         ("¿Por qué el servidor nunca guarda la contraseña?", {"size": 12})],
        [("3.4 · ", {"color": ORANGE, "bold": True, "size": 12}),
         ("¿Qué gana un dual-homed frente a uno single-homed?", {"size": 12})],
        [("3.5 · ", {"color": ORANGE, "bold": True, "size": 12}),
         ("¿Qué problema resuelve el routing mesh?", {"size": 12})],
        [("3.5 · ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Diferencia entre `scale` de Compose y de Swarm.", {"size": 12})],
        [("3.5 · ", {"color": ORANGE, "bold": True, "size": 12}),
         ("¿Por qué la contraseña va en `/run/secrets/` y no en el YAML?", {"size": 12})],
        [("— · ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Nombra las 4 métricas de red del tema 3.2.", {"size": 12})]], ORANGE, 12)
    callout(s, 6.78, 1.4, 6.1, 2.6, "Cómo se evalúa (para que no haya sorpresas)", [
        "Unidad III = Lab 10 + Lab 11 + Lab 12 (100 pts c/u).",
        "El Proyecto Semestral usa rúbrica aparte, **por avances**.",
        "Se entrega: compose.yml, stack.yml, evidencias de réplicas,",
        "capturas de SSH por llave, tabla de comparación y reflexión."], TEAL, 12.5)
    callout(s, 6.78, 4.25, 6.1, 2.6, "Para la próxima clase", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Trae ", {"size": 12}),
         ("compose.yml", {"size": 11.5, "font": "Consolas", "color": NAVY, "bold": True}),
         (" y ", {"size": 12}),
         ("stack.yml", {"size": 11.5, "font": "Consolas", "color": NAVY, "bold": True}),
         (" funcionando.", {"size": 12})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Trae las dos capturas de SSH (con y sin llave autorizada).", {"size": 12})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Repasa los comandos: ", {"size": 12}),
         ("`scale`, `service update`, `rollback`, `stack deploy`", {"size": 11, "font": "Consolas", "color": NAVY})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Dudas antes de empezar: es más barato que reprobar.", {"size": 12})]], NAVY, 12)
    notes(s, "⏱ 48-55 min · Autoevaluación y cierre.\n\n"
             "Deja que respondan en voz alta: la pregunta de 'difference entre scale de Compose y\n"
             "de Swarm' es la que mejor separa a quien entendió de quien memorizó.\n"
             "Lee la caja de abajo con calma: es la lista de tareas para la próxima clase y\n"
             "evita que el cierre termine en un 'nos vemos' sin rumbo.")

    prs.save(out)
    return out


if __name__ == "__main__":
    p = build(sys.argv[1] if len(sys.argv) > 1 else "Teoria-U3-Parte3-Orquestacion.pptx")
    print("OK ->", p)
