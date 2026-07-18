# CP2 · Preguntas guiadas (entregable)

Responde a las **5 preguntas** abajo en 1–2 párrafos cada una. Apóyate en los **plots y métricas** generados por tus notebooks 03–06 (`outputs/`).

> **Forma de entrega**: en el PDF que sube a Moodle (`cp2_<apellido>_<nombre>.pdf`).
> **Plazo**: 48 h tras la sesión.
> **Evaluación**: rúbrica en [`rubrica.md`](../rubrica.md).

---

## Pregunta 1 — Discrepancia MiDaS vs Depth Anything v2

> Muestra **una imagen donde MiDaS y Depth Anything v2 difieran significativamente** (mira `outputs/05_diff_normalized.png` o re-genera uno). Especula **por qué**.
>
> Apunta:
> 1. Imagen específica (nombre).
> 2. Dónde discrepan (zona de la imagen).
> 3. Hipótesis del porqué — ¿uno está acertando y el otro no, o son interpretaciones igualmente válidas?

**Respuesta:**

```
(escribe aquí)
```

---

## Pregunta 2 — Relativo vs métrico

> ¿Qué problema **geométrico fundamental** impide convertir profundidad monocular en métrica sin información adicional? Da **2 fuentes de información** que ayudarían a obtener métrica fiable.
>
> Pista: la respuesta no es "el modelo no es lo suficientemente bueno". Es algo más profundo, relacionado con la ambigüedad de tamaño en proyecciones 2D.

**Respuesta:**

```
(escribe aquí)
```

---

## Pregunta 3 — Failure modes sistémicos

> Identifica **2 superficies / situaciones** donde uno o ambos modelos fallan sistemáticamente sobre las imágenes del módulo (CP1 + CP2 extras). ¿Qué tienen en común? ¿Por qué los foundation models tienden a fallar ahí?

**Respuesta:**

```
(escribe aquí)
```

---

## Pregunta 4 — Tiempos y producción

> Mide tiempo de inferencia en tu CPU para ambos modelos (boxplot de `outputs/05_times.png`).
>
> 1. ¿Cuál es más rápido? ¿Por cuánto?
> 2. ¿Cuál es **más preciso** cualitativamente sobre las imágenes `challenge`?
> 3. Si tuvieras que **desplegar uno** en un ADAS de bajo coste (EyeQ4-class), ¿cuál elegirías? Argumenta considerando latencia, calidad y tamaño del modelo. ¿Tiene sentido FP16 / INT8 quantization?

**Respuesta:**

```
(escribe aquí)
```

---

## Pregunta 5 — Encaje en el stack real

> En un sistema de conducción real, **¿qué módulo del stack consumiría** un depth map de este tipo?
>
> Pista: piensa en términos de las **4 cajas** que vimos en P1 (Percepción → Fusión → Predicción → Planning). Adicionalmente, P2 introdujo BEV — ¿depth monocular encaja en algún paso de proyección a BEV?
>
> Dibuja o describe el flujo. Si necesitas info adicional (que ya cubrió la P3), dilo explícitamente.

**Respuesta:**

```
(escribe aquí)
```

---

## (Opcional) Extensiones

Si hiciste alguna extensión del syllabus (point cloud 3D, ZoeDepth, métrica con KITTI sparse, aplicación a vídeo), descríbela aquí. Suma puntos en eje "Ejecución técnica".

```
(opcional)
```

---

## Declaración de uso de IA asistente

```
(p. ej. "Usé Claude para entender la fórmula afín de calibración inverse-to-metric.")
```
