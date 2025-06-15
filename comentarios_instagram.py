##############################################################################
# 📦 1. Instalar el entorno virtual (solo la primera vez)
#
#    $ python3 -m venv .venv
#    $ source .venv/bin/activate            # Windows: .venv\Scripts\activate
#    $ pip install -U \
#          "git+https://github.com/instaloader/instaloader@master" \
#          browser-cookie3
#
# 🍪 2. Generar / actualizar la sesión de Instagram a partir de tus cookies
#
#    $ instaloader -b chrome -f remediosoneshot_experience.session
#      # Cambia “chrome” por firefox / edge / brave, según tu navegador.
#      # El archivo .session se guarda en el directorio actual y el script
#      # lo reutiliza automáticamente en cada ejecución.
#
# 🔑 3. Hash de la query GraphQL para comentarios
#
#      Q_HASH = "97b41c52301f77ce508f55e66d17620e"
#      # Es el hash que Instagram Web usa para la consulta
#      # edge_media_to_parent_comment.  Lo obtienes abriendo la publicación,
#      # pestaña Network → graphql/query y copiando el ?query_hash=…
#      # ⚠️  Si Instagram lo cambia, hay que reemplazarlo aquí.
#
# ▶️ 4. Uso
#
#    $ python ig_commenters.py <url_del_post> remediosoneshot_experience
#
#    El script cargará la sesión, lanzará la consulta GraphQL y mostrará
#    la lista de usuarios que comentaron la publicación.
##############################################################################

import json, instaloader, requests, time
from urllib.parse import urlparse

USER      = "remediosoneshot_experience"
SESSION   = f"{USER}.session"
POST_URL  = "https://www.instagram.com/p/DK2iYjppyyd/?igsh=MWo1aGp2eWhwejdjZw=="
Q_HASH    = "97b41c52301f77ce508f55e66d17620e"      # query-hash de comentarios

L = instaloader.Instaloader(quiet=True)
L.load_session_from_file(USER, SESSION)

# --- Sesión HTTP con cookies válidas (vale para todas las versiones) ----
ctx  = L.context
sess = getattr(ctx, "session", getattr(ctx, "_session", None))
if sess is None:
    raise RuntimeError("No se encontró la sesión HTTP en Instaloader")

shortcode = urlparse(POST_URL).path.strip('/').split('/')[-1]
vars_     = {"shortcode": shortcode, "first": 50}
users     = set()

while True:
    r = sess.get(
        "https://www.instagram.com/graphql/query/",
        params={"query_hash": Q_HASH, "variables": json.dumps(vars_)},
        headers={"x-ig-app-id": "936619743392459"}   # cabecera de la web-app
    ).json()

    edges = r["data"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"]
    users.update(e["node"]["owner"]["username"] for e in edges)

    page = r["data"]["shortcode_media"]["edge_media_to_parent_comment"]["page_info"]
    if not page["has_next_page"]:
        break

    vars_["after"] = page["end_cursor"]          # siguiente página
    time.sleep(0.7)                              # pequeño respiro a IG

print("\n".join(sorted(users)))
