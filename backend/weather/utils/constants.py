"""
Constants and configuration values for the weather application
"""

# Cache timeouts (in seconds)
CACHE_TIMEOUT_HOUR = 3600      # 1 hour
CACHE_TIMEOUT_DAY = 86400      # 1 day
CACHE_TIMEOUT_MONTH = 2592000  # 30 days

# API configuration
USER_AGENT = "WeatherDataPlatform/1.0"
DEFAULT_LANGUAGE = "en-US,en;q=0.9"

# API endpoints
WEATHER_API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_API_BASE_URL = "https://nominatim.openstreetmap.org/search"

# Application limits
MAX_DAYS_ALLOWED = 30
