# CP4 · Preguntas guiadas (entregable)

Responde a las **5 preguntas** abajo en 1–2 párrafos cada una.

> **Forma de entrega**: PDF a Moodle (`cp4_<apellido>_<nombre>.pdf`).
> **Plazo**: 48 h tras la sesión.
> **Evaluación**: rúbrica en [`rubrica.md`](../rubrica.md).

---

## P1 — Sesgo de steering hacia 0

> Mira el histograma de `outputs/03_dataset_stats.json` (o regéneralo en `03_dataset.ipynb`). ¿Por qué la distribución de steering está sesgada hacia 0? ¿Cómo afecta al entrenamiento de la CNN?
>
> Pista: piensa en qué porcentaje del tiempo un conductor en autopista de hecho gira.

**Respuesta:**

```
(escribe aquí)
```

---

## P2 — In-distribution vs OOD

> Compara MSE en `val_in` vs `val_ood` (de `outputs/05_eval_summary.json`). El gap relativo debería ser ≥ 30%. Argumenta el resultado:
>
> 1. ¿Qué diferencias entre los entornos in-dist y OOD justifican el gap?
> 2. Si el gap es **menor del esperado** (<10%), ¿qué podría haber salido mal en tu generación de dataset?
> 3. Si el gap es **mucho mayor** (>200%), ¿qué dice eso del modelo?

**Respuesta:**

```
(escribe aquí)
```

---

## P3 — Compounding error en tus palabras

> Explica con tus palabras qué es **compounding error** en BC closed-loop, **usando como evidencia** tu plot de `outputs/06_closed_loop.png` y la métrica de divergencia en `outputs/06_divergence.png`.
>
> 1. ¿En qué step empieza a divergir la trayectoria?
> 2. ¿Es la divergencia lineal en el tiempo o supralineal?
> 3. ¿Qué implicaciones tendría para un sistema real?

**Respuesta:**

```
(escribe aquí)
```

---

## P4 — Mitigaciones

> Has visto el problema. ¿Cómo lo mitigarías? Nombra **2 técnicas concretas** (no genéricas: "más datos") y explica cómo cada una atacaría el problema.
>
> Pista: P4 habló de DAgger, data augmentation, on-policy correction, cost-augmented imitation, ensembles. Elige 2 y razónalas para tu caso específico.

**Respuesta:**

```
(escribe aquí)
```

---

## P5 — Por qué Tesla puede

> Tesla afirma usar **Behavioral Cloning** (con detalles propios) en su Planning Transformer v12+. ¿Cómo logra que funcione donde tu BC mini falla?
>
> Investiga (web/papers) y argumenta:
>
> 1. ¿Qué tiene Tesla que tú no? Sé específico: hardware, datos, pipeline.
> 2. ¿Hay algún componente clásico en su pipeline que **recupere** de fallos del BC? (Pista: la planning module no es 100% E2E todavía).
> 3. ¿Crees que sin un dataset masivo escalaría el approach BC puro? Argumenta.

**Respuesta:**

```
(escribe aquí)
```

---

## (Opcional) Extensiones

- **DAgger lite**: añade ~200 muestras de recovery al training y compara.
- **Huber loss** en vez de MSE.
- **Augmentations adicionales**: brightness, gaussian noise.
- **Ensemble**: 3 modelos con random seeds, votar.
- **Comparación con CP5 RL**: ejecutar el policy de CP5 sobre el mismo entorno y comparar trayectorias.

```
(opcional)
```

---

## Declaración de uso de IA asistente

```
(p. ej. "Usé Claude para debuggear un mismatch de shapes en el DataLoader.")
```
