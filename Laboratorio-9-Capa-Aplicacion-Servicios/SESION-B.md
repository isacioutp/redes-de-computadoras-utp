# Laboratorio N.° 9 — Servicios de la Capa de Aplicación · Sesión B: Correo (SMTP), FTP y SNMP (monitoreo)

Semana 11 · Clase 2

Cubre las **Partes 4, 5, 6 y 7** del laboratorio original: SMTP/POP3/IMAP con
MailHog y la conversación SMTP hablada con `nc`, FTP con vsftpd y `curl`,
SNMP con `snmpd` + `snmpwalk`, y la puesta en conjunto (tabla de
servicios/puertos y capturas de DNS y SMTP).

## Objetivo de la sesión

Vas a enviar un correo hablando el protocolo SMTP en texto plano con `nc`, a
ver tu propio correo aparecer en la web de MailHog, a subir y bajar archivos
por FTP con `curl`, a leer variables de un agente de monitoreo SNMP con
`snmpwalk`, y a reunir todos los servicios de la semana en una tabla de
puertos con capturas de tráfico en vivo.

---

## Paso 1. Levanta el servidor de correo de pruebas (MailHog)

```bash
# MailHog: SMTP 1025, UI web 8025
docker run -d --name mail-server --network lab9-red -p 8025:8025 -p 1025:1025 \
  mailhog/mailhog

# Verificar puertos
docker exec mail-server netstat -tlnp 2>/dev/null || docker port mail-server
```

**Pregunta 1**: ¿Qué puertos expone MailHog? ¿Cuál corresponde a SMTP y cuál a
la web de administración?

## Paso 2. Envía un correo hablando SMTP con `nc`

```bash
# Desde el host: diálogo SMTP en texto plano
printf "EHLO localhost\r\nMAIL FROM:<yo@universidad.pa>\r\nRCPT TO:<alumno@universidad.pa>\r\nDATA\r\nSubject: Hola desde la capa de aplicacion\r\nHola estudiante!\r\n.\r\nQUIT\r\n" | \
  timeout 5 nc localhost 1025
```

¿Qué respuestas recibiste?

```
250 EHLO
250 MAIL FROM
250 RCPT TO
354 End data with <CRLF>.<CRLF>
250 OK
221 Bye
```

## Paso 3. Ve el correo en la interfaz web

Abre `http://localhost:8025` en el navegador. El correo que enviaste por SMTP
aparece ahí (MailHog es un "pozo" de prueba que no reenvía realmente).

**Pregunta 2**: ¿Por qué el protocolo SMTP tiene comandos en texto plano en
el puerto 25? ¿Qué protocolo usaría una aplicación real para asegurar el
correo (SMTPS/STARTTLS, puertos 465/587)?

**Pregunta 3**: Diferencia entre SMTP (enviar), POP3 (descargar) e IMAP
(sincronizar en el servidor). ¿Cuál se usa en Gmail móvil y por qué?

## Paso 4. Levanta el servidor FTP (vsftpd)

```bash
# vsftpd con configuraciones mínimas
mkdir -p ftp-home
chmod 777 ftp-home

docker run -d --name ftp-server --network lab9-red \
  -p 21:21 -p 21000-21010:21000-21010 \
  -v $(pwd)/ftp-home:/home/vsftpd \
  -e FTP_USER=alumno -e FTP_PASS=lab123 \
  -e PASV_ADDRESS=127.0.0.1 \
  -e PASV_MIN_PORT=21000 -e PASV_MAX_PORT=21010 \
  fauria/vsftpd
```

## Paso 5. Consume FTP con `curl`

Desde el host usa `curl` (ya soporta FTP):

```bash
# Listar directorio
curl ftp://alumno:lab123@localhost/

# Subir un archivo
curl -T /etc/hostname ftp://alumno:lab123@localhost/subido.txt

# Descargar
curl ftp://alumno:lab123@localhost/subido.txt -o descargado.txt
cat descargado.txt
```

O desde un contenedor Alpine:

```bash
docker run --rm --network lab9-red alpine sh -c \
  "apk add --no-cache lftp && \
   lftp -u alumno,lab123 ftp-server -e 'ls; put /etc/hostname archivo-local.txt; quit'"
```

O con el cliente interactivo (si `ftp` está instalado en el host):

```bash
ftp -n localhost 21
> user alumno lab123
> pwd
> ls
> put /etc/hostname subido.txt
> get subido.txt
> quit
```

**Pregunta 4**: ¿Qué puertos usó FTP para la conexión de control (21) y para
la transferencia de datos (activo/pasivo)? ¿Por qué el modo pasivo necesita un
rango de puertos como 21000-21010?

> Nota de seguridad: FTP transmite usuario y contraseña **en texto plano**.
> ¿Qué alternativa segura conocerías (SFTP/FTPS)?

## Paso 6. Levanta el agente SNMP

```bash
docker run -d --name snmp-agent --network lab9-red \
  -p 161:161/udp \
  -e COMMUNITY=public \
  polinux/snmpd

# Ver el agente
docker exec snmp-agent snmpwalk -v2c -c public localhost 1.3.6.1.2.1.1.5.0
```

> Si la imagen `polinux/snmpd` fallara, puedes instalar `snmpd` del sistema:
> `sudo apt install -y snmpd && sudo service snmpd start`.

## Paso 7. Lee variables con `snmpwalk` (desde el host)

```bash
# Instalar herramientas SNMP (host)
sudo apt install -y snmp 2>/dev/null || true

# system.sysName
snmpwalk -v2c -c public localhost 1.3.6.1.2.1.1.5.0

# interfaces de red
snmpwalk -v2c -c public localhost 1.3.6.1.2.1.2.2.1.2

# estadísticas TCP (UDP/TCP de la capa de transporte)
snmpwalk -v2c -c public localhost 1.3.6.1.2.1.6.13.1
```

## Paso 8. Recorre el MIB — árbol de información

```bash
snmpwalk -v2c -c public localhost system
snmpwalk -v2c -c public localhost 1.3.6.1.2.1.7  # UDP stats
snmpwalk -v2c -c public localhost 1.3.6.1.2.1.6  # TCP stats
```

**Pregunta 5**: ¿Qué capa del modelo OSI reportan las estadísticas del OID
`1.3.6.1.2.1.6` (TCP)? ¿Para qué sirve SNMP en una infraestructura moderna de
monitoreo (Zabbix, Prometheus)?

## Paso 9. Puesta en conjunto: inventario de servicios activos

```bash
docker ps --format 'table {{.Names}}\t{{.Ports}}'

# Desde el host, listar puertos en escucha
netstat -tlnp | grep -E ':(80|443|21|25|53|1025|161)'
```

| Servicio | Contenedor | Puerto host | Puerto contenedor | Protocolo |
|----------|------------|-------------|-------------------|-----------|
| HTTP | web-server | 8081 | 80 | TCP |
| HTTPS | https-server | 8443 | 443 | TCP |
| FTP | ftp-server | 21 | 21 | TCP |
| SMTP | mail-server | 1025 | 1025 | TCP |
| DNS | dns-server | 53 | 53 | UDP/TCP |
| SNMP | snmp-agent | 161 | 161 | UDP |

**Pregunta 6**: Elabora una tabla como la anterior en tu entregable y
clasifica cada servicio según **puerto bien conocido** (registry of known
ports) y si usa TCP o UDP.

## Paso 10. Captura la conversación de una aplicación (DNS y SMTP)

```bash
# Terminal A: capturar DNS
docker exec dns-server tcpdump -i eth0 -nn port 53 &
# Terminal B: consultar DNS
docker run --rm --network lab9-red alpine sh -c \
  "apk add --no-cache bind-tools; dig app.io @dns-server +short"

# Terminal C: capturar SMTP
docker exec mail-server tcpdump -i eth0 -nn port 1025 &
# Terminal D: enviar correo smtp
printf "EHLO t\r\nQUIT\r\n" | timeout 3 nc localhost 1025
```

**Pregunta 7**: En la captura de DNS, ¿qué mensajes se ven (`query`, `answer`)?
¿En qué transporte viaja por defecto y cuándo se usa TCP para DNS?

---

## Entregable de la sesión

1. **Captura del diálogo SMTP con `nc`** (respuestas 250/354/221) y de MailHog mostrando el correo en la web.
2. **Captura de FTP** con `curl`: listar, subir y descargar `subido.txt`.
3. **Captura de `snmpwalk`** (sysName, interfaces y stats UDP/TCP).
4. **Tabla de servicios con puertos y protocolo** (Pregunta 6).
5. **Capturas de tcpdump** de la conversación DNS y SMTP.
6. **Respuestas** a las preguntas 1 a 7.

## Rúbrica de la sesión

| Criterio | Puntos |
|----------|--------|
| Correo SMTP: MailHog + envío con `nc` | 12 |
| FTP: vsftpd + `curl`/`lftp` (listar, subir, bajar) | 8 |
| SNMP: agente + `snmpwalk` | 10 |
| Tabla de servicios y puertos (Pregunta 6) | 6 |
| Capturas tcpdump de DNS y SMTP | 6 |
| Evidencias y capturas | 8 |
| **Total** | **50** |