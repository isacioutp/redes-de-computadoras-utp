# Laboratorio N.° 11 — Claves SSH y Servidores Bastión

Semana 13 · Unidad III · 2 clases

- **Clase 1:** Claves SSH y acceso sin contraseña → [Sesión A](SESION-A.md)
- **Clase 2:** Servidores bastión en producción → [Sesión B](SESION-B.md)

## Objetivo general

Aprender a **generar y administrar llaves SSH** (pública/privada) para
autenticación sin contraseña en servidores, y diseñar **servidores tipo
bastión** (single-homed, dual-homed, multihomed) para proteger un entorno de
desarrollo usando exclusivamente contenedores Docker.

## Contexto teórico

### Claves SSH

- **Llave pública**: lo que pones en el servidor (`~/.ssh/authorized_keys`) —
  no es secreta.
- **Llave privada**: la guardas SOLO tú en tu máquina (`id_ed25519`) — nunca
  se comparte.
- `ssh-keygen` genera el par. SSH autentica porque puedes firmar datos con tu
  llave privada y el servidor lo verifica con la pública.

```
Tu PC (llave privada) ──[desafío cifrado]──> Servidor (llave pública)
        ◄──────────────[firma correcta]──────  acceso concedido
```

### Servidor bastión

Es el **único** punto de entrada a una red privada. Al ser "blindado"
(endurecido), el resto de servidores internos no se exponen a internet.

| Tipo | Conexiones de red | Uso |
|------|-------------------|-----|
| Single-homed | 1 interfaz | Acceso a una sola red |
| Dual-homed | 2 interfaces | Puente entre red pública e interna (sin reenvío) |
| Multihomed | 3+ interfaces / múltiples servicios | Gateway con varios caminos (web, proxy, VPN) |

## Materiales

- Docker Engine.
- Cliente SSH en el host (`ssh`, `ssh-keygen`). En Windows: OpenSSH incluido o
  Git Bash.

## Cómo se trabaja esta semana

| Sesión | Qué haces | Entregable breve | Guía |
|--------|-----------|------------------|------|
| **Sesión A — Claves SSH y acceso sin contraseña** | Generación de llaves `ed25519`, permisos `chmod` (Parte 1), servidor OpenSSH con autenticación por llave y rechazo de llave no autorizada (Parte 2), bastión single-homed y túnel SSH `-L` a la DB (Parte 3). Preguntas 1–6. | Llave pública, capturas de acceso exitoso y de rechazo, túnel a la DB funcionando. | [Sesión A](SESION-A.md) |
| **Sesión B — Servidores bastión en producción** | Bastión dual-homed con red `--internal` y ProxyJump (Parte 4), bastión web con nginx proxy inverso y iptables deep-secure (Parte 5), flujo completo y `~/.ssh/config` (Parte 6). Preguntas del original 7–12 (renumeradas 1–6). | Diagrama dual-homed, evidencia del proxy 8085, `ssh.config` usado y preguntas. | [Sesión B](SESION-B.md) |

## Rúbrica global

100 puntos (Sesión A 50 + Sesión B 50).

| Sesión | Criterio | Puntos |
|--------|----------|--------|
| A | Llaves ed25519 generadas y protegidas (`chmod`) | 10 |
| A | Autenticación sin contraseña + rechazo de llave no autorizada | 15 |
| A | Bastión single-homed + túnel SSH `-L` a la DB | 15 |
| A | Preguntas 1–6 | 10 |
| B | Bastión dual-homed + red `--internal` | 10 |
| B | ProxyJump + diagrama de ruta | 10 |
| B | Bastión web (proxy inverso) + deep-secure iptables | 15 |
| B | `~/.ssh/config` + flujo completo | 10 |
| B | Preguntas 7–12 (renumeradas 1–6) | 5 |
| | **Total** | **100** |

## Limpieza

Al terminar la semana, elimina los recursos:

```bash
docker rm -f ssh-srv db-interna app-interno bastion bastion-web internal-api
docker network rm lab11-red red-publica red-privada 2>/dev/null
```