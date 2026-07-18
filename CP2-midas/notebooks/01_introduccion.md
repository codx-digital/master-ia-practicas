# CP2 · Introducción — Profundidad monocular con foundation models

> Lee esto antes de tocar los notebooks. 5 min.

## Lo que viene

Vas a usar dos modelos pre-entrenados (sin entrenar nada) que predicen profundidad a partir de **una sola imagen RGB**:

- **MiDaS small** (Intel, 2022 — refinado 2024). La referencia clásica.
- **Depth Anything v2 small** (HKU + TikTok, 2024). El SOTA actual.

Ambos son ~22–24 MB. Corren en CPU en 1–3 segundos por imagen.

## Por qué importa

Un LiDAR del segmento medio cuesta **500–2000 €** por unidad. Si tu coche usa 4–8 → **2.000–16.000 € por vehículo solo en sensores**. Multiplica por **1 millón** de coches al año y tienes 2.000–16.000 millones de euros en hardware.

Si un modelo que cabe en 24 MB y corre en cualquier CPU te da profundidad **suficientemente buena**, te ahorras todo eso.

Tesla apuesta exactamente esto. **Toda su pila de percepción 2026 es camera-only**.

La pregunta de este CP es: **¿cómo de "suficientemente buena" es esta profundidad?** Spoiler — **depende, y es importante saber dónde**.

## Conceptos que vas a tocar

| Concepto | Donde aparece |
|----------|----------------|
| Profundidad **inverse** (más cerca = mayor valor) | `03_midas_basico.ipynb` |
| Profundidad **relativa** vs **métrica** | `04_relativa_vs_metrica.ipynb` |
| Foundation model — **zero-shot OOD** | implícito en todo |
| Failure modes específicos del dominio | `06_failure_modes.ipynb` |
| **Calibración** de relativo a métrico (naïve) | `04` |

## La trampa del depth monocular

Imagina dos escenas idénticas excepto el tamaño:
1. Una calle real de 4 m de ancho.
2. Una maqueta a escala 1:10 de esa misma calle.

Una foto **monocular** de cada una se ve **exactamente igual** (porque la geometría es idéntica). El modelo no sabe distinguir.

**Conclusión**: un foundation model monocular **no puede dar metros reales** sin información adicional (cámara estéreo, IMU, tamaño conocido de algún objeto, mapa HD…). Esto es geometría, no limitación del modelo. La cubrimos en detalle en `04_relativa_vs_metrica.ipynb`.

## Lo que NO vamos a hacer (cubierto en P3)

- Fusión de depth monocular con LiDAR sparse para obtener métrica.
- Proyección del depth map a representación BEV.
- Calibración intrínseca de cámara desde un patrón ajedrez.

Esto cae en P3 (Fusión) y en CPs futuros. Aquí nos quedamos con el modelo "por sí solo".

---

Cuando estés listo, abre `02_setup.ipynb`.
