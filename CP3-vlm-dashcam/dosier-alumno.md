---
marp: true
theme: aic
paginate: true
size: 16:9
header: 'aic.'
footer: 'CP3 · VLM + Dashcam · Máster en IA · AIC'
---

<!-- _class: lead -->

# VLM + Dashcam: IA que razona sobre conducción

## Caso Práctico 3 · Dosier del alumno

**Máster en IA — AIC**
Módulo: IA Aplicada al Vehículo Autónomo · 2026

---

## Alcance y requisitos previos

En este tercer caso práctico usará un **VLM** (modelo de visión-lenguaje): una IA que **mira una imagen y la describe con palabras**, y que puede razonar sobre la escena. Aplicará uno pequeño y **local** (Moondream2) a 17 imágenes de dashcam y descubrirá **dónde acierta** y **dónde alucina**.

Está pensado para realizarse **sin conocimientos previos de programación**. El ordenador ya se preparó en CP1; aquí se reutiliza (con un entorno propio de CP3).

> 🕐 **Duración estimada**: ~45 min. Sin GPU. 8 GB de RAM. Internet la primera vez (el modelo son ~3.7 GB — descárguelo con antelación).

---

## Objeto de la práctica

Es el **caso diferenciador del módulo**: ningún curso de IA general te hace tocar este paradigma aplicado a conducción.

Aplicará **Moondream2** (un VLM de ~1.9 B parámetros, que corre en su portátil) a 17 imágenes clasificadas en 6 categorías (trivial, urbano, edge case visual, edge case semántico, trampa, ambigua), y responderá a la pregunta central:

> **¿Dónde encaja realmente un VLM en el stack de un coche autónomo?** ¿Y cuándo NO se debe usar?

Trabajará con un modelo **local** (sin API, sin coste, reproducible), y **discutirá** el contraste con los modelos "frontier" (Claude, GPT) en el ensayo final.

---

## Objetivos de aprendizaje

Al finalizar la práctica, el alumno será capaz de:

1. Cargar y usar un **VLM local** en CPU, sin entrenar nada.
2. Pedirle **descripciones** y **tareas estructuradas** (objetos, nivel de riesgo, acción sugerida).
3. Medir su **latencia** y su **consistencia** (respuestas deterministas vs variables).
4. Detectar y **categorizar sus alucinaciones**, y razonar por qué ocurren.
5. Argumentar **dónde sí y dónde no** encaja un VLM en un sistema de conducción real.

---

## Estructura del trabajo

| Archivo | Función | Duración |
|---------|---------|----------|
| `02_setup` | Carga Moondream2 + test | 5 min (+descarga la 1ª vez) |
| `03_descripcion_basica` | Describe las 17 imágenes | 8 min |
| `04_tareas_estructuradas` | Objetos + riesgo + acción | 8 min |
| `05_consistencia` | Respuestas deterministas vs variables | 8 min |
| `06_failure_analysis` | Cataloga los fallos | 10 min |
| `07_local_vs_frontier` | Mini-ensayo (entregable) | 15 min |

> ⏳ **Ojo**: el VLM es **lento en CPU** (varios segundos por imagen). Procesar las 17 puede tardar unos minutos por notebook. Es normal — no lo pare.

---

<!-- _class: lead -->

# Parte 0
## Preparación

---

## Lo que hace falta antes de empezar

El ordenador ya quedó preparado en CP1. Para CP3:

1. **Tener la carpeta `CP3-vlm-dashcam`** (mismo repositorio que CP1/CP2: **Code → Download ZIP** si no la tiene).
2. Crear un **entorno virtual** propio de CP3 e instalar dependencias.
3. Las **17 imágenes** dashcam **ya vienen** con el material (no hay que descargarlas).
4. El **modelo** se descarga solo la primera vez (~3.7 GB — hágalo con tiempo).

> Repositorio: **https://github.com/codx-digital/master-ia-practicas**

---

## Paso 1 · Entorno de CP3 + dependencias

Entre en la carpeta `CP3-vlm-dashcam` y:

```
python -m venv .venv
```
```
.venv\Scripts\activate      ← Windows
source .venv/bin/activate   ← Mac
```
> ✅ Debe aparecer **`(.venv)`**.

```
pip install --upgrade pip
pip install -r requirements.txt
```
> Tarda unos minutos.

---

## Paso 2 · Las imágenes ya vienen incluidas

Las **17 imágenes** (6 categorías) **ya están** en `datasets/dashcam-curated/`, dentro del material que descargó. **No tiene que descargar nada.**

> 💡 Si quisiera regenerarlas o ampliarlas, existe `python scripts/download_dataset.py` (las baja de Wikimedia), pero **no es necesario** para hacer el caso.

---

## Paso 3 · Cargar el modelo y verificar (`02_setup`)

Abra Jupyter y ejecute `02_setup.ipynb` entero:

```
jupyter notebook
```

> ⏳ La **primera vez** descarga el modelo (~3.7 GB): puede tardar **5–10 min**. Hágalo antes de la sesión. Después queda cacheado y ya no toca internet.

Debe terminar con `✅ Setup OK — listo para 03`.

---

<!-- _class: lead -->

# Parte 1 · Descripciones
## Notebook `03_descripcion_basica` · ~8 min

---

## Qué hace este notebook

Le pide al VLM que **describa** cada una de las 17 imágenes (peatones, vehículos, señales, clima, peligros). El alumno ejecuta y **lee** las respuestas junto a cada imagen.

Fíjese, por categoría:

- En **trivial** y **urbano**: ¿la descripción es acertada?
- En **edge case**, **trampa** y **ambigua**: ¿empieza a **inventar** cosas que no están?

> ✍️ **Anote** la **latencia** (segundos por imagen) que reporta el notebook: la usará en el ensayo.

---

<!-- _class: lead -->

# Parte 2 · Tareas estructuradas
## Notebook `04_tareas_estructuradas` · ~8 min

---

## Qué hace este notebook

En vez de una descripción libre, le pide al VLM tareas **concretas y accionables**, como haría un sistema real:

- **Objetos críticos** presentes (peatones, coches, señales).
- Un **nivel de riesgo** de la escena.
- Una **acción sugerida** (frenar, mantener, precaución).

Observe si el VLM es **fiable** en estas tareas o si su respuesta cambia de forma o inventa. Un sistema de conducción necesita respuestas **estructuradas y fiables**, no prosa bonita.

---

<!-- _class: lead -->

# Parte 3 · Consistencia
## Notebook `05_consistencia` · ~8 min

---

## 💡 La pregunta: ¿da siempre la misma respuesta?

El notebook pregunta lo mismo **varias veces** a la misma imagen, en dos modos:

- **Determinista** (greedy): debería dar **siempre** la misma respuesta.
- **Con azar** (sampling): cada vez puede dar una **distinta**.

> Para un sistema de seguridad, la **consistencia** importa tanto como el acierto: un módulo que responde algo distinto cada vez no es fiable.

Observe cuánto **varían** las respuestas con sampling. ¿Confiaría en este modelo para una decisión de seguridad?

---

<!-- _class: lead -->

# Parte 4 · Análisis de fallos
## Notebook `06_failure_analysis` · ~10 min

---

## Qué hace este notebook

Le ayuda a **catalogar los fallos** del VLM por tipo:

- **Omisión**: se deja algo importante.
- **Alucinación**: describe algo que **no está**.
- **Localización**: sitúa mal las cosas.
- **Semántica**: malinterpreta el significado de la escena.

Su trabajo es identificar **≥2 ejemplos de cada tipo** y razonar la causa (dominio fuera de su entrenamiento, ambigüedad, sesgo del modelo…).

> Para nota alta: proponga una **mitigación concreta** por tipo de fallo (no "mejor prompt" a secas).

---

<!-- _class: lead -->

# Parte 5 · El entregable
## Mini-ensayo `07_local_vs_frontier`

---

## Qué se entrega

Un **mini-ensayo** de 1–2 páginas en PDF (`cp3_<apellido>_<nombre>.pdf`), a **Moodle** (sección "CP3 — VLM"), en **48 h**. Usa la **plantilla `plantilla-respuestas-cp3.docx`** (carpeta `entregable/`).

Responde a **5 preguntas** apoyándote en tus datos:

1. **Caracterización empírica** — calidad por categoría, latencia y consistencia, con **tus números**.
2. **Cuándo SÍ** usar un VLM en conducción — 3 casos (auto-etiquetado, explicación al conductor…).
3. **Cuándo NO** — 3 casos (control en tiempo real…), con la alternativa que usarías.
4. **Local vs Frontier** — ¿Moondream2 local o un modelo de API (Claude/GPT)? Argumenta sobre ≥3 ejes (coste, latencia, calidad, privacidad, offline).
5. **La pregunta de cierre** — en 2028, ¿estarán los VLMs dentro del control en tiempo real de un coche? Defiende tu postura.

---

## Cómo se te evalúa (16 puntos)

| Se valora | En qué consiste |
|-----------|-----------------|
| **Ejecución** | Los 5 notebooks corren + mejoras tus prompts |
| **Comprensión** | Ves el patrón "acierta lo típico, falla lo raro" **y razonas por qué** |
| **Análisis crítico** | Catalogas tipos de fallo + mitigación concreta + dónde sí/no encaja |
| **Comunicación** | Ensayo claro, con datos y ejemplos lado a lado |

> Lo que **más sube la nota**: números medidos por ti, ejemplos concretos de alucinación, y un argumento **matizado** sobre dónde encaja (y dónde no) un VLM.

---

## Normas de la actividad

- Se **permite** el uso de herramientas de IA como apoyo, pero el análisis y las conclusiones deben ser **propios**. Copiar penaliza.
- Si usó una de estas herramientas, **decláralo** en una línea. No baja la nota; ocultarlo, sí.
- La carpeta `soluciones/` **no debe consultarse** hasta haber intentado el caso.

---

<!-- _class: lead -->

# Para comenzar

**Orden:** `02` → `03` → `04` → `05` → `06` → escribir `07`.

Recuerde: el VLM es **lento en CPU**; los notebooks tardan minutos, es normal. Ante dudas, el **foro del máster**.

> "Un VLM describe la escena con palabras y razona sobre ella — pero también inventa. La gracia de este caso es aprender **dónde puedes confiar en él y dónde no**."
