# CP3 · Notebook 07 — Local vs Frontier (mini-ensayo)

> **Entregable principal del CP**. 1-2 páginas (PDF) respondiendo las preguntas abajo + tu análisis.
>
> Forma: PDF a Moodle (`cp3_<apellido>_<nombre>.pdf`). Plazo: 48 h. Rúbrica: [`../rubrica.md`](../rubrica.md).

---

## El contexto

Has corrido **Moondream2 (~1.9B params local)** sobre 18 imágenes. Has visto que:
- **Acierta** lo trivial y lo estándar.
- **Alucina** en edge cases.
- **Es determinista** con greedy, variable con sampling.
- **Tarda 3-6 segundos** por imagen.

La pregunta de este entregable es:

> **¿Dónde encaja un VLM (local o frontier) en un sistema de conducción real?**

---

## Pregunta 1 — Caracterización empírica

Resume **con tus datos** las 3 propiedades clave que has observado de Moondream2:

1. **Calidad por categoría** (1-2 frases con tu evidencia de `06_failure_analysis.ipynb`).
2. **Latencia** (cita números de `03_descriptions.json`).
3. **Consistencia** (greedy vs sampling — cita evidencia de `05`).

**Tu respuesta:**

```
(escribe aquí — 5-8 frases)
```

---

## Pregunta 2 — Cuándo SÍ usar un VLM en conducción

P5 (auto-labeling) y P6 (VLA, HMI) explicaron varios roles. **Identifica 3 casos** donde un VLM local tipo Moondream2 **encaja bien**:

1. ...
2. ...
3. ...

Por cada caso, explica:
- Por qué el VLM aporta valor concreto.
- Por qué un modelo clásico no lo resuelve igual de bien.
- ¿Es OK la latencia de Moondream2 para ese caso? ¿Necesitarías quantization?

**Respuesta:**

```
(escribe aquí — 3 párrafos)
```

---

## Pregunta 3 — Cuándo NO usar un VLM

Identifica **3 casos** donde un VLM local **NO encaja**:

1. ...
2. ...
3. ...

Por cada caso, explica:
- Por qué falla el VLM (latencia, hallucination, sample inefficiency, ...).
- ¿Qué alternativa usarías? (CV clásica, modelo especializado pequeño, sensor adicional...).

**Respuesta:**

```
(escribe aquí — 3 párrafos)
```

---

## Pregunta 4 — Local vs Frontier

Si pudieras elegir entre:
- **Local Moondream2** (CPU, ~3 s/img, ~1.9B params, cero coste por inferencia)
- **Frontier (Claude Opus, GPT-5V)** (API, ~2-5 s/img, latencia variable, ~3 €/1000 calls, calidad mucho mayor)

¿Cuándo elegirías cada uno? Argumenta sobre **al menos 3 ejes** (coste, latencia, calidad, privacidad, deployment offline...).

**Respuesta:**

```
(escribe aquí — 4-6 párrafos)
```

---

## Pregunta 5 — La pregunta de cierre

> *"En 2028, ¿estarán los VLMs ya dentro del closed-loop control de un coche autónomo en producción?"*

Defiende tu posición. Considera:
- Latencia hardware previsto 2028 (NPU automotive grade).
- Avances esperados en quantization + distillation.
- Certificación: ¿se puede certificar un VLM?
- Tendencia actual: ¿industria converge a VLA o sigue híbrido?

**Respuesta:**

```
(escribe aquí — 4-6 párrafos. Esta pregunta tiene respuesta abierta y compleja.)
```

---

## (Opcional) Extensiones

- **Probar Claude Vision o GPT-4V** con tu propia key sobre las **mismas 18 imágenes** → comparativa cualitativa.
- **Multi-frame**: pasar 3 frames consecutivos y pedir descripción de movimiento.
- **Few-shot**: enseñarle al VLM con 2 ejemplos de descripción ideal antes.
- **Structured output**: forzar JSON con schema.
- **Long-tail mining**: ¿el VLM identifica las imágenes `trampa` y `ambigua` como diferentes?

```
(opcional)
```

---

## Declaración de uso de IA

```
(p. ej. "Usé Claude para reformular mi mini-ensayo de la pregunta 5.")
```
