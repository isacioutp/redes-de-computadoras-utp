"""Unidad III · Parte 2 — Claves SSH y servidores bastión (temas 3.3 y 3.4) · 55 min."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ppt_kit import *  # noqa

PART = "Parte 2 · SSH y bastión"


def build(out):
    prs = new_deck()
    n = 0

    s = cover(prs, "UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES",
              "Unidad III — Parte 2",
              "Claves SSH y servidores bastión",
              ["Tema 3.3 · Creación y administración de claves SSH",
               "Tema 3.4 · Servidores bastión: single-homed, dual-homed, multihomed",
               "Laboratorio N.º 11 · Semana 11 · 2 sesiones"],
              "Parte 2 de 3", "2 h 45 min de clase (3 partes de 55 min)")
    notes(s, "⏱ 0-3 min · Apertura de la Parte 2.\n\n"
             "Enlace con la Parte 1: la LAN ya existe y hay un segmento de administración (10.0.3.0/28).\n"
             "La pregunta de hoy: ¿cómo entro a esos servidores de forma segura y que quede registro?\n"
             "Respuesta corta que se va a desarrollar: sin contraseñas, con llaves; y con un bastión de por medio.\n"
             "Este es el bloque de seguridad de la unidad y el más pedido en el Proyecto Semestral.")

    n += 1
    s = content(prs, "Qué vamos a ver en esta parte", "Dos temas del programa: autenticación segura y control de acceso", PART, n + 1)
    table(s, [["#", "Tema del programa", "Pregunta que responde", "Min"],
              ["3.3", "Claves SSH (pública / privada)", "¿Cómo me autentico sin escribir ni guardar contraseñas?", "22"],
              ["3.4", "Servidores bastión", "¿Cómo hago que la red interna no quede expuesta?", "23"],
              ["—", "Cierre y repaso", "Preguntas y repaso previo a la práctica del Lab 11", "10"]],
          0.45, 1.45, 12.4, col_w=[0.8, 3.9, 6.7, 1.0], size=13, row_h=0.5)
    callout(s, 0.45, 3.75, 6.1, 1.75, "Por qué importa (objetivo del programa)", [
        "El objetivo general dice: *conexiones seguras a servidores remotos*.",
        "El enunciado del proyecto **prohíbe** contraseñas en el código.",
        "Una contraseña compartida se filtra, no se rota, no se audita."], ORANGE, 12.5)
    callout(s, 6.78, 3.75, 6.1, 1.75, "Qué se entregan (Lab 11)", [
        "Llave pública funcionando: acceso **sin contraseña** (captura).",
        "Un bastión dual-homed protegiendo la red interna.",
        "Evidencia del túnel o del proxy inverso."], TEAL, 12.5)
    callout(s, 0.45, 5.65, 12.4, 1.05, "El ataque que estamos evitando", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Un atacante encuentra el puerto 22 abierto, prueba usuario/contraseña por fuerza bruta y entra. "
          "Con llaves, ", {"size": 12.5}),
         ("aunque el puerto esté abierto, no puede autenticarse", {"size": 12.5, "bold": True}),
          (" sin tu archivo privado — que nunca sale de tu máquina.", {"size": 12.5})]], RED, 12.5)
    notes(s, "⏱ 3-5 min · Agenda.\n\n"
             "No le des más de 2 min a la agenda; la Parte 2 es densa.\n"
             "La caja roja es el argumento de venta: SSH por llave no es solo cómodo, es lo que hace\n"
             "imposible un brute force exitoso aunque el puerto esté expuesto.\n"
             "Enfoca el ataque en que el puerto 22 abierto NO es el problema:\n"
             "con llaves, un atacante puede probar pares de llaves todo el día sin éxito.")

    # ---------------------------------------------------------------- 3 sección 3.3
    n += 1
    s = divider(prs, "3.3", "Claves SSH", "Autenticarte con criptografía en vez de con un secreto que se puede copiar",
                ["El problema de la contraseña compartida",
                 "Par de llaves: qué es la pública y qué es la privada",
                 "ssh-keygen, permisos correctos y acceso sin contraseña"], "22 min")
    notes(s, "⏱ 5-6 min · Transición a 3.3.")

    n += 1
    s = content(prs, "El problema de la contraseña", "Tres razones por las que una contraseña no sirve para administrar servidores", PART, n + 1)
    table(s, [["Problema", "Qué pasa en la práctica", "Consecuencia"],
              ["Se comparte", "Varias personas usan la misma clave", "Alguien se va y nadie rota nada"],
              ["Se filtra", "Phishing, listas filtradas, una máquina comprometida", "Acceso del atacante"],
              ["No se audita", "El servidor solo ve «un usuario entró»", "No sabes quién fue ni qué hizo"],
              ["Se reescribe", "En papel, en un chat, en un correo", "Volante por la red"]],
          0.45, 1.45, 12.4, col_w=[2.0, 5.6, 4.8], size=12.5, row_h=0.46)
    callout(s, 0.45, 4.2, 6.1, 2.1, "La idea que resuelve todo", [
        "Con una contraseña, el servidor **necesita saber el secreto**.",
        "Con una llave, el servidor solo necesita tu llave **pública**.",
        "El secreto nunca viaja ni se almacena en el servidor."], ORANGE, 12.5)
    callout(s, 6.78, 4.2, 6.1, 2.1, "Y además queda el rastro", [
        "La llave pública identifica a una persona o un sistema concreto.",
        "`authorized_keys` dice: «este servidor acepta a esta llave».",
        "Se puede revocar una llave sin cambiar la contraseña de nadie."], TEAL, 12.5)
    notes(s, "⏱ 6-10 min · El problema.\n\n"
             "Pregunta a la clase: '¿quién ha visto una contraseña de servidor compartida?' — todos.\n"
             "El giro de la caja izquierda es la frase que deben memorizar: el servidor nunca conoce el secreto.\n"
             "La segunda fila es la clásica: quien tiene una máquina comprometida pierde la llave.\n"
             "Por eso la rotación de llaves es parte del mantenimiento, no un extra.")

    n += 1
    s = content(prs, "El par de llaves: criptografía asimétrica", "Tu PC firma con la privada · el servidor verifica con la pública", PART, n + 1)
    rect(s, 0.6, 1.6, 4.6, 1.15, LIGHT)
    text(s, 0.75, 1.72, 4.3, 0.95, [[("Tu PC", {"size": 14, "bold": True, "color": NAVY})],
         [("id_ed25519  ·  la PRIVADA", {"size": 12, "color": TEXT})],
         [("Nunca sale de aquí", {"size": 11, "color": GRAY, "italic": True})]], space=1)
    rect(s, 8.1, 1.6, 4.6, 1.15, LIGHT)
    text(s, 8.25, 1.72, 4.3, 0.95, [[("El servidor", {"size": 14, "bold": True, "color": NAVY})],
         [("~/.ssh/authorized_keys  ·  la PÚBLICA", {"size": 12, "color": TEXT})],
         [("Se puede compartir sin riesgo", {"size": 11, "color": GRAY, "italic": True})]], space=1)
    text(s, 5.3, 1.95, 2.7, 0.5, "1  desafío", size=13, color=ORANGE, bold=True, align=PP_ALIGN.CENTER)
    text(s, 5.3, 2.25, 2.7, 0.4, "↓", size=18, color=NAVY, align=PP_ALIGN.CENTER)
    text(s, 5.3, 2.5, 2.7, 0.5, "2  firma", size=13, color=ORANGE, bold=True, align=PP_ALIGN.CENTER)
    text(s, 5.3, 2.8, 2.7, 0.4, "↓", size=18, color=NAVY, align=PP_ALIGN.CENTER)
    text(s, 5.3, 3.05, 2.7, 0.4, "3  acceso", size=13, color=ORANGE, bold=True, align=PP_ALIGN.CENTER)
    flow(s, [("Servidor envía", "texto aleatorio"), ("Tu PC firma", "con la privada"),
             ("Servidor verifica", "con tu pública")],
         0.6, 3.75, 12.1, h=0.95, colors=[BLUE, ORANGE, TEAL], size=12.5)
    table(s, [["", "Llave pública", "Llave privada"],
              ["Dónde vive", "En el servidor (authorized_keys)", "Solo en tu PC"],
              ["¿Se comparte?", "Sí, sin problema", "Nunca, con nadie"],
              ["¿Para qué sirve?", "Verificar firmas", "Firmar (crear el desafío)"],
              ["Tamaño típico", "ed25519: 32 bytes de clave", "32 bytes + cadena privada"]],
          0.45, 5.0, 12.4, col_w=[2.2, 5.1, 5.1], size=12, row_h=0.36)
    notes(s, "⏱ 10-15 min · Criptografía.\n\n"
             "Es la diapositiva más conceptual de la parte; tómate el tiempo.\n"
             "Analogía que funciona: la firma es como un sello. El sello (pública) lo puede verificar\n"
             "cualquiera, pero solo tú puedes estamparlo (privada).\n"
             "Aclare que SSH no 'manda la contraseña cifrada': manda un desafío y el cliente lo firma.\n"
             "Mencione ed25519 vs rsa: ed25519 es el default moderno y más rápido; rsa sigue aceptándose.\n"
             "Si alguien pregunta por la clave del servidor: no la tiene, solo verifica firmas.")

    n += 1
    s = content(prs, "ssh-keygen: generar el par en 30 segundos", "Un comando en tu máquina, un comando en el servidor — y la contraseña deja de existir", PART, n + 1)
    text(s, 0.45, 1.3, 6.1, 0.3, "1 · En tu PC — generar el par", size=13.5, color=NAVY, bold=True)
    code(s, 0.45, 1.7, 6.1, 1.85, [
        ("$ ssh-keygen -t ed25519 -C \"equipo@mi-pc\"", ORANGE),
        "  Generating public/private ed25519 key pair.",
        "  Enter file in which to save the key:",
        ("  Enter passphrase (empty for no passphrase):", SUB),
        "",
        ("$ ls -l ~/.ssh/", SUB),
        "  id_ed25519       ← la privada (permisos 600)",
        "  id_ed25519.pub   ← la pública (permisos 644)"], size=10.5)
    text(s, 0.45, 3.7, 6.1, 0.3, "2 · En el servidor — autorizar la llave", size=13.5, color=NAVY, bold=True)
    code(s, 0.45, 4.1, 6.1, 1.9, [
        ("$ ssh-copy-id usuario@10.0.3.10", ORANGE),
        "  # copia id_ed25519.pub a ~/.ssh/authorized_keys",
        "",
        ("# o a mano, desde tu contenedor:", SUB),
        "  mkdir -p ~/.ssh && chmod 700 ~/.ssh",
        "  cat id_ed25519.pub >> ~/.ssh/authorized_keys",
        ("  chmod 600 ~/.ssh/authorized_keys", GREEN)], size=10.5)
    callout(s, 6.95, 1.55, 5.9, 2.15, "3 · Probar: ya no pide contraseña", [
        [("$ ssh usuario@10.0.3.10", {"font": "Consolas", "size": 11.5, "color": NAVY, "bold": True})],
        "Si no pide nada y entras, la llave quedó bien autorizada.",
        "La clave del éxito son los **permisos**: SSH se niega a leer un archivo abierto."], ORANGE, 12.5)
    callout(s, 6.95, 3.95, 5.9, 2.0, "Permisos que SSH exige (si los cambias, falla)", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("`~/.ssh/`", {"size": 12, "font": "Consolas", "color": NAVY, "bold": True}),
         (" → ", {"size": 12}), ("700", {"size": 12, "bold": True, "color": RED})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("`authorized_keys`", {"size": 12, "font": "Consolas", "color": NAVY, "bold": True}),
         (" → ", {"size": 12}), ("600", {"size": 12, "bold": True, "color": RED})],
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12}),
         ("`id_ed25519`", {"size": 12, "font": "Consolas", "color": NAVY, "bold": True}),
         (" → ", {"size": 12}), ("600", {"size": 12, "bold": True, "color": RED})],
        "SSH avisa «UNPROTECTED PRIVATE KEY FILE» si el permiso está abierto."], TEAL, 12)
    notes(s, "⏱ 15-20 min · ssh-keygen.\n\n"
             "Si hay tiempo, GENERAR EL PAR EN VIVO con el proyector. Es instantáneo y lo entienden rápido.\n"
             "El detalle que más cuesta: los permisos. El 90 % de los «no me funciona SSH» son permisos.\n"
             "Muestra el aviso literal de OpenSSH: 'UNPROTECTED PRIVATE KEY FILE' — se les queda grabado.\n"
             "El passphrase es opcional; en el laboratorio se deja vacío para simplificar, pero\n"
             "menciona que en producción conviene ponerlo (o usar ssh-agent).\n"
             "Insiste en el aviso literal de permisos; es el error más común del laboratorio.")

    n += 1
    s = content(prs, "La entrada real: el servidor OpenSSH", "Dónde vive el servicio y cómo decide a quién acepta", PART, n + 1)
    code(s, 0.45, 1.45, 6.1, 2.3, [
        ("# contenedor con el servidor SSH", SUB),
        "docker run -d --name ssh-srv --network interna \\",
        "  -p 2222:22 \\",
        ("  -v ~/.ssh:/root/.ssh:ro alpine \\", ORANGE),
        "  sh -c 'apk add --no-cache openssh && \\",
        "        ssh-keygen -A && sshd -D'",
        "",
        ("$ docker exec ssh-srv sshd -T | grep -i ", SUB),
        ("  'pubkeyauthentication'", ORANGE),
        ("  → pubkeyauthentication yes", GREEN)], size=10.5)
    table(s, [["Directiva sshd_config", "Qué controla", "Valor seguro"],
              ["PubkeyAuthentication", "Aceptar autenticación por llave", "yes"],
              ["PasswordAuthentication", "Permitir entrar con contraseña", "no (con llave lista)"],
              ["PermitRootLogin", "Entrar como root directo", "no"],
              ["AllowUsers", "Quiénes pueden entrar", "lista explícita"]],
          6.95, 1.45, 5.9, col_w=[2.2, 2.4, 1.3], size=11, row_h=0.5, header_h=0.44)
    callout(s, 0.45, 4.05, 6.1, 2.35, "La demostración del Lab 11 (obligatoria)", [
        "1 · Entra con la llave autorizada → acceso concedido.",
        "2 · Entra con una llave **no** autorizada → «Permission denied».",
        "Las dos capturas son el entregable de la sesión A."], ORANGE, 12.5)
    callout(s, 6.95, 4.35, 5.9, 2.05, "Orden correcto de endurecimiento", [
        "Primero agrega la llave. **Después** apaga contraseñas.",
        "Si apagas contraseñas antes de tener llave, te quedas fuera.",
        "Este error se llama lock-out y es el más caro del tema."], RED, 12.5)
    notes(s, "⏱ 20-22 min · OpenSSH.\n\n"
             "No te metas a configurar sshd a fondo: es tema de la Unidad 3.3, no un curso de Linux.\n"
             "Lo importante: la tabla de directivas y el ORDEN (agregar llave → luego apagar contraseña).\n"
             "La advertencia de lock-out merece una anécdota: es el error que más caro sale en la vida real.\n"
             "Este es el bloque de seguridad: acá se ve la diferencia entre 'funciona' y 'es seguro'.")

    # ---------------------------------------------------------------- 4 sección 3.4
    n += 1
    s = divider(prs, "3.4", "Servidores bastión", "El único punto de entrada a una red que no debe exponerse",
                ["Qué es un bastión y por qué la red interna se esconde detrás",
                 "Single-homed · dual-homed · multihomed",
                 "Bastión web: proxy inverso y reglas de firewall"], "23 min")
    notes(s, "⏱ 22-23 min · Transición a 3.4.")

    n += 1
    s = content(prs, "Qué es un bastión (y por qué existe)", "Un host que se expone para que los demás no tengan que hacerlo", PART, n + 1)
    text(s, 0.45, 1.3, 12.4, 0.35,
         [[("Sin bastión: ", {"size": 14, "bold": True, "color": RED}),
           ("cada servidor interno publica su propio puerto hacia internet. Con 5 servicios, 5 puertas abiertas.",
            {"size": 14, "color": TEXT})]])
    text(s, 0.45, 1.75, 12.4, 0.35,
         [[("Con bastión: ", {"size": 14, "bold": True, "color": GREEN}),
           ("solo el bastión tiene salida a internet. Todo lo demás vive en una red interna sin ruta de vuelta.",
            {"size": 14, "color": TEXT})]])
    rect(s, 0.45, 2.25, 5.9, 1.9, LIGHT)
    text(s, 0.62, 2.35, 5.6, 0.3, "❌ Sin bastión", size=12.5, color=RED, bold=True)
    text(s, 0.62, 2.7, 5.6, 1.35, [
        [("INTERNET", {"size": 11, "color": TEXT, "bold": True})],
        [("  ↓ 22   ↓ 8080   ↓ 5432   ↓ 443   ↓ 80", {"size": 10.5, "font": "Consolas", "color": RED})],
        [("app  web  db  mail  proxy", {"size": 10.5, "font": "Consolas", "color": SUB})],
        [("5 superficies de ataque", {"size": 10.5, "color": RED, "italic": True})]], space=2)
    rect(s, 6.85, 2.25, 5.9, 1.9, LIGHT)
    text(s, 7.02, 2.35, 5.6, 0.3, "✓ Con bastión", size=12.5, color=GREEN, bold=True)
    text(s, 7.02, 2.7, 5.6, 1.35, [
        [("INTERNET", {"size": 11, "color": TEXT, "bold": True})],
        [("  ↓ 22   ↓ 443", {"size": 10.5, "font": "Consolas", "color": GREEN})],
        [("     ┌──────────┐", {"size": 10.5, "font": "Consolas", "color": SUB})],
        [("     │ BASTIÓN  │  ← única puerta", {"size": 10.5, "font": "Consolas", "color": GREEN})],
        [("     └────┬─────┘   red interna sin NAT", {"size": 10.5, "font": "Consolas", "color": SUB})]], space=1)
    table(s, [["Característica", "Qué significa", "Consecuencia práctica"],
              ["Es el único expuesto", "Solo él tiene interfaz pública", "Internet ve 1 host, no 5"],
              ["Está endurecido (hardened)", "Mínimo software, sin extras", "Menos superficie de ataque"],
              ["Todo pasa por él", "SSH, proxy web, túnel", "Auditoría: hay un solo punto de control"],
              ["La red interna no tiene salida", "Sin ruta por defecto a internet", "Aunque lo comprometan, no sale"]],
          0.45, 4.35, 12.4, col_w=[3.2, 4.6, 4.6], size=12, row_h=0.44)
    notes(s, "⏱ 23-28 min · Qué es un bastión.\n\n"
             "La analogía: es el guardia de la entrada. No es que sea más fuerte que los demás,\n"
             "es que es el único que queda en la calle.\n"
             "El punto clave de la última fila: la red interna SIN RUTA DE SALIDA. Aunque alguien\n"
             "entre a un servidor interno, no puede salir a internet. Eso es aislamiento real.\n"
             "Si preguntan por qué el bastión no reenvía tráfico, revisar la siguiente diapositiva.")

    n += 1
    s = content(prs, "Los tres tipos de bastión", "La diferencia es cuántas interfaces tiene: de ahí sale toda la clasificación", PART, n + 1)
    table(s, [["Tipo", "Interfaces", "Función", "Ejemplo en el Lab 11"],
              ["Single-homed", "1", "Acceso a una sola red, sin reenviar tráfico", "bastión simple + túnel -L"],
              ["Dual-homed", "2 (pública + interna)", "Puente entre pública e interna, sin reenvío", "bastión + red --internal"],
              ["Multihomed", "3 o más", "Gateway con varios caminos: web, proxy, VPN", "bastión web + proxy inverso"]],
          0.45, 1.45, 12.4, col_w=[1.9, 2.6, 4.4, 3.5], size=12.5, row_h=0.5)
    callout(s, 0.45, 3.5, 6.1, 2.0, "Dual-homed: el punto dulce", [
        "Una interfaz en la red pública (recibe las conexiones).",
        "Una en la red interna (habla con los servidores).",
        "**No** reenvía tráfico: es puente de acceso, no router."], ORANGE, 12.5)
    callout(s, 6.78, 3.5, 6.1, 2.0, "El detalle que hace la seguridad", [
        "La red interna se crea con `docker network create --internal`.",
        "Esa opción quita la puerta de salida por defecto.",
        "Sin esa opción, el dual-homed es solo decorativo."], RED, 12.5)
    callout(s, 0.45, 5.7, 12.4, 1.05, "El enunciado del proyecto pide dual-homed mínimo", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Avance N.º 2: ", {"size": 12.5}),
         ("«Servidor bastión: mínimo dual-homed (o multi) protegiendo la red interna; la aplicación "
          "interna NO tiene exposición directa.»", {"size": 12.5, "italic": True, "color": NAVY})]], NAVY, 12.5)
    notes(s, "⏱ 28-32 min · Tipos de bastión.\n\n"
             "Diapositiva de examen: la pregunta clásica es '¿qué tipo es este y por qué?'.\n"
             "Regla: interfaces = clasificación. Si tiene 1 = single, 2 = dual, 3+ = multi.\n"
             "El detalle de `--internal` en la caja roja es lo que hace la diferencia entre un trabajo\n"
             "real y uno de adorno. Si lo dicen, el proyecto está bien hecho.\n"
             "Aclara que 'sin reenviar' no significa 'inútil': reenviar sería convertirlo en router.")

    n += 1
    s = content(prs, "Bastión web: proxy inverso y deep-secure", "El bastión también sirve sitios, no solo SSH", PART, n + 1)
    text(s, 0.45, 1.3, 6.1, 0.3, "Proxy inverso con nginx (el patrón del proyecto)", size=13.5, color=NAVY, bold=True)
    code(s, 0.45, 1.7, 6.1, 1.95, [
        "server {",
        "  listen 443 ssl;",
        "  server_name app.feria.local;",
        "",
        "  # el bastion responde, el backend no",
        ("  location / {", ORANGE),
        ("    proxy_pass http://app-srv:5000;", ORANGE),
        "  }",
        "}", ], size=10.5)
    callout(s, 0.45, 3.85, 6.1, 1.6, "Qué aporta el proxy inverso", [
        "El cliente nunca ve la IP real del backend.",
        "El bastión termina el TLS: los internos hablan HTTP plano.",
        "Un solo puerto público para varios servicios."], ORANGE, 12.5)
    text(s, 0.45, 5.65, 6.1, 0.3, "Reglas de firewall (iptables) — deep-secure", size=13.5, color=NAVY, bold=True)
    code(s, 0.45, 6.05, 6.1, 1.15, [
        "# por defecto, bloquea todo",
        ("iptables -P INPUT DROP", RED),
        "# y deja entrar solo SSH y HTTPS",
        ("iptables -A INPUT -p tcp --dport 22 -j ACCEPT", GREEN),
        ("iptables -A INPUT -p tcp --dport 443 -j ACCEPT", GREEN)], size=10)
    table(s, [["Capa", "Control", "Herramienta"],
              ["Qué puerto se publica", "Solo SSH + HTTPS del bastión", "`-p 2222:22`"],
              ["Quién entra", "Solo llaves autorizadas", "`authorized_keys`"],
              ["Qué se alcanza", "Solo lo que el bastión publica", "proxy inverso"],
              ["Qué sale a internet", "Solo el bastión", "red interna `--internal`"]],
          6.95, 1.5, 5.9, col_w=[2.2, 2.5, 1.2], size=11, row_h=0.55, header_h=0.44)
    callout(s, 6.95, 4.5, 5.9, 2.3, "Las 4 capas de un bastión «bien hecho»", [
        [("1. ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Pocos puertos publicados", {"size": 12, "bold": True})],
        [("2. ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Autenticación por llave, no contraseña", {"size": 12, "bold": True})],
        [("3. ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Firewall con default DROP", {"size": 12, "bold": True})],
        [("4. ", {"color": ORANGE, "bold": True, "size": 12}),
         ("Red interna sin salida a internet", {"size": 12, "bold": True})],
        "Si falta una, la red sigue expuesta por ese lado."], TEAL, 12)
    notes(s, "⏱ 32-40 min · Bastión web.\n\n"
             "Explica el proxy inverso con la analogía del mostrador: el cliente habla con el mostrador,\n"
             "nunca entra al almacén. El almacén es la red interna.\n"
             "El TLS termina en el bastión: los internos no necesitan certificado.\n"
             "Las 4 capas de la derecha son el checklist del docente. Es lo que revisa la rúbrica.\n"
             "El TLS terminando en el bastión es una decisión real de arquitectura, no un detalle.")

    n += 1
    s = content(prs, "ProxyJump: atravesar el bastión con una línea", "El usuario entra al bastión y desde ahí salta a la red interna", PART, n + 1)
    text(s, 0.45, 1.28, 12.4, 0.6,
         [[("El problema: ", {"size": 14, "bold": True, "color": RED}),
           ("la red interna no tiene ruta a internet, así que no puedes alcanzarla directamente. "
            "ProxyJump te deja entrar en dos saltos usando el bastión de trampolín.", {"size": 14, "color": TEXT})]])
    code(s, 0.45, 2.0, 6.1, 1.8, [
        "# en una sola línea, saltando por el bastión",
        ("$ ssh -J usuario@bastion app-srv", ORANGE),
        "",
        "# o declarándolo en ~/.ssh/config (mejor)",
        ("Host app-srv", TEAL),
        "  HostName 10.0.1.10",
        ("  ProxyJump usuario@bastion", TEAL),
        ("  User usuario", SUB)], size=10.5)
    callout(s, 0.45, 4.0, 6.1, 1.6, "Con ~/.ssh/config", [
        "Un alias por servidor: `ssh app-srv` y listo.",
        "El puerto y el usuario se documentan en el archivo.",
        "El manual de despliegue del proyecto lo puede citar."], ORANGE, 12.5)
    text(s, 6.95, 1.3, 5.9, 0.3, "Túneles SSH: llegar a la DB sin abrirla", size=13.5, color=NAVY, bold=True)
    code(s, 6.95, 1.7, 5.9, 1.6, [
        "# -L tunnel: la DB no se publica nunca",
        ("$ ssh -L 5433:db-srv:5432 bastion", ORANGE),
        "",
        "# ahora postgres está en localhost:5433",
        ("$ psql -h localhost -p 5433 -U admin", GREEN)], size=10.5)
    callout(s, 6.95, 3.5, 5.9, 1.9, "Por qué el túnel es la respuesta", [
        "La DB **no** tiene puerto publicado: no existe en internet.",
        "El túnel existe solo mientras dura la sesión SSH.",
        "Se cierra la terminal, se cierra el acceso."], TEAL, 12.5)
    callout(s, 0.45, 5.75, 12.4, 1.2, "Los tres patrones de acceso que deben dominar", [
        [("▸ ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("`ssh -J`", {"size": 12.5, "font": "Consolas", "color": NAVY, "bold": True}),
         (" / ProxyJump → entrar a la red interna saltando por el bastión.   ", {"size": 12.5}),
         ("`ssh -L`", {"size": 12.5, "font": "Consolas", "color": NAVY, "bold": True}),
         (" → tunelizar un puerto interno sin abrirlo.   ", {"size": 12.5}),
         ("`ssh host`", {"size": 12.5, "font": "Consolas", "color": NAVY, "bold": True}),
         (" → con alias en ~/.ssh/config, sin repetir nada.", {"size": 12.5})]], NAVY, 12.5)
    notes(s, "⏱ 40-48 min · ProxyJump y túneles.\n\n"
             "Esta es la parte más práctica de la sesión. Si hay tiempo, en vivo:\n"
             "  ssh -L contra la DB del lab y un psql que se conecte.\n"
             "El argumento del túnel es el que cierra el proyecto: la DB no se publica, punto.\n"
             "ProxyJump es lo que hace usable la red interna sin abrirla.\n"
             "El túnel es la respuesta al requisito del proyecto: la DB no se publica nunca.")

    # ---------------------------------------------------------------- cierre
    n += 1
    s = content(prs, "Resumen y cierre de la Parte 2", "Qué debe quedar en la cabeza antes de ir al Lab 11", PART, n + 1)
    callout(s, 0.45, 1.45, 6.1, 2.6, "Ideas clave (3.3 + 3.4)", [
        "La llave **pública** autoriza; la **privada** firma y no sale.",
        "El servidor nunca almacena el secreto.",
        "SSH se niega a leer llaves con permisos abiertos: 600 / 700.",
        "Bastión = única puerta; la red interna sin salida."], ORANGE, 12.5)
    callout(s, 6.78, 1.45, 6.1, 2.6, "Puente hacia la Parte 3", [
        "Ya tenemos la red, el acceso seguro y el monitoreo.",
        "Falta **escalar**: un contenedor, o muchos copias de uno.",
        "Parte 3: orquestación con Compose y Swarm (3.5).",
        "Ahí las llaves y los secretos se vuelven clave de despliegue."], TEAL, 12.5)
    callout(s, 0.45, 4.25, 12.4, 2.2, "Preguntas de autoevaluación (sal de clase sabiendo responderlas)", [
        [("1. ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Explica en una frase por qué la llave pública puede ir en el servidor y la privada no.", {"size": 12.5})],
        [("2. ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("¿Qué permisos deben tener `~/.ssh/` y `authorized_keys`, y qué pasa si no?", {"size": 12.5})],
        [("3. ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Diferencia un bastión single-homed de uno dual-homed con un ejemplo.", {"size": 12.5})],
        [("4. ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("¿Por qué la red interna se crea con `--internal` y qué pasaría sin eso?", {"size": 12.5})],
        [("5. ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("¿Cómo accedes a la base de datos sin publicar su puerto? Nombra el comando.", {"size": 12.5})],
        [("6. ", {"color": ORANGE, "bold": True, "size": 12.5}),
         ("Si endureces un bastión, ¿qué va primero y por qué?", {"size": 12.5})]],
         NAVY, 12.5)
    notes(s, "⏱ 48-55 min · Cierre de la Parte 2.\n\n"
             "La pregunta 6 es la que más discrimina: agregar llave → luego apagar contraseña.\n"
             "La 5 es la del proyecto: ssh -L.\n"
             "Deja 5 min y pide dos respuestas en voz alta antes de pasar a la Parte 3.\n"
             "Si la respuesta es 'primero apago las contraseñas', la pregunta no se entendió:\n"
             "eso es justamente el error de lock-out de la diapositiva 12.")

    prs.save(out)
    return out


if __name__ == "__main__":
    p = build(sys.argv[1] if len(sys.argv) > 1 else "Teoria-U3-Parte2-SSH-Bastion.pptx")
    print("OK ->", p)
