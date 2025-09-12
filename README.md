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

2. Set up environment variables:
   ```bash
   # On Linux/macOS
   ./scripts/setup_env.sh
   
   # On Windows PowerShell
   .\scripts\setup_env.ps1
   ```
   This will create a `.env` file from the `.env.example` template. **Make sure to update all passwords and sensitive information in the `.env` file before proceeding.**

3. Start the development environment:
   ```bash
   # On Linux/macOS
   ./dev.sh up
   
   # On Windows PowerShell
   .\dev.ps1 up
   ```

4. Access the services:
   - Backend API: http://localhost:8000/
   - API Documentation: http://localhost:8000/swagger/
   - Database Admin: http://localhost:5050/ (Login with credentials from your `.env` file)
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

## Environment Configuration

The project uses environment variables for all sensitive information. The setup is managed through:

- `.env` file for development (created from `.env.example` template)
- `.env.prod` file for production (must be created manually before deployment)

**Never commit environment files with actual credentials to the repository.**

Key environment variables include:
- Database credentials
- Django secret key
- API keys (if required)
- Debug settings

## API Documentation

API documentation is available at the following endpoints when the backend is running:

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Production Deployment

For production deployment:

1. Create a production environment file:
   ```bash
   cp .env.example .env.prod
   ```

2. Edit the `.env.prod` file with secure production values.

3. Deploy the application:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```
