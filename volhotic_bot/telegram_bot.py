"""Bot de Telegram para consultar el stock.

Uso:  TELEGRAM_TOKEN=... ANTHROPIC_API_KEY=... python -m volhotic_bot.telegram_bot
"""

from __future__ import annotations

import asyncio
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from . import config, modo_simple

log = logging.getLogger(__name__)

AYUDA = (
    "Hola, soy el bot de stock de Volhotic.\n\n"
    "Escribime qué repuesto buscás (ej: \"disco de freno gol trend\") o pasame un código "
    "OEM/SKU (ej: 1J0411336H).\n\n"
    "/buscar <texto> — búsqueda directa por palabras\n"
    "/codigo <código> — búsqueda directa por código\n"
    "/nuevo — empezar una charla nueva\n"
    "/stock — resumen del inventario"
)


def crear_app(token: str) -> Application:
    inventario = config.cargar_inventario()
    asistente = None
    if config.USAR_IA:
        from .agente import AsistenteStock

        asistente = AsistenteStock(inventario, interno=config.INTERNO)
    log.info("Inventario cargado: %s | IA: %s", inventario.resumen(), bool(asistente))

    async def responder_largo(update: Update, texto: str) -> None:
        # Telegram corta los mensajes en 4096 caracteres.
        for i in range(0, len(texto), 4000):
            await update.message.reply_text(texto[i:i + 4000])

    async def inicio(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(AYUDA)

    async def nuevo(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        if asistente:
            asistente.nueva_charla(str(update.effective_chat.id))
        await update.message.reply_text("Listo, empezamos de cero. ¿Qué repuesto buscás?")

    async def stock(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        r = inventario.resumen()
        await update.message.reply_text(
            f"Artículos: {r['articulos']}\nCon stock: {r['con_stock']}\n"
            f"Unidades totales: {r['unidades']}\nMarcas: {r['marcas']}"
        )

    async def buscar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        consulta = " ".join(context.args)
        if not consulta:
            await update.message.reply_text("Usá: /buscar disco freno gol")
            return
        resultados = inventario.buscar(consulta, limite=modo_simple.MAX_RESULTADOS + 1)
        await responder_largo(update, modo_simple.formatear(resultados, config.INTERNO))

    async def codigo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        consulta = " ".join(context.args)
        if not consulta:
            await update.message.reply_text("Usá: /codigo 1J0411336H")
            return
        resultados = inventario.buscar_por_codigo(consulta)
        await responder_largo(update, modo_simple.formatear(resultados, config.INTERNO))

    async def mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        texto = update.message.text
        if not asistente:
            await responder_largo(update, modo_simple.responder(inventario, texto, config.INTERNO))
            return
        charla_id = str(update.effective_chat.id)
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        try:
            # La llamada a Claude es bloqueante: se corre en otro hilo para no frenar el bot.
            respuesta = await asyncio.to_thread(asistente.responder, charla_id, texto)
        except Exception:
            log.exception("Error consultando a Claude; respondo con búsqueda directa")
            asistente.nueva_charla(charla_id)
            respuesta = modo_simple.responder(inventario, texto, config.INTERNO)
        await responder_largo(update, respuesta)

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler(["start", "ayuda", "help"], inicio))
    app.add_handler(CommandHandler("nuevo", nuevo))
    app.add_handler(CommandHandler("stock", stock))
    app.add_handler(CommandHandler("buscar", buscar))
    app.add_handler(CommandHandler("codigo", codigo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje))
    return app


def main() -> None:
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
    if not config.TELEGRAM_TOKEN:
        raise SystemExit("Falta TELEGRAM_TOKEN (pedíselo a @BotFather en Telegram).")
    crear_app(config.TELEGRAM_TOKEN).run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
