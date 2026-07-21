---
marp: true
theme: aic
paginate: true
size: 16:9
header: 'aic.'
footer: 'CP4 · Behavioral Cloning · Máster en IA · AIC'
---

<!-- _class: lead -->

# Behavioral Cloning: Aprender a Conducir Mirando

## Caso Práctico 4 · Dosier del alumno

**Máster en IA — AIC**
Módulo: IA Aplicada al Vehículo Autónomo · 2026

---

## Alcance y requisitos previos

En este cuarto caso práctico **entrenará usted mismo una red neuronal** que aprende a conducir **imitando** a un conductor experto (esto se llama *Behavioral Cloning*). Y vivirá en su propio ordenador el problema que hace que esto sea difícil: el **compounding error** (los errores se acumulan).

Está pensado para realizarse **sin conocimientos previos de programación**. El ordenador ya se preparó en CP1; aquí se reutiliza (con un entorno propio de CP4).

> 🕐 **Duración estimada**: ~45–60 min. Sin GPU. 8 GB de RAM. No necesita internet salvo para instalar dependencias.

---

## Objeto de la práctica

Usará un **simulador de autopista** (`highway-env`) para:

1. **Generar un dataset** viendo conducir a un "experto" (~5000 pares imagen → giro de volante).
2. **Entrenar una red** (PilotNet, una CNN pequeña) que predice el giro a partir de la imagen. En CPU, en unos minutos.
3. **Evaluarla** en situaciones **conocidas** vs **nuevas** (otra densidad de tráfico).
4. **Ver fallar al modelo** cuando conduce él solo: el **compounding error**.

> La pregunta del caso: **¿por qué Tesla puede hacer esto en producción y un proyecto académico no?**

---

## Objetivos de aprendizaje

Al finalizar la práctica, el alumno será capaz de:

1. Entender qué es **Behavioral Cloning** (aprender por imitación) y sus límites.
2. Reconocer el **sesgo de los datos** (en autopista casi siempre se va recto) y cómo afecta al entrenamiento.
3. Distinguir rendimiento **en distribución** vs **fuera de distribución** (OOD).
4. **Vivir el compounding error**: por qué un modelo que imita bien en teoría se sale de la carretera al conducir solo.
5. Razonar **mitigaciones** (DAgger, data augmentation…) y por qué la escala de datos de Tesla cambia el juego.

---

## Estructura del trabajo

| Archivo | Función | Duración |
|---------|---------|----------|
| `02_setup` | Verifica el entorno + genera/carga el dataset | 5 min |
| `03_dataset` | Explora los datos (sesgo del volante) | 8 min |
| `04_modelo_pilotnet` | **Entrena** la CNN (~6 min en CPU) | 10 min |
| `05_evaluacion` | Evalúa en conocido vs nuevo (OOD) | 8 min |
| `06_compounding_error` | El modelo conduce solo → se desvía | 10 min |
| `07_preguntas` | Cuestionario de entrega | 10 min |

---

<!-- _class: lead -->

# Parte 0
## Preparación

---

## Lo que hace falta antes de empezar

El ordenador ya quedó preparado en CP1. Para CP4:

1. **Tener la carpeta `CP4-behavioral-cloning`** (mismo repositorio: **Code → Download ZIP** si no la tiene).
2. Crear un **entorno virtual** propio de CP4 e instalar dependencias.
3. **Generar el dataset** con el simulador (un comando).

> Repositorio: **https://github.com/codx-digital/master-ia-practicas**

---

## Paso 1 · Entorno de CP4 + dependencias

Entre en la carpeta `CP4-behavioral-cloning` y:

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
> Instala el simulador (`highway-env`, `pygame`) y PyTorch. Tarda unos minutos.

---

## Paso 2 · Generar el dataset

Un comando crea el dataset viendo conducir al "experto" en el simulador:

```
python scripts/generate_dataset.py
```

Genera ~5000 muestras (imagen → giro) y las guarda en `datasets/cp4-highway-bc.npz`. Tarda **1–3 min**.

> 💡 Es **100% reproducible** (usa semillas fijas): a todos os sale el mismo dataset. Y se genera en local, no se descarga nada.
>
> 🍎 Si ve avisos tipo `objc[...] SDL ... implemented in both`, **ignórelos** — son inofensivos (dos copias de una librería de vídeo) y no afectan al resultado.

---

## Paso 3 · Abrir Jupyter y verificar (`02_setup`)

```
jupyter notebook
```

Ejecute `02_setup.ipynb` entero. Comprueba que el simulador y el dataset están bien. Debe terminar con `✅ Setup OK — listo para 03`.

---

<!-- _class: lead -->

# Parte 1 · Los datos
## Notebook `03_dataset` · ~8 min

---

## Qué hace este notebook

Explora el dataset que generó. Lo más importante: el **histograma del giro de volante** (steering).

> 🔎 **Observe**: la inmensa mayoría de las muestras tienen giro **cercano a 0**. ¿Por qué? Porque en autopista un conductor va **recto** casi todo el tiempo.

Esto crea un **dataset desbalanceado**, y tiene una consecuencia importante para el entrenamiento:

> ✍️ **Anote**: si el 90% de los datos es "ir recto", ¿qué es lo más fácil que puede aprender la red para equivocarse poco… aunque no sepa girar? (es la Pregunta 1)

---

<!-- _class: lead -->

# Parte 2 · Entrenar la red
## Notebook `04_modelo_pilotnet` · ~10 min

---

## Qué hace este notebook

**Entrena** una CNN pequeña (PilotNet, ~250.000 parámetros) para predecir el giro a partir de la imagen. En **CPU**, en unos **6 minutos**.

- Verá la **curva de pérdida** (loss) bajar época a época.
- No hace falta que entienda la arquitectura: lo importante es que **entrena de verdad** en su portátil, sin GPU.

> ⏳ Las épocas tardan; es normal que el notebook esté "pensando" un rato. No lo pare mientras la loss vaya bajando.

---

<!-- _class: lead -->

# Parte 3 · Evaluación
## Notebook `05_evaluacion` · ~8 min

---

## 💡 Lo conocido vs lo nuevo

Se evalúa el modelo en dos conjuntos:

- **In-distribution** (`val_in`): mismo tipo de escenario que el entrenamiento.
- **Fuera de distribución** (`val_ood`): otra densidad de tráfico / geometría que **no vio**.

> Casi siempre el error (MSE) será **más alto en el nuevo** que en el conocido. Ese hueco es la primera señal de que el modelo **no generaliza** tan bien como parecía.

> ✍️ **Anote** el MSE de cada uno y el hueco relativo — es la Pregunta 2.

---

<!-- _class: lead -->

# Parte 4 · El compounding error
## Notebook `06_compounding_error` · ~10 min · **la lección central**

---

## Qué hace este notebook

Hasta ahora el modelo solo **predecía** sobre imágenes fijas. Aquí lo dejamos **conducir solo** (closed-loop): su predicción mueve el coche, lo que genera la siguiente imagen, y así sucesivamente.

> 🔑 **Lo que va a ver**: aunque el modelo imita bien "foto a foto", cuando conduce él solo, un pequeño error lo lleva a una posición **algo distinta** de las que vio entrenando → ahí predice **peor** → el error crece → **se desvía y se sale**. Eso es el **compounding error**.

El notebook mide la **divergencia** entre la trayectoria del modelo y la del experto.

> ✍️ **Observe**: ¿en qué momento (step) empieza a desviarse? ¿La desviación crece **poco a poco** o **cada vez más rápido**? (Pregunta 3)

---

<!-- _class: lead -->

# Parte 5 · El entregable
## Documento a subir a Moodle

---

## Qué se entrega

Un **PDF** (`cp4_<apellido>_<nombre>.pdf`), a **Moodle** (sección "CP4 — Behavioral Cloning"), en **48 h**. Use la **plantilla `plantilla-respuestas-cp4.docx`** (carpeta `entregable/`).

Responde a **5 preguntas** apoyándote en tus resultados:

1. **Sesgo del volante** — ¿por qué el steering se concentra en 0 y cómo afecta al entrenamiento?
2. **Conocido vs nuevo** — compara el error in-dist vs OOD; interpreta el hueco.
3. **Compounding error** — explícalo con tu plot de `06`: ¿cuándo diverge?, ¿crece lineal o más rápido?
4. **Mitigaciones** — 2 técnicas concretas (DAgger, data augmentation…) y cómo atacan el problema.
5. **Por qué Tesla puede** — ¿qué tiene Tesla (datos, hardware, pipeline) que tu BC mini no?

---

## Cómo se te evalúa (16 puntos)

| Se valora | En qué consiste |
|-----------|-----------------|
| **Ejecución** | Generas dataset, entrenas y evalúas correctamente |
| **Comprensión** | Entiendes el sesgo, el OOD y el compounding error |
| **Análisis crítico** | Razonas causas y propones mitigaciones concretas |
| **Comunicación** | PDF ordenado, con plots (loss, MSE, divergencia) |

> Lo que **más sube la nota**: citar **números y steps concretos** de tus plots, y mitigaciones específicas (no "más datos").

---

## Normas de la actividad

- Se **permite** el uso de herramientas de IA como apoyo, pero el análisis y las conclusiones deben ser **propios**. Copiar penaliza.
- Si usó una de estas herramientas, **decláralo** en una línea. No baja la nota; ocultarlo, sí.
- La carpeta `soluciones/` **no debe consultarse** hasta haber intentado el caso.

---

<!-- _class: lead -->

# Para comenzar

**Orden:** `02` → `03` → `04` → `05` → `06` → responder `07`.

El objetivo no es "que el modelo conduzca perfecto" — es **vivir por qué es difícil**. Ante dudas, el **foro del máster**.

> "Imitar foto a foto es fácil. El problema es que, cuando conduces tú, cada pequeño error te lleva a un sitio que no viste — y ahí fallas más. Ese es el muro del Behavioral Cloning."
