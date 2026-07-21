# Dataset CP4 — Highway BC sintético

## Qué hay aquí

Un único archivo NPZ generado localmente desde `highway-env`:

```
cp4-highway-bc.npz  (~30 MB)
├── train_obs       (3500, 84, 84, 3)  uint8 — observación grayscale stack 3 frames
├── train_actions   (3500,)            float32 — steering normalizado [-1, 1]
├── val_in_obs      (750, 84, 84, 3)   uint8
├── val_in_actions  (750,)             float32
├── val_ood_obs     (750, 84, 84, 3)   uint8
└── val_ood_actions (750,)             float32
```

## Cómo se genera

```bash
python scripts/generate_dataset.py
```

**Tiempo**: ~3 min en CPU.

**Determinista**: misma semilla (`100/2000/3000` para train / val_in / val_ood) → todos los alumnos obtienen el **mismo dataset**.

## ¿Qué es OOD aquí?

| Config | TRAIN | VAL in-dist | VAL OOD |
|--------|-------|-------------|---------|
| `lanes_count` | 4 | 4 | **3** |
| `vehicles_count` | 20 | 20 | **35** (~75% más denso) |
| Semilla base | 100 | 2000 | 3000 |

El OOD no es radical (mismo simulador, mismo expert) — solo cambian densidad y carriles. Suficiente para que un BC pequeño exhiba **degradación de MSE**.

## El expert policy (cómo se generan las acciones)

```python
def expert_policy(kinematics_obs):
    # 1) Si nadie delante cercano → centrarse en el carril (steering ≈ 0)
    # 2) Si hay vehículo delante muy cerca en mismo carril → cambiar al lado contrario
    # 3) Steering continuo en [-1, 1]
```

Es deliberadamente **simple** — un humano lo haría mejor — pero es **consistente** y permite a la CNN aprender un patrón claro.

## ¿Por qué synthetic + highway-env y no Udacity?

Decisión 2026-05-27 documentada en [ESTADO.md](../../../../ESTADO.md):
- Reproducibilidad total (un seed, un dataset).
- **Mismo entorno que CP5** → conexión narrativa directa con RL.
- Sin problemas de licencia del Udacity Self-Driving Car Dataset (~2 GB, descarga inestable).
- Ligero (<60 MB) — gen en 3 min.

Si quieres trabajar con datos reales como extensión opcional, el `notebooks/03_dataset.ipynb` documenta cómo swapear.

## Anti-trampa

**Si tu modelo da MSE muy bajo en val OOD también** (~igual que in-dist), revisa:
1. ¿Mezclaste los splits sin querer?
2. ¿Hay leakage del expert (action_t depende de obs_t+1 por error)?
3. ¿El val OOD se generó con las semillas correctas?

El OOD debería **siempre** dar MSE mayor — si no, hay un bug.
