# CP1 · Preguntas guiadas (entregable)

Responde a las **5 preguntas** abajo en 1–2 párrafos cada una. Apóyate en los **plots y métricas** que generaron tus notebooks 02, 03 y 04 (los PNG en `outputs/`).

> **Forma de entrega**: incluye estas respuestas en el PDF que sube a Moodle (`cp1_<apellido>_<nombre>.pdf`).
>
> **Plazo**: 48 h tras la sesión en directo.
>
> **Evaluación**: rúbrica en [`rubrica.md`](../rubrica.md). Cuenta el **razonamiento causal** y el **análisis cuantitativo**, no la longitud.

---

## Pregunta 1 — ¿Dónde gana el DL al clásico?

> Identifica **3 imágenes específicas** (por nombre, p.ej. `hard/img_07.png`) donde el clásico falló y el DL acertó. Para cada una:
>
> 1. Pega el overlay del clásico y el del DL lado a lado.
> 2. Describe qué hay en la imagen (sombras, oclusión, línea discontinua, curva, lluvia…).
> 3. Explica **por qué** el clásico falla ahí ("Canny detectó el borde de la sombra como si fuera línea") y **por qué** el DL no.

**Espacio para tu respuesta:**

```
(escribe aquí)
```

---

## Pregunta 2 — ¿Dónde gana el clásico al DL?

> Esta es la pregunta más interesante. Hay 3 posibilidades:
>
> 1. Hay 1+ imagen donde el clásico acierta y el DL falla → enséñala y explícala.
> 2. No hay ninguna → analiza qué dice eso (¿es el dataset benévolo con DL? ¿el clásico tiene los hiperparámetros mal? ¿el modelo está demasiado bien entrenado para este tipo de imagen?).
> 3. Hay alguna donde ambos fallan pero por motivos distintos → enséñala y compara los modos de fallo.

**Espacio para tu respuesta:**

```
(escribe aquí)
```

---

## Pregunta 3 — Tiempo de inferencia y throughput

> Usa los datos de `outputs/04_comparison_summary.json` y `outputs/04_box_times.png`.
>
> 1. **¿Cuál es más rápido en tu CPU?** Da media y p95 de ambos.
> 2. **¿Por qué?** (sin entrar en arquitecturas: en términos de operaciones por píxel y de paralelismo CPU).
> 3. A 30 FPS de cámara, el budget por frame es **33 ms**. ¿Cabe el clásico? ¿Cabe el DL en CPU? Si no cabe, ¿qué harías para que cupiera? Da al menos **2 técnicas distintas** que cubrimos en P1 (sección "Hardware típico" y "El modelo del paper ≠ el modelo en producción").

**Espacio para tu respuesta:**

```
(escribe aquí)
```

---

## Pregunta 4 — Decisión de producto: ADAS de bajo coste

> Eres ingeniero de un Tier-1 que vende un sistema **Lane Keep Assist** para el segmento C (coche urbano-medio, presupuesto ajustado). Tu hardware destino es un Mobileye EyeQ4 (~10 W TDP, ~5 TFLOPS, sin GPU dedicada).
>
> 1. ¿Elegirías el enfoque clásico, el DL, o un híbrido? Argumenta.
> 2. ¿Qué métricas adicionales pedirías al equipo de QA antes de firmar?
> 3. ¿Cuál sería tu **fallback** si el detector principal falla un frame? (Pista: P1 habla de redundancia y de "lo que pasa cuando el sistema no está seguro").

**Espacio para tu respuesta:**

```
(escribe aquí)
```

---

## Pregunta 5 — Edge case que rompe ambos

> Diseña (no implementes — solo razona) **una imagen o escenario** que romperá ambos enfoques. Razones por qué el clásico falla y por qué el DL también.
>
> Ejemplos del estilo (no copies, inventa el tuyo): líneas pintadas en la cuneta como parte de obras y la real continúa en otro lado; carriles cubiertos por nieve fresca; calle de adoquines sin marcas pintadas pero con bordes naturales tipo bordillo; doble línea amarilla que el dataset de entrenamiento no contenía.
>
> 1. Describe el escenario en 3–4 frases.
> 2. ¿Por qué falla el clásico? (Canny, ROI, Hough…)
> 3. ¿Por qué falla el DL? (out-of-distribution, sesgo del training set, geometría no presente…)
> 4. **¿Qué cambiarías del sistema completo** (no del modelo) para mitigarlo? (Más sensores, mapas HD, V2X, anomaly detection sobre la salida del modelo, etc.)

**Espacio para tu respuesta:**

```
(escribe aquí)
```

---

## (Opcional) Extensiones

Si hiciste alguna de las extensiones del syllabus (polynomial fitting, otro modelo DL, métricas IoU contra ground truth, aplicación a vídeo…), descríbelas aquí. **Suma puntos en el eje "Ejecución técnica" de la rúbrica.**

```
(opcional)
```

---

## Declaración de uso de IA asistente

Si has usado un LLM (Claude, ChatGPT, Copilot…) durante el ejercicio, declara dónde y para qué (1 línea). No baja la nota; **ocultar sí**.

```
(p. ej. "Usé Claude para entender el formato de salida del modelo ONNX y para depurar un error de import de scipy.")
```
