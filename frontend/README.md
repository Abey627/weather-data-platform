# Weather Data Platform - Frontend

This directory will contain the React frontend application for the Weather Data Platform.

## Planned Features

- User interface for entering city name and number of days
- Display of average temperature data
- Loading states and error handling
- Responsive design for various devices

## Technology Stack

- React
- Axios for API communication
- Bootstrap or Material UI for styling
- Jest and React Testing Library for tests

## Docker-Only Development

This project is designed for Docker-only development to ensure consistency and simplify setup.

### Running the Frontend with Docker

From the project root:

```bash
# Start the frontend service with hot reloading enabled
docker-compose up -d frontend
```

### Development Commands

Use the following Docker commands to manage the frontend:

```bash
# View frontend logs
docker-compose logs -f frontend

# Run frontend tests
docker-compose exec frontend npm test

# Open a shell in the frontend container
docker-compose exec frontend sh
```

For a complete list of available commands, please refer to the [Docker Commands Reference](../docs/docker-commands.md) in the project root.
