"""Configuración por variables de entorno (ver .env.example)."""

from __future__ import annotations

import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# URL de la web app de Apps Script (con ?token=...) o ruta a un .csv/.json local.
FUENTE = os.environ.get("VOLHOTIC_FUENTE") or os.environ.get("VOLHOTIC_CSV") or str(RAIZ / "data" / "stock.csv")
RUTA_DB = Path(os.environ.get("VOLHOTIC_DB", RAIZ / "data" / "stock.db"))
# Cada cuántos minutos se vuelve a leer la planilla (0 = nunca).
REFRESCO_MIN = float(os.environ.get("VOLHOTIC_REFRESCO_MIN", "10"))
# "interno" muestra ubicación en depósito y notas; "cliente" las oculta.
INTERNO = os.environ.get("VOLHOTIC_MODO", "interno").lower() != "cliente"
USAR_IA = bool(os.environ.get("ANTHROPIC_API_KEY")) and os.environ.get("VOLHOTIC_IA", "1") != "0"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")


def cargar_inventario():
    from .fuentes import InventarioVivo

    inventario = InventarioVivo(FUENTE, RUTA_DB, intervalo_min=REFRESCO_MIN)
    inventario.iniciar_actualizacion()
    return inventario
