# CP3 — VLM + Dashcam: IA que razona sobre conducción

> Caso práctico 3 del módulo "IA Aplicada al Vehículo Autónomo"
> Máster en IA · AIC × Universidad de Monterrey · 2026

---

## Lo que vas a hacer

Cargar un **VLM (Vision-Language Model) pequeño local** — **Moondream2 ~1.9B** — y aplicarlo a 18 imágenes dashcam curadas en 6 categorías (trivial, urbano, edge case visual, edge case semántico, trampa, ambigua). Descubrir **dónde el VLM brilla** y **dónde alucina**.

Es el **caso diferenciador del módulo** — ninguna otra formación de IA general te hace tocar este paradigma aplicado a conducción.

**Duración estimada**: 30–45 min · **Sin GPU** · 8 GB RAM (Moondream2 en INT4 ~2 GB).

---

## Por qué este CP

P6 (bloque 2) explicó:
- Los VLMs pueden razonar sobre escenas — pero alucinan.
- Latencia ~100-1000 ms — no aptos para closed-loop control 30 FPS.
- Útiles para **auto-labeling** (P5) y **HMI explicativo** (Wayve LINGO).

Aquí lo experimentas. La pregunta del lab: **¿dónde encaja realmente un VLM en el stack?**

**Decisión 2026-05-27**: usamos modelo **local en CPU** (no API) por:
- Cero coste, 100% reproducible offline.
- El contraste local-pequeño vs frontier-API se discute conceptualmente en notebook 07.

---

## Estructura

```
CP3-vlm-dashcam/
├── README.md                              ← estás aquí
├── requirements.txt
├── rubrica.md
├── datasets/
│   ├── README.md
│   └── dashcam-curated/                   ← 18 imágenes + expected descriptions
├── notebooks/
│   ├── 01_introduccion.md
│   ├── 02_setup.ipynb                     ← cargar Moondream2 desde HF
│   ├── 03_descripcion_basica.ipynb        ← describir las 18 imágenes
│   ├── 04_tareas_estructuradas.ipynb      ← objetos críticos + risk score + acción
│   ├── 05_consistencia.ipynb              ← greedy vs sampling
│   ├── 06_failure_analysis.ipynb          ← categorizar fallos
│   └── 07_local_vs_frontier.md            ← mini-ensayo
├── scripts/
│   └── download_dataset.py                ← curado público dashcam
└── soluciones/                            ← referencia profesor
```

---

## Requisitos previos

- Python 3.10+
- 8 GB RAM (Moondream2 FP16 ~3.8 GB, INT4 ~2 GB).
- Sin GPU (todo CPU).
- Conexión a internet **la primera vez** (descarga ~3.7 GB de Moondream2).

---

## Setup paso a paso

### 1. Entorno virtual

```bash
cd CP3-vlm-dashcam
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Dataset

```bash
python scripts/download_dataset.py
```

Descarga ~18 imágenes dashcam públicas (Wikimedia Commons, CC) y prepara la estructura. ~5 MB.

### 3. Carga del modelo (primera vez)

```bash
jupyter notebook notebooks/02_setup.ipynb
```

La primera ejecución **descarga Moondream2** (~3.7 GB) y lo cachea en `~/.cache/huggingface/`. Sesiones siguientes no tocan red.

Al final debe imprimir `✅ Setup OK — listo para 03`.

---

## Orden recomendado

| Notebook | Tiempo | Qué hace |
|----------|--------|----------|
| `02_setup` | 5-10 min (1ª vez, descarga modelo) / <1 min (siguientes) | Cargar Moondream2 + test |
| `03_descripcion_basica` | 5 min | Describir 18 imágenes + comparar con expected |
| `04_tareas_estructuradas` | 6 min | Objetos críticos + risk score + acción recomendada |
| `05_consistencia` | 4 min | Greedy vs sampling — variabilidad |
| `06_failure_analysis` | 8 min | Categorizar tipos de fallo |
| `07_local_vs_frontier` (md) | 10 min | Mini-ensayo: rol del VLM en sistema real |

**Total**: ~30-40 min activos (más descarga inicial).

---

## Entregable

PDF con:

1. **3 imágenes** con descripción de Moondream + expected_description + tu análisis del gap.
2. **Tabla risk score** por imagen (objetos críticos + grav + acción).
3. **Análisis de consistencia**: ¿el modelo es determinista con greedy? ¿variable con sampling?
4. **Categorización de fallos** (omisión, alucinación, error de localización...) con ≥3 ejemplos.
5. **Mini-ensayo** de `07_local_vs_frontier.md`: dónde encaja un VLM (local vs frontier) en el stack real.
6. (Opcional) Extensiones.

**Subir a**: Moodle de AIC, sección "CP3". Nombre: `cp3_<apellido>_<nombre>.pdf`. Plazo 48 h.

Eval: [rúbrica](rubrica.md). Máximo 16 pts.

---

## FAQ

**¿Por qué Moondream2 y no Claude/GPT-4V?**
- Cero coste, 100% reproducible offline (cualquier alumno puede correrlo).
- Lección añadida: ver las limitaciones de **modelos pequeños** — útil para entender qué falta en frontier.
- Discusión conceptual en notebook 07.

**¿Y si quiero usar Claude o GPT-4V como extensión?**
Bienvenido. El notebook 07 explica cómo swapear con tu propia key.

**¿Por qué solo 18 imágenes?**
- Latencia CPU: 3-6 s/imagen × 18 = ~1-2 min total por ronda.
- Más imágenes = más espera en sesión. 18 es **suficiente** para los 6 tipos de categoría.

**Conexión con P5 y P6**:
- **P5**: VLM como auto-labeler.
- **P6**: VLM como razonador de escena + HMI + VLA.
