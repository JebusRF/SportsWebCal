import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def obtener_fechas_competicion(slug):

    url = (
        f"https://sports.core.api.espn.com/v2/"
        f"sports/soccer/leagues/{slug}/calendar/ondays"
    )

    respuesta = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    respuesta.raise_for_status()

    datos = respuesta.json()

    fechas = []

    for fecha in datos["eventDate"]["dates"]:
        fechas.append(fecha[:10].replace("-", ""))

    return fechas


def obtener_eventos_fecha(slug, fecha):

    url = (
        f"https://sports.core.api.espn.com/v2/"
        f"sports/soccer/leagues/{slug}/events"
        f"?dates={fecha}"
    )

    respuesta = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    respuesta.raise_for_status()

    datos = respuesta.json()

    eventos = []

    for item in datos.get("items", []):
        eventos.append(item["$ref"])

    return eventos


def obtener_detalle_evento(url):

    url = url.replace("http://", "https://")

    respuesta = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    respuesta.raise_for_status()

    return respuesta.json()
