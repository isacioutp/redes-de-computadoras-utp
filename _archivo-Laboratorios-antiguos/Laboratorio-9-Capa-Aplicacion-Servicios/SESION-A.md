# Laboratorio N.° 9 — Servicios de la Capa de Aplicación · Sesión A: HTTP, HTTPS y DNS (con curl y dig)

Semana 9 · Clase 1

Cubre las **Partes 1, 2 y 3** del laboratorio original: HTTP (nginx, `curl -v`,
códigos de estado y tcpdump), HTTPS (certificado con `openssl` + nginx + `curl
-k`) y DNS (resolución con `dig`, servidor propio dnsmasq y service discovery
de Docker).

## Objetivo de la sesión

Vas a levantar servidores web (nginx y Apache), a dialogar con HTTP escribiendo
los métodos con `curl -v` y leyendo los códigos de estado, a crear un
certificado con `openssl` para servir HTTPS, y a montar tu propio servidor DNS
que traduzca nombres hacia direcciones que tú definas.

---

## Paso 1. Levanta los servidores web

```bash
# Red de trabajo
docker network create lab9-red

# Servidor web estático
docker run -d --name web-server --network lab9-red -v $(pwd)/html:/usr/share/nginx/html:ro -p 8081:80 nginx:alpine

# Servidor web 2 (Apache) en otro puerto
docker run -d --name apache-server --network lab9-red -p 8082:80 httpd:alpine

mkdir -p html
echo "<h1>Redes - Laboratorio 9</h1>" > html/index.html
echo "Server 1" > html/servidor1.txt
```

**Pregunta 1**: ¿Qué diferencia hay entre los puertos `8081` y `80`? ¿Por qué
se mapean?

## Paso 2. Consume HTTP con `curl -v`

```bash
# GET (leer)
curl -v http://localhost:8081/
curl -v http://localhost:8081/servidor1.txt

# Decodificar headers
curl -i http://localhost:8081/

# Métodos que el servidor soporta (opcional de nginx)
curl -X OPTIONS http://localhost:8081/ -i
```

Verás la **conversación HTTP**:

```
GET / HTTP/1.1
Host: localhost:8081
User-Agent: curl/8.x
Accept: */*

HTTP/1.1 200 OK
Server: nginx/1.25.x
Date: ...
Content-Type: text/html
Content-Length: 44
```

## Paso 3. Observa los códigos de estado

```bash
# 200 OK
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8081/

# 404 Not Found
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8081/no-existe

# 301 Redirect (configurable con nginx)
curl -s -I http://localhost:8081/ | head -1
```

**Pregunta 2**: Enumera 5 códigos de estado HTTP y cuándo se usan
(200, 301, 400, 401, 404, 500, etc.).

## Paso 4. Consume HTTP hacia dentro del contenedor

```bash
# Desde el host: curl hacia internet
docker exec web-server wget -q -O - http://localhost/ 2>/dev/null || true

# Desde otro contenedor, usar la IP interna de web-server
curl -s http://$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web-server)/
```

**Pregunta 3**: ¿La IP del host y la del contenedor podrían chocar? ¿Cómo
resolvería Docker ese conflicto de puertos?

## Paso 5. Observa la conversación con tcpdump

```bash
docker exec web-server sh -c "apk add --no-cache tcpdump" 
```

```bash
# Terminal A: iniciar la captura (queda escuchando)
docker exec web-server tcpdump -i eth0 -nn port 80
```

```bash
# Terminal B: hacer la petición
curl -v http://localhost:8081/
```

Observa la secuencia: `SYN → SYN-ACK → ACK` (transporte) y luego las
peticiones HTTP (aplicación).

**Pregunta 4**: ¿Qué capas coexisten en la petición HTTP? ¿Qué headers de
aplicación añadió curl y cuáles respondió nginx?

## Paso 6. Sirve HTTPS con un certificado autofirmado

```bash
# Generar certificado autofirmado con openssl (en el host)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout privkey.pem -out server.crt \
  -subj "/C=PA/ST=Panama/L=CD/L=UTP/O=Redes/CN=localhost"

# Servidor HTTPS con nginx
docker run -d --name https-server \
  -p 8443:443 \
  -v $(pwd)/server.crt:/etc/nginx/ssl/server.crt:ro \
  -v $(pwd)/privkey.pem:/etc/nginx/ssl/privkey.pem:ro \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  -v $(pwd)/nginx-ssl.conf:/etc/nginx/conf.d/default.conf:ro \
  nginx:alpine

# nginx-ssl.conf
cat > nginx-ssl.conf << 'EOF'
server {
    listen 443 ssl;
    server_name localhost;
    ssl_certificate     /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    location / {
        root /usr/share/nginx/html;
        index index.html;
    }
}
EOF
```

Probarlo:

```bash
# Falla (certificado no confiable)
curl https://localhost:8443/ --insecure -v 2>/dev/null | head -5
# con -k (insecure) para aceptar el certificado generado
curl -k https://localhost:8443/
```

**Pregunta 5**: ¿Por qué aparece "certificate verification failed"? ¿Qué hace
`-k`? ¿Cómo se llama la mano de obra TLS/X.509 en este escenario de
desarrollo?

## Paso 7. Resuelve nombres hacia internet con `dig`

```bash
# Desde un contenedor
docker run --rm --network lab9-red alpine sh -c "apk add --no-cache bind-tools && \
  dig google.com +short && \
  dig google.com A AAAA +short"
```

**Pregunta 6**: ¿Qué registros `A` y `AAAA` obtuviste? ¿Qué significa que
google.com tenga varias IPs *A*?

## Paso 8. Levanta tu propio servidor DNS (dnsmasq)

```bash
# Servidor DNS local
docker run -d --name dns-server --network lab9-red -p 53:53/udp -p 53:53/tcp \
  jpillora/dnsmasq --log-queries \
  --address=/app.io/10.10.10.10 \
  --address=/.docker.lab/192.168.99.100 \
  --server=8.8.8.8
```

## Paso 9. Consulta tu DNS con `dig`/`nslookup`

```bash
# Resolver un host local inventado
docker exec dns-server dig app.io @localhost +short

# Resolver un nombre de base de datos falso
docker run --rm --network lab9-red alpine sh -c "apk add --no-cache bind-tools; \
  nslookup app.io 172.18.0.X; nslookup db.docker.lab dns-server"
```

> Reemplaza `172.18.0.X` con la IP del dns-server: `docker inspect
> -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dns-server`

**Pregunta 7**: Con `app.io` respondiendo `10.10.10.10`, ¿qué registro DNS se
está usando? ¿Cuántos tipos de registro conoces (A, AAAA, CNAME, MX, TXT,
NS)?

## Paso 10. Observa el service discovery de Docker

```bash
# Servicio con nombre explícito en Docker
docker run -d --name api-service --network lab9-red alpine sleep 3600

# Resolver el nombre del contenedor (lo usó el Lab N.º 5)
docker run --rm --network lab9-red alpine sh -c "apk add --no-cache bind-tools; \
  nslookup api-service"
```

**Pregunta 8**: ¿Cómo resuelve Docker el nombre `api-service` sin un servidor
DNS explícito? ¿Qué implicación tiene para los microservicios de tu proyecto?

---

## Entregable de la sesión

1. **Captura de `curl -v`** mostrando la conversación HTTP (request + response headers).
2. **Captura de los códigos de estado** (200 y 404) con `-w "%{http_code}"`.
3. **Captura de `curl -k`** respondiendo por HTTPS en el puerto 8443.
4. **Captura de `dig`** con las respuestas (A/AAAA de google.com, `app.io` y `api-service`).
5. **Respuestas** a las preguntas 1 a 8.

## Rúbrica de la sesión

| Criterio | Puntos |
|----------|--------|
| Servidores HTTP levantados (nginx y Apache) + conversación con `curl -v` | 12 |
| Códigos de estado HTTP observados | 6 |
| HTTPS con `openssl` + nginx + `curl -k` | 10 |
| Servidor DNS propio (dnsmasq) + consultas con `dig`/`nslookup` | 12 |
| Evidencias y capturas | 10 |
| **Total** | **50** |