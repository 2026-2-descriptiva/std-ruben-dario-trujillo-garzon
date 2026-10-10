import gzip


def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna.
    """

    meses = {}

    with gzip.open("data/data.csv.gz", "rt") as archivo:
        for registro in archivo:
            datos = registro.strip().split("\t")

            if len(datos) < 3:
                continue

            fecha = datos[2]
            _, mes, _ = fecha.split("-")

            meses[mes] = meses.setdefault(mes, 0) + 1

    return [(mes, meses[mes]) for mes in sorted(meses)]