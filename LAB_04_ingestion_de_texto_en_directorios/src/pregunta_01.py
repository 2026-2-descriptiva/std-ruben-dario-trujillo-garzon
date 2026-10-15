from pathlib import Path
import pandas as pd


def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """

    ruta_base = Path(__file__).parent.parent

    carpeta_datos = ruta_base / "data"
    carpeta_salida = ruta_base / "submission"

    carpeta_salida.mkdir(exist_ok=True)

    for conjunto in sorted(["test", "train"]):

        filas = []

        for sentimiento in sorted(["negative", "neutral", "positive"]):

            carpeta_sentimiento = carpeta_datos / conjunto / sentimiento

            for archivo in sorted(carpeta_sentimiento.glob("*.txt")):

                filas.append(
                    {
                        "phrase": archivo.read_text(encoding="utf-8").strip(),
                        "target": sentimiento,
                    }
                )

        pd.DataFrame(filas).to_csv(
            carpeta_salida / f"{conjunto}_dataset.csv",
            index=False,
        )