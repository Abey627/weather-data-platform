# Backend API Reference

This document provides detailed information about the API endpoints available in the Weather Data Platform backend.

## Authentication

Authentication is not currently implemented. All endpoints are publicly accessible.

## API Endpoints

### Weather Data Endpoints

#### GET `/api/weather/average`

Calculate the average temperature for a specific city over a specified number of days.

**Query Parameters:**

- `city` (required): The name of the city to fetch weather data for (e.g., "London")
- `days` (required): Number of days to calculate the average for (e.g., 7)

**Response:**

```json
{
  "city": "London",
  "average_temperature": 20.75,
  "days": 7,
  "start_date": "2025-09-05",
  "end_date": "2025-09-12"
}
```

#### GET `/api/weather/history`

Retrieve historical weather data records from the database.

**Query Parameters:**

- `city` (optional): Filter results by city name
- `start_date` (optional): Filter results by start date (YYYY-MM-DD)
- `end_date` (optional): Filter results by end date (YYYY-MM-DD)

**Response:**

```json
[
  {
    "id": 1,
    "city": "London",
    "date": "2025-09-12",
    "temperature": 21.3,
    "humidity": 65,
    "weather_condition": "Partly cloudy"
  },
  // Additional weather records...
]
```

### Admin Interface

#### `/admin/`

Django Admin interface for managing application data.

- Requires admin credentials
- Provides access to all database models and configurations

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
# Get average temperature for London over 7 days
curl -X GET "http://localhost:8000/api/weather/average?city=London&days=7"

# Get historical weather data
curl -X GET "http://localhost:8000/api/weather/history"

# Get historical weather data for a specific city
curl -X GET "http://localhost:8000/api/weather/history?city=London"
```

### PowerShell Example

```powershell
# Get average temperature for London over 7 days
Invoke-WebRequest -Uri "http://localhost:8000/api/weather/average?city=London&days=7" -Method GET

# Get historical weather data
Invoke-WebRequest -Uri "http://localhost:8000/api/weather/history" -Method GET
```

### Python Example

```python
import requests

# Get average temperature for London over 7 days
response = requests.get("http://localhost:8000/api/weather/average?city=London&days=7")
weather_data = response.json()
print(f"Average temperature in London: {weather_data['average_temperature']}°C")

# Get historical weather data
response = requests.get("http://localhost:8000/api/weather/history")
history_data = response.json()
print(f"Number of historical records: {len(history_data)}")
```

## Related Documentation

- [Backend Overview](./overview.md) - General information about the backend
- [API Reference (Swagger UI)](http://localhost:8000/swagger/) - Interactive API documentation (requires backend to be running)