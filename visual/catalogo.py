"""Arma catalogo.html: una página para ver los íconos, los logos y los stickers juntos."""
import json
import os

raiz = os.path.dirname(os.path.abspath(__file__))
iconos = json.load(open(os.path.join(raiz, 'iconos', 'iconos.json'), encoding='utf-8'))
stickers = json.load(open(os.path.join(raiz, 'stickers', 'stickers.json'), encoding='utf-8'))
sprite = open(os.path.join(raiz, 'iconos', 'sprite.svg'), encoding='utf-8').read()
logos = sorted(f for f in os.listdir(os.path.join(raiz, 'marca')) if f.endswith('.svg') and '_solo' not in f)

celdas_iconos = ''.join(f'<figure><svg aria-hidden="true"><use href="#h-{n}"/></svg><figcaption>{n}</figcaption></figure>'
                        for n in iconos)
celdas_logos = ''.join(f'<figure class="logo"><img src="marca/{f}" alt=""><figcaption>{f}</figcaption></figure>' for f in logos)
celdas_stickers = ''.join(
    f'<h3>{"hottie" if p == "hottie" else "Matías"}</h3><div class="grilla stickers">'
    + ''.join(f'<figure><img src="stickers/{s["archivo"]}" alt="{s["texto"]}"><figcaption>{s["archivo"]}<br>'
              f'<span>{s["uso"]}</span></figcaption></figure>' for s in lista.values())
    + '</div>' for p, lista in stickers.items())

html = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pack visual hotic.</title>
<style>
:root {{ --fondo:#f4f6f8; --tarjeta:#fff; --texto:#111; --suave:#667; --acento:#22c7c9; }}
@media (prefers-color-scheme: dark) {{ :root {{ --fondo:#111317; --tarjeta:#1b1e24; --texto:#f2f2f2; --suave:#99a; }} }}
body {{ margin:0; background:var(--fondo); color:var(--texto); font:14px/1.4 "Helvetica Neue", Helvetica, Arial, sans-serif; }}
main {{ max-width:1100px; margin:0 auto; padding:24px 16px 48px; }}
h1 {{ font-size:32px; margin:0 0 4px; }} h1 b {{ color:var(--acento); }}
h2 {{ margin:36px 0 12px; font-size:20px; }} h3 {{ margin:20px 0 8px; font-size:16px; color:var(--suave); }}
.grilla {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(110px, 1fr)); gap:10px; }}
.grilla.logos {{ grid-template-columns:repeat(auto-fill, minmax(220px, 1fr)); }}
.grilla.stickers {{ grid-template-columns:repeat(auto-fill, minmax(150px, 1fr)); }}
figure {{ margin:0; background:var(--tarjeta); border-radius:10px; padding:12px 8px; text-align:center; }}
figure svg {{ width:32px; height:32px; color:var(--texto); }}
figure:hover svg {{ color:var(--acento); }}
figure img {{ width:100%; height:auto; display:block; }}
figure.logo img {{ height:120px; object-fit:contain; }}
figcaption {{ margin-top:6px; font-size:11px; color:var(--suave); word-break:break-all; }}
figcaption span {{ color:var(--texto); }}
</style></head><body>
{sprite}
<main>
<h1>hotic<b>.</b> pack visual</h1>
<p>{len(iconos)} íconos, {len(logos)} logos y {sum(len(v) for v in stickers.values())} stickers. Todo en SVG; los stickers también en PNG y WebP.</p>
<h2>Íconos</h2><div class="grilla">{celdas_iconos}</div>
<h2>Marca</h2><div class="grilla logos">{celdas_logos}</div>
<h2>Stickers</h2>{celdas_stickers}
</main></body></html>
'''
open(os.path.join(raiz, 'catalogo.html'), 'w', encoding='utf-8').write(html)
print('catalogo.html')
