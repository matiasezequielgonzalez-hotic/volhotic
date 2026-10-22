"""Convierte png/stickers/*.png a webp/stickers/*.webp (512×512, menos de 100 KB: sirve para WhatsApp)."""
import os

from PIL import Image

raiz = os.path.dirname(os.path.abspath(__file__))
origen, destino = os.path.join(raiz, 'png', 'stickers'), os.path.join(raiz, 'webp', 'stickers')
os.makedirs(destino, exist_ok=True)
for archivo in sorted(os.listdir(origen)):
    imagen = Image.open(os.path.join(origen, archivo)).convert('RGBA')
    salida = os.path.join(destino, archivo.replace('.png', '.webp'))
    for calidad in (90, 80, 70, 60):
        imagen.save(salida, 'WEBP', quality=calidad, method=6)
        if os.path.getsize(salida) < 100 * 1024:
            break
print(len(os.listdir(destino)), 'WebP')
