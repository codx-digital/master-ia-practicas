# Dataset CP3 — Dashcam curado

## Estructura

```
dashcam-curated/
├── trivial/                    ← 3 imágenes: autopista despejada
├── urbano_standard/            ← 3 imágenes: cruces, peatones visibles
├── edge_visual/                ← 3 imágenes: sol bajo, lluvia, noche
├── edge_semantic/              ← 3 imágenes: animales, obras, ciclistas raros
├── trampa/                     ← 3 imágenes: algo crítico parcialmente oculto
└── ambigua/                    ← 3 imágenes: situación social compleja
```

Cada imagen viene acompañada de un `<nombre>_expected.md` que documenta la **descripción humana esperada** + objetos críticos + risk score + decisión recomendada.

## Cómo se genera

```bash
python scripts/download_dataset.py
```

Descarga imágenes desde Wikimedia Commons (CC) usando la API con `gsrnamespace=6` (File namespace) y filtrado de PDFs/TIFs. ~5 MB total.

## Categorías

| Categoría | Qué busca |
|-----------|-----------|
| `trivial` | Lo trivial — autopista despejada, no debería suponer reto |
| `urbano_standard` | Cruces, peatones — el caso "estándar urbano" |
| `edge_visual` | Iluminación adversa (sol bajo, noche, lluvia) — estresa percepción |
| `edge_semantic` | Categorías raras (animales en carretera, obras, ciclistas) — OOD semántico |
| `trampa` | Algo crítico **parcialmente oculto** (peatón tras coche aparcado) |
| `ambigua` | Situación social compleja (peatón mirando, ambulancia detrás) |

## Para qué se usan

- **Notebook 03**: descripción básica + comparar con expected
- **Notebook 04**: tareas estructuradas (objetos críticos + risk score)
- **Notebook 05**: consistency (greedy vs sampling)
- **Notebook 06**: failure analysis — categorizar tipos de fallo del modelo

## El profesor: anti-trampa

Si una entrega no menciona **ninguna imagen de `trampa` o `ambigua`** en el failure analysis, el alumno se quedó en lo trivial. Eje 3 ≤ 2 pts.

## Limitaciones del dataset

Wikimedia es **fotografía general**, no dashcam profesional. Hay sesgo en:
- Iluminación: bueno mayoritariamente, no escenas nocturnas reales.
- Ángulo: no siempre vista frontal de coche.
- Geografía: Europa y USA sobre-representadas.

Para v2 del módulo, considerar:
- Roboflow datasets de dashcam con licencia abierta.
- Frames de vídeos YouTube CC-licensed.
- Generación con CARLA / GAIA-2 cuando estén accesibles.
