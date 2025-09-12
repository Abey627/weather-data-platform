````markdown
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
# On Linux/macOS
./dev.sh backend

# On Windows PowerShell
.\dev.ps1 backend
```

This starts the backend service along with PostgreSQL and Redis.

### Development Commands

Use our convenient scripts to manage the development environment:

```bash
# Run Django migrations
./dev.sh migrate     # Linux/macOS
.\dev.ps1 migrate    # Windows

# View backend logs
./dev.sh logs-backend    # Linux/macOS
.\dev.ps1 logs-backend   # Windows

# Run backend tests
./dev.sh test-backend    # Linux/macOS
.\dev.ps1 test-backend   # Windows

# Open a Django shell
./dev.sh shell           # Linux/macOS
.\dev.ps1 shell          # Windows

# Open a bash shell in the backend container
./dev.sh bash-backend    # Linux/macOS
.\dev.ps1 bash-backend   # Windows
```

## API Documentation

API documentation is available at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

When the server is running, access these URLs to view and interact with the API documentation.

````