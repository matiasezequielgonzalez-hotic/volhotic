"""Base de datos de stock de autopartes.

Carga el CSV exportado del Excel de stock a una base SQLite y expone
búsquedas por descripción y por código (SKU / código OEM).

El CSV es la fuente inicial: cuando se migre a otra base (Postgres, el ERP,
la API de Mercado Libre), solo hay que reemplazar `Inventario`.
"""

from __future__ import annotations

import csv
import re
import sqlite3
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path

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


@dataclass
class Repuesto:
    id: int
    descripcion: str
    sku: str
    stock: int
    marca: str
    codigo_oem: str
    ubicacion: str
    piso: str
    zona: str
    estado: str
    observacion: str

    def a_dict(self, interno: bool = True) -> dict:
        datos = asdict(self)
        if not interno:
            # Los datos de depósito y las notas del equipo no salen al cliente.
            for campo in ("ubicacion", "piso", "zona", "estado", "observacion"):
                datos.pop(campo)
        return {k: v for k, v in datos.items() if v not in ("", None)}


_COLUMNAS = (
    "id, descripcion, sku, stock, marca, codigo_oem, ubicacion, piso, zona, "
    "estado, observacion"
)


class Inventario:
    def __init__(self, conexion: sqlite3.Connection):
        self.db = conexion
        self.db.row_factory = sqlite3.Row

    # --- carga -------------------------------------------------------------

    @classmethod
    def desde_csv(cls, ruta_csv: str | Path, ruta_db: str | Path = ":memory:") -> "Inventario":
        """Crea (o recrea) la base a partir del CSV del Excel de stock."""
        conexion = sqlite3.connect(str(ruta_db), check_same_thread=False)
        inventario = cls(conexion)
        inventario._crear_tablas()
        inventario._importar(Path(ruta_csv))
        return inventario

    def _crear_tablas(self) -> None:
        self.db.executescript(
            """
            DROP TABLE IF EXISTS repuestos;
            CREATE TABLE repuestos (
                id INTEGER PRIMARY KEY,
                descripcion TEXT NOT NULL,
                sku TEXT,
                stock INTEGER NOT NULL DEFAULT 0,
                marca TEXT,
                codigo_oem TEXT,
                ubicacion TEXT,
                piso TEXT,
                zona TEXT,
                estado TEXT,
                observacion TEXT,
                texto_busqueda TEXT NOT NULL,
                codigos_busqueda TEXT NOT NULL
            );
            """
        )

    def _importar(self, ruta_csv: Path) -> None:
        filas = []
        with ruta_csv.open(encoding="utf-8-sig", newline="") as f:
            for fila in csv.DictReader(f):
                fila = {(k or "").strip(): (v or "").strip() for k, v in fila.items()}
                descripcion = fila.get("Descripcion", "")
                # Saltea filas vacías y encabezados repetidos dentro del Excel.
                if not descripcion or descripcion == "Descripcion" or fila.get("Estado") == "Estado":
                    continue
                sku = fila.get("SKU", "")
                marca = fila.get("Marca", "")
                # La columna "EAN" del Excel en realidad trae el código OEM / de fábrica.
                oem = fila.get("EAN", "")
                filas.append((
                    descripcion,
                    sku,
                    _parsear_stock(fila.get("Stock", "")),
                    marca,
                    oem,
                    fila.get("Ubicacion", ""),
                    fila.get("Piso", ""),
                    fila.get("Zona", ""),
                    fila.get("Estado", ""),
                    fila.get("Observación", fila.get("Observacion", "")),
                    normalizar(f"{descripcion} {marca} {sku} {oem}"),
                    f"|{normalizar_codigo(sku)}|{normalizar_codigo(oem)}|",
                ))
        self.db.executemany(
            "INSERT INTO repuestos (descripcion, sku, stock, marca, codigo_oem, ubicacion,"
            " piso, zona, estado, observacion, texto_busqueda, codigos_busqueda)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            filas,
        )
        self.db.commit()

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
        """Busca por SKU o código OEM ignorando espacios, guiones y barras.

        Un código parcial también matchea: 'G052145' encuentra 'G052145/A1/A2'.
        """
        codigo_norm = normalizar_codigo(codigo)
        if len(codigo_norm) < 3:
            return []
        filas = self.db.execute(
            f"SELECT {_COLUMNAS} FROM repuestos WHERE codigos_busqueda LIKE ?"
            " ORDER BY (codigos_busqueda LIKE ?) DESC, stock DESC LIMIT ?",
            (f"%{codigo_norm}%", f"%|{codigo_norm}|%", limite),
        ).fetchall()
        return self._a_repuestos(filas)

    def resumen(self) -> dict:
        fila = self.db.execute(
            "SELECT COUNT(*) AS articulos, SUM(stock) AS unidades,"
            " SUM(stock > 0) AS con_stock, COUNT(DISTINCT marca) AS marcas FROM repuestos"
        ).fetchone()
        return dict(fila)
