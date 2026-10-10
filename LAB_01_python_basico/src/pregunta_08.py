import gzip
from pathlib import Path


def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    ruta = Path(__file__).parent.parent / "data" / "data.csv.gz"

    agrupacion = {}

    with gzip.open(ruta, "rt") as archivo:

        for linea in archivo:

            columnas = linea.strip().split("\t")

            letra = columnas[0]
            valor = int(columnas[1])

            if valor not in agrupacion:
                agrupacion[valor] = []

            if letra not in agrupacion[valor]:
                agrupacion[valor].append(letra)

    return [
        (valor, sorted(letras))
        for valor, letras in sorted(agrupacion.items())
    ]