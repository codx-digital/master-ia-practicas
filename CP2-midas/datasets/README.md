# Datasets CP2 — Profundidad monocular

CP2 usa **dos fuentes de imágenes**:

## 1. Imágenes "típicas" → reutilizamos las de CP1

Las 14 imágenes de carretera de [`../../CP1-carriles/datasets/lanes-subset/`](../../CP1-carriles/datasets/lanes-subset/) (Udacity CarND, MIT). Son el grueso del dataset porque ya las tienes si hiciste CP1 — el módulo se mantiene ligero.

Si no tienes CP1 descargado todavía:

```bash
cd ../../CP1-carriles
python scripts/download_assets.py --dataset-only
cd -
```

## 2. Imágenes "depth challenge" → `cp2-depth-extras/`

5–7 imágenes descargadas dinámicamente desde **Wikimedia Commons** (licencia CC). Cada una estresa específicamente algún failure mode del depth monocular:

| Archivo local | Concepto que ataca |
|---------------|--------------------|
| `reflection_glass.jpg`   | Reflejos en cristal — el modelo "ve" el reflejado |
| `wet_road_night.jpg`     | Reflejos en suelo mojado de noche |
| `foggy_road.jpg`         | Pérdida de contraste por niebla |
| `night_highway.jpg`      | Escena nocturna, luces puntuales |
| `clear_sky_highway.jpg`  | Cielo plano sin textura |
| `rainy_windshield.jpg`   | Gotas de agua frente a la cámara |
| `tunnel_road.jpg`        | Túnel con iluminación pobre |

Descarga:

```bash
python scripts/download_assets.py
```

El script usa la **API de Wikimedia Commons** (sin auth, gratis) y busca por query. Si alguna imagen no resuelve, sigue con las demás — necesitas **mínimo 5** para que `02_setup.ipynb` no falle.

**¿Por qué no GH Release como CP1?**

- Las imágenes son pequeñas (~5 MB total) y CC.
- Wikimedia las hostea gratis y permanentemente.
- No queremos congelar el corpus — si en v2 del módulo añadimos más challenges, basta con extender `QUERIES` en el script.
- Reduce el coste operativo (un release menos que mantener).

## Cómo se usan en los notebooks

`02_setup.ipynb` arma una lista combinada:

```python
image_set = []
for cat in ['easy', 'medium', 'hard']:
    for p in (CP1_DATA / cat).glob('*.png'):
        image_set.append({'path': p, 'origin': 'CP1', 'category': cat})
for p in CP2_EXTRAS.glob('*.jpg'):
    image_set.append({'path': p, 'origin': 'CP2_extras', 'category': 'challenge'})
```

Las 4 categorías (`easy`, `medium`, `hard`, `challenge`) se usan en los plots y en el análisis del notebook 06 (failure modes).

## Para el profesor: anti-trampa

Las imágenes `challenge` son **clave para el eje 3 de la rúbrica** (análisis crítico). Si el alumno no menciona ningún failure mode específico de las imágenes Wikimedia, no llegó al notebook 06 o no lo entendió.
