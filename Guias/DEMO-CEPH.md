# Demo en vivo — Ceph sobre Tailscale (Parte 4: almacenamiento compartido)

Guion docente para **2 VM (ceph-1 y ceph-2)** ya conectadas por **Tailscale**
(overlay de WireGuard). Cada demo prueba una lámina de
`../Teoria/Teoria-U3-Parte4-Almacenamiento-Compartido.pptx` — de la teoría al clúster real.

> **Idea ancla:** el storage distribuido es software sobre Ethernet. Aquí lo
> montamos con dos comandos por VM, y la "red de storage" es literalmente una
> overlay WireGuard: red segmentada (3.1) + latencia medible (3.2) + replicación
> por software (Parte 4).

**Por qué 2 nodos es la demo perfecta (y un desastre de producción):** Ceph con
2 monitores **no tolera ninguna caída** — sin mayoría no hay quórum y el clúster
se congela. Eso es exactamente la lámina 9. En la Demo 4 lo provocamos a
propósito; en la Demo 5 lo arreglamos con un tercer voto.

---

## 0. Qué queda montado al final de la preparación

```
        tailnet Tailscale (WireGuard, 100.64.0.0/10)
   ceph-1 (100.114.231.54)◄──────►ceph-2 (100.78.198.83)
   mon · mgr · mds · osd          mon · mgr · mds · osd
   1 OSD loop de 8 GiB            1 OSD loop de 8 GiB
   └── CephFS "demo-fs" montado en /mnt/cephfs de AMBAS VM
   └── export NFS → /pgdata (para el Lab 14)
```

---

## 1. Preparación (antes de clase · ~30 min)

### 1.1 Instalar MicroCeph en ambas VM

```bash
sudo snap install microceph
sudo snap refresh --hold microceph     # congelar auto-actualizaciones
```

### 1.2 Formar el clúster

```bash
# en ceph-1
sudo microceph cluster bootstrap

# si ceph-2 no alcanza la IP que trae el token (VM en nubes distintas),
# repetir el bootstrap con la IP de Tailscale:
sudo microceph cluster bootstrap --mon-ip 100.114.231.54

sudo microceph cluster add ceph-2      # imprime un TOKEN largo
```

```bash
# en ceph-2  (si hace falta, añade: --microceph-ip 100.78.198.83)
sudo microceph cluster join <TOKEN>
```

### 1.3 Almacenamiento y ajuste a 2 nodos

```bash
# en CADA VM: 1 OSD de demo (loop — suficiente para clase, jamás producción)
sudo microceph disk add loop,8G,1

# en ceph-1: réplicas=2 porque solo hay 2 OSD (Ceph quiere 3 por defecto)
sudo microceph.ceph config set global osd_pool_default_size 2
sudo microceph.ceph config set global osd_pool_default_min_size 1
sudo microceph.ceph osd pool set .mgr size 2   # el pool interno ya existía

sudo microceph status     # debe mostrar los 2 nodos: mds, mgr, mon, osd
```

### 1.4 El sistema de archivos compartido (CephFS)

```bash
# en ceph-1
sudo microceph.ceph fs volume create demo-fs
```

```bash
# en CADA VM (para montar desde las propias nodos)
sudo apt install ceph-common
sudo ln -s /var/snap/microceph/current/conf/ceph.conf   /etc/ceph/ceph.conf
sudo ln -s /var/snap/microceph/current/conf/ceph.keyring /etc/ceph/ceph.keyring
sudo mkdir -p /mnt/cephfs
sudo mount -t ceph :/ /mnt/cephfs -o name=admin,fs=demo-fs
```

### 1.5 (Opcional, para la Demo 5) el tercer voto

En **cualquier tercera máquina del tailnet** (laptop, VM pequeña — no necesita
disco, solo mon):

```bash
sudo snap install microceph
# en ceph-1: sudo microceph cluster add testigo   → TOKEN
sudo microceph cluster join <TOKEN-testigo>
```

### 1.6 Verificación final (checkpoint de la preparación)

```bash
sudo microceph.ceph -s          # en ceph-1: health, 2 mons en quórum, 2 OSD up
sudo microceph.ceph osd tree    # 2 hosts, 1 OSD cada uno
ls /mnt/cephfs                  # montado en ambas VM, vacío
```

---

## 2. Guion en clase (~25 min)

| # | Demo | Lámina que prueba | Min |
|---|------|-------------------|-----|
| 1 | El mapa del clúster | Cómo lo consume el orquestador | 4 |
| 2 | Storage compartido real | El dato no es desechable / distribuido | 5 |
| 3 | La red que hay debajo | El storage ES tráfico de red | 3 |
| 4 | **Quórum: se cae un nodo** | Quórum y split-brain | 5 |
| 5 | El tercer voto (opcional) | «3 nodos toleran 1» | 5 |
| 6 | El puente al Lab 14 (NFS) | Volumen NFS en Compose | 3 |

### Demo 1 — El mapa del clúster

```bash
sudo microceph status
sudo microceph.ceph osd tree
```

**Qué señalar:** 2 hosts, 1 OSD cada uno, servicios `mon·mgr·mds·osd` en
ambos. **Paralelo exacto con `docker node ls` y `docker service ps` de la
Parte 3:** mismo modelo de clúster, distinta capa.

### Demo 2 — Storage compartido real

```bash
# en ceph-1
echo "escrito en $(hostname) · $(date)" | sudo tee /mnt/cephfs/nota.txt

# en ceph-2
cat /mnt/cephfs/nota.txt        # el mismo archivo, al instante
sudo microceph.ceph df           # el cluster creció ~2x el tamaño del archivo
```

**Qué señalar:** escribimos en un nodo y lo leímos en el otro **sin copiar
nada**: no hay "el disco de ceph-1", hay un sistema de archivos del clúster.
Y `df` muestra el precio: **2 réplicas** de cada dato (lámina 10).

### Demo 3 — La red que hay debajo

```bash
tailscale status | grep ceph
tailscale ping ceph-2
ping -c 5 100.78.198.83         # latencia y jitter (3.2)
```

**Qué señalar:** toda la replicación de la Demo 2 viajó cifrada por una
**overlay WireGuard** — el mismo concepto de red overlay que Swarm (Parte 3).
Cada escritura = ida y vuelta: la latencia aquí se paga doble (lámina 8).

### Demo 4 — Quórum: se cae un nodo (LA demo)

```bash
# apagar la VM ceph-2 por completo (o desde ceph-2: sudo shutdown -h now)

# en ceph-1:
sudo microceph.ceph -s          # se cuelga / "quorum lost": sin mayoría no responde
cat /mnt/cephfs/nota.txt        # la lectura se queda esperando: clúster congelado
```

**Qué señalar:** **2 monitores = 0 caídas toleradas.** Sin mayoría, el clúster
prefiere congelarse antes que arriesgar el dato (anti-split-brain, lámina 9).
Encender ceph-2 de nuevo y esperar ~1 min: vuelve el quórum y responde todo.

### Demo 5 — El tercer voto (opcional)

Con la máquina `testigo` de la preparación 1.5, repetir la caída de ceph-2:

```bash
sudo microceph.ceph -s           # ahora SÍ responde: HEALTH_WARN
sudo microceph.ceph osd tree     # marca el OSD de ceph-2 "down"
cat /mnt/cephfs/nota.txt         # la réplica que queda en ceph-1 sigue sirviendo
```

**Qué señalar:** con **3 mons, 1 caída es tolerable** — el clúster degrada
(`HEALTH_WARN`) pero sigue vivo: eso es HA de verdad. El testigo no tiene
discos: **los votos son baratos, las réplicas no**.

### Demo 6 — El puente al Lab 14: NFS desde CephFS

```bash
# en ceph-1
sudo microceph enable nfs --cluster-id ha-demo --target ceph-1
sudo microceph.ceph nfs export create cephfs ha-demo /pgdata demo-fs

# desde cualquier máquina del tailnet (o el host Docker del Lab 14):
sudo apt install nfs-common
sudo mkdir -p /mnt/pgdata
sudo mount -t nfs 100.114.231.54:/pgdata /mnt/pgdata
```

Y la pieza que cierra el círculo — el volumen `pgdata` del Lab 14 ya no vive
en el host (lámina 12, tal cual):

```yaml
volumes:
  pgdata:
    driver_opts:
      type: nfs
      o: addr=100.114.231.54,rw,nfsvers=4
      device: ":/pgdata"
```

**Qué señalar:** la db del Lab 14 escribiendo en storage **distribuido y
replicado**, montado por NFS (2049/TCP) — la lámina 12 funcionando en vivo.

---

## 3. Troubleshooting de la demo

| Síntoma | Causa | Arreglo |
|---------|-------|---------|
| `cluster join` no conecta | la IP del token no es alcanzable | `bootstrap --mon-ip <IP-tailnet-de-ceph-1>` y `join --microceph-ip <IP-tailnet-de-ceph-2>` |
| `HEALTH_WARN` "undersized/not enough" | pools con size 3 y solo 2 OSD | `config set global osd_pool_default_size 2` + `osd pool set .mgr size 2` |
| `mount -t ceph` pide keyring | faltan los symlinks de `/etc/ceph` | repetir el paso 1.4 de symlinks |
| `ceph -s` se cuelga | **sin quórum — esperado en la Demo 4** | no es un error: es el tema de la clase |
| montaje NFS "no route to host" | ganesha escucha en otra interfaz | `ss -ltnp \| grep 2049` y montar por la IP del tailnet |
| OSD lentos / disco lleno | los OSD son loop de 8 GiB | es una demo, no producción: tamaño a gusto |

## 4. Limpieza (si hay que repetir la clase desde cero)

```bash
sudo umount /mnt/cephfs /mnt/pgdata 2>/dev/null
sudo snap remove microceph              # en cada VM — borra todo el estado
```

---

## Lo que se lleva el estudiante (3 ideas)

1. **El contenedor es desechable; el dato, no** — y el dato vive en el clúster,
   no en "el disco del nodo" (Demo 2).
2. **Un clúster par es una trampa**: sin mayoría se congela todo (Demo 4). El
   quórum (N/2+1) es la matemática que evita el split-brain (Demo 5).
3. **Todo lo anterior es tráfico de red**: WireGuard, NFS 2049/TCP, latencia
   pagada al doble — elegir storage es diseñar red (Demo 3 y 6).
