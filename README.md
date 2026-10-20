# Bot de stock Volhotic

Bot que responde consultas sobre el stock de autopartes de Volhotic. Lee el stock directo de la
planilla de Google Sheets **vol_ml_listings(No_tocar)** (hojas `General` y `Publicaciones`) y la
vuelve a leer cada 10 minutos. También puede trabajar con un CSV exportado.

- **Con IA (Claude):** entiende preguntas en lenguaje natural ("¿tenés disco de freno para un Gol
  Trend?", "¿qué hay de Luk para Vento?"), busca en el stock con herramientas y responde. Nunca
  inventa artículos: todo sale de la base.
- **Sin IA:** si no hay `ANTHROPIC_API_KEY`, hace una búsqueda directa por palabras o por código.
- **Canal:** Telegram (y una consola para probar). La lógica no depende del canal, así que se
  puede sumar WhatsApp u otro después.

## Estructura

| Archivo | Qué hace |
|---|---|
| `apps_script/ExportarStock.gs` | Web app de solo lectura que le pasa la planilla al bot |
| `volhotic_bot/fuentes.py` | Lee la planilla (web app, .json o .csv) y la recarga periódicamente |
| `volhotic_bot/inventario.py` | Carga los datos a SQLite y hace las búsquedas (texto, SKU, OEM, ID) |
| `volhotic_bot/agente.py` | Asistente con Claude + herramientas `buscar_repuestos` / `buscar_por_codigo` |
| `volhotic_bot/modo_simple.py` | Respuestas sin IA |
| `volhotic_bot/telegram_bot.py` | Bot de Telegram |
| `volhotic_bot/consola.py` | Chat por terminal para probar |

## Conectar la planilla de Google Sheets

El bot no toca la web app que ya usa el equipo: se crea un proyecto de Apps Script aparte, de
solo lectura, que devuelve únicamente las columnas que el bot necesita (nada de Costos, Ventas
ni Equipo).

1. Entrá a [script.google.com](https://script.google.com) con la cuenta dueña de la planilla →
   **Nuevo proyecto** → pegá el contenido de `apps_script/ExportarStock.gs`.
2. **Configuración del proyecto → Propiedades del script** → agregá `TOKEN` con una clave larga
   al azar. Sin ese token, la web app responde "no autorizado".
3. **Implementar → Nueva implementación → Aplicación web**. Ejecutar como: *Yo*. Quién tiene
   acceso: *Cualquier persona*. Autorizá los permisos.
4. Copiá la URL que termina en `/exec` y configurá en el bot:
   `VOLHOTIC_FUENTE=https://script.google.com/macros/s/.../exec?token=TU_CLAVE`

Columnas que usa el bot de la hoja `General`: ID, Descripcion, SKU, Stock, Marca, EAN, Condicion,
Deposito, Ubicacion, Piso, Zona, Estado, Estado_ML, Observación. De `Publicaciones` toma MLA, SKU
y Estado_ML para armar el link de Mercado Libre de cada artículo (solo publicaciones activas).

## Cómo usarlo

```bash
pip install -r requirements.txt
cp .env.example .env                       # completar los tokens y VOLHOTIC_FUENTE
export $(grep -v '^#' .env | xargs)

python -m volhotic_bot.consola             # probar en la terminal
python -m volhotic_bot.telegram_bot        # levantar el bot de Telegram
```

El token de Telegram se obtiene hablando con [@BotFather](https://t.me/BotFather) (`/newbot`).

Comandos del bot: `/buscar <texto>`, `/codigo <código>`, `/nuevo` (charla nueva), `/stock` (resumen).

### Modo interno / cliente

`VOLHOTIC_MODO=interno` (por defecto) muestra el ID interno, el depósito, la ubicación (piso,
zona), el estado de publicación y las observaciones. `VOLHOTIC_MODO=cliente` las oculta y está pensado para que lo usen
los compradores.

### Actualizar el stock

Con la planilla conectada no hay que hacer nada: el bot la vuelve a leer cada
`VOLHOTIC_REFRESCO_MIN` minutos. Si una lectura falla, sigue con los últimos datos.

Sin planilla, se puede usar un CSV: `VOLHOTIC_FUENTE=data/stock.csv` (está en `.gitignore`
porque el repositorio es público).

## Notas sobre los datos

- La columna **EAN** de la planilla en realidad contiene el **código OEM** (número de pieza original),
  y así se trata en el bot.
- La columna **SKU** a veces tiene el código del fabricante y a veces una marca ("Ossca", "Ford").
- Se ignoran filas vacías y encabezados repetidos; un stock como "1 caja" se toma como 1.
- Hay 8 artículos con ubicación "SIN STOCK" pero cantidad > 0; en modo interno el bot lo avisa.

## Tests

```bash
python -m pytest
```
