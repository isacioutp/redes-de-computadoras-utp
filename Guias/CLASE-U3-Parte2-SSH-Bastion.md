# Clase — Unidad III · 3.3 Claves SSH y 3.4 Servidores bastión (guion docente)

> **Punto del módulo:** segunda parte de la **Unidad III**. Cubre los temas
> **3.3 (creación y administración de claves SSH)** y **3.4 (servidores bastión:
> single-homed, dual-homed, multihomed)** — semana 11 del `../Administrativo/CRONOGRAMA.md`.
>
> **Materiales que acompaña:** presentación `../Teoria/Teoria-U3-Parte2-SSH-Bastion.pptx`
> (generada por `../tools/build_parte2.py`; versión en texto en
> `../Teoria/TEORIA-U3-Parte2-SSH-Bastion.md`), laboratorio
> `../Laboratorio-11-SSH-Servidores-Bastion` (`SESION-A.md` y `SESION-B.md`) y
> `GUIA-CLASE-UNIDAD-III.md`.
>
> **Objetivo en una frase:** que el estudiante pase de «entro con usuario y
> contraseña» a **entrar con llaves y dejar la red interna detrás de un bastión**.

---

## 1. Ficha de la clase

| Campo | Valor |
|-------|-------|
| Unidad | III — Implementación de LAN y orquestación de aplicaciones |
| Temas | 3.3 Creación y administración de claves SSH · 3.4 Servidores bastión |
| Semana | 11 (dos clases) |
| Laboratorio | N.º 11 — Clase 1: 11A (llaves SSH) · Clase 2: 11B (bastión en producción) |
| Duración | Teoría 55 min + 2 sesiones prácticas (≈2 h 45 min cada una) |
| Entregable del lab | 100 pts (Sesión A 50 + Sesión B 50) |
| Insumo para el proyecto | **Avance N.º 2** (SSH sin contraseña + bastión dual-homed) |

### Objetivos de aprendizaje

Al terminar el punto, el estudiante debe poder:

1. **Explicar** por qué la autenticación por llave (pública/privada) es superior a
   la contraseña: el secreto nunca viaja ni se guarda en el servidor.
2. **Generar** un par `ed25519` con `ssh-keygen`, aplicar los **permisos**
   correctos (`600` / `700`) y conectarse **sin contraseña**.
3. **Demostrar** el rechazo de una llave no autorizada (`Permission denied
   (publickey)`) y explicar por qué ocurre.
4. **Clasificar** un bastión como **single-homed, dual-homed o multihomed** según
   sus interfaces, y justificar cuál protege de verdad la red interna.
5. **Entrar a la red interna** con `ProxyJump` (`ssh -J`) y con túneles (`ssh -L`)
   sin exponer ningún puerto interno.

### Requisitos previos (lo que ya vieron)

| Ya visto en… | Concepto que se reutiliza |
|--------------|---------------------------|
| Parte 1 (3.1) | LAN segmentada, subred de administración, router entre subredes |
| Caso 1 (ECOSISTEMA) | DNS interno, HTTP/HTTPS, puertos y servicios |
| Caso 2 | TCP/UDP, puerto publicado vs. interno, ruta ida/vuelta |

> **Regla de oro del docente:** esta clase es **seguridad de acceso**, no un curso
> de Linux. No configurar `sshd` a fondo ni repasar `iptables` completo; usar lo
> mínimo para sostener el concepto de **única puerta de entrada**.

---

## 2. Materiales y preparación previa (30 min antes)

### En el host (docente)

```bash
# Imágenes que conviene tener ya descargadas (evita perder clase esperando red)
docker pull linuxserver/openssh-server:latest
docker pull postgres:15-alpine
docker pull nginx:alpine
docker pull alpine

# Verificar Docker y limpiar restos de pruebas anteriores
docker ps
docker network prune -f
```

### En la pizarra / pantalla

- El **esquema del par de llaves** (privada en tu PC → desafío → firma → acceso) y,
  al lado, el **diagrama del bastión** (internet → bastión → red interna sin salida).
- La tabla de los **tres tipos de bastión** (sección 4) — dejarla visible durante
  el tema 3.4.

### Puntos de control (checkpoints) que se van a pedir

1. `llave_lab11.pub` mostrada en pantalla (contenido tipo–base64–comentario).
2. Acceso sin contraseña **y** rechazo de la llave no autorizada (dos capturas).
3. `db-interna` sin puerto publicado, alcanzada por túnel `ssh -L`.
4. Bastión con **dos** IP (`docker exec bastion ip addr show`).
5. `curl http://localhost:8085/api/` devolviendo el contenido del servicio interno.

---

## 3. Estructura de la clase (dos formas de dictarla)

### Opción 1 — Clase teórica (55 min) + prácticas aparte

| Bloque | Min | Qué se hace |
|--------|-----|-------------|
| Teoría 3.3 + 3.4 | 55 | Presentación `../Teoria/Teoria-U3-Parte2-SSH-Bastion.pptx` (diapositivas 1-13) |
| Sesión A | ≈120-165 | Lab 11A: llaves SSH + túnel a la DB |
| Sesión B | ≈120-165 | Lab 11B: bastión dual-homed + bastión web |

### Opción 2 — Bloque semanal (2 clases de 2 h 45 min)

| Clase | Min | Qué se hace |
|-------|-----|-------------|
| **Clase 1** | 55 + 110 | Teoría 3.3 (llaves) + **Sesión A** (acceso sin contraseña) |
| **Clase 2** | 55 + 110 | Teoría 3.4 (bastión) + **Sesión B** (bastión en producción) |

> El resto de este documento se lee **bloque por bloque**, así que sirve para
> cualquiera de las dos opciones.

---

## 4. Guion teoría — Temas 3.3 y 3.4 (55 min)

> Alineado con las **notas del presentador** del PPT (que ya traen el minuto de
> cada diapositiva). Aquí está el *cómo contarlo*, no el texto de cada diapositiva.

### Encuadre (0-5 min)

- Retomar la Parte 1: la LAN ya existe y hay un **segmento de administración**.
  La pregunta de hoy: *«¿cómo entro a esos servidores de forma segura y que quede
  registro?»*.
- Frase para abrir: *«En la Parte 1 construimos la red. Hoy aprendemos a entrar a
  ella sin contraseñas y dejando la parte interna invisible desde internet.»*
- Anunciar los entregables: llave pública funcionando, bastión dual-homed, evidencia
  del túnel o del proxy inverso.

### 3.3 · Claves SSH (5-22 min)

| Min | Diapositiva / tema | Cómo contarlo |
|-----|--------------------|---------------|
| 5-6 | Transición a 3.3 | Hilo: el problema de la contraseña → el par de llaves → `ssh-keygen` → el servidor OpenSSH. |
| 6-10 | **El problema de la contraseña** | Preguntar *«¿quién ha visto una contraseña de servidor compartida?»*. Frase que deben memorizar: **con una llave, el servidor nunca conoce el secreto**. Cerrar con que una contraseña no se rota ni se audita. |
| 10-15 | **El par de llaves (criptografía asimétrica)** | Diapositiva más conceptual: tomarla con calma. Analogía del **sello**: la pública verifica, solo tú puedes estampar la privada. Aclarar que SSH **no manda la contraseña cifrada**: manda un desafío y el cliente lo firma. Mencionar `ed25519` (default moderno) vs. `rsa`. |
| 15-20 | **`ssh-keygen` y permisos** | Si hay proyector, **generar el par en vivo** (es instantáneo). El 90 % de los «no me funciona SSH» son **permisos**; mostrar el aviso literal `UNPROTECTED PRIVATE KEY FILE`. Passphrase opcional en el lab; en producción conviene (o `ssh-agent`). |
| 20-22 | **El servidor OpenSSH y el orden de endurecimiento** | Tabla de directivas (`PubkeyAuthentication`, `PasswordAuthentication`, `PermitRootLogin`, `AllowUsers`). **Orden correcto: primero agregar la llave, después apagar contraseñas.** El error de apagarlas antes se llama **lock-out** y sale caro. |

### 3.4 · Servidores bastión (22-48 min)

| Min | Diapositiva / tema | Cómo contarlo |
|-----|--------------------|---------------|
| 22-23 | Transición a 3.4 | *«Ya entramos seguro a un servidor. ¿Y si son cinco y no quiero exponer ninguno?»* |
| 23-28 | **Qué es un bastión (y por qué existe)** | Analogía del **guardia de la entrada**: no es más fuerte que los demás, es el único que queda en la calle. Punto clave: **la red interna no tiene ruta de salida**; aunque comprometan un servidor interno, no sale a internet. |
| 28-32 | **Single-homed · dual-homed · multihomed** | Diapositiva de examen: **interfaces = clasificación** (1 = single, 2 = dual, 3+ = multi). Caja roja: la red interna se crea con `docker network create --internal`; **sin esa opción el dual-homed es decorativo**. |
| 32-40 | **Bastión web: proxy inverso y firewall** | Analogía del **mostrador**: el cliente habla con el mostrador, nunca entra al almacén. nginx hace `proxy_pass` al backend; el TLS termina en el bastión. Checklist de las **4 capas de un bastión bien hecho** (pocos puertos, llave no contraseña, firewall default DROP, interna sin salida). |
| 40-48 | **`ProxyJump` y túneles SSH** | Parte más práctica. Patrones que deben dominar: `ssh -J` (saltar por el bastión), `ssh -L` (tunelizar un puerto interno sin abrirlo), `ssh host` (con alias en `~/.ssh/config`). Argumento del túnel: **la DB no se publica, punto**. |

### Cierre (48-55 min)

- Repasar las **6 preguntas de autoevaluación** de la diapositiva 13 (sección 9 de
  este documento); pedir dos respuestas en voz alta.
- **Puente a la Parte 3:** ya hay red, acceso seguro y monitoreo; falta **escalar**
  el despliegue (Compose y Swarm).

---

## 5. Guion práctica — Sesión A: claves SSH y acceso sin contraseña (11A)

**Meta:** dejar el acceso por llave funcionando y **capturar los checkpoints 1-3**.
**Tiempo sugerido:** 15 min demo guiada + 60-90 min trabajo + 15 min cierre.

| Min | Etapa | Qué hace el docente / el estudiante |
|-----|-------|-------------------------------------|
| 0-10 | Pasos 1-2 en vivo | `ssh-keygen -t ed25519`, mostrar los dos archivos y aplicar `chmod 600`/`644`. |
| 10-25 | Paso 3 guiado | Levantar `ssh-srv` (linuxserver/openssh-server) con la llave pública montada en `authorized_keys`. |
| 25-45 | Pasos 4-5 | Conectar **sin contraseña**; luego crear `otra_llave` y ver el **rechazo**. |
| 45-70 | Pasos 6-7 | Levantar `db-interna` (sin puerto publicado) y abrir el **túnel `-L`**. |
| 70-90 | Evidencias y preguntas | Capturas del acceso, del rechazo y del `SELECT version()`; responder preguntas 1-6. |

### Comandos núcleo (si el estudiante se pierde, dictarlos)

```bash
mkdir -p ~/lab11 && cd ~/lab11

# 1 · Generar el par (sin passphrase, para el lab)
ssh-keygen -t ed25519 -f llave_lab11 -C "alumno@lab11" -N ""
chmod 600 llave_lab11 && chmod 644 llave_lab11.pub

# 2 · Servidor SSH con la llave pública autorizada
docker network create lab11-red
docker run -d --name ssh-srv --network lab11-red -p 2222:2222 \
  -e PASSWORD_ACCESS=false -e PUBLIC_KEY_FILE=/authorized_keys \
  -e USER_NAME=alumno -e USER_PASSWORD=labpass123 \
  -v $(pwd)/llave_lab11.pub:/authorized_keys:ro \
  linuxserver/openssh-server:latest

# 3 · Entrar SIN contraseña
ssh -i llave_lab11 -p 2222 alumno@localhost 'echo "Acceso permitido sin password"'

# 4 · Comprobar el rechazo de una llave NO autorizada
ssh-keygen -t ed25519 -f otra_llave -N ""
ssh -i otra_llave -p 2222 alumno@localhost 'echo nunca' 2>&1 | head

# 5 · DB aislada (sin puerto público) + túnel SSH -L
docker run -d --name db-interna --network lab11-red \
  -e POSTGRES_PASSWORD=labpass123 postgres:15-alpine
ssh -i llave_lab11 -N -L 5432:db-interna:5432 -p 2222 alumno@localhost &
sleep 3
docker run --rm --add-host=host.docker.internal:host-gateway \
  -e PGPASSWORD=labpass123 postgres:15-alpine \
  psql -h host.docker.internal -U postgres -c "SELECT version();"
kill %1
```

### Preguntas de la Sesión A (con la respuesta esperada)

1. ¿Cuántos archivos se generaron? ¿Qué contiene la llave pública?
   → **Dos**: `llave_lab11` (privada) y `llave_lab11.pub`; la pública es
   `tipo base64 comentario` y puede compartirse.
2. ¿Por qué la privada debe ser `600`?
   → Para que **solo el dueño** la lea; si se filtra, cualquiera entra como tú.
   SSH se niega a usarla con permisos abiertos.
3. ¿Pudiste autenticarte sin contraseña? ¿Qué papel jugó `authorized_keys`?
   → Sí; la llave **pública** en `authorized_keys` es la que autoriza al cliente
   que firma con la privada.
4. ¿Qué mensaje recibe la llave no autorizada? ¿Qué significa `Permission denied
   (publickey)`?
   → El servidor no reconoce su pública en `authorized_keys`; rechaza la firma.
5. ¿Podrías conectarte **directo** a `db-interna` por el 5432? ¿Está expuesta?
   → No: no tiene puerto publicado; solo es alcanzable dentro de `lab11-red`.
6. ¿Qué hace `-L 5432:db:5432`?
   → Crea un reenvío local: `localhost:5432` en tu máquina se tuneliza por SSH
   hasta `db:5432`, sin publicar la DB.

> **Error típico a vigilar:** permisos abiertos en la llave privada
> (`UNPROTECTED PRIVATE KEY FILE`) y confundir el **puerto del host** (`-p 2222`)
> con el puerto interno (`22`).

---

## 6. Guion práctica — Sesión B: bastión en producción (11B)

**Meta:** construir el **bastión dual-homed** y **probar los tres patrones de acceso**.
**Tiempo sugerido:** 15 min pasos 1-3 + 60 min pasos 4-7 + 15 min cierre.

| Min | Etapa | Qué demuestra |
|-----|-------|---------------|
| 0-15 | Pasos 1-3: redes + bastión dual-homed | Red privada `--internal`; bastión con **2 IP**; `app-interno` sin salida a internet. |
| 15-35 | Paso 4: `ProxyJump` | Saltar por el bastión hacia la red privada. |
| 35-60 | Paso 5: bastión web | nginx como **proxy inverso** publicando `internal-api` en `:8085` sin exponerla. |
| 60-75 | Paso 6: `iptables` deep-secure | Política `INPUT DROP` y solo los puertos del bastión. |
| 75-90 | Paso 7 + cierre | `~/.ssh/config` con `ProxyJump` automático; diagrama y preguntas. |

### Comandos núcleo

```bash
# 1 · Redes: la privada NO tiene salida a internet
docker network create red-publica --subnet 172.20.0.0/24
docker network create red-privada --subnet 172.20.1.0/24 --internal

# 2 · Bastión dual-homed (una interfaz por red)
docker run -d --name bastion -p 2200:2222 \
  -e PUBLIC_KEY_FILE=/authorized_keys -e USER_NAME=alumno \
  -v $(pwd)/llave_lab11.pub:/authorized_keys:ro \
  linuxserver/openssh-server
docker network connect red-publica bastion
docker network connect red-privada bastion
docker exec bastion ip addr show | grep inet

# 3 · Servicio interno aislado (sin salida)
docker run -d --name app-interno --network red-privada --cap-add=NET_ADMIN \
  alpine sleep 3600
docker exec app-interno ping -c 1 8.8.8.8   # debe FALLAR

# 4 · Entrar por el bastión con ProxyJump
ssh -J alumno@localhost:2200 -i llave_lab11 root@172.20.1.2

# 5 · Bastión web: proxy inverso al servicio interno (puerto 8085)
docker run -d --name bastion-web -p 8085:80 \
  -v $(pwd)/basweb/nginx.conf:/etc/nginx/nginx.conf:ro nginx:alpine
docker network connect red-privada bastion-web
curl http://localhost:8085/api/

# 6 · Endurecer el bastión (deep-secure)
docker exec bastion sh -c "apk add --no-cache iptables -q; \
  iptables -A INPUT -p tcp --dport 2222 -j ACCEPT; iptables -P INPUT DROP"
```

`~/.ssh/config` (o `ssh.config`) para el salto automático:

```text
Host bastion-lab
    HostName localhost
    Port 2200
    User alumno
    IdentityFile /home/tu-usuario/lab11/llave_lab11

Host app-interno
    HostName 172.20.1.2
    ProxyJump bastion-lab
    IdentityFile /home/tu-usuario/lab11/llave_lab11
```

### Preguntas de la Sesión B (con la respuesta esperada)

1. ¿Cuántas IP tiene el bastión y en qué red? ¿Es dual-homed por las NIC?
   → Dos (una en `172.20.0.0/24` y otra en `172.20.1.0/24`); sí, dual-homed = 2
   interfaces, una por red.
2. ¿La red `--internal` da internet? ¿Qué capa lo corta?
   → No; `ping 8.8.8.8` falla porque no hay ruta/NAT de salida.
3. Diagrama de la ruta `TuPC → [bastión:2200] → app-interno`.
   → El interno **no** está expuesto; se llega en dos saltos por el bastión.
4. ¿Qué servicio está expuesto y cuál no? ¿Qué rol juega nginx?
   → Expuesto: `bastion-web` (`:8085`). Interno: `internal-api`. nginx es **proxy
   inverso**: el cliente nunca ve la IP real del backend.
5. ¿Qué política de firewall aplicaste? ¿Por qué *deep-secure*?
   → `INPUT DROP` con solo `2222`/`443` permitidos: por defecto se bloquea todo y
   se abre lo mínimo.
6. ¿Qué ventaja da `~/.ssh/config` para un equipo?
   → Centraliza host, puerto, usuario y llave; facilita rotación de llaves y SSO
   (equivalente a AWS Session Manager, Azure Bastion).

> **Error típico a vigilar:** crear la red privada **sin `--internal`** (el
> dual-homed queda decorativo) y ordenar mal `iptables` (un `DROP` antes del
> `ACCEPT` del puerto corta la propia sesión SSH).

---

## 7. Autoevaluación / salida de clase

Preguntas que el estudiante debe poder responder **antes de irse**:

1. Explica en una frase por qué la llave **pública** puede ir en el servidor y la
   **privada** no.
2. ¿Qué permisos deben tener `~/.ssh/` y `authorized_keys`, y qué pasa si no?
3. Diferencia un bastión **single-homed** de uno **dual-homed** con un ejemplo.
4. ¿Por qué la red interna se crea con `--internal` y qué pasaría sin eso?
5. ¿Cómo accedes a la base de datos **sin publicar** su puerto? Nombra el comando.
6. Si endureces un bastión, ¿qué va primero y por qué?

**Respuestas guía:** (1) la pública solo verifica firmas, la privada firma y nunca
sale de tu equipo; (2) `700` y `600`; SSH rechaza llaves con permisos abiertos;
(3) single = 1 interfaz, una sola red; dual = 2 interfaces (pública + interna),
como el bastión del lab; (4) `--internal` quita la salida a internet; sin eso el
interno podría salir y el aislamiento es falso; (5) `ssh -L` (túnel); (6) primero
agregar la llave y **después** apagar contraseñas, para no quedar fuera (lock-out).

---

## 8. Errores frecuentes y cómo resolverlos en clase

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| `UNPROTECTED PRIVATE KEY FILE` | Permisos abiertos en la llave privada | `chmod 600 ~/lab11/llave_lab11` |
| `Permission denied (publickey)` | La pública no está en `authorized_keys` | Montar/copiar `llave_lab11.pub` y revisar el `-v` del contenedor |
| Sigo pidiendo contraseña | `PASSWORD_ACCESS=false` pero la llave no llegó | Verificar el bind mount de `authorized_keys` dentro del contenedor |
| Lock-out del servidor | Apagué contraseñas antes de autorizar la llave | Recrear con `PASSWORD_ACCESS=true`, autorizar la llave y reintentar |
| El interno sí sale a internet | La red se creó sin `--internal` | Recrear: `docker network create red-privada --internal` |
| `ProxyJump` no conecta | Puerto/usuario/llave mal en `~/.ssh/config` | Revisar `Port 2200` y `IdentityFile`; probar primero `ssh -J` directo |
| `curl :8085/api/` da 502 | `bastion-web` no está en `red-privada` | `docker network connect red-privada bastion-web` |
| La sesión SSH se cae tras `iptables` | `DROP` por defecto antes de permitir el puerto | Permitir `--dport 2222` **antes** de `-P INPUT DROP` |

---

## 9. Conexión con el resto del curso

- **Hacia atrás (lo que ya saben):** la Parte 1 dejó la LAN segmentada y un
  segmento de administración; los Casos 1-3 dieron DNS, TCP/UDP y puertos.
- **Hacia adelante (Parte 3):** con el acceso resuelto, falta **escalar** el
  despliegue; las llaves y los secretos se vuelven clave de operación (3.5).
- **Hacia el proyecto:** esto es el **Avance N.º 2**. La rúbrica pide **SSH sin
  contraseña** (captura) y **bastión dual/multi-homed** que aísle de verdad la red
  interna. El bastión es, además, el punto donde el **manual de despliegue** del
  Proyecto Final explica «cómo se conecta».

---

## 10. Checklist rápido antes de salir del aula

- [ ] Par `ed25519` generado y protegido (`600` / `644`).
- [ ] Acceso **sin contraseña** con la llave autorizada (captura).
- [ ] Rechazo de la llave no autorizada (captura).
- [ ] `db-interna` aislada + túnel `ssh -L` funcionando (`SELECT version()`).
- [ ] Bastión **dual-homed** con dos IP en dos redes.
- [ ] Red privada `--internal` verificada (`ping 8.8.8.8` falla).
- [ ] Bastión web (proxy inverso) sirviendo `/api/` en `:8085`.
- [ ] `iptables` con `INPUT DROP` y solo los puertos del bastión permitidos.
- [ ] `~/.ssh/config` con `ProxyJump` probado.
- [ ] Respuestas a las preguntas de Sesión A (1-6) y Sesión B (1-6).

---

## 11. Limpieza (recordar al cierre)

```bash
docker rm -f ssh-srv db-interna app-interno bastion bastion-web internal-api
docker network rm lab11-red red-publica red-privada 2>/dev/null
```

---

**Referencias**

- `../Teoria/Teoria-U3-Parte2-SSH-Bastion.pptx` — presentación de la clase (Parte 2).
- `../Teoria/TEORIA-U3-Parte2-SSH-Bastion.md` — versión en texto (con notas del orador).
- `GUIA-CLASE-UNIDAD-III.md` — reparto de las 3 partes y notas de uso.
- `../Laboratorio-11-SSH-Servidores-Bastion/` — prácticas (`SESION-A.md`, `SESION-B.md`).
- `Proyecto-Semestral/ENUNCIADO.md` — Avance N.º 2 (SSH + bastión).
- Kurose & Ross, *Computer Networking: A Top-Down Approach*; documentación de
  OpenSSH (`ssh-keygen`, `sshd_config`, `ProxyJump`).
- Recurso externo opcional: [Generate SSH key pair](https://devopscube.com/generate-ssh-key-pair/)
  (ver también `CLASE-U3-LAN-Monitoreo.md`, sección 12).
