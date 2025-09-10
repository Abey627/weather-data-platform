import logging
from weather.integration.clients.geocoding import GeocodingClient

logger = logging.getLogger(__name__)

class GeocodingService:
    """Service for converting city names to geographical coordinates"""
    
    @staticmethod
    def get_coordinates(city):
        """
        Convert a city name to geographical coordinates
        
        Args:
            city (str): City name to geocode
            
        Returns:
            dict: Dictionary containing latitude and longitude
        """
        # Delegate directly to the client - let the client handle specific errors
        # as it already has appropriate error handling
        return GeocodingClient.get_coordinates(city)
