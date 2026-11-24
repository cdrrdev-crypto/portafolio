"""Interfaz de línea de comandos para consultar el clima."""

import argparse
import sys

import requests

from .weather import get_current_weather


def main() -> int:
    parser = argparse.ArgumentParser(description="Consulta el clima actual de una ciudad.")
    parser.add_argument("ciudad", help="Nombre de la ciudad (por ejemplo, Madrid)")
    args = parser.parse_args()

    try:
        report = get_current_weather(args.ciudad)
    except (requests.RequestException, ValueError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    location = report["location"]
    current = report["current"]
    place = ", ".join(
        part
        for part in (location.get("name"), location.get("admin1"), location.get("country"))
        if part
    )
    print(f"Clima actual en {place}")
    print(f"  Condición: {report['description']}")
    print(f"  Temperatura: {current['temperature_2m']} °C")
    print(f"  Sensación térmica: {current['apparent_temperature']} °C")
    print(f"  Humedad: {current['relative_humidity_2m']} %")
    print(f"  Viento: {current['wind_speed_10m']} km/h")
    print(f"  Hora local: {current['time']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
