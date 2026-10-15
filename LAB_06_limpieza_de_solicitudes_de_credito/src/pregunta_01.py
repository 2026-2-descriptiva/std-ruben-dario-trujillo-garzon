from pathlib import Path
import pandas as pd
import re


def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`.
    """

    base = Path(__file__).parent.parent

    datos = pd.read_csv(
        base / "data" / "solicitudes_de_credito.csv.gz",
        sep=";",
        index_col=0,
    )

    columnas = {}

    for nombre in datos.columns:
        if "nea_credito" in nombre:
            columnas[nombre] = "línea_credito"

    datos = datos.rename(columns=columnas)

    requeridas = [
        columna
        for columna in datos.columns
        if columna != "comuna_ciudadano"
    ]

    datos = datos.dropna(subset=requeridas)

    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]

    for columna in columnas_texto:

        datos[columna] = (
            datos[columna]
            .astype(str)
            .str.lower()
            .str.replace("_", " ", regex=False)
            .str.replace("-", " ", regex=False)
            .apply(lambda valor: " ".join(valor.split()))
        )

    datos["estrato"] = datos["estrato"].astype(int)

    datos["monto_del_credito"] = (
        datos["monto_del_credito"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    datos["monto_del_credito"] = (
        pd.to_numeric(datos["monto_del_credito"])
        .astype(int)
    )

    def estandarizar_fecha(fecha):

        fecha = str(fecha).strip()

        partes = re.split(r"[-/]", fecha)

        if len(partes) != 3:
            return fecha

        if len(partes[0]) == 4:
            anio, mes, dia = partes
        else:
            dia, mes, anio = partes

        return f"{anio}-{mes.zfill(2)}-{dia.zfill(2)}"

    datos["fecha_de_beneficio"] = (
        datos["fecha_de_beneficio"]
        .apply(estandarizar_fecha)
    )

    datos = datos[
        [
            "sexo",
            "tipo_de_emprendimiento",
            "idea_negocio",
            "barrio",
            "estrato",
            "comuna_ciudadano",
            "fecha_de_beneficio",
            "monto_del_credito",
            "línea_credito",
        ]
    ]

    datos = datos.drop_duplicates()

    salida = base / "submission"
    salida.mkdir(exist_ok=True)

    datos.to_csv(
        salida / "solicitudes_de_credito.csv",
        sep=";",
        index=False,
    )

    return datos

