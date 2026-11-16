# Unidad III — Guía de uso de las presentaciones

Clase de **2 h 45 min (165 min)** dividida en tres partes de **55 minutos**.
Cada presentación trae **notas del presentador** con el minuto exacto de cada
diapositiva, así que basta con abrirla en modo presentación y avanzar con el reloj a la vista.

| Parte | Archivo | Temas | Diapositivas | Min |
|-------|---------|-------|--------------|-----|
| 1 | `../Teoria/Teoria-U3-Parte1-LAN-Monitoreo.pptx` | 3.1 LAN · 3.2 Monitoreo | 18 | 55 |
| 2 | `../Teoria/Teoria-U3-Parte2-SSH-Bastion.pptx` | 3.3 Claves SSH · 3.4 Bastión | 13 | 55 |
| 3 | `../Teoria/Teoria-U3-Parte3-Orquestacion.pptx` | 3.5 Orquestación (Compose/Swarm) | 12 | 55 |
| | | **Total** | **43** | **165** |

### Documentos que acompañan cada parte

| Parte | Guion docente | Versión en texto |
|-------|---------------|------------------|
| 1 | `CLASE-U3-LAN-Monitoreo.md` | `../Teoria/TEORIA-U3-Parte1-LAN-Monitoreo.md` |
| 2 | `CLASE-U3-Parte2-SSH-Bastion.md` | `../Teoria/TEORIA-U3-Parte2-SSH-Bastion.md` |
| 3 | `CLASE-U3-Parte3-Orquestacion.md` | `../Teoria/TEORIA-U3-Parte3-Orquestacion.md` |

Además, para los temas 3.1/3.2 hay una **guía de estudio del estudiante**
(`GUIA-ESTUDIO-U3-LAN-Monitoreo.md`: repaso + banco de preguntas). Los **guiones
docentes** traen el *minuto a minuto* y las prácticas; las **versiones en texto**
son el volcado de las diapositivas con sus notas del orador.

> **Sesión de cierre (opcional, después de la Parte 4):** DevOps en una sesión de
> 165 min con **caso de estudio** («el despliegue del viernes»). El enfoque sigue
> siendo **redes**: los flujos del despliegue (puertos, NAT, subredes, cifrado), el
> smoke test y el rollback en dos comandos. Su teoría va en
> `../DevOps/Teoria-DevOps-Despliegue.pptx` (**55 min**, 17 diapositivas · texto en
> `../DevOps/TEORIA-DEVOPS-DESPLIEGUE.md`) y su práctica en
> `../DevOps/Laboratorio-15-DevOps-Despliegue/` (archivos listos + guía de 10
> comandos, planteada como caso de estudio).
>
> El guion minuto a minuto de esa sesión está en `../DevOps/DOCENTE/CLASE-DEVOPS.md`,
> que no se versiona.

---

## Cómo usarlas

- **Notas del presentador:** en PowerPoint, `Vista → Notas`. En LibreOffice Impress,
  `Vista → Notas`. Ahí está el reparto de minutos diapositiva por diapositiva.
- **Tiempo de transición:** ya está incluido (cada parte empieza con portada y agenda).
  Si se atrasa, se recorta la práctica, no las diapositivas de concepto.
- **Partes independientes:** se pueden abrir en cualquier orden, aunque el hilo
  recomendado es 1 → 2 → 3 (la red, el acceso, el despliegue).
- **Diapositivas de práctica:** las que dicen «demo» o «caja roja» están pensadas
  para demonstration en vivo. Si falla la demo, la caja roja tiene el texto
  completo para explicar de todos modos.

---

## Parte 1 · LAN y monitoreo (55 min)

Temas 3.1 y 3.2 del programa.

| Min | Contenido |
|-----|-----------|
| 0-3 | Portada y encuadre |
| 3-5 | Agenda |
| 5-6 | Transición a 3.1 |
| 6-9 | Qué es una LAN (repaso de Unidad I) |
| 9-12 | Por qué una LAN plana se degrada |
| **12-20** | **VLAN (802.1Q)** — el bloque central de esta parte |
| 20-23 | Subredes (capa 3) |
| 23-26 | VLAN vs subred |
| 26-28 | DHCP (DORA) |
| 28-31 | DNS y NAT |
| 31-35 | Router de capa 3 |
| 35-37 | Ruta de ida y vuelta |
| 37-38 | Transición a 3.2 |
| 38-41 | Las cinco métricas de red |
| 41-45 | Las cuatro herramientas |
| 45-49 | `iperf3`: TCP vs UDP |
| 49-52 | Monitoreo por capas OSI |
| 52-55 | Cierre y autoevaluación |

**Sobre VLAN.** No aparece como tema explícito en el analítico del programa, pero
sí como conocimiento de apoyo en el Lab 10, y es el puente natural entre la LAN
plana y los bridges de Docker. Por eso se incluye como bloque central dentro del
tema 3.1, no como tema aparte. Si prefieres no cubrirlo, se puede saltar la
diapositiva 6 y la clase sigue cuadrando en ~47 min.

---

## Parte 2 · SSH y bastión (55 min)

Temas 3.3 y 3.4 del programa.

| Min | Contenido |
|-----|-----------|
| 0-3 | Portada |
| 3-5 | Agenda |
| 5-6 | Transición a 3.3 |
| 6-10 | El problema de la contraseña |
| 10-15 | Par de llaves y criptografía asimétrica |
| 15-20 | `ssh-keygen` y permisos |
| 20-22 | El servidor OpenSSH y el orden de endurecimiento |
| 22-23 | Transición a 3.4 |
| 23-28 | Qué es un bastión y por qué existe |
| 28-32 | Single-homed, dual-homed, multihomed |
| 32-40 | Bastión web: proxy inverso y firewall |
| 40-48 | `ProxyJump` y túneles SSH |
| 48-55 | Cierre, autoevaluación y puente a la Parte 3 |

**Demos que valen la pena hacer en vivo:**
1. `ssh-keygen` + `ssh-copy-id` — 1 minuto, y la clase entera cobra sentido.
2. `ssh -L` contra la base de datos del laboratorio — muestra por qué la DB
   no necesita puerto publicado.

**Errores que conviene anticipar** (están en las notas):
- Permisos abiertos en `~/.ssh` → SSH se niega a leer la llave.
- Apagar contraseñas antes de tener llave autorizada → lock-out.
- Crear la red interna sin `--internal` → el dual-homed es decorativo.

---

## Parte 3 · Orquestación (55 min)

Tema 3.5 del programa. Es la parte con más peso en la rúbrica del proyecto.

| Min | Contenido |
|-----|-----------|
| 0-3 | Portada |
| 3-5 | Agenda |
| 5-6 | Transición a 3.5 |
| 6-11 | Qué significa orquestar (las 6 capacidades) |
| 11-16 | Compose vs Swarm |
| 16-22 | `compose.yml` y escalado |
| 22-27 | Nodos manager y worker |
| 27-33 | Réplicas, routing mesh y auto-curación |
| 33-37 | Secretos en `/run/secrets` |
| 37-40 | Rolling update, rollback y `stack deploy` |
| 40-48 | Cierre de la unidad |
| 48-55 | Autoevaluación y tareas para la próxima clase |

**Demos que valen la pena hacer en vivo:**
1. `docker compose up --scale api=3` + `getent hosts api` → 3 IPs. Prueba directa
   del ítem de rúbrica.
2. `curl` repetido al routing mesh para mostrar que cambia el nodo que responde.
3. Matar un contenedor y ver cómo el manager lo vuelve a crear.

---

## Si hay que recortar

Los 43 puntos se pueden bajar a ~110 min sin romper el hilo:

- **Cortar primero:** las demos en vivo (15 min), la diapositiva de VLAN (8 min),
  la comparación de tipos de bastión (4 min).
- **Nunca cortar:** la criptografía asimétrica (5), las 6 capacidades de
  orquestación (5) y la autoevaluación final (7). Son los tres bloques que
  más se preguntan y los que atan la unidad.
