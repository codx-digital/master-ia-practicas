# CP5 · Preguntas guiadas (entregable)

> **Forma**: PDF a Moodle (`cp5_<apellido>_<nombre>.pdf`). **Plazo**: 48 h. **Eval**: [rúbrica](../rubrica.md).

---

## P1 — Random vs Rule-based vs DQN

> Mira `outputs/06_eval_summary.json` (o tu tabla del notebook 06). ¿Cuál de los 3 enfoques tuvo mejor return? ¿Esperabas eso?
>
> 1. Da los 3 returns medios concretos.
> 2. ¿Por qué el rule-based puede o no superar al DQN dependiendo del entrenamiento?
> 3. Si tu DQN **no supera** al rule-based, ¿qué hipótesis tienes? (Pista: insuficientes timesteps, lr, exploración, target update interval.)

**Respuesta:**

```
(escribe aquí)
```

---

## P2 — Sample efficiency

> Mira `outputs/05_learning_curve.png`. ¿En qué timestep el DQN empezó a superar el baseline rule-based?
>
> 1. Da el número de timesteps aproximado.
> 2. Calcula equivalente en tiempo simulado: `timesteps / 5 Hz = segundos sim`. Convierte a minutos.
> 3. Si un BC con 3500 muestras (CP4) aprende en ~5 min de training, ¿cuánto tiempo "vivido" necesitó el DQN para algo comparable? Reflexiona sobre **sample efficiency** de RL vs supervised.

**Respuesta:**

```
(escribe aquí)
```

---

## P3 — Reward hacking

> En `07_reward_shaping.ipynb` añadiste una penalty por cambio de carril. Mira `outputs/07_shaping_compare.png`:
>
> 1. ¿Bajó el número de cambios de carril? ¿Cuánto?
> 2. ¿Subió la tasa de colisión? Si sí, ¿qué te dice eso sobre el agente?
> 3. ¿Cómo modificarías la recompensa para mitigar este reward hacking? Sé específico — no "mejor reward", sino qué cambiarías y por qué.

**Respuesta:**

```
(escribe aquí)
```

---

## P4 — De highway-env al mundo real

> highway-env es un **simulador juguete**. Identifica **3 simplificaciones** que lo hacen distinto del mundo real:
>
> Pista: piensa en qué partes del problema "conducir" no aparecen aquí (peatones, semáforos, tráfico cruzado, climatología, etc.).

**Respuesta:**

```
(escribe aquí)
```

---

## P5 — Cierre: sim-to-real

> Si fueras a usar este DQN en un coche real, ¿qué pasos darías para pasar de simulación a calle?
>
> Pista: P5 (Datos a Escala) y P6 cubrirán sim-to-real con más detalle. Aquí queremos saber **qué pasos generales** darías:
>
> 1. BC inicial sobre demostraciones humanas reales antes del RL.
> 2. Sim-to-real: domain randomization, fotorrealismo, fine-tuning real.
> 3. Certificación: ¿es desplegable un policy aprendido sin garantía formal?
> 4. Híbrido: ¿RL puro o como módulo encima de planning clásico?
>
> Argumenta tu plan en 4-6 párrafos.

**Respuesta:**

```
(escribe aquí)
```

---

## (Opcional) Extensiones

- PPO en vez de DQN.
- Curriculum (`highway` → `merge` → `roundabout`).
- State stacking (4 frames).
- **Comparación con CP4 BC**: aplicar el policy de CP4 sobre highway-env y comparar trayectorias.
- Sim-to-sim transfer: entrenar en `highway-v0`, evaluar en `merge-v0`.

```
(opcional)
```

## Declaración de IA

```
(p. ej. "Usé Claude para entender por qué `FlattenObservation` era necesario.")
```
