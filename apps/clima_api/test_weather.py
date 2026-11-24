import unittest
from unittest.mock import Mock, patch

import requests

from apps.clima_api.weather import find_location, get_current_weather


class WeatherTests(unittest.TestCase):
    @patch("apps.clima_api.weather.requests.get")
    def test_find_location_returns_first_match(self, get):
        get.return_value.json.return_value = {
            "results": [{"name": "Madrid", "latitude": 40.4, "longitude": -3.7}]
        }

        location = find_location(" Madrid ")

        self.assertEqual(location["name"], "Madrid")
        self.assertEqual(get.call_args.kwargs["timeout"], 10)

    @patch("apps.clima_api.weather.requests.get")
    def test_weather_uses_location_and_maps_code(self, get):
        geocoding = Mock()
        geocoding.json.return_value = {
            "results": [{"name": "Quito", "latitude": -0.2, "longitude": -78.5}]
        }
        forecast = Mock()
        forecast.json.return_value = {
            "current": {
                "temperature_2m": 18,
                "apparent_temperature": 18,
                "relative_humidity_2m": 60,
                "wind_speed_10m": 5,
                "weather_code": 0,
                "time": "2026-01-01T10:00",
            }
        }
        get.side_effect = [geocoding, forecast]

        report = get_current_weather("Quito")

        self.assertEqual(report["description"], "Despejado")
        self.assertEqual(get.call_count, 2)

    @patch("apps.clima_api.weather.requests.get")
    def test_http_errors_are_not_suppressed(self, get):
        get.return_value.raise_for_status.side_effect = requests.HTTPError("fallo HTTP")

        with self.assertRaises(requests.HTTPError):
            find_location("Lima")

    def test_empty_city_is_rejected_without_request(self):
        with patch("apps.clima_api.weather.requests.get") as get:
            with self.assertRaises(ValueError):
                find_location("  ")
        get.assert_not_called()

    @patch("apps.clima_api.weather.requests.get")
    def test_unknown_city_is_reported(self, get):
        get.return_value.json.return_value = {}

        with self.assertRaisesRegex(ValueError, "No se encontró"):
            find_location("Ciudad inventada")


if __name__ == "__main__":
    unittest.main()
