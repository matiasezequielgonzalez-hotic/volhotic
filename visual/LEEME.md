# Pack visual hotic.

Elementos visuales propios de hotic., hechos en código (SVG). Se pueden editar y regenerar.

## Qué hay

| Carpeta | Qué es |
|---|---|
| `iconos/` | 53 íconos de línea (24×24, trazo 2, `currentColor`): uno por archivo, más `sprite.svg` con todos como `<symbol id="h-nombre">` y `iconos.json` (nombre → etiqueta). |
| `marca/` | Logos redibujados en vectores: `hotic`, `h` (monograma), `h_ho-tic`, `cursor` (la marca `._`) y `hotic_agent`, en versiones cuadradas y horizontales. Cada uno viene en `_negro` (negro sobre blanco), `_blanco` (blanco sobre negro) y `_solo` (sin fondo, toma el color del texto). |
| `stickers/` | 24 stickers con borde blanco: 13 de hottie y 11 de Matías. `stickers.json` dice el texto y para qué se usa cada uno. |
| `png/` | Los stickers en PNG transparente de 512×512 y los logos en PNG de 1024 px de ancho. |
| `webp/` | Los stickers en WebP de 512×512 y menos de 100 KB, el formato de los stickers de WhatsApp. |
| `catalogo.html` | Página para ver todo junto. Abrila en el navegador. |

## Usarlo en el panel

**Íconos.** Pegá el contenido de `iconos/sprite.svg` una sola vez en la página (o en el layout) y usalos así:

```html
<svg class="icono" aria-hidden="true"><use href="#h-pedido"/></svg>
```

```css
.icono { width: 20px; height: 20px; color: inherit; } /* toman el color del texto */
```

En React o Vue también podés importar cada `.svg` suelto como componente o como `<img>`.

**Paleta** (la misma del juego y la escuela):

| Uso | Color |
|---|---|
| Marca | negro `#000` y blanco `#fff` |
| hottie / acento | turquesa `#22c7c9` |
| Líneas | Autopartes `#3b6bff` · Pet `#2fbf71` · Bio `#ff6fb5` · Kid `#5ec8f2` · Tec `#e5484d` · Sex `#9b5cff` |
| Equipo | Facundo `#4d8dff` · Gabriel `#f2b84b` · Sebastián `#a98bff` · Agustín `#ff7a7a` · Matías `#ff9f43` |

**Stickers.** Para reacciones en la escuela o en el chat de hottie, por ejemplo:

| Momento | Sticker |
|---|---|
| Respuesta correcta | `hottie_guino` |
| Respuesta incorrecta | `hottie_ups` |
| Lección terminada | `hottie_festejo` o `hottie_xp` |
| Pregunta de repaso | `hottie_pensando` |
| Aviso del horario de corte | `hottie_apurada` o `matias_corte` |
| Pedido armado | `hottie_paquete` |
| hottie se presenta | `hottie_agente` |

Cada SVG de sticker tiene un id de filtro propio (`borde-<personaje>-<nombre>`), así que se pueden poner varios en línea en la misma página sin que choquen.

**Logos.** Para fondos de color o modo oscuro usá `_solo`: hereda el color del texto (`color: #fff`).

## Regenerar o cambiar algo

Necesitás Python 3 con `fonttools` (`pip install fonttools`) y la tipografía Liberation Sans, que tiene la métrica de Arial/Helvetica.
Los textos quedan convertidos a trazos, así que se ven igual en cualquier lado.

```bash
python3 iconos.py     # iconos/
python3 marca.py      # marca/
python3 stickers.py   # stickers/
python3 catalogo.py   # catalogo.html
node exportar.js      # png/ (necesita playwright; CHROMIUM=/ruta/al/chromium si no lo encuentra)
python3 webp.py       # webp/ (necesita Pillow)
```

- **Agregar un ícono:** sumalo a `ICONOS` en `iconos.py`, dibujado en una grilla de 24×24 sin relleno.
- **Agregar un sticker:** sumá una fila a `STICKERS` en `stickers.py`. Se arma combinando ojos, cejas, boca, brazos y un accesorio que ya existen.
