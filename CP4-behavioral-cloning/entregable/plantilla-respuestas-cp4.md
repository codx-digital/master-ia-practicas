% CP4 — Behavioral Cloning · Plantilla de respuestas
% Máster en IA — AIC · Módulo IA Aplicada al Vehículo Autónomo
% Nombre y apellidos:  ____________________________    Fecha: __________

---

**Instrucciones**

1. Rellene esta plantilla con sus resultados y respuestas (apóyese en los `outputs/` de los notebooks 03–06).
2. Donde diga *[Pegue aquí…]*, inserte la captura correspondiente (**Insertar → Imagen**).
3. Al terminar, exporte a PDF (**Archivo → Exportar → PDF**) con el nombre `cp4_apellido_nombre.pdf` y súbalo a Moodle.

---

# 0. Equipo empleado

*(Una frase: sistema operativo, procesador y tiempo total.)*

>

\

# Pregunta 1 — Sesgo de steering hacia 0

*Mire el histograma de steering (`03_dataset.ipynb` / `outputs/03_dataset_stats.json`). ¿Por qué la distribución está sesgada hacia 0? ¿Cómo afecta al entrenamiento de la CNN?*

*[Pegue aquí el histograma de steering]*

>

\

# Pregunta 2 — In-distribution vs OOD

*Compare el MSE en `val_in` vs `val_ood` (`outputs/05_eval_summary.json`). (1) ¿Qué diferencias justifican el gap? (2) Si el gap es <10%, ¿qué pudo salir mal en la generación del dataset? (3) Si es >200%, ¿qué dice del modelo?*

>

\

# Pregunta 3 — Compounding error en tus palabras

*Explique qué es el compounding error en BC closed-loop, usando como evidencia `outputs/06_closed_loop.png` y `outputs/06_divergence.png`.*

*[Pegue aquí el plot de closed-loop y/o el de divergencia]*

*(1) ¿En qué step empieza a divergir? (2) ¿La divergencia es lineal o supralineal en el tiempo? (3) ¿Implicaciones para un sistema real?*

>

\

# Pregunta 4 — Mitigaciones

*Nombre 2 técnicas concretas para mitigar el compounding error (no "más datos") y explique cómo cada una ataca el problema en su caso. (Pista P4: DAgger, data augmentation, on-policy correction, cost-augmented imitation, ensembles.)*

**Técnica 1:**

>

**Técnica 2:**

>

\

# Pregunta 5 — Por qué Tesla puede

*Tesla usa Behavioral Cloning en su Planning Transformer v12+. ¿Cómo lo consigue donde su BC mini falla? (1) ¿Qué tiene Tesla que usted no (hardware, datos, pipeline)? (2) ¿Hay un componente clásico que recupere de fallos del BC? (3) ¿Escalaría el BC puro sin un dataset masivo?*

>

\

# (Opcional) Extensiones probadas

>

\

# Declaración de uso de IA asistente

*Si usó una herramienta de IA (Claude, ChatGPT, Copilot…), indique dónde y para qué. No baja la nota; ocultarlo, sí.*

>
