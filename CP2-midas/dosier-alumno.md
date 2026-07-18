---
marp: true
theme: aic
paginate: true
size: 16:9
header: 'aic.'
footer: 'CP2 · Profundidad Monocular · Máster en IA · AIC'
---

<!-- _class: lead -->

# Profundidad Monocular con Foundation Models

## Caso Práctico 2 · Dosier del alumno

**Máster en IA — AIC**
Módulo: IA Aplicada al Vehículo Autónomo · 2026

---

## Alcance y requisitos previos

En este segundo caso práctico se aplican **dos modelos de inteligencia artificial de última generación** que estiman la **profundidad** (la distancia a cada punto) a partir de **una sola cámara**, sin sensores especiales.

Está pensado para realizarse **sin conocimientos previos de programación**. La preparación del ordenador (Python, terminal, GitHub) ya se hizo en el **Caso Práctico 1**; aquí se reutiliza. Si aún no ha completado CP1, hágalo primero.

> 🕐 **Duración estimada**: ~45 min. Sin GPU. 8 GB de RAM. Se necesita conexión a internet la primera vez (para descargar los modelos, ~50 MB).

---

## Objeto de la práctica

Se aplicarán **dos modelos de profundidad** a las mismas imágenes de CP1 (más algunas nuevas "difíciles"), y se compararán:

1. **MiDaS small** (Intel) — la referencia clásica de estimación de profundidad.
2. **Depth Anything v2 small** — el modelo de referencia actual (2024), que ha superado a MiDaS.

No se entrena nada: un *foundation model* se **carga y se usa**. Y se responderá a una pregunta central:

> **¿Puede una cámara sustituir a un sensor LiDAR para saber a qué distancia está cada cosa?** *(La respuesta tiene matices, y en ellos está la lección.)*

---

## Objetivos de aprendizaje

Al finalizar la práctica, el alumno será capaz de:

1. Cargar y aplicar **modelos de profundidad pre-entrenados** desde HuggingFace, sin entrenar nada.
2. Distinguir entre **profundidad relativa** y **profundidad métrica** — la distinción más importante del tema, y la que más se confunde.
3. Comprender **por qué** una sola cámara no puede dar distancias en metros sin información adicional.
4. Identificar **en qué situaciones fallan** estos modelos y razonar la causa.
5. Comparar dos modelos con **evidencia visual y de tiempo**, y razonar cuál desplegar en un sistema real.

---

## Estructura del trabajo

Se trabaja sobre estos notebooks, en orden:

| Archivo | Función | Duración |
|---------|---------|----------|
| `02_setup` | Verifica el entorno y descarga los modelos | 2 min |
| `03_midas_basico` | Aplica MiDaS a todas las imágenes | 8 min |
| `04_relativa_vs_metrica` | La distinción clave + calibración | 8 min |
| `05_depth_anything_v2` | Lo mismo con Depth Anything v2 + comparativa | 8 min |
| `06_failure_modes` | Dónde y por qué fallan los modelos | 10 min |
| `07_preguntas` | Cuestionario de entrega | 10 min |

> Como resultado se entrega **un PDF** con resultados y respuestas.

---

<!-- _class: lead -->

# Parte 0
## Preparación (más corta que en CP1)

---

## Lo que hace falta antes de empezar

El ordenador ya quedó preparado en CP1. Para CP2 solo hay que:

1. **Tener la carpeta `CP2-midas`** (está en el mismo repositorio que CP1: descárguela igual que en CP1, con **Code → Download ZIP**, si no la tiene ya).
2. **Tener descargadas las imágenes de CP1** (este caso las reutiliza).
3. Crear un **entorno virtual** propio de CP2 e instalar sus dependencias.
4. Descargar unas **imágenes "difíciles"** adicionales.

> El repositorio es el mismo de CP1: **https://github.com/codx-digital/master-ia-practicas**

---

## Paso 1 · Comprobar las imágenes de CP1

Este caso reutiliza las 14 imágenes de carretera de CP1. Si ya hizo CP1, las tiene. Para asegurarse, desde una terminal:

```
cd  (arrastre aquí la carpeta CP1-carriles)  → Intro
source .venv/bin/activate
python scripts/download_assets.py --dataset-only
```

Esto descarga las imágenes de CP1 **solo si faltan** (si ya están, no hace nada).

> 💡 Recuerde: para "entrar" en una carpeta se escribe `cd`, un espacio, y se **arrastra la carpeta** desde el explorador a la terminal.

---

## Paso 2 · Entorno virtual de CP2

CP2 usa librerías nuevas (los modelos de HuggingFace), así que crea **su propio entorno**. Entre en la carpeta `CP2-midas` y:

```
python -m venv .venv
```
```
.venv\Scripts\activate      ← Windows
source .venv/bin/activate   ← Mac
```

> ✅ Debe aparecer **`(.venv)`** al principio de la línea.

Después instale las dependencias (tarda unos minutos; descarga varios cientos de MB):

```
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Paso 3 · Descargar las imágenes "difíciles"

Un comando descarga ~7 imágenes públicas (de Wikimedia) pensadas para **estresar** a los modelos de profundidad: reflejos, túneles, cielo plano, escenas nocturnas.

```
python scripts/download_assets.py
```

> 💡 Estas imágenes **no** necesitan GitHub ni permisos: se bajan de una web pública. Si alguna falla, no pasa nada, el caso funciona con las demás.

---

## Paso 4 · Los modelos se descargan solos

No hay que descargar los modelos a mano. La **primera vez** que ejecute el notebook `02_setup`, se descargan automáticamente desde HuggingFace (~50 MB) y quedan guardados en su ordenador. Las siguientes veces ya no tocan internet.

Abra Jupyter y ejecute `02_setup.ipynb` entero:

```
jupyter notebook
```

Debe terminar con:

```
✅ Setup OK — listo para 03
```

> Si algo falla aquí, revise que el entorno está activado (`(.venv)`) y que tiene conexión a internet.

---

<!-- _class: lead -->

# Parte 1 · MiDaS
## Notebook `03_midas_basico` · ~8 min

---

## Qué hace este notebook

Aplica el modelo **MiDaS** a todas las imágenes y genera, por cada una, un **mapa de profundidad**: una imagen en color donde el color indica **cómo de cerca o lejos** está cada punto.

El alumno ejecuta las celdas en orden y observa los mapas. Fíjese en:

- El **degradado**: lo cercano (el capó, la carretera próxima) frente a lo lejano (el horizonte).
- El **tiempo** de cálculo por imagen en su CPU (aparece medido).

> Es "cargar y usar": el modelo ya viene entrenado. Usted solo lo aplica y observa.

---

## 💡 Un aviso sobre el color

Los mapas de profundidad se muestran con paletas tipo **`plasma`** o **`viridis`**, no con el arcoíris (`jet`). No es un capricho estético: el arcoíris **engaña al ojo** creando falsos bordes donde no los hay. Usar buenas paletas es parte de comunicar bien un resultado técnico (y puntúa en la rúbrica).

> ✍️ **Anote** el tiempo medio por imagen. Lo comparará con el otro modelo más adelante.

---

<!-- _class: lead -->

# Parte 2 · Relativo vs métrico
## Notebook `04_relativa_vs_metrica` · ~8 min · **la parte clave**

---

## La distinción más importante del tema

El mapa de MiDaS dice **qué está más cerca que qué** (profundidad **relativa**), pero **no dice cuántos metros** (profundidad **métrica**). Y esto no es un defecto del modelo: es **geometría**.

> 🔑 **La idea a interiorizar**: en una foto, un coche de juguete cerca y un coche real lejos pueden ocupar **exactamente los mismos píxeles**. Con una sola cámara es **imposible** distinguir tamaño de distancia sin información extra.

El notebook lo hace tangible: intenta convertir el resultado a "metros" con una calibración sencilla de 2 puntos… y le enseña **por qué esa calibración no se sostiene** al cambiar de imagen.

---

## Lo que tiene que observar

1. El notebook toma el resultado de MiDaS y aplica una fórmula para pasarlo a "metros" usando dos puntos de referencia.
2. Luego aplica **esa misma fórmula** a otra imagen distinta. Observe si los "metros" siguen teniendo sentido.
3. Verá una tabla con la **variación** del rango de profundidad entre imágenes.

**Preguntas para su cabeza** (irán en la entrega):

- ¿Por qué una sola cámara no puede dar metros por sí sola?
- ¿Qué **información adicional** haría falta para conseguir metros fiables? (piense en: dos cámaras, un LiDAR aunque sea pobre, saber el tamaño real de una señal, un mapa…)

---

<!-- _class: lead -->

# Parte 3 · Depth Anything v2
## Notebook `05_depth_anything_v2` · ~8 min

---

## Qué hace este notebook

Repite el mismo proceso con el modelo **Depth Anything v2** (el de referencia actual) y lo **compara** con MiDaS sobre las mismas imágenes. Genera:

- Una **comparativa lado a lado** (original · MiDaS · Depth Anything v2).
- Un mapa de **diferencias** entre ambos.
- Un **gráfico de tiempos** de los dos modelos.

Observe **una imagen donde discrepen claramente**: ¿cuál parece acertar más? ¿O son dos interpretaciones igual de plausibles de una escena ambigua?

> ✍️ Esa imagen de discrepancia, con su interpretación, es material directo para la entrega.

---

<!-- _class: lead -->

# Parte 4 · Dónde mienten los modelos
## Notebook `06_failure_modes` · ~10 min

---

## Qué hace este notebook

Pasa por los modelos las imágenes "difíciles" y le muestra **dónde fallan**: reflejos en cristales, superficies sin textura (cielo, paredes lisas), escenas nocturnas, transparencias.

Su trabajo es **razonar la causa**, no solo constatar el fallo. Pista conceptual:

> Estos modelos asumen que las superficies son **opacas y mates** (reflejan la luz de forma uniforme). Cuando esa suposición se rompe —un cristal, agua, un reflejo, una pared sin textura— el modelo **inventa** profundidad donde no la hay.

- Identifique **al menos 3 situaciones** de fallo y qué tienen en común.
- Para nota alta: proponga una **mitigación concreta** (no "más datos"), p. ej. combinar con otro sensor donde el modelo alucina.

---

<!-- _class: lead -->

# Parte 5 · La entrega
## Documento a subir a Moodle

---

## Contenido de la entrega

Un **único PDF** llamado `cp2_<apellido>_<nombre>.pdf`, a **Moodle** (sección "CP2 — Profundidad"), en **48 horas** tras la sesión.

Debe contener:

1. **Equipo empleado** — 1 frase: qué ordenador y cuánto tiempo.
2. **MiDaS** — 5 imágenes representativas con su mapa de profundidad.
3. **Depth Anything v2** — las mismas 5 imágenes.
4. **Comparativa** + **1 imagen donde discrepen**, con su interpretación.
5. **Failure modes** — mínimo 3, con su razonamiento.
6. **Respuestas** a las 5 preguntas de `07_preguntas.md`.

> 💡 Use la **plantilla `plantilla-respuestas-cp2.docx`** (carpeta `entregable/`): trae las secciones y las preguntas ya montadas. Solo tiene que rellenarla, pegar las imágenes y exportarla a PDF (**Archivo → Exportar → PDF**).

---

## Las 5 preguntas, en síntesis

1. **Discrepancia** — una imagen donde los dos modelos difieran; ¿por qué?
2. **Relativo vs métrico** — ¿qué problema **geométrico** impide obtener metros con una cámara? Dé **2 fuentes** de información que ayudarían.
3. **Failure modes** — 2 situaciones donde fallan; ¿qué tienen en común?
4. **Tiempos y producción** — ¿cuál es más rápido/preciso?; ¿cuál desplegaría en un sistema de bajo coste y por qué?
5. **Encaje en el sistema** — ¿qué módulo del stack de conducción usaría este mapa de profundidad?

> No se busca una respuesta única, sino un **razonamiento fundamentado** en lo que ha visto.

---

## Cómo se te evalúa (16 puntos)

| Se valora | En qué consiste |
|-----------|-----------------|
| **Ejecución** | Los 5 notebooks corren + prueba imágenes propias |
| **Comprensión** | Distingue relativo de métrico **y lo argumenta** |
| **Análisis crítico** | Identifica failure modes + propone mitigación concreta |
| **Comunicación** | PDF ordenado, mapas con buen color y escala |

> Lo que **más sube la nota**: llegar a que lo de "relativo vs métrico" es **geometría**, no falta de datos; failure modes con causa estructural; y honestidad sobre lo que no funcionó.

---

## Normas de la actividad

- Se **permite** el uso de herramientas de inteligencia artificial como apoyo, pero las **conclusiones deben ser propias**. Copiar respuestas literales penaliza.
- Si usó una de estas herramientas, **decláralo** en una línea al final. No baja la nota; ocultarlo, sí.
- La carpeta `soluciones/` **no debe consultarse** hasta haber intentado el caso: la rúbrica premia el razonamiento.

---

<!-- _class: lead -->

# Para comenzar

**Orden:** `02` → `03` → `04` → `05` → `06` → responder `07`.

Ante cualquier dificultad, revise el apartado de preparación y pregunte en el **foro del máster**.

> "Con una sola cámara sabes qué está más cerca. Saber *cuántos metros* es otro problema — y es de geometría, no de tener un modelo mejor."
