# Docker Commands Reference

This document provides a list of `docker-compose` commands to replace the functionality previously available in PowerShell scripts.

## Environment Setup

```bash
# Copy example .env file (if .env doesn't exist)
cp .env.example .env

# Generate a secure Django secret key (you'll need to update the .env file manually)
python scripts/generate_secret_key.py
```

## Start Services

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

## Stop Services

```bash
# Stop all services
docker-compose down
```

## View Logs

```bash
# View logs of all services
docker-compose logs -f

# View logs of the backend service
docker-compose logs -f backend

# View logs of the frontend service
docker-compose logs -f frontend
```

## Database Migrations

```bash
# Create new Django migrations
docker-compose exec backend python manage.py makemigrations

# Check if migrations are needed
docker-compose exec backend python manage.py makemigrations --check
docker-compose exec backend python manage.py showmigrations

# Run Django migrations
docker-compose exec backend python manage.py migrate
```

## Testing

```bash
# Run backend tests
docker-compose exec backend pytest

# Run backend tests with coverage report
docker-compose exec backend pytest --cov=weather

# Run frontend tests
docker-compose exec frontend npm test

# Run contract tests for external API integrations
# Make sure the backend container is running
docker-compose up -d backend
# Install jsonschema package if needed
docker-compose exec backend pip install jsonschema
# Run the contract tests
docker-compose exec backend pytest -v -m contract
```

## Development Tools

```bash
# Open a Django shell
docker-compose exec backend python manage.py shell

# Open a bash shell in the backend container
docker-compose exec backend bash

# Open a bash shell in the frontend container
docker-compose exec frontend sh
```

## Check and Apply Migrations (for CI/CD)

```bash
# Check if migrations are needed
docker-compose exec backend chmod +x /app/scripts/check_apply_migrations.sh
docker-compose exec backend /app/scripts/check_apply_migrations.sh

# Check and apply migrations if needed
docker-compose exec backend chmod +x /app/scripts/check_apply_migrations.sh
docker-compose exec backend /app/scripts/check_apply_migrations.sh --apply
```