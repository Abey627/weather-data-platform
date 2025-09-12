````markdown
# ELK Stack Implementation Plan for Weather Data Platform

This document outlines the detailed implementation plan for integrating the ELK Stack (Elasticsearch, Logstash, Kibana) with the Weather Data Platform for comprehensive logging, monitoring, and observability.

## 1. Architecture Overview

```
┌────────────────┐    ┌────────────────┐    ┌────────────────┐
│                │    │                │    │                │
│  Django API    │───►│    Logstash    │───►│ Elasticsearch  │
│                │    │                │    │                │
└────────────────┘    └────────────────┘    └────────────────┘
                                                    │
                                                    ▼
                                            ┌────────────────┐
                                            │                │
                                            │     Kibana     │
                                            │                │
                                            └────────────────┘
```

## 2. Docker Configuration

### 2.1 Update Docker Compose

Add the following services to `docker-compose.yml`:

```yaml
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - xpack.security.enabled=false  # For development; enable for production
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    networks:
      - weather-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9200"]
      interval: 30s
      timeout: 10s
      retries: 5

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    volumes:
      - ./elk/logstash/pipeline:/usr/share/logstash/pipeline
      - ./elk/logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml
    ports:
      - "5044:5044"
      - "9600:9600"  # For monitoring Logstash API
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - weather-network

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - weather-network

volumes:
  elasticsearch-data:
```

### 2.2 Create Required Directory Structure

```
elk/
├── logstash/
│   ├── pipeline/
│   │   └── logstash.conf
│   └── config/
│       └── logstash.yml
└── kibana/
    └── kibana.yml
```

## 3. Logstash Configuration

### 3.1 Basic Configuration (logstash.yml)

```yaml
# elk/logstash/config/logstash.yml
http.host: "0.0.0.0"
xpack.monitoring.elasticsearch.hosts: ["http://elasticsearch:9200"]
```

### 3.2 Pipeline Configuration (logstash.conf)

```conf
# elk/logstash/pipeline/logstash.conf
input {
  tcp {
    port => 5044
    codec => json
  }
}

filter {
  # Add event type based on tags
  if [tags] {
    if "django" in [tags] {
      mutate {
        add_field => { "[@metadata][type]" => "django" }
      }
    }
    if "weather-api" in [tags] {
      mutate {
        add_field => { "[@metadata][type]" => "weather-api" }
      }
    }
  }
  
  # Extract city information from weather API logs
  if [message] =~ "city" {
    grok {
      match => { "message" => ".*city[:|=]\s*['|\"]?%{WORD:city}['|\"]?.*" }
    }
  }
  
  # Parse timestamps
  date {
    match => [ "asctime", "yyyy-MM-dd HH:mm:ss,SSS" ]
    target => "@timestamp"
  }
  
  # Categorize log messages
  if [message] =~ "error" or [levelname] == "ERROR" {
    mutate {
      add_field => { "log_category" => "error" }
    }
  } else if [message] =~ "warning" or [levelname] == "WARNING" {
    mutate {
      add_field => { "log_category" => "warning" }
    }
  } else {
    mutate {
      add_field => { "log_category" => "info" }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "weather-api-%{+YYYY.MM.dd}"
  }
  # Optional: Output to console for debugging
  # stdout { codec => rubydebug }
}
```

## 4. Django Integration

### 4.1 Add Required Packages

Update `requirements.txt` to include:

```
python-logstash==0.4.8
python-json-logger==2.0.7
```

### 4.2 Update Django Settings

Add the following to `settings.py`:

```python
# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d %(funcName)s %(process)d %(thread)d %(threadName)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'logstash': {
            'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': os.environ.get('LOGSTASH_HOST', 'logstash'),
            'port': int(os.environ.get('LOGSTASH_PORT', 5044)),
            'version': 1,
            'message_type': 'weather-api',
            'fqdn': False,
            'tags': ['django', 'weather-api'],
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logstash'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'weather': {
            'handlers': ['console', 'logstash'],
            'level': os.environ.get('WEATHER_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
```

### 4.3 Enhance Logging Context

Create a middleware to add request context to logs:

```python
# Create file at weather/middleware/logging.py

import uuid
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware to add request ID and other context to all logs"""
    
    def process_request(self, request):
        request.id = str(uuid.uuid4())
        
    def process_response(self, request, response):
        if hasattr(request, 'id'):
            response['X-Request-ID'] = request.id
            
            # Log completed request
            log_data = {
                'request_id': request.id,
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'user': request.user.username if request.user.is_authenticated else 'anonymous',
                'ip': self.get_client_ip(request),
            }
            
            if response.status_code >= 400:
                logger.warning(f"Request failed: {log_data}", extra=log_data)
            else:
                logger.info(f"Request completed: {log_data}", extra=log_data)
                
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

Add the middleware to your settings:

```python
MIDDLEWARE = [
    # ... existing middleware
    'weather.middleware.logging.RequestLoggingMiddleware',
]
```

## 5. Kibana Dashboard Setup

Once the ELK Stack is running, set up the following dashboards in Kibana:

### 5.1 API Performance Dashboard
- Request rate over time
- Average response time by endpoint
- Status code distribution
- Slowest API calls

### 5.2 Error Monitoring Dashboard
- Error rate over time
- Top error messages
- Errors by city/location
- User impact (number of affected users)

### 5.3 Weather Query Analysis
- Most queried cities
- Query patterns over time
- Average temperature trends
- Query distribution by day of week/time of day

### 5.4 System Health Dashboard
- Cache hit/miss ratio
- External API response times
- Database query performance
- System resource usage

## 6. Alerting Setup

Configure alerts in Kibana for:

1. High error rates (e.g., >5% of requests resulting in errors)
2. Slow response times (e.g., average response time >1s)
3. External API failures (e.g., repeated failures to connect to weather API)
4. Unusual query patterns (e.g., sudden spike in requests)

## 7. Production Considerations

For production deployments:

1. **Security**: Enable X-Pack security with proper authentication
2. **Resource Allocation**: Increase Elasticsearch resources based on log volume
3. **Data Retention**: Configure index lifecycle management (ILM) policies
4. **Backup**: Set up regular snapshots of Elasticsearch indices
5. **Network Security**: Properly secure the ELK Stack with appropriate firewalls and access controls

## 8. Documentation

Create the following documentation:

1. ELK Stack setup and configuration guide
2. Dashboard usage guide with screenshots
3. Alert response procedures
4. Troubleshooting guide
5. Log query examples for common scenarios

````