"""Stickers de hottie y de Matías en SVG, con borde blanco de sticker.

hottie: pelo negro con mechas rojas, campera negra con paneles turquesa, polera roja, auricular turquesa, pecas.
Matías: corte texturizado con flequillo y degradé, barba corta, campera de jean gris lavada, remera negra,
cadena con un cubo, aro; en "facha", lentes ovalados oscuros.

Cada sticker combina un personaje, una cara (ojos, cejas, boca), una pose de brazos, un accesorio y un
texto. El texto se convierte a trazos con la misma tipografía de la marca (ver marca.py).

Uso: python3 stickers.py   → stickers/<personaje>_<nombre>.svg y stickers/stickers.json
"""
import json
import math
import os

from marca import NEGRITA, texto

TURQUESA, ROJO, TINTA = '#22c7c9', '#d62839', '#13212a'
ANCHO, ALTO = 240, 300

# ---------- personajes ----------

def _hottie():
    pelo, mecha, campera = '#17121a', '#e0303f', '#1c1c22'
    atras = (f'<path d="M54,96 C46,40 88,20 120,20 C152,20 194,40 186,96 C190,128 198,160 206,196 L190,186 '
             f'L194,210 L176,196 L170,206 L162,180 C150,172 90,172 78,180 L70,206 L64,196 L46,210 L50,186 '
             f'L34,196 C42,160 50,128 54,96 Z" fill="{pelo}"/>'
             f'<g fill="none" stroke="{mecha}" stroke-width="6" stroke-linecap="round">'
             f'<path d="M56,120 C50,150 46,172 42,190"/><path d="M184,120 C190,150 194,172 198,190"/></g>')
    cuerpo = (
        f'<rect x="108" y="140" width="24" height="26" fill="#eebba5"/>'
        f'<path d="M98,162 Q120,154 142,162 L148,262 L92,262 Z" fill="#b3202f"/>'
        f'<rect x="103" y="151" width="34" height="15" rx="6" fill="#c62a3a"/>'
        f'<g stroke="#9c1b28" stroke-width="1.5"><path d="M110,153 v11"/><path d="M116,153 v11"/>'
        f'<path d="M122,153 v11"/><path d="M128,153 v11"/><path d="M134,154 v10"/></g>'
        f'<path d="M58,262 L62,204 C64,182 80,170 100,166 L110,184 L112,262 Z" fill="{campera}"/>'
        f'<path d="M182,262 L178,204 C176,182 160,170 140,166 L130,184 L128,262 Z" fill="{campera}"/>'
        f'<path d="M62,204 C66,186 80,174 96,169 L100,180 C86,184 76,194 71,210 Z" fill="{TURQUESA}"/>'
        f'<path d="M178,204 C174,186 160,174 144,169 L140,180 C154,184 164,194 169,210 Z" fill="{TURQUESA}"/>'
        f'<g stroke="#c9ccd2" stroke-width="2" stroke-dasharray="2 2"><path d="M110,186 V262"/><path d="M130,186 V262"/></g>')
    cabeza = ('<path d="M72,95 C72,60 95,48 120,48 C145,48 168,60 168,95 C168,128 148,152 120,152 '
              'C92,152 72,128 72,95 Z" fill="#f9dccb"/>')
    adelante = (
        f'<path d="M64,102 C58,52 88,30 120,30 C152,30 182,52 176,102 L170,86 L163,98 L157,76 L147,90 L140,68 '
        f'L129,84 L121,62 L112,82 L103,66 L94,88 L85,72 L77,96 L71,84 Z" fill="{pelo}"/>'
        f'<path d="M74,84 C64,112 66,142 73,166 L80,150 L81,170 L89,150 C84,130 81,110 83,92 Z" fill="{pelo}"/>'
        f'<path d="M166,84 C176,112 174,142 167,166 L160,150 L159,170 L151,150 C156,130 159,110 157,92 Z" fill="{pelo}"/>'
        f'<g fill="none" stroke="{mecha}" stroke-width="4.5" stroke-linecap="round">'
        f'<path d="M102,40 C94,54 92,66 96,82"/>'
        f'<path d="M76,100 C72,124 73,144 77,160"/><path d="M164,100 C168,124 167,144 163,160"/></g>'
        f'<circle cx="170" cy="114" r="5.5" fill="{TURQUESA}" stroke="#0f2e30" stroke-width="2"/>'
        f'<circle cx="168.5" cy="112.5" r="1.6" fill="#bff6f6"/>')
    return dict(piel='#f9dccb', sombra='#eebba5', ojo='#4f7d78', labios='#c2465a', ceja='#3a1a22',
                rubor=.45, pecas=True, manga=campera, raya=TURQUESA,
                atras=atras, cuerpo=cuerpo, cabeza=cabeza, adelante=adelante, barba='')


def _matias():
    pelo, jean, jean_claro = '#16121a', '#4b4d57', '#5f626d'
    orejas = ('<ellipse cx="73" cy="108" rx="7" ry="11" fill="#d9a27e"/>'
              '<ellipse cx="167" cy="108" rx="7" ry="11" fill="#d9a27e"/>'
              '<circle cx="168" cy="120" r="2.6" fill="none" stroke="#c9ccd2" stroke-width="1.8"/>')
    cuerpo = (
        f'<rect x="108" y="140" width="24" height="26" fill="#c08660"/>'
        f'<path d="M96,160 Q120,170 144,160 L148,262 L92,262 Z" fill="#17171b"/>'
        f'<path d="M101,161 Q120,173 139,161" fill="none" stroke="#2c2c33" stroke-width="3"/>'
        f'<path d="M106,165 Q120,200 134,165" fill="none" stroke="#c9ccd2" stroke-width="1.4"/>'
        f'<g fill="none" stroke="#c9ccd2" stroke-width="1.6" stroke-linejoin="round">'
        f'<path d="M120,196 l7,4 v8 l-7,4 l-7,-4 v-8 z"/><path d="M113,200 l7,4 l7,-4 M120,204 v8"/></g>'
        f'<path d="M58,262 L62,204 C64,182 80,170 100,166 L108,184 L110,262 Z" fill="{jean}"/>'
        f'<path d="M182,262 L178,204 C176,182 160,170 140,166 L132,184 L130,262 Z" fill="{jean}"/>'
        f'<path d="M100,163 L84,172 L96,198 L106,182 Z" fill="{jean_claro}" stroke="#3a3c44" stroke-width="1.5" stroke-linejoin="round"/>'
        f'<path d="M140,163 L156,172 L144,198 L134,182 Z" fill="{jean_claro}" stroke="#3a3c44" stroke-width="1.5" stroke-linejoin="round"/>'
        f'<g fill="none" stroke="#7a7d89" stroke-width="2" stroke-linecap="round" opacity=".6">'
        f'<path d="M68,216 q8,-6 14,2"/><path d="M74,240 q8,-5 16,1"/><path d="M162,222 q8,-6 14,2"/>'
        f'<path d="M156,246 q8,-5 14,1"/></g>'
        f'<g stroke="#c9ccd2" stroke-width="2" stroke-dasharray="2 2"><path d="M108,190 V262"/><path d="M132,190 V262"/></g>')
    cabeza = (orejas + '<path d="M74,92 C74,58 96,46 120,46 C144,46 166,58 166,92 C166,124 150,150 120,152 '
              'C90,150 74,124 74,92 Z" fill="#d9a27e"/>')
    dientes = ''.join(f'L{x},{y} ' for x, y in ((166, 84), (160, 80), (155, 85), (149, 79), (143, 84), (137, 78),
                                                (131, 84), (125, 78), (119, 83), (113, 78), (107, 84), (101, 78),
                                                (95, 84), (89, 79), (83, 85), (78, 81)))
    adelante = (f'<path d="M70,100 C62,50 92,28 120,28 C150,28 180,48 170,100 {dientes}L74,92 Z" fill="{pelo}"/>'
                f'<path d="M71,100 L76,86 L78,108 Z M169,100 L164,86 L162,108 Z" fill="#7a6258" opacity=".55"/>'
                f'<g fill="none" stroke="#3d3440" stroke-width="2" stroke-linecap="round">'
                f'<path d="M96,44 q6,-4 10,2"/><path d="M118,38 q6,-4 10,2"/><path d="M140,46 q6,-4 10,2"/>'
                f'<path d="M106,60 q6,-4 10,2"/><path d="M130,62 q6,-4 10,2"/><path d="M86,66 q5,-4 9,2"/></g>')
    barba = ('<path d="M80,116 C84,140 100,155 120,156 C140,155 156,140 160,116 C152,134 140,146 120,147 '
             'C100,146 88,134 80,116 Z" fill="#2a1d1a" opacity=".42"/>'
             '<path d="M108,130 Q120,124 132,130 Q120,127 108,130 Z" fill="#2a1d1a" opacity=".7"/>'
             '<path d="M112,145 Q120,153 128,145 Q120,149 112,145 Z" fill="#2a1d1a" opacity=".55"/>')
    return dict(piel='#d9a27e', sombra='#c08660', ojo='#4a2e22', labios='#a85a52', ceja='#1b1416',
                rubor=.18, pecas=False, manga=jean, raya=None,
                atras='', cuerpo=cuerpo, cabeza=cabeza, adelante=adelante, barba=barba)


PERSONAJES = {'hottie': _hottie(), 'matias': _matias()}

# ---------- cara ----------

def ojos(tipo, p):
    trazo = f'fill="none" stroke="{TINTA}" stroke-width="3.2" stroke-linecap="round"'
    piezas = []
    for i, ex in enumerate((100, 140)):
        t = tipo[i] if isinstance(tipo, tuple) else tipo
        if t in ('abierto', 'concentrado'):
            piezas.append(f'<ellipse cx="{ex}" cy="110" rx="8" ry="10" fill="{p["ojo"]}"/>'
                          f'<ellipse cx="{ex}" cy="111" rx="4.6" ry="5.6" fill="#13212a"/>'
                          f'<circle cx="{ex - 3}" cy="106" r="2.6" fill="#fff"/>'
                          f'<path d="M{ex - 10},104 Q{ex},96 {ex + 10},103" {trazo}/>')
            if t == 'concentrado':
                piezas.append(f'<path d="M{ex - 11},98 L{ex + 11},98 L{ex + 11},108 Q{ex},104 {ex - 11},108 Z" fill="{p["piel"]}"/>'
                              f'<path d="M{ex - 10},108 Q{ex},104 {ex + 10},108" {trazo}/>')
        elif t == 'sorpresa':
            piezas.append(f'<ellipse cx="{ex}" cy="109" rx="9.5" ry="11.5" fill="#fff" stroke="{TINTA}" stroke-width="2.4"/>'
                          f'<circle cx="{ex}" cy="110" r="4.2" fill="#13212a"/>')
        elif t == 'guino':
            piezas.append(f'<path d="M{ex - 9},111 Q{ex},104 {ex + 9},111" {trazo}/>')
        elif t == 'feliz':
            piezas.append(f'<path d="M{ex - 9},113 Q{ex},101 {ex + 9},113" {trazo}/>')
        elif t == 'cerrado':
            piezas.append(f'<path d="M{ex - 9},108 Q{ex},116 {ex + 9},108" {trazo}/>')
        elif t == 'lentes':
            piezas.append(f'<ellipse cx="{ex}" cy="110" rx="15" ry="8" fill="#1d1a22" stroke="#c9ccd2" stroke-width="1.6"/>'
                          f'<path d="M{ex - 9},107 q4,-3 9,-2" fill="none" stroke="#6a6f7d" stroke-width="2" stroke-linecap="round"/>')
    if tipo == 'lentes':
        piezas.append('<path d="M115,109 Q120,106 125,109" fill="none" stroke="#c9ccd2" stroke-width="1.8"/>'
                      '<path d="M85,108 L74,104 M155,108 L166,104" stroke="#c9ccd2" stroke-width="1.8"/>')
    return ''.join(piezas)


def cejas(tipo, p):
    grosor = 3.6 if p['raya'] is None else 2.6
    trazo = f'fill="none" stroke="{p["ceja"]}" stroke-width="{grosor}" stroke-linecap="round"'
    formas = {
        'normal': ('M91,92 Q100,87 109,90', 'M131,90 Q140,87 149,92'),
        'arriba': ('M91,88 Q100,82 109,85', 'M131,85 Q140,82 149,88'),
        'preocupada': ('M91,93 Q100,91 108,86', 'M132,86 Q140,91 149,93'),
        'decidida': ('M91,88 Q100,89 108,93', 'M132,93 Q140,89 149,88'),
        'picara': ('M91,92 Q100,87 109,90', 'M131,86 Q140,82 149,86'),
    }
    a, b = formas[tipo]
    return f'<path d="{a}" {trazo}/><path d="{b}" {trazo}/>'


def boca(tipo, p):
    trazo = f'fill="none" stroke="{p["labios"]}" stroke-width="3" stroke-linecap="round"'
    formas = {
        'sonrisa': f'<path d="M110,135 Q120,143 130,135" {trazo}/>',
        'picara': f'<path d="M111,137 Q123,142 131,132" {trazo}/>',
        'abierta': '<path d="M108,133 Q120,151 132,133 Z" fill="#7d2030"/><path d="M114,142 Q120,146 126,142" fill="#ff8c98"/>',
        'o': '<ellipse cx="120" cy="139" rx="5" ry="6.5" fill="#7d2030"/>',
        'ups': f'<path d="M108,139 q4,-4 8,0 q4,4 8,0 q4,-4 8,0" {trazo}/>',
        'linea': f'<path d="M113,138 L127,138" {trazo}/>',
    }
    return formas[tipo]


def cara(o, c, b, p):
    pecas = ''.join(f'<circle cx="{x}" cy="{y}" r="1.3" fill="#c98a72"/>'
                    for x, y in ((88, 121), (93, 125), (84, 125), (152, 121), (147, 125), (156, 125),
                                 (115, 122), (125, 122))) if p['pecas'] else ''
    return (f'<ellipse cx="90" cy="127" rx="8" ry="4.5" fill="#ff8a9a" opacity="{p["rubor"]}"/>'
            f'<ellipse cx="150" cy="127" rx="8" ry="4.5" fill="#ff8a9a" opacity="{p["rubor"]}"/>{pecas}'
            f'<path d="M119,119 q2.5,3 -1,5.5" fill="none" stroke="{p["sombra"]}" stroke-width="2" stroke-linecap="round"/>'
            + p['barba'] + ojos(o, p) + cejas(c, p) + boca(b, p))

# ---------- brazos (manga y mano) ----------

def mano(x, y, p):
    return f'<circle cx="{x}" cy="{y}" r="11" fill="{p["piel"]}" stroke="{p["sombra"]}" stroke-width="2"/>'


def manga(d, p, ancho=22):
    raya = (f'<path d="{d}" fill="none" stroke="{p["raya"]}" stroke-width="5" stroke-linecap="round"/>'
            if p['raya'] else '')
    return f'<path d="{d}" fill="none" stroke="{p["manga"]}" stroke-width="{ancho}" stroke-linecap="round"/>' + raya


def pulgar(x, y, p):
    """Puño con el pulgar para arriba."""
    piel, sombra = p['piel'], p['sombra']
    return (f'<rect x="{x - 12}" y="{y - 9}" width="24" height="21" rx="7" fill="{piel}" stroke="{sombra}" stroke-width="2"/>'
            f'<g stroke="{sombra}" stroke-width="1.8" stroke-linecap="round">'
            f'<path d="M{x - 2},{y - 3} h10"/><path d="M{x - 2},{y + 2} h10"/><path d="M{x - 2},{y + 7} h10"/></g>'
            f'<rect x="{x - 12}" y="{y - 24}" width="9" height="20" rx="4.5" fill="{piel}" stroke="{sombra}" stroke-width="2"/>')


def brazos(tipo, p):
    saludo = (manga('M168,206 Q188,180 192,146', p) + mano(193, 138, p)
              + '<g fill="none" stroke="#13212a" stroke-width="2.5" stroke-linecap="round">'
                '<path d="M208,126 q6,6 4,14"/><path d="M214,118 q9,9 6,22"/></g>')
    return {
        'saludo': saludo,
        'arriba': manga('M72,206 Q52,180 48,146', p) + mano(47, 138, p)
                  + manga('M168,206 Q188,180 192,146', p) + mano(193, 138, p),
        'pulgar': manga('M166,216 Q184,216 184,204', p) + pulgar(184, 198, p),
        'menton': manga('M150,262 Q160,190 146,164', p, 20) + mano(142, 156, p),
        'frente': manga('M70,214 Q76,226 90,224', p) + mano(92, 222, p)
                  + manga('M170,214 Q164,226 150,224', p) + mano(148, 222, p),
        'derecha': manga('M168,216 Q180,216 182,202', p) + mano(182, 198, p),
        'ninguno': '',
    }[tipo]

# ---------- accesorios ----------

def estrella(cx, cy, r, color):
    puntos = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * .45
        puntos.append(f'{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}')
    return f'<polygon points="{" ".join(puntos)}" fill="{color}" stroke="#13212a" stroke-width="2.5" stroke-linejoin="round"/>'


def codigo(x, y, ancho=22, alto=16):
    barras = ''.join(f'<path d="M{x + dx},{y + 3} v{alto - 6}"/>' for dx in (3, 6, 8, 12, 15, 18) if dx < ancho - 2)
    return (f'<rect x="{x}" y="{y}" width="{ancho}" height="{alto}" fill="#fff" stroke="#13212a" stroke-width="1.5"/>'
            f'<g stroke="#13212a" stroke-width="1.2">{barras}</g>')


GOTA = '<path d="M64,70 q-8,12 0,16 q8,-4 0,-16 Z" fill="#8fdcf5" stroke="#13212a" stroke-width="2"/>'


def accesorio(tipo, p):
    return {
        'caja': (f'<rect x="84" y="196" width="72" height="54" rx="3" fill="#c8935a" stroke="#13212a" stroke-width="2.5"/>'
                 f'<path d="M84,210 H156" stroke="#a87440" stroke-width="2"/>'
                 f'<rect x="114" y="196" width="12" height="54" fill="#e8c18f" opacity=".8"/>' + codigo(92, 218)),
        'escaner': (f'<path d="M199,190 L206,232 L230,224 Z" fill="{ROJO}" opacity=".28"/>'
                    f'<path d="M199,190 L218,228" stroke="{ROJO}" stroke-width="2.5"/>'
                    + codigo(204, 222, 26, 18)
                    + f'<path d="M172,184 h24 l5,8 h-12 l-6,22 h-10 z" fill="#3a3f48" stroke="#13212a" '
                      f'stroke-width="2.5" stroke-linejoin="round"/><rect x="195" y="186" width="5" height="6" fill="{ROJO}"/>'),
        'reloj': (f'<circle cx="198" cy="56" r="22" fill="#fff" stroke="{ROJO}" stroke-width="5"/>'
                  f'<path d="M198,42 V56 L208,62" fill="none" stroke="#13212a" stroke-width="3" stroke-linecap="round"/>'
                  f'<rect x="192" y="28" width="12" height="6" rx="2" fill="{ROJO}"/>' + GOTA),
        'estrella': estrella(196, 58, 28, '#f2b84b') + estrella(36, 70, 11, TURQUESA) + estrella(214, 116, 9, '#ff7a7a'),
        'confeti': ''.join(f'<rect x="{x}" y="{y}" width="8" height="4" rx="1" fill="{c}" transform="rotate({r} {x} {y})"/>'
                           for x, y, c, r in ((30, 40, TURQUESA, 30), (60, 14, '#f2b84b', -20), (178, 18, '#ff7a7a', 45),
                                              (212, 60, '#a98bff', -35), (22, 96, '#4d8dff', 60), (206, 96, TURQUESA, 10),
                                              (100, 6, '#2fbf71', -50), (150, 8, '#ff6fb5', 25))),
        'idea': ('<circle cx="196" cy="52" r="18" fill="#fff6c9" stroke="#13212a" stroke-width="2.5"/>'
                 '<rect x="189" y="68" width="14" height="10" rx="2" fill="#9aa2ad" stroke="#13212a" stroke-width="2"/>'
                 '<path d="M190,52 q6,-10 12,0" fill="none" stroke="#f2b84b" stroke-width="3" stroke-linecap="round"/>'
                 '<g stroke="#f2b84b" stroke-width="3" stroke-linecap="round"><path d="M196,22 v-6"/>'
                 '<path d="M222,52 h6"/><path d="M164,52 h-6"/><path d="M215,33 l4,-4"/><path d="M177,33 l-4,-4"/></g>'),
        'gota': GOTA,
        'exclamacion': (f'<g fill="{ROJO}" stroke="#13212a" stroke-width="2">'
                        '<rect x="190" y="30" width="9" height="28" rx="4"/><circle cx="194.5" cy="68" r="5"/>'
                        '<rect x="38" y="38" width="8" height="24" rx="4" transform="rotate(-15 42 50)"/>'
                        '<circle cx="46" cy="72" r="4.5"/></g>'),
        'mate': ('<path d="M144,200 q-2,-8 4,-10 h20 q6,2 4,10 q10,14 -2,32 h-24 q-12,-18 -2,-32 z" '
                 'fill="#7a5230" stroke="#13212a" stroke-width="2.5"/>'
                 '<ellipse cx="158" cy="200" rx="14" ry="4" fill="#5d8c3a"/>'
                 '<path d="M162,200 L176,160" stroke="#c9ccd2" stroke-width="4" stroke-linecap="round"/>'
                 '<g fill="none" stroke="#9aa2ad" stroke-width="2.5" stroke-linecap="round" opacity=".8">'
                 '<path d="M188,150 q-6,-8 0,-16 q6,-8 0,-16"/><path d="M200,156 q-6,-8 0,-16 q6,-8 0,-16"/></g>'
                 + mano(150, 222, p)),
        'check': ('<circle cx="198" cy="58" r="22" fill="#2fbf71" stroke="#13212a" stroke-width="2.5"/>'
                  '<path d="M187,58 l8,8 l15,-16" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'),
        'cursor': ('<path d="M168,30 h56 a10,10 0 0 1 10,10 v28 a10,10 0 0 1 -10,10 h-34 l-12,12 v-12 h-10 '
                   'a10,10 0 0 1 -10,-10 v-28 a10,10 0 0 1 10,-10 z" fill="#000"/>'
                   f'<rect x="180" y="44" width="9" height="9" fill="#fff"/><rect x="194" y="58" width="24" height="4" fill="{TURQUESA}"/>'),
        'brillo': ('<g fill="#fff" stroke="#13212a" stroke-width="2" stroke-linejoin="round">'
                   '<path d="M200,40 l4,10 l10,4 l-10,4 l-4,10 l-4,-10 l-10,-4 l10,-4 z"/>'
                   '<path d="M40,60 l3,7 l7,3 l-7,3 l-3,7 l-3,-7 l-7,-3 l7,-3 z"/></g>'),
        'nada': '',
    }[tipo]

# ---------- catálogo ----------

# (texto, ojos, cejas, boca, brazos, accesorio, para qué se usa)
STICKERS = {
    'hottie': {
        'hola': ('¡Hola!', 'abierto', 'arriba', 'sonrisa', 'saludo', 'nada', 'Saludo al entrar'),
        'guino': ('¡Bien ahí!', ('abierto', 'guino'), 'picara', 'picara', 'pulgar', 'nada', 'Respuesta correcta'),
        'festejo': ('¡Pedido perfecto!', 'feliz', 'arriba', 'abierta', 'arriba', 'confeti', 'Pedido sin errores'),
        'ups': ('Ups… revisalo', 'abierto', 'preocupada', 'ups', 'ninguno', 'gota', 'Error en un paso'),
        'pensando': ('Mmm…', 'concentrado', 'normal', 'linea', 'menton', 'idea', 'Pregunta de repaso'),
        'escaneando': ('Escaneá antes', 'concentrado', 'decidida', 'sonrisa', 'ninguno', 'escaner', 'Verificar el producto'),
        'paquete': ('¡Listo para despachar!', 'feliz', 'normal', 'sonrisa', 'frente', 'caja', 'Pedido armado'),
        'apurada': ('¡Se viene el corte!', 'sorpresa', 'decidida', 'o', 'ninguno', 'reloj', 'Aviso de horario de corte'),
        'xp': ('+XP', ('feliz', 'guino'), 'arriba', 'abierta', 'ninguno', 'estrella', 'Suma de experiencia'),
        'ok': ('OK', 'abierto', 'normal', 'sonrisa', 'pulgar', 'check', 'Confirmación'),
        'sorpresa': ('¿¡Qué!?', 'sorpresa', 'arriba', 'o', 'ninguno', 'exclamacion', 'Algo inesperado'),
        'descanso': ('Pausa de mate', 'cerrado', 'normal', 'sonrisa', 'ninguno', 'mate', 'Pausa'),
        'agente': ('Soy un bot', 'abierto', 'normal', 'sonrisa', 'saludo', 'cursor', 'hottie se presenta: hotic._agent'),
    },
    'matias': {
        'hola': ('¡Buenas, equipo!', 'abierto', 'normal', 'sonrisa', 'saludo', 'nada', 'Saludo del día'),
        'facha': ('Así se despacha', 'lentes', 'normal', 'picara', 'pulgar', 'brillo', 'Pedido impecable'),
        'aprobado': ('Aprobado', 'abierto', 'normal', 'picara', 'pulgar', 'check', 'Confirmación'),
        'bien': ('¡Bien ahí!', ('abierto', 'guino'), 'picara', 'picara', 'pulgar', 'nada', 'Felicitación'),
        'festejo': ('¡Récord de ventas!', 'feliz', 'arriba', 'abierta', 'arriba', 'confeti', 'Meta cumplida'),
        'pensando': ('Mmm…', 'concentrado', 'normal', 'linea', 'menton', 'idea', 'Pregunta'),
        'corte': ('¡Al corte, equipo!', 'abierto', 'decidida', 'abierta', 'ninguno', 'reloj', 'Aviso de horario de corte'),
        'paquete': ('¡A despachar!', 'feliz', 'normal', 'sonrisa', 'frente', 'caja', 'Pedido armado'),
        'xp': ('+XP', ('feliz', 'guino'), 'arriba', 'abierta', 'ninguno', 'estrella', 'Suma de experiencia'),
        'revisemos': ('Revisemos eso', 'abierto', 'preocupada', 'linea', 'ninguno', 'gota', 'Algo para corregir'),
        'mate': ('Mate y a laburar', 'cerrado', 'normal', 'sonrisa', 'ninguno', 'mate', 'Arranque del día'),
    },
}


def leyenda(cadena):
    """Cartel negro con el texto en blanco, centrado abajo (estilo hotic._agent)."""
    alto = 20
    _, (x0, _, x1, _) = texto(NEGRITA, cadena, alto, 0, 0)
    ancho = x1 - x0
    trazo, _ = texto(NEGRITA, cadena, alto, (ANCHO - ancho) / 2 - x0, 284)
    pad = 12
    return (f'<rect x="{(ANCHO - ancho) / 2 - pad:.1f}" y="262" width="{ancho + 2 * pad:.1f}" height="32" rx="6" fill="#000"/>'
            f'<path d="{trazo}" fill="#fff"/>')


def sticker(personaje, nombre, datos):
    cadena, o, c, b, pose, extra, _ = datos
    p = PERSONAJES[personaje]
    filtro = f'borde-{personaje}-{nombre}'
    titulo = f'{"hottie" if personaje == "hottie" else "Matías"}: {cadena}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-12 -12 {ANCHO + 24} {ALTO + 24}" '
            f'role="img" aria-label="{titulo}"><title>{titulo}</title>'
            f'<defs><filter id="{filtro}" x="-10%" y="-10%" width="120%" height="120%">'
            f'<feMorphology in="SourceAlpha" operator="dilate" radius="7" result="d"/>'
            f'<feOffset in="d" dy="3" result="o"/><feFlood flood-color="#000" flood-opacity=".22"/>'
            f'<feComposite in2="o" operator="in" result="sombra"/>'
            f'<feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="blanco"/>'
            f'<feMerge><feMergeNode in="sombra"/><feMergeNode in="blanco"/><feMergeNode in="SourceGraphic"/></feMerge>'
            f'</filter></defs>'
            f'<g filter="url(#{filtro})">{p["atras"]}{p["cuerpo"]}{p["cabeza"]}{cara(o, c, b, p)}{p["adelante"]}'
            f'{brazos(pose, p)}{accesorio(extra, p)}{leyenda(cadena)}</g></svg>\n')


def generar(salida):
    os.makedirs(salida, exist_ok=True)
    catalogo = {}
    for personaje, lista in STICKERS.items():
        catalogo[personaje] = {}
        for nombre, datos in lista.items():
            with open(os.path.join(salida, f'{personaje}_{nombre}.svg'), 'w', encoding='utf-8') as f:
                f.write(sticker(personaje, nombre, datos))
            catalogo[personaje][nombre] = {'archivo': f'{personaje}_{nombre}.svg', 'texto': datos[0], 'uso': datos[6]}
    with open(os.path.join(salida, 'stickers.json'), 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=2)
    return sum(len(v) for v in catalogo.values())


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.abspath(__file__))
    print(generar(os.path.join(raiz, 'stickers')), 'stickers')
