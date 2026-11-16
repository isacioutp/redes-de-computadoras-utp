# GUÍA Y RÚBRICA DE EVALUACIÓN

## Cálculo y Despliegue de Recursos de Memoria y Procesos para Servicios en Producción
### Evaluación Práctica: Demo en Vivo (Instalación Nativa O Contenedores Docker)

---

## ÍNDICE DE CASOS DE ESTUDIO

1. **Caso de Estudio 01:** Nginx + PostgreSQL 16
2. **Caso de Estudio 02:** Apache HTTPD + MySQL 8.0
3. **Caso de Estudio 03:** Caddy + MariaDB 11
4. **Caso de Estudio 04:** HAProxy + Redis 7
5. **Caso de Estudio 05:** OpenResty + MongoDB 7
6. **Caso de Estudio 06:** Envoy + Cassandra 5
7. **Caso de Estudio 07:** Tengine + Elasticsearch 8
8. **Caso de Estudio 08:** LiteSpeed + ClickHouse

---

## MARCO DE EVALUACIÓN Y MODALIDAD DEL DEMO

Para la resolución y defensa práctica de todos los casos de estudio contenidos en este documento, se evalúan únicamente las capas de **RAM (Memoria)** y **CPU (Procesos/Workers)** bajo un **Escenario Único Intermedio**:

### 1. Especificación del Escenario Único Intermedio
- **Hardware Base:** 6 GB RAM | 3 vCPU.
- **Overhead Nativo:** 13.5% de la RAM total.
- **Overhead Docker:** 25.0% de la RAM total (incluye daemon, runtime y aislamiento de procesos).

### 2. Instrucciones para la Presentación (Demo en Vivo)
- **Modalidad Elegible:** El grupo o estudiante debe seleccionar y desplegar la arquitectura utilizando **UNA sola vía** (Instalación Nativa **O** Contenedores Docker).
- **Evidencia en Vivo:** Durante la defensa se deberá validar mediante comandos de consola (`htop`, `free -m`, `docker stats`, `ps aux`, etc.) que los límites de memoria, asignación de CPU y workers configurados en los archivos de servicio coinciden exactamente con los cálculos de la tabla.

---

---

# CASO DE ESTUDIO 01: Nginx + PostgreSQL 16

### 1. Contexto del Negocio
Plataforma e-commerce transaccional de alto tráfico expuesta a picos de ventas relámpago (*flash sales*).
- **Perfil de Tráfico:** Picos de 8,000 req/s con 15,000 usuarios concurrentes (duración media de sesión: 3 s).
- **Relación Lectura:Escritura:** 10:1.

### 2. Parámetros de Memoria y Procesos
- **Nativo (`memoria_web`):** 0.15 GB.
- **Docker (`mem_limit` Nginx):** 0.40 GB con 0.75 vCPU.
- **Parámetros PostgreSQL:** `max_connections` = 200; `work_mem` + `costo_por_conexion` = 3.5 MB; `margen` = 275 MB.

### 3. Entregables Solicitados

#### Tabla de Recursos (Seleccionar según la vía a presentar en el Demo)
| Parámetro / Recurso                                      | Vía Seleccionada (Nativo O Docker) |
| :------------------------------------------------------- | :--------------------------------- |
| **Arquitectura Elegida para el Demo**                    | [ ] Nativo / [ ] Docker            |
| **Overhead SO / Docker Daemon (GB)**                     |                                    |
| **RAM Libre para Servicios (GB)**                        |                                    |
| **`mem_limit` o RAM asignada a Nginx (GB)**              |                                    |
| **`mem_limit` o RAM asignada a PostgreSQL (GB)**         |                                    |
| **vCPUs asignadas a Nginx**                              |                                    |
| **vCPUs asignadas a PostgreSQL**                         |                                    |
| **Workers / hilos del servidor web**                     |                                    |
| **Conexiones sostenidas por worker**                     |                                    |
| **`shared_buffers` / Caché efectiva de PostgreSQL (GB)** |                                    |

#### Justificación Técnica
> *"Si durante una venta relámpago la concurrencia de conexiones a PostgreSQL alcanza el límite máximo y el host de 6 GB comienza a utilizar memoria de intercambio (swap) o activa el OOM Killer, ¿cuál es el componente que conviene ajustar o limitar primero: el número de conexiones en PostgreSQL, los worker_connections en Nginx, o la cuota de memoria en cgroups/Docker? Justifique analizando la interacción entre la memoria del sistema operativo y los procesos del servidor web y base de datos."*

---

---

# CASO DE ESTUDIO 02: Apache HTTPD + MySQL 8.0

### 1. Contexto del Negocio
Portal institucional y de noticias con gestión de contenidos (CMS) dinámicos y generación de páginas personalizadas por usuario.
- **Perfil de Tráfico:** Picos de 3,500 req/s con 8,000 usuarios concurrentes (duración media de sesión: 5 s).
- **Relación Lectura:Escritura:** 20:1.

### 2. Parámetros de Memoria y Procesos
- **Nativo (`memoria_web`):** 0.25 GB.
- **Docker (`mem_limit` Apache):** 0.50 GB con 1.0 vCPU.
- **Parámetros MySQL:** `max_connections` = 120; `costo_por_conexion` = 4.0 MB; `margen` = 275 MB.

### 3. Entregables Solicitados

#### Tabla de Recursos (Seleccionar según la vía a presentar en el Demo)
| Parámetro / Recurso                                          | Vía Seleccionada (Nativo O Docker) |
| :----------------------------------------------------------- | :--------------------------------- |
| **Arquitectura Elegida para el Demo**                        | [ ] Nativo / [ ] Docker            |
| **Overhead SO / Docker Daemon (GB)**                         |                                    |
| **RAM Libre para Servicios (GB)**                            |                                    |
| **`mem_limit` o RAM asignada a Apache (GB)**                 |                                    |
| **`mem_limit` o RAM asignada a MySQL (GB)**                  |                                    |
| **vCPUs asignadas a Apache**                                 |                                    |
| **vCPUs asignadas a MySQL**                                  |                                    |
| **Workers / hilos del servidor web**                         |                                    |
| **Conexiones sostenidas por worker**                         |                                    |
| **`innodb_buffer_pool_size` / Caché efectiva de MySQL (GB)** |                                    |

#### Justificación Técnica
> *"A diferencia de los servidores de eventos asíncronos, Apache HTTPD suele utilizar modelos basados en hilos/procesos (MPM event/worker/prefork). Analice el impacto en el consumo de memoria del host cuando Apache incrementa sus procesos activos para atender ráfagas de peticiones frente al tamaño fijado para el `innodb_buffer_pool_size` de MySQL."*

---

---

# CASO DE ESTUDIO 03: Caddy + MariaDB 11

### 1. Contexto del Negocio
Plataforma SaaS B2B multi-tenant que sirve a empresas cliente donde cada una posee su propio esquema lógico en la base de datos.
- **Perfil de Tráfico:** Picos de 5,000 req/s con 20,000 usuarios concurrentes (duración media de sesión: 4 s).
- **Relación Lectura:Escritura:** 30:1.

### 2. Parámetros de Memoria y Procesos
- **Nativo (`memoria_web`):** 0.125 GB.
- **Docker (`mem_limit` Caddy):** 0.3 GB con 0.75 vCPU.
- **Parámetros MariaDB:** `max_conexiones` = 150; `costo_por_conexion` = 2.5 MB; `margen` = 275 MB.

### 3. Entregables Solicitados

#### Tabla de Recursos (Seleccionar según la vía a presentar en el Demo)
| Parámetro / Recurso                           | Vía Seleccionada (Nativo O Docker) |
| :-------------------------------------------- | :--------------------------------- |
| **Arquitectura Elegida para el Demo**         | [ ] Nativo / [ ] Docker            |
| **Overhead SO / Docker Daemon (GB)**          |                                    |
| **RAM Libre para Servicios (GB)**             |                                    |
| **`mem_limit` o RAM asignada a Caddy (GB)**   |                                    |
| **`mem_limit` o RAM asignada a MariaDB (GB)** |                                    |
| **vCPUs asignadas a Caddy**                   |                                    |
| **vCPUs asignadas a MariaDB**                 |                                    |
| **Workers / hilos del servidor web**          |                                    |
| **Conexiones sostenidas por worker**          |                                    |
| **Caché efectiva de MariaDB (GB)**            |                                    |

#### Justificación Técnica
> *"Si este entorno multi-tenant experimenta degradación debido a la concurrencia de consultas e hilos activos en la memoria, ¿qué conviene ajustar o modificar primero: la asignación de RAM/workers para Caddy, los buffers de conexión/caché de MariaDB, o la separación de MariaDB a un nodo dedicado? Justifique desde la perspectiva de límites de memoria y planificación de hilos de CPU."*

---

---

# CASO DE ESTUDIO 04: HAProxy + Redis 7

### 1. Contexto del Negocio
Plataforma de juegos en línea que gestiona rankings en tiempo real, sesiones y estados con TTL.
- **Perfil de Tráfico:** 1,000,000 ops/s sostenidas con 50,000 jugadores concurrentes (duración media de sesión: 50 ms).
- **Relación Lectura:Escritura:** 50:1.

### 2. Parámetros de Memoria y Procesos
- **Nativo (`memoria_web`):** 0.20 GB.
- **Docker (`mem_limit` HAProxy):** 0.45 GB con 0.75 vCPU.
- **Parámetros Redis:** `max_conexiones` = 15,000; `costo_por_conexion` = 10 KB; `margen` = 275 MB.

### 3. Entregables Solicitados

#### Tabla de Recursos (Seleccionar según la vía a presentar en el Demo)
| Parámetro / Recurso                           | Vía Seleccionada (Nativo O Docker) |
| :-------------------------------------------- | :--------------------------------- |
| **Arquitectura Elegida para el Demo**         | [ ] Nativo / [ ] Docker            |
| **Overhead SO / Docker Daemon (GB)**          |                                    |
| **RAM Libre para Servicios (GB)**             |                                    |
| **`mem_limit` o RAM asignada a HAProxy (GB)** |                                    |
| **`mem_limit` o RAM asignada a Redis (GB)**   |                                    |
| **vCPUs asignadas a HAProxy**                 |                                    |
| **vCPUs asignadas a Redis**                   |                                    |
| **Workers / hilos del servidor web**          |                                    |
| **Conexiones sostenidas por worker**          |                                    |
| **Caché / Memoria efectiva de Redis (GB)**    |                                    |

#### Justificación Técnica
> *"Si las claves almacenadas en memoria exceden la RAM disponible asignada a Redis en este host de 6 GB, analice las implicaciones del uso de memoria al aplicar políticas de eviction (`allkeys-lru`) frente a `noeviction`, y evalúe si la adición de vCPUs al contenedor mejora la velocidad del hilo principal de procesamiento de Redis."*

---

---

# CASO DE ESTUDIO 05: OpenResty + MongoDB 7

### 1. Contexto del Negocio
Catálogo dinámico de productos e IoT que aloja millones de documentos con esquemas variables.
- **Perfil de Tráfico:** 5,000 req/s en pico con 10,000 usuarios concurrentes (duración media de sesión: 2 s).
- **Relación Lectura:Escritura:** 25:1.

### 2. Parámetros de Memoria y Procesos
- **Nativo (`memoria_web`):** 0.30 GB.
- **Docker (`mem_limit` OpenResty):** 0.75 GB con 1.0 vCPU.
- **Parámetros MongoDB:** `max_conexiones` = 150; `costo_por_conexion` = 4 MB; `margen` = 275 MB.

### 3. Entregables Solicitados

#### Tabla de Recursos (Seleccionar según la vía a presentar en el Demo)
| Parámetro / Recurso                             | Vía Seleccionada (Nativo O Docker) |
| :---------------------------------------------- | :--------------------------------- |
| **Arquitectura Elegida para el Demo**           | [ ] Nativo / [ ] Docker            |
| **Overhead SO / Docker Daemon (GB)**            |                                    |
| **RAM Libre para Servicios (GB)**               |                                    |
| **`mem_limit` o RAM asignada a OpenResty (GB)** |                                    |
| **`mem_limit` o RAM asignada a MongoDB (GB)**   |                                    |
| **vCPUs asignadas a OpenResty**                 |                                    |
| **vCPUs asignadas a MongoDB**                   |                                    |
| **Workers / hilos del servidor web**            |                                    |
| **Conexiones sostenidas por worker**            |                                    |
| **Caché efectiva de MongoDB (GB)**              |                                    |

#### Justificación Técnica
> *"Evalúe la distribución de RAM entre la caché en memoria de WiredTiger y la caché de respuesta compartida gestionada en Lua/OpenResty, considerando la carga de procesos por trabajador y el presupuesto de memoria remanente en el host."*

---

---

# CASO DE ESTUDIO 06: Envoy + Cassandra 5

### 1. Contexto del Negocio
Plataforma de telemetría IoT que procesa lecturas continuas de miles de sensores.
- **Perfil de Tráfico:** 50,000 escrituras/s sostenidas con 10,000 dispositivos concurrentes (duración media de sesión: 200 ms).
- **Relación Lectura:Escritura:** 1:1 (Write-heavy).

### 2. Parámetros de Memoria y Procesos
- **Nativo (`memoria_web`):** 0.25 GB.
- **Docker (`mem_limit` Envoy):** 0.60 GB con 0.75 vCPU.
- **Parámetros Cassandra:** `max_conexiones` = 150; `costo_por_conexion` = 3 MB; `margen` = 275 MB.

### 3. Entregables Solicitados

#### Tabla de Recursos (Seleccionar según la vía a presentar en el Demo)
| Parámetro / Recurso                             | Vía Seleccionada (Nativo O Docker) |
| :---------------------------------------------- | :--------------------------------- |
| **Arquitectura Elegida para el Demo**           | [ ] Nativo / [ ] Docker            |
| **Overhead SO / Docker Daemon (GB)**            |                                    |
| **RAM Libre para Servicios (GB)**               |                                    |
| **`mem_limit` o RAM asignada a Envoy (GB)**     |                                    |
| **`mem_limit` o RAM asignada a Cassandra (GB)** |                                    |
| **vCPUs asignadas a Envoy**                     |                                    |
| **vCPUs asignadas a Cassandra**                 |                                    |
| **Workers / hilos del servidor web**            |                                    |
| **Conexiones sostenidas por worker**            |                                    |
| **Caché efectiva de Cassandra (GB)**            |                                    |

#### Justificación Técnica
> *"En un contexto de alta tasa de escrituras entrantes, analice la competencia por CPU y memoria entre el procesamiento de eventos de Envoy y la gestión de Heap JVM / Memtables en Cassandra dentro de las restricciones del escenario de 6 GB RAM / 3 vCPU."*

---

---

# CASO DE ESTUDIO 07: Tengine + Elasticsearch 8

### 1. Contexto del Negocio
Plataforma de observabilidad que centraliza logs de microservicios y ofrece un motor de búsqueda rápida.
- **Perfil de Tráfico:** 3,000 consultas/s en pico con 5,000 usuarios concurrentes (duración media de sesión: 1 s).
- **Relación Lectura:Escritura:** 40:1.

### 2. Parámetros de Memoria y Procesos
- **Nativo (`memoria_web`):** 0.25 GB.
- **Docker (`mem_limit` Tengine):** 0.60 GB con 0.75 vCPU.
- **Parámetros Elasticsearch:** `max_conexiones` = 150; `costo_por_conexion` = 2 MB; `margen` = 275 MB.

### 3. Entregables Solicitados

#### Tabla de Recursos (Seleccionar según la vía a presentar en el Demo)
| Parámetro / Recurso                                 | Vía Seleccionada (Nativo O Docker) |
| :-------------------------------------------------- | :--------------------------------- |
| **Arquitectura Elegida para el Demo**               | [ ] Nativo / [ ] Docker            |
| **Overhead SO / Docker Daemon (GB)**                |                                    |
| **RAM Libre para Servicios (GB)**                   |                                    |
| **`mem_limit` o RAM asignada a Tengine (GB)**       |                                    |
| **`mem_limit` o RAM asignada a Elasticsearch (GB)** |                                    |
| **vCPUs asignadas a Tengine**                       |                                    |
| **vCPUs asignadas a Elasticsearch**                 |                                    |
| **Workers / hilos del servidor web**                |                                    |
| **Conexiones sostenidas por worker**                |                                    |
| **Caché efectiva de Elasticsearch (GB)**            |                                    |

#### Justificación Técnica
> *"Explique el impacto en la presión de memoria y pausa por Garbage Collection (GC) si se intenta dimensionar un Heap superior al 50% del total de RAM asignada a Elasticsearch, considerando la limitación estricta de memoria libre en este host."*

---

---

# CASO DE ESTUDIO 08: LiteSpeed + ClickHouse

### 1. Contexto del Negocio
Plataforma de analítica y BI que realiza consultas sobre volúmenes masivos de ventas e inventario.
- **Perfil de Tráfico:** 250 consultas/s con 2,000 analistas concurrentes (duración media de consulta: 8 s).
- **Relación Lectura:Escritura:** 100:1 (Sólo lectura analítica).

### 2. Parámetros de Memoria y Procesos
- **Nativo (`memoria_web`):** 0.20 GB.
- **Docker (`mem_limit` LiteSpeed):** 0.50 GB con 1.0 vCPU.
- **Parámetros ClickHouse:** `max_memory_usage` por query = 2 GB; `max_concurrent_queries` = 15; `costo_por_conexion_HTTP` = 5 MB; `margen` = 275 MB.

### 3. Entregables Solicitados

#### Tabla de Recursos (Seleccionar según la vía a presentar en el Demo)
| Parámetro / Recurso                              | Vía Seleccionada (Nativo O Docker) |
| :----------------------------------------------- | :--------------------------------- |
| **Arquitectura Elegida para el Demo**            | [ ] Nativo / [ ] Docker            |
| **Overhead SO / Docker Daemon (GB)**             |                                    |
| **RAM Libre para Servicios (GB)**                |                                    |
| **`mem_limit` o RAM asignada a LiteSpeed (GB)**  |                                    |
| **`mem_limit` o RAM asignada a ClickHouse (GB)** |                                    |
| **vCPUs asignadas a LiteSpeed**                  |                                    |
| **vCPUs asignadas a ClickHouse**                 |                                    |
| **Workers / hilos del servidor web**             |                                    |
| **Conexiones sostenidas por worker**             |                                    |
| **Consultas simultáneas (Ley de Little)**        |                                    |
| **RAM comprometida en queries (GB)**             |                                    |
| **Caché analítica de ClickHouse (GB)**           |                                    |
| **`max_concurrent_queries` real que cabe**       |                                    |

#### Justificación Técnica
> *"Considerando que la memoria física del host es de 6 GB, justifique por qué el parámetro `max_concurrent_queries` debe limitarse a nivel de ClickHouse en lugar de permitir que los hilos de ejecución saturen la memoria RAM total disponible."*

---

---

# RELACIÓN DEL CASO DE ESTUDIO CON EL PROYECTO SEMESTRAL

Este **Caso de Estudio es una versión reducida y simplificada (MVP / Piloto) del Proyecto Semestral**. 

Su propósito es validar que el grupo domina los fundamentos metodológicos, el dimensionamiento matemático de recursos y la capacidad de demostración en vivo a menor escala, como preparación previa a la arquitectura de mayor complejidad que defenderán en el Proyecto Semestral.

---

# RÚBRICA DE EVALUACIÓN GENERAL

| Criterio de Evaluación                           | Excelente (100%)                                             | Aceptable (70%)                                              | Deficiente (30%)                                             | No Realizado (0%)                                          |
| :----------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------- |
| **1. Precisión de Cálculos de Memoria (RAM)**    | Determina correctamente el overhead de la vía elegida (SO o Docker), la RAM libre y la asignación efectiva/caché para la base de datos sin errores numéricos. | Presenta pequeños errores de redondeo o cálculo en no más de 2 parámetros de RAM, pero la metodología general es coherente. | Errores significativos en el cálculo de la RAM disponible o confusión entre los modelos Nativo y Docker. | No completa las métricas de memoria en la tabla.           |
| **2. Planificación de Procesos y CPU**           | Calcula de manera precisa los workers del servidor web, las vCPUs asignadas y la distribución de conexiones sostenidas por trabajador para la vía elegida. | Asigna correctamente los workers pero comete errores en la distribución de conexiones por worker o asignación de vCPU. | No comprende la relación entre vCPUs asignadas y el número de workers/hilos generados por el servicio. | Omite los cálculos referentes a CPU y procesos.            |
| **3. Ejecución y Verificación del Demo en Vivo** | Muestra en vivo la infraestructura activa (Nativa o Docker) y demuestra mediante comandos CLI que la configuración real coincide exactamente con la tabla calculada. | El entorno funciona pero muestra discrepancias menores entre la configuración desplegada y los datos entregados en la tabla. | El servicio no levanta adecuadamente durante la demostración o presenta fallos severos de límites de recursos. | No presenta la demostración en vivo de la infraestructura. |
| **4. Rigor y Justificación Técnica**             | Argumenta de forma lógica la respuesta a la pregunta técnica, utilizando conceptos clave de arquitectura de sistemas (OOM Killer, GC, cgroups, hilos, evicción, etc.). | Responde a la pregunta técnica correctamente pero con argumentos genéricos o poca profundidad en la gestión de recursos del SO/Docker. | La justificación es errónea, contradictoria con los datos de la tabla o carece de fundamento técnico en sistemas operativos. | No responde a la pregunta de justificación técnica.        |
| **5. Formato y Presentación**                    | Mantiene la estructura tabular completa, especificando claramente la vía elegida (Nativo/Docker) con unidades claras (GB, MB, vCPUs, workers). | Completa la tabla pero omite unidades en algunas celdas o presenta descuidos menores de formato. | Presenta datos desordenados, tablas incompletas o altera la estructura requerida. | No entrega el trabajo en el formato solicitado.            |