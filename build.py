"""Genera la web a partir de src/.

  - index.html, en/index.html, de/index.html          portada en cada idioma
  - blog/<slug>/index.html (y en/, de/)                una página por artículo
  - feed.xml, en/feed.xml, de/feed.xml                 RSS de cada idioma

Cada artículo vive en src/posts/<slug>/: meta.json (fecha, títulos, descripciones)
y un archivo por idioma (es.html, en.html, de.html) con el cuerpo del texto.
Con "draft": true en meta.json el artículo no se publica.

Uso: python3 build.py            -> web para GitHub Pages
     python3 build.py --preview  -> además preview/ para la vista previa en Claude
"""
import html, json, os, re, sys
from datetime import date

SITE = "https://luisarevalo.es"
FONTS = "https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&display=swap"
LANGS = {
    "es": {"dir": "", "label": "ES",
           "title": "Luis Arévalo Villa · IA, operaciones y aviones",
           "desc": "Ingeniero aeroespacial en Madrid. Escribo sobre lo que aprendo usando la IA para trabajar mejor.",
           "back": "← Volver al blog",
           "months": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
           "months_long": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                           "septiembre", "octubre", "noviembre", "diciembre"],
           "short": "{d} {m} {y}", "long": "{d} de {m} de {y}"},
    "en": {"dir": "en/", "label": "EN",
           "title": "Luis Arévalo Villa · AI, operations and planes",
           "desc": "Aerospace engineer in Madrid. I write about what I learn using AI to work better.",
           "back": "← Back to the blog",
           "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
           "months_long": ["January", "February", "March", "April", "May", "June", "July", "August",
                           "September", "October", "November", "December"],
           "short": "{d} {m} {y}", "long": "{d} {m} {y}"},
    "de": {"dir": "de/", "label": "DE",
           "title": "Luis Arévalo Villa · KI, Operations und Flugzeuge",
           "desc": "Luft- und Raumfahrtingenieur in Madrid. Ich schreibe darüber, was ich lerne, wenn ich KI nutze, um besser zu arbeiten.",
           "back": "← Zurück zum Blog",
           "months": ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Okt.", "Nov.", "Dez."],
           "months_long": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
                           "September", "Oktober", "November", "Dezember"],
           "short": "{d}. {m} {y}", "long": "{d}. {m} {y}"},
}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def fmt_date(iso, code, long=False):
    d = date.fromisoformat(iso)
    L = LANGS[code]
    months = L["months_long"] if long else L["months"]
    return L["long" if long else "short"].format(d=d.day, m=months[d.month - 1], y=d.year)


def load_posts():
    posts = []
    base = "src/posts"
    for slug in sorted(os.listdir(base)) if os.path.isdir(base) else []:
        meta = json.loads(read(f"{base}/{slug}/meta.json"))
        if meta.get("draft"):
            continue
        meta["slug"] = slug
        meta["body"] = {c: read(f"{base}/{slug}/{c}.html") for c in LANGS}
        posts.append(meta)
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def langs_nav(cur, root, sub=""):
    links = []
    for code, L in LANGS.items():
        cur_attr = ' aria-current="true"' if code == cur else ""
        href = (root + L["dir"] + sub) or "./"
        links.append(f'<a href="{href}" hreflang="{code}" lang="{code}"{cur_attr}>{L["label"]}</a>')
    return '<span class="langs" aria-label="Idioma / Language / Sprache">' + "".join(links) + "</span>"


def posts_list(code, posts):
    items = []
    for p in posts:
        t = p[code]
        items.append(
            f'<li><a class="post-link" href="blog/{p["slug"]}/">\n'
            f'          <span class="date">{fmt_date(p["date"], code)}</span>\n'
            f'          <span class="body"><h3>{t["title"]}</h3><p>{t["desc"]}</p></span>\n'
            f'        </a></li>')
    return "\n        ".join(items)


def head(code, title, desc, path, og_type="website", extra=""):
    alt = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{SITE}/{X["dir"]}{path}">' for c, X in LANGS.items())
    feed = f'{SITE}/{LANGS[code]["dir"]}feed.xml'
    url = f'{SITE}/{LANGS[code]["dir"]}{path}'
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
{alt}
<link rel="alternate" hreflang="x-default" href="{SITE}/{path}">
<link rel="alternate" type="application/rss+xml" title="Luis Arévalo Villa" href="{feed}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/foto-luis.jpg">
<meta name="twitter:card" content="summary">{extra}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">"""


def document(code, head_html, body, css, js):
    return f"""<!doctype html>
<html lang="{code}">
<head>
{head_html}
<style>
html {{ -webkit-text-size-adjust: 100%; }}
body {{ margin: 0; }}
img {{ max-width: 100%; }}
[hidden] {{ display: none !important; }}
{css}</style>
</head>
<body>
{body}
<script>
{js}</script>
<script data-goatcounter="https://luisarevalo.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
"""


def home_body(code, posts):
    root = "../" if LANGS[code]["dir"] else ""
    body = read(f"src/body.{code}.html")
    return (body.replace("{{LANGS}}", langs_nav(code, root))
                .replace("{{ROOT}}", root)
                .replace("{{POSTS}}", posts_list(code, posts)))


def post_body(code, post):
    L = LANGS[code]
    root = "../../" + ("../" if L["dir"] else "")
    home = "../../"
    src = read(f"src/body.{code}.html")
    header = src[src.index('<header class="top">'):src.index("</header>") + 9]
    footer = src[src.index("<footer>"):src.index("</footer>") + 9]
    header = re.sub(r'href="#', f'href="{home}#', header)
    header = header.replace("{{LANGS}}", langs_nav(code, root, f'blog/{post["slug"]}/'))
    t = post[code]
    return f"""{header}

<main>
<article class="post">
  <section>
    <div class="wrap">
      <a class="back" href="{home}#blog">{L["back"]}</a>
      <span class="label">{fmt_date(post["date"], code, long=True)} · {t["read"]}</span>
      <h1 class="post-title">{t["title"]}</h1>
      {post["body"][code].strip()}
      <a class="back" href="{home}#blog">{L["back"]}</a>
    </div>
  </section>
</article>
</main>

{footer}"""


def feed(code, posts):
    L = LANGS[code]
    base = f'{SITE}/{L["dir"]}'
    items = []
    for p in posts:
        t = p[code]
        link = f'{base}blog/{p["slug"]}/'
        pub = date.fromisoformat(p["date"]).strftime("%a, %d %b %Y 08:00:00 +0000")
        items.append(f"""  <item>
    <title>{html.escape(t["title"])}</title>
    <link>{link}</link>
    <guid>{link}</guid>
    <pubDate>{pub}</pubDate>
    <description>{html.escape(t["desc"])}</description>
  </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Luis Arévalo Villa</title>
  <link>{base}</link>
  <description>{html.escape(L["desc"])}</description>
  <language>{code}</language>
{chr(10).join(items)}
</channel>
</rss>
"""


def build(out="", css="", js="", posts=()):
    pages = {}
    for code, L in LANGS.items():
        pages[f'{L["dir"]}index.html'] = document(code, head(code, L["title"], L["desc"], ""), home_body(code, posts), css, js)
        pages[f'{L["dir"]}feed.xml'] = feed(code, posts)
        for p in posts:
            t = p[code]
            path = f'blog/{p["slug"]}/'
            extra = f'\n<meta property="article:published_time" content="{p["date"]}">'
            pages[f'{L["dir"]}{path}index.html'] = document(
                code, head(code, f'{t["title"]} · Luis Arévalo Villa', t["desc"], path, "article", extra),
                post_body(code, p), css, js)
    for path, content in pages.items():
        write(os.path.join(out, path), content)
    return pages


def preview_fix(s):
    # El visor de Claude necesita enlaces relativos con index.html explícito.
    def fix(m):
        path, anchor = m.group(1), m.group(2) or ""
        if not path:
            return m.group(0)
        path = "" if path == "./" else path
        return f'href="{path}index.html{anchor}"'
    return re.sub(r'href="((?:\./|(?:\.\./)+)?(?:[a-z0-9-]+/)*)(#[\w-]*)?"', fix, s)


if __name__ == "__main__":
    css, js = read("src/style.css"), read("src/script.js")
    posts = load_posts()
    build("", css, js, posts)
    if "--preview" in sys.argv:
        pages = build("preview", css, js, posts)
        for path in pages:
            if path.endswith(".html"):
                p = os.path.join("preview", path)
                s = preview_fix(read(p))
                if path == "index.html":
                    # La página principal se publica sin esqueleto: Claude lo añade.
                    body = s[s.index("<body>") + 6:s.index("</body>")]
                    style = s[s.index("<style>"):s.index("</style>") + 8]
                    s = (f'<title>Luis Arévalo Villa</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
                         f'<link rel="stylesheet" href="{FONTS}">\n{style}\n{body}')
                write(p, s)
    print("ok:", len(posts), "artículos")
