import json
from pathlib import Path

import pandas as pd


def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona.
    """

    base = Path(__file__).parent.parent

    df = pd.read_csv(base / "data" / "insurance.csv.gz")

    def grupo_edad(x):
        if x < 30:
            return "18-29"
        elif x < 40:
            return "30-39"
        elif x < 50:
            return "40-49"
        return "50-64"

    def grupo_bmi(x):
        if x < 18.5:
            return "bajo peso"
        elif x < 25:
            return "normal"
        elif x < 30:
            return "sobrepeso"
        return "obesidad"

    def grupo_hijos(x):
        if x == 0:
            return "0"
        elif x in [1, 2]:
            return "1-2"
        return "3+"

    df["age_group"] = df["age"].apply(grupo_edad)
    df["bmi_group"] = df["bmi"].apply(grupo_bmi)
    df["children_group"] = df["children"].apply(grupo_hijos)

    originales = ["age", "sex", "bmi", "children", "region"]
    conteos = df.groupby(originales).size()
    original_k = int(conteos.min())
    original_unique_records = int((conteos == 1).sum())

    def evaluar_esquema(df, columnas):

        grupos = df.groupby(columnas)
        publicados = df[
            df.groupby(columnas)["smoker"].transform("count") >= 5
        ].copy()

        clases_sin_diversidad = 0
        registros_sin_diversidad = 0

        for _, grupo in publicados.groupby(columnas):

            if grupo["smoker"].nunique() == 1:
                clases_sin_diversidad += 1
                registros_sin_diversidad += len(grupo)

        resultado = {
            "quasi_identifiers": columnas,
            "equivalence_classes": len(grupos),
            "k_before_suppression": int(grupos.size().min()),
            "suppressed_records": len(df) - len(publicados),
            "published_records": len(publicados),
            "published_classes": len(publicados.groupby(columnas)),
            "classes_without_smoker_diversity": clases_sin_diversidad,
            "records_without_smoker_diversity": registros_sin_diversidad,
        }

        return resultado, publicados

    esquema_con_hijos = [
        "age_group",
        "sex",
        "bmi_group",
        "children_group",
        "region",]

    esquema_sin_hijos = [
        "age_group",
        "sex",
        "bmi_group",
        "region",]

    resultado_con_hijos, publicados_con_hijos = evaluar_esquema(df,esquema_con_hijos,)
    resultado_sin_hijos, publicados_sin_hijos = evaluar_esquema(df,esquema_sin_hijos,)

    if (resultado_con_hijos["suppressed_records"]
        <= resultado_sin_hijos["suppressed_records"]):
        selected_scheme = "with_children"
        publicados = publicados_con_hijos
    else:
        selected_scheme = "without_children"
        publicados = publicados_sin_hijos

    reporte = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": {
            "with_children": resultado_con_hijos,
            "without_children": resultado_sin_hijos,},
        "selected_scheme": selected_scheme,
        "mean_charges_original": float(df["charges"].mean()),
        "mean_charges_published": float(publicados["charges"].mean()),
        "smoker_rate_original": float((df["smoker"] == "yes").mean()),
        "smoker_rate_published": float(
            (publicados["smoker"] == "yes").mean()
        ),
    }

    submission = base / "submission"
    submission.mkdir(exist_ok=True)

    with open(
        submission / "privacy_report.json",
        "w",
        encoding="utf-8",
    ) as archivo:
        json.dump(reporte, archivo, indent=4)

    columnas_publicadas = (
        reporte["schemes"][selected_scheme]["quasi_identifiers"]
        + ["smoker", "charges"])

    publicados[columnas_publicadas].to_csv(
        submission / "insurance_published.csv",
        index=False,)

    return reporte