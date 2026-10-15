from pathlib import Path
import pandas as pd


def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """

    ruta_tbl0 = Path(__file__).parent.parent / "data" / "tbl0.tsv"
    ruta_tbl2 = Path(__file__).parent.parent / "data" / "tbl2.tsv"

    tabla_0 = pd.read_csv(ruta_tbl0, sep="\t")
    tabla_2 = pd.read_csv(ruta_tbl2, sep="\t")

    resultado = (
        tabla_0
        .merge(tabla_2, on="c0")
        .groupby("c1")
        .agg({"c5b": "sum"})
    )

    return resultado["c5b"]