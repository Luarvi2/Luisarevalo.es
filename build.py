"""Genera index.html (es), en/index.html y de/index.html a partir de src/.

Uso: python3 build.py            -> web para GitHub Pages
     python3 build.py --preview  -> además preview/ para la vista previa en Claude
"""
import os, sys

SITE = "https://luisarevalo.es"
LANGS = {
    "es": {"dir": "", "label": "ES", "name": "Español",
           "title": "Luis Arévalo Villa · IA, operaciones y aviones",
           "desc": "Ingeniero aeroespacial en Madrid. Escribo sobre lo que aprendo usando la IA para trabajar mejor."},
    "en": {"dir": "en/", "label": "EN", "name": "English",
           "title": "Luis Arévalo Villa · AI, operations and planes",
           "desc": "Aerospace engineer in Madrid. I write about what I learn using AI to work better."},
    "de": {"dir": "de/", "label": "DE", "name": "Deutsch",
           "title": "Luis Arévalo Villa · KI, Operations und Flugzeuge",
           "desc": "Luft- und Raumfahrtingenieur in Madrid. Ich schreibe darüber, was ich lerne, wenn ich KI nutze, um besser zu arbeiten."},
}

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def write(p, s):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)

def langs_nav(cur, root):
    links = []
    for code, L in LANGS.items():
        cur_attr = ' aria-current="true"' if code == cur else ""
        links.append(f'<a href="{(root + L["dir"]) or "./"}" hreflang="{code}" lang="{code}"{cur_attr}>{L["label"]}</a>')
    return '<span class="langs" aria-label="Idioma / Language / Sprache">' + "".join(links) + "</span>"

def body_for(code):
    L = LANGS[code]
    root = "../" if L["dir"] else ""
    body = read(f"src/body.{code}.html")
    return body.replace("{{LANGS}}", langs_nav(code, root)).replace("{{ROOT}}", root)

def page(code, css, js):
    L = LANGS[code]
    alt = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{SITE}/{X["dir"]}">' for c, X in LANGS.items())
    return f"""<!doctype html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{L["title"]}</title>
<meta name="description" content="{L["desc"]}">
<link rel="canonical" href="{SITE}/{L["dir"]}">
{alt}
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:title" content="{L["title"]}">
<meta property="og:description" content="{L["desc"]}">
<meta property="og:url" content="{SITE}/{L["dir"]}">
<meta property="og:image" content="{SITE}/foto-luis.jpg">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&display=swap">
<style>
html {{ -webkit-text-size-adjust: 100%; }}
body {{ margin: 0; }}
img {{ max-width: 100%; }}
[hidden] {{ display: none !important; }}
{css}</style>
</head>
<body>
{body_for(code)}
<script>
{js}</script>
</body>
</html>
"""

def preview(code, css, js):
    # Página principal de la vista previa: sin esqueleto (lo añade Claude al publicar).
    L = LANGS[code]
    return f"""<title>Luis Arévalo Villa</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&display=swap">
<style>
{css}</style>
{body_for(code)}
<script>
{js}</script>
"""

if __name__ == "__main__":
    css, js = read("src/style.css"), read("src/script.js")
    for code, L in LANGS.items():
        write(f'{L["dir"]}index.html', page(code, css, js))
    if "--preview" in sys.argv:
        # El visor de Claude necesita enlaces con index.html explícito.
        fix = lambda s: (s.replace('href="../"', 'href="../index.html"')
                          .replace('href="en/"', 'href="en/index.html"').replace('href="de/"', 'href="de/index.html"')
                          .replace('href="../en/"', 'href="../en/index.html"').replace('href="../de/"', 'href="../de/index.html"')
                          .replace('href="./"', 'href="index.html"'))
        write("preview/index.html", fix(preview("es", css, js)))
        for code in ("en", "de"):
            write(f"preview/{code}/index.html", fix(page(code, css, js)))
    print("ok")
