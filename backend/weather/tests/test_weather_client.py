import pytest
from unittest.mock import patch, MagicMock
from weather.integration.clients.weather import WeatherClient

@patch('weather.integration.clients.weather.requests.get')
@patch('weather.integration.clients.weather.CacheManager.get_or_set')
class TestWeatherClient:
    """Tests for WeatherClient"""
    
    def test_get_historical_weather_success(self, mock_cache, mock_requests):
        """Test successful historical weather API call"""
        # Setup
        latitude = 40.71
        longitude = -74.01
        start_date = "2025-09-10"
        end_date = "2025-09-12"
        
        # Create a mock response
        mock_response = MagicMock()
        expected_data = {
            "daily": {
                "time": ["2025-09-10", "2025-09-11", "2025-09-12"],
                "temperature_2m_max": [25.5, 26.8, 24.3]
            }
        }
        mock_response.json.return_value = expected_data
        mock_requests.return_value = mock_response
        
        # Configure the cache mock to call the real function
        def cache_side_effect(key, func, timeout):
            return func()
        
        mock_cache.side_effect = cache_side_effect
        
        # Call the method
        result = WeatherClient.get_historical_weather(latitude, longitude, start_date, end_date)
        
        # Verify
        assert result == expected_data
        mock_requests.assert_called_once()
        
        # Check request parameters
        args, kwargs = mock_requests.call_args
        assert 'params' in kwargs
        params = kwargs['params']
        assert params['latitude'] == latitude
        assert params['longitude'] == longitude
        assert params['start_date'] == start_date
        assert params['end_date'] == end_date
    
    def test_get_historical_weather_request_error(self, mock_cache, mock_requests):
        """Test handling of request errors"""
        # Setup
        latitude = 40.71
        longitude = -74.01
        start_date = "2025-09-10"
        end_date = "2025-09-12"
        
        # Configure the request to raise an exception
        mock_requests.side_effect = Exception("Network error")
        
        # Configure the cache mock to call the real function
        def cache_side_effect(key, func, timeout):
            return func()
        
        mock_cache.side_effect = cache_side_effect
        
        # Call the method and expect an error
        with pytest.raises(Exception) as excinfo:
            WeatherClient.get_historical_weather(latitude, longitude, start_date, end_date)
        
        # Verify the error message
        assert "Error fetching weather data" in str(excinfo.value) or "Network error" in str(excinfo.value)