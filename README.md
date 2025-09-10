# Weather Data Platform

A comprehensive weather data aggregation system built with React and Django REST Framework, featuring historical weather data analysis and visualization.

## Project Overview

This project consists of a weather data aggregation API and frontend application that work together to:

1. Fetch historical weather data from third-party APIs
2. Process and analyze temperature data
3. Display meaningful weather insights to users

## Key Features

### Backend (Django REST Framework)
- RESTful API to fetch and process weather data from external sources
- Endpoint to calculate average temperature for any city over a specified number of days
- API documentation with Swagger/OpenAPI
- PostgreSQL for persistent data storage
- Redis for efficient request caching

### Frontend (React)
- User-friendly interface for city and time period selection
- Display of average temperature results
- Graceful handling of loading states and error messages

### Infrastructure
- Docker setup for both backend and frontend
- Docker Compose for service orchestration
- Comprehensive testing suite

## Repository Structure
- `/backend` - Django REST Framework API
- `/frontend` - React frontend application

## Docker-Only Development

This project is designed for Docker-only development to ensure consistency and simplify setup. All development, testing, and deployment are done using Docker containers.

### Prerequisites

- Docker
- Docker Compose

No local installation of Python, Node.js, PostgreSQL, or Redis is required!

### Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/Abey627/weather-data-platform.git
   cd weather-data-platform
   ```

2. Start the development environment:
   ```bash
   # On Linux/macOS
   ./dev.sh up
   
   # On Windows PowerShell
   .\dev.ps1 up
   ```

3. Access the services:
   - Backend API: http://localhost:8000/
   - API Documentation: http://localhost:8000/swagger/
   - Database Admin: http://localhost:5050/ (Email: admin@example.com, Password: admin)
   - Frontend (when implemented): http://localhost:3000/

### Development Commands

Use our convenient scripts to manage the development environment:

```bash
# Start all services
./dev.sh up      # Linux/macOS
.\dev.ps1 up     # Windows

# Stop all services
./dev.sh down    # Linux/macOS
.\dev.ps1 down   # Windows

# Run Django migrations
./dev.sh migrate # Linux/macOS
.\dev.ps1 migrate # Windows

# View logs
./dev.sh logs    # Linux/macOS
.\dev.ps1 logs   # Windows

# Run tests
./dev.sh test-backend  # Linux/macOS
.\dev.ps1 test-backend # Windows

# Open a shell in the container
./dev.sh bash-backend  # Linux/macOS
.\dev.ps1 bash-backend # Windows
```

## API Documentation

API documentation is available at the following endpoints when the backend is running:

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Production Deployment

For production deployment:

```bash
docker-compose -f docker-compose.prod.yml up -d
```
