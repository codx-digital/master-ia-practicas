# CP4 · Introducción — Behavioral Cloning

> Lee esto antes de tocar los notebooks. 5 min.

## Lo que viene

Vas a entrenar una **CNN end-to-end** que aprende a predecir steering desde una observación visual del entorno. **Sin reglas escritas a mano. Solo demostraciones**.

Pero también vas a vivir **el lado oscuro de BC** — el **compounding error** que en P4 fue concepto.

## El paradigma

```
Demostraciones del expert:    {(obs_t, action_t)} t=1...N
                                       │
                                       ▼
                              CNN regresor (MSE)
                                       │
                                       ▼
                              Política π(obs) → action
```

En entrenamiento parece **fácil**: regresión supervisada estándar.

En **deployment** la red se aplica recursivamente:
```
obs_0 ──► CNN ──► action_0 ──► entorno ──► obs_1 ──► CNN ──► action_1 ──► ...
```

Si la CNN se equivoca en `action_0`, **`obs_1` ya no es como las que vio en training** → action_1 sale aún peor → distribución se va. Esto es **compounding error**.

## Lo que vamos a hacer paso a paso

1. **Setup** (notebook 02) — verificar highway-env corre y dataset existe.
2. **Dataset EDA** (notebook 03) — histograma steering (verás que está sesgado a 0), visualización de observaciones, augmentation.
3. **Modelo PilotNet** (notebook 04) — definir CNN ~250k params, entrenar 3-5 épocas, ver convergencia.
4. **Evaluación** (notebook 05) — MSE in-dist vs OOD, scatter prediction-vs-truth, qualitative.
5. **Compounding error** (notebook 06) — desplegar el policy en el entorno cerrado, graficar la trayectoria. Confirmar el drift.
6. **Preguntas** (markdown 07) — entregable.

## Lecciones esperadas

✅ La CNN converge bonita en val (in-distribution).
✅ Val OOD es claramente peor — esperado.
✅ Closed-loop muestra **divergencia**: el policy entrenado **no recupera** de pequeñas desviaciones.
✅ El histograma de steering está **sesgado a 0** → modelo aprende un sesgo de inacción.
✅ Tras vivir esto, entiendes por qué Tesla apuesta por **5M coches** y no por "una idea mejor".

## Si todo va bien...

...al cerrar el laboratorio entenderás **por qué el compounding error es el problema fundamental de BC** y por qué la solución no es "modelo más grande" sino **DAgger / on-policy correction / datos masivos**.

---

Cuando estés listo, abre `02_setup.ipynb`.
