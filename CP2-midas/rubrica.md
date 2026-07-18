# Rúbrica — CP2 Profundidad Monocular

**Total: 16 puntos** · Pondera 1/5 sobre la nota final del módulo.

---

## Eje 1 — Ejecución técnica (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | Los notebooks no corren / no llegan al final. |
| **1** | Algunos notebooks corren parcialmente. No produce depth maps visibles. |
| **2** | Los 5 notebooks corren. MiDaS y Depth Anything v2 producen outputs visibles. |
| **3** | Idem + el alumno ha experimentado con **al menos 2 imágenes propias** (no del dataset) y documentado el resultado. |
| **4** | Idem + alguna **extensión opcional implementada** (point cloud 3D, ZoeDepth tercer modelo, métrica cuantitativa contra KITTI sparse, aplicación a vídeo). |

---

## Eje 2 — Comprensión (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | No distingue profundidad relativa de métrica, o lo confunde. |
| **1** | Lo distingue conceptualmente pero sin aplicar. |
| **2** | Lo distingue + en sus respuestas a las preguntas argumenta por qué el depth de MiDaS no se puede usar "tal cual" para planning. |
| **3** | Idem + identifica al menos **2 piezas de info** que harían falta para convertir relativo a métrico (estéreo, IMU, tamaños conocidos, mapas HD, LiDAR sparse...). |
| **4** | Idem + demuestra cuantitativamente la diferencia (calibración naïve sobre KITTI sparse, computa AbsRel / RMSE, discute si la calibración funciona o no). |

---

## Eje 3 — Análisis crítico (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | No identifica failure modes. Trata el output como verdad absoluta. |
| **1** | Identifica los failure modes cubiertos en `06_failure_modes.ipynb` (reflejos, cielo, transparencias). |
| **2** | Idem + **encuentra al menos 1 failure mode adicional** sobre las imágenes del módulo y lo razona. |
| **3** | Idem + **prueba imágenes propias** específicamente diseñadas para romper el modelo, documenta resultados. |
| **4** | Idem + **propone mitigación** específica (no genérica): "para detectar reflejos podría usar X foundation model de segmentación que identifica superficies espejo y enmascararlas antes del depth"; "para superficies sin textura podría combinar con radar para tener señal donde el depth alucina"; etc. |

---

## Eje 4 — Comunicación (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | Entrega sin estructura, sin plots, sin separación código/texto. |
| **1** | Estructura mínima. Algún plot. Colores feos (e.g. jet) que engañan. |
| **2** | Plots claros con colorbar, escalas apropiadas (viridis / plasma), título por subplot. |
| **3** | Idem + tabla de tiempos por modelo, comparativa lado-a-lado bien formateada. |
| **4** | Idem + entregable como **reporte ejecutivo**: alguien que no conoce el problema puede leer 2 páginas y entender qué hiciste, qué funciona, qué no, y qué recomendarías para un sistema real. |

---

## Cómo se entrega

Un único PDF (o markdown exportable a PDF) con secciones:

1. **Setup** (1 párrafo: qué OS, qué CPU, qué tiempo total).
2. **MiDaS — 5 imágenes representativas** con depth map + overlay sobre original.
3. **Depth Anything v2 — mismas 5 imágenes**.
4. **Comparativa visual + 1 imagen donde discrepan** (con tu interpretación).
5. **Failure modes** identificados (mínimo 3, con razonamiento).
6. **Respuestas a las 5 preguntas** (`07_preguntas.md`).
7. (Opcional) **Extensiones que probaste**.

Nombre del archivo: `cp2_<apellido>_<nombre>.pdf`.

Plazo: **48h** tras la sesión en directo.

---

## Anti-trampas y honestidad académica

- Usar **IA asistente** (Claude, ChatGPT, Copilot) está permitido. **Pero** las conclusiones y el análisis deben ser tuyos.
- Si has usado un LLM, **decláralo** (1 línea al final). No baja la nota; ocultarlo sí.
- **No abrir `soluciones/`** hasta haber intentado el ejercicio completo. La rúbrica premia el razonamiento, no la solución copiada.
- **Honestidad sobre limitaciones**: si tu CPU es lenta y solo procesaste 10 imágenes en vez de 21, dilo en el reporte — no inventes datos.
