# Laboratorio N.° 7 — Direccionamiento IP y Subredes

Tema 2.7 · Semana 9 · Unidad II · 2 clases
**Alimenta el Avance N.º 1 del Proyecto Semestral (diagrama + direccionamiento IP).**

## Objetivo general

Comprender el direccionamiento IP, las máscaras de red, el subneteo (CIDR) y
los protocolos de apoyo **ARP, DHCP e ICMP**, implementando múltiples subredes
reales con Docker y aplicando el diseño a un escenario de proyecto de software.

## Contexto teórico

### El datagrama IP (capa de red)

```
┌────────┬────────┬──────────┬──────────┬──────────┬──────────┐
│Versión │  IHL   │ TOS      │ Longitud total          │ Frag    │
├────────┴────────┴──────────┴──────────┴──────────┴──────────┤
│ TTL   │ Protocolo │ Checksum │                             │
├─────────────────────────────────────────┬───────────────────┤
│ IP origen (4 bytes)                     │ IP destino (4)    │
├─────────────────────────────────────────┴───────────────────┤
│ Opciones (opcional)                                        │
└─────────────────────────────────────────────────────────────┘
```

### Direccionamiento IPv4 y máscara

- **IPv4**: 32 bits, se escribe en 4 octetos: `192.168.1.10`
- **Máscara**: indica qué parte es **red** y qué parte es **host**.
  - `255.255.255.0` = `/24` → 24 bits de red, 8 bits de host.
- **Prefijo CIDR**: `/24`, `/26`, `/30` → es la forma moderna de escribir la máscara.

### Clases de dirección (legacy, para entender IPv4)

| Clase | 1er octeto | Defecto | Uso |
|-------|------------|---------|-----|
| A | 1–126 | /8 | Redes muy grandes |
| B | 128–191 | /16 | Redes medianas |
| C | 192–223 | /24 | Redes pequeñas (la más común en LAN) |
| D | 224–239 | — | Multicast |
| E | 240–255 | — | Experimental |

### Direcciones privadas (RFC 1918)

| Rango | Clase |
|-------|-------|
| 10.0.0.0/8 | A |
| 172.16.0.0/12 | B |
| 192.168.0.0/16 | C |

### Subneteo y CIDR

Dividir una red en subredes:

```
192.168.1.0/24
├── Subred 1: 192.168.1.0/26  → hosts 1-62   (máscara 255.255.255.192)
├── Subred 2: 192.168.1.64/26 → hosts 65-126
├── Subred 3: 192.168.1.128/26→ hosts 129-190
└── Subred 4: 192.168.1.192/26→ hosts 193-254
```

Cálculos clave para cada subred:
- **Dirección de red** (primera, hosts todos en 0)
- **Broadcast** (última, hosts todos en 1) — no asignable
- **Gateway** (dirección del router, típicamente la 1ª asignable)
- **Nº de hosts útiles** = 2^(32-prefijo) − 2

### Protocolos de apoyo

| Protocolo | Sigla | Función | Transporte |
|-----------|-------|---------|------------|
| ARP | Address Resolution Protocol | IP → MAC | L2 (broadcast) |
| DHCP | Dynamic Host Configuration Protocol | Asigna IP/máscara/gateway | UDP 67/68 |
| ICMP | Internet Control Message Protocol | Diagnóstico y errores | L3 directo |
| BOOTP | Bootstrap Protocol | Antecesor del DHCP | UDP 67/68 |

## Materiales y requisitos

- Docker instalado.
- Calculadora de subredes (opcional): `ipcalc` local o online.
- Acceso a internet.

## Cómo se trabaja esta semana

Dos clases en la misma semana. La **Sesión A** construye el esquema de subredes
con Docker; la **Sesión B** agrega enrutamiento, DHCP y redacta el esquema VLSM
del proyecto semestral.

| Sesión | Contenido | Entregable breve | Guía |
|--------|-----------|------------------|------|
| Sesión A — Direcciones IP y subneteo VLSM con Docker | Parte 1 (direccionamiento IP básico: srv1/srv2 e ipcalc) y Parte 2 (subneteo y subredes reales con `docker network create`). | IPs de srv1/srv2, `ipcalc`, subredes creadas, tabla de asignación, respuestas 1–5. | [Sesión A](SESION-A.md) |
| Sesión B — ICMP, enrutamiento, DHCP y el esquema del proyecto | Parte 3 (ICMP y router contenedor), Parte 4 (DHCP con dnsmasq y ARP) y Parte 5 (esquema VLSM del proyecto + `docker-compose.yml`). | Pings fallido/exitoso, traceroute, DHCP/ARP, esquema VLSM del proyecto, compose final, respuestas 1–9. | [Sesión B](SESION-B.md) |

## Rúbrica global

Cada sesión suma **50 puntos**; ambas juntas conforman la calificación total de
la semana (**100 puntos**).

| Criterio | Puntos |
|----------|--------|
| Sesión A — Direcciones IP y subneteo VLSM con Docker | 50 |
| Sesión B — ICMP, enrutamiento, DHCP y el esquema del proyecto | 50 |
| **Total** | **100** |

## Limpieza

```bash
docker rm -f srv1 srv2 web-front api-backend db-main admin-pc router-lab7 dhcp-srv dhcp-client
docker network rm lab7-red frontend backend dbsub admin linknet dhcp-lab
docker compose -f docker-compose.yml down --remove-orphans
```