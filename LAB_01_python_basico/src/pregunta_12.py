import gzip
from pathlib import Path


def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    ruta = Path(__file__).parent.parent / "data" / "data.csv.gz"

    acumulado = {}

    with gzip.open(ruta, "rt") as archivo:

        for linea in archivo:

            columnas = linea.strip().split("\t")

            letra = columnas[0]

            suma_metricas = 0

            for elemento in columnas[4].split(","):
                suma_metricas += int(elemento.split(":")[1])

            if letra not in acumulado:
                acumulado[letra] = suma_metricas
            else:
                acumulado[letra] += suma_metricas

    return dict(sorted(acumulado.items()))
