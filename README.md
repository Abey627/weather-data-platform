# Weather Data Platform

A comprehensive weather data aggregation system built with React and Django REST Framework, featuring historical weather data analysis and visualization.

> **Current Project Status:** 55% Complete - [View Detailed Status](./docs/project/status.md)

## Project Overview

This project consists of a weather data aggregation API and frontend application that work together to:

1. Fetch historical weather data from third-party APIs ✅
2. Process and analyze temperature data ✅
3. Display meaningful weather insights to users 🚧

## Key Features

### Backend (Django REST Framework) ✅
- RESTful API to fetch and process weather data from external sources ✅
- Endpoint to calculate average temperature for any city over a specified number of days ✅
- API documentation with Swagger/OpenAPI ✅
- PostgreSQL for persistent data storage ✅
- Redis for efficient request caching ✅

### Frontend (React) 📝
- User-friendly interface for city and time period selection 📝
- Display of average temperature results 📝
- Graceful handling of loading states and error messages 📝

### Infrastructure
- Docker setup for both backend and frontend ✅
- Docker Compose for service orchestration ✅
- Comprehensive testing suite ✅
- ELK Stack for centralized logging and monitoring 📝

> **Legend:**  
> ✅ Implemented - Feature is complete and working  
> 🚧 In Progress - Feature is partially implemented  
> 📝 Planned - Feature is planned but not yet implemented

## Repository Structure
- `/backend` - Django REST Framework API
- `/frontend` - React frontend application
- `/docs` - Project documentation
  - Check out the [Documentation Index](./docs/index.md) for comprehensive guides and information

## Docker-Only Development

This project is designed for Docker-only development to ensure consistency and simplify setup. All development, testing, and deployment are done using Docker containers.

### Prerequisites

- Docker
- Docker Compose
- Python (only needed to generate the initial Django secret key)

Most dependencies are containerized, so no local installation of Node.js, PostgreSQL, or Redis is required.

### Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/Abey627/weather-data-platform.git
   cd weather-data-platform
   ```

2. Set up environment variables:
   ```bash
   # Copy example .env file
   cp .env.example .env
   
   # Generate a secure Django secret key (requires Python)
   python scripts/generate_secret_key.py
   ```
   After generating the secret key, update it in your `.env` file. **Make sure to update all passwords and sensitive information in the `.env` file before proceeding.**

3. Start the development environment:
   ```bash
   # Start all services
   docker-compose up -d
   ```

4. Access the services:
   - Backend API: http://localhost:8000/
   - API Documentation: http://localhost:8000/swagger/
   - Database Admin: http://localhost:5050/ (Login with credentials from your `.env` file)
   - Frontend (when implemented): http://localhost:3000/

### Development Commands

Use the following Docker commands to manage the development environment:

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Run Django migrations
docker-compose exec backend python manage.py migrate

# View logs
docker-compose logs -f

# Run tests
docker-compose exec backend pytest

# Open a shell in the container
docker-compose exec backend bash
```

For a complete list of available commands, please refer to the [Command Reference](./docs/reference/commands.md).

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

For detailed information about available API endpoints and examples, please refer to the [Backend API Reference](./docs/components/backend/api.md).

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

## Documentation

The project documentation is organized in the `/docs` directory:

- [Documentation Index](./docs/index.md) - Complete documentation directory
- [Project Overview](./docs/project/overview.md) - Comprehensive overview of the project
- [Architecture Documentation](./docs/architecture/overview.md) - System architecture details
- [Backend Guide](./docs/components/backend/overview.md) - Backend API details and development guide
- [Frontend Guide](./docs/components/frontend/overview.md) - Frontend application guide
- [Command Reference](./docs/reference/commands.md) - All Docker and development commands
- [Infrastructure Guide](./docs/components/infrastructure/overview.md) - Deployment and monitoring setup

For API documentation, visit the endpoints when the backend is running:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
