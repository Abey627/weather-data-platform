# API Reference

This document provides a detailed reference for the Weather Data Platform REST API endpoints.

> **Status: ✅ Implemented** - The core API endpoints are fully functional and documented.

## API Base URL

- Development: `http://localhost:8000/api/`
- Production: `https://your-domain.com/api/`

## Authentication

Currently, the API is open and does not require authentication. Authentication will be added in a future update.

## Endpoints

### Weather Data

#### Get Average Temperature

Returns the average temperature for a specified city over a specified number of days.

- **URL**: `/weather/average`
- **Method**: `GET`
- **Status**: ✅ Implemented

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| city | string | Yes | The name of the city to get weather data for |
| days | integer | Yes | The number of past days to include in the average |

**Response**:

```json
{
  "city": "London",
  "average_temperature": 15.7,
  "period_days": 7,
  "start_date": "2025-09-05",
  "end_date": "2025-09-12",
  "units": "celsius"
}
```

**Error Responses**:

- `400 Bad Request`: Missing or invalid parameters
  ```json
  {
    "error": "Missing required parameter: city"
  }
  ```

- `404 Not Found`: City not found
  ```json
  {
    "error": "City not found: NonexistentCity"
  }
  ```

- `429 Too Many Requests`: Rate limit exceeded
  ```json
  {
    "error": "Rate limit exceeded. Please try again later."
  }
  ```

- `500 Internal Server Error`: Server error
  ```json
  {
    "error": "An unexpected error occurred"
  }
  ```

**Example Request**:

```bash
curl "http://localhost:8000/api/weather/average?city=London&days=7"
```

#### Get Historical Weather Data

Returns historical weather data for a specified city over a date range.

- **URL**: `/weather/history`
- **Method**: `GET`
- **Status**: ✅ Implemented

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| city | string | Yes | The name of the city to get weather data for |
| start_date | date (YYYY-MM-DD) | Yes | The start date for the historical data |
| end_date | date (YYYY-MM-DD) | Yes | The end date for the historical data |

**Response**:

```json
{
  "city": "London",
  "start_date": "2025-09-05",
  "end_date": "2025-09-12",
  "units": "celsius",
  "data": [
    {
      "date": "2025-09-05",
      "temperature": 14.5,
      "precipitation": 2.3,
      "humidity": 65
    },
    {
      "date": "2025-09-06",
      "temperature": 15.2,
      "precipitation": 0.0,
      "humidity": 60
    },
    // Additional days...
  ]
}
```

**Error Responses**: Same as for the average temperature endpoint.

**Example Request**:

```bash
curl "http://localhost:8000/api/weather/history?city=London&start_date=2025-09-05&end_date=2025-09-12"
```

### System Information

#### Health Check

Returns the current status of the API.

- **URL**: `/health`
- **Method**: `GET`
- **Status**: ✅ Implemented

**Response**:

```json
{
  "status": "ok",
  "version": "1.0.0",
  "database": "connected",
  "cache": "connected",
  "timestamp": "2025-09-12T14:30:45Z"
}
```

**Example Request**:

```bash
curl "http://localhost:8000/api/health"
```

## Request Rate Limiting

The API implements rate limiting to prevent abuse:

- 60 requests per minute per IP address for regular endpoints
- 10 requests per minute per IP address for expensive operations (like historical data)

When a rate limit is exceeded, the API returns a `429 Too Many Requests` response with a `Retry-After` header indicating the number of seconds to wait before retrying.

## Response Format

All API responses are in JSON format and include:

- For successful responses: The requested data
- For error responses: An `error` field with a description of the error

## Planned Endpoints

The following endpoints are planned for future releases:

### User Management (📝 Planned)

- **URL**: `/user/profile`
- **Methods**: `GET`, `POST`
- **Description**: User profile management

### Data Export (📝 Planned)

- **URL**: `/weather/export`
- **Method**: `GET`
- **Description**: Export weather data in various formats (CSV, JSON)

### Weather Trends (📝 Planned)

- **URL**: `/weather/trends`
- **Method**: `GET`
- **Description**: Get trend analysis for weather data over time

## Testing the API

You can test the API using the Swagger UI, which is available at:

- Development: `http://localhost:8000/swagger/`
- Production: `https://your-domain.com/swagger/`

Alternatively, you can use tools like curl, Postman, or any HTTP client to make requests to the API endpoints.

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests:

- `200 OK`: Request succeeded
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Requested resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server-side error

## Versioning

The API is currently at version 1.0. Future versions will be available at `/api/v2/`, etc., while maintaining backward compatibility.

> **Legend:**  
> ✅ Implemented - Feature is complete and working  
> 🚧 In Progress - Feature is partially implemented  
> 📝 Planned - Feature is planned but not yet implemented