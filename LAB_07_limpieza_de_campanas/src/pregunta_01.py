from pathlib import Path
import pandas as pd
import numpy as np


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.

    La función debe generar:
    - client.csv
    - campaign.csv
    - economics.csv

    y retornar los tres DataFrames en ese mismo orden.
    """

    base = Path(__file__).parent.parent

    carpeta_datos = base / "data"
    carpeta_salida = base / "submission"

    carpeta_salida.mkdir(exist_ok=True)

    archivos = sorted(
        carpeta_datos.glob("bank-marketing-campaing-*.csv.gz")
    )

    datos = pd.concat(
        [pd.read_csv(archivo) for archivo in archivos],
        ignore_index=True,
    )

    datos = datos.sort_values("client_id").reset_index(drop=True)

    # -----------------------------
    # CLIENT
    # -----------------------------

    client = datos[
        [
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage",
        ]
    ].copy()

    client["job"] = (
        client["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )

    client["education"] = (
        client["education"]
        .str.replace(".", "_", regex=False)
        .replace("unknown", np.nan)
    )

    client["credit_default"] = (
        client["credit_default"]
        .eq("yes")
        .astype(int)
    )

    client["mortgage"] = (
        client["mortgage"]
        .eq("yes")
        .astype(int)
    )

    # -----------------------------
    # CAMPAIGN
    # -----------------------------

    campaign = datos[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
        ]
    ].copy()

    campaign["previous_outcome"] = (
        campaign["previous_outcome"]
        .eq("success")
        .astype(int)
    )

    campaign["campaign_outcome"] = (
        campaign["campaign_outcome"]
        .eq("yes")
        .astype(int)
    )

    meses = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }

    campaign["last_contact_date"] = (
        "2022-"
        + datos["month"].str.lower().map(meses)
        + "-"
        + datos["day"].astype(str).str.zfill(2)
    )

    # -----------------------------
    # ECONOMICS
    # -----------------------------

    economics = datos[
        [
            "client_id",
            "cons_price_idx",
            "euribor_three_months",
        ]
    ].copy()

    # -----------------------------
    # EXPORTAR
    # -----------------------------

    client.to_csv(
        carpeta_salida / "client.csv",
        index=False,
    )

    campaign.to_csv(
        carpeta_salida / "campaign.csv",
        index=False,
    )

    economics.to_csv(
        carpeta_salida / "economics.csv",
        index=False,
    )

    return client, campaign, economics
