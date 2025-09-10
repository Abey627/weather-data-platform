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
# On Linux/macOS
./dev.sh frontend

# On Windows PowerShell
.\dev.ps1 frontend
```

This starts the frontend service with hot reloading enabled.

### Development Commands

Use our convenient scripts to manage the development environment:

```bash
# View frontend logs
./dev.sh logs-frontend    # Linux/macOS
.\dev.ps1 logs-frontend   # Windows

# Run frontend tests
./dev.sh test-frontend    # Linux/macOS
.\dev.ps1 test-frontend   # Windows

# Open a shell in the frontend container
./dev.sh bash-frontend    # Linux/macOS
.\dev.ps1 bash-frontend   # Windows
```
