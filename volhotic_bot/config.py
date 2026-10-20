"""Configuración por variables de entorno (ver .env.example)."""

from __future__ import annotations

import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

RUTA_CSV = Path(os.environ.get("VOLHOTIC_CSV", RAIZ / "data" / "stock.csv"))
RUTA_DB = Path(os.environ.get("VOLHOTIC_DB", RAIZ / "data" / "stock.db"))
# "interno" muestra ubicación en depósito y notas; "cliente" las oculta.
INTERNO = os.environ.get("VOLHOTIC_MODO", "interno").lower() != "cliente"
USAR_IA = bool(os.environ.get("ANTHROPIC_API_KEY")) and os.environ.get("VOLHOTIC_IA", "1") != "0"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")


def cargar_inventario():
    from .inventario import Inventario

    return Inventario.desde_csv(RUTA_CSV, RUTA_DB)
