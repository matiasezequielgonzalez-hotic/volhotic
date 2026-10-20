"""Asistente conversacional sobre el stock, usando Claude con herramientas.

Claude no ve el Excel completo: consulta el inventario a través de dos
herramientas (búsqueda por texto y por código) y responde con lo que encuentra.
"""

from __future__ import annotations

import json
import logging
import os

import anthropic

from .inventario import Inventario

log = logging.getLogger(__name__)

MODELO = os.environ.get("VOLHOTIC_MODELO", "claude-opus-5-5")
# Cantidad de mensajes de una charla antes de empezar una nueva (para acotar costo).
MAX_MENSAJES_HISTORIAL = 40

HERRAMIENTAS = [
    {
        "name": "buscar_repuestos",
        "description": (
            "Busca repuestos en el stock de Volhotic por palabras: tipo de pieza, modelo de auto, "
            "marca del repuesto, motor, posición (delantero/trasero, izq/der). Todas las palabras "
            "tienen que aparecer. Usá pocas palabras clave (ej: 'disco freno gol', 'bomba agua "
            "amarok'); si no hay resultados, probá con menos palabras o sinónimos."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "consulta": {"type": "string", "description": "Palabras clave a buscar."},
                "solo_con_stock": {
                    "type": "boolean",
                    "description": "true para devolver solo artículos con stock mayor a cero.",
                },
            },
            "required": ["consulta", "solo_con_stock"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "name": "buscar_por_codigo",
        "description": (
            "Busca un repuesto por su código: SKU del fabricante (ej: '415 0431 10'), código OEM / "
            "número de pieza original (ej: '1J0411336H', 'G052145') o ID interno (ej: 'P00002'). "
            "Ignora espacios, guiones y "
            "barras, y acepta códigos parciales."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"codigo": {"type": "string", "description": "Código a buscar."}},
            "required": ["codigo"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

PROMPT_BASE = """Sos el asistente de stock de Volhotic, una casa de autopartes de Argentina \
especializada en Volkswagen, Audi, Ford y afines. Respondés en español rioplatense, breve y claro, \
porque la charla es por chat.

Para cualquier pregunta sobre repuestos, disponibilidad o códigos, consultá siempre las \
herramientas: nunca inventes artículos, stock ni códigos. Si el usuario pasa un código, usá \
buscar_por_codigo; si describe la pieza, usá buscar_repuestos. Si la consulta es ambigua \
(ej: "disco de freno" sin modelo), mostrá las opciones más relevantes y preguntá el modelo/año.

En los datos, "marca" es la marca del repuesto: "Legitimo" significa original de fábrica, \
"Importado" es alternativo importado. "codigo_oem" es el número de pieza original de la automotriz. \
Si un artículo tiene "link_ml", es su publicación en Mercado Libre: compartila cuando sirva.

No tenés precios: si los piden, decí que un vendedor los confirma."""

PROMPT_INTERNO = """
Estás hablando con alguien del equipo de Volhotic. Podés mostrar el ID interno (id_producto), \
el depósito y la ubicación (ubicacion, piso, zona), el estado de publicación y las observaciones. Si una ubicación \
dice "SIN STOCK" pero la cantidad es mayor a cero, avisá que el dato está inconsistente."""

PROMPT_CLIENTE = """
Estás hablando con un cliente. Informá si hay stock y cuántas unidades, pero no menciones \
datos internos del depósito. Para concretar la compra, invitalo a hablar con un vendedor."""


class AsistenteStock:
    def __init__(self, inventario: Inventario, interno: bool = True, cliente: anthropic.Anthropic | None = None):
        self.inventario = inventario
        self.interno = interno
        self.cliente = cliente or anthropic.Anthropic()
        self.system = PROMPT_BASE + (PROMPT_INTERNO if interno else PROMPT_CLIENTE)
        self.historiales: dict[str, list] = {}

    def nueva_charla(self, charla_id: str) -> None:
        self.historiales.pop(charla_id, None)

    def _ejecutar_herramienta(self, nombre: str, entrada: dict) -> str:
        if nombre == "buscar_repuestos":
            resultados = self.inventario.buscar(
                entrada["consulta"], solo_con_stock=bool(entrada.get("solo_con_stock"))
            )
        elif nombre == "buscar_por_codigo":
            resultados = self.inventario.buscar_por_codigo(entrada["codigo"])
        else:
            raise ValueError(f"Herramienta desconocida: {nombre}")
        if not resultados:
            return "Sin resultados."
        return json.dumps([r.a_dict(interno=self.interno) for r in resultados], ensure_ascii=False)

    def responder(self, charla_id: str, texto: str) -> str:
        mensajes = self.historiales.setdefault(charla_id, [])
        # El historial solo se agrega (nunca se edita) para no invalidar la caché ni el
        # razonamiento previo; cuando crece demasiado se empieza una charla nueva.
        if len(mensajes) >= MAX_MENSAJES_HISTORIAL:
            mensajes.clear()
        mensajes.append({"role": "user", "content": texto})

        while True:
            respuesta = self.cliente.beta.messages.create(
                model=MODELO,
                max_tokens=16000,
                system=self.system,
                tools=HERRAMIENTAS,
                messages=mensajes,
                thinking={"type": "adaptive"},
                output_config={"effort": "low"},
                cache_control={"type": "ephemeral"},
                # Si el modelo declina por error un pedido, la API lo reintenta con otro modelo.
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            )
            mensajes.append({"role": "assistant", "content": respuesta.content})

            if respuesta.stop_reason == "refusal":
                self.nueva_charla(charla_id)
                return "Perdón, no puedo ayudarte con eso. ¿Buscamos algún repuesto?"

            if respuesta.stop_reason != "tool_use":
                texto_final = "\n".join(b.text for b in respuesta.content if b.type == "text").strip()
                if respuesta.stop_reason == "max_tokens":
                    log.warning("Respuesta cortada por max_tokens en la charla %s", charla_id)
                return texto_final or "No encontré una respuesta, ¿podés reformular la consulta?"

            resultados = []
            for bloque in respuesta.content:
                if bloque.type != "tool_use":
                    continue
                try:
                    contenido = self._ejecutar_herramienta(bloque.name, bloque.input)
                    resultados.append({"type": "tool_result", "tool_use_id": bloque.id, "content": contenido})
                except Exception as e:  # el error vuelve a Claude para que se corrija
                    log.exception("Falló la herramienta %s", bloque.name)
                    resultados.append({
                        "type": "tool_result", "tool_use_id": bloque.id,
                        "content": f"Error: {e}", "is_error": True,
                    })
            mensajes.append({"role": "user", "content": resultados})
