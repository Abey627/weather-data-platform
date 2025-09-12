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
    def _make_geocoding_request(city):
        """
        Make a direct request to the geocoding API.
        This is an internal method exposed for contract testing.
        
        Args:
            city (str): City name to geocode
            
        Returns:
            list: Raw API response data
        """
        logger.info(f"Making direct geocoding request for city: {city}")
        
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
        
        # Respect Nominatim's usage policy (max 1 request per second)
        time.sleep(NOMINATIM_RATE_LIMIT_SECONDS)
        
        response = requests.get(
            GEOCODING_API_BASE_URL, 
            params=params,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def get_coordinates(city, _skip_cache=False):
        """
        Convert a city name to geographical coordinates using Nominatim
        
        Args:
            city (str): City name to geocode
            _skip_cache (bool, optional): If True, bypass the cache (used for contract testing)
            
        Returns:
            dict: Dictionary containing latitude and longitude
        """
        # Prepare cache key
        cache_key = f"geocode_{city.lower()}"
        
        # Define the function to get fresh data
        def fetch_coordinates():
            logger.info(f"Geocoding city: {city}")
            
            try:
                # Get raw response from geocoding API
                data = GeocodingClient._make_geocoding_request(city)
                
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
        
        # Skip cache if requested (for contract testing)
        if _skip_cache:
            return fetch_coordinates()
            
        # Use the cache manager to get or set the data
        return CacheManager.get_or_set(cache_key, fetch_coordinates, timeout=CACHE_TIMEOUT_MONTH)
