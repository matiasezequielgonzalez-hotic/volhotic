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


# --- Google Sheets (formato de apps_script/ExportarStock.gs) -----------------

from volhotic_bot.fuentes import InventarioVivo, leer_filas, link_mercadolibre

JSON_PLANILLA = Path(__file__).resolve().parent / "datos" / "planilla_ejemplo.json"


def test_planilla_json_columnas_nuevas():
    inventario = InventarioVivo(str(JSON_PLANILLA), intervalo_min=0)
    assert inventario.resumen()["articulos"] == 3  # la fila P00001 sin descripción se saltea
    disco = inventario.buscar_por_codigo("1J0615301E")[0]
    assert disco.deposito == "Segurola" and disco.condicion == "Nuevo"
    # Se cruza con la hoja Publicaciones por SKU
    assert disco.link_ml == "https://articulo.mercadolibre.com.ar/MLA-667587416"
    # Publicación pausada: sin link. Y el cero a la izquierda del SKU se mantiene.
    capot = inventario.buscar_por_codigo("09600")[0]
    assert capot.sku == "09600" and capot.link_ml == ""


def test_busqueda_por_id_interno():
    inventario = InventarioVivo(str(JSON_PLANILLA), intervalo_min=0)
    assert inventario.buscar_por_codigo("P00002")[0].descripcion == "Abrasadera Golf Bora"


def test_modo_cliente_oculta_deposito():
    inventario = InventarioVivo(str(JSON_PLANILLA), intervalo_min=0)
    disco = inventario.buscar_por_codigo("1J0615301E")[0]
    publico = disco.a_dict(interno=False)
    assert "deposito" not in publico and "observacion" not in publico
    assert publico["link_ml"].startswith("https://")


def test_error_de_la_web_app(tmp_path):
    ruta = tmp_path / "error.json"
    ruta.write_text('{"error": "no autorizado"}', encoding="utf-8")
    with pytest.raises(RuntimeError, match="no autorizado"):
        leer_filas(str(ruta))


def test_recarga_fallida_mantiene_datos(tmp_path):
    ruta = tmp_path / "planilla.json"
    ruta.write_text(JSON_PLANILLA.read_text(encoding="utf-8"), encoding="utf-8")
    inventario = InventarioVivo(str(ruta), intervalo_min=0)
    ruta.write_text("esto no es json", encoding="utf-8")
    with pytest.raises(Exception):
        inventario.recargar()
    assert inventario.resumen()["articulos"] == 3


def test_link_mercadolibre():
    assert link_mercadolibre("MLA688185887") == "https://articulo.mercadolibre.com.ar/MLA-688185887"
    assert link_mercadolibre("") == ""
