from pathlib import Path
import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """
    base = Path(__file__).parent.parent

    web = pd.read_csv(
        base / "data" / "historical_requests_web.csv.gz",
        compression="gzip",
        parse_dates=["in_date", "out_date"],
    ).drop_duplicates()

    cartas = pd.read_csv(
        base / "data" / "historical_requests_letter.csv.gz",
        compression="gzip",
        parse_dates=["in_date", "out_date"],
    ).drop_duplicates()

    web["channel"] = "web"
    cartas["channel"] = "letter"

    df = pd.concat(
        [cartas, web],
        ignore_index=True,
    )

    df["year"] = df["in_date"].dt.year
    df["day_name"] = df["in_date"].dt.day_name()

    respondidas = df["out_date"].notna()

    dias_calendario = (
        df.loc[respondidas, "out_date"]
        - df.loc[respondidas, "in_date"]
    ).dt.days

    dia_semana = df.loc[
        respondidas,
        "in_date",
    ].dt.weekday

    semanas = dias_calendario // 7
    resto = dias_calendario % 7

    dias_habiles = semanas * 5

    for i in range(1, 7):

        dias_habiles += (
            (resto >= i)
            & ((dia_semana + i) % 7 < 5)
        ).astype(int)

    df["calendar_days"] = pd.Series(
        pd.NA,
        index=df.index,
        dtype="Int64",
    )

    df["business_days"] = pd.Series(
        pd.NA,
        index=df.index,
        dtype="Int64",
    )

    df.loc[
        respondidas,
        "calendar_days",
    ] = dias_calendario

    df.loc[
        respondidas,
        "business_days",
    ] = dias_habiles

    df["on_time"] = (
        respondidas
        & df["business_days"].le(15).fillna(False)
    )

    # ---------------------------------
    # Resumen por canal
    # ---------------------------------

    canales = (
        df.groupby("channel")
        .agg(
            requests=("record_id", "size"),
            answered=("out_date", "count"),
            pending=("out_date", lambda x: x.isna().sum()),
            median_business_days=("business_days", "median"),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
    )

    # ---------------------------------
    # Resumen por año
    # ---------------------------------

    anual = (
        df.groupby(["year", "channel"])
        .agg(
            requests=("record_id", "size"),
            pending=("out_date", lambda x: x.isna().sum()),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
        .sort_values(["year", "channel"])
    )

    # ---------------------------------
    # Resumen por día de entrada
    # ---------------------------------

    dias = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    entrada = (
        df.groupby("day_name")
        .agg(
            requests=("record_id", "size"),
            median_calendar_days=("calendar_days", "median"),
            median_business_days=("business_days", "median"),
        )
        .reindex(dias)
        .reset_index()
    )

    # ---------------------------------
    # Exportar
    # ---------------------------------

    submission = base / "submission"
    submission.mkdir(exist_ok=True)

    canales.to_csv(
        submission / "channel_summary.csv",
        index=False,
    )

    anual.to_csv(
        submission / "yearly_summary.csv",
        index=False,
    )

    entrada.to_csv(
        submission / "entry_day_summary.csv",
        index=False,
    )

    return canales, anual, entrada


if __name__ == "__main__":
    pregunta_01()
