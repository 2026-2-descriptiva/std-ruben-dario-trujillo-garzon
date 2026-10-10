import gzip
from pathlib import Path


def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    ruta = Path(__file__).parent.parent / "data" / "data.csv.gz"

    resultados = {}

    with gzip.open(ruta, "rt") as archivo:

        for linea in archivo:

            columnas = linea.strip().split("\t")

            letra = columnas[0]
            valor = int(columnas[1])

            if letra not in resultados:
                resultados[letra] = {
                    "maximo": valor,
                    "minimo": valor,
                }
            else:
                resultados[letra]["maximo"] = max(
                    resultados[letra]["maximo"],
                    valor,
                )

                resultados[letra]["minimo"] = min(
                    resultados[letra]["minimo"],
                    valor,
                )

    return [
        (
            letra,
            datos["maximo"],
            datos["minimo"],
        )
        for letra, datos in sorted(resultados.items())
    ]

