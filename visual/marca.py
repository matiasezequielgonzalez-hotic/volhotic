"""Logos de hotic. en SVG, con el texto convertido a trazos (no dependen de la tipografía instalada).

Redibujados a partir de los logos originales: wordmark "hotic.", monograma "h.", "h." con la
pronunciación "ho-tic", la marca "._" y "hotic._agent" (hottie). Cada uno en negro y en blanco.

Uso: python3 marca.py   (necesita fonttools y Liberation Sans, la métrica de Arial/Helvetica)
"""
import os

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FUENTES = '/usr/share/fonts/truetype/liberation/'
NEGRITA = TTFont(FUENTES + 'LiberationSans-Bold.ttf')
ITALICA = TTFont(FUENTES + 'LiberationSans-Italic.ttf')
# (color, fondo). 'solo' no tiene fondo y toma el color del texto donde se use (currentColor).
COLORES = {'negro': ('#000', '#fff'), 'blanco': ('#fff', '#000'), 'solo': ('currentColor', None)}


def texto(fuente, cadena, alto, x, y, espaciado=0.0):
    """Path SVG del texto, con la línea de base en y. alto = tamaño en unidades del dibujo."""
    glifos = fuente.getGlyphSet()
    cmap = fuente.getBestCmap()
    escala = alto / fuente['head'].unitsPerEm
    trazo, limites = SVGPathPen(glifos), BoundsPen(glifos)
    for letra in cadena:
        nombre = cmap[ord(letra)]
        matriz = (escala, 0, 0, -escala, x, y)
        glifos[nombre].draw(TransformPen(trazo, matriz))
        glifos[nombre].draw(TransformPen(limites, matriz))
        x += glifos[nombre].width * escala + espaciado * alto
    return trazo.getCommands(), limites.bounds


def svg(nombre, piezas, margen, color, fondo, cuadrado=False):
    """piezas: lista de (path, bounds) o ('rect', (x0, y0, x1, y1))."""
    caja = [min(p[1][0] for p in piezas), min(p[1][1] for p in piezas),
            max(p[1][2] for p in piezas), max(p[1][3] for p in piezas)]
    ancho, alto = caja[2] - caja[0] + 2 * margen, caja[3] - caja[1] + 2 * margen
    x0, y0 = caja[0] - margen, caja[1] - margen
    if cuadrado:
        lado = max(ancho, alto)
        x0 -= (lado - ancho) / 2
        y0 -= (lado - alto) / 2
        ancho = alto = lado
    cuerpo = ''.join(
        f'<rect x="{b[0]:.1f}" y="{b[1]:.1f}" width="{b[2] - b[0]:.1f}" height="{b[3] - b[1]:.1f}"/>' if p == 'rect'
        else f'<path d="{p}"/>' for p, b in piezas)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {ancho:.1f} {alto:.1f}" '
            f'role="img" aria-label="{nombre}"><title>{nombre}</title>'
            + (f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{ancho:.1f}" height="{alto:.1f}" fill="{fondo}"/>' if fondo else '')
            + f'<g fill="{color}">{cuerpo}</g></svg>\n')


def logos():
    """Devuelve {archivo: (titulo, piezas, margen, cuadrado)}."""
    wordmark = [texto(NEGRITA, 'hotic.', 100, 0, 0, -0.01)]
    monograma = [texto(NEGRITA, 'h.', 100, 0, 0, 0.06)]
    monograma_ho_tic = monograma + [texto(ITALICA, 'ho-tic', 30, 6, 52, 0.04)]
    agente = [texto(NEGRITA, 'hotic._agent', 100, 0, 0, -0.01)]
    # La marca "._": el punto cuadrado y el guion bajo, como un cursor.
    marca = [('rect', (0, 0, 70, 73)), ('rect', (113, 115, 388, 143))]
    return {
        'hotic': ('hotic.', wordmark, 30, False),
        'hotic_cuadrado': ('hotic.', wordmark, 30, True),
        'h': ('h.', monograma, 22, True),
        'h_ho-tic': ('h. ho-tic', monograma_ho_tic, 22, True),
        'cursor': ('hotic. ._', marca, 110, True),
        'hotic_agent': ('hotic._agent', agente, 30, False),
        'hotic_agent_cuadrado': ('hotic._agent', agente, 30, True),
    }


def generar(salida):
    os.makedirs(salida, exist_ok=True)
    n = 0
    for archivo, (titulo, piezas, margen, cuadrado) in logos().items():
        for variante, (color, fondo) in COLORES.items():
            with open(os.path.join(salida, f'{archivo}_{variante}.svg'), 'w', encoding='utf-8') as f:
                f.write(svg(titulo, piezas, margen, color, fondo, cuadrado))
            n += 1
    return n


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.abspath(__file__))
    print(generar(os.path.join(raiz, 'marca')), 'logos')
