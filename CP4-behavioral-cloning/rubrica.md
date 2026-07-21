# Rúbrica — CP4 Behavioral Cloning

**Total: 16 puntos** · Pondera 1/5 sobre la nota final del módulo.

---

## Eje 1 — Ejecución técnica (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | Los notebooks no corren / no entrena. |
| **1** | Entrena pero loss no converge (no baja). |
| **2** | Los 5 notebooks corren, modelo converge (val loss baja consistentemente). |
| **3** | Idem + el alumno **tuneó hiperparámetros propios** (lr, batch, épocas) y documentó la decisión. |
| **4** | Idem + alguna **extensión opcional implementada** (DAgger lite, Huber loss, augmentation rica, ensemble, comparación con CP5 RL). |

---

## Eje 2 — Comprensión (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | No entiende qué es BC ni el compounding error. |
| **1** | Lo describe conceptualmente sin demostración empírica. |
| **2** | Lo describe + el rollout closed-loop muestra divergencia clara. |
| **3** | Idem + cuantifica el gap in-distribution vs OOD con métricas concretas. |
| **4** | Idem + razona **por qué Tesla puede** (datos masivos, DAgger online, cost-augmented imitation) **y argumenta** qué falta a su modelo para escalar. |

---

## Eje 3 — Análisis crítico (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | Acepta el modelo como bueno sin matizar. |
| **1** | Identifica que hay un problema pero sin causa raíz. |
| **2** | Identifica compounding error + sesgo de steering hacia 0 (clases desbalanceadas). |
| **3** | Idem + propone al menos **2 mitigaciones concretas** (no genéricas: "más datos"). |
| **4** | Idem + **implementa** al menos una mitigación y compara antes/después. |

---

## Eje 4 — Comunicación (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | Sin plots ni estructura. |
| **1** | Plots básicos sin formato. |
| **2** | Loss curves + scatter prediction-vs-truth con leyendas. |
| **3** | Idem + tabla comparativa in-dist vs OOD + visualización del rollout. |
| **4** | Idem + entregable como **reporte ejecutivo**: alguien que no conoce BC puede leer 2 páginas y entender el concepto + tu evidencia + tu conclusión. |

---

## Cómo se entrega

Un único PDF con secciones:

1. **Setup** (1 párrafo).
2. **Dataset** — histograma de steering + 3 observaciones de ejemplo.
3. **Entrenamiento** — curvas loss + hiperparámetros usados.
4. **Evaluación** — MSE in-dist vs OOD + scatter prediction-vs-ground-truth.
5. **Compounding error** — plot del rollout closed-loop (200 steps) + explicación.
6. **Respuestas a las 5 preguntas**.
7. (Opcional) Extensiones.

Nombre: `cp4_<apellido>_<nombre>.pdf`. Plazo: **48 h** tras la sesión.

---

## Anti-trampas

- **IA asistente permitida**, declárala al final.
- **`soluciones/`** no abrir antes de intentar — el ejercicio premia el camino, no el destino.
- **Si tu rollout NO muestra divergencia**, sospecha — casi seguro hay un bug. Pídele opinión a un compañero antes de reportar "no hay compounding error".
