# Rúbrica — CP3 VLM + Dashcam

**Total: 16 puntos** · Pondera 1/5 sobre la nota final.

---

## Eje 1 — Ejecución técnica (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | No corre / modelo no carga. |
| **1** | Corre parcialmente, no genera tabla risk. |
| **2** | Los 5 notebooks corren. Moondream genera respuestas legibles. |
| **3** | Idem + el alumno **mejoró prompts** propios y documenta antes/después. |
| **4** | Idem + alguna extensión (Claude/GPT-4V con su key + comparativa, structured output JSON, multi-frame, few-shot). |

## Eje 2 — Comprensión (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | Acepta respuestas del VLM sin crítica. |
| **1** | Compara con expected_description sin razonar. |
| **2** | Identifica el patrón "el VLM acierta lo típico, falla lo raro". |
| **3** | Idem + cuantifica latencia, consistency, accuracy por categoría. |
| **4** | Idem + razona **conceptualmente** por qué fallaron los failures: dominio fuera del training, sesgo cognitivo del modelo, hallucination específica. |

## Eje 3 — Análisis crítico (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | No detecta hallucinations. |
| **1** | Detecta hallucinations obvias (visible en una imagen). |
| **2** | Categoriza tipos de fallo (omisión, alucinación, localización, semántica) con ≥2 ejemplos cada uno. |
| **3** | Idem + propone **mitigación específica** por tipo (no genérica "mejor prompt"). |
| **4** | Idem + razona dónde **SÍ encaja** un VLM (auto-labeling off-line) y dónde **NO** (closed-loop control). |

## Eje 4 — Comunicación (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | Sin estructura. |
| **1** | Markdown legible sin plots. |
| **2** | Tabla de respuestas + plots de latencia. |
| **3** | Idem + casos lado-a-lado (imagen | descripción Moondream | expected). |
| **4** | Idem + reporte ejecutivo: lectura de 2 páginas explica qué hizo, qué falla, dónde se desplegaría. |

---

## Entrega

PDF con: 3 imágenes comparadas · tabla risk · análisis consistencia · categorización fallos · mini-ensayo (notebook 07).

Nombre `cp3_<apellido>_<nombre>.pdf`. Plazo 48 h.

## Anti-trampas

- **IA permitida** (irónico — el ejercicio es sobre VLMs), declararla.
- **`soluciones/`** no abrir antes de intentarlo.
- **No falsear respuestas del modelo** — el profesor las puede re-generar.
