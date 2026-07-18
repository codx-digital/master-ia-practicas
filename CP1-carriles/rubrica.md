# Rúbrica — CP1 Detección de Carriles

**Total: 16 puntos** · Pondera 1/5 sobre la nota final del módulo.

---

## Eje 1 — Ejecución técnica (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | Los notebooks no corren / no llegan al final / dan errores no resueltos. |
| **1** | Algunos notebooks corren parcialmente, no se llega a producir comparativa visual. |
| **2** | Los 4 notebooks corren y producen los outputs esperados (overlays, plots, tabla). |
| **3** | Idem + el alumno ha **tuneado parámetros propios** (thresholds Canny, ROI, votos Hough) y documentado la decisión. |
| **4** | Idem + alguna **extensión opcional implementada** (polynomial fit, vídeo, métricas IoU, otro modelo DL). |

---

## Eje 2 — Comprensión (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | Respuestas a las preguntas son vagas, genéricas, parecen copiadas o no demuestran haber ejecutado el código. |
| **1** | Responde a las preguntas pero sin referencia a sus propios resultados. |
| **2** | Respuestas correctas con referencia a las imágenes específicas que vio. |
| **3** | Respuestas con **razonamiento causal** ("falla aquí *porque* el Canny detecta el borde de la sombra como si fuera línea"). |
| **4** | Idem + **análisis cuantitativo**: tiempos medidos, % de aciertos categorizado, tabla comparativa con números reales. |

---

## Eje 3 — Análisis crítico (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | No identifica ningún límite de los enfoques. Trata todo como "funciona". |
| **1** | Identifica los límites obvios (lluvia, sombras pronunciadas) pero sin profundizar. |
| **2** | Identifica límites cubiertos en notebook + alguno propio. |
| **3** | Identifica edge cases **no evidentes** (p.ej. carril segmentado con sombra alternante engaña al clásico pero también ralentiza al DL, o detección de carril fantasma en reflejos de carrocería). |
| **4** | Idem + **propone mitigación específica** (no genérica: "más datos") sino concreta ("preproceso CLAHE para normalizar iluminación antes de Canny" o "ensemble clásico+DL con voting"). |

---

## Eje 4 — Comunicación (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | Entrega sin estructura, mezcla código y texto sin separación, sin plots. |
| **1** | Estructura mínima (markdown legible), plots básicos sin formato. |
| **2** | Plots claros con título, ejes, leyendas. Texto separado del código en celdas markdown. |
| **3** | Idem + tabla comparativa bien formateada + conclusiones explícitas separadas. |
| **4** | Idem + entregable como **reporte ejecutivo**: alguien que no conoce el problema podría leer 2 páginas y entender qué hiciste, qué encontraste y qué recomiendas. |

---

## Cómo se entrega

Un único PDF (o markdown exportable a PDF) con secciones:

1. **Setup** (1 párrafo: qué OS, qué CPU, qué tiempo total te llevó).
2. **Pipeline clásico**: 5 imágenes con overlay + 1 párrafo explicando tu configuración final.
3. **Deep learning**: 5 mismas imágenes con overlay + 1 párrafo (tiempo, observaciones).
4. **Comparativa**: tabla + grid visual + 1 párrafo de síntesis.
5. **Respuestas a las 5 preguntas** (`05_preguntas.md`).
6. (Opcional) **Extensiones que probaste**.

Nombre del archivo: `cp1_<apellido>_<nombre>.pdf`.

Plazo: **48h** tras la sesión en directo.

---

## Anti-trampas y honestidad académica

- Usar **IA asistente (Claude, ChatGPT, Copilot)** está permitido — es parte del entorno profesional 2026. **Pero** las **conclusiones y el análisis crítico deben ser tuyos**. Si copias respuestas literales de un LLM se nota y se penaliza.
- Si has usado un LLM, declara dónde y para qué (1 línea al final del entregable). No baja la nota; oculta sí.
- Las **soluciones de referencia** en `soluciones/` están disponibles. Mirarlas antes del propio intento es un disservicio para uno mismo — la rúbrica premia el razonamiento, no la solución copiada.
