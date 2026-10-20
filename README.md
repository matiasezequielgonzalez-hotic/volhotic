# Bot de stock Volhotic

Bot que responde consultas sobre el stock de autopartes de Volhotic. Por ahora la base de datos
es el Excel de stock exportado a CSV.

- **Con IA (Claude):** entiende preguntas en lenguaje natural ("¿tenés disco de freno para un Gol
  Trend?", "¿qué hay de Luk para Vento?"), busca en el stock con herramientas y responde. Nunca
  inventa artículos: todo sale de la base.
- **Sin IA:** si no hay `ANTHROPIC_API_KEY`, hace una búsqueda directa por palabras o por código.
- **Canal:** Telegram (y una consola para probar). La lógica no depende del canal, así que se
  puede sumar WhatsApp u otro después.

## Estructura

| Archivo | Qué hace |
|---|---|
| `volhotic_bot/inventario.py` | Carga el CSV a SQLite y hace las búsquedas (texto y código SKU/OEM) |
| `volhotic_bot/agente.py` | Asistente con Claude + herramientas `buscar_repuestos` / `buscar_por_codigo` |
| `volhotic_bot/modo_simple.py` | Respuestas sin IA |
| `volhotic_bot/telegram_bot.py` | Bot de Telegram |
| `volhotic_bot/consola.py` | Chat por terminal para probar |

## Cómo usarlo

```bash
pip install -r requirements.txt
cp ruta/al/stock.csv data/stock.csv      # Excel → Archivo → Guardar como CSV UTF-8
cp .env.example .env                       # completar los tokens
export $(grep -v '^#' .env | xargs)

python -m volhotic_bot.consola             # probar en la terminal
python -m volhotic_bot.telegram_bot        # levantar el bot de Telegram
```

El token de Telegram se obtiene hablando con [@BotFather](https://t.me/BotFather) (`/newbot`).

Comandos del bot: `/buscar <texto>`, `/codigo <código>`, `/nuevo` (charla nueva), `/stock` (resumen).

### Modo interno / cliente

`VOLHOTIC_MODO=interno` (por defecto) muestra ubicación en el depósito (piso, zona), estado de
publicación y observaciones. `VOLHOTIC_MODO=cliente` las oculta y está pensado para que lo usen
los compradores.

### Actualizar el stock

Reemplazá `data/stock.csv` y reiniciá el bot: la base SQLite se regenera en cada arranque.

> `data/stock.csv` está en `.gitignore` porque el repositorio es público.

## Notas sobre los datos

- La columna **EAN** del Excel en realidad contiene el **código OEM** (número de pieza original),
  y así se trata en el bot.
- La columna **SKU** a veces tiene el código del fabricante y a veces una marca ("Ossca", "Ford").
- Se ignoran filas vacías y encabezados repetidos; un stock como "1 caja" se toma como 1.
- Hay 8 artículos con ubicación "SIN STOCK" pero cantidad > 0; en modo interno el bot lo avisa.

## Tests

```bash
python -m pytest
```
