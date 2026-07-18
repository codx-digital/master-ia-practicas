% CP1 — Detección de Carriles · Plantilla de respuestas
% Máster en IA — AIC · Módulo IA Aplicada al Vehículo Autónomo
% Nombre y apellidos:  ____________________________    Fecha: __________

---

**Instrucciones**

1. Rellene esta plantilla con sus resultados y respuestas.
2. Donde diga *[Pegue aquí la imagen]*, inserte la captura correspondiente (menú **Insertar → Imagen**).
3. Al terminar, exporte a PDF (**Archivo → Guardar como / Exportar → PDF**) con el nombre `cp1_apellido_nombre.pdf` y súbalo a Moodle.

---

# 1. Equipo empleado

*(Una frase: sistema operativo, procesador y tiempo total que le llevó.)*

>

\

# 2. Detector clásico (Canny + Hough)

*Inserte 5 imágenes con los carriles dibujados y explique la configuración que eligió (umbrales de Canny, ROI, votos de Hough) y por qué.*

**Imagen 1 — nombre: ______________**   *[Pegue aquí la imagen]*

**Imagen 2 — nombre: ______________**   *[Pegue aquí la imagen]*

**Imagen 3 — nombre: ______________**   *[Pegue aquí la imagen]*

**Imagen 4 — nombre: ______________**   *[Pegue aquí la imagen]*

**Imagen 5 — nombre: ______________**   *[Pegue aquí la imagen]*

Mi configuración final y por qué:

>

\

# 3. Detector con inteligencia artificial (ONNX)

*Las mismas 5 imágenes con la detección del modelo + observaciones (tiempo, aciertos).*

*[Pegue aquí las 5 imágenes del detector con IA]*

Observaciones (tiempo, dónde acierta/falla):

>

\

# 4. Comparación

*Inserte las 3 gráficas del notebook 04 (mosaico, barras de aciertos, tiempos) y escriba su conclusión.*

*[Pegue aquí el mosaico `04_grid_visual.png`]*

*[Pegue aquí las barras `04_bar_detection_rate.png`]*

*[Pegue aquí los tiempos `04_box_times.png`]*

Síntesis (qué es mejor para qué):

>

\

# 5. Respuestas a las 5 preguntas

## Pregunta 1 — ¿Dónde gana la IA al clásico?

*3 imágenes concretas (por nombre) donde el clásico falla y la IA acierta. Explique el porqué en cada una.*

>

\

## Pregunta 2 — ¿Dónde gana el clásico a la IA?

*La pregunta con trampa. Si no encuentra ninguna, dígalo y analice por qué (sesgo del dataset). La honestidad puntúa.*

>

\

## Pregunta 3 — Tiempo de inferencia y throughput

*(1) ¿Cuál es más rápido (media y p95)? (2) ¿Por qué? (3) ¿Caben en 33 ms (30 FPS)? Si la IA no cabe, dé 2 técnicas para acelerarla.*

>

\

## Pregunta 4 — Decisión de producto (ADAS de bajo coste)

*Lane Keep Assist barato sobre un Mobileye EyeQ4: ¿clásico, IA o híbrido? Argumente con hardware y explicabilidad. ¿Qué métricas pediría a QA? ¿Qué fallback usaría?*

>

\

## Pregunta 5 — Caso límite que rompe ambos

*Invente un escenario plausible que engañe a los dos métodos. Explique por qué falla cada uno y qué cambiaría del sistema (no del modelo) para mitigarlo.*

>

\

# 6. (Opcional) Extensiones probadas

>

\

# Declaración de uso de IA asistente

*Si usó una herramienta de IA (Claude, ChatGPT, Copilot…), indique dónde y para qué. No baja la nota; ocultarlo, sí.*

>
