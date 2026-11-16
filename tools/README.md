# Herramientas (`tools/`)

Scripts para **generar y mantener** las presentaciones de la Unidad III y su
documentación (versiones en texto). Todo se hace sin abrir PowerPoint.

## Requisitos

- Python 3.
- [`python-pptx`](https://python-pptx.readthedocs.io/): `pip install python-pptx`.

## Scripts

| Script | Qué hace | Cómo se usa |
|--------|----------|-------------|
| `ppt_kit.py` | **Kit de diseño**: tokens de color, portada, separador, encabezado, tabla, bloque de código, callouts, flujos y notas. No se ejecuta solo; lo importan los `build_*`. | (librería) |
| `build_parte1.py` | Genera `Teoria-U3-Parte1-LAN-Monitoreo.pptx` (**18** diapositivas). | `python3 tools/build_parte1.py` |
| `build_parte2.py` | Genera `Teoria-U3-Parte2-SSH-Bastion.pptx` (**13**). | `python3 tools/build_parte2.py` |
| `build_parte3.py` | Genera `Teoria-U3-Parte3-Orquestacion.pptx` (**12**). | `python3 tools/build_parte3.py` |
| `build_parte4.py` | Genera `Teoria-U3-Parte4-Almacenamiento-Compartido.pptx` (**15**). | `python3 tools/build_parte4.py` |
| `build_devops.py` | Genera `Teoria-DevOps-Despliegue.pptx` (**16**): sesión de cierre — qué es DevOps, el caso del viernes, el pipeline y su tráfico, rollback y DORA. | `python3 tools/build_devops.py` |
| `check_layout.py` | **Validador de layout**: estima si el texto o las tablas se desbordan y detecta cajas fuera del lienzo. | `python3 tools/check_layout.py Teoria-U3-Parte*.pptx` |
| `dump_ppt_md.py` | **Volcado a Markdown**: título + índice + cada diapositiva (tablas, código, negritas) + notas del orador en bloques plegables. | `python3 tools/dump_ppt_md.py <pptx> "<título>"` |

## Flujo de trabajo

1. Editar el `build_*.py` correspondiente (el contenido vive en el script).
2. Regenerar el `.pptx`.
3. Validar el layout.
4. Regenerar la versión `.md` de teoría.

```bash
# 1-2 · Regenerar las presentaciones de la Unidad III
python3 tools/build_parte1.py
python3 tools/build_parte2.py
python3 tools/build_parte3.py
python3 tools/build_parte4.py
python3 tools/build_devops.py

# 3 · Validar el layout (sin abrir PowerPoint)
python3 tools/check_layout.py \
  Teoria-U3-Parte1-LAN-Monitoreo.pptx \
  Teoria-U3-Parte2-SSH-Bastion.pptx \
  Teoria-U3-Parte3-Orquestacion.pptx \
  Teoria-U3-Parte4-Almacenamiento-Compartido.pptx \
  Teoria-DevOps-Despliegue.pptx

# 4 · Regenerar las versiones en texto (TEORIA-U3-*.md)
python3 tools/dump_ppt_md.py Teoria-U3-Parte1-LAN-Monitoreo.pptx \
  "Unidad III · Parte 1: LAN y monitoreo" > TEORIA-U3-Parte1-LAN-Monitoreo.md
python3 tools/dump_ppt_md.py Teoria-U3-Parte2-SSH-Bastion.pptx \
  "Unidad III · Parte 2: Claves SSH y servidores bastión" > TEORIA-U3-Parte2-SSH-Bastion.md
python3 tools/dump_ppt_md.py Teoria-U3-Parte3-Orquestacion.pptx \
  "Unidad III · Parte 3: Orquestación de servicios con Docker" > TEORIA-U3-Parte3-Orquestacion.md
python3 tools/dump_ppt_md.py Teoria-U3-Parte4-Almacenamiento-Compartido.pptx \
  "Unidad III · Parte 4: Almacenamiento compartido para alta disponibilidad" > TEORIA-U3-Parte4-Almacenamiento-Compartido.md
python3 tools/dump_ppt_md.py Teoria-DevOps-Despliegue.pptx \
  "Unidad III · Sesión de cierre: DevOps sobre la red" > TEORIA-DEVOPS-DESPLIEGUE.md
```

## Notas

- **Fuente de verdad:** el contenido de cada presentación está en su `build_*.py`;
  el `.pptx` y el `TEORIA-*.md` son **salidas generadas**. No se editan a mano.
- **`check_layout.py` es una estimación** (cuenta caracteres por línea), pensada
  para trabajar cuando no se puede ver el render. No reemplaza abrir la
  presentación, pero atrapa los desbordes más comunes.
- **Pie de página y estilo:** los define `ppt_kit.py` (`FOOT`, colores, Calibri +
  Consolas). Al cambiar un token, todas las partes cambian a la vez.
- **Repositorio anidado:** el laboratorio `laboratorio-enruntamiento-vlan/` trae su
  propio `tools/` (`build_teoria_lab.py`, `dump_ppt_md.py`) porque es un
  **repositorio Git anidado**; no se mezcla con estos scripts.
- No se versiona `__pycache__/` (ver `.gitignore`).
