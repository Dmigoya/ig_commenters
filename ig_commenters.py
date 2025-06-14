#!/usr/bin/env python3
"""
ig_commenters.py — Lista todos los usuarios que comentaron en un post de Instagram.

Uso:
    python ig_commenters.py <url_del_post> <tu_usuario_IG>

Requisitos:
    • Instaloader (`brew install instaloader` o `pip install instaloader`).
    • Archivo‑sesión generado con `instaloader -l <user>`.
      ─ El CLI guarda la sesión como `<user>.session` (desde Instaloader 4.12+).
      ─ Si tu versión lo guardó sin extensión, también funciona.

Flujo:
    1. Busca el archivo‑sesión en el cwd y en tu $HOME (con o sin «.session»).
    2. Si existe, lo carga y no pide credenciales.
    3. Si no existe, pide contraseña (+ 2FA), inicia sesión y guarda el archivo
       como `<user>.session` en el cwd para la próxima vez.
"""

from __future__ import annotations

import re
import sys
from getpass import getpass
from pathlib import Path
from urllib.parse import urlparse

import instaloader

# ───────────────────── helpers ──────────────────────────────


def extract_shortcode(url: str) -> str:
    match = re.search(r"/p/([^/]+)/", urlparse(url).path)
    if not match:
        sys.exit("❌  URL de post no válida.")
    return match.group(1)


def session_candidates(username: str) -> list[Path]:
    """Posibles nombres y rutas de la sesión."""
    names = [username, f"{username}.session", f"{username}.json"]
    bases = [Path.cwd(), Path.home()]
    return [base / name for base in bases for name in names]


def ensure_login(loader: instaloader.Instaloader, username: str) -> None:
    # 1) intenta cargar sesión existente
    for sfile in session_candidates(username):
        if sfile.exists():
            loader.load_session_from_file(username, filename=str(sfile))
            return

    # 2) primera vez → login interactivo
    password = getpass(f"🔑  Contraseña de {username}: ")
    try:
        loader.login(username, password)
    except instaloader.TwoFactorAuthRequiredException:
        code = input("🔐  Código 2FA: ").strip()
        loader.two_factor_login(code)

    # 3) guarda la sesión con sufijo .session en cwd
    session_path = Path.cwd() / f"{username}.session"
    loader.save_session_to_file(filename=str(session_path))
    print(f"✅  Sesión guardada en {session_path}\n")


def fetch_commenters(post_url: str, username: str) -> set[str]:
    loader = instaloader.Instaloader(quiet=True, download_pictures=False)
    ensure_login(loader, username)
    post = instaloader.Post.from_shortcode(loader.context, extract_shortcode(post_url))
    return {c.owner.username for c in post.get_comments()}

# ────────────────────── main ────────────────────────────────


def main() -> None:
    if len(sys.argv) < 3:
        print("Uso: python ig_commenters.py <url_del_post> <tu_usuario_IG>")
        sys.exit(1)

    post_url, ig_user = sys.argv[1], sys.argv[2]
    print("⏳  Extrayendo usuarios…")
    try:
        users = fetch_commenters(post_url, ig_user)
    except instaloader.exceptions.InstaloaderException as e:
        sys.exit(f"🚫  Instaloader error: {e}")

    print(f"\n✅  {len(users)} comentaristas encontrados:\n")
    print("\n".join(sorted(users)))


if __name__ == "__main__":
    main()

