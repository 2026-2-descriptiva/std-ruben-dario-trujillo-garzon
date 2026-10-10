import gzip
from pathlib import Path


def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """

    archivo = Path("data/data.csv.gz")

    if not archivo.exists():
        archivo = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"

    letras = {}

    with gzip.open(archivo, "rt", encoding="utf-8") as datos:
        for registro in datos:
            letra = registro.split("\t")[0]

            letras[letra] = letras.get(letra, 0) + 1

    resultado = sorted(letras.items())

    return resultado