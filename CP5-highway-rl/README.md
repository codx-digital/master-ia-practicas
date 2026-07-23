# CP5 — highway-env + RL: Agente autónomo en simulador

> Caso práctico 5 (final) del módulo "IA Aplicada al Vehículo Autónomo"
> Máster en IA · AIC × Universidad de Monterrey · 2026

---

## Lo que vas a hacer

Entrenar un agente **DQN** que aprende a conducir en `highway-env` **explorando**, no imitando. Vivir los puntos dolorosos clásicos de RL — recompensa sparse, sample inefficiency, **reward hacking** — y entender por qué la industria no despliega RL puro.

1. **Explorar** el entorno highway-env (observación, acciones, recompensa).
2. **Baselines**: random + rule-based simple.
3. **DQN** con `stable-baselines3` (~8–10 min CPU, 40k timesteps).
4. **Evaluación** sobre 50 episodios deterministic.
5. **Reward shaping**: modificar la recompensa y ver cómo cambia el comportamiento.

**Duración estimada**: 45–60 min · **Sin GPU** · 8 GB RAM.

---

## Por qué este CP

P4 (bloque 3) explicó:
- RL captura comportamientos sociales que reglas no.
- Pero: reward sparse, safety durante exploración, sim-to-real gap.
- Por eso producción usa **híbridos** (BC + RL fine-tuning).

CP5 te hace tocar esos puntos en código. Es el **complemento de CP4** — mismo entorno, paradigma opuesto.

---

## Estructura

```
CP5-highway-rl/
├── README.md                              ← estás aquí
├── requirements.txt
├── rubrica.md
├── notebooks/
│   ├── 01_introduccion.md
│   ├── 02_setup.ipynb                     ← imports + smoke test
│   ├── 03_entorno.ipynb                   ← obs, action, reward, rollout random
│   ├── 04_baselines.ipynb                 ← random + rule-based
│   ├── 05_dqn_entrenamiento.ipynb         ← DQN con stable-baselines3
│   ├── 06_evaluacion.ipynb                ← métricas + vídeo
│   ├── 07_reward_shaping.ipynb            ← modificar recompensa + observar
│   └── 08_preguntas.md
├── models/                                ← donde se guardan modelos entrenados
└── soluciones/                            ← referencia profesor
```

---

## Requisitos previos

- Python 3.10+, 8 GB RAM, sin GPU.
- (Recomendado) Haber hecho **CP4** antes — mismo entorno, vale la familiaridad.
- (Opcional) `ffmpeg` para grabar vídeos de evaluación (sino, el notebook produce GIFs).

---

## Setup paso a paso

### 1. Entorno virtual y dependencias

```bash
cd CP5-highway-rl
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Verifica entorno

```bash
jupyter notebook notebooks/02_setup.ipynb
```

Al final debe imprimir `✅ Setup OK — listo para 03`.

---

## Orden recomendado

| Notebook | Tiempo | Qué hace |
|----------|--------|----------|
| `02_setup` | 1 min | Imports + smoke test del entorno |
| `03_entorno` | 5 min | Explorar obs/action/reward + rollout random |
| `04_baselines` | 5 min | Random + rule-based, tabla comparativa |
| `05_dqn_entrenamiento` | 8-10 min | DQN 40k timesteps + learning curve |
| `06_evaluacion` | 5 min | 50 episodios deterministic + vídeos + tabla |
| `07_reward_shaping` | 8 min | Modificar reward + entrenar +10k + comparar |
| `08_preguntas` (md) | 10 min | Responder 5 preguntas |

**Total**: ~45 min activos.

---

## Entregable

PDF con:

1. Curva de aprendizaje DQN.
2. **Tabla comparativa** random vs rule-based vs DQN sobre 50 episodios (return medio, % éxito, % colisión).
3. Capturas (o vídeo/GIF) de 1 episodio del DQN.
4. **Análisis del reward shaping**: comportamiento antes/después + posible reward hacking.
5. Respuestas a las 5 preguntas.
6. (Opcional) Extensiones.

**Subir a**: Moodle de AIC, sección "CP5". Nombre: `cp5_<apellido>_<nombre>.pdf`. Plazo 48 h.

Evaluación: [rúbrica](rubrica.md). Máximo 16 pts.

---

## FAQ rápido

**¿Y si highway-env y gymnasium dan conflicto?**
Las versiones de `requirements.txt` están pineadas y validadas. Si quieres versiones más recientes, prueba antes en `02_setup.ipynb`.

**¿Puedo usar PPO en vez de DQN?**
Sí — extensión opcional. PPO funciona mejor con `ContinuousAction`. Cubierto en CP4 indirectamente (acción continua).

**¿Por qué no CARLA?**
CARLA es **mucho más costoso** computacionalmente (GPU + 16 GB RAM). highway-env es **didáctico** — el mensaje del CP es que RL funciona en juguete y los retos del mundo real son otros.

**Conexión con CP4**:
Mismo entorno highway-env. Comparar trayectorias **BC (CP4) vs RL (CP5)** es una extensión brutal — distingue alumnos avanzados.
