import gzip
from pathlib import Path


def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """

    ruta = Path(__file__).parent.parent / "data" / "data.csv.gz"

    metricas = {}

    with gzip.open(ruta, "rt") as archivo:

        for linea in archivo:

            columnas = linea.strip().split("\t")

            for elemento in columnas[4].split(","):

                clave, valor = elemento.split(":")
                valor = int(valor)

                if clave not in metricas:
                    metricas[clave] = [valor, valor]
                else:
                    metricas[clave][0] = min(metricas[clave][0], valor)
                    metricas[clave][1] = max(metricas[clave][1], valor)

    return [
        (clave, valores[0], valores[1])
        for clave, valores in sorted(metricas.items())
    ]
