import pytest
from unittest.mock import patch, MagicMock
from weather.integration.services.geocoding import GeocodingService
from weather.integration.clients.geocoding import GeocodingClient

class TestGeocodingService:
    """Tests for GeocodingService"""
    
    @patch('weather.integration.clients.geocoding.GeocodingClient.get_coordinates')
    def test_get_coordinates_success(self, mock_client):
        """Test successful geocoding"""
        # Setup
        city = "New York"
        expected_coords = {"latitude": 40.71, "longitude": -74.01}
        mock_client.return_value = expected_coords
        
        # Call the method
        result = GeocodingService.get_coordinates(city)
        
        # Verify
        assert result == expected_coords
        mock_client.assert_called_once_with(city)
    
    @patch('weather.integration.clients.geocoding.GeocodingClient.get_coordinates')
    def test_get_coordinates_error(self, mock_client):
        """Test error handling in geocoding"""
        # Setup
        city = "NonExistentCity"
        mock_client.side_effect = ValueError("Could not find coordinates for city")
        
        # Call the method and expect an error
        with pytest.raises(ValueError) as excinfo:
            GeocodingService.get_coordinates(city)
        
        # Verify the error message
        assert "Could not find coordinates for city" in str(excinfo.value)
        mock_client.assert_called_once_with(city)

@patch('weather.integration.clients.geocoding.requests.get')
@patch('weather.integration.clients.geocoding.CacheManager.get_or_set')
class TestGeocodingClient:
    """Tests for GeocodingClient"""
    
    def test_get_coordinates_success(self, mock_cache, mock_requests):
        """Test successful geocoding API call"""
        # Setup
        city = "New York"
        
        # Create a mock response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"lat": "40.71", "lon": "-74.01"}
        ]
        mock_requests.return_value = mock_response
        
        # Configure the cache mock to call the real function
        def cache_side_effect(key, func, timeout):
            return func()
        
        mock_cache.side_effect = cache_side_effect
        
        # Call the method
        result = GeocodingClient.get_coordinates(city)
        
        # Verify
        assert result == {"latitude": 40.71, "longitude": -74.01}
        mock_requests.assert_called_once()
    
    def test_get_coordinates_empty_response(self, mock_cache, mock_requests):
        """Test handling of empty API response"""
        # Setup
        city = "NonExistentCity"
        
        # Create a mock response with empty results
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_requests.return_value = mock_response
        
        # Configure the cache mock to call the real function
        def cache_side_effect(key, func, timeout):
            return func()
        
        mock_cache.side_effect = cache_side_effect
        
        # Call the method and expect an error
        with pytest.raises(ValueError) as excinfo:
            GeocodingClient.get_coordinates(city)
        
        # Verify the error message
        assert f"Could not find coordinates for city: {city}" in str(excinfo.value)
    
    def test_get_coordinates_request_error(self, mock_cache, mock_requests):
        """Test handling of request errors"""
        # Setup
        city = "New York"
        
        # Configure the request to raise an exception
        mock_requests.side_effect = Exception("Network error")
        
        # Configure the cache mock to call the real function
        def cache_side_effect(key, func, timeout):
            return func()
        
        mock_cache.side_effect = cache_side_effect
        
        # Call the method and expect an error
        with pytest.raises(Exception) as excinfo:
            GeocodingClient.get_coordinates(city)
        
        # Verify the error message
        assert "Error geocoding city" in str(excinfo.value) or str(excinfo.value) == "Network error"
    
    def test_get_coordinates_response_processing_error(self, mock_cache, mock_requests):
        """Test handling of response processing errors"""
        # Setup
        city = "New York"
        
        # Create a mock response with invalid data structure
        mock_response = MagicMock()
        mock_response.json.return_value = [{"invalid_key": "value"}]  # Missing lat/lon
        mock_requests.return_value = mock_response
        
        # Configure the cache mock to call the real function
        def cache_side_effect(key, func, timeout):
            return func()
        
        mock_cache.side_effect = cache_side_effect
        
        # Call the method and expect an error
        with pytest.raises(ValueError) as excinfo:
            GeocodingClient.get_coordinates(city)
        
        # Verify the error message
        assert "Failed to process geocoding response" in str(excinfo.value)