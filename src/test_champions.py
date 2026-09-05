from config import COMPETITIONS
from espn_provider import (
    obtener_fechas_competicion,
    obtener_eventos_fecha
)

slug = COMPETITIONS[0]["slug"]

fechas = obtener_fechas_competicion(slug)

print("FECHAS ENCONTRADAS:")
print(fechas)

if fechas:

    eventos = obtener_eventos_fecha(
        slug,
        fechas[0]
    )

    print("")
    print("EVENTOS ENCONTRADOS:")
    print(len(eventos))

    for evento in eventos[:5]:
        print(evento)
