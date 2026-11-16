"""Unidad III · Sesión de cierre — DevOps: el despliegue del viernes · 55 min."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ppt_kit import *  # noqa

PART = "Sesión DevOps · el despliegue del viernes"


def build(out):
    prs = new_deck()
    n = 0

    s = cover(prs, "UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES",
              "Unidad III — Sesión de cierre",
              "DevOps sobre la red: el despliegue del viernes",
              ["Qué es DevOps: una definición que no nombra herramientas",
               "El caso: un despliegue manual que costó 3 h 50 min de servicio",
               "El pipeline y su tráfico: puertos, NAT, DNS y rollback en dos comandos"],
              "Sesión de cierre", "55 min de teoría")
    notes(s, "⏱ 0-2 min · Portada.\n\n"
             "Abrir con la promesa: 'hoy no hay herramienta nueva; hoy el sistema que ya\n"
             "construyeron recorre el camino hasta producción y aprende a volver atrás'.\n"
             "Aclarar de entrada que sigue siendo una clase de redes: lo que se va a mirar\n"
             "es el tráfico del despliegue, no una moda de la industria.")

    n += 1
    s = content(prs, "Qué vamos a ver", "Un caso real, una definición y el camino del código a producción", PART, n + 1)
    table(s, [["#", "Bloque", "La pregunta que responde", "Min"],
              ["1", "¿Qué es DevOps?", "¿Por qué el mismo deploy sale distinto cada vez?", "14"],
              ["2", "El caso del viernes", "¿Qué le faltaba al despliegue de PagosYA?", "14"],
              ["3", "El pipeline y su red", "¿Qué puerto, en qué dirección, y cómo se vuelve atrás?", "22"],
              ["4", "Medir y cerrar", "¿Cómo sabemos que mejoró?", "5"]],
           0.45, 1.35, 12.4, col_w=[0.8, 3.6, 7.0, 1.0], size=12.5, row_h=0.46)
    callout(s, 0.45, 3.9, 12.4, 2.6, "La regla de esta sesión", [
        "**Sigue siendo un curso de redes.** El pipeline es el escenario; el tema es el tráfico.",
        "Cada etapa es un flujo con **origen, destino, puerto y cifrado**.",
        "Cada falla del caso es una **decisión de red** mal tomada: un puerto, una ruta, una versión.",
        "**No se evalúa** memorizar comandos: se evalúa saber qué se abrió y por qué."], ORANGE, 12.5)
    notes(s, "⏱ 2-4 min · Agenda.\n\n"
             "Enuncia los cuatro bloques y el peso: el caso ocupa tanto como la definición\n"
             "porque el caso ES la clase. Si el tiempo aprieta, el bloque 4 se recorta a\n"
             "una frase: 'se mide con DORA'.")

    n += 1
    s = divider(prs, "DevOps", "¿Qué es DevOps, en serio?",
                "Antes de pipeline, registry y métricas: el acuerdo",
                ["Las 3 vías: flujo, retroalimentación, aprendizaje",
                 "La prueba de fuego del martes a las 4 de la tarde",
                 "Lo que DevOps NO es"], "14 min")
    notes(s, "⏱ 4-5 min · Transición al bloque 1.")

    n += 1
    s = content(prs, "DevOps no es una herramienta", "Es un acuerdo sobre cómo se cambia un sistema en producción", PART, n + 1)
    flow(s, [("Planear", "qué cambia"), ("Construir", "build"), ("Probar", "test"),
             ("Desplegar", "deploy"), ("Operar", "corre"), ("Medir", "DORA")],
         0.45, 1.35, 12.4, h=0.95, colors=[BLUE, TEAL, GREEN, ORANGE, NAVY, RED], size=11.5)
    callout(s, 0.45, 2.5, 6.1, 2.05, "La definición que sirve", [
        "El **mismo cambio** se despliega **igual** todas las veces.",
        "Se **mide**: hay una prueba que dice si sirve.",
        "Se puede **revertir** sin drama.",
        "Si depende de una persona o de una laptop, no es DevOps."], ORANGE, 12.5)
    callout(s, 6.78, 2.5, 6.1, 2.05, "Las 3 vías (la parte cultural)", [
        "**Flujo:** cambios pequeños y frecuentes.",
        "**Retroalimentación:** cada etapa avisa en segundos.",
        "**Aprendizaje:** el fallo se documenta y se automatiza la lección.",
        "Nada de esto se compra: se acuerda."], TEAL, 12.5)
    callout(s, 0.45, 4.7, 12.4, 1.55, "Lo que DevOps NO es", [
        "No es Kubernetes, ni una herramienta de moda, ni «el equipo de DevOps».",
        "En esta clase se hace **a mano y con Docker**, que ya saben: `git`, `build`, `push`, `compose`, `curl`."], RED, 12.5)
    notes(s, "⏱ 5-13 min · Qué es DevOps.\n\n"
             "Empieza por el ciclo de arriba, pero sin software: 'planear, construir, probar,\n"
             "desplegar, operar, medir' es lo que hace un restaurante todas las noches.\n"
             "La definición hay que leerla despacio; la frase que más discusión genera es\n"
             "la última: 'si depende de una persona, no es DevOps'.\n"
             "Las 3 vías en versión de clase, sin nombres de libros.\n"
             "Cierra con el NO: desmonta la idea de que DevOps es un puesto de trabajo.")

    n += 1
    s = content(prs, "La prueba de fuego", "¿Puedes desplegar un martes a las 4 de la tarde y salir tranquilo?", PART, n + 1)
    table(s, [["Pregunta", "Viernes (manual)", "Con pipeline"],
              ["¿Qué versión corre?", "No se sabe", "El tag del commit"],
              ["¿Quién detecta el fallo?", "El cliente", "El smoke test"],
              ["¿Cuánto tarda el rollback?", "3 h 50 min", "≈ 2 s"],
              ["¿Se pierde dato al volver?", "Sí: 8 horas", "No"],
              ["¿Se repite igual?", "Depende de quién", "Es una lista de comandos"]],
           0.45, 1.35, 12.4, col_w=[4.4, 4.2, 3.8], size=12.5, row_h=0.5)
    callout(s, 0.45, 4.55, 12.4, 1.9, "La idea que ordena todo lo demás", [
        [("▸ ", {"color": NAVY, "bold": True, "size": 13}),
         ("DevOps no se nota cuando todo va bien: se nota cuando hay que volver atrás.",
          {"size": 13, "bold": True})],
        "Y volver atrás rápido no es suerte: es tener la versión anterior a un `pull` de distancia."], NAVY, 12.5)
    notes(s, "⏱ 13-18 min · La prueba de fuego.\n\n"
             "Esta tabla es el resumen del caso que viene; úsala como promesa, no como\n"
             "respuesta. Pregunta al grupo: '¿alguno desplegó algo un viernes?'.\n"
             "La caja azul es la frase que se llevan.")

    n += 1
    s = divider(prs, "Caso", "El despliegue del viernes",
                "PagosYA · tres personas · un servidor · ningún pipeline",
                ["15:30 merge · 16:10 despliegue · 16:20 primer 502",
                 "17:00 «volver atrás» sin versión anterior",
                 "20:10 estable: 3 h 50 min caído"], "14 min")
    notes(s, "⏱ 18-19 min · Transición al caso.\n\n"
             "Decir que el caso es real en su forma: no importa la empresa, importa la\n"
             "secuencia. Si alguien reconoce su propio trabajo, mejor.")

    n += 1
    s = content(prs, "PagosYA: el sistema y la costumbre", "La API de pagos del Caso 2, ahora con clientes de verdad", PART, n + 1)
    kpi(s, [("3", "personas en el equipo"), ("1", "servidor con Docker"),
            ("0", "pipelines"), ("8", "meses funcionando así")],
        0.45, 1.35, 12.4)
    callout(s, 0.45, 2.65, 6.1, 2.3, "El sistema", [
        "`nginx` delante, la API de pagos detrás.",
        "PostgreSQL con su volumen `pgdata`.",
        "Un `compose.yml` y un servidor: nada más."], TEAL, 12.5)
    callout(s, 6.78, 2.65, 6.1, 2.3, "La costumbre (8 meses)", [
        "Ana entra por SSH.",
        "`git pull` y `docker compose up -d --build`.",
        "«Si funciona en mi máquina, funciona».",
        "El despliegue **es** la persona."], ORANGE, 12.5)
    callout(s, 0.45, 5.15, 12.4, 1.2, "La deuda invisible", [
        "Funciona mientras nadie tenga prisa. El día que falla no hay versión anterior, ni prueba automática, ni registro de lo que corría."],
        NAVY, 12.5)
    notes(s, "⏱ 19-22 min · Contexto.\n\n"
             "Subraya los dos KPIs que importan: 1 servidor (no hay redundancia) y 0\n"
             "pipelines (todo pasa por manos). Los otros dos son contexto.\n"
             "La deuda invisible es el concepto: el costo no se paga hasta el incidente.")

    n += 1
    s = content(prs, "La bitácora", "Viernes 8 de noviembre · de 15:30 a 20:10", PART, n + 1)
    table(s, [["Hora", "Qué pasó"],
              ["15:30", "Se fusiona el PR «descuentos de temporada» a `main`."],
              ["15:45", "Ana construye la imagen **en su laptop** y copia el `compose.yml`."],
              ["16:10", "Servidor: `git pull` + `compose up -d --build`. La app arranca y se cae."],
              ["16:20", "Primer cliente: **502** al pagar. `nginx` no tiene a quién reenviar."],
              ["16:35", "La app **reinicia en bucle**: dependencias no fijadas."],
              ["17:00", "«Volver atrás»: no hay versión anterior, todo era `latest`."],
              ["17:40", "Reconstruir el commit viejo falla: no compila con las deps de hoy."],
              ["18:30", "Restauran el backup de las 2:00 a. m.: **8 horas de pagos perdidas**."]],
           0.45, 1.35, 12.4, col_w=[1.2, 11.2], size=12, row_h=0.36)
    callout(s, 0.45, 4.75, 12.4, 1.6, "20:10 · servicio estable", [
        [("▸ ", {"color": RED, "bold": True, "size": 13}),
         ("Tiempo total caído: **3 h 50 min**. El código del PR no era el problema.", {"size": 13, "bold": True})],
        "El problema fue que el despliegue no era una operación repetible."], RED, 12.5)
    notes(s, "⏱ 22-28 min · La bitácora.\n\n"
             "Léela como una historia, no como una tabla: 15:30 es una decisión normal;\n"
             "16:20 es el cliente enterándose primero; 17:00 es el momento en que se dan\n"
             "cuenta de que no tienen a dónde volver.\n"
             "Pausa en 17:40: 'no compila' es la prueba de que construir desde el código no\n"
             "es lo mismo que desplegar un artefacto.\n"
             "No avances sin que alguien diga en voz alta qué pieza faltaba.")

    n += 1
    s = content(prs, "Lo que la bitácora revela", "Tres piezas que faltaban — y una consecuencia que se paga con datos", PART, n + 1)
    callout(s, 0.45, 1.35, 3.95, 3.0, "Faltaba un tag inmutable", [
        "Todo se publicaba como `latest`.",
        "«La versión que corre» era una suposición.",
        "Un tag por commit la vuelve un hecho."], ORANGE, 12)
    callout(s, 4.65, 1.35, 3.95, 3.0, "Faltaba un smoke test", [
        "Lo detectó un cliente, no el sistema.",
        "`docker ps` decía `Up` mientras nadie pagaba.",
        "La puerta es la respuesta, no el proceso."], TEAL, 12)
    callout(s, 8.85, 1.35, 3.95, 3.0, "Faltaba el registro", [
        "Nadie sabía cuál era la última buena.",
        "Sin registro no hay rollback: hay arqueología.",
        "Un archivo `.last-good` lo resuelve."], NAVY, 12)
    callout(s, 0.45, 4.55, 12.4, 1.75, "Y la consecuencia que sí se paga", [
        [("▸ ", {"color": RED, "bold": True, "size": 12.5}),
         ("Sin rollback de la aplicación, «volver atrás» fue restaurar la base: **8 horas de pagos**. El dato no es desechable (Parte 4).",
          {"size": 12.5, "bold": True})]], RED, 12.5)
    notes(s, "⏱ 28-33 min · El diagnóstico.\n\n"
             "Pide las tres piezas antes de mostrarlas: casi siempre sale 'un backup' o\n"
             "'probar mejor', que son síntomas, no la causa.\n"
             "Aquí se enlaza con la Parte 4: el respaldo existe para desastres, no para\n"
             "cada despliegue. Si el plan de vuelta es un backup, el diseño está mal.")

    n += 1
    s = divider(prs, "Pipeline", "Del commit a producción",
                "Siete etapas, diez comandos y cinco flujos de red",
                ["Build once, deploy everywhere",
                 "El smoke test es la puerta",
                 "El rollback elige una imagen que ya existe"], "22 min")
    notes(s, "⏱ 33-34 min · Transición al bloque técnico.")

    n += 1
    s = content(prs, "Las 7 etapas", "Cada etapa deja una evidencia que se puede comprobar", PART, n + 1)
    table(s, [["#", "Etapa", "Qué garantiza", "Evidencia"],
              ["1", "Commit", "El cambio está identificado", "`git rev-parse --short HEAD`"],
              ["2", "Build", "La imagen sale del repo, no de una laptop", "`docker build -t ...:$TAG`"],
              ["3", "Test", "El artefacto es el que dice ser", "`docker run ... cat /app/VERSION`"],
              ["4", "Registry", "El artefacto es inmutable y reutilizable", "`docker push` · `v2/_catalog`"],
              ["5", "Deploy", "Se despliega un tag explícito, no `latest`", "`TAG=$TAG compose up -d`"],
              ["6", "Smoke", "Responde como usuario, no solo «arrancó»", "`curl localhost:8080/`"],
              ["7", "Registro", "Hay una versión anterior conocida", "`echo $TAG > .last-good`"]],
           0.45, 1.35, 12.4, col_w=[0.6, 2.0, 5.7, 4.1], size=11.5, row_h=0.4)
    callout(s, 0.45, 4.75, 12.4, 1.5, "El pipeline no es magia", [
        "Son estos comandos, pegados en orden. Lo que agrega es que corren **igual** a las 3 de la mañana, sin depender de quién esté despierto."],
        ORANGE, 12.5)
    notes(s, "⏱ 34-39 min · Las 7 etapas.\n\n"
             "Recorre la columna 'Evidencia': cada etapa se puede comprobar sin creerle a\n"
             "nadie. Ese es el punto de la clase.\n"
             "La 3 es la que suele faltar en los proyectos: 'probé en mi máquina' no es test\n"
             "del artefacto.\n"
             "Si hay tiempo, muestra el comando 1 y el 7 en pantalla: son una línea cada uno.")

    n += 1
    s = content(prs, "El mapa de tráfico del despliegue", "Cinco flujos: si uno se bloquea, el pipeline se cae en esa etapa", PART, n + 1)
    table(s, [["Flujo", "Origen → destino", "Puerto / protocolo", "Si se bloquea"],
              ["Código", "tu host → servidor Git", "22 o 443/TCP", "no hay commit"],
              ["Push", "daemon → registry", "5000/TCP", "el artefacto no sale"],
              ["Pull", "servidor → registry", "5000/TCP", "no encuentra la imagen"],
              ["Servicio", "cliente → app publicada", "8080 → 8000 · **NAT**", "RST; con proxy, 502"],
              ["Interno", "app → db", "5432/TCP · DNS `db`", "arranca y falla al conectar"]],
           0.45, 1.35, 12.4, col_w=[1.9, 4.4, 3.5, 2.6], size=12, row_h=0.5)
    callout(s, 0.45, 4.5, 12.4, 1.9, "Los errores también son de red", [
        "`connection refused` = nadie escucha · `timeout` = algo descarta · `502` = el proxy no tiene upstream sano.",
        [("▸ ", {"color": NAVY, "bold": True, "size": 12.5}),
         ("En esta demo se ejercitan los flujos 2, 3 y 4; el 1 y el 5 ya los vieron en el Lab 14.",
          {"size": 12.5, "bold": True})]], NAVY, 12.5)
    notes(s, "⏱ 39-44 min · El mapa de tráfico.\n\n"
             "Esta es la lámina que justifica la sesión en el pénsum. Lee la fila 4 dos\n"
             "veces: es el mismo NAT de la Unidad II, con otra tabla.\n"
             "Pregunta: '¿quién inicia cada conexión?'. Ningún servicio empuja: alguien abre\n"
             "la conexión. Por eso un firewall que bloquea la salida rompe el deploy igual\n"
             "que uno que bloquea la entrada.")

    n += 1
    s = content(prs, "La red detrás del despliegue", "Donde el pipeline deja de ser DevOps y vuelve a ser el curso", PART, n + 1)
    callout(s, 0.45, 1.35, 6.1, 2.35, "8080 → 8000 es DNAT", [
        "El puerto del host se traduce al del contenedor.",
        "Se ve con `docker port`.",
        "Es el NAT de la Unidad II: otra tabla, otro comando."], TEAL, 12.5)
    callout(s, 6.78, 1.35, 6.1, 2.35, "`localhost` es loopback", [
        "`127.0.0.1`: no pasa por la tarjeta de red.",
        "No se alcanza desde otra máquina.",
        "Por eso el registry de clase no necesita DNS."], ORANGE, 12.5)
    callout(s, 0.45, 3.9, 6.1, 2.15, "Pregunta que ordena todo", [
        "**¿Quién inicia la conexión?**",
        "Push y pull: el daemon. Smoke: el cliente.",
        "Hacia la db: la app.",
        "Sin conexión abierta no hay tráfico."], NAVY, 12.5)
    code(s, 6.78, 3.9, 6.1, 1.05, [
        ("$ docker port pagosya-devops-api-1", ORANGE),
        "8000/tcp -> 0.0.0.0:8080",
        ("$ ss -ltnp | grep :8080", ORANGE),
        "LISTEN 0.0.0.0:8080"], size=10)
    callout(s, 6.78, 5.1, 6.1, 0.95, "Regla y hecho", [
        "`docker port` muestra la **regla**; `ss` muestra el **hecho**. Si no coinciden, el despliegue miente."],
        RED, 12)
    notes(s, "⏱ 44-48 min · La red.\n\n"
             "La caja de la pregunta es la evaluación: si el estudiante no sabe quién\n"
             "inicia la conexión, no entendió el flujo.\n"
             "Menciona el `-p 127.0.0.1:5000:5000`: el registry de clase queda solo local;\n"
             "con `-p 5000:5000` queda expuesto en toda la máquina. Es segmentación (3.1).\n"
             "No te detengas en TLS: se nombra y se sigue.")

    n += 1
    s = content(prs, "El rollback: dos comandos", "La versión anterior ya existe en el registry: no se reconstruye", PART, n + 1)
    code(s, 0.45, 1.35, 6.4, 3.0, [
        ("$ cat .last-good", ORANGE),
        "0311133",
        ("", WHITE),
        ("$ TAG=$(cat .last-good)", ORANGE),
        ("$ TAG=$TAG docker compose up -d", ORANGE),
        " Container pagosya-devops-api-1 Started",
        ("", WHITE),
        ("# dos segundos después", GREEN),
        ("$ curl localhost:8080/", ORANGE),
        "PagosYA api 0311133"], size=11)
    code(s, 7.15, 1.35, 5.7, 1.55, [
        ("$ curl -s localhost:5000/v2/pagosya-api/tags/list", ORANGE),
        "{\"name\":\"pagosya-api\",\"tags\":", 
        " [\"0311133\",\"faf2193\"]}"], size=10)
    callout(s, 7.15, 3.1, 5.7, 1.25, "La versión mala no se borra", [
        "Queda en el registry como evidencia.",
        "Auditar es listar tags, no adivinar."], TEAL, 12)
    callout(s, 0.45, 4.55, 12.4, 1.75, "Volver atrás es elegir, no reconstruir", [
        [("▸ ", {"color": NAVY, "bold": True, "size": 13}),
         ("Por eso tarda segundos y no 3 h 50 min: el artefacto ya está a un `pull` de distancia.", {"size": 13, "bold": True})],
        "`rollback.sh` no consulta al sistema roto: lee un archivo. Si el sistema caído dictara cómo volver, el rollback caería con él."], NAVY, 12.5)
    notes(s, "⏱ 48-51 min · El rollback.\n\n"
             "Si hay proyector y Docker, ejecuta los comandos: el 'Started' en segundos es\n"
             "más elocuente que cualquier lámina.\n"
             "El detalle del archivo es intencional: un rollback no debe depender de la\n"
             "disponibilidad del sistema que está fallando.\n"
             "La lista de tags cierra el argumento: la versión mala sigue ahí, pero no\n"
             "está sirviendo.")

    n += 1
    s = content(prs, "Medir: las 4 claves DORA", "Lo que no se mide no se mejora — y el pipeline deja la medida gratis", PART, n + 1)
    kpi(s, [("Frecuencia", "cada commit"), ("Lead time", "minutos"),
            ("Tasa de fallo", "la decide el smoke"), ("MTTR", "≈ 2 s")],
        0.45, 1.35, 12.4)
    callout(s, 0.45, 2.65, 6.1, 3.4, "Qué mide cada una", [
        "**Frecuencia:** cada cuánto se pone algo en producción.",
        "**Lead time:** del commit al usuario.",
        "**Tasa de fallo:** % de despliegues que no pasan la puerta.",
        "**MTTR:** de la falla al servicio sano.",
        "Antes: 1 al mes · días · 1 de 1 · 3 h 50 min."], ORANGE, 12.5)
    callout(s, 6.78, 2.65, 6.1, 3.4, "El hilo de redes", [
        "El **lead time** es, en buena parte, **tiempo de red**: subir y bajar la imagen.",
        "El **smoke test** es una medición de 3.2 aplicada a un despliegue.",
        "El **MTTR** bajo es tener el artefacto anterior a un `pull`.",
        "Las cuatro se mejoran acortando el camino, no comprando herramientas."], TEAL, 12.5)
    notes(s, "⏱ 51-54 min · DORA.\n\n"
             "No nombres el libro si no hace falta: las cuatro se explican solas.\n"
             "La comparación 'antes/después' es la que se lleva al Proyecto: no se pide\n"
             "número exacto, se pide tendencia y por qué.\n"
             "Cierra el enlace con 3.2: el smoke es monitoreo aplicado a un despliegue.")

    n += 1
    s = content(prs, "Qué se lleva de la sesión", "Tres ideas, un entregable y una práctica", PART, n + 1)
    callout(s, 0.45, 1.35, 3.95, 3.1, "El despliegue es una operación", [
        "Si depende de una persona o de una laptop, no es repetible.",
        "Un tag por commit le pone nombre a lo que corre.",
        "Y ese nombre viaja: **build once**."], ORANGE, 12)
    callout(s, 4.65, 1.35, 3.95, 3.1, "La puerta es la respuesta", [
        "`docker ps` dice que el proceso existe.",
        "El smoke dice que el sistema sirve.",
        "Solo el segundo decide si el despliegue pasó."], TEAL, 12)
    callout(s, 8.85, 1.35, 3.95, 3.1, "Volver es elegir", [
        "La versión anterior está en el registry.",
        "`.last-good` dice cuál es.",
        "Dos comandos; cero reconstrucción."], NAVY, 12)
    callout(s, 0.45, 4.65, 12.4, 1.75, "Entregable y siguiente paso", [
        "**Bitácora de los 10 comandos + mapa de los 5 flujos + postmortem de una página.**",
        "Es, literalmente, el **manual de despliegue** que pide la rúbrica del Proyecto Final.",
        "Siguiente: la práctica — estos comandos, en su terminal, hasta romperlo y volver."], ORANGE, 12.5)
    notes(s, "⏱ 54-55 min · Cierre.\n\n"
             "Lee las tres cajas como las tres frases que deben poder repetir.\n"
             "El entregable se explica en una línea: la bitácora es el manual.\n"
             "No cierres con '¿preguntas?': cierra con la práctica y el primer comando.")

    prs.save(out)
    return out


if __name__ == "__main__":
    p = build(sys.argv[1] if len(sys.argv) > 1 else "Teoria-DevOps-Despliegue.pptx")
    print("OK ->", p)
