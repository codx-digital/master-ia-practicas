# CP2 — Profundidad Monocular con Foundation Models

> Caso práctico 2 del módulo "IA Aplicada al Vehículo Autónomo"
> Máster en IA · AIC × Universidad de Monterrey · 2026

---

## Lo que vas a hacer

Aplicar **dos foundation models de profundidad** a las mismas imágenes que usaste en CP1, descubrir dónde acuden y dónde fallan, y entender la distinción crítica entre **profundidad relativa** y **profundidad métrica** en un sistema real.

1. **MiDaS small** (Intel) — la referencia clásica de foundation depth.
2. **Depth Anything v2 small** — el SOTA 2024 que ha desplazado a MiDaS.

Y vas a contestar una pregunta concreta: **¿puede esto sustituir a un LiDAR?** (Spoiler: depende, y por eso este CP es interesante.)

**Duración estimada**: 30–45 min · **Sin GPU** · 8 GB RAM mínimo.

---

## Por qué este CP

P2 (bloque 4) explicó:
- Tesla apuesta camera-only → necesita 3D sin LiDAR.
- Foundation models 2024–2026 (MiDaS, Depth Anything v2, ZoeDepth) lo hacen viable.
- Profundidad relativa vs métrica es **la distinción clave** que mucha gente no conoce.

Aquí lo tocas en código. Sin entrenar nada. Foundation model = "cargar y aplicar".

---

## Estructura del caso

```
CP2-midas/
├── README.md                              ← estás aquí
├── requirements.txt
├── rubrica.md
├── datasets/
│   ├── README.md                          ← qué imágenes usamos y de dónde
│   └── cp2-depth-extras/                  ← 5–7 imágenes "depth challenge" (descargadas por script)
├── notebooks/
│   ├── 01_introduccion.md
│   ├── 02_setup.ipynb                     ← verifica entorno + descarga modelos HF
│   ├── 03_midas_basico.ipynb              ← MiDaS sobre las 14 + 7 imágenes
│   ├── 04_relativa_vs_metrica.ipynb       ← inverse depth + calibración naïve
│   ├── 05_depth_anything_v2.ipynb         ← comparativa con DA v2
│   ├── 06_failure_modes.ipynb             ← dónde mienten los modelos
│   └── 07_preguntas.md                    ← entregable
├── scripts/
│   └── download_assets.py                 ← imágenes extras (modelos los baja transformers)
└── soluciones/                            ← referencia profesor
```

---

## Requisitos previos

- Python 3.10+
- 8 GB RAM (Depth Anything v2 small llega a usar ~1.5 GB en inferencia)
- Sin GPU
- Conexión a internet **la primera vez** (para descargar modelos desde HuggingFace ~50 MB total)

**Prerequisito CP1**: necesitas las imágenes de CP1 ya descargadas (`../CP1-carriles/datasets/lanes-subset/`). Si no las tienes:

```bash
cd ../CP1-carriles
python scripts/download_assets.py --dataset-only
cd -
```

---

## Setup paso a paso

### 1. Entorno virtual y dependencias

```bash
cd CP2-midas
python -m venv .venv
source .venv/bin/activate                  # macOS/Linux
# .venv\Scripts\activate                   # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Descarga imágenes "depth challenge" extras

```bash
python scripts/download_assets.py
```

Esto descarga ~7 imágenes públicas (Wikimedia Commons, CC) que estresan los modelos de profundidad: reflejos, túneles, cielo plano, escena nocturna. ~5 MB.

### 3. Modelos (se bajan automáticamente al primer uso)

Los modelos viven en HuggingFace Hub. La **primera ejecución** del notebook `02_setup.ipynb` descarga ~50 MB y los cachea en `~/.cache/huggingface/`. Sesiones siguientes no tocan red.

```bash
jupyter notebook notebooks/02_setup.ipynb
```

Si todo OK, imprime `✅ Setup OK — listo para 03`.

---

## Orden recomendado

| Notebook | Tiempo | Qué hace |
|----------|--------|----------|
| `02_setup` | 2 min (15 s warmup + descarga modelos primera vez) | Carga MiDaS + DA v2, test rápido |
| `03_midas_basico` | 8 min | Pipeline completo MiDaS + visualización + timing |
| `04_relativa_vs_metrica` | 8 min | La distinción crítica + calibración naïve |
| `05_depth_anything_v2` | 8 min | Mismo workflow con DA v2 + comparativa |
| `06_failure_modes` | 10 min | Imágenes "trampa", razonar por qué falla |
| `07_preguntas` (markdown) | 10 min | Responder 5 preguntas guiadas |

**Total**: ~45 min activos. Date margen para imprevistos.

---

## Entregable

Un único PDF (o markdown con plots embebidos) con:

1. Resultado de MiDaS sobre 5 imágenes representativas (depth map en color + overlay).
2. Idem para Depth Anything v2.
3. Comparativa visual lado a lado + **1 imagen donde discrepan claramente** (con tu interpretación).
4. Respuestas a las 5 preguntas de `07_preguntas.md`.
5. Si hiciste alguna **extensión opcional**, descríbela.

**Subir a**: el **Moodle de AIC** (sección "CP2 — Profundidad"). Nombre: `cp2_<apellido>_<nombre>.pdf`.

Se evalúa con la [rúbrica](rubrica.md). Máximo 16 pts.

---

## FAQ rápido

**¿Puedo usar GPU si tengo?**
Sí. Los notebooks detectan CUDA y la usan automáticamente. Pero **todo está validado en CPU** — si los tiempos te dan muy distintos del syllabus, posiblemente estés en GPU sin darte cuenta.

**¿Por qué no usar el MiDaS original (`isl-org/MiDaS`)?**
Lo usamos via `transformers` (`Intel/dpt-swinv2-tiny-256`), que es la versión empaquetada por Intel + HF — más fácil de cargar, misma calidad para "small". Los puristas pueden swapear al original.

**¿Y Depth Anything v3?**
A fecha de producción del módulo (2026-05), v2 es lo último estable público. Si sale v3 antes de impartir, **adaptar el notebook** (cambio de model ID, mismo workflow).

**¿Cuándo se publica la solución?**
En `soluciones/`. **No abrir hasta haber intentado el caso completo** — el análisis crítico es lo que cuenta en la rúbrica.
