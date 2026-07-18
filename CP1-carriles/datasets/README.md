# Dataset CP1 — Subset Udacity CarND (lane detection)

## Qué hay aquí

14 imágenes de carretera categorizadas por dificultad para detección de carriles:

```
lanes-subset/
├── easy/        ← 5 imágenes: líneas sólidas blancas/amarillas, recta o curva muy suave, buen contraste
├── medium/      ← 5 imágenes: curva más marcada, sombras ligeras, líneas discontinuas a la derecha
├── hard/        ← 4 imágenes: sombras profundas, cambio de carril, contraste reducido
└── metadata.csv ← información de cada imagen
```

Formato: PNG · 1280×720 · RGB

Tamaño total: ~10 MB (ZIP de release: 9.6 MB)

## Origen

Combinación de dos datasets oficiales de Udacity (licencia **MIT**):
- [CarND-LaneLines-P1/test_images](https://github.com/udacity/CarND-LaneLines-P1/tree/master/test_images) — 6 imágenes
- [CarND-Advanced-Lane-Lines/test_images](https://github.com/udacity/CarND-Advanced-Lane-Lines/tree/master/test_images) — 8 imágenes

Razón de elegir este dataset y no TuSimple proper:
- Licencia clara y permisiva (MIT vs CC BY-NC-SA).
- Tamaño manejable (~10 MB total) para empaquetado en GitHub Release.
- Diversidad de dificultad suficiente para el contraste pedagógico clásico vs DL.
- Curvas y sombras de los `test_*.jpg` de Advanced cubren las situaciones donde Canny+Hough falla — ideal para el ejercicio.

**Para v2 del módulo**: si se necesita más volumen, ampliar con un subset curado de BDD100K (también permisivo, soporta segmentación pixel-level para extensiones IoU). Plan documentado en `soluciones/respuestas-referencia.md`.

## Cómo obtenerlo

**Opción 1 — Script automático** (recomendado):

Desde la raíz de `CP1-carriles/`:

```bash
python scripts/download_assets.py
```

Esto descarga desde el GitHub Release `cp1-v1` del repo. Requiere `gh auth` activa (el repo es privado) — el script detecta `gh` y lo usa, o lee `GITHUB_TOKEN` como fallback.

**Opción 2 — Manual** (si el script falla):

1. Asegúrate de tener `gh` autenticado: `gh auth login`.
2. Descarga directa:
   ```bash
   gh release download cp1-v1 -R codx-digital/aic -p cp1-lanes-subset.zip
   unzip cp1-lanes-subset.zip -d datasets/
   ```
3. Verifica:
   ```bash
   ls datasets/lanes-subset/easy/ | wc -l    # Debe dar 5
   ls datasets/lanes-subset/medium/ | wc -l  # Debe dar 5
   ls datasets/lanes-subset/hard/ | wc -l    # Debe dar 4
   ```

**Opción 3 — Generar tú mismo** desde los repos originales de Udacity (lo que hizo este módulo para v1):

```bash
# Bajar las 14 imágenes desde los dos repos de Udacity:
for f in solidWhiteCurve solidWhiteRight solidYellowCurve solidYellowCurve2 solidYellowLeft whiteCarLaneSwitch; do
  curl -sf -O "https://raw.githubusercontent.com/udacity/CarND-LaneLines-P1/master/test_images/$f.jpg"
done
for f in straight_lines1 straight_lines2 test1 test2 test3 test4 test5 test6; do
  curl -sf -O "https://raw.githubusercontent.com/udacity/CarND-Advanced-Lane-Lines/master/test_images/$f.jpg"
done
# Después: convertir a PNG 1280x720 y categorizar manualmente.
```

## metadata.csv

Cada fila describe una imagen:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `filename` | str | Ruta relativa desde `lanes-subset/` |
| `category` | str | easy / medium / hard |
| `weather` | str | clear / cloudy / rain / night |
| `lane_count_gt` | int | Número de carriles visibles (ground truth, anotación humana ligera) |
| `notes` | str | Observaciones cualitativas (sombras, curvatura, oclusión) |

## Para extensiones opcionales

Si quieres ground truth pixel-level para calcular IoU, el TuSimple original incluye `label.json` con anotaciones de puntos por carril. No se incluye en el subset por defecto para mantener el tamaño bajo. Está disponible en el repo original.

---

## Anti-trampa

**No mires `metadata.csv` antes de hacer `02_clasico_canny_hough.ipynb`**. Forma parte del ejercicio identificar tú mismo por qué algunas imágenes son más difíciles.
