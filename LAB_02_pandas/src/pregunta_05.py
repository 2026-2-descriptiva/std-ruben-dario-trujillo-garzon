from pathlib import Path
import pandas as pd


def pregunta_05():
    """
    Usando `data/tbl0.tsv`, encuentre el valor máximo de la columna `c2` para
    cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice
    son las categorías, en orden alfabético, y cuyos valores son los máximos.

    Ejemplo del formato de la respuesta:

        c1
        A    9
        B    9
        C    9
        ...
    """

    ruta = Path(__file__).parent.parent / "data" / "tbl0.tsv"

    tabla = pd.read_csv(ruta, sep="\t")

    return tabla.groupby("c1").agg({"c2": "max"})["c2"]
