import logging
from weather.integration.services.geocoding import GeocodingService
from weather.integration.clients.weather import WeatherClient
from weather.utils.date_utils import get_date_range
from weather.utils.cache_utils import CacheManager
from weather.utils.constants import CACHE_TIMEOUT_HOUR

logger = logging.getLogger(__name__)

class WeatherService:
    """Service for fetching weather data from external API"""
    
    @staticmethod
    def get_historical_weather(city, days):
        """
        Fetch historical weather data for a city for the specified number of days
        
        Args:
            city (str): City name
            days (int): Number of days to fetch data for
            
        Returns:
            list: List of temperature data for each day
        """
        # Prepare cache key
        cache_key = f"processed_weather_{city}_{days}"
        
        # Define the function to get fresh data
        def fetch_and_process_weather():
            logger.info(f"Fetching and processing weather data for {city} for {days} days")
            
            # Calculate date range using utility function
            start_date, end_date = get_date_range(days)
            
            # Use the Geocoding service to get coordinates for the city
            try:
                coords = GeocodingService.get_coordinates(city)
            except ValueError as e:
                logger.error(f"Geocoding error for city '{city}': {str(e)}")
                raise ValueError(f"Could not find coordinates for city: {city}. Please check the spelling or try another city.")
            except Exception as e:
                logger.error(f"Geocoding service error: {str(e)}")
                raise Exception(f"Geocoding service error: {str(e)}")
            
            # Use the Weather client to get historical weather data
            try:
                data = WeatherClient.get_historical_weather(
                    coords["latitude"],
                    coords["longitude"],
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d")
                )
                
                # Process the data
                return WeatherService._process_weather_data(data)
                
            except Exception as e:
                logger.error(f"Error fetching weather data: {str(e)}")
                raise Exception(f"Error fetching weather data: {str(e)}")
        
        # Use the cache manager to get or set the data
        return CacheManager.get_or_set(cache_key, fetch_and_process_weather, timeout=CACHE_TIMEOUT_HOUR)
    
    @staticmethod
    def _process_weather_data(data):
        """
        Process raw weather data into a simplified format
        
        Args:
            data (dict): Raw weather data from API
            
        Returns:
            list: Processed list of temperature data
        """
        daily_data = data.get("daily", {})
        dates = daily_data.get("time", [])
        temperatures = daily_data.get("temperature_2m_max", [])
        
        # Use list comprehension for more concise code
        return [{"date": dates[i], "temperature": temperatures[i]} for i in range(len(dates))]
    
    @staticmethod
    def calculate_average_temperature(temperature_data):
        """
        Calculate the average temperature from the provided data
        
        Args:
            temperature_data (list): List of temperature data
            
        Returns:
            float: Average temperature
        """
        if not temperature_data:
            return 0
            
        # Use more concise calculation with list comprehension
        return round(sum(item["temperature"] for item in temperature_data) / len(temperature_data), 2)
