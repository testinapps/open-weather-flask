import unittest
from weather_fetcher.core import WeatherFetcher
from unittest.mock import patch


class TestWeatherFetcher(unittest.TestCase):
    def setUp(self):
        # Mock API key
        self.fetcher = WeatherFetcher(api_key="test_api_key")

    @patch("weather_fetcher.core.requests.get")
    def test_get_weather_success(self, mock_get):
        # Mock API response
        mock_response = {
            "weather": [{"description": "clear sky"}],
            "main": {"temp": 298.15},
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Test fetching weather
        response = self.fetcher.get_weather("New York")
        self.assertIn("weather", response)
        self.assertEqual(response["main"]["temp"], 298.15)

    @patch("weather_fetcher.core.requests.get")
    def test_get_weather_failure(self, mock_get):
        # Mock API failure
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"message": "city not found"}

        with self.assertRaises(ValueError):
            self.fetcher.get_weather("Invalid City")


if __name__ == "__main__":
    unittest.main()
