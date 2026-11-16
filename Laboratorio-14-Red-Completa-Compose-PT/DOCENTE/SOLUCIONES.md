# Soluciones y respuestas de referencia — Laboratorio N.º 14

Documento **interno** (no publicar). Contiene la plantilla `docker-compose.yml`
de referencia, las **respuestas** de las preguntas de la pista A y —como
**pista B opcional**— la configuración del `.pkt`.

---

## 1. Configuración del `.pkt` (pista B, opcional)

### 1.1 Direccionamiento

| Dispositivo | Interfaz | IP | Máscara | Gateway |
|-------------|----------|----|---------|---------|
| R1 | G0/0 (WAN) | 200.200.200.1 | 255.255.255.252 | — |
| R1 | G0/1 (LAN) | 10.10.10.1 | 255.255.255.0 | — |
| srv-bastion | Fa0 | 10.10.10.2 | 255.255.255.0 | 10.10.10.1 |
| srv-bastion | Fa1 | 10.20.20.2 | 255.255.255.0 | — |
| srv-interno | Fa0 | 10.20.20.10 | 255.255.255.0 | 10.20.20.2 |
| PC-admin | Fa0 | 10.10.10.10 | 255.255.255.0 | 10.10.10.1 |

### 1.2 Router R1

```
enable
conf t
 hostname R1
 interface GigabitEthernet0/0
  ip address 200.200.200.1 255.255.255.252
  no shutdown
 interface GigabitEthernet0/1
  ip address 10.10.10.1 255.255.255.0
  no shutdown
 ip route 10.20.20.0 255.255.255.0 <siguiente salto hacia el bastión si aplica>
end
write
```

> Nota didáctica: la red 10.20.20.0/24 **no** debe ser enrutada por R1 hacia
> Internet. El único camino a ella es a través del bastión (doble salto SSH).

### 1.3 Bastión (SSH)

En `srv-bastion` → Desktop → **Services → SSH**: activar, usuario `admin`,
password `lab14pass`. En CLI:

```
enable
conf t
 hostname srv-bastion
 ip domain-name lab14.local
 crypto key generate rsa modulus 1024
 ip ssh version 2
 username admin privilege 15 secret cisco
 line vty 0 15
  transport input ssh
  login local
 exit
end
write
```

- **No** habilitar `ip routing` en el bastión: no es router, es estación.

### 1.4 ACL en R1 (Paso 3 del lab paralelo)

```
conf t
 ip access-list extended SOLO-ADMIN
   permit tcp host 10.10.10.10 host 10.10.10.2 eq 22
   deny   ip any host 10.20.20.10
   permit ip 10.10.10.0 0.0.0.255 any
 exit
 interface GigabitEthernet0/1
   ip access-group SOLO-ADMIN in
 exit
end
```

**Verificación en Simulation mode:** el ping PC-admin → 10.20.20.10 debe
detenerse en R1 con marca de descarte.

---

## 2. `docker-compose.yml` de referencia (resultado de la Sesión 3)

> Es el mismo contenido de [`../sesion-4/`](../sesion-4/README.md) (punto de
> partida de la Sesión 4). Los puntos de partida de cada sesión están en
> [`../sesion-1/`](../sesion-1/README.md), [`../sesion-2/`](../sesion-2/README.md),
> [`../sesion-3/`](../sesion-3/README.md) y [`../sesion-4/`](../sesion-4/README.md).

```yaml
services:
  dns:
    image: strm/dnsmasq
    container_name: dns-corp
    volumes: [ ./dnsmasq.conf:/etc/dnsmasq.conf:ro ]
    networks:
      front: { ipv4_address: 172.28.10.53 }
    command: ["-k", "--log-facility=-", "-u", "root"]
    healthcheck:
      test: ["CMD", "nslookup", "web.local", "127.0.0.1"]
      interval: 5s
      timeout: 3s
      retries: 5
    restart: unless-stopped

  web:
    image: nginx:alpine
    container_name: web-srv
    ports: ["8080:80"]
    depends_on:
      api: { condition: service_healthy }
    networks:
      front: { ipv4_address: 172.28.10.10 }
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost/"]
      interval: 5s
      timeout: 3s
      retries: 5
    restart: unless-stopped

  api:
    build: ./api
    image: lab14-api
    environment:
      DB_HOST: db.local
      DB_USER: appuser
    networks: [front, back]
    expose: ["8000"]
    healthcheck:
      test: ["CMD", "python", "-c",
             "import urllib.request as u;u.urlopen('http://localhost:8000/ping')"]
      interval: 5s
      timeout: 3s
      retries: 5
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: db-srv
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD_FILE: /run/secrets/db_pass
    secrets: [db_pass]
    volumes: [pgdata:/var/lib/postgresql/data]
    networks:
      back: { ipv4_address: 172.28.20.20 }
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser"]
      interval: 5s
      retries: 5
    restart: unless-stopped

secrets:
  db_pass:
    file: ./db_pass.txt

networks:
  front:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.10.0/24
  back:
    driver: bridge
    internal: true
    ipam:
      config:
        - subnet: 172.28.20.0/24

volumes:
  pgdata: {}
```

**`dnsmasq.conf`**

```
address=/web.local/172.28.10.10
address=/api.local/172.28.10.20
address=/db.local/172.28.20.20
```

> Con `--scale api=2` la IP fija del API entra en conflicto; por eso en el stack
> orquestado ([`../sesion-4/`](../sesion-4/README.md)) la API **no** tiene
> `ipv4_address` y se resuelve con el DNS de Docker (`nslookup api`). El
> `dnsmasq.conf` de `sesion-4/` solo publica `web.local` y `db.local`.

---

## 3. Respuestas — Preguntas de la pista B (Packet Tracer, opcional)

1. **¿Por qué srv-interno tiene como gateway al bastión y no a R1?** Porque
   `srv-interno` está en la red interna (10.20.20.0/24) y solo el bastión tiene
   una interfaz ahí. Enrutar su tráfico hacia R1 lo expondría; pasar por el
   bastión obliga a que todo acceso interno se autentique.
2. **¿Qué pasa si intercambias `permit` y `deny` en la ACL?** La ACL se evalúa
   de arriba hacia abajo y **se detiene en la primera coincidencia**. Si `deny
   ip any host 10.20.20.10` queda **antes** del `permit`, incluso el tráfico
   permitido que coincida caería en la regla denegada (o dejaría de permitirse
   el ICMP legítimo). El orden define la semántica.
3. **¿En qué dispositivo cambia la IP de destino y la de origen?** El paquete
   viaja **con la IP final** (10.20.20.10) hasta el bastión; la IP de origen
   sigue siendo la del PC-admin. El bastión **no reescribe** (no es router): por
   eso se usa **SSH con doble salto**, que crea dos conexiones distintas (PC→
   bastión y bastión→interno). En PT lo ves como dos PDUs separados.
4. **¿Está el forwarding habilitado en el bastión?** No (`ip routing` deshabilitado).
   Un bastión **no** debe reenviar paquetes: si reenvía, deja de ser "punto de
   entrada controlado" y pasa a ser un router (un salto más en una ruta).
5. **¿Cuál modelo es más defendible ante un auditor?** El de PT: hay una **ruta
   inexistente + ACL explícita** documentadas y verificables (Simulation mode).
   En Docker, `internal: true` + no publicar puertos es correcto pero **menos
   visible**; por eso se documenta y se demuestra con `curl` fallido.

---

## 4. Respuestas — Sesión 1

1. **¿Qué hace Compose que no hacía `docker run`?** Declara el **estado
   deseado** en un archivo versionable y lo reconcilia: crea redes, resuelve
   dependencias, asigna nombres DNS y reproduce el entorno completo con `up`,
   sin recordar la secuencia de `docker run`.
2. **¿Qué cambió para que `web` ya no alcance `db`?** (a) la DB se movió a la
   red `back` (`internal: true`) y la web quedó solo en `front`; (b) la DB dejó
   de publicar puertos. El único puente entre ambas redes es la API, que está en
   las dos.
3. **¿Qué protege `internal: true` y qué no?** Protege contra la salida a
   Internet (quita NAT/masquerade). **No** aísla a los contenedores *dentro* de
   la red ni impide que alguien alcance un contenedor que **publique** un puerto.
4. **¿Por qué publicar `ports:` en la DB rompería la segmentación?** Abriría un
   puerto del host hacia la DB; cualquiera con acceso al host llegaría directo a
   5432, evadiendo el diseño "solo la API toca la DB".

## 5. Respuestas — Sesión 2

1. **¿Qué mecanismo de Linux implementa el aislamiento de `back`?** Los
   **puentes** de red (bridge) de Docker más reglas de **iptables/nftables**;
   `internal: true` traduce a reglas que cortan el *egress*. Es "menos visible"
   porque no hay una ACL legible en un equipo: son reglas generadas.
2. **¿Qué cambia si quitas `internal: true` de `back`?** La red gana salida a
   Internet (NAT); los contenedores de `back` podrían alcanzar/hacia fuera. La
   segmentación de *datos* sigue, pero se pierde el aislamiento de *egress*.
3. **¿Por qué el API puede ser el puente y la DB no?** El API necesita hablar con
   web (front) y con la DB (back): es su función. La DB no necesita salir de
   `back`; darle doble red solo ampliaría su superficie de ataque.
4. **¿Por qué el host es más seguro que un contenedor bastión?** Porque el host
   es un sistema separado con su propio kernel: su compromiso no expone
   mágicamente a otros hosts, y el acceso se controla con `sshd`
   (`PasswordAuthentication no`) + `authorized_keys`. Un contenedor bastión
   comparte kernel con lo que "protege".

## 6. Respuestas — Sesión 3

1. **¿Por qué la db no tiene `ports:` y la web sí?** La web es el punto público
   (única puerta). La DB no debe ser alcanzable desde fuera; vive solo en la red
   interna. Publicar la DB anula la segmentación.
2. **¿Qué problema evita `service_healthy` frente a `depends_on` sin condición?**
   `depends_on` solo ordena el *arranque*; `service_healthy` espera a que el
   servicio pase su `healthcheck` (esté **listo**). Evita que la web reciba
   tráfico antes de que la API responda (errores en los primeros segundos).
3. **¿Por qué `docker inspect` no revela la clave pero `/run/secrets` sí?** El
   secreto se monta como archivo dentro del contenedor (solo visible desde
   dentro); `inspect` mostraría `environment:` en claro. Principio: **mínima
   exposición / separación de secretos**.
4. **3 cosas que Swarm sí y Compose no:** (1) cluster multi-nodo con
   manager/worker; (2) red **overlay** entre nodos; (3) balanceo ingress mesh +
   rolling update/rollback gestionado.

## 7. Respuestas — Sesión 4

1. **¿Por qué `down` conserva datos y `down -v` no?** `down` borra contenedores
   y redes pero respeta los **volúmenes** (`pgdata`); `-v` los elimina. En
   producción, los datos deben vivir en un volumen (o volumen externo) y
   respaldarse aparte.
2. **Diferencia de self-healing Compose vs Swarm:** Compose reinicia
   contenedores en el **mismo host**; Swarm reprograma **tareas entre nodos**
   cuando un nodo cae (reconciliación distribuida).
3. **Frase final:** el bastión real es el host/VM porque es un sistema aislado
   por kernel, endurecido (solo llave) y con el firewall real (iptables) a su
   cargo; un contenedor comparte kernel y su "aislamiento" es lógico, no de
   sistema.

---

## 8. Comandos de referencia rápida

```bash
# Arranque limpio y reproducibilidad
docker compose down -v --remove-orphans
docker compose up -d --wait
docker compose ps

# Segmentación
docker run --rm --network front alpine ping -c1 172.28.20.20   # falla
docker exec api-srv sh -c "nc -z 172.28.20.20 5432 && echo ok" # funciona

# Monitoreo
docker exec web-srv tcpdump -i eth0 -c 20 -n port 80
sudo iftop -i br-front
# netdata en http://localhost:19999

# Secretos
docker exec db-srv cat /run/secrets/db_pass
docker inspect db-srv | grep -i password   # vacío

# Escalado y balanceo
docker compose up -d --scale api=2
docker compose exec web nslookup api 127.0.0.11

# Respaldo / restauración
docker exec db-srv pg_dump -U appuser postgres > respaldo_lab14.sql
docker compose down -v && docker compose up -d --wait
docker exec -i db-srv psql -U appuser postgres < respaldo_lab14.sql

# Self-healing
docker exec api-srv pkill -f app.py && sleep 6 && docker compose ps api
```

## 9. Criterios de corrección rápida

- Si la captura de segmentación muestra que `front` alcanza `back` → revisar
  `internal: true` y `ports:` antes de calificar.
- Si el `docker-compose.yml` contiene la contraseña → 0 en el criterio de
  secretos.
- Si el stack no se reproduce desde cero con un comando → no cumple
  reproducibilidad.
- Si las capturas no coinciden con lo levantado al revisar → descuento por
  evidencia no verificable (ver política anti-copia en EVALUACION.md).
