# Teoría — Unidad III · Parte 4: Almacenamiento compartido para alta disponibilidad

> Contenido completo de [`Teoria-U3-Parte4-Almacenamiento-Compartido.pptx`](Teoria-U3-Parte4-Almacenamiento-Compartido.pptx) (15 diapositivas, 16:9).
> Volcado textual de la presentación: mismo contenido y mismo orden de
> lectura, sin depender de PowerPoint.
>
> Se regenera con:
> `python3 tools/dump_ppt_md.py Teoria-U3-Parte4-Almacenamiento-Compartido.pptx "Unidad III · Parte 4: Almacenamiento compartido para alta disponibilidad"`
>
> Cada diapositiva conserva sus **notas del orador** al final, en bloques
> plegables: en GitHub y en la mayoría de editores se despliegan con un clic.

## Índice

- **1.** Unidad III — Parte 4
- **2.** Qué vamos a ver en esta parte
- **3.** El dato no es desechable
- **4.** Repaso: dónde viven los datos hoy
- **5.** Qué significa alta disponibilidad (HA)
- **6.** Dos filosofías: shared-everything vs shared-nothing
- **7.** DAS, NAS y SAN: el mapa del almacenamiento
- **8.** El storage compartido ES un problema de red
- **9.** Quórum: evitar el split-brain
- **10.** Almacenamiento distribuido: replicar por software
- **11.** Cómo lo consume el orquestador
- **12.** El puente alcanzable: un volumen NFS en Compose
- **13.** Patrones: qué hacer con cada tipo de estado
- **14.** Anti-patrones: los que tumban producción
- **15.** Autoevaluación y cierre

---

## 1. Unidad III — Parte 4

**UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES**

Almacenamiento compartido para alta disponibilidad

- Extensión del tema 3.5 · de un host con Compose a un clúster HA
- Dónde viven los datos cuando un nodo muere: NAS, SAN, quórum, réplicas
- Material de integración · semanas 12-13 · Proyecto Final

<details><summary>Notas del orador</summary>

⏱ 0-3 min · Apertura de la Parte 4 (extensión).

Esta parte no es del programa original: es la pregunta que la Parte 3 dejó
abierta y que todo el mundo encuentra en producción. Frase de apertura:
'el orquestador mueve contenedores; el dato no se mueve solo'.
Va después de las presentaciones del semestral y del Lab 14, como profundización.

</details>

---

## 2. Qué vamos a ver en esta parte

> La pregunta que quedó abierta al final de la Parte 3

| # | Tema | Qué resuelve | Min |
|---|---|---|---|
| — | Almacenamiento compartido (DAS/NAS/SAN/distribuido) | Que el dato sobreviva al nodo caído | 20 |
| — | Quórum y fencing | Evitar el split-brain cuando la red se parte | 10 |
| — | Volúmenes del orquestador (NFS/CSI) | Declarar el almacenamiento como declaras los servicios | 15 |
| — | Patrones y anti-patrones de datos | Qué se replica, qué se comparte, qué no se toca | 10 |

**La pregunta que quedó abierta**
- La Parte 3 cerró con: «Swarm mueve el contenedor al nodo sano».
- Pero el **volumen** era local al nodo: la réplica de la db levanta en otro host…
- …y no encuentra `/var/lib/postgresql/data`.
- **El contenedor es desechable; el dato, no.**

**Lo que NO es esta parte**
- No es un curso de Kubernetes ni de Ceph.
- Es la capa **red + datos** que todo clúster HA necesita.
- En producción, la mayoría de caídas «del servidor» son de storage o de red:
- las dos cosas que este curso enseña.

<details><summary>Notas del orador</summary>

⏱ 3-5 min · Agenda.

Ancla la parte en algo que ya vieron: el `pgdata` del Lab 14. Ahí está el
conflicto entero en un ejemplo. Si alguien preguntó '¿y si se cae la máquina'
en la Sesión 4, esta presentación es la respuesta completa.

</details>

---

## 3. El dato no es desechable

De «el contenedor se reinicia solo» a «el dato sobrevive al nodo»

- Repaso: dónde viven los datos en Compose
- Los modelos: DAS, NAS, SAN — y el distribuido
- Quórum: por qué 3 nodos y no 2

25 min

<details><summary>Notas del orador</summary>

⏱ 5-6 min · Transición al bloque técnico.

</details>

---

## 4. Repaso: dónde viven los datos hoy

> El volumen del Lab 14, visto con lupa

```text
$ docker volume ls
DRIVER    VOLUME NAME
local     lab14-sesion-4_pgdata
$ docker compose down    # conserva pgdata
$ docker compose down -v # borra pgdata
```

**En el Lab 14 (Sesiones 3-4)**
- La db escribe en el volumen `pgdata`.
- El contenedor se recrea; el dato sigue ahí.
- `down` sin `-v` = política de datos ya aprendida (Drill 6 del refuerzo).

| Mecanismo | Qué es | Quién lo gestiona | ¿Sobrevive a `down`? |
|---|---|---|---|
| bind mount | una carpeta del host (`./datos`) | tú, a mano | sí (es del host) |
| volume | `pgdata`, gestionado por Docker | Docker | sí (salvo `-v`) |
| tmpfs | RAM, nunca toca disco | Docker | no |

**El «pero» que motiva toda esta parte**
- **Ese volumen vive en UN solo host: si el nodo muere, el dato muere con él. Escalar la db sin storage compartido =** **dos bases divergentes****.**

<details><summary>Notas del orador</summary>

⏱ 6-11 min · Repaso de volúmenes.

No asumas que lo recuerdan: haz la pregunta '¿dónde quedó la base del Lab 14
cuando hicimos down?' y deja que lo respondan.
El paso de bind mount → volume ya lo vieron; aquí solo hace falta nombrarlo.
El callout rojo es la bisagra: léelo en voz alta y no avances hasta que cale.

</details>

---

## 5. Qué significa alta disponibilidad (HA)

> No es tener réplicas: es seguir sirviendo cuando algo muere

**99,9 %**
≈ 8,8 h/año caído

**99,99 %**
≈ 53 min/año caído

**RTO**
cuánto tarda en volver

**RPO**
cuánto dato se pierde

**SPOF: el punto único de falla**
- Cualquier componente sin respaldo: la fuente, el switch de salida,
- el nodo, el disco… **y la persona que solo ella sabe reiniciar**.
- HA = eliminar SPOF **capa por capa** (energía, red, nodo, dato).

**Réplicas ≠ datos disponibles**
- 3 réplicas de la api **sin estado** = HA fácil (Parte 3).
- La db **con estado** = el problema real de esta parte.
- **Stateless es barato; stateful es difícil.**

**La definición en una línea**
- **Un sistema HA sigue sirviendo cuando falla un componente cualquiera — y no pierde los datos que ya había comprometido.**
- RTO y RPO son los dos números que un jefe entiende: cuánto tiempo y cuánto dato.

<details><summary>Notas del orador</summary>

⏱ 11-16 min · Qué es HA.

Los porcentajes de disponibilidad suelen sorprender: 99,9 % son casi 9 horas
al año. Pregunta cuántas 9 exige un banco y cuántas un blog.
RTO/RPO en una frase cada uno; no hace más detalle hoy.

</details>

---

## 6. Dos filosofías: shared-everything vs shared-nothing

> Todo clúster de datos elige uno de estos dos caminos

|  | Shared-everything | Shared-nothing |
|---|---|---|
| Idea | todos los nodos ven el mismo almacenamiento | cada nodo tiene su copia y se sincroniza |
| Ejemplos | Oracle RAC sobre SAN · VMs sobre NFS | réplica de PostgreSQL · Ceph · Galera |
| Si un nodo muere | otro monta el mismo dato | otro promueve su réplica |
| Riesgo clásico | dos escritores = corrupción (split-brain) | lag de replicación (última transacción) |
| Exigencia de red | subred de storage muy estable y rápida | ancho de banda para replicar |

**Dónde vive cada cosa hoy**
- VMs y archivos → NFS/SAN sigue siendo el estándar.
- Bases de datos → hoy se prefiere **replicar** (shared-nothing).
- Ninguno es «mejor»: cambian el punto de falla y el costo.

**En contenedores**
- Swarm y Kubernetes **no replican volúmenes**: el dato sigue al nodo.
- El orquestador orquesta **procesos**; el dato lo orquesta el storage.
- Por eso el estado migra a servicios especializados (siguientes láminas).

<details><summary>Notas del orador</summary>

⏱ 16-21 min · Los dos modelos.

La analogía que funciona: shared-everything es una pizarra común (todos ven
lo mismo, pero pueden chocar al escribir); shared-nothing es que cada uno
fotocopie la pizarra (chocan menos, pero la copia llega tarde).
Insiste en la caja derecha: el orquestador NO resuelve esto por ti.

</details>

---

## 7. DAS, NAS y SAN: el mapa del almacenamiento

> Tres formas de conectar discos — y dónde entra cada protocolo

| Nivel | Qué es | Protocolo típico | El cliente ve |
|---|---|---|---|
| DAS | disco pegado al servidor | SATA / SAS | un disco local (`/dev/sdb`) |
| NAS | servidor de archivos en la LAN | NFS / SMB | una carpeta montada (`/mnt/datos`) |
| SAN | red dedicada de bloques | iSCSI / Fibre Channel | un disco (el formato lo pone el cliente) |
| Objeto | almacenamiento por API (nube) | S3 sobre HTTP | URLs con binarios |

**La diferencia que importa (y se pregunta en el examen)**
- NAS comparte **archivos**: el servidor coordina los accesos; varios clientes a la vez, sin peligro.
- SAN comparte **bloques**: si dos máquinas montan el mismo LUN sin coordinarse, **lo corrompen**.

**Traducción a contenedores**
- Un volumen NFS es **NAS**: varios nodos montan la misma carpeta. Un LUN iSCSI es **SAN**: un solo dueño a la vez.

<details><summary>Notas del orador</summary>

⏱ 21-26 min · DAS/NAS/SAN.

Truco para que no se olviden: DAS = Directo, NAS = Archivos (Network **File**
System), SAN = Bloques (Storage Area Network = red de **discos**).
La fila «objeto» está para cerrar el mapa: S3/MinIO aparecen de nuevo en la
lámina de patrones.

</details>

---

## 8. El storage compartido ES un problema de red

> Por esto el tema está en un curso de redes y no de sistemas

**Aplicación**
lee/escribe archivos

**Sistema de archivos**
NFS · iSCSI · SMB

**La red**
TCP/IP o Fibre Channel

**El array**
NAS / SAN

| Protocolo | Puerto | Qué transporta |
|---|---|---|
| NFS | 2049 TCP/UDP | archivos sobre la LAN (Linux) |
| SMB/CIFS | 445 TCP | archivos (mundo Windows) |
| iSCSI | 3260 TCP | SCSI (bloques) dentro de TCP/IP |
| Fibre Channel | red propia, sin TCP | bloques, latencia mínima |

**Reglas de la subred de storage**
- VLAN/subred **dedicada** (como `back` en el Lab 14).
- Que no atraviese routers ni WAN.
- Jumbo frames (MTU 9000) para menos overhead.

**Por qué esto es de ESTE curso**
- Cada escritura = ida y vuelta: la latencia (3.2) se paga **dos veces**.
- Jitter en la red de storage = rendimiento errático en toda la app.
- Se diseña con VLSM y VLAN como cualquier otra red (3.1).

<details><summary>Notas del orador</summary>

⏱ 26-32 min · El ángulo de red.

Esta es la lámina que justifica la presentación en el pénsum: el storage
compartido no es un periférico, es TRÁFICO DE RED.
iSCSI es literalmente SCSI encapsulado en TCP: puedes verlo en Wireshark
(filtro `tcp.port == 3260`), igual que vieron la trama del Lab 4.
Conecta con las 4 métricas del tema 3.2: latencia y jitter, de nuevo.

</details>

---

## 9. Quórum: evitar el split-brain

> El desastre clásico cuando la red falla a medias

**2 nodos**
sin mayoría: peligro

**3 nodos**
toleran 1 caído

**5 nodos**
toleran 2 caídos

**N/2+1**
la mayoría que decide

**Split-brain**
- La red se parte en dos mitades.
- Cada mitad cree que la otra murió.
- Ambas escriben el mismo disco → **corrupción**.
- La falla no fue de discos: fue de **red**.

**Fencing (exclusión)**
- Apartar **por la fuerza** al nodo sospechoso.
- Que no pueda volver a escribir («shoot the other node in the head»).
- Mejor un nodo sano apagado que un disco corrupto.

**Dónde ya lo viste**
- Los **managers** de Swarm sincronizan estado con **Raft**.
- 3 managers toleran 1 caído: mismo quórum.
- Ojo: Raft protege los **metadatos** del cluster, no tus datos.

**Moraleja de diseño**
- Los clústeres pares (2, 4) tienen el mismo problema: agrega nodos **impares** y deja un árbitro (witness) si el presupuesto no da.

<details><summary>Notas del orador</summary>

⏱ 32-37 min · Quórum.

Ejemplo en vivo si quieres: con 3 personas votando a mano, pide que se tapen
los ojos dos de tres: la mayoría no existe y nadie decide escribir.
El detalle fino: Swarm elige 3 managers por la misma matemática.
El error común que hay que desmontar: 'Raft ya replica, mis datos están
seguros'. No: Raft replica el ESTADO DEL CLUSTER (servicios, secretos).

</details>

---

## 10. Almacenamiento distribuido: replicar por software

> La SAN es hardware; la alternativa moderna es software sobre Ethernet

**La idea (Ceph, GlusterFS, Longhorn, MinIO)**
- N nodos con discos comunes, conectados por Ethernet.
- Cada dato se guarda en **≥ 2** de ellos.
- El conjunto expone **un** disco/cubo virtual al orquestador.

**El precio**
- 2-3× el espacio bruto en disco.
- Confirmar tras escribir en ≥ 2 réplicas: seguro, pero más lento.
- La red de replicación se dimensiona (3.1) y se vigila (3.2).

**Escritura**
la app escribe 1 dato

**Replicación**
se copia a otros nodos

**ACK**
confirman al cliente

**Listo**
consistente y tolerante

**Conclusión del bloque técnico**
- **NAS, SAN o distribuido — los tres son** **tráfico de red****: elegir uno es un ejercicio de direccionamiento, aislamiento y presupuesto de ancho de banda.**
- No hay que instalar ninguno en el curso: hay que saber qué elegiría y por qué.

<details><summary>Notas del orador</summary>

⏱ 37-40 min · Distribuido.

Ceph es el ejemplo canónico; no hace falta más nombre. Si alguien pregunta
por cloud: EBS/S3 de AWS es esto administrado por otro (y cobrado por GB).
Cierra el bloque aquí: hasta ahora el QUÉ; lo que sigue es el CÓMO se consume.

</details>

---

## 11. Cómo lo consume el orquestador

> El mismo giro declarativo de la Parte 3, ahora para el disco

| Nivel | Mecanismo | Detalle |
|---|---|---|
| Compose (1 host) | `volumes:` + driver local | el volumen vive en el host (Lab 14) |
| Swarm (N nodos) | el mismo YAML + driver externo (NFS) | el volumen debe existir en todos los nodos |
| Kubernetes | PV / PVC + StorageClass (CSI) | pides «10 Gi» y el cluster los consigue |

**La idea declarativa, ahora para el disco**
- Igual que `DB_HOST=db` evitó las IP (Parte 3),
- el **PVC** evita «monta 172.28.30.20:/export».
- Declaras **qué** necesitas (10 Gi, un escritor),
- y el orquestador decide **dónde y cómo**.

**CSI: el estándar de la capa**
- **C**ontainer **S**torage **I**nterface.
- Cualquier storage (NFS, Ceph, nube) habla el mismo idioma
- con cualquier orquestador (Swarm, K8s, Nomad).
- Es para el storage lo que Ethernet es para la red:
- un estándar de **interfaz**, no un producto.

<details><summary>Notas del orador</summary>

⏱ 40-43 min · Cómo lo consume el orquestador.

El paralelo con `DB_HOST=db` es la llave: la Parte 3 ya les enseñó a no
depender de la IP; esto es lo mismo un piso más abajo.
CSI nómbralo y pasa: lo importante es el patrón declarativo.

</details>

---

## 12. El puente alcanzable: un volumen NFS en Compose

> El mismo YAML del Lab 14, cambiando una sola pieza

```text
services:
db:
volumes:
- pgdata:/var/lib/postgresql/data
volumes:
pgdata:
driver_opts:
type: nfs
o: addr=172.28.30.20,rw,nfsvers=4
device: ":/export/pgdata"
```

**Qué cambia**
- El YAML es casi el del Lab 14.
- El volumen ya no vive en el host: vive en el NAS.
- Cualquier nodo que levante el stack ve el mismo dato.

**Cómo se verifica**
- **`docker volume inspect pgdata`** muestra el driver nfs.
- Dos contenedores leen el mismo archivo desde el mismo volumen.
- `down` sin `-v`: el dato sigue en el NAS.

```text
$ docker volume create --driver local \
--opt type=nfs --opt o=addr=172.28.30.20,rw \
--opt device=:/export/pgdata  pgdata
```

**La red de storage, ahora en el diseño**
- 172.28.30.0/24 es la tercera subred, después de `front` y `back` (Lab 14): NFS/iSCSI viaja en su propia VLAN, lejos de la LAN de usuarios.

<details><summary>Notas del orador</summary>

⏱ 43-48 min · El puente alcanzable.

Si hay docker a mano y un servidor NFS (o un contenedor `erichough/nfs-server`),
la demo vale la pena: es literalmente cambiar el bloque `volumes:` del Lab 14.
El comando de abajo es la versión imperativa, para crear el volumen a mano.
Subraya la subred: están diseñando la VLAN de storage con VLSM, como el Caso 3.

</details>

---

## 13. Patrones: qué hacer con cada tipo de estado

> La decisión de diseño que el Proyecto Final te pide justificar

| Pieza | ¿Tiene estado? | Patrón HA recomendado |
|---|---|---|
| web / api | no | N réplicas + balanceo (routing mesh, Parte 3) |
| sesiones de usuario | poco | Redis/JWT fuera del contenedor |
| base de datos | sí | réplica nativa o failover gestionado (1 escritor) |
| archivos / imágenes | sí | objetos (S3/MinIO) o NFS compartido |
| logs y métricas | sí | enviarlos fuera del nodo (remoto) |

**Regla práctica**
- **Stateless primero**: cada byte de estado que quitas del contenedor es un SPOF menos.
- La escalera del REFUERZO llega a `--scale api=N`; esta parte añade el peldaño de los **datos**.
- La db del Proyecto no necesita SAN ni Ceph: necesita volumen nombrado + política de respaldo documentada.

<details><summary>Notas del orador</summary>

⏱ 48-50 min · Patrones.

La tabla es la lámina que se llevan al Proyecto: léela por filas.
Insiste en la última línea del callout: el curso no pide instalar HA real;
pide entender qué haría falta y decirlo por escrito.

</details>

---

## 14. Anti-patrones: los que tumban producción

> Los cinco que se repiten en todos los incidentes

| Síntoma | Causa | Arreglo |
|---|---|---|
| el dato desaparece al reiniciar | bind mount del host en un clúster | volumen con driver NFS o distribuido |
| dos réplicas de la db «divergen» | escalar la db como si fuera stateless | 1 escritor + réplicas o failover gestionado |
| disco corrupto tras caída de red | clúster de 2 nodos sin quórum | 3 o 5 nodos + fencing |
| se pierde todo tras mantenimiento | `down -v` en producción | `-v` solo en dev; respaldo + RPO definido |
| secretos legibles en la red | NFS sin cifrar comparte credenciales | secrets cifrados (Parte 3) + VLAN interna |

**El patrón detrás de los cinco**
- **Casi todos son el mismo error:** **tratar un servicio con estado como si no lo tuviera****.**
- El orquestador escala lo que le das; distinguir lo escalable es trabajo tuyo.

<details><summary>Notas del orador</summary>

⏱ 50-52 min · Anti-patrones.
Cada fila es una historia real de guardia. La fila 2 es la más común en
proyectos de estudiantes: `--scale db=2` y a correr.

</details>

---

## 15. Autoevaluación y cierre

> Si puedes responder esto en voz alta, la parte quedó

**Responde en voz alta**
- ¿Por qué el volumen de Compose no basta en un clúster multi-nodo?
- ¿NAS vs SAN en una frase? (archivos vs bloques)
- ¿Por qué un clúster de 2 nodos es más peligroso que uno de 3?
- iSCSI: ¿qué transporta y en qué puerto? (SCSI sobre TCP, 3260)
- ¿Qué patrón HA eliges para la db del Proyecto y por qué?

**Para el Proyecto Final**
- No se pide SAN ni Ceph: se pide **justificar la decisión**.
- «Nuestra db es stateful; elegimos volumen nombrado + respaldo, porque…».
- Documentar `down` sin `-v` ya es señal de madurez.

**El hilo completo de la unidad**
- Red segmentada (3.1) → acceso por llave (3.3) →
- un solo punto de exposición (3.4) →
- orquestación (3.5) →
- **y el dato que sobrevive al nodo** (Parte 4).

<details><summary>Notas del orador</summary>

⏱ 52-55 min · Autoevaluación y cierre.

Las cinco preguntas son el filtro de la parte; la segunda y la cuarta son
las que separan quién entendió de quién memorizó.
Cierra con el hilo de la caja azul: toda la unidad es una sola historia,
y esta parte es su final honesto.

</details>

---

