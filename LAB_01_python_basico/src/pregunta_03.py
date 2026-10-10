import gzip
from pathlib import Path


def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """

    archivo = Path("data/data.csv.gz")

    if not archivo.exists():
        archivo = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"

    acumulados = {}

    with gzip.open(archivo, "rt", encoding="utf-8") as datos:
        for linea in datos:
            campos = linea.strip().split("\t")

            letra = campos[0]
            valor = int(campos[1])

            acumulados[letra] = acumulados.get(letra, 0) + valor

    return sorted(acumulados.items())