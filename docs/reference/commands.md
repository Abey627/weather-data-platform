# Command Reference Guide

This document serves as the single source of truth for all commands used in the Weather Data Platform project. Rather than duplicating command instructions across multiple documents, other documentation should link to this reference.

## Table of Contents

- [Environment Setup](#environment-setup)
- [Service Management](#service-management)
- [Database Operations](#database-operations)
- [Testing](#testing)
- [Development Tools](#development-tools)
- [Production Deployment](#production-deployment)

## Environment Setup

### Initialize Environment Variables

```bash
# Copy example .env file (if .env doesn't exist)
cp .env.example .env

# Generate a secure Django secret key
python scripts/generate_secret_key.py
```

> **Note:** After generating the secret key, update it in your `.env` file. Make sure to update all passwords and sensitive information before proceeding.

## Service Management

### Start Services

```bash
# Start all services
docker-compose up -d

# Start only backend, database, and redis
docker-compose up -d backend db redis

# Start only frontend
docker-compose up -d frontend

# Start only the database
docker-compose up -d db
```

### Stop Services

```bash
# Stop all services
docker-compose down
```

### View Logs

```bash
# View logs of all services
docker-compose logs -f

# View logs of the backend service
docker-compose logs -f backend

# View logs of the frontend service
docker-compose logs -f frontend
```

## Database Operations

### Database Migrations

```bash
# Create new Django migrations
docker-compose exec backend python manage.py makemigrations

# Check if migrations are needed
docker-compose exec backend python manage.py makemigrations --check
docker-compose exec backend python manage.py showmigrations

# Run Django migrations
docker-compose exec backend python manage.py migrate
```

### Check and Apply Migrations (for CI/CD)

```bash
# Check if migrations are needed
docker-compose exec backend chmod +x /app/scripts/check_apply_migrations.sh
docker-compose exec backend /app/scripts/check_apply_migrations.sh

# Check and apply migrations if needed
docker-compose exec backend chmod +x /app/scripts/check_apply_migrations.sh
docker-compose exec backend /app/scripts/check_apply_migrations.sh --apply
```

## Testing

### Backend Testing

```bash
# Run all backend tests
docker-compose exec backend pytest

# Run backend tests with coverage report
docker-compose exec backend pytest --cov=weather

# Run specific test file
docker-compose exec backend pytest weather/tests/test_views.py

# Run specific test class or method
docker-compose exec backend pytest weather/tests/test_views.py::TestWeatherAverageView

# Run contract tests for external API integrations
docker-compose exec backend pytest -v -m contract
```

### Frontend Testing

```bash
# Run frontend tests
docker-compose exec frontend npm test
```

## Development Tools

### Django Management

```bash
# Open a Django shell
docker-compose exec backend python manage.py shell
```

### Shell Access

```bash
# Open a bash shell in the backend container
docker-compose exec backend bash

# Open a bash shell in the frontend container
docker-compose exec frontend sh
```

## Production Deployment

### Preparation

```bash
# Create a production environment file
cp .env.example .env.prod

# Edit the .env.prod file with secure production values
```

### Deployment

```bash
# Deploy the application
docker-compose -f docker-compose.prod.yml up -d
```

> **Note:** Make sure to update all passwords and sensitive information in the `.env.prod` file before deployment.