# CP4 — Behavioral Cloning: Aprender a Conducir Mirando

> Caso práctico 4 del módulo "IA Aplicada al Vehículo Autónomo"
> Máster en IA · AIC × Universidad de Monterrey · 2026

---

## Lo que vas a hacer

**Entrenar una CNN end-to-end** que aprende a predecir steering desde una vista BEV del entorno, **vivir en código el "compounding error"** que vimos en P4, y entender por qué Tesla puede hacer Behavioral Cloning en producción pero un proyecto académico no.

1. **Generar dataset sintético** con `highway-env` y un policy heurístico ("expert"): ~5000 pares (observación, steering).
2. **Entrenar PilotNet adaptado** (4 conv + 2 FC, ~250k params) en CPU en <10 min.
3. **Evaluar in-distribution vs OOD** (densidad de tráfico distinta).
4. **Demostrar compounding error** con rollout closed-loop del policy entrenado.

**Duración estimada**: 45–60 min · **Sin GPU** · 8 GB RAM.

---

## Por qué este CP

P4 (bloque 3) explicó:
- BC funciona en distribución, falla fuera (compounding error).
- DAgger, data augmentation y datos masivos son las mitigaciones.
- Tesla puede porque tiene 5M coches → tú no.

Aquí lo experimentas. **El objetivo no es vencer al baseline cinemático**, es **vivir el compounding error en tu propia CPU**.

---

## Estructura del caso

```
CP4-behavioral-cloning/
├── README.md                              ← estás aquí
├── requirements.txt
├── rubrica.md
├── datasets/
│   └── README.md
├── notebooks/
│   ├── 01_introduccion.md
│   ├── 02_setup.ipynb                     ← verifica entorno + highway-env
│   ├── 03_dataset.ipynb                   ← cargar / generar + EDA
│   ├── 04_modelo_pilotnet.ipynb           ← entrenar la red
│   ├── 05_evaluacion.ipynb                ← MSE in-distribution vs OOD
│   ├── 06_compounding_error.ipynb         ← rollout closed-loop
│   └── 07_preguntas.md
├── scripts/
│   └── generate_dataset.py                ← 5000 pares (obs, steering)
└── soluciones/                            ← referencia profesor
```

---

## Requisitos previos

- Python 3.10+
- 8 GB RAM
- Sin GPU
- Conexión a internet **solo** para `pip install` inicial

---

## Setup paso a paso

### 1. Entorno virtual y dependencias

```bash
cd CP4-behavioral-cloning
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Generar el dataset sintético

```bash
python scripts/generate_dataset.py
```

Esto crea `datasets/cp4-highway-bc.npz` (~30 MB) con 5000 pares (obs 84×84×3, steering ∈ [-1,1]):
- 3500 train (highway tráfico denso, semilla fija)
- 750 val in-distribution
- 750 val OOD (carriles más estrechos + densidad distinta)

**Tiempo**: ~3 min en CPU (la simulación es lo lento, no el ML).

> **¿Por qué generar y no descargar?** Es **el mismo entorno que CP5**, así sois conscientes de qué hay dentro de los datos. Reproducible con una semilla.

### 3. Verifica entorno

```bash
jupyter notebook notebooks/02_setup.ipynb
```

Al final debe imprimir `✅ Setup OK — listo para 03`.

---

## Orden recomendado

| Notebook | Tiempo | Qué hace |
|----------|--------|----------|
| `02_setup` | 1 min | Verifica imports + dataset + highway-env |
| `03_dataset` | 8 min | EDA: histograma steering, visualización observaciones, augmentation |
| `04_modelo_pilotnet` | 12 min | Entrenar PilotNet adaptado (3-5 épocas CPU) |
| `05_evaluacion` | 5 min | MSE in-distribution vs OOD, scatter, qualitative |
| `06_compounding_error` | 10 min | Rollout closed-loop del policy entrenado |
| `07_preguntas` (md) | 10 min | Responder 5 preguntas |

**Total**: ~45 min activos.

---

## Entregable

Un único PDF (o markdown con plots embebidos) con:

1. Curvas train/val loss de tu entrenamiento.
2. Tabla comparativa MSE in-distribution vs OOD (con razonamiento del gap).
3. **Plot de rollout closed-loop**: trayectoria del policy entrenado vs trayectoria del expert sobre 200 steps.
4. **Respuestas a las 5 preguntas** de `07_preguntas.md`.
5. (Opcional) Extensiones implementadas.

**Subir a**: el **Moodle de AIC** (sección "CP4"). Nombre: `cp4_<apellido>_<nombre>.pdf`.

Se evalúa con la [rúbrica](rubrica.md). Máximo 16 pts.

---

## FAQ rápido

**¿Puedo usar GPU?**
Sí. El entrenamiento es muy pequeño — en CPU ya cabe holgadamente.

**¿El compounding error siempre se ve?**
Sí, con casi total seguridad: el dataset es de 3500 pares — insuficiente para evitar el problema. **Esa es la lección**.

**¿Y si quiero entrenar con dataset Udacity Self-Driving real?**
Bienvenido como extensión opcional. La idea de CP4 es vivir el concepto, no maximizar performance.

**¿Conexión con CP5?**
Mucha: **mismo entorno highway-env**. CP5 hace lo mismo pero con RL en lugar de BC. Vas a poder **comparar políticas BC vs RL** si lo deseas como extensión.
