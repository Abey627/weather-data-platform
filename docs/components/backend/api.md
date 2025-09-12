# Backend API Reference

This document provides detailed information about the API endpoints available in the Weather Data Platform backend.

## Authentication

Authentication is not currently implemented. All endpoints are publicly accessible.

## API Endpoints

### Weather Data Endpoints

#### GET `/api/weather/{city}/`

Retrieve weather data for a specific city.

**Parameters:**

- `city` (path parameter, required): The name of the city to fetch weather data for

**Query Parameters:**

- `days` (optional): Number of days to get historical data for. Default is 5.

**Response:**

```json
{
  "city": "New York",
  "country": "United States",
  "coordinates": {
    "latitude": 40.7128,
    "longitude": -74.006
  },
  "weather_data": [
    {
      "date": "2023-05-10",
      "temperature": {
        "min": 15.2,
        "max": 22.8,
        "avg": 18.5
      },
      "humidity": 65,
      "wind_speed": 10.2,
      "conditions": "Partly cloudy"
    },
    // Additional days...
  ],
  "aggregated": {
    "avg_temperature": 19.2,
    "min_temperature": 12.1,
    "max_temperature": 25.3
  }
}
```

#### GET `/api/weather/{city}/average/`

Calculate the average temperature for a specific city over a specified number of days.

**Parameters:**

- `city` (path parameter, required): The name of the city to fetch weather data for

**Query Parameters:**

- `days` (optional): Number of days to calculate the average for. Default is 5.

**Response:**

```json
{
  "city": "New York",
  "country": "United States",
  "period": "5 days",
  "avg_temperature": 19.2,
  "min_temperature": 12.1,
  "max_temperature": 25.3
}
```

### Location Endpoints

#### GET `/api/locations/search/`

Search for cities that match a given query string.

**Query Parameters:**

- `q` (required): The query string to search for cities

**Response:**

```json
[
  {
    "name": "New York",
    "country": "United States",
    "coordinates": {
      "latitude": 40.7128,
      "longitude": -74.006
    }
  },
  // Additional cities...
]
```

## Error Responses

The API uses standard HTTP status codes to indicate the success or failure of requests:

- `200 OK`: The request was successful
- `400 Bad Request`: The request was invalid or cannot be served
- `404 Not Found`: The requested resource could not be found
- `500 Internal Server Error`: An error occurred on the server

Error responses have the following format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "A descriptive error message"
  }
}
```

## Rate Limiting

There are currently no rate limits on the API endpoints. However, rate limits are enforced by the third-party weather APIs that this platform relies on.

## Example Usage

### Curl Example

```bash
# Get weather data for New York
curl -X GET "http://localhost:8000/api/weather/New%20York/?days=3"

# Get average temperature for San Francisco
curl -X GET "http://localhost:8000/api/weather/San%20Francisco/average/?days=7"
```

### Python Example

```python
import requests

# Get weather data for London
response = requests.get("http://localhost:8000/api/weather/London/?days=5")
weather_data = response.json()
print(f"Average temperature in London: {weather_data['aggregated']['avg_temperature']}°C")
```

## Related Documentation

- [Backend Overview](./overview.md) - General information about the backend
- [API Reference (Swagger UI)](http://localhost:8000/swagger/) - Interactive API documentation (requires backend to be running)