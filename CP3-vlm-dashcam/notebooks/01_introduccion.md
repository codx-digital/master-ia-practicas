# CP3 · Introducción — VLM + Dashcam

> Lee esto antes de los notebooks. 5 min.

## Lo que viene

Cargar un **VLM (Vision-Language Model) pequeño local** — **Moondream2 ~1.9B** — y pedirle que describa, evalúe y razone sobre 18 imágenes dashcam. **Sin entrenar nada**. Foundation model = "cargar y aplicar".

## Por qué un VLM en este módulo

P6 explicó:
- VLMs son **multimodal**: ven imagen + leen texto + generan respuesta natural.
- En conducción tienen 5 roles: razonamiento de escena, auto-labeling, HMI, planning auxiliar, VLA.
- Limitación clave: **latencia + hallucination** los excluyen del closed-loop control real-time.

Aquí lo tocas:
- Lo bueno: el modelo te dice cosas inteligentes sobre escenas que no ha visto antes.
- Lo malo: **alucina** detalles que no están. Categorizar esto es lo central.

## Local vs Frontier

Usamos un VLM **local** (Moondream2) en lugar de frontier API (Claude/GPT-4V) porque:

1. **Cero coste**: cualquier alumno puede correrlo sin keys.
2. **Reproducible offline**: tras la descarga inicial, no toca red.
3. **Pedagógico**: ver las **limitaciones** del modelo pequeño te ayuda a entender qué hace ganar al frontier.

El **contraste local vs frontier** se discute en el notebook 07 (mini-ensayo).

## 5 lecciones esperadas

✅ **El modelo "ve" cosas con sentido**: describe el entorno, identifica vehículos.
✅ **El modelo "alucina"**: ve cosas que no están (un semáforo en una autopista despejada, por ejemplo).
✅ **Es determinista con greedy**, variable con sampling.
✅ **Falla más en edge cases y trampa**: lo trivial sale bien.
✅ **No es producción safety-critical**: latencia + hallucination → off-line OK, closed-loop NO.

## Lo que NO hacemos

- Fine-tunear el modelo (cae fuera del alcance del módulo).
- Comparar con frontier (opcional como extensión con tu propia key).
- Generar vídeo (Moondream2 es solo imagen estática).

---

Cuando estés listo, abre `02_setup.ipynb`.
