#!/bin/bash
# Script to check and apply migrations in a CI/CD or build process
# This script runs the bash script inside the Docker container

APPLY_FLAG=""
if [ "$1" == "--apply" ]; then
    APPLY_FLAG="--apply"
    echo "Will apply migrations if needed."
fi

echo "=== Checking Django migrations ==="

# Make sure the script is executable inside the container
docker-compose exec backend chmod +x /app/scripts/check_apply_migrations.sh

# Run the migration check script inside the container
docker-compose exec backend /app/scripts/check_apply_migrations.sh $APPLY_FLAG

# Store the exit code
EXIT_CODE=$?

# Check the exit code to determine if there were issues
if [ $EXIT_CODE -eq 0 ]; then
    echo "Migration check successful."
elif [ $EXIT_CODE -eq 1 ]; then
    echo "ERROR: New migrations need to be created."
    exit 1
elif [ $EXIT_CODE -eq 2 ]; then
    echo "WARNING: Pending migrations need to be applied."
    exit 2
else
    echo "Unknown error during migration check."
    exit $EXIT_CODE
fi