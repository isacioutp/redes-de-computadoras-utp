# Guía de estudio — Laboratorio N.º 14

Repaso del laboratorio y **banco de preguntas con respuestas** para preparar la
evaluación. Complementa [TEORIA.md](TEORIA.md) y las 4 sesiones.

> **Cómo usarla:** primero lee el repaso (sección 1) y contesta el banco
> (sección 2) **sin mirar las respuestas**. Luego compara y marca lo que falló.

---

## 1. Repaso en 10 ideas

1. **Segmentar** (VLAN → red bridge) aísla el broadcast y las fallas.
2. **VLSM** ajusta cada subred a los hosts que de verdad necesita.
3. **DHCP** asigna (DORA); **DNS** traduce nombres; **NAT** permite salir.
4. El **router** une subredes, pero solo si hay **ruta de ida y vuelta**.
5. `internal: true` deja una red Docker **sin salida a Internet**.
6. Un **bastión** es el único punto de entrada a una red privada.
7. Un bastión **contenedorizado no es un bastión real**: comparte kernel. El
   bastión real es el **host** (SSH por llave).
8. **Monitorear** = medir ancho de banda, latencia, pérdida, jitter y throughput.
9. **Orquestar** = declarar el estado deseado (`docker-compose.yml`) y dejar que
   el motor lo reconcilie (crear, escalar, reiniciar).
10. **Compose** es para un host; **Swarm** es multi-nodo (overlay, balanceo,
    rolling update). El mismo YAML migra de uno a otro.

---

## 2. Banco de preguntas

### Bloque A — LAN y segmentación

**A1.** ¿Por qué una LAN plana se degrada? Menciona 3 razones.
> *R:* Una sola tormenta de broadcast afecta a todos; no hay aislamiento (un
> host comprometido alcanza a todos); no se prioriza el tráfico crítico.

**A2.** ¿Qué objeto de Docker equivale a una VLAN?
> *R:* Una red **bridge** (`docker network`) por proyecto.

**A3.** Calcula la máscara para 30 hosts.
> *R:* Se necesitan 5 bits de host (2⁵−2 = 30) → prefijo `/27`
> (255.255.255.224).

**A4.** ¿Qué hace `internal: true` y qué **no** hace?
> *R:* Quita la salida a Internet (NAT) de esa red. **No** impide que un
> contenedor de otra red alcance a uno de esta si este **publica** un puerto.
> Para eso hay que no publicar puertos.

**A5.** ¿Por qué el API puede estar en `front` y `back` pero la DB no?
> *R:* El API es el **puente de aplicación** (necesita hablar con la web y con la
> DB). La DB solo la consume el API, así que vive **solo** en `back`: menos
> superficie de ataque.

### Bloque B — Monitoreo

**B1.** Empareja métrica ↔ herramienta: ancho de banda, latencia, throughput.
> *R:* ancho de banda → `iftop`/netdata; latencia → `ping`/`mtr`; throughput →
> `iperf3`.

**B2.** ¿Qué diferencia hay entre `iperf3` TCP y UDP?
> *R:* TCP ajusta ventana y reintenta (sin pérdidas, throughput menor). UDP no
> controla flujo (throughput alto, puede haber pérdidas y jitter).

**B3.** ¿Qué comando captura solo HTTP en la interfaz del contenedor?
> *R:* `tcpdump -i eth0 -n port 80`.

**B4.** ¿A qué equivale la Simulation mode de Packet Tracer en Docker?
> *R:* `tcpdump`: ver el paquete real en la interfaz, pero sin inspección salto a
> salto.

### Bloque C — SSH y bastión

**C1.** ¿Cuál de las dos llaves se comparte y cuál se protege?
> *R:* La **pública** se coloca en el servidor (`authorized_keys`); la
> **privada** se protege con `chmod 600` y nunca se comparte.

**C2.** ¿Por qué `ed25519` sobre RSA?
> *R:* Llaves más cortas, generación y firma más rápidas, seguridad moderna.

**C3.** ¿Qué hace `ssh -L 5432:db.local:5432 usuario@host`?
> *R:* Reenvío local: el puerto 5432 de tu máquina se conecta, a través del host,
> al 5432 de `db.local`. Permite alcanzar la DB **sin publicarla**.

**C4.** ¿Qué hace `ssh -J bastion usuario@interno`?
> *R:* ProxyJump: salta por el bastión para llegar al equipo interno.

**C5.** Nombra 3 razones por las que un bastión **no** debe ser un contenedor.
> *R:* Kernel compartido (romper uno compromete a todos); interfaces virtuales
> (no hay perímetro físico); el firewall real es iptables del host (invisible).

### Bloque D — Orquestación con Compose

**D1.** Diferencia `docker run` de `docker compose up`.
> *R:* `run` ejecuta un contenedor de forma imperativa; `compose up` levanta todo
> el stack desde un archivo declarativo (estado deseado, dependencias, redes,
> volúmenes).

**D2.** ¿Cómo escala Compose y cómo balancea?
> *R:* `--scale servicio=N`; el DNS embebido devuelve las N IPs (round-robin de
> nombres), no hay proxy dedicado.

**D3.** ¿Qué ventaja tiene `secrets:` frente a `environment:`?
> *R:* El secreto se monta en `/run/secrets` y **no** aparece en el YAML ni (por
> defecto) en `docker inspect`; `environment` lo deja en texto plano visible.

**D4.** ¿Qué hace `depends_on: condition: service_healthy`?
> *R:* Arranca un servicio solo cuando el otro pasó su `healthcheck` (orden de
> arranque basado en salud, no solo en creación).

**D5.** Menciona 3 cosas que Compose **no** hace y Swarm sí.
> *R:* (1) cluster multi-nodo; (2) red overlay entre nodos; (3) balanceo ingress
> mesh + rolling update/rollback gestionado.

**D6.** ¿Qué conserva y qué borra `docker compose down`?
> *R:* `down` apaga y borra contenedores/redes pero **conserva** los volúmenes;
> `down -v` **borra** también los volúmenes (adiós datos).

---

## 3. Autoevaluación

Marca lo que ya dominas:

- [ ] Explico la diferencia entre segmentar con VLAN y con red bridge.
- [ ] Sé por qué `internal: true` no sustituye a "no publicar puertos".
- [ ] Instalé una llave SSH y entré sin contraseña.
- [ ] Puedo explicar por qué el host es el bastión real.
- [ ] Sé leer un `docker-compose.yml` con redes, secretos y healthchecks.
- [ ] Puedo escalar un servicio y mostrar el balanceo por DNS.
- [ ] Sé qué diferencia Compose de Swarm.
- [ ] Puedo respaldar y restaurar la base de datos.

---

## 4. Errores frecuentes (y cómo evitarlos)

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| `front` alcanza la DB | la red `back` no es `internal` o la DB publica `ports:` | quitá `ports:` de la DB y poné `internal: true` |
| `nslookup` no resuelve | dnsmasq no está en la red o la IP no coincide | revisá `dnsmasq.conf` y la IP del contenedor |
| El stack arranca a medias | `depends_on` sin `condition` | usá `condition: service_healthy` |
| Se ve la contraseña en `docker inspect` | usaste `environment:` | pasá a `secrets:` |
| `up` no espera | falta `--wait` | `docker compose up -d --wait` |
| Perdí los datos | `down -v` | respaldá antes; usá `down` sin `-v` |
