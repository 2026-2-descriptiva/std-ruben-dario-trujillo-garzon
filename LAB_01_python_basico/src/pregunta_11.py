import gzip
from pathlib import Path


def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """

    ruta = Path(__file__).parent.parent / "data" / "data.csv.gz"

    acumulados = {}

    with gzip.open(ruta, "rt") as archivo:

        for linea in archivo:

            columnas = linea.strip().split("\t")

            valor = int(columnas[1])

            for letra in columnas[3].split(","):

                if letra not in acumulados:
                    acumulados[letra] = valor
                else:
                    acumulados[letra] += valor

    return dict(sorted(acumulados.items()))