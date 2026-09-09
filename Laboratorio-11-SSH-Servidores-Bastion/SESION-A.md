# Laboratorio N.° 11 — Claves SSH y Servidores Bastión · Sesión A: Claves SSH y acceso sin contraseña

Semana 13 · Clase 1

Cubre las **Partes 1, 2 y 3** del laboratorio original: generación de llaves
`ed25519`, servidor SSH en un contenedor, autenticación sin contraseña, rechazo
de llave no autorizada y el primer bastión *single-homed* con túnel SSH a la
base de datos.

## Objetivo de la sesión

Generar tu par de llaves SSH, conectarte a un servidor sin escribir contraseña
y comprobar cómo SSH rechaza una llave no autorizada. Luego aíslas una base de
datos en una red privada y la alcanzas desde tu host mediante un túnel SSH
(`-L`), igual que un bastión single-homed real.

## Pasos

### Paso 1: Genera el par de llaves

Crea la carpeta de trabajo y genera el par `ed25519`:

```bash
mkdir -p ~/lab11 && cd ~/lab11

# Generar par ed25519 (más seguro y rápido que RSA)
ssh-keygen -t ed25519 -f llave_lab11 -C "alumno@lab11" -N ""
```

Mira los dos archivos creados:

```bash
ls -la llave_lab11*   # llave_lab11 (privada) y llave_lab11.pub (pública)
cat llave_lab11.pub
```

### Paso 2: Protege la llave privada

Aplica los permisos correctos:

```bash
chmod 600 llave_lab11          # SOLO el dueño lee/escribe
chmod 644 llave_lab11.pub      # pública puede leerse
```

### Paso 3: Levanta un servidor SSH en un contenedor

Crea la red de laboratorio y despliega el servidor OpenSSH:

```bash
docker network create lab11-red

docker run -d --name ssh-srv \
  --network lab11-red \
  -p 2222:2222 \
  -e PASSWORD_ACCESS=false \
  -e PUBLIC_KEY_FILE=/authorized_keys \
  -e USER_NAME=alumno \
  -e USER_PASSWORD=labpass123 \
  -v $(pwd)/llave_lab11.pub:/authorized_keys:ro \
  -e DOCKER_MODS=linuxserver/mods:openssh-mod-ssh-key-pair `#opcional` \
  linuxserver/openssh-server:latest

docker logs ssh-srv 2>&1 | grep -i "ssh host key" | head
```

*(Si el usuario `alumno` ya tiene llave pública: `-e PI_USER=alumno`.)*

### Paso 4: Conéctate con la llave (sin contraseña)

Desde la carpeta de la llave privada, entra al servidor sin digitar
contraseña:

```bash
# Viajar a la caña de la llave privada
ssh -i llave_lab11 -p 2222 alumno@localhost 'echo "Acceso permitido sin password"'
ssh -i llave_lab11 -p 2222 alumno@localhost 'hostname; ip addr show | grep 10.0'
```

> **Checkpoint:** si ves `Acceso permitido sin password`, tu llave pública ya
> está autorizada en el servidor. Captura esa salida.

### Paso 5: Comprueba el rechazo de la llave no autorizada

Crea OTRA llave y observa cómo el servidor la rechaza:

```bash
# Crear OTRA llave (no autorizada)
ssh-keygen -t ed25519 -f otra_llave -N ""
# Intentar conectar con la llave no autorizada
ssh -i otra_llave -p 2222 alumno@localhost 'echo nunca' 2>&1 | head
```

### Paso 6: Aísla la base de datos (bastión single-homed)

Levanta la DB solo en la red interna (sin puerto público):

```bash
# DB en red aislada (solo interna)
docker run -d --name db-interna \
  --network lab11-red \
  -e POSTGRES_PASSWORD=labpass123 postgres:15-alpine
```

### Paso 7: Abre un túnel SSH hacia la DB

Como no hay puerto público, usa el bastión/SSH para hacer *forwarding*:

```bash
# Desde el host, con la llave: crea un túnel 5432 local → db-interna:5432
ssh -i llave_lab11 -N -L 5432:db-interna:5432 -p 2222 alumno@localhost &
sleep 3

# Ahora tu host "cree" que localhost:5432 es la DB
docker run --rm --add-host=host.docker.internal:host-gateway \
  -e PGPASSWORD=labpass123 postgres:15-alpine \
  psql -h host.docker.internal -U postgres -c "SELECT version();"

kill %1
```

> **Checkpoint:** si `SELECT version();` responde la versión de postgres, el
> túnel funciona y la DB está siendo usada sin exponer su puerto. Captúralo.

## Preguntas de la sesión

1. ¿Cuántos archivos se generaron? ¿Qué extensión tiene la llave pública? ¿Qué
   contiene ese archivo (tipo, base64, comentario)?
2. ¿Por qué la llave privada debe tener permisos `600`? ¿Qué pasaría si se
   filtra?
3. ¿Pudiste autenticarte sin escribir la contraseña? ¿Qué papel jugó la llave
   pública (`authorized_keys`) del servidor?
4. ¿Qué mensaje de rechazo recibe la llave no autorizada? ¿Por qué SSH la
   rechaza a pesar de que "existe" la llave? ¿Qué significa `Permission denied
   (publickey)`?
5. Desde tu host, ¿podrías conectarte a la DB `postgres:15` de `db-interna`
   directamente (`puerto 5432`)? ¿Está expuesta al público?
6. ¿Qué hace la opción `-L 5432:db:5432` del túnel SSH? ¿Por qué el DB nunca
   se expone directamente pero podemos usarlo?

## Entregable de la sesión

1. Evidencia de la generación de llaves: contenido de `llave_lab11.pub`.
2. Captura del acceso sin contraseña (Paso 4).
3. Captura del rechazo con la llave no autorizada (Paso 5).
4. Captura del túnel SSH a la DB funcionando (`SELECT version()`).
5. Respuestas a las preguntas 1–6.

## Rúbrica de la sesión (50 puntos)

| Criterio | Puntos |
|----------|--------|
| Llaves ed25519 generadas y protegidas (`chmod 600`/`644`) | 10 |
| Acceso sin contraseña con la llave autorizada + rechazo de la no autorizada | 15 |
| Bastión single-homed + túnel SSH `-L` a la DB funcionando | 15 |
| Preguntas 1–6 respondidas | 10 |
| **Total** | **50** |