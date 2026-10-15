from pathlib import Path
import pandas as pd


def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """

    ruta = Path(__file__).parent.parent / "data" / "tbl1.tsv"

    tabla = pd.read_csv(ruta, sep="\t")

    valores = set(tabla["c4"].map(str.upper))

    return sorted(valores)