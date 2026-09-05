from icalendar import Calendar, Event
from datetime import datetime, timedelta

from config import COMPETITIONS

from espn_provider import (
    obtener_fechas_competicion,
    obtener_eventos_fecha,
    obtener_detalle_evento
)


def crear_calendario():

    calendario = Calendar()

    calendario.add(
        "prodid",
        "-//SportsWebCal UEFA Champions League//"
    )

    calendario.add(
        "version",
        "2.0"
    )

    calendario.add(
        "X-WR-CALNAME",
        "UEFA Champions League"
    )

    calendario.add(
        "X-WR-CALDESC",
        "SportsWebCal UEFA Champions League Calendar"
    )

    slug = COMPETITIONS[0]["slug"]

    fechas = obtener_fechas_competicion(slug)

    eventos_agregados = set()
    total = 0

    for fecha in fechas:

        eventos = obtener_eventos_fecha(
            slug,
            fecha
        )

        for ref in eventos:

            try:

                partido = obtener_detalle_evento(
                    ref
                )

                uid = partido["id"]

                if uid in eventos_agregados:
                    continue

                eventos_agregados.add(uid)

                nombre = partido["name"]

                if " at " in nombre:

                    visitante, local = (
                        nombre.split(" at ")
                    )

                    titulo = (
                        f"{local} vs {visitante}"
                    )

                else:

                    titulo = nombre

                inicio = datetime.fromisoformat(
                    partido["date"].replace(
                        "Z",
                        "+00:00"
                    )
                )

                termino = (
                    inicio +
                    timedelta(hours=2)
                )

                estadio = "Venue to be confirmed"

                try:
                    estadio = (
                        partido["competitions"][0]
                        ["venue"]
                        ["fullName"]
                    )
                except Exception:
                    pass

                evento = Event()

                evento.add(
                    "uid",
                    uid
                )

                evento.add(
                    "summary",
                    titulo
                )

                evento.add(
                    "location",
                    estadio
                )

                evento.add(
                    "description",
                    (
                        "Competition: UEFA Champions League\n\n"
                        f"Venue: {estadio}\n\n"
                        "Source: ESPN Core API\n\n"
                        "SportsWebCal"
                    )
                )

                evento.add(
                    "dtstart",
                    inicio
                )

                evento.add(
                    "dtend",
                    termino
                )

                calendario.add_component(
                    evento
                )

                total += 1

            except Exception as e:

                print(
                    f"ERROR: {ref}"
                )

                print(e)

    with open(
        "docs/champions.ics",
        "wb"
    ) as archivo:

        archivo.write(
            calendario.to_ical()
        )

    print(
        f"PARTIDOS GENERADOS: {total}"
    )


if __name__ == "__main__":
    crear_calendario()
