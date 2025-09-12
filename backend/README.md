# Weather Data Platform - Backend API

This directory contains the Django REST Framework backend for the Weather Data Platform.

## Features

- RESTful API for fetching and processing weather data
- Endpoint for calculating average temperature for a city over X days
- PostgreSQL database integration
- Redis caching
- Swagger/OpenAPI documentation

## API Endpoints

- `GET /api/weather/average?city={city}&days={X}`: Get the average temperature for a city over the past X days.

## Docker-Only Development

This project is designed for Docker-only development to ensure consistency and simplify setup.

### Running the Backend with Docker

From the project root:

```bash
# Start the backend service along with PostgreSQL and Redis
docker-compose up -d backend db redis
```

### Development Commands

Use the following Docker commands to manage the backend:

```bash
# Run Django migrations
docker-compose exec backend python manage.py migrate

# View backend logs
docker-compose logs -f backend

# Run backend tests
docker-compose exec backend pytest

# Open a Django shell
docker-compose exec backend python manage.py shell

# Open a bash shell in the backend container
docker-compose exec backend bash
```

For a complete list of available commands, please refer to the [Command Reference](../docs/reference/commands.md) in the project root.

## API Documentation

API documentation is available at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

When the server is running, access these URLs to view and interact with the API documentation.
