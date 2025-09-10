import requests
import time
import logging
from weather.utils.cache_utils import CacheManager
from weather.utils.constants import GEOCODING_API_BASE_URL, CACHE_TIMEOUT_MONTH, USER_AGENT, DEFAULT_LANGUAGE

logger = logging.getLogger(__name__)

# Rate limiting constant
NOMINATIM_RATE_LIMIT_SECONDS = 1

class GeocodingClient:
    """Client for converting city names to geographical coordinates using Nominatim API"""
    
    @staticmethod
    def get_coordinates(city):
        """
        Convert a city name to geographical coordinates using Nominatim
        
        Args:
            city (str): City name to geocode
            
        Returns:
            dict: Dictionary containing latitude and longitude
        """
        # Prepare cache key
        cache_key = f"geocode_{city.lower()}"
        
        # Define the function to get fresh data
        def fetch_coordinates():
            logger.info(f"Geocoding city: {city}")
            
            # Prepare API request parameters
            params = {
                "q": city,
                "format": "json",
                "limit": 1,
                "addressdetails": 0,
                "featuretype": "city"  # Limit to cities
            }
            
            # Set required headers according to Nominatim usage policy
            headers = {
                "User-Agent": USER_AGENT,
                "Accept-Language": DEFAULT_LANGUAGE
            }
            
            try:
                # Respect Nominatim's usage policy (max 1 request per second)
                time.sleep(NOMINATIM_RATE_LIMIT_SECONDS)
                
                response = requests.get(
                    GEOCODING_API_BASE_URL, 
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    logger.warning(f"No coordinates found for city: {city}")
                    raise ValueError(f"Could not find coordinates for city: {city}")
                
                # Extract coordinates from the first result
                coordinates = {
                    "latitude": float(data[0]["lat"]),
                    "longitude": float(data[0]["lon"])
                }
                
                return coordinates
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error geocoding city '{city}': {str(e)}")
                raise Exception(f"Error geocoding city: {str(e)}")
            except (KeyError, IndexError) as e:
                logger.error(f"Error processing geocoding response for '{city}': {str(e)}")
                raise ValueError(f"Failed to process geocoding response: {str(e)}")
        
        # Use the cache manager to get or set the data
        return CacheManager.get_or_set(cache_key, fetch_coordinates, timeout=CACHE_TIMEOUT_MONTH)
