"""De dónde salen los datos del stock.

`VOLHOTIC_FUENTE` puede ser:
- la URL de la web app de Apps Script (`apps_script/ExportarStock.gs`), que devuelve
  las hojas General y Publicaciones de vol_ml_listings(No_tocar) en JSON;
- un archivo local .json con ese mismo formato;
- un archivo local .csv exportado de la planilla (hoja General).
"""

from __future__ import annotations

import csv
import json
import logging
import sqlite3
import threading
import time
import urllib.request
from pathlib import Path

from .inventario import Inventario, normalizar_codigo

log = logging.getLogger(__name__)

# Estados de Mercado Libre en los que la publicación no sirve para mandarle al cliente.
_ESTADOS_ML_INACTIVOS = ("paus", "final", "closed", "inactiv", "under_review")


def _tabla_a_dicts(tabla: list[list]) -> list[dict]:
    """[[encabezados], [fila], ...] -> [{encabezado: valor}, ...]"""
    if not tabla:
        return []
    encabezados = [str(h).strip() for h in tabla[0]]
    return [dict(zip(encabezados, fila)) for fila in tabla[1:]]


def link_mercadolibre(mla: str) -> str:
    """'MLA688185887' -> 'https://articulo.mercadolibre.com.ar/MLA-688185887'"""
    mla = mla.strip().upper().replace("-", "")
    if not mla.startswith("MLA") or not mla[3:].isdigit():
        return ""
    return f"https://articulo.mercadolibre.com.ar/MLA-{mla[3:]}"


def _agregar_links_ml(filas: list[dict], publicaciones: list[dict]) -> None:
    """Cruza la hoja Publicaciones por SKU y agrega la columna Link_ML a cada fila."""
    links: dict[str, str] = {}
    for pub in publicaciones:
        sku = normalizar_codigo(str(pub.get("SKU", "")))
        estado = str(pub.get("Estado_ML", "")).lower()
        link = link_mercadolibre(str(pub.get("MLA", "")))
        if sku and link and not any(e in estado for e in _ESTADOS_ML_INACTIVOS):
            links.setdefault(sku, link)
    for fila in filas:
        sku = normalizar_codigo(str(fila.get("SKU", "")))
        if sku in links:
            fila["Link_ML"] = links[sku]


def filas_desde_json(datos: dict) -> list[dict]:
    """Formato de la web app: {"general": [[...], ...], "publicaciones": [[...], ...]}."""
    if "error" in datos:
        raise RuntimeError(f"La web app de la planilla respondió: {datos['error']}")
    filas = _tabla_a_dicts(datos.get("general", []))
    _agregar_links_ml(filas, _tabla_a_dicts(datos.get("publicaciones", [])))
    return filas


def leer_filas(fuente: str, timeout: float = 60) -> list[dict]:
    if fuente.startswith(("http://", "https://")):
        # Apps Script redirige a script.googleusercontent.com; urllib sigue la redirección.
        with urllib.request.urlopen(fuente, timeout=timeout) as respuesta:
            cuerpo = respuesta.read().decode("utf-8")
        try:
            datos = json.loads(cuerpo)
        except json.JSONDecodeError:
            raise RuntimeError(
                "La URL de la planilla no devolvió JSON. ¿La web app está publicada con acceso "
                "'Cualquier persona' y la URL termina en /exec?token=...?"
            ) from None
        return filas_desde_json(datos)

    ruta = Path(fuente)
    if ruta.suffix.lower() == ".json":
        return filas_desde_json(json.loads(ruta.read_text(encoding="utf-8")))
    with ruta.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


class InventarioVivo(Inventario):
    """Inventario que se vuelve a leer de la fuente cada `intervalo_min` minutos.

    Si una recarga falla (sin internet, planilla caída), sigue con los últimos datos.
    """

    def __init__(self, fuente: str, ruta_db: str | Path = ":memory:", intervalo_min: float = 10):
        super().__init__(sqlite3.connect(str(ruta_db), check_same_thread=False))
        self.fuente = fuente
        self.intervalo_min = intervalo_min
        self.ultima_carga: float | None = None
        self.recargar()  # la primera carga sí tiene que funcionar

    def recargar(self) -> int:
        cantidad = self.cargar(leer_filas(self.fuente))
        self.ultima_carga = time.time()
        log.info("Stock cargado desde %s: %d artículos", _ocultar_token(self.fuente), cantidad)
        return cantidad

    def iniciar_actualizacion(self) -> None:
        if self.intervalo_min <= 0:
            return

        def bucle():
            while True:
                time.sleep(self.intervalo_min * 60)
                try:
                    self.recargar()
                except Exception:
                    log.exception("No se pudo actualizar el stock; sigo con los datos anteriores")

        threading.Thread(target=bucle, name="actualizar-stock", daemon=True).start()


def _ocultar_token(fuente: str) -> str:
    return fuente.split("?")[0]
