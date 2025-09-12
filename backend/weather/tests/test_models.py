from django.test import TestCase
from weather.models import WeatherData

class WeatherDataModelTests(TestCase):
    """Tests for the WeatherData model"""
    
    def setUp(self):
        # Create test data
        WeatherData.objects.create(
            city="Test City",
            date="2025-01-01",
            temperature=25.5
        )
    
    def test_weather_data_str(self):
        """Test the string representation of a WeatherData object"""
        weather_data = WeatherData.objects.get(city="Test City")
        self.assertEqual(str(weather_data), "Test City - 2025-01-01 - 25.5°C")