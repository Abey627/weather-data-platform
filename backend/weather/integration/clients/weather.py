import requests
import logging
from weather.utils.cache_utils import CacheManager
from weather.utils.constants import WEATHER_API_BASE_URL, CACHE_TIMEOUT_HOUR

logger = logging.getLogger(__name__)

class WeatherClient:
    """Client for fetching weather data from Open-Meteo API"""
    
    @staticmethod
    def get_historical_weather(latitude, longitude, start_date, end_date, _skip_cache=False):
        """
        Fetch historical weather data for specific coordinates and date range
        
        Args:
            latitude (float): Latitude of the location
            longitude (float): Longitude of the location
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            _skip_cache (bool, optional): If True, bypass the cache (used for contract testing)
            
        Returns:
            dict: Weather API response data
        """
        # Prepare cache key
        cache_key = f"weather_{latitude}_{longitude}_{start_date}_{end_date}"
        
        # Define the function to get fresh data
        def fetch_weather_data():
            logger.info(f"Fetching weather data for coordinates ({latitude}, {longitude})")
            
            # Prepare API request parameters
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "start_date": start_date,
                "end_date": end_date,
                "daily": "temperature_2m_max",
                "timezone": "auto"
            }
            
            try:
                response = requests.get(WEATHER_API_BASE_URL, params=params)
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching weather data: {str(e)}")
                raise Exception(f"Error fetching weather data: {str(e)}")
        
        # Skip cache if requested (for contract testing)
        if _skip_cache:
            return fetch_weather_data()
            
        # Use the cache manager to get or set the data
        return CacheManager.get_or_set(cache_key, fetch_weather_data, timeout=CACHE_TIMEOUT_HOUR)
