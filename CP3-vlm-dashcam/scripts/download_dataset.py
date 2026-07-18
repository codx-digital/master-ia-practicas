#!/usr/bin/env python3
"""
CP3 — Descarga del dataset dashcam curado.

18 imágenes desde Wikimedia Commons en 6 categorías (3 cada una):
  - trivial            (autopista despejada)
  - urbano_standard    (cruces, peatones visibles)
  - edge_visual        (sol bajo, lluvia, noche)
  - edge_semantic      (ciclista raro, animales, obras)
  - trampa             (algo crítico parcialmente oculto)
  - ambigua            (situación social compleja)

Por cada imagen además crea un `expected_description.md` plantilla que el
profesor o el equipo de curación rellena con la descripción "humana experta".

Uso:
    python scripts/download_dataset.py
    python scripts/download_dataset.py --force
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# Wikimedia exige un User-Agent descriptivo CON información de contacto,
# si no responde 429 ("robot policy"). Formato: nombre/versión (contacto).
USER_AGENT = "AIC-MasterIA-CP3/1.1 (https://github.com/codx-digital/master-ia-practicas; educational use)"
DEST = "datasets/dashcam-curated"

# (local_filename, category, search_query)
QUERIES = [
    # trivial
    ('trivial_01.jpg',          'trivial',         'empty highway daylight'),
    ('trivial_02.jpg',          'trivial',         'straight highway clear weather'),
    ('trivial_03.jpg',          'trivial',         'rural road clear sky driving'),
    # urbano standard
    ('urbano_01.jpg',           'urbano_standard', 'city intersection pedestrian crosswalk'),
    ('urbano_02.jpg',           'urbano_standard', 'urban street crosswalk traffic'),
    ('urbano_03.jpg',           'urbano_standard', 'downtown street pedestrians cars'),
    # edge visual
    ('edge_visual_01.jpg',      'edge_visual',     'driving sunset glare road'),
    ('edge_visual_02.jpg',      'edge_visual',     'night highway car headlights'),
    ('edge_visual_03.jpg',      'edge_visual',     'rainy road driving windshield'),
    # edge semantic
    ('edge_semantic_01.jpg',    'edge_semantic',   'construction work zone road'),
    ('edge_semantic_02.jpg',    'edge_semantic',   'deer animal crossing road'),
    ('edge_semantic_03.jpg',    'edge_semantic',   'cyclist rural road'),
    # trampa
    ('trampa_01.jpg',           'trampa',          'pedestrian behind parked car obscured'),
    ('trampa_02.jpg',           'trampa',          'truck blocking view intersection'),
    ('trampa_03.jpg',           'trampa',          'parked cars side street narrow'),
    # ambigua
    ('ambigua_01.jpg',          'ambigua',         'emergency vehicle ambulance street'),
    ('ambigua_02.jpg',          'ambigua',         'school bus stop pedestrians'),
    ('ambigua_03.jpg',          'ambigua',         'pedestrian street looking phone'),
]


def cp3_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _request(url, timeout=12):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    return urllib.request.urlopen(req, timeout=timeout)


def wm_search(query, max_retries=3):
    """Devuelve [(title, url), ...] de Wikimedia Commons (solo File namespace)."""
    api = ('https://commons.wikimedia.org/w/api.php?'
           'action=query&generator=search&'
           'gsrnamespace=6&'
           f'gsrsearch={urllib.parse.quote(query)}&'
           'gsrlimit=10&prop=imageinfo&iiprop=url&iiurlwidth=1280&format=json')
    for attempt in range(max_retries):
        try:
            with _request(api) as r:
                data = json.loads(r.read())
            results = []
            for _, info in data.get('query', {}).get('pages', {}).items():
                title = info.get('title', '')
                if any(title.lower().endswith(e) for e in ('.pdf', '.tif', '.tiff', '.svg', '.djvu')):
                    continue
                ii = info.get('imageinfo', [{}])[0]
                url = ii.get('thumburl') or ii.get('url')
                if url and url.lower().endswith(('.jpg', '.jpeg', '.png')):
                    results.append((title, url))
            return results
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                time.sleep(2 ** attempt); continue
            raise


def download(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    def _p(b, bsize, total):
        if total <= 0: return
        pct = min(100, b * bsize * 100 // total)
        bar = '#' * (pct // 4) + '-' * (25 - pct // 4)
        sys.stdout.write(f'\r    [{bar}] {pct:3d}%'); sys.stdout.flush()
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', USER_AGENT)]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, dest, _p)
    sys.stdout.write('\n')


def make_expected_template(dest_dir, name, category):
    md = dest_dir / (Path(name).stem + '_expected.md')
    md.write_text(f"""# Expected description — {name} ({category})

> Lo que un humano experto vería en esta imagen. Lo rellena el equipo de curación.

## Descripción humana esperada

(Descripción de 2-3 frases por un humano experto en conducción)

## Objetos críticos

- ...

## Risk score (0-10) y razón

- score: X
- razón: ...

## Decisión recomendada para el conductor

(continuar, frenar, ceder, etc.)
""", encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()

    dest_dir = cp3_root() / DEST
    dest_dir.mkdir(parents=True, exist_ok=True)
    print(f'CP3 — Descarga dashcam dataset')
    print(f'      Destino: {dest_dir}')

    ok, fail = 0, 0
    for local_name, category, query in QUERIES:
        cat_dir = dest_dir / category
        cat_dir.mkdir(exist_ok=True)
        target = cat_dir / local_name
        if target.exists() and not args.force:
            print(f'✅ {category}/{local_name}  ya existe, skip')
            make_expected_template(cat_dir, local_name, category)
            ok += 1
            continue

        print(f'\n📷 {category}/{local_name}  ←  "{query}"')
        try:
            results = wm_search(query)
        except Exception as e:
            print(f'    ERROR de búsqueda: {e}')
            fail += 1; continue

        if not results:
            print(f'    ⚠️  sin resultados para "{query}"')
            fail += 1; continue

        title, url = results[0]
        print(f'    {title[:70]}')
        try:
            download(url, target)
            make_expected_template(cat_dir, local_name, category)
            ok += 1
        except Exception as e:
            print(f'    ERROR descarga: {e}')
            fail += 1

        time.sleep(1.5)   # pausa entre peticiones para no disparar el rate-limit de Wikimedia

    print(f'\n✅ {ok}/{len(QUERIES)} imágenes descargadas en {dest_dir}/')
    if fail > 0:
        print(f'⚠️  {fail} fallaron — re-intenta con --force')
        if ok < 12:
            sys.exit(1)


if __name__ == '__main__':
    main()
