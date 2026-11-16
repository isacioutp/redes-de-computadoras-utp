# Diagramas del Laboratorio N.º 14 (Mermaid para draw.io)

Topología de Packet Tracer, arquitectura de Docker Compose y flujos del
laboratorio, listos para insertar en **draw.io**.

## Cómo usarlos en draw.io

1. Abre draw.io (diagram.net) → **Arrange > Insert > Mermaid** (o el botón `+`).
2. Copia el bloque `mermaid` y pégalo en el cuadro de texto.
3. Deja la opción **Diagram** (formas editables) o **Image** (SVG único).
4. Clic en **Insert**.

> Si el parser falla, borra las líneas `classDef`/`class`: son solo estilo.

---

## 1. Topología física — Packet Tracer (el perímetro)

```mermaid
flowchart TB
  NET["☁ Internet / ISP"]

  subgraph PER["Perímetro (público) · 10.10.10.0/24"]
    R1["R1 · Router + ACL<br/>G0/1: 10.10.10.1"]
    SW["SW · 2960"]
    BAST["srv-bastion (dual-homed)<br/>Fa0: 10.10.10.2"]
    PC["PC-admin<br/>10.10.10.10"]
  end

  subgraph INT["Red interna · 10.20.20.0/24 (sin ruta a Internet)"]
    SRVI["srv-interno<br/>10.20.20.10"]
  end

  NET --- R1
  R1 --- SW
  SW --- BAST
  SW --- PC
  BAST -- "Fa1: 10.20.20.2" --- SRVI

  classDef per fill:#e3f2fd,stroke:#1565c0;
  classDef int fill:#ffebee,stroke:#c62828;
  class R1,SW,BAST,PC per;
  class SRVI int;
```

**Lectura:** el bastión es el **único** equipo con pie en las dos redes. No hay
ruta directa PC → srv-interno: hay que pasar por el bastión (doble salto SSH).

---

## 2. Arquitectura del stack — Docker Compose (el data center)

```mermaid
flowchart TB
  HOST["🖥 Host = bastión real<br/>(solo SSH con llave)"]

  subgraph FRONT["red front · 172.28.10.0/24"]
    WEB["web (nginx)<br/>172.28.10.10<br/>:8080 publicado"]
    API1["api réplica 1<br/>172.28.10.20"]
    API2["api réplica 2"]
    DNS["dns-corp (dnsmasq)<br/>172.28.10.53"]
    MON["netdata<br/>:19999 (opcional)"]
  end

  subgraph BACK["red back · 172.28.20.0/24 (internal: true)"]
    API3["api (2ª interfaz)"]
    DB["db (postgres)<br/>172.28.20.20<br/>SIN puertos publicados"]
  end

  HOST -. "ssh -i llave" .-> WEB
  WEB --> API1
  WEB --> API2
  API1 --> API3
  API2 --> API3
  API3 --> DB
  DNS -. resuelve .-> WEB
  DNS -. resuelve .-> API1
  DNS -. resuelve .-> DB
  MON -. observa .-> FRONT

  classDef front fill:#e8f5e9,stroke:#2e7d32;
  classDef back fill:#ffebee,stroke:#c62828;
  class WEB,API1,API2,DNS,MON front;
  class API3,DB back;
```

**Lectura:** el API es el único "puente" front↔back. La DB vive **solo** en
`back` (interna) y no publica puertos: es inalcanzable desde el host.

---

## 3. Flujo de un paquete (comparación de lupas)

```mermaid
sequenceDiagram
  participant U as Usuario (navegador)
  participant H as Host (NAT)
  participant W as web (nginx)
  participant A as api
  participant D as db (postgres)

  U->>H: HTTP :8080
  H->>W: reenvío al contenedor (docker-proxy)
  W->>A: GET /ping (red front, DNS api.local)
  A->>D: SELECT ... (red back, solo si es el API)
  D-->>A: filas
  A-->>W: JSON
  W-->>H: 200 OK
  H-->>U: respuesta

  Note over D: la DB nunca es alcanzable<br/>directamente desde U ni desde el host
```

**En Packet Tracer** este mismo flujo se ve paquete a paquete en **Simulation
mode** (PDU por salto, con ACL evaluada en R1). En Docker se ve con
`tcpdump -i br-front` (la lupa cambia, el paquete es el mismo).

---

## 4. Acceso por SSH al bastión (el host)

```mermaid
sequenceDiagram
  participant Admin as Administrador (llave privada)
  participant Bast as Host-bastión (sshd, PasswordAuthentication no)
  participant Doc as Contenedores (redes Docker internas)

  Admin->>Bast: ssh -i id_lab14 usuario@host (puerto 22)
  Bast->>Admin: desafío firmado → acceso SIN contraseña
  Admin->>Bast: desde el host, alcanzo las redes internas
  Bast->>Doc: docker exec / ssh a servicios internos

  Note over Admin,Bast: La contraseña está deshabilitada:<br/>solo la llave entra.
```

---

## 5. Ciclo de vida orquestado (Compose)

```mermaid
flowchart LR
  CODE["docker-compose.yml<br/>(estado deseado)"] --> UP["docker compose up -d --wait"]
  UP --> RUN["Stack corriendo<br/>web + api×2 + db (healthy)"]
  RUN --> SCALE["--scale api=2"]
  RUN --> HEAL["healthcheck falla →<br/>restart automático"]
  RUN --> DOWN["docker compose down"]
  DOWN -->|conserva volúmenes| RUN
  DOWN -->|con -v borra datos| CODE

  classDef ok fill:#e8f5e9,stroke:#2e7d32;
  class RUN,SCALE,HEAL ok;
```

---

## 6. Mapa de la asignatura dentro del laboratorio

```mermaid
flowchart TB
  L10["Lab 10 — LAN + monitoreo"] --> L14
  L11["Lab 11 — SSH + bastión"] --> L14
  L12["Lab 12 — Compose/Swarm"] --> L14
  L14["Lab 14 (integrador)<br/>PT + Compose, sin Swarm"]
  L14 --> AV2["Proyecto: Avance 2<br/>(LAN + acceso + monitoreo)"]
  L14 --> FIN["Proyecto: Proyecto Final<br/>(orquestación con Compose)"]

  classDef old fill:#eceff1,stroke:#607d8b;
  classDef new fill:#fff8e1,stroke:#f9a825;
  class L10,L11,L12 old;
  class L14,AV2,FIN new;
```
