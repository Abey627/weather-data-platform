import logging
from datetime import datetime
from weather.integration.services.geocoding import GeocodingService
from weather.integration.clients.weather import WeatherClient
from weather.utils.date_utils import get_date_range
from weather.utils.cache_utils import CacheManager
from weather.utils.constants import CACHE_TIMEOUT_HOUR
from weather.models import WeatherData

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
            
            # Try to get data from the database first
            db_data = WeatherService.get_weather_from_db(city, start_date, end_date)
            
            # If we have complete data in the database, return it
            if db_data and len(db_data) == days:
                logger.info(f"Retrieved complete weather data for {city} from database")
                return db_data
            
            # Otherwise, fetch from API
            logger.info(f"Fetching weather data for {city} from external API")
            
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
                processed_data = WeatherService._process_weather_data(data)
                
                # Store the data in the database for future use
                WeatherService.store_weather_data(city, processed_data)
                
                return processed_data
                
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
    def store_weather_data(city, temperature_data):
        """
        Store weather data in the database
        
        Args:
            city (str): City name
            temperature_data (list): List of temperature data
            
        Returns:
            list: List of created or updated WeatherData objects
        """
        stored_data = []
        
        for item in temperature_data:
            # Convert string date to datetime object if needed
            date_obj = item["date"]
            if isinstance(date_obj, str):
                date_obj = datetime.strptime(date_obj, "%Y-%m-%d").date()
                
            # Use get_or_create to avoid duplicates based on unique_together constraint
            weather_obj, created = WeatherData.objects.get_or_create(
                city=city,
                date=date_obj,
                defaults={"temperature": item["temperature"]}
            )
            
            # If the record already existed but the temperature is different, update it
            if not created and weather_obj.temperature != item["temperature"]:
                weather_obj.temperature = item["temperature"]
                weather_obj.save()
                
            stored_data.append(weather_obj)
            
            if created:
                logger.info(f"Created new weather record for {city} on {date_obj}")
            else:
                logger.info(f"Updated existing weather record for {city} on {date_obj}")
                
        return stored_data
    
    @staticmethod
    def get_weather_from_db(city, start_date, end_date):
        """
        Get weather data from the database for a city and date range
        
        Args:
            city (str): City name
            start_date (date): Start date
            end_date (date): End date
            
        Returns:
            list: List of temperature data from the database
        """
        # Query the database for weather data for the city and date range
        weather_data = WeatherData.objects.filter(
            city=city,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')
        
        # Convert queryset to the same format as the API data
        return [
            {"date": data.date.strftime("%Y-%m-%d"), "temperature": data.temperature} 
            for data in weather_data
        ]
    
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
