% CP5 — RL en highway-env · Plantilla de respuestas
% Máster en IA — AIC · Módulo IA Aplicada al Vehículo Autónomo
% Nombre y apellidos:  ____________________________    Fecha: __________

---

**Instrucciones**

1. Rellene esta plantilla con sus resultados y respuestas (apóyese en los `outputs/` de los notebooks 04–07).
2. Donde diga *[Pegue aquí…]*, inserte la captura correspondiente (**Insertar → Imagen**).
3. Al terminar, exporte a PDF (**Archivo → Exportar → PDF**) con el nombre `cp5_apellido_nombre.pdf` y súbalo a Moodle.

---

# 0. Equipo empleado

*(Una frase: sistema operativo, procesador y tiempo total, sobre todo cuánto tardó el entrenamiento del DQN.)*

>

\

# Pregunta 1 — Random vs Rule-based vs DQN

*Mire `outputs/06_eval_summary.json`. ¿Cuál tuvo mejor return? (1) Da los 3 returns medios. (2) ¿Por qué el rule-based puede o no superar al DQN? (3) Si tu DQN no supera al rule-based, ¿qué hipótesis tienes (timesteps, lr, exploración…)?*

*[Pegue aquí la tabla/gráfica de comparación `06_eval_compare.png`]*

>

\

# Pregunta 2 — Sample efficiency

*Mire `outputs/05_learning_curve.png`. (1) ¿En qué timestep el DQN empezó a superar el baseline? (2) Equivalente en tiempo simulado (`timesteps / 5 Hz`). (3) Compara con la sample efficiency del BC de CP4 (~5 min de training con 3500 muestras). Reflexiona sobre RL vs supervisado.*

*[Pegue aquí la curva de aprendizaje `05_learning_curve.png`]*

>

\

# Pregunta 3 — Reward hacking

*En `07_reward_shaping.ipynb` añadiste una penalty por cambio de carril. Mira `outputs/07_shaping_compare.png`: (1) ¿Bajaron los cambios de carril? ¿Cuánto? (2) ¿Subió la tasa de colisión? ¿Qué te dice? (3) ¿Cómo modificarías la recompensa para mitigarlo? Sé específico.*

*[Pegue aquí `07_shaping_compare.png`]*

>

\

# Pregunta 4 — De highway-env al mundo real

*highway-env es un simulador juguete. Identifica 3 simplificaciones que lo hacen distinto del mundo real (peatones, semáforos, tráfico cruzado, clima…).*

1.

2.

3.

>

\

# Pregunta 5 — Cierre: sim-to-real

*Si fueras a usar este DQN en un coche real, ¿qué pasos darías para pasar de simulación a calle? Considera: (1) BC inicial sobre demostraciones reales, (2) sim-to-real (domain randomization, fine-tuning real), (3) certificación de un policy aprendido, (4) ¿RL puro o como módulo sobre planning clásico? Argumenta en 4–6 párrafos.*

>

\

# (Opcional) Extensiones probadas

>

\

# Declaración de uso de IA asistente

*Si usó una herramienta de IA (Claude, ChatGPT, Copilot…), indique dónde y para qué. No baja la nota; ocultarlo, sí.*

>
