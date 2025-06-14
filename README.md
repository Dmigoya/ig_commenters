# IG Commenters 📸🗒️

Un script en Python para **extraer la lista de usuarios que han comentado en cualquier post de Instagram** usando la librería [Instaloader](https://instaloader.github.io/).

---

## 📂 Contenido del repo

| Archivo            | Descripción                                                 |
| ------------------ | ----------------------------------------------------------- |
| `ig_commenters.py` | Script principal que devuelve los comentaristas de un post. |
| `README.md`        | Esta guía de instalación y uso.                             |
|                    |                                                             |

---

## ⚙️ Requisitos

* **Python 3.8+**
* **Instaloader** (CLI + librería Python)
* Una cuenta de Instagram válida (para generar la sesión).

> **Nota macOS/Homebrew**: si usas el Python de Homebrew te mostrará el error *externally-managed-environment* al hacer `pip install`. Sigue los pasos del apartado *Entorno virtual* o usa `pipx`.

---

## 🚀 Instalación y entorno

### 1. Clona el repo

```bash
git clone https://github.com/tu_usuario/ig-commenters.git
cd ig-commenters
```

### 2. Crea un entorno virtual (recomendado)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install instaloader
```

> Si prefieres **`pipx`**:
>
> ```bash
> brew install pipx        # una vez
> pipx install instaloader
> ```

### 3. Genera tu archivo‐sesión de Instagram (una sola vez)

```bash
instaloader -l TU_USUARIO_IG
```

* Introduce tu contraseña.
* Si tienes 2FA, ingresa el código cuando lo pida.
* Esto creará `TU_USUARIO_IG.session` en el directorio actual.
* **No subas este archivo a Git ni lo compartas.** Añade `*.session` a tu `.gitignore`.

Si ya lo habías generado antes, simplemente copia el archivo `.session` al directorio del proyecto.

---

## 🏃‍♂️ Uso

```bash
python ig_commenters.py 'https://www.instagram.com/p/SHORTCODE/' TU_USUARIO_IG
```

* El script buscará el archivo de sesión (`TU_USUARIO_IG.session` o variantes) en el directorio actual y en tu `$HOME`.
* Si no lo encuentra, pedirá la contraseña (y 2FA) y lo guardará.
* Devuelve en pantalla la lista única de usuarios que comentaron en el post.

> Redirige la salida a un archivo si lo necesitas:
>
> ```bash
> python ig_commenters.py 'URL' TU_USUARIO_IG > commenters.txt
> ```

---

## 📜 Licencia

MIT. Consulta el archivo `LICENSE` si lo añades.

---

## 🤝 Contribuciones

¡Pull requests bienvenidos! Abre un *issue* si encuentras algún problema o quieres proponer mejoras.

---

## ☕ Créditos

* [Instaloader](https://github.com/instaloader/instaloader) por el motor de scraping.
* Inspirado y mantenido por **David Migoya**

---

> **⚠️ Descargo de responsabilidad**: Utiliza este script respetando los términos de servicio de Instagram. El autor no se hace responsable del uso indebido.

