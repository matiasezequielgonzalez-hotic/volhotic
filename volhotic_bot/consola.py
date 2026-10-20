"""Chat por terminal para probar el bot sin Telegram.

Uso:  python -m volhotic_bot.consola          (con IA si hay ANTHROPIC_API_KEY)
      VOLHOTIC_IA=0 python -m volhotic_bot.consola   (solo búsqueda directa)
"""

from __future__ import annotations

from . import config, modo_simple


def main() -> None:
    inventario = config.cargar_inventario()
    asistente = None
    if config.USAR_IA:
        from .agente import AsistenteStock

        asistente = AsistenteStock(inventario, interno=config.INTERNO)
    r = inventario.resumen()
    print(f"Stock Volhotic: {r['articulos']} artículos, {r['unidades']} unidades. "
          f"IA: {'sí' if asistente else 'no'}. Escribí 'salir' para terminar.\n")
    while True:
        try:
            texto = input("vos> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if texto.lower() in ("salir", "exit", "quit"):
            break
        if not texto:
            continue
        if asistente:
            respuesta = asistente.responder("consola", texto)
        else:
            respuesta = modo_simple.responder(inventario, texto, config.INTERNO)
        print(f"\nbot> {respuesta}\n")


if __name__ == "__main__":
    main()
