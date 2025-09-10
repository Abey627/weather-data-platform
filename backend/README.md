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

## Setup Instructions

### Local Development

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. Set up the PostgreSQL database:
   - Create a database named `weather_db`
   - Update settings in `weatherapi/settings.py` if needed

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

### Using Docker

1. Make sure Docker and Docker Compose are installed
2. From the project root, run:
   ```
   docker-compose up -d backend
   ```

## API Documentation

API documentation is available at:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

When the server is running, access these URLs to view and interact with the API documentation.
