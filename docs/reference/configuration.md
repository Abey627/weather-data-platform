# Configuration Reference

This document provides a comprehensive reference for all configuration options in the Weather Data Platform.

## Environment Variables

The Weather Data Platform uses environment variables for configuration. These are typically defined in a `.env` file for development and a `.env.prod` file for production.

### Core Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DEBUG` | No | `False` | Set to `True` to enable debug mode |
| `SECRET_KEY` | Yes | None | Django secret key for security |
| `ALLOWED_HOSTS` | No | `localhost,127.0.0.1` | Comma-separated list of allowed hosts |

### Database Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DB_NAME` | Yes | None | PostgreSQL database name |
| `DB_USER` | Yes | None | PostgreSQL username |
| `DB_PASSWORD` | Yes | None | PostgreSQL password |
| `DB_HOST` | Yes | None | PostgreSQL host address |
| `DB_PORT` | No | `5432` | PostgreSQL port |

### Redis Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `REDIS_HOST` | Yes | None | Redis host address |
| `REDIS_PORT` | No | `6379` | Redis port |
| `REDIS_DB` | No | `0` | Redis database number |
| `REDIS_PASSWORD` | No | None | Redis password if authentication is enabled |

### API Keys

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `WEATHER_API_KEY` | Yes | None | API key for the external weather service |
| `GEOCODING_API_KEY` | No | None | API key for the geocoding service (if used) |

### Caching Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CACHE_TIMEOUT` | No | `3600` | Default cache timeout in seconds |
| `CACHE_WEATHER_TIMEOUT` | No | `1800` | Cache timeout for weather data in seconds |

### Logging Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DJANGO_LOG_LEVEL` | No | `INFO` | Log level for Django logs |
| `WEATHER_LOG_LEVEL` | No | `INFO` | Log level for app-specific logs |
| `LOGSTASH_HOST` | No | `logstash` | Logstash host for centralized logging |
| `LOGSTASH_PORT` | No | `5044` | Logstash port for centralized logging |

### Email Settings (📝 Planned)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EMAIL_HOST` | No | None | SMTP server host |
| `EMAIL_PORT` | No | `587` | SMTP server port |
| `EMAIL_USE_TLS` | No | `True` | Whether to use TLS for SMTP |
| `EMAIL_HOST_USER` | No | None | SMTP username |
| `EMAIL_HOST_PASSWORD` | No | None | SMTP password |
| `DEFAULT_FROM_EMAIL` | No | None | Default sender email address |

## Example `.env` File

```ini
# Core settings
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=weather_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis settings
REDIS_HOST=redis
REDIS_PORT=6379

# API keys
WEATHER_API_KEY=your_api_key_here

# Caching settings
CACHE_TIMEOUT=3600
CACHE_WEATHER_TIMEOUT=1800

# Logging settings
DJANGO_LOG_LEVEL=DEBUG
WEATHER_LOG_LEVEL=DEBUG
```

## Django Settings

The Django settings are defined in `weatherapi/settings.py`. The most important settings that can be customized are:

### REST Framework Settings

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/minute',
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```

### Cache Settings

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': int(os.environ.get('CACHE_TIMEOUT', 3600)),
    }
}
```

### External API Settings

```python
# Weather API settings
WEATHER_API_URL = 'https://api.weatherapi.com/v1'
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
WEATHER_API_TIMEOUT = 10  # seconds

# Geocoding API settings (if used)
GEOCODING_API_URL = 'https://api.geocoding-provider.com/v1'
GEOCODING_API_KEY = os.environ.get('GEOCODING_API_KEY')
GEOCODING_API_TIMEOUT = 10  # seconds
```

## Docker Configuration

### Development Configuration

The development Docker configuration is defined in `docker-compose.yml`. Key configuration options include:

- Service definitions (backend, frontend, db, redis)
- Port mappings
- Volume mounts for code and data
- Environment variable configuration

### Production Configuration

The production Docker configuration is defined in `docker-compose.prod.yml`. Key differences from development include:

- Production-optimized service settings
- Nginx for serving static files and as a reverse proxy
- Gunicorn as the WSGI server instead of Django's development server
- Database backup configuration
- Reduced debug output
- Enhanced security settings

## Feature Flags

Feature flags allow enabling/disabling specific features. These are configured in Django settings:

```python
FEATURE_FLAGS = {
    'ENABLE_WEATHER_HISTORY': True,
    'ENABLE_DATA_EXPORT': False,  # Planned feature
    'ENABLE_USER_PROFILES': False,  # Planned feature
}
```

To use a feature flag in code:

```python
from django.conf import settings

if settings.FEATURE_FLAGS.get('ENABLE_WEATHER_HISTORY'):
    # Feature-specific code here
```

## Performance Tuning

### Database Connection Pool

Configure the database connection pool size:

```python
DATABASES = {
    'default': {
        # ... other settings ...
        'CONN_MAX_AGE': 60,  # Keep connections alive for 60 seconds
        'OPTIONS': {
            'MAX_CONNS': 20,  # Maximum number of connections in the pool
        },
    },
}
```

### Caching Strategies

Configure different cache timeouts for different types of data:

```python
WEATHER_CACHE_TIMEOUT = int(os.environ.get('CACHE_WEATHER_TIMEOUT', 1800))  # 30 minutes
GEOCODING_CACHE_TIMEOUT = 86400  # 24 hours
```

## Future Configuration Options (📝 Planned)

The following configuration options are planned for future releases:

### Authentication Settings

```python
# JWT Authentication settings
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
}
```

### Monitoring Settings

```python
# ELK Stack configuration
ELK_ENABLED = True
ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST', 'elasticsearch')
ELASTICSEARCH_PORT = os.environ.get('ELASTICSEARCH_PORT', '9200')
```

> **Legend:**  
> ✅ Implemented - Feature is complete and working  
> 🚧 In Progress - Feature is partially implemented  
> 📝 Planned - Feature is planned but not yet implemented