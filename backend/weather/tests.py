from django.test import TestCase
from rest_framework.test import APIClient
from .models import WeatherData

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

class WeatherAPITests(TestCase):
    """Tests for the Weather API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_average_endpoint_validation(self):
        """Test validation on the average endpoint"""
        # Test with missing parameters
        response = self.client.get('/api/weather/average')
        self.assertEqual(response.status_code, 400)
        
        # Test with invalid days parameter
        response = self.client.get('/api/weather/average?city=London&days=0')
        self.assertEqual(response.status_code, 400)
