"""Set de íconos hotic.: línea de 2 px, puntas redondeadas, grilla de 24×24.
Todos usan currentColor, así que toman el color del texto donde se pongan.
Genera visual/iconos/<nombre>.svg, visual/iconos/sprite.svg (todos como <symbol>) y visual/iconos/iconos.json."""
import json
import os

# nombre -> (etiqueta, contenido SVG dentro de la grilla 24×24)
ICONOS = {
    # Panel
    'inventario': ('Inventario', '<path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/>'),
    'plano': ('Plano', '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 10h7v11"/><path d="M14 3v7h7"/>'),
    'equipo': ('Equipo', '<circle cx="9" cy="8" r="4"/><path d="M2 21c0-4 3-7 7-7s7 3 7 7"/><path d="M16 4a4 4 0 0 1 0 8"/><path d="M22 21c0-3-2-5-4-6"/>'),
    'importar': ('Importar', '<path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M4 21h16"/>'),
    'escuela': ('Escuela', '<path d="M2 9l10-5 10 5-10 5-10-5z"/><path d="M6 11v5c0 1.5 3 3 6 3s6-1.5 6-3v-5"/><path d="M22 9v6"/>'),
    'sex': ('Sexhotic', '<path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/>'),
    'hottie': ('hottie', '<path d="M5 13v-2a7 7 0 0 1 14 0v2"/><rect x="3.5" y="12" width="3.5" height="5" rx="1.2"/><rect x="17" y="12" width="3.5" height="5" rx="1.2"/><path d="M19 17c0 2-2 3.5-5 3.5h-1.5"/>'),
    'sala': ('Sala 3D', '<rect x="2" y="7" width="20" height="11" rx="4"/><path d="M7 11v3"/><path d="M5.5 12.5h3"/><circle cx="15.5" cy="11.5" r="1"/><circle cx="18" cy="14" r="1"/>'),
    # Stock y depósito
    'buscar': ('Buscar', '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>'),
    'stock': ('Stock', '<rect x="3.5" y="13" width="7" height="7" rx="1"/><rect x="13.5" y="13" width="7" height="7" rx="1"/><rect x="8.5" y="5" width="7" height="7" rx="1"/>'),
    'ubicacion': ('Ubicación', '<path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>'),
    'estanteria': ('Estantería', '<path d="M4 3v18"/><path d="M20 3v18"/><path d="M4 9h16"/><path d="M4 15h16"/><path d="M7 6.5h4"/><path d="M13 12.5h4"/><path d="M7 18.5h5"/>'),
    'piso': ('Pisos', '<path d="M12 3l9 4.5-9 4.5-9-4.5L12 3z"/><path d="M3 12l9 4.5 9-4.5"/><path d="M3 16.5L12 21l9-4.5"/>'),
    'numero_pieza': ('Número de pieza', '<path d="M12 2.5l8.5 4.8v9.4L12 21.5l-8.5-4.8V7.3z"/><circle cx="12" cy="12" r="3.5"/>'),
    'no_lo_encontre': ('No lo encontré', '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/><path d="M8.5 8.5l5 5"/><path d="M13.5 8.5l-5 5"/>'),
    # Pedido: de la venta al despacho
    'venta': ('Venta', '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8"/><path d="M12 16v4"/><path d="M8 9l2.5 2.5L16 7"/>'),
    'pedido': ('Pedido', '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2V3z"/><path d="M9 8h6"/><path d="M9 12h6"/><path d="M9 16h3"/>'),
    'etiqueta': ('Etiqueta', '<rect x="4" y="5" width="16" height="14" rx="2"/><path d="M8 9v6"/><path d="M10.5 9v6"/><path d="M13 9v6"/><path d="M16 9v6"/>'),
    'imprimir': ('Imprimir', '<path d="M7 9V3h10v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M7 14h10v7H7z"/>'),
    'caja': ('Caja', '<path d="M3 8h18v12H3z"/><path d="M3 8l2.5-4h13L21 8"/><path d="M10 4v7h4V4"/>'),
    'cinta': ('Cinta', '<circle cx="9" cy="11" r="6"/><circle cx="9" cy="11" r="2"/><path d="M15 11h6v4h-6"/>'),
    'proteger': ('Proteger', '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/><path d="M9 12l2 2 4-4"/>'),
    'canasto': ('Canasto', '<path d="M4 9h16l-1.6 11H5.6L4 9z"/><path d="M8 9l3-5"/><path d="M16 9l-3-5"/><path d="M9 13v4"/><path d="M12 13v4"/><path d="M15 13v4"/>'),
    'colecta': ('Colecta', '<path d="M2 6h12v10H2z"/><path d="M14 10h4l3 3v3h-7z"/><circle cx="6.5" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>'),
    'flex': ('Flex', '<circle cx="5.5" cy="17" r="3"/><circle cx="18.5" cy="17" r="3"/><path d="M5.5 17l4-6h5l4 6"/><path d="M9.5 11L8.5 8H6"/><path d="M14.5 11l1.5-4h3"/>'),
    'full': ('Full', '<path d="M3 21V9l9-5 9 5v12"/><path d="M7 21v-7h10v7"/><path d="M7 17.5h10"/>'),
    'punto_despacho': ('Punto de despacho', '<path d="M4 10h16"/><path d="M5 10l1-5h12l1 5"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>'),
    'corte': ('Horario de corte', '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2"/><path d="M9 2h6"/>'),
    'pack': ('Pack', '<path d="M2 10h9v9H2z"/><path d="M13 10h9v9h-9z"/><path d="M7 4h10v6H7z"/>'),
    'reciclaje': ('Reciclaje', '<path d="M7 19H4.5l2.8-5"/><path d="M9.8 5.2L12 2l2.2 3.2"/><path d="M17 19h2.5l-2.8-5"/><path d="M8 19h8"/><path d="M5.5 13.5L9 8"/><path d="M18.5 13.5L15 8"/>'),
    # Reputación y comprador
    'reputacion': ('Reputación', '<path d="M4 18a8 8 0 1 1 16 0"/><path d="M12 18l4-5"/><circle cx="12" cy="18" r="1.2"/>'),
    'reclamo': ('Reclamo', '<path d="M4 5h16v11H9l-5 4V5z"/><path d="M12 8v4"/><path d="M12 14.5v.01"/>'),
    'mensaje': ('Mensaje', '<path d="M4 5h16v11H9l-5 4V5z"/><path d="M8 9.5h8"/><path d="M8 12.5h5"/>'),
    'devolucion': ('Devolución', '<path d="M9 14l-4-4 4-4"/><path d="M5 10h9a5 5 0 0 1 0 10h-3"/>'),
    'cancelacion': ('Cancelación', '<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/>'),
    'factura': ('Factura', '<path d="M6 3h9l4 4v14H6V3z"/><path d="M15 3v4h4"/><path d="M9 12h7"/><path d="M9 16h7"/><path d="M9 8h3"/>'),
    # Publicaciones
    'publicacion': ('Publicación', '<path d="M3 12V4h8l10 10-8 8L3 12z"/><circle cx="7.5" cy="7.5" r="1.5"/>'),
    'foto': ('Foto', '<path d="M4 8h3l2-3h6l2 3h3v11H4V8z"/><circle cx="12" cy="13" r="3.5"/>'),
    'titulo': ('Título', '<path d="M5 5h14"/><path d="M12 5v14"/><path d="M9 19h6"/>'),
    'compatibilidad': ('Compatibilidad', '<path d="M3 15l2-5.5A2 2 0 0 1 6.9 8h10.2a2 2 0 0 1 1.9 1.5L21 15v4H3v-4z"/><path d="M3 15h18"/><circle cx="7" cy="17.5" r="1"/><circle cx="17" cy="17.5" r="1"/>'),
    'catalogo': ('Catálogo', '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>'),
    # Juego y progreso
    'xp': ('XP', '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>'),
    'nivel': ('Nivel', '<path d="M12 3l2.7 5.5 6 .9-4.4 4.2 1 6L12 16.8 6.7 19.6l1-6-4.4-4.2 6-.9L12 3z"/>'),
    'racha': ('Racha', '<path d="M12 22c4 0 7-2.8 7-7 0-3.5-2.5-5.5-3.5-8.5-1 1.8-2.2 2.8-3.8 3 .8-2.4.3-5-1.7-7.5-.8 4-4 6.2-4 11 0 4.6 2.6 9 6 9z"/>'),
    'trofeo': ('Trofeo', '<path d="M8 4h8v5a4 4 0 0 1-8 0V4z"/><path d="M8 6H5a3 3 0 0 0 3 4"/><path d="M16 6h3a3 3 0 0 1-3 4"/><path d="M12 13v4"/><path d="M9 21h6"/><path d="M10 17h4v4h-4z"/>'),
    'ranking': ('Ranking', '<path d="M3 21v-7h6v7"/><path d="M9 21V9h6v12"/><path d="M15 21v-5h6v5"/>'),
    'desafio': ('Desafío', '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>'),
    'repaso': ('Repaso', '<path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>'),
    'leccion': ('Lección', '<path d="M4 4h6a3 3 0 0 1 2 1 3 3 0 0 1 2-1h6v15h-6a2 2 0 0 0-2 2 2 2 0 0 0-2-2H4V4z"/><path d="M12 5v16"/>'),
    'check': ('Bien', '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.5 2.5L16 9.5"/>'),
    'error': ('Error', '<circle cx="12" cy="12" r="9"/><path d="M9 9l6 6"/><path d="M15 9l-6 6"/>'),
    'alerta': ('Alerta', '<path d="M12 3l10 17H2L12 3z"/><path d="M12 10v4"/><path d="M12 17v.01"/>'),
    'fuente': ('Fuente oficial', '<path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/>'),
}

ATRIBUTOS = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'


def generar(salida):
    os.makedirs(salida, exist_ok=True)
    simbolos = []
    for nombre, (etiqueta, cuerpo) in ICONOS.items():
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" {ATRIBUTOS} '
               f'role="img" aria-label="{etiqueta}"><title>{etiqueta}</title>{cuerpo}</svg>\n')
        with open(os.path.join(salida, nombre + '.svg'), 'w', encoding='utf-8') as f:
            f.write(svg)
        simbolos.append(f'  <symbol id="h-{nombre}" viewBox="0 0 24 24" {ATRIBUTOS}><title>{etiqueta}</title>{cuerpo}</symbol>')
    with open(os.path.join(salida, 'sprite.svg'), 'w', encoding='utf-8') as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n' + '\n'.join(simbolos) + '\n</svg>\n')
    with open(os.path.join(salida, 'iconos.json'), 'w', encoding='utf-8') as f:
        json.dump({n: e for n, (e, _) in ICONOS.items()}, f, ensure_ascii=False, indent=2)
    return len(ICONOS)


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.abspath(__file__))
    print(generar(os.path.join(raiz, 'iconos')), 'íconos')
