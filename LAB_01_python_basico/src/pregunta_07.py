import gzip
from pathlib import Path


def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """

    ruta = Path(__file__).parent.parent / "data" / "data.csv.gz"

    agrupados = {}

    with gzip.open(ruta, "rt") as archivo:

        for linea in archivo:

            columnas = linea.strip().split("\t")

            letra = columnas[0]
            valor = int(columnas[1])

            if valor not in agrupados:
                agrupados[valor] = []

            agrupados[valor].append(letra)

    return sorted(agrupados.items())
