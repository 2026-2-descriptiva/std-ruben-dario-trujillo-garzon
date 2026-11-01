from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """
    base = Path(__file__).parent.parent

    df = pd.read_csv(
        base / "data" / "sales.csv.gz",
        compression="gzip",
    )

    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    df["order_month"] = df["OrderDate"].dt.to_period("M")

    primer_mes = (
        df.groupby("CustomerID")["order_month"]
        .min()
    )

    df["cohort_month"] = df["CustomerID"].map(primer_mes)

    df["period_index"] = (
        (df["order_month"].dt.year - df["cohort_month"].dt.year) * 12
        + df["order_month"].dt.month
        - df["cohort_month"].dt.month
    )

    cohort_size = (
        primer_mes.groupby(primer_mes)
        .size()
    )

    cohortes = (
        df.groupby(["cohort_month", "period_index"])
        ["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )

    cohortes["cohort_month"] = (
        cohortes["cohort_month"]
        .astype(str)
    )

    cohortes["cohort_size"] = cohortes[
        "cohort_month"
    ].map(
        cohort_size.rename(index=str)
    )

    cohortes["retention_rate"] = (
        cohortes["active_customers"]
        / cohortes["cohort_size"]
    )

    cohortes = cohortes[
        [
            "cohort_month",
            "period_index",
            "active_customers",
            "cohort_size",
            "retention_rate",
        ]
    ]

    cohortes = cohortes.sort_values(
        ["cohort_month", "period_index"]
    ).reset_index(drop=True)

    # -------------------------
    # Exportar CSV
    # -------------------------

    submission = base / "submission"
    submission.mkdir(exist_ok=True)

    cohortes.to_csv(
        submission / "cohort_retention.csv",
        index=False,
    )

    # -------------------------
    # Heatmap
    # -------------------------

    heatmap = cohortes.pivot(
        index="cohort_month",
        columns="period_index",
        values="retention_rate",
    )

    fig, ax = plt.subplots(
        figsize=(
            max(8, heatmap.shape[1]),
            max(4, heatmap.shape[0] * 0.7),
        )
    )

    grafico = ax.imshow(
        heatmap,
        cmap="YlGnBu",
        aspect="auto",
        vmin=0,
        vmax=1,
    )

    grafico.cmap.set_bad("white")

    ax.set_xticks(
        range(len(heatmap.columns)),
        heatmap.columns,
    )

    ax.set_yticks(
        range(len(heatmap.index)),
        heatmap.index,
    )

    ax.set_xlabel("Período")
    ax.set_ylabel("Cohorte")
    ax.set_title("Retención por cohorte")

    for fila in range(heatmap.shape[0]):
        for columna in range(heatmap.shape[1]):

            valor = heatmap.iloc[fila, columna]

            if pd.notna(valor):
                ax.text(
                    columna,
                    fila,
                    f"{valor:.0%}",
                    ha="center",
                    va="center",
                    fontsize=8,
                )

    fig.colorbar(
        grafico,
        ax=ax,
        label="Retención",
    )

    fig.tight_layout()

    fig.savefig(
        submission / "cohort_retention_heatmap.png",
        dpi=150,
    )

    plt.close()

    return cohortes


if __name__ == "__main__":
    build_cohort_analysis()
