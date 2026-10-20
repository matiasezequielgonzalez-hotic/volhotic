from pathlib import Path
from types import SimpleNamespace

import pytest

from volhotic_bot import modo_simple
from volhotic_bot.agente import AsistenteStock
from volhotic_bot.inventario import Inventario

CSV = Path(__file__).resolve().parent / "datos" / "stock_ejemplo.csv"


@pytest.fixture(scope="module")
def inventario():
    return Inventario.desde_csv(CSV)


def test_carga_saltea_vacias_y_encabezados(inventario):
    descripciones = {r[0] for r in inventario.db.execute("SELECT descripcion FROM repuestos")}
    assert "Descripcion" not in descripciones
    assert "" not in descripciones
    assert inventario.resumen()["articulos"] == 10


def test_stock_no_numerico(inventario):
    # "1 caja" se toma como 1
    assert all(isinstance(r[0], int) for r in inventario.db.execute("SELECT stock FROM repuestos"))


def test_busqueda_plural_y_acentos(inventario):
    assert inventario.buscar("amortiguadores")
    assert inventario.buscar("AUTOMÁTICA febi")


def test_busqueda_prioriza_palabra_exacta(inventario):
    primero = inventario.buscar("disco de freno gol")[0]
    assert "Gol " in primero.descripcion and "Golf" not in primero.descripcion


def test_busqueda_por_codigo_ignora_formato(inventario):
    assert inventario.buscar_por_codigo("1j0-411 336/h")[0].descripcion.startswith("Abrasadera")
    # Código parcial de un OEM con variantes
    assert inventario.buscar_por_codigo("G052145")[0].codigo_oem == "G052145/A1/A2"
    assert inventario.buscar_por_codigo("abc-123")[0].stock == 1  # stock "1 caja"


def test_modo_cliente_oculta_datos_internos(inventario):
    repuesto = inventario.buscar_por_codigo("415 0491 09")[0]
    assert "observacion" in repuesto.a_dict(interno=True)
    assert "observacion" not in repuesto.a_dict(interno=False)
    assert "obs:" not in modo_simple.formatear([repuesto], interno=False)


def test_modo_simple_detecta_codigo(inventario):
    assert "Abrasadera" in modo_simple.responder(inventario, "1J0411336H")
    assert "Disco De Freno" in modo_simple.responder(inventario, "disco freno gol trend")


class ClienteFalso:
    """Simula la API: primero pide una herramienta, después contesta con texto."""

    def __init__(self):
        self.pedidos = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.pedidos.append(kwargs)
        if len(self.pedidos) == 1:
            bloque = SimpleNamespace(type="tool_use", id="tu_1", name="buscar_por_codigo",
                                     input={"codigo": "1J0411336H"})
            return SimpleNamespace(stop_reason="tool_use", content=[bloque])
        return SimpleNamespace(stop_reason="end_turn",
                               content=[SimpleNamespace(type="text", text="Sí, hay 8 unidades.")])


def test_agente_ejecuta_herramientas(inventario):
    cliente = ClienteFalso()
    asistente = AsistenteStock(inventario, interno=False, cliente=cliente)
    assert asistente.responder("chat1", "¿tienen la 1J0411336H?") == "Sí, hay 8 unidades."
    # El historial queda: usuario, tool_use, tool_result, respuesta final
    resultado_herramienta = asistente.historiales["chat1"][2]["content"][0]
    assert resultado_herramienta["tool_use_id"] == "tu_1"
    assert "Abrasadera" in resultado_herramienta["content"]
    assert cliente.pedidos[0]["model"] and cliente.pedidos[0]["fallbacks"] == "default"
