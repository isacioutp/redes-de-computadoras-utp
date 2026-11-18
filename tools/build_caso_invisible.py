"""Unidad III · Caso 2 — El despliegue que nadie vio · 20 min."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ppt_kit import *  # noqa

PART = "Caso invisible · DevOps sobre la red"


def build(out):
    prs = new_deck()
    n = 0

    s = cover(prs, "UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES",
              "Unidad III — Caso 2: el despliegue invisible",
              "Pipeline en verde, usuario en 502",
              ["El caso: el smoke pasa y nadie ve la versión nueva",
               "Redes: DNS, TTL, resolución de nombres y proxy inverso",
               "DevOps: verificar la ruta, no solo el artefacto"],
              "Caso de cierre", "20 min")
    notes(s, "⏱ 0-1 min · Portada.\n\n"
             "Abrir con la contradicción: 'el pipeline salió verde, el smoke dio v2 y\n"
             "el usuario llamó a soporte'. Preguntar dónde puede estar el fallo antes de\n"
             "mostrar cualquier comando. Dejar la respuesta para la diapositiva 6.")

    n += 1
    s = content(prs, "La pregunta del caso", "Todo sale bien menos lo que importa", PART, n + 1)
    kpi(s, [("1", "pipeline en verde"), ("v2", "devuelve el smoke"),
            ("502", "ve el usuario"), ("1 h", "de impacto")],
        0.45, 1.35, 12.4)
    callout(s, 0.45, 2.65, 6.1, 2.35, "Lo que midió el equipo", [
        "La imagen `v2` se construyó y se publicó.",
        "El contenedor nuevo arrancó.",
        "`curl localhost:18081/` devolvió `CitasYA api v2`.",
        "El health check respondió 200."], TEAL, 12)
    callout(s, 6.78, 2.65, 6.1, 2.35, "Lo que recibió el usuario", [
        "En el host nuevo: **502**.",
        "En el host viejo: todavía **v1**.",
        "Los clientes con caché nunca alcanzaron el `v2`.",
        "Una hora hasta que venció el TTL."], RED, 12)
    callout(s, 0.45, 5.15, 12.4, 1.4, "La tesis del caso", [
        "El artefacto estaba bien. El camino estaba roto.",
        "Acá se estudia el tráfico del despliegue, no el build."], NAVY, 12.5)
    notes(s, "⏱ 1-3 min · La contradicción.\n\n"
             "Leer los cuatro KPIs en voz alta. El 502 y la hora son los que importan.\n"
             "No explicar todavía por qué: el valor de esta diapositiva es que el grupo\n"
             "piense en dos sistemas distintos, el pipeline y el usuario.")

    n += 1
    s = divider(prs, "Caso", "CitasYA, el despliegue que nadie vio",
                "API de turnos · dos hosts · un cambio de DNS",
                ["09:12 merge · 09:19 DNS · 09:40 host viejo apagado",
                 "10:20 vence el TTL y todo vuelve a verse bien",
                 "Dos fallas de red, una sola hora de impacto"], "20 min")
    notes(s, "⏱ 3-4 min · Transición.\n\n"
             "Aclarar que es un caso inventado con forma real. Lo importante es la\n"
             "secuencia de decisiones: cambiar DNS, recrear un contenedor y apagar el\n"
             "host anterior en la misma ventana.")

    n += 1
    s = content(prs, "El sistema: dos hosts, dos caminos", "Lo mismo que simula el Laboratorio 16", PART, n + 1)
    code(s, 0.45, 1.35, 12.4, 2.5, [
        ("  cliente con caché              cliente que resuelve ahora", BLUE),
        ("  127.0.0.2:18080                127.0.0.1:18080", BLUE),
        ("        |                                |", SUB),
        ("   proxy-viejo                      proxy-nuevo", WHITE),
        ("        |                                |", SUB),
        ("   api-viejo (v1)                   api (v1 -> v2)", WHITE),
        ("   172.28.16.12                     172.28.16.10 -> .11", SUB),
        ], size=10.5)
    callout(s, 0.45, 4.05, 6.1, 2.35, "Qué representa cada IP", [
        "`127.0.0.2` es el host viejo; `127.0.0.1`, el nuevo.",
        "`curl --resolve` simula la entrada que el cliente ya tiene en caché.",
        "No se edita `/etc/hosts` ni se levanta un servidor DNS.",
        "Los puertos 18080 y 18081 son los del laboratorio."], TEAL, 11.5)
    callout(s, 6.78, 4.05, 6.1, 2.35, "Dos nombres que importan", [
        "`api.citasya.test`: lo que resuelve el cliente.",
        "`api`: lo que resuelve el DNS interno de Docker.",
        "nginx guarda la IP de `api` cuando arranca.",
        "Recrear el contenedor no se lo avisa a nginx."], ORANGE, 11.5)
    notes(s, "⏱ 4-6 min · Topología.\n\n"
             "Demo: levantar el lab y correr `docker compose ps`. Guion completo en\n"
             "`DevOps/DOCENTE/GUIA-DEMO-CASO-INVISIBLE.md`.\n\n"
             "Señalar los dos caminos con el dedo: el de arriba decide a qué host llega\n"
             "el cliente; el de abajo decide a qué contenedor llega el proxy. Los dos\n"
             "pueden fallar al mismo tiempo y dar síntomas distintos.\n"
             "Aclarar que las IP de loopback son un truco del laboratorio para no\n"
             "necesitar dos máquinas; en producción son dos IP públicas.")

    n += 1
    s = content(prs, "La línea de tiempo", "Una decisión normal por minuto", PART, n + 1)
    table(s, [["Hora", "Qué pasó"],
              ["09:12", "Se fusiona `v2`: build y push salen en verde."],
              ["09:18", "Arranca el stack nuevo; el smoke directo da `v2`."],
              ["09:19", "Cambia el registro A. El TTL sigue en 3600."],
              ["09:20", "Se recrea `api` en otra IP; no se recarga nginx."],
              ["09:25", "Soporte: unos ven `v1`, otros reciben 502."],
              ["09:40", "Apagan el host viejo para ahorrar costo."],
              ["09:55", "Reload de nginx: se arregla el 502 del host nuevo."],
              ["10:20", "Vence el TTL: una hora de impacto para el usuario."]],
          0.45, 1.35, 12.4, col_w=[1.2, 11.2], size=11.5, row_h=0.38)
    callout(s, 0.45, 4.95, 12.4, 1.5, "El costo no fue técnico", [
        "El arreglo tomó minutos; la espera del TTL tomó una hora.",
        "El MTTR mide tiempo de recuperación, no tiempo de escribir código."], RED, 12.5)
    notes(s, "⏱ 6-9 min · La historia.\n\n"
             "Demo: `getent hosts api` da la IP inicial .10. Después de la historia,\n"
             "recrear `api` con `TAG=v2 API_IP=172.28.16.11`.\n\n"
             "Leerla como una sucesión de decisiones razonables. El error no está en\n"
             "09:12. Está en 09:19 (TTL sin bajar) y en 09:20 (proxy sin recargar).\n"
             "Pausa en 09:40: apagar el host viejo convierte una versión antigua en un\n"
             "servicio caído. Preguntar qué se perdió en ese momento: el rollback.")

    n += 1
    s = content(prs, "El smoke pasó, el usuario no", "Dos respuestas verdaderas al mismo tiempo", PART, n + 1)
    callout(s, 0.45, 1.35, 6.1, 2.75, "Lo que midió el pipeline", [
        "`curl localhost:18081/` → `CitasYA api v2`.",
        "El puerto 18081 está publicado directo al contenedor.",
        "No pasa por nginx ni por el DNS del cliente.",
        "La puerta se abrió con el artefacto correcto."], TEAL, 12)
    callout(s, 6.78, 1.35, 6.1, 2.75, "Lo que vio el usuario", [
        "Por el proxy nuevo: **502**.",
        "Por el proxy viejo: **v1**.",
        "El cliente con caché nunca alcanzó el `v2`.",
        "El cambio no existió para quien paga el servicio."], RED, 12)
    callout(s, 0.45, 4.35, 12.4, 2.1, "La frase que se llevan", [
        [("▸ ", {"color": NAVY, "bold": True, "size": 13}),
         ("Un `200` en `localhost` no prueba un despliegue.", {"size": 13, "bold": True})],
        "La prueba tiene que entrar por el mismo camino que el usuario: nombre público, proxy y puerto real.",
        "Si la sonda corre al lado del servidor, siempre va a decir que está todo bien."], NAVY, 12)
    notes(s, "⏱ 9-11 min · El centro del caso.\n\n"
             "Demo: smoke directo en 18081 da `v2`; el proxy nuevo da 502 y el cliente\n"
             "con `--resolve ...127.0.0.2` sigue viendo `v1`.\n\n"
             "No avanzar hasta que alguien diga en voz alta la diferencia: el smoke\n"
             "pegó al contenedor, el usuario pasa por el proxy y por el DNS.\n"
             "La frase en negrita es la que se pide en el entregable.")

    n += 1
    s = content(prs, "DNS: el TTL decide cuándo cambia el mundo", "Registro A, caché y tiempo de expiración", PART, n + 1)
    callout(s, 0.45, 1.35, 6.1, 2.6, "Qué pasó con el nombre", [
        "El registro A pasó del host viejo al nuevo.",
        "El TTL quedó en 3600 segundos.",
        "Los resolutores guardaron la respuesta anterior.",
        "Cambiar el registro no cambia todas las copias a la vez."], ORANGE, 12)
    code(s, 6.78, 1.35, 6.1, 2.6, [
        ("$ dig api.citasya.test A +noall +answer", WHITE),
        ("api.citasya.test. 2340 IN A 127.0.0.2", BLUE),
        ("", SUB),
        ("$ curl --resolve api.citasya.test:18080:127.0.0.2 ...", WHITE),
        ("CitasYA api v1", GREEN),
        ], size=9.5)
    callout(s, 0.45, 4.2, 12.4, 2.25, "Qué se hace antes del corte", [
        "Bajar el TTL de 3600 a 60 con al menos una hora de anticipación.",
        "Esperar a que venza el TTL original antes de cambiar la IP.",
        "Mantener el host viejo arriba durante toda la ventana de caché.",
        "En el laboratorio, `--resolve` cumple el papel de esa caché."], TEAL, 12)
    notes(s, "⏱ 11-13 min · DNS.\n\n"
             "Demo: el laboratorio no tiene servidor DNS; `--resolve` simula la caché.\n"
             "El `dig` de la diapositiva es ilustrativo y se explica como tal.\n\n"
             "Explicar el TTL como 'cuánto tiempo una copia ajena puede seguir diciendo\n"
             "la verdad de ayer'. El número 2340 es el tiempo que todavía falta.\n"
             "El error no fue cambiar el registro: fue cambiarlo con TTL largo y apagar\n"
             "el host anterior enseguida.")

    n += 1
    s = content(prs, "nginx: el nombre se resuelve una vez", "Docker DNS y el proxy no siempre están de acuerdo", PART, n + 1)
    code(s, 0.45, 1.35, 6.1, 2.5, [
        ("$ docker exec ... getent hosts api", WHITE),
        ("172.28.16.11   api", GREEN),
        ("", SUB),
        ("$ docker exec ... nginx -T | grep proxy_pass", WHITE),
        ("proxy_pass http://api:8000;", BLUE),
        ('upstream: "http://172.28.16.10:8000/"', RED),
        ], size=9.5)
    callout(s, 6.78, 1.35, 6.1, 2.5, "Dos respuestas distintas", [
        "`getent` pregunta ahora: da la IP nueva.",
        "`nginx -T` muestra el nombre, no la IP.",
        "El proceso guardó la IP vieja al arrancar.",
        "El archivo no cambió, pero el proceso sí está desactualizado."], ORANGE, 11.5)
    callout(s, 0.45, 4.1, 12.4, 2.35, "El arreglo y la lección", [
        "`nginx -s reload` vuelve a resolver el nombre: el 502 desaparece sin tocar la configuración.",
        "Ese reload tiene que estar escrito en el pipeline, no en la memoria de quien está de guardia."], TEAL, 12.5)
    notes(s, "⏱ 13-15 min · Resolución interna.\n\n"
             "Demo: `getent hosts api` da .11 y los logs de nginx muestran .10.\n"
             "Después, `nginx -s reload` y el mismo `curl` da `v2`.\n\n"
             "La comparación clave: el DNS interno ya dice .11 y los logs de nginx\n"
             "muestran .10. Eso demuestra que el fallo está en el proceso, no en Docker.\n"
             "Si alguien pregunta por `resolver`, explicar que acá no hay una directiva\n"
             "que fuerce a nginx a volver a resolver: por eso hace falta el reload.")

    n += 1
    s = content(prs, "Los cinco flujos del caso", "Origen, destino, puerto y consecuencia", PART, n + 1)
    table(s, [["Flujo", "Origen → destino", "Puerto", "Qué falla"],
              ["Resolución pública", "cliente → resolutor", "53", "Caché con TTL 3600"],
              ["Entrada al proxy", "cliente → host nuevo", "443 / 80", "Solo llega quien tiene la IP nueva"],
              ["DNS interno", "nginx → 127.0.0.11", "53", "Nombre resuelto una sola vez"],
              ["Proxy a la API", "nginx → api:8000", "8000", "IP vieja: 502"],
              ["Smoke", "runner → host publicado", "18081", "Directo al contenedor: pasa"]],
          0.45, 1.35, 12.4, col_w=[2.4, 3.9, 1.3, 4.8], size=11.5, row_h=0.42)
    callout(s, 0.45, 4.55, 12.4, 1.95, "La regla para diagnosticar", [
        "Cada síntoma pertenece a un flujo: DNS, proxy, contenedor o medición.",
        "Sin el mapa dibujado, un 502 parece un bug de código y se pierde una hora buscando en el repo."], NAVY, 12.5)
    notes(s, "⏱ 15-16 min · Los flujos.\n\n"
             "Pedir al grupo que complete la columna 'Qué falla' antes de mostrarla.\n"
             "La fila del smoke es la que explica por qué el dashboard decía verde.\n"
             "Cerrar con la idea de capas: el mismo síntoma tiene dueños distintos.")

    n += 1
    s = content(prs, "Cinco porqués, una causa", "Del síntoma a la decisión de diseño", PART, n + 1)
    table(s, [["Pregunta", "Respuesta"],
              ["¿Por qué vieron v1 o 502?", "El tráfico no llegó al contenedor `v2`."],
              ["¿Por qué pasó el smoke?", "Entró por 18081, sin proxy ni DNS."],
              ["¿Por qué nginx siguió en la IP vieja?", "Resolvió `api` al arrancar; no hubo reload."],
              ["¿Por qué clientes seguían en el host viejo?", "TTL de 3600 en caché de resolutores."],
              ["¿Por qué empeoró al apagar el host?", "Se fue el rollback tibio."]],
          0.45, 1.35, 12.4, col_w=[5.2, 7.2], size=11.5, row_h=0.48)
    callout(s, 0.45, 4.85, 12.4, 1.6, "Causa raíz", [
        [("▸ ", {"color": RED, "bold": True, "size": 13}),
         ("El pipeline verificó el artefacto, no verificó la ruta.", {"size": 13, "bold": True})],
        "Las cinco piezas del caso anterior estaban presentes y aun así falló el despliegue."], RED, 12.5)
    notes(s, "⏱ 16-17 min · Los porqués.\n\n"
             "Esta tabla se puede tapar columna por columna. La última respuesta es la\n"
             "que más discusión genera: mantener el host viejo cuesta dinero y es lo que\n"
             "permite volver atrás durante una hora.\n"
             "Cerrar señalando que las tres piezas clásicas ya estaban: por eso hacía\n"
             "falta un caso nuevo.")

    n += 1
    s = content(prs, "Lo que agrega este caso", "Conceptos de DevOps y de redes que se ven acá", PART, n + 1)
    callout(s, 0.45, 1.35, 3.95, 3.05, "DevOps: verificar la ruta", [
        "El smoke entra por la URL pública, con el `Host` real.",
        "La sonda corre fuera del servidor.",
        "Éxito es ver la versión nueva en el cliente.",
        "El reload del proxy es un paso del pipeline."], TEAL, 11.5)
    callout(s, 4.65, 1.35, 3.95, 3.05, "Redes: resolución y caché", [
        "Registro A, TTL y resolutores caches.",
        "DNS interno de Docker y nombres de servicio.",
        "Un proxy puede guardar una IP resuelta.",
        "`dig`, `getent` y `curl --resolve` separan las capas."], ORANGE, 11.5)
    callout(s, 8.85, 1.35, 3.95, 3.05, "Operación: rollback tibio", [
        "El host viejo sigue arriba durante la ventana de TTL.",
        "El TTL se baja antes del corte, no después.",
        "Volver no es reconstruir: es seguir sirviendo.",
        "El MTTR incluye esperar a que expire la caché."], NAVY, 11.5)
    callout(s, 0.45, 4.6, 12.4, 1.85, "Las cuatro claves DORA en este caso", [
        "Frecuencia y lead time no cambiaron: el build estuvo bien.",
        "La tasa de fallo la puso el usuario, no el pipeline.",
        "El MTTR fue de una hora y lo dominó el TTL, no el arreglo del proxy."], GREEN, 12)
    notes(s, "⏱ 17-19 min · Conceptos.\n\n"
             "Pedir que clasifiquen cada idea en DevOps o redes. La respuesta correcta\n"
             "es que casi todas son de redes: DevOps decide que se verifiquen y se\n"
             "automaticen.\n"
             "DORA se menciona solo para ubicar el MTTR: mejorar el build no baja el\n"
             "tiempo de recuperación si la recuperación depende de un TTL.")

    n += 1
    s = content(prs, "Cierre y práctica", "Laboratorio 16: reproduce las dos fallas en tu Docker", PART, n + 1)
    callout(s, 0.45, 1.35, 6.1, 2.5, "Entregable", [
        "Bitácora de los 7 pasos con la IP de `api` en cada momento.",
        "Smoke en verde, proxy nuevo en 502 y cliente cacheado en `v1`.",
        "Un comando por falla: `getent hosts`, `nginx -T`, `curl --resolve`.",
        "Plan de corrección de cinco líneas."], ORANGE, 11.5)
    callout(s, 6.78, 1.35, 6.1, 2.5, "Tres frases para repetir", [
        "Un `200` en `localhost` no prueba un despliegue.",
        "Cambiar el DNS no cambia todas las copias a la vez.",
        "Sin host viejo arriba no hay rollback durante el TTL."], TEAL, 12)
    callout(s, 0.45, 4.1, 12.4, 2.35, "Pregunta final", [
        "¿Por qué el smoke puede decir que todo está bien mientras el usuario ve un 502?",
        "Respuesta corta: porque midió el artefacto en su puerto, sin pasar por el DNS ni por el proxy que usa el usuario.",
        "Carpeta: `DevOps/Laboratorio-16-Despliegue-Invisible/`."], NAVY, 12.5)
    notes(s, "⏱ 19-20 min · Cierre.\n\n"
             "Demo: apagar `proxy-viejo` y mostrar que el cliente cacheado se queda sin\n"
             "servicio. Limpiar con `docker compose down`.\n\n"
             "Hacer la pregunta final al grupo y esperar la respuesta antes de leerla.\n"
             "El laboratorio ya trae los archivos, la evidencia de la prueba ejecutada\n"
             "y los comandos de limpieza. No depende de ningún otro laboratorio.")

    prs.save(out)
    return out


if __name__ == "__main__":
    p = build(sys.argv[1] if len(sys.argv) > 1 else "DevOps/DOCENTE/Teoria-Despliegue-Invisible.pptx")
    print("OK ->", p)
