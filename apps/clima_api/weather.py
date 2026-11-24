"""Consulta el clima actual usando la API publica de Open-Meteo."""

from typing import Any

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_CODES = {
    0: "Despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Niebla",
    48: "Niebla con escarcha",
    51: "Llovizna ligera",
    53: "Llovizna moderada",
    55: "Llovizna intensa",
    61: "Lluvia ligera",
    63: "Lluvia moderada",
    65: "Lluvia intensa",
    71: "Nevada ligera",
    73: "Nevada moderada",
    75: "Nevada intensa",
    80: "Chubascos ligeros",
    81: "Chubascos moderados",
    82: "Chubascos fuertes",
    95: "Tormenta",
}


def _get_json(url: str, params: dict[str, Any]) -> dict[str, Any]:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def find_location(city: str) -> dict[str, Any]:
    """Busca una ciudad y devuelve su primer resultado geográfico."""
    city = city.strip()
    if not city:
        raise ValueError("El nombre de la ciudad no puede estar vacío.")

    data = _get_json(
        GEOCODING_URL,
        {"name": city, "count": 1, "language": "es", "format": "json"},
    )
    results = data.get("results", [])
    if not results:
        raise ValueError(f"No se encontró la ciudad «{city}».")
    return results[0]


def get_current_weather(city: str) -> dict[str, Any]:
    """Obtiene ubicación y condiciones actuales para una ciudad."""
    location = find_location(city)
    forecast = _get_json(
        FORECAST_URL,
        {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": (
                "temperature_2m,apparent_temperature,relative_humidity_2m,"
                "wind_speed_10m,weather_code"
            ),
            "timezone": "auto",
        },
    )
    return {
        "location": location,
        "current": forecast["current"],
        "description": WEATHER_CODES.get(
            forecast["current"].get("weather_code"), "Condición desconocida"
        ),
    }
