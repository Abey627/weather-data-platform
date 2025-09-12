#!/bin/bash

# Script to run contract tests for external API integrations
# These tests make actual API calls and should be run in a controlled environment

echo -e "\033[36mRunning contract tests for external API integrations...\033[0m"

# Build and run the backend container if not already running
if [ -z "$(docker-compose ps -q backend)" ]; then
    echo -e "\033[33mStarting backend container...\033[0m"
    docker-compose up -d backend
    
    # Wait for container to be ready
    sleep 5
fi

# Install jsonschema package if not already installed
echo -e "\033[33mEnsuring jsonschema package is installed...\033[0m"
docker-compose exec backend pip install jsonschema

# Run the contract tests
echo -e "\033[32mRunning contract tests...\033[0m"
docker-compose exec backend pytest -v -m contract

echo -e "\033[36mContract tests completed.\033[0m"