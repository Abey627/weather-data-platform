#!/usr/bin/env powershell

# Script to run contract tests for external API integrations
# These tests make actual API calls and should be run in a controlled environment

Write-Host "Running contract tests for external API integrations..." -ForegroundColor Cyan

# Build and run the backend container if not already running
$isRunning = docker-compose ps -q backend
if (!$isRunning) {
    Write-Host "Starting backend container..." -ForegroundColor Yellow
    docker-compose up -d backend
    
    # Wait for container to be ready
    Start-Sleep -Seconds 5
}

# Install jsonschema package if not already installed
Write-Host "Ensuring jsonschema package is installed..." -ForegroundColor Yellow
docker-compose exec backend pip install jsonschema

# Run the contract tests
Write-Host "Running contract tests..." -ForegroundColor Green
docker-compose exec backend pytest -v -m contract

Write-Host "Contract tests completed." -ForegroundColor Cyan