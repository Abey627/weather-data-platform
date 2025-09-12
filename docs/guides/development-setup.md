# Development Setup Guide

This document provides detailed instructions for setting up the Weather Data Platform development environment.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (version 20.10 or later)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or later)
- [Python](https://www.python.org/downloads/) (version 3.8 or later, only needed for initial setup)
- Git
- A code editor (VS Code recommended)

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Abey627/weather-data-platform.git
cd weather-data-platform
```

### 2. Set Up Environment Variables

```bash
# Copy example .env file
cp .env.example .env

# Generate a secure Django secret key
python scripts/generate_secret_key.py
```

Update the generated secret key in your `.env` file, and review other environment variables.

Example `.env` file:

```ini
# Database settings
DB_NAME=weather_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db

# Redis settings
REDIS_HOST=redis
REDIS_PORT=6379

# Django settings
DEBUG=True
SECRET_KEY=your_generated_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1

# API keys
WEATHER_API_KEY=your_api_key_here
```

### 3. Start the Development Environment

```bash
# Start all services
docker-compose up -d
```

This will start the following services:
- Django backend (http://localhost:8000)
- PostgreSQL database
- Redis cache
- PgAdmin (http://localhost:5050)

### 4. Verify Setup

Open your browser and navigate to:
- Backend API: http://localhost:8000/
- API Documentation: http://localhost:8000/swagger/

## Development Workflow

### Backend Development

#### Running the Backend Server

```bash
# Start only the backend and its dependencies
docker-compose up -d backend
```

#### Making Code Changes

1. Edit files in the `backend/` directory
2. The Django development server will automatically reload
3. View logs to check for errors:
   ```bash
   docker-compose logs -f backend
   ```

#### Database Migrations

After changing models, create and apply migrations:

```bash
# Create migrations
docker-compose exec backend python manage.py makemigrations

# Apply migrations
docker-compose exec backend python manage.py migrate
```

#### Running Tests

```bash
# Run all backend tests
docker-compose exec backend pytest

# Run with coverage report
docker-compose exec backend pytest --cov=weather

# Run specific tests
docker-compose exec backend pytest weather/tests/test_views.py
```

#### Django Shell

```bash
# Open Django shell
docker-compose exec backend python manage.py shell
```

### Frontend Development (🚧 Planned)

Once frontend development begins:

```bash
# Start only the frontend
docker-compose up -d frontend
```

The React development server will be accessible at http://localhost:3000.

For a complete list of available commands, see the [Commands Reference](../reference/commands.md).

## Working with the Database

### PgAdmin Access

A PgAdmin instance is included for database management:

1. Access PgAdmin at http://localhost:5050
2. Log in with credentials from your `.env` file
3. Connect to the database server using:
   - Host: `db` (the internal Docker network name)
   - Port: `5432`
   - Username: From your `.env` file (`DB_USER`)
   - Password: From your `.env` file (`DB_PASSWORD`)

### Database Reset

If you need to reset the database:

```bash
# Stop the services
docker-compose down

# Remove the volume
docker volume rm weather-data-platform_postgres_data

# Start services again
docker-compose up -d

# Apply migrations
docker-compose exec backend python manage.py migrate
```

## API Keys

The Weather Data Platform uses external APIs that require API keys:

1. Weather API: Sign up at [WeatherAPI.com](https://www.weatherapi.com/)
2. Add your API key to the `.env` file:
   ```
   WEATHER_API_KEY=your_api_key_here
   ```

## Troubleshooting

### Common Issues

1. **Port conflicts**: If services fail to start due to port conflicts, change the port mappings in `docker-compose.yml`

2. **Database connection issues**: Ensure the database service is running:
   ```bash
   docker-compose ps db
   ```

3. **Docker volume permission issues**: Some file permission errors can be fixed with:
   ```bash
   sudo chown -R $USER:$USER .
   ```

4. **Hot reloading not working**: Ensure you're using the development Dockerfiles and volumes are correctly mounted.

5. **Missing environment variables**: Double-check your `.env` file and compare it against `.env.example` to ensure all required variables are set.

### Debugging Django

For more verbose logging, set `DEBUG=True` in your `.env` file.

For more advanced debugging:

1. Install a Python debugger in your container:
   ```bash
   docker-compose exec backend pip install ipdb
   ```

2. Add breakpoints in your code:
   ```python
   import ipdb; ipdb.set_trace()
   ```

## Version Control Guidelines

- Use feature branches for new development
- Follow conventional commit messages
- Run tests locally before pushing changes
- Do not commit the `.env` file or any sensitive information

For more detailed information on project components, see:
- [Backend Documentation](../components/backend/overview.md)
- [Frontend Documentation](../components/frontend/overview.md) (🚧 Planned)
- [Testing Guide](./testing.md)

> **Legend:**  
> ✅ Implemented - Feature is complete and working  
> 🚧 In Progress - Feature is partially implemented  
> 📝 Planned - Feature is planned but not yet implemented