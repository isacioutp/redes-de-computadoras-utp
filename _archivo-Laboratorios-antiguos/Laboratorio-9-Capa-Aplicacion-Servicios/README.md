# Laboratorio N.° 9 — Servicios de la Capa de Aplicación

Semana 9 · Unidad II · 2 clases
**Protocolos: HTTP, FTP, DNS, SMTP/POP3/IMAP y SNMP.**

**Sesión A:** HTTP, HTTPS y DNS (con curl y dig)
**Sesión B:** Correo (SMTP), FTP y SNMP (monitoreo)

## Objetivo general

Levantar los servidores de aplicación más usados (web, archivos, DNS, correo y
monitoreo) con Docker, y consumirlos con herramientas de cliente (curl, dig,
ftp, telnet, snmpwalk) para comprender cómo funciona cada protocolo de la capa
de aplicación. Este laboratorio materializa todos los protocolos vistos en la
Unidad II en servicios que los estudiantes usarán en su carrera de desarrollo.

## Contexto teórico

| Protocolo | Puerto | Para qué sirve | Cliente típico |
|-----------|--------|----------------|----------------|
| HTTP | 80 | Navegación web, APIs | Browser, curl |
| HTTPS | 443 | Web cifrada (TLS) | Browser, curl |
| FTP | 20/21 | Transferencia de archivos | FileZilla, ftp |
| SMTP | 25 | Enviar correo | Mail client, telnet |
| POP3 | 110 | Recibir correo (descarga) | Mail client |
| IMAP | 143 | Leer correo (servidor) | Mail client |
| DNS | 53 | Traducir nombre → IP | dig, nslookup |
| SNMP | 161 | Monitoreo de dispositivos | snmpwalk, Zabbix |

La capa de **aplicación** (TCP/IP) agrupa las capas 5, 6 y 7 del modelo OSI:
formato, cifrado/compresión y la lógica del servicio que el usuario toca.

## Materiales

- Docker instalado.
- Cliente Wireshark o tcpdump (opcional, para ver la conversación completa).
- Navegador para los puertos de servicios web.

---

## Cómo se trabaja esta semana

| Sesión | Qué harás | Entregable |
|--------|-----------|------------|
| **Sesión A — HTTP, HTTPS y DNS (con curl y dig)** | Levantarás servidores web (nginx y Apache), consumirás HTTP con `curl -v`, verás los códigos de estado, crearás un certificado con `openssl` para HTTPS, y montarás tu propio servidor DNS (dnsmasq) consultado con `dig`. | Capturas de `curl -v`, de códigos de estado, de `curl -k` y de `dig`, más respuestas a 8 preguntas. — [Sesión A](SESION-A.md) |
| **Sesión B — Correo (SMTP), FTP y SNMP (monitoreo)** | Enviarás correo hablando SMTP en texto plano con `nc`, transferirás archivos por FTP con `curl`, leerás variables de un agente SNMP con `snmpwalk` y reunirás todos los servicios en una tabla de puertos con capturas de tráfico. | Tabla de servicios/puertos, capturas de `nc`, FTP y `snmpwalk`, más respuestas a 7 preguntas. — [Sesión B](SESION-B.md) |

## Rúbrica global

| Sesión | Puntos |
|--------|--------|
| Sesión A — HTTP, HTTPS y DNS (con curl y dig) | 50 |
| Sesión B — Correo (SMTP), FTP y SNMP (monitoreo) | 50 |
| **Total** | **100** |

## Para cerrar la semana

Aplicación al desarrollo de software (reflexión opcional, 200 palabras):

1. ¿Qué servicios de la capa de aplicación usarías desplegados en tu
   arquitectura (web, API, DNS, base de datos, correo, monitoreo)?
2. ¿Cuáles de estos puertos expondrías públicamente y cuáles mantendrías
   internos en la red Docker?
3. ¿Cómo asegurarías cada protocolo (HTTPS, SMTPS, SFTP, DNS-over-HTTPS)?

Preguntas de verificación global (autoevaluación):

1. ¿Qué diferencia fundamental existe entre la capa de transporte y la de
   aplicación según lo visto en los Labs N.º 8 y 9?
2. HTTP en los puertos 80/443, FTP 20/21, SMTP 25, DNS 53, SNMP 161 —
   ¿cuáles usan TCP, cuáles UDP y cuáles ambos?
3. ¿Por qué DNS puede usar UDP pero SNMP también? ¿Qué gana con UDP?
4. La aplicación de tu proyecto necesita subir archivos. ¿Usarías FTP puro o
   variantes seguras? ¿Por qué?
5. ¿Qué OID usarías para conocer la cantidad de paquetes UDP recibidos en un
   switch monitoreado por SNMP?

## Limpieza

```bash
# Eliminar todos los contenedores de la semana y la red
docker rm -f web-server apache-server https-server dns-server mail-server ftp-server snmp-agent api-service
docker network rm lab9-red

# Opcional: eliminar los archivos generados en el host
rm -f server.crt privkey.pem nginx-ssl.conf descargado.txt
rm -rf html ftp-home
```