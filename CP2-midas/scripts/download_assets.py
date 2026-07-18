#!/usr/bin/env python3
"""
CP2 — Profundidad Monocular · Descarga de imágenes "depth challenge".

Descarga 5–7 imágenes de Wikimedia Commons (CC) que estresan los modelos
de profundidad monocular: reflejos, túneles, cielo plano, lluvia, niebla,
escena nocturna.

Los modelos (MiDaS, Depth Anything v2) se descargan automáticamente la
primera vez que se carga el notebook 02_setup.ipynb — este script NO los
descarga. Solo imágenes.

Uso (desde la raíz de CP2-midas/):
    python scripts/download_assets.py
    python scripts/download_assets.py --force        # re-descarga si ya existen
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

USER_AGENT = "CODX-AIC-Module-CP2/1.0 (https://github.com/codx-digital/aic)"
DEST_DIR_NAME = "datasets/cp2-depth-extras"

# Cada entrada: (filename_local, search_query, fallback_filename_in_commons_if_known)
QUERIES = [
    ("reflection_glass.jpg",   "modern glass facade building reflection",       None),
    ("wet_road_night.jpg",     "wet street night reflection city",              None),
    ("foggy_road.jpg",         "foggy mountain road morning",                   None),
    ("night_highway.jpg",      "night highway traffic light trails",            None),
    ("clear_sky_highway.jpg",  "highway clear blue sky open road",              "Blue_sky_-_panoramio.jpg"),
    ("rainy_windshield.jpg",   "raindrops on windshield car",                   None),
    ("tunnel_road.jpg",        "tunnel entrance highway dashcam view",          None),
]


def cp2_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _request(url: str, timeout: int = 12):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req, timeout=timeout)


def wm_search(query: str, max_retries: int = 3) -> list[tuple[str, str]]:
    """Busca en Wikimedia Commons y devuelve [(title, image_url), ...]."""
    api = (
        "https://commons.wikimedia.org/w/api.php?"
        "action=query&generator=search&"
        "gsrnamespace=6&"  # NS 6 = File (sin esto la API devuelve páginas de categoría/galería)
        f"gsrsearch={urllib.parse.quote(query)}&"
        "gsrlimit=10&prop=imageinfo&iiprop=url&iiurlwidth=1280&format=json"
    )
    for attempt in range(max_retries):
        try:
            with _request(api) as r:
                data = json.loads(r.read())
            pages = data.get("query", {}).get("pages", {})
            results = []
            for _, info in pages.items():
                title = info.get("title", "")
                # Saltar PDFs, TIFs, SVGs, documents — Wikimedia genera thumb .jpg
                # de PDFs y eso engañaba el filtro de extensión anterior.
                title_low = title.lower()
                if any(title_low.endswith(ext) for ext in (".pdf", ".tif", ".tiff", ".svg", ".djvu")):
                    continue
                ii = info.get("imageinfo", [{}])[0]
                url = ii.get("thumburl") or ii.get("url")
                if url and url.lower().endswith((".jpg", ".jpeg", ".png")):
                    results.append((title, url))
            return results
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"    rate-limited, esperando {wait}s...")
                time.sleep(wait)
                continue
            raise


def wm_resolve(filename_commons: str) -> str | None:
    """Resuelve un nombre de archivo Commons → URL del thumb."""
    api = (
        "https://commons.wikimedia.org/w/api.php?"
        f"action=query&titles=File:{urllib.parse.quote(filename_commons)}&"
        "prop=imageinfo&iiprop=url&iiurlwidth=1280&format=json"
    )
    with _request(api) as r:
        data = json.loads(r.read())
    pages = data.get("query", {}).get("pages", {})
    for _, info in pages.items():
        ii = info.get("imageinfo", [{}])[0]
        return ii.get("thumburl") or ii.get("url")
    return None


def download(url: str, dest: Path) -> None:
    """Descarga sencilla con barra de progreso."""
    dest.parent.mkdir(parents=True, exist_ok=True)

    def _progress(b, bsize, total):
        if total <= 0:
            return
        pct = min(100, b * bsize * 100 // total)
        bar = "#" * (pct // 4) + "-" * (25 - pct // 4)
        sys.stdout.write(f"\r    [{bar}] {pct:3d}%")
        sys.stdout.flush()

    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", USER_AGENT)]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, dest, _progress)
    sys.stdout.write("\n")


def fetch_one(local_name: str, query: str, fallback: str | None, dest_dir: Path, force: bool) -> bool:
    dest = dest_dir / local_name
    if dest.exists() and not force:
        print(f"✅ {local_name}  ya existe, skip")
        return True

    print(f"\n📷 {local_name}  ←  search: '{query}'")

    # Intento 1: search API
    try:
        results = wm_search(query)
        if results:
            title, url = results[0]
            print(f"    encontrado: {title}")
            download(url, dest)
            return True
    except Exception as e:
        print(f"    search falló: {e}")

    # Intento 2: fallback hardcoded si lo hay
    if fallback:
        try:
            url = wm_resolve(fallback)
            if url:
                print(f"    fallback: {fallback}")
                download(url, dest)
                return True
        except Exception as e:
            print(f"    fallback también falló: {e}")

    print(f"    ⚠️  no se pudo descargar {local_name} — sigue con las demás")
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="Re-descarga aunque exista")
    args = parser.parse_args()

    dest_dir = cp2_root() / DEST_DIR_NAME
    print(f"CP2 — Descarga de imágenes 'depth challenge' desde Wikimedia Commons")
    print(f"      Destino: {dest_dir}")

    ok = 0
    for local_name, query, fallback in QUERIES:
        if fetch_one(local_name, query, fallback, dest_dir, args.force):
            ok += 1
        time.sleep(0.5)  # respect Wikimedia rate-limits

    print(f"\n✅ {ok}/{len(QUERIES)} imágenes descargadas en {dest_dir}/")
    if ok < 5:
        print("⚠️  Menos de 5 imágenes — algunas búsquedas fallaron. Comprueba conexión y reintenta con --force.")
        sys.exit(1)


if __name__ == "__main__":
    main()
