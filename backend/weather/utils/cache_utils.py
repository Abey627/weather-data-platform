"""
Caching utilities for the weather application
"""
from django.core.cache import cache

class CacheManager:
    """
    Utility class for managing cache operations
    """
    
    @staticmethod
    def get_or_set(key, getter_func, timeout=3600):
        """
        Get a value from cache or set it if not found
        
        Args:
            key (str): Cache key
            getter_func (callable): Function to get the value if not in cache
            timeout (int): Cache timeout in seconds (default: 1 hour)
            
        Returns:
            Any: The cached or newly fetched value
        """
        # Django's cache.get_or_set already implements this pattern efficiently
        return cache.get_or_set(key, getter_func, timeout)
