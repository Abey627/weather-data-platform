# Deployment Guide

This document provides instructions for deploying the Weather Data Platform to production environments.

> **Note:** Some production features are still in development (🚧).

## Prerequisites

- Docker and Docker Compose installed on the production server
- Access to a PostgreSQL database (can be containerized)
- Access to a Redis instance (can be containerized)
- Domain name configured for the application (optional)
- SSL certificate for production deployments (recommended)

## Deployment Steps

### 1. Prepare the Environment

Clone the repository on your production server:

```bash
git clone https://github.com/Abey627/weather-data-platform.git
cd weather-data-platform
```

### 2. Configure Production Environment

Create a production environment file:

```bash
cp .env.example .env.prod
```

Edit the `.env.prod` file with secure production values:

```bash
# Database settings
DB_NAME=weather_prod
DB_USER=db_user_prod
DB_PASSWORD=secure_password_here
DB_HOST=db

# Redis settings
REDIS_HOST=redis
REDIS_PORT=6379

# Django settings
DEBUG=False
SECRET_KEY=your_secure_secret_key_here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# API keys
WEATHER_API_KEY=your_api_key_here
```

### 3. Generate a Secure Secret Key

Use the provided script to generate a secure Django secret key:

```bash
python scripts/generate_secret_key.py
```

Add the generated key to your `.env.prod` file.

### 4. Deploy with Docker Compose

Deploy the application using the production Docker Compose file:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

This will start all necessary services defined in the production configuration.

### 5. Run Database Migrations

Apply database migrations:

```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

### 6. Create Superuser (Optional)

If you need admin access, create a superuser:

```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

### 7. Collect Static Files

Collect static files for the Django admin interface and API documentation:

```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --no-input
```

### 8. Verify Deployment

Check that all services are running:

```bash
docker-compose -f docker-compose.prod.yml ps
```

Test the API endpoints:

- Backend API: https://your-domain.com/
- API Documentation: https://your-domain.com/swagger/
- Admin Interface: https://your-domain.com/admin/

## Production Configuration Options

The `docker-compose.prod.yml` file includes several production-specific settings:

- Nginx as a reverse proxy with SSL termination
- Gunicorn as the WSGI server for Django
- Production-ready PostgreSQL settings
- Redis for caching and session storage

## Scaling Considerations

### Horizontal Scaling

For higher traffic loads:

1. Use a load balancer in front of multiple backend instances
2. Configure session sharing via Redis
3. Ensure database connection pooling is properly configured

### Vertical Scaling

Adjust container resource limits in the Docker Compose file:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
```

## Monitoring and Maintenance

### Logs

View container logs:

```bash
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Backup and Restore (🚧 In Progress)

Database backup (planned feature):

```bash
# Will be implemented in future version
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres weather_prod > backup.sql
```

### Updates and Rollbacks

To update to a new version:

```bash
git pull
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

To rollback to a previous version:

```bash
git checkout <previous_commit_or_tag>
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

## Security Best Practices

1. Always use HTTPS in production
2. Keep your `.env.prod` file secure and never commit it to version control
3. Regularly update dependencies to patch security vulnerabilities
4. Set appropriate file permissions for sensitive configuration files
5. Use non-root users in containers
6. Implement rate limiting for API endpoints

## Troubleshooting

### Common Issues

1. **Database connection errors**: Check database credentials and ensure the database container is running
2. **Redis connection errors**: Verify Redis container is running and accessible
3. **Static files not loading**: Make sure collectstatic has been run
4. **Permission issues**: Check file permissions for volume mounts

### Diagnostic Commands

Check container logs:
```bash
docker-compose -f docker-compose.prod.yml logs -f backend
```

Check container status:
```bash
docker-compose -f docker-compose.prod.yml ps
```

Access container shell:
```bash
docker-compose -f docker-compose.prod.yml exec backend bash
```

## Future Deployment Enhancements (📝 Planned)

1. Database backup and restore functionality
2. Integration with CI/CD pipelines for automated deployment
3. Blue-green deployment strategy
4. Container orchestration with Kubernetes

For more detailed commands, refer to the [Commands Reference](../reference/commands.md).

> **Legend:**  
> ✅ Implemented - Feature is complete and working  
> 🚧 In Progress - Feature is partially implemented  
> 📝 Planned - Feature is planned but not yet implemented