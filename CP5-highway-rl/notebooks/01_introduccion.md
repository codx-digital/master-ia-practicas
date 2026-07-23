# CP5 · Introducción — RL en highway-env

> Lee esto antes de los notebooks. 5 min.

## Lo que viene

Vas a entrenar un agente **DQN** (Deep Q-Network) que aprende a conducir en `highway-env` **sin demostraciones humanas**. Solo prueba/error + recompensa.

A diferencia de CP4 (donde el modelo imitaba), aquí el modelo **explora** y aprende qué acciones llevan a mayor recompensa.

## RL en una slide (recordatorio)

```
              ┌─────────┐
              │ Agente  │ ←── reward r_t
              └───┬─────┘
                  │ action a_t
                  ▼
              ┌─────────┐
              │ Entorno │
              └───┬─────┘
                  │ state s_(t+1), reward r_t
                  ▼
              ┌─────────┐
              │ Agente  │ ...
              └─────────┘
```

**DQN**: aprende una función Q(s, a) — "qué recompensa esperada si tomo acción `a` en estado `s`". La política es `argmax_a Q(s, a)`.

## highway-env en una frase

Simulador ligero (CPU-friendly) de autopista con tráfico denso. **DiscreteMetaAction**: 5 acciones (cambio carril izq, cambio carril der, mantener, acelerar, frenar). **Observation**: posiciones y velocidades de N coches cercanos.

Recompensa default:
```
reward = right_lane_bonus * 0.1
       + speed_bonus * 0.4    (proporcional a velocidad)
       - collision_penalty * 1.0
```

## Las 3 lecciones que vas a vivir

✅ **Sample efficiency**: necesitas decenas de miles de timesteps para superar baselines simples. RL es lento.

✅ **Reward hacking**: el agente encuentra atajos que maximizan la métrica sin "conducir bien". Modificar la recompensa cambia el comportamiento de formas a veces no deseadas.

✅ **Sim-to-real gap**: highway-env es **juguete didáctico**. CARLA sería un paso, calle real sería otro. Por eso producción usa híbridos BC + RL fine-tune en sim.

## Lo que NO vamos a hacer

- Compararlo con RL real en CARLA (necesita GPU + 16 GB RAM).
- Entrenar para conseguir SOTA — basta con superar baselines.
- Discutir PPO/A2C/SAC en detalle (DQN es suficiente como demo).

---

Cuando estés listo, abre `02_setup.ipynb`.
