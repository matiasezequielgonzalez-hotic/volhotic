"""Base de datos de stock de autopartes.

Carga el stock (Google Sheets o el CSV del Excel) a una base SQLite y expone
búsquedas por descripción y por código (SKU / código OEM). De dónde vienen
las filas lo resuelve `fuentes.py`.
"""

from __future__ import annotations

import csv
import re
import sqlite3
import threading
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

# Palabras que no aportan a la búsqueda ("disco de freno para gol").
STOPWORDS = {
    "de", "del", "la", "el", "los", "las", "para", "con", "por", "y", "a",
    "en", "un", "una", "unos", "unas", "al", "x", "tenes", "tienen", "hay",
}


def normalizar(texto: str) -> str:
    """Minúsculas, sin acentos y con espacios simples."""
    texto = unicodedata.normalize("NFKD", texto or "")
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto.lower()).strip()


def normalizar_codigo(texto: str) -> str:
    """Deja solo letras y números: '1J0 411-336/H' -> '1j0411336h'."""
    return re.sub(r"[^a-z0-9]", "", normalizar(texto))


def _raiz(palabra: str) -> str:
    """Plural simple a singular para que 'amortiguadores' encuentre 'amortiguador'."""
    if len(palabra) > 4 and palabra.endswith("es"):
        return palabra[:-2]
    if len(palabra) > 3 and palabra.endswith("s"):
        return palabra[:-1]
    return palabra


def _parsear_stock(valor: str) -> int:
    """'12' -> 12, '1 caja' -> 1, '' -> 0."""
    m = re.match(r"\s*(-?\d+)", valor or "")
    return int(m.group(1)) if m else 0


# Campo del bot -> columnas posibles en la planilla (la primera que exista gana).
# Sirve para el Excel original, para Bronze_Catalogo y para la hoja General de
# vol_ml_listings(No_tocar).
_COLUMNAS_PLANILLA = {
    "id_producto": ("ID",),
    "descripcion": ("Descripcion",),
    "sku": ("SKU",),
    "stock": ("Stock", "Stock_BD"),
    "marca": ("Marca",),
    # La columna "EAN" de la planilla en realidad trae el código OEM / de fábrica.
    "codigo_oem": ("EAN",),
    "condicion": ("Condicion",),
    "link_ml": ("Link_ML",),
    "deposito": ("Deposito",),
    "ubicacion": ("Ubicacion",),
    "piso": ("Piso",),
    "zona": ("Zona",),
    "estado": ("Estado",),
    "estado_ml": ("Estado_ML",),
    "observacion": ("Observación", "Observacion"),
    "auditoria_sku": ("SKU_AUD",),
}

# Datos del depósito y notas del equipo: no se muestran en modo cliente.
CAMPOS_INTERNOS = (
    "deposito", "ubicacion", "piso", "zona", "estado", "estado_ml", "observacion", "auditoria_sku",
)

# Valores de SKU_AUD que son marcas de la auditoría y no un SKU.
_MARCAS_AUDITORIA = {"sin definir", "duplicado", "sin existencia"}


@dataclass
class Repuesto:
    id: int
    id_producto: str
    descripcion: str
    sku: str
    stock: int
    marca: str
    codigo_oem: str
    condicion: str
    link_ml: str
    deposito: str
    ubicacion: str
    piso: str
    zona: str
    estado: str
    estado_ml: str
    observacion: str
    auditoria_sku: str

    def a_dict(self, interno: bool = True) -> dict:
        datos = asdict(self)
        datos.pop("id")
        if not interno:
            for campo in CAMPOS_INTERNOS:
                datos.pop(campo)
        return {k: v for k, v in datos.items() if v not in ("", None)}


_CAMPOS = list(_COLUMNAS_PLANILLA)
_COLUMNAS = "id, " + ", ".join(_CAMPOS)

_ESQUEMA = (
    "DROP TABLE IF EXISTS repuestos;\n"
    "CREATE TABLE repuestos (id INTEGER PRIMARY KEY, "
    + ", ".join(f"{c} {'INTEGER NOT NULL DEFAULT 0' if c == 'stock' else 'TEXT'}" for c in _CAMPOS)
    + ", texto_busqueda TEXT NOT NULL, codigos_busqueda TEXT NOT NULL);"
)


def _a_registro(fila: dict) -> tuple | None:
    fila = {(k or "").strip(): str(v if v is not None else "").strip() for k, v in fila.items()}
    datos = {
        campo: next((fila[c] for c in columnas if c in fila), "")
        for campo, columnas in _COLUMNAS_PLANILLA.items()
    }
    # Saltea filas vacías y encabezados repetidos dentro de la planilla.
    if not datos["descripcion"] or datos["descripcion"] == "Descripcion" or datos["estado"] == "Estado":
        return None
    datos["stock"] = _parsear_stock(datos["stock"])
    if datos["auditoria_sku"].lower() not in _MARCAS_AUDITORIA:
        datos["auditoria_sku"] = ""
    sku, oem = datos["sku"], datos["codigo_oem"]
    return (
        *(datos[c] for c in _CAMPOS),
        normalizar(f"{datos['descripcion']} {datos['marca']} {sku} {oem}"),
        f"|{normalizar_codigo(sku)}|{normalizar_codigo(oem)}|{normalizar_codigo(datos['id_producto'])}|",
    )


class Inventario:
    def __init__(self, conexion: sqlite3.Connection):
        self.db = conexion
        self.db.row_factory = sqlite3.Row
        # El bot consulta desde varios hilos y la recarga reemplaza la tabla entera.
        self._lock = threading.RLock()

    # --- carga -------------------------------------------------------------

    @classmethod
    def desde_csv(cls, ruta_csv: str | Path, ruta_db: str | Path = ":memory:") -> "Inventario":
        """Crea la base a partir de un CSV exportado de la planilla de stock."""
        with Path(ruta_csv).open(encoding="utf-8-sig", newline="") as f:
            return cls.desde_filas(csv.DictReader(f), ruta_db)

    @classmethod
    def desde_filas(cls, filas: Iterable[dict], ruta_db: str | Path = ":memory:") -> "Inventario":
        inventario = cls(sqlite3.connect(str(ruta_db), check_same_thread=False))
        inventario.cargar(filas)
        return inventario

    def cargar(self, filas: Iterable[dict]) -> int:
        """Reemplaza todo el stock por `filas` (dicts con los encabezados de la planilla).

        Devuelve la cantidad de artículos cargados.
        """
        registros = [r for r in (_a_registro(f) for f in filas) if r]
        with self._lock:
            self.db.executescript(_ESQUEMA)
            self.db.executemany(
                f"INSERT INTO repuestos ({', '.join(_CAMPOS)}, texto_busqueda, codigos_busqueda)"
                f" VALUES ({', '.join('?' * (len(_CAMPOS) + 2))})",
                registros,
            )
            self.db.commit()
        return len(registros)

    # --- consultas ---------------------------------------------------------

    def _a_repuestos(self, filas) -> list[Repuesto]:
        return [Repuesto(**{k: row[k] for k in row.keys() if k in Repuesto.__dataclass_fields__}) for row in filas]

    def buscar(self, consulta: str, limite: int = 15, solo_con_stock: bool = False) -> list[Repuesto]:
        """Búsqueda por palabras: todas tienen que aparecer en descripción, marca o códigos.

        Ordena primero los que tienen stock y los que matchean al inicio de la descripción.
        """
        palabras = [_raiz(p) for p in re.findall(r"[a-z0-9./-]+", normalizar(consulta))]
        palabras = [p for p in palabras if p not in STOPWORDS]
        if not palabras:
            return []
        condiciones = ["texto_busqueda LIKE ?"] * len(palabras)
        parametros: list = [f"%{p}%" for p in palabras]
        if solo_con_stock:
            condiciones.append("stock > 0")
        with self._lock:
            filas = self.db.execute(
                f"SELECT {_COLUMNAS}, texto_busqueda FROM repuestos WHERE {' AND '.join(condiciones)}",
                parametros,
            ).fetchall()

        def puntaje(row) -> tuple:
            texto = row["texto_busqueda"]
            # "gol" tiene que priorizar "Gol Trend" antes que "Golf".
            palabras_exactas = sum(
                bool(re.search(rf"(?<![a-z0-9]){re.escape(p)}(?:e?s)?(?![a-z0-9])", texto)) for p in palabras
            )
            al_inicio = texto.startswith(palabras[0])
            return (palabras_exactas, row["stock"] > 0, al_inicio, -len(texto))

        filas.sort(key=puntaje, reverse=True)
        return self._a_repuestos(filas[:limite])

    def buscar_por_codigo(self, codigo: str, limite: int = 15) -> list[Repuesto]:
        """Busca por SKU, código OEM o ID interno (P00123) ignorando espacios, guiones y barras.

        Un código parcial también matchea: 'G052145' encuentra 'G052145/A1/A2'.
        """
        codigo_norm = normalizar_codigo(codigo)
        if len(codigo_norm) < 3:
            return []
        with self._lock:
            filas = self.db.execute(
                f"SELECT {_COLUMNAS} FROM repuestos WHERE codigos_busqueda LIKE ?"
                " ORDER BY (codigos_busqueda LIKE ?) DESC, stock DESC LIMIT ?",
                (f"%{codigo_norm}%", f"%|{codigo_norm}|%", limite),
            ).fetchall()
        return self._a_repuestos(filas)

    def resumen(self) -> dict:
        with self._lock:
            fila = self.db.execute(
                "SELECT COUNT(*) AS articulos, SUM(stock) AS unidades,"
                " SUM(stock > 0) AS con_stock, COUNT(DISTINCT marca) AS marcas FROM repuestos"
            ).fetchone()
        return dict(fila)
