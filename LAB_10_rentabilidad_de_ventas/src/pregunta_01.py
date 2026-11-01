from pathlib import Path
import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """
    base = Path(__file__).parent.parent

    df = pd.read_csv(
        base / "data" / "superstore_orders.csv.gz",
        sep=";",
        decimal=",",
        compression="gzip",
    )

    df["perdida"] = df["Profit"] < 0
    df["perdida_monetaria"] = (-df["Profit"]).where(df["perdida"], 0)

    def resumir(datos):

        resumen = datos.agg(
            lines=("Profit", "size"),
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            loss_lines=("perdida", "sum"),
            lost_profit=("perdida_monetaria", "sum"),
        )

        resumen["profit_margin"] = (
            resumen["profit"] / resumen["sales"]
        )

        resumen["loss_line_rate"] = (
            resumen["loss_lines"] / resumen["lines"]
        )

        return resumen

    # -------------------------
    # Resumen general
    # -------------------------

    general = resumir(df.groupby(lambda x: 0)).iloc[[0]]

    profitability_summary = pd.DataFrame(
        {
            "lines": [int(general["lines"].iloc[0])],
            "orders": [df["Order ID"].nunique()],
            "sales": [general["sales"].iloc[0]],
            "profit": [general["profit"].iloc[0]],
            "profit_margin": [general["profit_margin"].iloc[0]],
            "loss_lines": [int(general["loss_lines"].iloc[0])],
            "loss_line_rate": [general["loss_line_rate"].iloc[0]],
            "lost_profit": [general["lost_profit"].iloc[0]],
        }
    )

    # -------------------------
    # Rangos de descuento
    # -------------------------

    def clasificar_descuento(x):

        if x == 0:
            return "0%"

        if x <= 0.05:
            return "1%-5%"

        if x <= 0.10:
            return "6%-10%"

        return "más de 10%"

    orden = ["0%", "1%-5%", "6%-10%", "más de 10%"]

    df["discount_band"] = df["Discount"].apply(
        clasificar_descuento
    )

    discount_summary = (
        resumir(df.groupby("discount_band"))
        .reindex(orden)
        .reset_index()
    )

    discount_summary = discount_summary[
        [
            "discount_band",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "loss_line_rate",
            "lost_profit",
        ]
    ]

    # -------------------------
    # Segmentos prioritarios
    # -------------------------

    segmentos = resumir(
        df.groupby(
            ["Customer Segment", "Product Category"]
        )
    )

    segmentos = segmentos[
        segmentos["lines"] >= 100
    ]

    segmentos = (
        segmentos.sort_values(
            "lost_profit",
            ascending=False,
        )
        .head(5)
        .reset_index()
    )

    priority_segments = segmentos[
        [
            "Customer Segment",
            "Product Category",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "lost_profit",
        ]
    ]

    # -------------------------
    # Exportar
    # -------------------------

    submission = base / "submission"
    submission.mkdir(exist_ok=True)

    profitability_summary.to_csv(
        submission / "profitability_summary.csv",
        index=False,
    )

    discount_summary.to_csv(
        submission / "discount_summary.csv",
        index=False,
    )

    priority_segments.to_csv(
        submission / "priority_segments.csv",
        index=False,
    )

    return (
        profitability_summary,
        discount_summary,
        priority_segments,
    )


if __name__ == "__main__":
    pregunta_01()
