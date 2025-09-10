#!/bin/bash

# Script to simplify Docker operations for development

# Display help information
show_help() {
    echo "Weather Data Platform Development Script"
    echo "----------------------------------------"
    echo "Usage: ./dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  up            Start all services in development mode"
    echo "  down          Stop all services"
    echo "  backend       Start only the backend service"
    echo "  frontend      Start only the frontend service"
    echo "  db            Start only the database service"
    echo "  logs          View logs of all services"
    echo "  logs-backend  View logs of the backend service"
    echo "  logs-frontend View logs of the frontend service"
    echo "  migrate       Run Django migrations"
    echo "  test-backend  Run backend tests"
    echo "  test-frontend Run frontend tests"
    echo "  shell         Open a Django shell"
    echo "  bash-backend  Open a bash shell in the backend container"
    echo "  bash-frontend Open a bash shell in the frontend container"
    echo "  help          Show this help message"
}

# Main command handler
case "$1" in
    up)
        docker-compose up -d
        ;;
    down)
        docker-compose down
        ;;
    backend)
        docker-compose up -d backend db redis
        ;;
    frontend)
        docker-compose up -d frontend
        ;;
    db)
        docker-compose up -d db
        ;;
    logs)
        docker-compose logs -f
        ;;
    logs-backend)
        docker-compose logs -f backend
        ;;
    logs-frontend)
        docker-compose logs -f frontend
        ;;
    migrate)
        docker-compose exec backend python manage.py migrate
        ;;
    test-backend)
        docker-compose exec backend pytest
        ;;
    test-frontend)
        docker-compose exec frontend npm test
        ;;
    shell)
        docker-compose exec backend python manage.py shell
        ;;
    bash-backend)
        docker-compose exec backend bash
        ;;
    bash-frontend)
        docker-compose exec frontend sh
        ;;
    help)
        show_help
        ;;
    *)
        show_help
        ;;
esac
