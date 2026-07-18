# CP1 — Detección de Carriles: Clásico vs Deep Learning

> Caso práctico 1 del módulo "IA Aplicada al Vehículo Autónomo"
> Máster en IA · AIC × Universidad de Monterrey · 2026

---

## Lo que vas a hacer

Vas a implementar **dos detectores de carriles** sobre las mismas imágenes y compararlos:

1. **Enfoque clásico**: Canny + Hough Transform (CV de los 90s, sin ML)
2. **Enfoque deep learning**: CNN pre-entrenada (Ultra-Fast-Lane-Detection v2)

Y vas a responder a una pregunta concreta: **¿en qué casos gana cada uno?**

**Duración estimada**: 45–60 min · **Sin GPU** · 8 GB RAM suficiente.

---

## Estructura del caso

```
CP1-carriles/
├── README.md                          ← estás aquí
├── requirements.txt                   ← dependencias Python
├── rubrica.md                         ← cómo se evalúa
├── datasets/
│   ├── README.md                      ← cómo obtener las imágenes
│   └── lanes-subset/                  ← imágenes pre-empaquetadas
├── notebooks/
│   ├── 01_setup.ipynb                 ← verifica entorno y dataset
│   ├── 02_clasico_canny_hough.ipynb   ← implementa pipeline clásico
│   ├── 03_deep_learning.ipynb         ← aplica modelo pre-entrenado
│   ├── 04_comparativa.ipynb           ← compara ambos
│   └── 05_preguntas.md                ← preguntas a responder en el entregable
└── soluciones/                        ← referencias (no abrir hasta intentarlo)
```

---

## Requisitos previos

- Python 3.10+
- 8 GB RAM
- Sin GPU
- Conexión a internet **solo** para instalar dependencias y descargar pesos del modelo (puedes hacerlo antes de la sesión)

**Conocimiento esperado** (cubierto en P1+P2 del módulo):
- Conceptos básicos de CV (gradientes, edges, espacios de color)
- CNN básica (no se entrena modelos en este CP)
- PyTorch a nivel "cargar y usar modelo pre-entrenado"

---

## Setup paso a paso

### 1. Clona/descarga este caso

Asume que ya tienes esta carpeta `CP1-carriles/` en tu máquina.

### 2. Crea un entorno virtual

```bash
cd CP1-carriles
python -m venv .venv
source .venv/bin/activate         # macOS/Linux
# .venv\Scripts\activate          # Windows
```

### 3. Instala dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Esto instala PyTorch CPU (no CUDA), OpenCV, numpy, matplotlib y dependencias del modelo DL.

> **Si estás en Apple Silicon (M1/M2/M3)**: el `requirements.txt` ya pinea las versiones compatibles. Si ves errores con OpenCV, prueba `pip install opencv-python-headless` en lugar de `opencv-python`.

### 4. Descarga el dataset y los pesos del modelo

```bash
python scripts/download_assets.py
```

Esto descarga (desde el GitHub Release `cp1-v1` del repo del módulo):
- 14 imágenes de carreteras (~10 MB, subset curado de Udacity CarND — MIT)
- Pesos del modelo U-Net depthwise (~17 MB ONNX, entrenado sobre BDD100K — MIT)

> **Repo privado**: el script usa `gh release download` por debajo, así que necesitas `gh auth login` antes (o exportar `GITHUB_TOKEN`).

Si la descarga falla, revisa [datasets/README.md](datasets/README.md) para fallback manual (URLs directas a los assets de la release).

### 5. Verifica el entorno

```bash
jupyter notebook notebooks/01_setup.ipynb
```

Ejecuta todas las celdas. Al final debe imprimir `✅ Setup OK — listo para 02`.

---

## Orden recomendado

| Notebook | Tiempo | Qué hace |
|----------|--------|----------|
| `01_setup` | 5 min | Verifica que todo está instalado y descargado |
| `02_clasico_canny_hough` | 15 min | Implementas el pipeline clásico paso a paso |
| `03_deep_learning` | 10 min | Cargas modelo y aplicas a las mismas imágenes |
| `04_comparativa` | 10 min | Grid visual + tabla de resultados |
| `05_preguntas` (markdown) | 10 min | Responder las preguntas guiadas |

**Total**: ~50 min activos. Date margen para imprevistos.

---

## Entregable

Al terminar entregas un **único PDF** (o markdown con plots embebidos) con:

1. Resultados de tu mejor configuración del clásico (5 imágenes representativas con overlay).
2. Resultados del DL en las mismas 5 imágenes.
3. Tabla comparativa (tiempo de inferencia, % éxito subjetivo, observaciones).
4. **Respuestas a las 5 preguntas de `05_preguntas.md`** (1–2 párrafos cada una).
5. Si hiciste alguna **extensión opcional** del syllabus, descríbela.

**Subir a**: el **Moodle de AIC** (curso del Máster IA, sección "CP1 — Carriles"). Formato del archivo: `cp1_<apellido>_<nombre>.pdf`.

Se evalúa con la [rúbrica](rubrica.md). Máximo 16 pts.

---

## Soporte durante la sesión

- **Durante la sesión en directo**: foro del Moodle del Máster (hilo "CP1 — Carriles") o canal que comunique el coordinador.
- Tras la sesión, dudas en el mismo foro — respuesta en 24h.
- Si tu notebook tarda >10 min en una celda, **para**, lee el mensaje "tiempos esperados" del notebook, y pregunta. Algo está mal.

---

## FAQ rápido

**¿Puedo usar GPU si tengo?**
Sí, pero todo está validado en CPU. Si usas GPU asegúrate de que tu PyTorch detecta CUDA (`torch.cuda.is_available()`).

**¿Puedo usar Google Colab?**
Sí. El requirements.txt es compatible. Sube la carpeta `datasets/` a tu Google Drive y monta.

**¿Y si quiero usar otro modelo DL?**
Bienvenido en la extensión opcional. Lo importante es que **ejecutes y compares**, no qué modelo concreto uses.

**¿Cuándo se publica la solución?**
Las soluciones de referencia están en `soluciones/` pero te recomiendo **no abrirlas** hasta haber intentado el ejercicio completo. La comparativa y las respuestas son intencionalmente abiertas — no hay una "respuesta correcta".
