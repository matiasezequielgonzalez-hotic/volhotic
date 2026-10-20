"""Respuestas sin IA: búsqueda directa en el stock.

Se usa cuando no hay ANTHROPIC_API_KEY configurada, o con /buscar y /codigo.
"""

from __future__ import annotations

import re

from .inventario import Inventario, Repuesto, normalizar_codigo

MAX_RESULTADOS = 10


def formatear(resultados: list[Repuesto], interno: bool = True) -> str:
    if not resultados:
        return "No encontré repuestos con esa búsqueda. Probá con menos palabras o con el código."
    lineas = []
    for r in resultados[:MAX_RESULTADOS]:
        linea = f"• {r.descripcion} — {r.marca or 's/marca'} — stock: {r.stock}"
        if r.condicion:
            linea += f" ({r.condicion})"
        codigos = " / ".join(c for c in (r.sku, r.codigo_oem) if c)
        if codigos:
            linea += f"\n   cód: {codigos}"
        if r.link_ml:
            linea += f"\n   {r.link_ml}"
        if interno:
            lugar = ", ".join(
                f"{nombre} {valor}" for nombre, valor in
                (("id", r.id_producto), ("dep.", r.deposito), ("ubic.", r.ubicacion),
                 ("piso", r.piso), ("zona", r.zona)) if valor
            )
            if lugar:
                linea += f"\n   {lugar}"
            if r.observacion:
                linea += f"\n   obs: {r.observacion}"
        lineas.append(linea)
    if len(resultados) > MAX_RESULTADOS:
        lineas.append("…y más resultados. Agregá el modelo o la marca para acotar.")
    return "\n".join(lineas)


def parece_codigo(texto: str) -> bool:
    """Una sola 'palabra' con letras y números, ej: 1J0411336H, G052145/A1."""
    texto = texto.strip()
    return (
        " " not in texto
        and len(normalizar_codigo(texto)) >= 5
        and bool(re.search(r"\d", texto))
    )


def responder(inventario: Inventario, texto: str, interno: bool = True) -> str:
    if parece_codigo(texto):
        resultados = inventario.buscar_por_codigo(texto)
        if resultados:
            return formatear(resultados, interno)
    return formatear(inventario.buscar(texto, limite=MAX_RESULTADOS + 1), interno)
