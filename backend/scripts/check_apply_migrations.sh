#!/bin/bash
# Script to check and apply migrations in a CI/CD or build process
# This script is meant to be run inside the Docker container

set -e  # Exit immediately if a command exits with a non-zero status

echo "=== Checking Django migrations ==="

# Check if new migrations need to be created
echo "Checking for model changes that would require new migrations..."
if ! python manage.py makemigrations --check 2>/dev/null; then
    echo "ERROR: There are model changes that require new migrations."
    echo "Run 'python manage.py makemigrations' to create them."
    exit 1
fi

# Check if there are pending migrations
echo "Checking for pending migrations..."
PENDING_MIGRATIONS=$(python manage.py showmigrations | grep -c "\[ \]" || true)

if [ "$PENDING_MIGRATIONS" -gt 0 ]; then
    echo "WARNING: There are $PENDING_MIGRATIONS pending migrations that need to be applied."
    
    # If this is a build process, we might want to apply them automatically
    if [ "$1" == "--apply" ]; then
        echo "Applying migrations automatically..."
        python manage.py migrate
    else
        echo "Run 'python manage.py migrate' to apply them."
        echo "Or run this script with --apply to apply them automatically."
        exit 2
    fi
else
    echo "All migrations are up to date."
fi

echo "=== Migration check completed ==="
exit 0