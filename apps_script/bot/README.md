# hottie: kit del bot de stock para Apps Script

hottie es la compañera del equipo que sabe dónde está cada repuesto. Buscador de stock (sin IA)
para sumar a la app del equipo, en tres formas: página de chat, **ventana emergente** y
**Modo Sala** (sala 3D tipo videojuego con XP y ranking). Lee la planilla
**vol_ml_listings(No_tocar)** en el momento. Diseño completo: ver el documento de diseño del bot.

| Archivo | Qué es | Dónde va |
|---|---|---|
| `Bot.gs` | Servidor: búsqueda, permisos, precios, acciones | Archivo de script en tu proyecto |
| `BotUI.html` | Pantalla del chat | Archivo HTML `BotUI` |
| `BotAvatar.html` | Avatar en base64 (una sola línea) | Archivo HTML `BotAvatar` |
| `BotWidget.html` | Ventana emergente (botón flotante + chat) | Archivo HTML `BotWidget` |
| `BotSala.html` | Modo Sala en 3D | Archivo HTML `BotSala` |
| `BotSprites.html` | Figuras de cuerpo entero para la sala | Archivo HTML `BotSprites` |
| `BotCharla.html` | Personalidad de hottie: charla y frases | Archivo HTML `BotCharla` |
| `Sinonimos.csv` | Sinónimos y errores de tipeo iniciales | Hoja nueva `Sinonimos` |
| `Precios_plantilla.csv` | Encabezados de la lista de precios | Hoja nueva `Precios` |

## Instalación

1. En tu proyecto de Apps Script, creá `Bot.gs`, `BotUI.html` y `BotAvatar.html` y pegá el contenido.
   Todo empieza con `bot`/`BOT` para no chocar con tu código.
2. **Quién está logueado:** cambiá `botEmailActual_()` en `Bot.gs` para que devuelva el Gmail del
   usuario como lo hace tu app. Por defecto usa `Session.getActiveUser().getEmail()`, que solo
   funciona si la web app se ejecuta como "el usuario que accede".
3. **Mostrar las pantallas:** al principio de tu `doGet`:
   ```js
   if (e.parameter.v === 'bot') return botPagina();       // chat
   if (e.parameter.v === 'sala') return botPaginaSala();  // Modo Sala 3D
   ```
   **Ventana emergente:** en cada página de tu app donde quieras el botón flotante, antes de
   `</body>` agregá `<?!= botWidget() ?>` (la página tiene que armarse con
   `HtmlService.createTemplateFromFile(...)`). Abre el chat en un panel; desde el chat hay un
   botón "🎮 Modo Sala".
4. En la planilla:
   - Hoja `Sinonimos` con columnas `Palabra | Equivale_a` (importá `Sinonimos.csv`; las columnas
     Tipo y Nota son solo ayuda). Solo palabras sueltas.
   - Hoja `Precios` con `ID | SKU | Precio | Moneda | Actualizado | Quien`.
   - En `Permisos`, sumá a cada persona las secciones `consultas`, `precios` y/o `ubicar`.
     Los de rol Admin tienen todo.
5. Si la planilla tiene un ID distinto o el proyecto está vinculado a ella, ajustá `BOT.PLANILLA_ID`.

## Reglas que ya trae

- **Línea:** SEX = Marca Sexhotic (solo para los Gmail de `SEX_ADMIN` en Config); Pet = SKU que
  empieza con `BIO`; Tecnología = SKU que empieza con `TEC`; el resto, Autopartes. Se cambia en
  `BOT_LINEAS`.
- **Búsqueda por código** si todas las partes de lo escrito tienen números (`1J0411336H`,
  `415 0491 09`, `P00002`). Ignora espacios, guiones, puntos y barras, y acepta códigos parciales.
  Si no encuentra, busca por palabras.
- **Búsqueda por palabras:** sin acentos, plural a singular, sinónimos, todas las palabras tienen que
  aparecer. Orden: palabra exacta ("gol" antes que "golf"), con stock, empieza con la primera palabra.
- **Fichas:** hasta 5, con el total. Avisos: "Dice SIN STOCK pero figura con N", "Sin ubicación",
  "No encontrado en el relevamiento", "Precio viejo" (más de 30 días).
- **Bilstein:** si la búsqueda dice Bilstein, agrega la nota de que lo que no figura en planta baja
  es de Fabián.
- **No lo encontré:** fila en `Recuentos` con Estado `Pendiente`; no duplica si ya hay uno pendiente.
  El tope `RECUENTOS_POR_DEPOSITO` lo sigue aplicando tu app cuando pide recuentos.
- **Corregir ubicación:** solo con `ubicar`, eligiendo pisos y zonas que ya existen. Busca la fila
  por ID, verifica que no la hayan cambiado en el medio, escribe y registra en `Decisiones`
  (Tipo `UBICACION`).
- **Precios:** solo con `precios`; sin el permiso el precio no llega al navegador.
- **Avatar de cada persona** (hoja `Equipo`): si la columna `Foto` tiene un link o ID de un archivo
  de Drive (o un `data:image/...`), muestra esa foto redonda al lado de sus mensajes. Si no, el emoji
  de `Icono` en un círculo; si tampoco hay, las iniciales con un color fijo por persona. La foto
  tiene que pesar menos de 300 KB (256 px alcanza) y el dueño del script tiene que poder abrirla.
  La primera vez Apps Script pide permiso de Drive.
- **Personalidad (`BotCharla.html`):** antes de buscar, hottie reconoce charla: saludos según la
  hora y con apodo (Facu, Seba, Gabi, Agus), "¿cómo estás?", "gracias", "¿quién sos?", "¿qué podés
  hacer?", "¿cómo voy?" (nivel y ranking, en la sala), chistes de depósito, "chau", y si alguien la
  chamuya lo corta con humor y vuelve al laburo. Las búsquedas también tienen frases que rotan y
  comentan el stock ("queda una sola", "hay una banda"). Abajo de cada respuesta hay botones de
  respuesta rápida. Para cambiar cómo habla, editá las listas de frases de ese archivo.
  "Hola hottie, ¿tenés disco de freno para gol?" igual busca: las palabras de charla se ignoran.
- **Modo Sala (3D, three.js r128 desde cdnjs):** cada uno maneja su figura con WASD/flechas, tocando
  el piso o arrastrando para girar la cámara. Con **E** habla con hottie en su terminal; le pregunta
  por un repuesto (búsqueda real) y ella marca con un rayo de luz la estantería de esa zona. Ahí
  elige "¡Lo encontré!" (+10 XP, lleva la caja a Despacho: +5 XP) o "No estaba" (crea el recuento:
  +3 XP). Si el producto no tiene ubicación y la persona tiene `ubicar`, lo deja en una estantería
  eligiendo el piso (+15 XP). Hay nivel, barra de XP y ranking semanal. Las estanterías son las 8
  zonas con más productos. Los compañeros con figura andan por la sala.
- **Sala compartida:** cada pantalla le avisa al servidor dónde está cada 2 segundos
  (`botSalaLatido`) y recibe dónde están los demás, que se ven caminar con su figura y su nombre.
  Todo vive en `CacheService` (no toca la planilla). Si la pestaña queda en segundo plano, deja de
  avisar. Con **T** (o el botón "💬 Decir") le escribís al equipo: sale como globito y en el feed.
  Lo que le preguntás a hottie también se ve como globito. El feed muestra quién entra, chats,
  hallazgos y despachos.
- **Pedidos (el proceso real, en juego):** en la **PC de pedidos** se toma un pedido de práctica
  armado por el servidor con productos reales (1 o 2 ítems, cantidad y tipo de envío Flex, Colecta o
  Retiro). Pasos: buscarlo en su zona (si no sabés, preguntale a hottie "¿dónde está lo de mi
  pedido?" y te marca el rack) → **comparar el SKU con la etiqueta** entre 3 cajas con códigos
  parecidos → **verificar la cantidad** → **revisar el estado** (a veces viene golpeada: hay que
  separarla) → en la **mesa de armado**, embalar en orden: caja del tamaño justo → proteger con papel →
  cinta → etiqueta → **canasto** del envío. Cada error tiene su explicación. Pedido perfecto +25 XP,
  con errores +10; el servidor solo paga pedidos que él entregó y no antes de 20 segundos.
- **Orden y limpieza:** cada tanto aparecen papeles y cartones tirados, y el embalaje deja papel
  sobrante. Se juntan (hasta 3) y se llevan al tacho de **reciclaje**: +2 XP cada uno, hasta 20 XP
  por día.
- **Bolsa de boxeo 🥊** para descargar: no da XP, hottie comenta cada 10 golpes.
- **Desafío ⚡ (aprender jugando):** hottie elige un repuesto real de las zonas de la sala y
  pregunta a todos dónde está, sin decir la zona. El primero que llega a la estantería correcta y
  aprieta E gana +20 XP; si errás, todos lo ven y esperás 10 s. A los 30 s hay pista (piso o
  código), al minuto se revela la zona y a los 2 minutos se cierra. 15 s después sale otro. El
  servidor decide quién ganó (con lock), así que no hay empates ni trampas.
- **Estética hotic.:** grafito `#191B1F`, azul cobalto `#1538BE`, blanco y grotesca bold
  (Helvetica/Arial). Azul claro `#8FA2FF` para texto azul sobre grafito.
- **XP:** se guarda en la hoja `BotXP` (la crea el bot). El servidor no da XP dos veces por la misma
  acción y producto en el día (el desafío da +20 una vez por desafío), tope 300 XP por día, y "reporte"/"ubicado" solo se ganan haciendo la
  acción real. Nivel n desde 50·(n-1)² XP (50, 200, 450…).
- **Figuras:** `BotSprites.html` tiene a hottie, Facundo, Gabriel, Sebastián y Agustín. El nombre del
  jugador se busca sin acentos (Sebastián → `sebastian`). Quien no tiene figura aparece como una
  silueta de su color con la inicial. Para sumar a alguien: agregá `"nombre": "data:image/webp;base64,..."`.
- **Caché:** el índice se guarda 10 minutos en `CacheService`; una corrección de ubicación lo renueva.

## Revisar contra tu app

- Los valores de `Estado` que usa tu app en `Recuentos` (el kit escribe `Pendiente`).
- Qué columnas de `Decisiones` son `Quien` y `Persona` (el kit pone nombre y Gmail).
- Si `Equipo` tiene una columna `Activo` con "NO" para la gente que ya no está (el kit la respeta).

## Pruebas

Se probó con una copia simulada de la planilla armada con el Excel de stock (6.310 artículos).
Consultas para probar en la app, con lo que tiene que pasar:

| Escribís | Tiene que mostrar primero |
|---|---|
| `disco de freno gol` | Disco De Freno Delantero Gol Trend 256mm (no un Golf) |
| `amortiguadores` | Amortiguador (Nakata) |
| `1j0-411 336/h` | Abrasadera Golf Bora (por código) |
| `G052145` | Aceite De Caja Velocidad Automatica, OEM G052145/A1/A2 |
| `P00002` | Abrasadera Golf Bora |
| `22-183705` | Amortiguador Delantero Audi A1 (SKU 22.183705) |
| `abrazadera golf` | Abrasadera Golf Bora (sinónimo) |
| `parachoques vento` | Algún Paragolpe de Vento (sinónimo) |
| `paasat` | Más de 600 resultados de Passat (error de tipeo) |
| `amortiguador bilstein` | Amortiguadores Bilstein + nota de Fabián |
| `alma paragolpe audi a3` | Aviso "Dice SIN STOCK pero figura con 7" |
| `xyzxyz freno` | Sin resultados + 3 sugerencias de freno |
