# luisarevalo.es

Web personal de Luis Arévalo Villa: su historia, su experiencia y un blog sobre lo que aprende usando la IA.

Se publica con GitHub Pages en https://luisarevalo.es

## Cómo se edita

El contenido está en `src/`: un archivo por idioma (`body.es.html`, `body.en.html`, `body.de.html`), más `style.css` y `script.js`.
Los artículos del blog están en `src/posts/<slug>/`: `meta.json` (fecha, título, descripción y tiempo de lectura en cada idioma) y un archivo por idioma con el texto. Con `"draft": true` un artículo no se publica.

Después de cambiar algo, ejecuta `python3 build.py`: regenera las portadas, una página por artículo y el RSS (`feed.xml`) de cada idioma.
