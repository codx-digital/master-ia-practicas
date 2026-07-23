# Rúbrica — CP5 RL en highway-env

**Total: 16 puntos** · Pondera 1/5 sobre la nota final del módulo.

---

## Eje 1 — Ejecución técnica (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | No entrena / no corre. |
| **1** | Entrena pero return no mejora vs random. |
| **2** | Los 6 notebooks corren, DQN supera al baseline rule-based en evaluación. |
| **3** | Idem + el alumno experimentó **reward shaping** propio y documentó el efecto. |
| **4** | Idem + alguna extensión (PPO, curriculum, sim-to-sim transfer, combinar con BC de CP4). |

## Eje 2 — Comprensión (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | No entiende sample efficiency. |
| **1** | Describe RL conceptualmente sin métricas. |
| **2** | Mide y discute timesteps necesarios para superar baselines. |
| **3** | Identifica el "warmup" del aprendizaje (return plano inicial) y razona por qué. |
| **4** | Cuantifica sample efficiency vs. supervised: "DQN necesitó 20k steps = ~2h sim para algo que un BC con 5k pares aprende en 5 min". |

## Eje 3 — Análisis crítico (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | No detecta reward hacking. |
| **1** | Detecta efectos no deseados del reward shaping. |
| **2** | Idem + identifica al menos un comportamiento "atajo" que el agente encontró. |
| **3** | Idem + propone restricciones/penalizaciones para mitigar. |
| **4** | Idem + razona sobre la **transferencia sim-to-real**: por qué este DQN no se desplegaría tal cual y qué pasos darías. |

## Eje 4 — Comunicación (0–4 pts)

| Pts | Criterio |
|-----|----------|
| **0** | Sin plots. |
| **1** | Learning curve básica. |
| **2** | Learning curve + tabla baselines + vídeo/GIF del agente. |
| **3** | Idem + análisis de failure modes específicos en el rollout. |
| **4** | Idem + reporte ejecutivo: alguien que no sabe RL entiende qué hiciste, qué medirá y qué recomiendas. |

---

## Entrega

PDF con: learning curve · tabla baselines vs DQN · GIF/vídeo de 1 episodio · análisis reward shaping · 5 preguntas. Nombre `cp5_<apellido>_<nombre>.pdf`. Plazo 48 h.

## Anti-trampas

- **IA permitida**, declararla al final.
- **`soluciones/`** no abrir antes.
- **Si tu DQN supera al rule-based en 5k steps**, sospecha — RL en este entorno necesita típicamente 15k+. Probablemente hay leakage (eval con misma semilla que train).
