# Teoría — Unidad III · Caso 2: el despliegue invisible

> Contenido completo de [`Teoria-Despliegue-Invisible.pptx`](Teoria-Despliegue-Invisible.pptx) (12 diapositivas, 16:9).
> Volcado textual de la presentación: mismo contenido y mismo orden de
> lectura, sin depender de PowerPoint.
>
> Se regenera con:
> `python3 tools/dump_ppt_md.py DevOps/Teoria-Despliegue-Invisible.pptx "Unidad III · Caso 2: el despliegue invisible"`
>
> Cada diapositiva conserva sus **notas del orador** al final, en bloques
> plegables: en GitHub y en la mayoría de editores se despliegan con un clic.

## Índice

- **1.** Unidad III — Caso 2: el despliegue invisible
- **2.** La pregunta del caso
- **3.** CitasYA, el despliegue que nadie vio
- **4.** El sistema: dos hosts, dos caminos
- **5.** La línea de tiempo
- **6.** El smoke pasó, el usuario no
- **7.** DNS: el TTL decide cuándo cambia el mundo
- **8.** nginx: el nombre se resuelve una vez
- **9.** Los cinco flujos del caso
- **10.** Cinco porqués, una causa
- **11.** Lo que agrega este caso
- **12.** Cierre y práctica

---

## 1. Unidad III — Caso 2: el despliegue invisible

**UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES**

Pipeline en verde, usuario en 502

- El caso: el smoke pasa y nadie ve la versión nueva
- Redes: DNS, TTL, resolución de nombres y proxy inverso
- DevOps: verificar la ruta, no solo el artefacto

<details><summary>Notas del orador</summary>

⏱ 0-1 min · Portada.

Abrir con la contradicción: 'el pipeline salió verde, el smoke dio v2 y
el usuario llamó a soporte'. Preguntar dónde puede estar el fallo antes de
mostrar cualquier comando. Dejar la respuesta para la diapositiva 6.

</details>

---

## 2. La pregunta del caso

> Todo sale bien menos lo que importa

pipeline en verde

**v2**
devuelve el smoke

ve el usuario

**1 h**
de impacto

**Lo que midió el equipo**
- La imagen `v2` se construyó y se publicó.
- El contenedor nuevo arrancó.
- `curl localhost:18081/` devolvió `CitasYA api v2`.
- El health check respondió 200.

**Lo que recibió el usuario**
- En el host nuevo: **502**.
- En el host viejo: todavía **v1**.
- Los clientes con caché nunca alcanzaron el `v2`.
- Una hora hasta que venció el TTL.

**La tesis del caso**
- El artefacto estaba bien. El camino estaba roto.
- Acá se estudia el tráfico del despliegue, no el build.

<details><summary>Notas del orador</summary>

⏱ 1-3 min · La contradicción.

Leer los cuatro KPIs en voz alta. El 502 y la hora son los que importan.
No explicar todavía por qué: el valor de esta diapositiva es que el grupo
piense en dos sistemas distintos, el pipeline y el usuario.

</details>

---

## 3. CitasYA, el despliegue que nadie vio

API de turnos · dos hosts · un cambio de DNS

- 09:12 merge · 09:19 DNS · 09:40 host viejo apagado
- 10:20 vence el TTL y todo vuelve a verse bien
- Dos fallas de red, una sola hora de impacto

20 min

<details><summary>Notas del orador</summary>

⏱ 3-4 min · Transición.

Aclarar que es un caso inventado con forma real. Lo importante es la
secuencia de decisiones: cambiar DNS, recrear un contenedor y apagar el
host anterior en la misma ventana.

</details>

---

## 4. El sistema: dos hosts, dos caminos

> Lo mismo que simula el Laboratorio 16

```text
cliente con caché              cliente que resuelve ahora
127.0.0.2:18080                127.0.0.1:18080
|                                |
proxy-viejo                      proxy-nuevo
|                                |
api-viejo (v1)                   api (v1 -> v2)
172.28.16.12                     172.28.16.10 -> .11
```

**Qué representa cada IP**
- `127.0.0.2` es el host viejo; `127.0.0.1`, el nuevo.
- `curl --resolve` simula la entrada que el cliente ya tiene en caché.
- No se edita `/etc/hosts` ni se levanta un servidor DNS.
- Los puertos 18080 y 18081 son los del laboratorio.

**Dos nombres que importan**
- `api.citasya.test`: lo que resuelve el cliente.
- `api`: lo que resuelve el DNS interno de Docker.
- nginx guarda la IP de `api` cuando arranca.
- Recrear el contenedor no se lo avisa a nginx.

<details><summary>Notas del orador</summary>

⏱ 4-6 min · Topología.

Señalar los dos caminos con el dedo: el de arriba decide a qué host llega
el cliente; el de abajo decide a qué contenedor llega el proxy. Los dos
pueden fallar al mismo tiempo y dar síntomas distintos.
Aclarar que las IP de loopback son un truco del laboratorio para no
necesitar dos máquinas; en producción son dos IP públicas.

</details>

---

## 5. La línea de tiempo

> Una decisión normal por minuto

| Hora | Qué pasó |
|---|---|
| 09:12 | Se fusiona `v2`: build y push salen en verde. |
| 09:18 | Arranca el stack nuevo; el smoke directo da `v2`. |
| 09:19 | Cambia el registro A. El TTL sigue en 3600. |
| 09:20 | Se recrea `api` en otra IP; no se recarga nginx. |
| 09:25 | Soporte: unos ven `v1`, otros reciben 502. |
| 09:40 | Apagan el host viejo para ahorrar costo. |
| 09:55 | Reload de nginx: se arregla el 502 del host nuevo. |
| 10:20 | Vence el TTL: una hora de impacto para el usuario. |

**El costo no fue técnico**
- El arreglo tomó minutos; la espera del TTL tomó una hora.
- El MTTR mide tiempo de recuperación, no tiempo de escribir código.

<details><summary>Notas del orador</summary>

⏱ 6-9 min · La historia.

Leerla como una sucesión de decisiones razonables. El error no está en
09:12. Está en 09:19 (TTL sin bajar) y en 09:20 (proxy sin recargar).
Pausa en 09:40: apagar el host viejo convierte una versión antigua en un
servicio caído. Preguntar qué se perdió en ese momento: el rollback.

</details>

---

## 6. El smoke pasó, el usuario no

> Dos respuestas verdaderas al mismo tiempo

**Lo que midió el pipeline**
- `curl localhost:18081/` → `CitasYA api v2`.
- El puerto 18081 está publicado directo al contenedor.
- No pasa por nginx ni por el DNS del cliente.
- La puerta se abrió con el artefacto correcto.

**Lo que vio el usuario**
- Por el proxy nuevo: **502**.
- Por el proxy viejo: **v1**.
- El cliente con caché nunca alcanzó el `v2`.
- El cambio no existió para quien paga el servicio.

**La frase que se llevan**
- **Un `200` en `localhost` no prueba un despliegue.**
- La prueba tiene que entrar por el mismo camino que el usuario: nombre público, proxy y puerto real.
- Si la sonda corre al lado del servidor, siempre va a decir que está todo bien.

<details><summary>Notas del orador</summary>

⏱ 9-11 min · El centro del caso.

No avanzar hasta que alguien diga en voz alta la diferencia: el smoke
pegó al contenedor, el usuario pasa por el proxy y por el DNS.
La frase en negrita es la que se pide en el entregable.

</details>

---

## 7. DNS: el TTL decide cuándo cambia el mundo

> Registro A, caché y tiempo de expiración

```text
$ dig api.citasya.test A +noall +answer
api.citasya.test. 2340 IN A 127.0.0.2
$ curl --resolve api.citasya.test:18080:127.0.0.2 ...
CitasYA api v1
```

**Qué pasó con el nombre**
- El registro A pasó del host viejo al nuevo.
- El TTL quedó en 3600 segundos.
- Los resolutores guardaron la respuesta anterior.
- Cambiar el registro no cambia todas las copias a la vez.

**Qué se hace antes del corte**
- Bajar el TTL de 3600 a 60 con al menos una hora de anticipación.
- Esperar a que venza el TTL original antes de cambiar la IP.
- Mantener el host viejo arriba durante toda la ventana de caché.
- En el laboratorio, `--resolve` cumple el papel de esa caché.

<details><summary>Notas del orador</summary>

⏱ 11-13 min · DNS.

Explicar el TTL como 'cuánto tiempo una copia ajena puede seguir diciendo
la verdad de ayer'. El número 2340 es el tiempo que todavía falta.
El error no fue cambiar el registro: fue cambiarlo con TTL largo y apagar
el host anterior enseguida.

</details>

---

## 8. nginx: el nombre se resuelve una vez

> Docker DNS y el proxy no siempre están de acuerdo

```text
$ docker exec ... getent hosts api
172.28.16.11   api
$ docker exec ... nginx -T | grep proxy_pass
proxy_pass http://api:8000;
upstream: "http://172.28.16.10:8000/"
```

**Dos respuestas distintas**
- `getent` pregunta ahora: da la IP nueva.
- `nginx -T` muestra el nombre, no la IP.
- El proceso guardó la IP vieja al arrancar.
- El archivo no cambió, pero el proceso sí está desactualizado.

**El arreglo y la lección**
- `nginx -s reload` vuelve a resolver el nombre: el 502 desaparece sin tocar la configuración.
- Ese reload tiene que estar escrito en el pipeline, no en la memoria de quien está de guardia.

<details><summary>Notas del orador</summary>

⏱ 13-15 min · Resolución interna.

La comparación clave: el DNS interno ya dice .11 y los logs de nginx
muestran .10. Eso demuestra que el fallo está en el proceso, no en Docker.
Si alguien pregunta por `resolver`, explicar que acá no hay una directiva
que fuerce a nginx a volver a resolver: por eso hace falta el reload.

</details>

---

## 9. Los cinco flujos del caso

> Origen, destino, puerto y consecuencia

| Flujo | Origen → destino | Puerto | Qué falla |
|---|---|---|---|
| Resolución pública | cliente → resolutor | 53 | Caché con TTL 3600 |
| Entrada al proxy | cliente → host nuevo | 443 / 80 | Solo llega quien tiene la IP nueva |
| DNS interno | nginx → 127.0.0.11 | 53 | Nombre resuelto una sola vez |
| Proxy a la API | nginx → api:8000 | 8000 | IP vieja: 502 |
| Smoke | runner → host publicado | 18081 | Directo al contenedor: pasa |

**La regla para diagnosticar**
- Cada síntoma pertenece a un flujo: DNS, proxy, contenedor o medición.
- Sin el mapa dibujado, un 502 parece un bug de código y se pierde una hora buscando en el repo.

<details><summary>Notas del orador</summary>

⏱ 15-16 min · Los flujos.

Pedir al grupo que complete la columna 'Qué falla' antes de mostrarla.
La fila del smoke es la que explica por qué el dashboard decía verde.
Cerrar con la idea de capas: el mismo síntoma tiene dueños distintos.

</details>

---

## 10. Cinco porqués, una causa

> Del síntoma a la decisión de diseño

| Pregunta | Respuesta |
|---|---|
| ¿Por qué vieron v1 o 502? | El tráfico no llegó al contenedor `v2`. |
| ¿Por qué pasó el smoke? | Entró por 18081, sin proxy ni DNS. |
| ¿Por qué nginx siguió en la IP vieja? | Resolvió `api` al arrancar; no hubo reload. |
| ¿Por qué clientes seguían en el host viejo? | TTL de 3600 en caché de resolutores. |
| ¿Por qué empeoró al apagar el host? | Se fue el rollback tibio. |

**Causa raíz**
- **El pipeline verificó el artefacto, no verificó la ruta.**
- Las cinco piezas del caso anterior estaban presentes y aun así falló el despliegue.

<details><summary>Notas del orador</summary>

⏱ 16-17 min · Los porqués.

Esta tabla se puede tapar columna por columna. La última respuesta es la
que más discusión genera: mantener el host viejo cuesta dinero y es lo que
permite volver atrás durante una hora.
Cerrar señalando que las tres piezas clásicas ya estaban: por eso hacía
falta un caso nuevo.

</details>

---

## 11. Lo que agrega este caso

> Conceptos de DevOps y de redes que se ven acá

**DevOps: verificar la ruta**
- El smoke entra por la URL pública, con el `Host` real.
- La sonda corre fuera del servidor.
- Éxito es ver la versión nueva en el cliente.
- El reload del proxy es un paso del pipeline.

**Redes: resolución y caché**
- Registro A, TTL y resolutores caches.
- DNS interno de Docker y nombres de servicio.
- Un proxy puede guardar una IP resuelta.
- `dig`, `getent` y `curl --resolve` separan las capas.

**Operación: rollback tibio**
- El host viejo sigue arriba durante la ventana de TTL.
- El TTL se baja antes del corte, no después.
- Volver no es reconstruir: es seguir sirviendo.
- El MTTR incluye esperar a que expire la caché.

**Las cuatro claves DORA en este caso**
- Frecuencia y lead time no cambiaron: el build estuvo bien.
- La tasa de fallo la puso el usuario, no el pipeline.
- El MTTR fue de una hora y lo dominó el TTL, no el arreglo del proxy.

<details><summary>Notas del orador</summary>

⏱ 17-19 min · Conceptos.

Pedir que clasifiquen cada idea en DevOps o redes. La respuesta correcta
es que casi todas son de redes: DevOps decide que se verifiquen y se
automaticen.
DORA se menciona solo para ubicar el MTTR: mejorar el build no baja el
tiempo de recuperación si la recuperación depende de un TTL.

</details>

---

## 12. Cierre y práctica

> Laboratorio 16: reproduce las dos fallas en tu Docker

**Entregable**
- Bitácora de los 7 pasos con la IP de `api` en cada momento.
- Smoke en verde, proxy nuevo en 502 y cliente cacheado en `v1`.
- Un comando por falla: `getent hosts`, `nginx -T`, `curl --resolve`.
- Plan de corrección de cinco líneas.

**Tres frases para repetir**
- Un `200` en `localhost` no prueba un despliegue.
- Cambiar el DNS no cambia todas las copias a la vez.
- Sin host viejo arriba no hay rollback durante el TTL.

**Pregunta final**
- ¿Por qué el smoke puede decir que todo está bien mientras el usuario ve un 502?
- Respuesta corta: porque midió el artefacto en su puerto, sin pasar por el DNS ni por el proxy que usa el usuario.
- Carpeta: `DevOps/Laboratorio-16-Despliegue-Invisible/`.

<details><summary>Notas del orador</summary>

⏱ 19-20 min · Cierre.

Hacer la pregunta final al grupo y esperar la respuesta antes de leerla.
El laboratorio ya trae los archivos, la evidencia de la prueba ejecutada
y los comandos de limpieza. No depende de ningún otro laboratorio.

</details>

---

