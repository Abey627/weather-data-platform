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

## Getting Started

### Prerequisites

- Python 3.10+ (for backend)
- Node.js 16+ (for frontend)
- PostgreSQL 14+
- Redis 7+
- Docker and Docker Compose (for containerized setup)

### Backend Setup

The backend is a Django REST Framework application that provides the weather data API.

```bash
# Navigate to the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

For more details, see the [backend README](./backend/README.md).

### Frontend Setup

The frontend is a React application (to be implemented).

### Docker Setup

For a complete containerized setup with PostgreSQL and Redis:

```bash
# Build and start all services
docker-compose up -d

# To stop all services
docker-compose down
```

## API Documentation

API documentation is available at the following endpoints when the backend is running:

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
