# PowerShell script to simplify Docker operations for development

# Display help information
function Show-Help {
    Write-Host "Weather Data Platform Development Script"
    Write-Host "----------------------------------------"
    Write-Host "Usage: .\dev.ps1 [command]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  up            Start all services in development mode"
    Write-Host "  down          Stop all services"
    Write-Host "  backend       Start only the backend service"
    Write-Host "  frontend      Start only the frontend service"
    Write-Host "  db            Start only the database service"
    Write-Host "  logs          View logs of all services"
    Write-Host "  logs-backend  View logs of the backend service"
    Write-Host "  logs-frontend View logs of the frontend service"
    Write-Host "  migrate       Run Django migrations"
    Write-Host "  test-backend  Run backend tests"
    Write-Host "  test-frontend Run frontend tests"
    Write-Host "  shell         Open a Django shell"
    Write-Host "  bash-backend  Open a bash shell in the backend container"
    Write-Host "  bash-frontend Open a bash shell in the frontend container"
    Write-Host "  help          Show this help message"
}

# Main command handler
switch ($args[0]) {
    "up" {
        docker-compose up -d
    }
    "down" {
        docker-compose down
    }
    "backend" {
        docker-compose up -d backend db redis
    }
    "frontend" {
        docker-compose up -d frontend
    }
    "db" {
        docker-compose up -d db
    }
    "logs" {
        docker-compose logs -f
    }
    "logs-backend" {
        docker-compose logs -f backend
    }
    "logs-frontend" {
        docker-compose logs -f frontend
    }
    "migrate" {
        docker-compose exec backend python manage.py migrate
    }
    "test-backend" {
        docker-compose exec backend pytest
    }
    "test-frontend" {
        docker-compose exec frontend npm test
    }
    "shell" {
        docker-compose exec backend python manage.py shell
    }
    "bash-backend" {
        docker-compose exec backend bash
    }
    "bash-frontend" {
        docker-compose exec frontend sh
    }
    "help" {
        Show-Help
    }
    default {
        Show-Help
    }
}
