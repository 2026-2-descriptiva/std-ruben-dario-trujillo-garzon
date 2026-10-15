import json
import re
from pathlib import Path

import pandas as pd


def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios
    al inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json`.
    """

    ruta_base = Path(__file__).parent.parent

    archivo_datos = ruta_base / "data" / "ventas.csv.gz"
    carpeta_salida = ruta_base / "submission"

    carpeta_salida.mkdir(exist_ok=True)

    columnas_requeridas = [
        "supplier_id",
        "supplier",
        "country",
        "city",
        "purchase_date",
        "amount",
        "discount",
        "weight",
        "units",
        "unit_price",
        "contact_email",
    ]

    datos = pd.read_csv(
        archivo_datos,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8-sig",
    )

    datos.columns = [
        columna.replace("\ufeff", "")
        .strip()
        .lower()
        .replace(" ", "_")
        for columna in datos.columns
    ]

    faltantes = datos.apply(
        lambda columna: columna.str.strip().isin(["", "N/A"])
    )

    patron_email = re.compile(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    def unidad_invalida(valor):

        try:
            numero = float(valor)
        except ValueError:
            return False

        return numero <= 0 or numero != int(numero)

    emails_invalidos = 0

    if "contact_email" in datos.columns:
        for email in datos["contact_email"]:
            if not patron_email.match(email.strip()):
                emails_invalidos += 1

    unidades_invalidas = 0

    if "units" in datos.columns:
        for unidad in datos["units"]:

            if unidad.strip() in ("", "N/A"):
                continue

            if unidad_invalida(unidad):
                unidades_invalidas += 1

    reporte = {
        "row_count": int(datos.shape[0]),
        "column_count": int(datos.shape[1]),
        "missing_required_columns": sorted(
            set(columnas_requeridas) - set(datos.columns)
        ),
        "unexpected_columns": sorted(
            set(datos.columns) - set(columnas_requeridas)
        ),
        "duplicate_row_count": int(datos.duplicated().sum()),
        "duplicate_supplier_id_row_count": (
            int(datos["supplier_id"].duplicated(keep=False).sum())
            if "supplier_id" in datos.columns
            else 0
        ),
        "missing_value_count_by_column": {
            columna: int(faltantes[columna].sum())
            for columna in datos.columns
        },
        "invalid_email_count": emails_invalidos,
        "invalid_unit_count": unidades_invalidas,
        "country_values": (
            sorted(datos["country"].unique().tolist())
            if "country" in datos.columns
            else []
        ),
    }

    with open(
        carpeta_salida / "data_quality_report.json",
        "w",
        encoding="utf-8",
    ) as archivo:
        json.dump(
            reporte,
            archivo,
            ensure_ascii=False,
            indent=2,
        )

    return reporte