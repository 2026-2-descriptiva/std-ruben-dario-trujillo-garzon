from pathlib import Path


def pregunta_02():
    """
    ¿Cuántas columnas tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        4
    """

    ruta = Path(__file__).parent.parent / "data" / "tbl0.tsv"

    with open(ruta, "r", encoding="utf-8") as archivo:

        primera_fila = archivo.readline().strip()

    return len(primera_fila.split("\t"))
