# Teoría — Unidad III · Parte 2: Claves SSH y servidores bastión

> Contenido completo de [`Teoria-U3-Parte2-SSH-Bastion.pptx`](Teoria-U3-Parte2-SSH-Bastion.pptx) (13 diapositivas, 16:9).
> Volcado textual de la presentación: mismo contenido y mismo orden de
> lectura, sin depender de PowerPoint.
>
> Se regenera con:
> `python3 tools/dump_ppt_md.py Teoria-U3-Parte2-SSH-Bastion.pptx "Unidad III · Parte 2: Claves SSH y servidores bastión"`
>
> Cada diapositiva conserva sus **notas del orador** al final, en bloques
> plegables: en GitHub y en la mayoría de editores se despliegan con un clic.

## Índice

- **1.** Unidad III — Parte 2
- **2.** Qué vamos a ver en esta parte
- **3.** Claves SSH
- **4.** El problema de la contraseña
- **5.** El par de llaves: criptografía asimétrica
- **6.** ssh-keygen: generar el par en 30 segundos
- **7.** La entrada real: el servidor OpenSSH
- **8.** Servidores bastión
- **9.** Qué es un bastión (y por qué existe)
- **10.** Los tres tipos de bastión
- **11.** Bastión web: proxy inverso y deep-secure
- **12.** ProxyJump: atravesar el bastión con una línea
- **13.** Resumen y cierre de la Parte 2

---

## 1. Unidad III — Parte 2

**UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES**

Claves SSH y servidores bastión

- Tema 3.3 · Creación y administración de claves SSH
- Tema 3.4 · Servidores bastión: single-homed, dual-homed, multihomed
- Laboratorio N.º 11 · Semana 11 · 2 sesiones

<details><summary>Notas del orador</summary>

⏱ 0-3 min · Apertura de la Parte 2.

Enlace con la Parte 1: la LAN ya existe y hay un segmento de administración (10.0.3.0/28).
La pregunta de hoy: ¿cómo entro a esos servidores de forma segura y que quede registro?
Respuesta corta que se va a desarrollar: sin contraseñas, con llaves; y con un bastión de por medio.
Este es el bloque de seguridad de la unidad y el más pedido en el Proyecto Semestral.

</details>

---

## 2. Qué vamos a ver en esta parte

> Dos temas del programa: autenticación segura y control de acceso

| # | Tema del programa | Pregunta que responde | Min |
|---|---|---|---|
| 3.3 | Claves SSH (pública / privada) | ¿Cómo me autentico sin escribir ni guardar contraseñas? | 22 |
| 3.4 | Servidores bastión | ¿Cómo hago que la red interna no quede expuesta? | 23 |
| — | Cierre y repaso | Preguntas y repaso previo a la práctica del Lab 11 | 10 |

**Por qué importa (objetivo del programa)**
- El objetivo general dice: *conexiones seguras a servidores remotos*.
- El enunciado del proyecto **prohíbe** contraseñas en el código.
- Una contraseña compartida se filtra, no se rota, no se audita.

**Qué se entregan (Lab 11)**
- Llave pública funcionando: acceso **sin contraseña** (captura).
- Un bastión dual-homed protegiendo la red interna.
- Evidencia del túnel o del proxy inverso.

**El ataque que estamos evitando**
- Un atacante encuentra el puerto 22 abierto, prueba usuario/contraseña por fuerza bruta y entra. Con llaves, **aunque el puerto esté abierto, no puede autenticarse** sin tu archivo privado — que nunca sale de tu máquina.

<details><summary>Notas del orador</summary>

⏱ 3-5 min · Agenda.

No le des más de 2 min a la agenda; la Parte 2 es densa.
La caja roja es el argumento de venta: SSH por llave no es solo cómodo, es lo que hace
imposible un brute force exitoso aunque el puerto esté expuesto.
Enfoca el ataque en que el puerto 22 abierto NO es el problema:
con llaves, un atacante puede probar pares de llaves todo el día sin éxito.

</details>

---

## 3. Claves SSH

Autenticarte con criptografía en vez de con un secreto que se puede copiar

- El problema de la contraseña compartida
- Par de llaves: qué es la pública y qué es la privada
- ssh-keygen, permisos correctos y acceso sin contraseña

22 min

<details><summary>Notas del orador</summary>

⏱ 5-6 min · Transición a 3.3.

</details>

---

## 4. El problema de la contraseña

> Tres razones por las que una contraseña no sirve para administrar servidores

| Problema | Qué pasa en la práctica | Consecuencia |
|---|---|---|
| Se comparte | Varias personas usan la misma clave | Alguien se va y nadie rota nada |
| Se filtra | Phishing, listas filtradas, una máquina comprometida | Acceso del atacante |
| No se audita | El servidor solo ve «un usuario entró» | No sabes quién fue ni qué hizo |
| Se reescribe | En papel, en un chat, en un correo | Volante por la red |

**La idea que resuelve todo**
- Con una contraseña, el servidor **necesita saber el secreto**.
- Con una llave, el servidor solo necesita tu llave **pública**.
- El secreto nunca viaja ni se almacena en el servidor.

**Y además queda el rastro**
- La llave pública identifica a una persona o un sistema concreto.
- `authorized_keys` dice: «este servidor acepta a esta llave».
- Se puede revocar una llave sin cambiar la contraseña de nadie.

<details><summary>Notas del orador</summary>

⏱ 6-10 min · El problema.

Pregunta a la clase: '¿quién ha visto una contraseña de servidor compartida?' — todos.
El giro de la caja izquierda es la frase que deben memorizar: el servidor nunca conoce el secreto.
La segunda fila es la clásica: quien tiene una máquina comprometida pierde la llave.
Por eso la rotación de llaves es parte del mantenimiento, no un extra.

</details>

---

## 5. El par de llaves: criptografía asimétrica

> Tu PC firma con la privada · el servidor verifica con la pública

**Tu PC**
id_ed25519  ·  la PRIVADA
Nunca sale de aquí

**El servidor**
~/.ssh/authorized_keys  ·  la PÚBLICA
Se puede compartir sin riesgo

**1  desafío**
↓

**2  firma**
↓

**3  acceso**

**Servidor envía**
texto aleatorio

**Tu PC firma**
con la privada

**Servidor verifica**
con tu pública

|  | Llave pública | Llave privada |
|---|---|---|
| Dónde vive | En el servidor (authorized_keys) | Solo en tu PC |
| ¿Se comparte? | Sí, sin problema | Nunca, con nadie |
| ¿Para qué sirve? | Verificar firmas | Firmar (crear el desafío) |
| Tamaño típico | ed25519: 32 bytes de clave | 32 bytes + cadena privada |

<details><summary>Notas del orador</summary>

⏱ 10-15 min · Criptografía.

Es la diapositiva más conceptual de la parte; tómate el tiempo.
Analogía que funciona: la firma es como un sello. El sello (pública) lo puede verificar
cualquiera, pero solo tú puedes estamparlo (privada).
Aclare que SSH no 'manda la contraseña cifrada': manda un desafío y el cliente lo firma.
Mencione ed25519 vs rsa: ed25519 es el default moderno y más rápido; rsa sigue aceptándose.
Si alguien pregunta por la clave del servidor: no la tiene, solo verifica firmas.

</details>

---

## 6. ssh-keygen: generar el par en 30 segundos

> Un comando en tu máquina, un comando en el servidor — y la contraseña deja de existir

**1 · En tu PC — generar el par**

```text
$ ssh-keygen -t ed25519 -C "equipo@mi-pc"
Generating public/private ed25519 key pair.
Enter file in which to save the key:
Enter passphrase (empty for no passphrase):
$ ls -l ~/.ssh/
id_ed25519       ← la privada (permisos 600)
id_ed25519.pub   ← la pública (permisos 644)
```

**3 · Probar: ya no pide contraseña**
**$ ssh usuario@10.0.3.10**
- Si no pide nada y entras, la llave quedó bien autorizada.
- La clave del éxito son los **permisos**: SSH se niega a leer un archivo abierto.

**2 · En el servidor — autorizar la llave**

```text
$ ssh-copy-id usuario@10.0.3.10
# copia id_ed25519.pub a ~/.ssh/authorized_keys
# o a mano, desde tu contenedor:
mkdir -p ~/.ssh && chmod 700 ~/.ssh
cat id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**Permisos que SSH exige (si los cambias, falla)**
- **`~/.ssh/`** → **700**
- **`authorized_keys`** → **600**
- **`id_ed25519`** → **600**
- SSH avisa «UNPROTECTED PRIVATE KEY FILE» si el permiso está abierto.

<details><summary>Notas del orador</summary>

⏱ 15-20 min · ssh-keygen.

Si hay tiempo, GENERAR EL PAR EN VIVO con el proyector. Es instantáneo y lo entienden rápido.
El detalle que más cuesta: los permisos. El 90 % de los «no me funciona SSH» son permisos.
Muestra el aviso literal de OpenSSH: 'UNPROTECTED PRIVATE KEY FILE' — se les queda grabado.
El passphrase es opcional; en el laboratorio se deja vacío para simplificar, pero
menciona que en producción conviene ponerlo (o usar ssh-agent).
Insiste en el aviso literal de permisos; es el error más común del laboratorio.

</details>

---

## 7. La entrada real: el servidor OpenSSH

> Dónde vive el servicio y cómo decide a quién acepta

| Directiva sshd_config | Qué controla | Valor seguro |
|---|---|---|
| PubkeyAuthentication | Aceptar autenticación por llave | yes |
| PasswordAuthentication | Permitir entrar con contraseña | no (con llave lista) |
| PermitRootLogin | Entrar como root directo | no |
| AllowUsers | Quiénes pueden entrar | lista explícita |

```text
# contenedor con el servidor SSH
docker run -d --name ssh-srv --network interna \
-p 2222:22 \
-v ~/.ssh:/root/.ssh:ro alpine \
sh -c 'apk add --no-cache openssh && \
ssh-keygen -A && sshd -D'
$ docker exec ssh-srv sshd -T | grep -i
'pubkeyauthentication'
→ pubkeyauthentication yes
```

**La demostración del Lab 11 (obligatoria)**
- 1 · Entra con la llave autorizada → acceso concedido.
- 2 · Entra con una llave **no** autorizada → «Permission denied».
- Las dos capturas son el entregable de la sesión A.

**Orden correcto de endurecimiento**
- Primero agrega la llave. **Después** apaga contraseñas.
- Si apagas contraseñas antes de tener llave, te quedas fuera.
- Este error se llama lock-out y es el más caro del tema.

<details><summary>Notas del orador</summary>

⏱ 20-22 min · OpenSSH.

No te metas a configurar sshd a fondo: es tema de la Unidad 3.3, no un curso de Linux.
Lo importante: la tabla de directivas y el ORDEN (agregar llave → luego apagar contraseña).
La advertencia de lock-out merece una anécdota: es el error que más caro sale en la vida real.
Este es el bloque de seguridad: acá se ve la diferencia entre 'funciona' y 'es seguro'.

</details>

---

## 8. Servidores bastión

El único punto de entrada a una red que no debe exponerse

- Qué es un bastión y por qué la red interna se esconde detrás
- Single-homed · dual-homed · multihomed
- Bastión web: proxy inverso y reglas de firewall

23 min

<details><summary>Notas del orador</summary>

⏱ 22-23 min · Transición a 3.4.

</details>

---

## 9. Qué es un bastión (y por qué existe)

> Un host que se expone para que los demás no tengan que hacerlo

**Sin bastión:** cada servidor interno publica su propio puerto hacia internet. Con 5 servicios, 5 puertas abiertas.
**Con bastión:** solo el bastión tiene salida a internet. Todo lo demás vive en una red interna sin ruta de vuelta.

**❌ Sin bastión**
**INTERNET**
↓ 22   ↓ 8080   ↓ 5432   ↓ 443   ↓ 80
app  web  db  mail  proxy
5 superficies de ataque

**✓ Con bastión**
**INTERNET**
↓ 22   ↓ 443
┌──────────┐
│ BASTIÓN  │  ← única puerta
└────┬─────┘   red interna sin NAT

| Característica | Qué significa | Consecuencia práctica |
|---|---|---|
| Es el único expuesto | Solo él tiene interfaz pública | Internet ve 1 host, no 5 |
| Está endurecido (hardened) | Mínimo software, sin extras | Menos superficie de ataque |
| Todo pasa por él | SSH, proxy web, túnel | Auditoría: hay un solo punto de control |
| La red interna no tiene salida | Sin ruta por defecto a internet | Aunque lo comprometan, no sale |

<details><summary>Notas del orador</summary>

⏱ 23-28 min · Qué es un bastión.

La analogía: es el guardia de la entrada. No es que sea más fuerte que los demás,
es que es el único que queda en la calle.
El punto clave de la última fila: la red interna SIN RUTA DE SALIDA. Aunque alguien
entre a un servidor interno, no puede salir a internet. Eso es aislamiento real.
Si preguntan por qué el bastión no reenvía tráfico, revisar la siguiente diapositiva.

</details>

---

## 10. Los tres tipos de bastión

> La diferencia es cuántas interfaces tiene: de ahí sale toda la clasificación

| Tipo | Interfaces | Función | Ejemplo en el Lab 11 |
|---|---|---|---|
| Single-homed | 1 | Acceso a una sola red, sin reenviar tráfico | bastión simple + túnel -L |
| Dual-homed | 2 (pública + interna) | Puente entre pública e interna, sin reenvío | bastión + red --internal |
| Multihomed | 3 o más | Gateway con varios caminos: web, proxy, VPN | bastión web + proxy inverso |

**Dual-homed: el punto dulce**
- Una interfaz en la red pública (recibe las conexiones).
- Una en la red interna (habla con los servidores).
- **No** reenvía tráfico: es puente de acceso, no router.

**El detalle que hace la seguridad**
- La red interna se crea con `docker network create --internal`.
- Esa opción quita la puerta de salida por defecto.
- Sin esa opción, el dual-homed es solo decorativo.

**El enunciado del proyecto pide dual-homed mínimo**
- Avance N.º 2: «Servidor bastión: mínimo dual-homed (o multi) protegiendo la red interna; la aplicación interna NO tiene exposición directa.»

<details><summary>Notas del orador</summary>

⏱ 28-32 min · Tipos de bastión.

Diapositiva de examen: la pregunta clásica es '¿qué tipo es este y por qué?'.
Regla: interfaces = clasificación. Si tiene 1 = single, 2 = dual, 3+ = multi.
El detalle de `--internal` en la caja roja es lo que hace la diferencia entre un trabajo
real y uno de adorno. Si lo dicen, el proyecto está bien hecho.
Aclara que 'sin reenviar' no significa 'inútil': reenviar sería convertirlo en router.

</details>

---

## 11. Bastión web: proxy inverso y deep-secure

> El bastión también sirve sitios, no solo SSH

**Proxy inverso con nginx (el patrón del proyecto)**

| Capa | Control | Herramienta |
|---|---|---|
| Qué puerto se publica | Solo SSH + HTTPS del bastión | `-p 2222:22` |
| Quién entra | Solo llaves autorizadas | `authorized_keys` |
| Qué se alcanza | Solo lo que el bastión publica | proxy inverso |
| Qué sale a internet | Solo el bastión | red interna `--internal` |

```text
server {
listen 443 ssl;
server_name app.feria.local;
# el bastion responde, el backend no
location / {
proxy_pass http://app-srv:5000;
}
}
```

**Qué aporta el proxy inverso**
- El cliente nunca ve la IP real del backend.
- El bastión termina el TLS: los internos hablan HTTP plano.
- Un solo puerto público para varios servicios.

**Las 4 capas de un bastión «bien hecho»**
1. **Pocos puertos publicados**
2. **Autenticación por llave, no contraseña**
3. **Firewall con default DROP**
4. **Red interna sin salida a internet**
- Si falta una, la red sigue expuesta por ese lado.

**Reglas de firewall (iptables) — deep-secure**

```text
# por defecto, bloquea todo
iptables -P INPUT DROP
# y deja entrar solo SSH y HTTPS
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

<details><summary>Notas del orador</summary>

⏱ 32-40 min · Bastión web.

Explica el proxy inverso con la analogía del mostrador: el cliente habla con el mostrador,
nunca entra al almacén. El almacén es la red interna.
El TLS termina en el bastión: los internos no necesitan certificado.
Las 4 capas de la derecha son el checklist del docente. Es lo que revisa la rúbrica.
El TLS terminando en el bastión es una decisión real de arquitectura, no un detalle.

</details>

---

## 12. ProxyJump: atravesar el bastión con una línea

> El usuario entra al bastión y desde ahí salta a la red interna

**El problema:** la red interna no tiene ruta a internet, así que no puedes alcanzarla directamente. ProxyJump te deja entrar en dos saltos usando el bastión de trampolín.

**Túneles SSH: llegar a la DB sin abrirla**

```text
# -L tunnel: la DB no se publica nunca
$ ssh -L 5433:db-srv:5432 bastion
# ahora postgres está en localhost:5433
$ psql -h localhost -p 5433 -U admin
```

```text
# en una sola línea, saltando por el bastión
$ ssh -J usuario@bastion app-srv
# o declarándolo en ~/.ssh/config (mejor)
Host app-srv
HostName 10.0.1.10
ProxyJump usuario@bastion
User usuario
```

**Por qué el túnel es la respuesta**
- La DB **no** tiene puerto publicado: no existe en internet.
- El túnel existe solo mientras dura la sesión SSH.
- Se cierra la terminal, se cierra el acceso.

**Con ~/.ssh/config**
- Un alias por servidor: `ssh app-srv` y listo.
- El puerto y el usuario se documentan en el archivo.
- El manual de despliegue del proyecto lo puede citar.

**Los tres patrones de acceso que deben dominar**
- **`ssh -J`** / ProxyJump → entrar a la red interna saltando por el bastión.   **`ssh -L`** → tunelizar un puerto interno sin abrirlo.   **`ssh host`** → con alias en ~/.ssh/config, sin repetir nada.

<details><summary>Notas del orador</summary>

⏱ 40-48 min · ProxyJump y túneles.

Esta es la parte más práctica de la sesión. Si hay tiempo, en vivo:
  ssh -L contra la DB del lab y un psql que se conecte.
El argumento del túnel es el que cierra el proyecto: la DB no se publica, punto.
ProxyJump es lo que hace usable la red interna sin abrirla.
El túnel es la respuesta al requisito del proyecto: la DB no se publica nunca.

</details>

---

## 13. Resumen y cierre de la Parte 2

> Qué debe quedar en la cabeza antes de ir al Lab 11

**Ideas clave (3.3 + 3.4)**
- La llave **pública** autoriza; la **privada** firma y no sale.
- El servidor nunca almacena el secreto.
- SSH se niega a leer llaves con permisos abiertos: 600 / 700.
- Bastión = única puerta; la red interna sin salida.

**Puente hacia la Parte 3**
- Ya tenemos la red, el acceso seguro y el monitoreo.
- Falta **escalar**: un contenedor, o muchos copias de uno.
- Parte 3: orquestación con Compose y Swarm (3.5).
- Ahí las llaves y los secretos se vuelven clave de despliegue.

**Preguntas de autoevaluación (sal de clase sabiendo responderlas)**
1. Explica en una frase por qué la llave pública puede ir en el servidor y la privada no.
2. ¿Qué permisos deben tener `~/.ssh/` y `authorized_keys`, y qué pasa si no?
3. Diferencia un bastión single-homed de uno dual-homed con un ejemplo.
4. ¿Por qué la red interna se crea con `--internal` y qué pasaría sin eso?
5. ¿Cómo accedes a la base de datos sin publicar su puerto? Nombra el comando.
6. Si endureces un bastión, ¿qué va primero y por qué?

<details><summary>Notas del orador</summary>

⏱ 48-55 min · Cierre de la Parte 2.

La pregunta 6 es la que más discrimina: agregar llave → luego apagar contraseña.
La 5 es la del proyecto: ssh -L.
Deja 5 min y pide dos respuestas en voz alta antes de pasar a la Parte 3.
Si la respuesta es 'primero apago las contraseñas', la pregunta no se entendió:
eso es justamente el error de lock-out de la diapositiva 12.

</details>

---

