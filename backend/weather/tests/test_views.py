import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from datetime import date, timedelta
from weather.views import WeatherAverageView, WeatherDataListView
from weather.models import WeatherData

@pytest.fixture
def api_factory():
    """Fixture for API request factory"""
    return APIRequestFactory()

@pytest.fixture
def sample_weather_data():
    """Fixture for sample weather data"""
    return [
        {"date": "2025-09-10", "temperature": 25.5},
        {"date": "2025-09-11", "temperature": 26.8},
        {"date": "2025-09-12", "temperature": 24.3},
    ]

class TestWeatherAverageView:
    """Tests for WeatherAverageView"""
    
    def test_missing_parameters(self, api_factory):
        """Test validation when parameters are missing"""
        view = WeatherAverageView.as_view()
        
        # Test without any parameters
        request = api_factory.get('/api/weather/average')
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Test with only city
        request = api_factory.get('/api/weather/average', {'city': 'New York'})
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Test with only days
        request = api_factory.get('/api/weather/average', {'days': 5})
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_invalid_days_parameter(self, api_factory):
        """Test validation with invalid days parameter"""
        view = WeatherAverageView.as_view()
        
        # Test with days=0
        request = api_factory.get('/api/weather/average', {'city': 'New York', 'days': 0})
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Test with negative days
        request = api_factory.get('/api/weather/average', {'city': 'New York', 'days': -5})
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Test with non-integer days
        request = api_factory.get('/api/weather/average', {'city': 'New York', 'days': 'abc'})
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('weather.views.WeatherService.get_historical_weather')
    @patch('weather.views.WeatherService.calculate_average_temperature')
    @patch('weather.views.get_date_range')
    def test_successful_response(self, mock_date_range, mock_calc_avg, mock_get_weather, api_factory, sample_weather_data):
        """Test successful response"""
        view = WeatherAverageView.as_view()
        
        # Setup mocks
        mock_get_weather.return_value = sample_weather_data
        mock_calc_avg.return_value = 25.53
        start_date = date(2025, 9, 10)
        end_date = date(2025, 9, 12)
        mock_date_range.return_value = (start_date, end_date)
        
        # Make request
        request = api_factory.get('/api/weather/average', {'city': 'New York', 'days': 3})
        response = view(request)
        
        # Check response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['city'] == 'New York'
        assert response.data['average_temperature'] == 25.53
        assert response.data['days'] == 3
        assert response.data['start_date'] == start_date.isoformat()
        assert response.data['end_date'] == end_date.isoformat()
        
        # Verify mocks were called correctly
        mock_get_weather.assert_called_once_with('New York', 3)
        mock_calc_avg.assert_called_once_with(sample_weather_data)
        mock_date_range.assert_called_once_with(3)
    
    @patch('weather.views.WeatherService.get_historical_weather')
    def test_weather_service_error(self, mock_get_weather, api_factory):
        """Test error handling when WeatherService raises an exception"""
        view = WeatherAverageView.as_view()
        
        # Setup mock to raise an error
        mock_get_weather.side_effect = ValueError("City not found")
        
        # Make request
        request = api_factory.get('/api/weather/average', {'city': 'NonExistentCity', 'days': 3})
        response = view(request)
        
        # Check response
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "City not found" in str(response.data)
        
        # Verify mock was called
        mock_get_weather.assert_called_once_with('NonExistentCity', 3)
    
    @patch('weather.views.WeatherService.get_historical_weather')
    def test_unexpected_error(self, mock_get_weather, api_factory):
        """Test handling of unexpected errors"""
        view = WeatherAverageView.as_view()
        
        # Setup mock to raise an unexpected error
        mock_get_weather.side_effect = Exception("Unexpected error")
        
        # Make request
        request = api_factory.get('/api/weather/average', {'city': 'New York', 'days': 3})
        response = view(request)
        
        # Check response
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "unexpected error" in str(response.data['error']).lower()
        
        # Verify mock was called
        mock_get_weather.assert_called_once_with('New York', 3)

@pytest.mark.django_db
class TestWeatherDataListView:
    """Tests for WeatherDataListView"""
    
    @pytest.fixture
    def setup_weather_data(self):
        """Fixture to create test weather data in the database"""
        # Create test data for different cities and dates
        WeatherData.objects.create(city="New York", date="2025-09-10", temperature=25.5)
        WeatherData.objects.create(city="New York", date="2025-09-11", temperature=26.8)
        WeatherData.objects.create(city="London", date="2025-09-10", temperature=18.2)
        WeatherData.objects.create(city="London", date="2025-09-11", temperature=17.5)
        WeatherData.objects.create(city="Tokyo", date="2025-09-10", temperature=28.9)
    
    def test_list_all_weather_data(self, api_factory, setup_weather_data):
        """Test listing all weather data"""
        view = WeatherDataListView.as_view()
        
        # Make request with no filters
        request = api_factory.get('/api/weather/data')
        response = view(request)
        
        # Check response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5  # All 5 records
    
    def test_filter_by_city(self, api_factory, setup_weather_data):
        """Test filtering by city"""
        view = WeatherDataListView.as_view()
        
        # Make request filtered by city
        request = api_factory.get('/api/weather/data', {'city': 'New York'})
        response = view(request)
        
        # Check response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # Only New York records
        for item in response.data:
            assert item['city'] == 'New York'
    
    def test_filter_by_date_range(self, api_factory, setup_weather_data):
        """Test filtering by date range"""
        view = WeatherDataListView.as_view()
        
        # Make request filtered by date range
        request = api_factory.get('/api/weather/data', {'start_date': '2025-09-11'})
        response = view(request)
        
        # Check response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # Only records for 2025-09-11
        for item in response.data:
            assert item['date'] == '2025-09-11'
    
    def test_combined_filters(self, api_factory, setup_weather_data):
        """Test combining multiple filters"""
        view = WeatherDataListView.as_view()
        
        # Make request with multiple filters
        request = api_factory.get('/api/weather/data', {
            'city': 'New York',
            'start_date': '2025-09-10',
            'end_date': '2025-09-10'
        })
        response = view(request)
        
        # Check response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # Only one record matches all criteria
        assert response.data[0]['city'] == 'New York'
        assert response.data[0]['date'] == '2025-09-10'