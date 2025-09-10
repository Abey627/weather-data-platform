import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    """Service for fetching weather data from external API"""
    
    # Using Open-Meteo API as it's free and doesn't require API key
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
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
        # Check cache first
        cache_key = f"weather_{city}_{days}"
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Retrieved cached weather data for {city} for {days} days")
            return cached_data
        
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # For this demo, we'll use hardcoded coordinates for a few major cities
        # In a real app, you would use a geocoding service to convert city name to coordinates
        city_coordinates = {
            "new york": {"latitude": 40.71, "longitude": -74.01},
            "london": {"latitude": 51.51, "longitude": -0.13},
            "paris": {"latitude": 48.85, "longitude": 2.35},
            "tokyo": {"latitude": 35.68, "longitude": 139.77},
            "sydney": {"latitude": -33.87, "longitude": 151.21},
            "singapore": {"latitude": 1.29, "longitude": 103.85},
            # Add more cities as needed
        }
        
        city_lower = city.lower()
        if city_lower not in city_coordinates:
            raise ValueError(f"City '{city}' not supported. Please choose from: {', '.join(city_coordinates.keys())}")
        
        coords = city_coordinates[city_lower]
        
        # Prepare API request parameters
        params = {
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "daily": "temperature_2m_max",
            "timezone": "auto"
        }
        
        try:
            response = requests.get(WeatherService.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Process the data
            daily_data = data.get("daily", {})
            dates = daily_data.get("time", [])
            temperatures = daily_data.get("temperature_2m_max", [])
            
            result = []
            for i in range(len(dates)):
                result.append({
                    "date": dates[i],
                    "temperature": temperatures[i]
                })
                
            # Cache the result for 1 hour (3600 seconds)
            cache.set(cache_key, result, 3600)
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            raise Exception(f"Error fetching weather data: {str(e)}")
    
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
            
        total = sum(item["temperature"] for item in temperature_data)
        return round(total / len(temperature_data), 2)
