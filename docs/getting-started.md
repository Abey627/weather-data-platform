# Getting Started with Weather Data Platform

This guide will help you quickly set up and start using the Weather Data Platform for development.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (version 20.10 or later)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or later)
- [Python](https://www.python.org/downloads/) (version 3.8 or later, only needed for initial setup)

Most dependencies are containerized, so you don't need to install Node.js, PostgreSQL, or Redis locally.

## Quick Setup

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

After generating the secret key, update it in your `.env` file. **Make sure to update all passwords and sensitive information in the `.env` file before proceeding.**

### 3. Start the Development Environment

#### Using Docker Compose

```bash
# Start all services
docker-compose up -d
```

This will start all necessary services defined in docker-compose.yml.

### 4. Access the Services

Once the containers are up and running, you can access:

- Backend API: http://localhost:8000/
- API Documentation: http://localhost:8000/swagger/
- Database Admin: http://localhost:5050/ (Login with credentials from your `.env` file)
- Frontend (when implemented): http://localhost:3000/

## Verifying Your Setup

To verify that everything is working correctly:

1. Check if containers are running:
   ```bash
   docker-compose ps
   ```

2. Test the backend API:
   - Visit http://localhost:8000/swagger/ to see the API documentation
   - Try the `/api/weather/average` endpoint with a city name and days parameter

3. Check the logs for any errors:
   ```bash
   docker-compose logs
   ```

## Next Steps

- [Command Reference](./reference/commands.md) - Learn all available commands
- [Backend Documentation](./components/backend/overview.md) - Explore the backend API
- [Development Setup](./guides/development-setup.md) - More detailed development instructions
- [Project Status](./project/status.md) - View the current project status and roadmap

## Troubleshooting

### Common Issues

1. **Port conflicts**: If you see errors about ports being in use, you may have other services running on the same ports. Edit the `.env` file to change the port mappings.

2. **Database connection errors**: Ensure the database container is running and the database credentials in `.env` are correct.

3. **Permission issues**: If you encounter permission problems with Docker volumes, try running the Docker commands with elevated privileges or fix the permissions on your host system.

For more detailed help, check the [full documentation](./index.md) or submit an issue on GitHub.