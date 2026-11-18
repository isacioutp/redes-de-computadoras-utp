# Laboratorio N.º 16 — El despliegue que nadie vio

Semana 14+ · Unidad III · **1 sesión** (recorte a 20 min)

Un despliegue sale en verde: la imagen nueva está publicada y el smoke test
responde `v2`. Los usuarios, mientras tanto, siguen viendo `v1` o reciben un
502. No falló el build: fallaron dos caminos de red por los que pasa el
tráfico, el DNS y el proxy.

> Este laboratorio es independiente: no necesita otros laboratorios ni material
> previo del curso.

## 1. Lo que vas a reproducir

Dos fallas distintas, en dos capas:

1. **El proxy guardó una IP vieja.** `nginx` resolvió el nombre `api` cuando
   arrancó. Al recrear el contenedor con `v2` cambió su IP, pero el `nginx` en
   ejecución sigue conectándose a la IP anterior: 502.
2. **El DNS tenía un TTL largo.** Los clientes que ya resolvieron el nombre
   siguen yendo al host antiguo, que todavía sirve `v1`. Si se apaga ese host,
   esos clientes se quedan sin servicio.

El smoke test pasa porque consulta al contenedor por su puerto publicado, sin
pasar por el proxy ni por el DNS.

## 2. Topología

```text
  cliente con caché                 cliente que resuelve ahora
  127.0.0.2:18080                   127.0.0.1:18080
        |                                  |
   proxy-viejo                        proxy-nuevo
        |                                  |
   api-viejo (v1)                     api (v1 -> v2)
   172.28.16.12:8000                  172.28.16.10 -> .11 :8000
```

| Servicio | Función | Dirección |
|----------|---------|-----------|
| `proxy-viejo` | Simula el host antiguo | `127.0.0.2:18080` |
| `proxy-nuevo` | Simula el host nuevo | `127.0.0.1:18080` |
| `api-viejo` | Versión `v1` que siguen viendo los clientes cacheados | red `lab` |
| `api` | Versión `v1`, se reemplaza por `v2` en el paso 3 | red `lab` |

Las direcciones `127.0.0.2` y `127.0.0.1` representan dos hosts distintos. El
parámetro `--resolve` de `curl` simula la entrada que el cliente ya tiene en
caché, así que no hay que editar `/etc/hosts` ni levantar un servidor DNS.

## 3. Requisitos

- Docker Engine con el plugin **Compose v2** (`docker compose version`).
- `curl`.
- Linux, macOS o WSL. En macOS, `127.0.0.2` no responde: cambiá el mapeo del
  `proxy-viejo` a `127.0.0.1:18090:80` y usá `18090` en los comandos del cliente
  cacheado.

Los puertos 18080 y 18081 tienen que estar libres.

## Paso 1 · Levantar la versión inicial

```bash
cd DevOps/Laboratorio-16-Despliegue-Invisible
docker compose up -d --build
docker compose ps
```

Comprobá los dos caminos antes del cambio:

```bash
curl -fsS --resolve api.citasya.test:18080:127.0.0.2 \
  http://api.citasya.test:18080/
# CitasYA api v1

curl -fsS --resolve api.citasya.test:18080:127.0.0.1 \
  http://api.citasya.test:18080/
# CitasYA api v1
```

## Paso 2 · Ver qué resolvió el proxy

```bash
docker exec lab16-proxy-nuevo getent hosts api
# 172.28.16.10      api  api

docker exec lab16-proxy-nuevo nginx -T | grep proxy_pass
# proxy_pass http://api:8000;
```

El archivo de configuración dice `api`, no una IP. nginx resolvió ese nombre al
arrancar y guardó el resultado dentro del proceso.

## Paso 3 · Desplegar `v2`

El tag cambia y también la IP del contenedor, como pasaría al recrearlo en otra
dirección:

```bash
TAG=v2 API_IP=172.28.16.11 docker compose up -d --build api
```

El smoke test va directo al contenedor publicado y pasa:

```bash
for i in $(seq 1 20); do
  curl -fsS localhost:18081/ && break
  sleep 0.5
done
# CitasYA api v2
```

## Paso 4 · Medir desde donde está el usuario

```bash
curl -sS -o /dev/null -w '%{http_code}\n' \
  --resolve api.citasya.test:18080:127.0.0.1 \
  http://api.citasya.test:18080/
# 502

docker logs --tail 4 lab16-proxy-nuevo
# connect() failed (113: Host is unreachable) while connecting to upstream,
# upstream: "http://172.28.16.10:8000/"
```

El pipeline está en verde y el usuario recibe un 502. El `getent hosts api` del
paso 2 ahora devuelve `172.28.16.11`: el DNS interno ya cambió, el proceso de
nginx no.

## Paso 5 · Reparar el proxy

```bash
docker exec lab16-proxy-nuevo nginx -s reload
curl -fsS --resolve api.citasya.test:18080:127.0.0.1 \
  http://api.citasya.test:18080/
# CitasYA api v2
```

No cambió ni una línea de configuración: alcanzó con recargar el proceso. Por eso
el reload tiene que ser parte del despliegue.

## Paso 6 · El cliente con DNS cacheado

```bash
curl -fsS --resolve api.citasya.test:18080:127.0.0.2 \
  http://api.citasya.test:18080/
# CitasYA api v1
```

Ese cliente no llega al host nuevo. Si apagás el host viejo, se queda sin
servicio:

```bash
docker compose stop proxy-viejo
curl -sS --resolve api.citasya.test:18080:127.0.0.2 \
  http://api.citasya.test:18080/
# curl: (7) Failed to connect to api.citasya.test port 18080
```

En un caso real el equivalente es bajar el TTL del registro A antes del corte,
esperar a que venza y mantener el host anterior arriba durante esa ventana.

## Paso 7 · Limpieza

```bash
docker compose down
docker rmi citas-api:v1 citas-api:v2
```

## Evidencia de la prueba

Salida real de este laboratorio ejecutado de punta a punta:

```text
== v1 por ambos caminos
CitasYA api v1
CitasYA api v1
== despliegue de v2
 Container lab16-api Recreated
== smoke directo al contenedor
CitasYA api v2
== por el proxy nuevo
502
== por el proxy viejo (cliente con caché)
CitasYA api v1
== DNS interno
172.28.16.11      api  api
== logs del proxy
connect() failed (113: Host is unreachable) while connecting to upstream,
upstream: "http://172.28.16.10:8000/"
== tras nginx -s reload
CitasYA api v2
== cliente con caché, host viejo apagado
curl: (7) Failed to connect to api.citasya.test port 18080
```

## Qué entregas

1. **Bitácora** de los 7 pasos con la IP del contenedor `api` en cada momento.
2. **Las tres respuestas** del smoke, del proxy nuevo y del cliente cacheado,
   con el código HTTP de cada una.
3. **Un comando por falla** que lo demuestre: `getent hosts`, `nginx -T` y
   `curl --resolve`.
4. **Mapa de los 4 flujos**: cliente → DNS, cliente → proxy, proxy → contenedor
   y smoke → contenedor. origen, destino, puerto y qué se rompe si falla.
5. **Plan de corrección** de cinco líneas: smoke por la ruta del usuario,
   reload del proxy, TTL bajo antes del corte, host viejo arriba durante la
   ventana y sonda desde fuera del servidor.

> Se evalúa la explicación de red: saber por qué el smoke pasa y el usuario no.
