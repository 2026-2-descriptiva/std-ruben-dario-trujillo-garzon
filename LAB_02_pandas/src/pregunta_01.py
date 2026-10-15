from pathlib import Path
import pandas as pd


def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """

    ruta = Path("data/tbl0.tsv")

    if not ruta.is_file():
        ruta = Path(__file__).resolve().parent.parent / "data" / "tbl0.tsv"

    datos = pd.read_csv(ruta, sep="\t")

    return datos.shape[0]