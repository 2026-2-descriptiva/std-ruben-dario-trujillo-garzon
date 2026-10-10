import gzip
from pathlib import Path


def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    ruta = Path(__file__).parent.parent / "data" / "data.csv.gz"

    frecuencias = {}

    with gzip.open(ruta, "rt") as archivo:

        for linea in archivo:

            datos = linea.strip().split("\t")

            for metrica in datos[4].split(","):

                clave = metrica.split(":")[0]

                if clave not in frecuencias:
                    frecuencias[clave] = 1
                else:
                    frecuencias[clave] += 1

    return dict(sorted(frecuencias.items()))
