#!/usr/bin/env python3
"""
CP1 — Detección de Carriles · Descarga de dataset y pesos del modelo.

Descarga desde el GitHub Release `cp1-v1` del repo público `codx-digital/master-ia-practicas`:
  - cp1-lanes-subset.zip      (9.6 MB) → datasets/lanes-subset/
  - cp1-lane-segmenter.onnx  (16.9 MB) → models/cp1-lane-segmenter.onnx

Uso (desde la raíz de CP1-carriles/):
    python scripts/download_assets.py
    python scripts/download_assets.py --force          # re-descarga aunque exista
    python scripts/download_assets.py --dataset-only
    python scripts/download_assets.py --model-only

Repo público → cualquiera puede descargar (con `gh` autenticado o token).

Flujo preferido (más robusto):
    1. Instalar GitHub CLI:  brew install gh  /  apt install gh  /  winget install GitHub.cli
    2. Autenticar:           gh auth login
    3. Ejecutar este script.  Detecta `gh` automáticamente y lo usa.

Fallback (si `gh` no disponible): exporta un Personal Access Token con scope `repo`:
    export GITHUB_TOKEN=ghp_xxxx...
    python scripts/download_assets.py
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional

# ────────────────────────────────────────────────────────────────────────────
#  Configuración del release
# ────────────────────────────────────────────────────────────────────────────

RELEASE_TAG = "cp1-v1"
REPO        = "codx-digital/master-ia-practicas"

ASSETS = {
    "dataset": {
        "filename":      "cp1-lanes-subset.zip",
        "size_mb":       9.6,
        "sha256":        "9103e66b32d7bcbd2a5b7cce4973c7aeadd34b7146acb4a71da1af60611ceb94",
        "extract_to":    Path("datasets"),
        "extract_check": Path("datasets/lanes-subset/easy"),
    },
    "model": {
        "filename":      "cp1-lane-segmenter.onnx",
        "size_mb":       16.9,
        "sha256":        "f714c02c5b8efb71ce24fd33d8d73c32fed98c79f295a9d097dce9fc6d7772fb",
        "extract_to":    Path("models"),
        "extract_check": Path("models/cp1-lane-segmenter.onnx"),
    },
}


# ────────────────────────────────────────────────────────────────────────────
#  Helpers
# ────────────────────────────────────────────────────────────────────────────

def cp1_root() -> Path:
    return Path(__file__).resolve().parent.parent


def sha256_of(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            buf = f.read(chunk)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


def has_gh_cli() -> bool:
    if shutil.which("gh") is None:
        return False
    try:
        r = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=10)
        return r.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def download_via_gh(asset_name: str, dest: Path) -> None:
    """Usa `gh release download` — la opción más robusta para repos privados."""
    print(f"  → vía gh release download")
    print(f"    asset: {asset_name}  →  {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["gh", "release", "download", RELEASE_TAG,
         "-R", REPO,
         "-p", asset_name,
         "--dir", str(dest.parent),
         "--clobber"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"gh falló (rc={r.returncode}):\n{r.stderr}")
    # gh descarga el archivo con su nombre original al --dir
    landed = dest.parent / asset_name
    if landed != dest:
        landed.rename(dest)


def download_via_token(asset_name: str, dest: Path, size_mb: float) -> None:
    """Fallback con GITHUB_TOKEN (Bearer auth a la API de releases)."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise RuntimeError(
            "GITHUB_TOKEN no definido y `gh` CLI no disponible.\n"
            "   Soluciones:\n"
            "     1) brew install gh && gh auth login   (recomendado)\n"
            "     2) export GITHUB_TOKEN=ghp_xxx        (con scope 'repo')"
        )

    # API: GET /repos/{owner}/{repo}/releases/tags/{tag}
    api = f"https://api.github.com/repos/{REPO}/releases/tags/{RELEASE_TAG}"
    req = urllib.request.Request(api, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    })
    import json
    with urllib.request.urlopen(req, timeout=15) as r:
        release_meta = json.loads(r.read())

    asset_meta = next((a for a in release_meta["assets"] if a["name"] == asset_name), None)
    if asset_meta is None:
        raise RuntimeError(f"asset '{asset_name}' no está en release '{RELEASE_TAG}'")

    asset_id = asset_meta["id"]
    asset_url = f"https://api.github.com/repos/{REPO}/releases/assets/{asset_id}"

    print(f"  → vía GITHUB_TOKEN (asset id={asset_id}, {size_mb} MB)")
    print(f"    asset: {asset_name}  →  {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(asset_url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/octet-stream",
    })

    def _progress(b, bsize, total):
        if total <= 0: return
        pct = min(100, b * bsize * 100 // total)
        bar = "#" * (pct // 4) + "-" * (25 - pct // 4)
        sys.stdout.write(f"\r    [{bar}] {pct:3d}%")
        sys.stdout.flush()

    # urlretrieve no acepta headers; usar opener
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ("Authorization", f"Bearer {token}"),
        ("Accept", "application/octet-stream"),
    ]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(asset_url, dest, _progress)
    sys.stdout.write("\n")


def verify_sha256(path: Path, expected: str) -> None:
    actual = sha256_of(path)
    if actual.lower() != expected.lower():
        path.unlink(missing_ok=True)
        raise SystemExit(
            f"❌ sha256 no coincide para {path.name}\n"
            f"   Esperado: {expected}\n"
            f"   Actual:   {actual}\n"
            f"   Archivo borrado. Reintenta con `--force`."
        )
    print(f"    ✅ sha256 verificado")


def unzip_to(zip_path: Path, dest_dir: Path) -> None:
    print(f"    descomprimiendo en {dest_dir}/")
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(dest_dir)


# ────────────────────────────────────────────────────────────────────────────
#  Acciones por asset
# ────────────────────────────────────────────────────────────────────────────

def ensure_dataset(force: bool = False) -> None:
    spec = ASSETS["dataset"]
    root = cp1_root()
    check = root / spec["extract_check"]
    zip_path = root / spec["extract_to"] / spec["filename"]

    if check.exists() and not force:
        n_easy = len(list(check.glob("*.png"))) + len(list(check.glob("*.jpg")))
        print(f"✅ Dataset ya presente ({check} con {n_easy} archivos easy/). Skip.")
        return

    print(f"\n📦 Dataset ({spec['filename']}, {spec['size_mb']} MB)")
    if has_gh_cli():
        download_via_gh(spec["filename"], zip_path)
    else:
        download_via_token(spec["filename"], zip_path, spec["size_mb"])
    verify_sha256(zip_path, spec["sha256"])
    unzip_to(zip_path, root / spec["extract_to"])
    zip_path.unlink(missing_ok=True)
    if not check.exists():
        raise SystemExit(
            f"❌ Tras descomprimir, no encuentro {check}. ¿El ZIP tiene la estructura esperada?"
        )
    print(f"    ✅ dataset listo en {root / spec['extract_to']}/lanes-subset/")


def ensure_model(force: bool = False) -> None:
    spec = ASSETS["model"]
    root = cp1_root()
    dest = root / spec["extract_check"]

    if dest.exists() and not force:
        size_mb = dest.stat().st_size / 1e6
        print(f"✅ Modelo ya presente ({dest}, {size_mb:.1f} MB). Skip.")
        return

    print(f"\n🧠 Modelo DL ({spec['filename']}, {spec['size_mb']} MB)")
    if has_gh_cli():
        download_via_gh(spec["filename"], dest)
    else:
        download_via_token(spec["filename"], dest, spec["size_mb"])
    verify_sha256(dest, spec["sha256"])
    print(f"    ✅ modelo listo en {dest}")


# ────────────────────────────────────────────────────────────────────────────
#  Main
# ────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true",
                        help="Re-descarga aunque el archivo ya exista")
    parser.add_argument("--dataset-only", action="store_true",
                        help="Solo el dataset, no el modelo")
    parser.add_argument("--model-only", action="store_true",
                        help="Solo el modelo, no el dataset")
    args = parser.parse_args()

    if args.dataset_only and args.model_only:
        parser.error("--dataset-only y --model-only son excluyentes")

    os.chdir(cp1_root())
    print(f"CP1 — Descarga de assets desde release '{RELEASE_TAG}' de {REPO}")
    print(f"      Working dir: {Path.cwd()}")
    print(f"      Método: {'gh CLI (auth)' if has_gh_cli() else 'GITHUB_TOKEN env var'}")

    try:
        if not args.model_only:
            ensure_dataset(force=args.force)
        if not args.dataset_only:
            ensure_model(force=args.force)
    except RuntimeError as e:
        raise SystemExit(f"\n❌ {e}")

    print("\n✅ Listo. Abre notebooks/01_setup.ipynb para verificar.")


if __name__ == "__main__":
    main()
