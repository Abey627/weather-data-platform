# Setup Environment Script for Windows PowerShell
# Run this script to set up your development environment

Write-Host "Setting up Weather Data Platform environment..." -ForegroundColor Green

# Check if .env file exists
if (-Not (Test-Path -Path ".env")) {
    # Copy example .env file
    if (Test-Path -Path ".env.example") {
        Write-Host "Creating .env file from example..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        
        # Generate a secure Django secret key
        if (Test-Path -Path "scripts/generate_secret_key.py") {
            Write-Host "Generating secure Django secret key..." -ForegroundColor Yellow
            $secretKey = python scripts/generate_secret_key.py | Select-Object -Last 3 | Select-Object -First 1
            
            # Update the secret key in .env file
            (Get-Content .env) -replace "DJANGO_SECRET_KEY=change-this-to-a-random-secure-string", "DJANGO_SECRET_KEY=$secretKey" | Set-Content .env
        } else {
            Write-Host "Warning: Secret key generator script not found!" -ForegroundColor Red
            Write-Host "Please manually update the DJANGO_SECRET_KEY in your .env file." -ForegroundColor Yellow
        }
        
        Write-Host "`nPlease update the passwords in your .env file with secure values." -ForegroundColor Yellow
    } else {
        Write-Host "Error: .env.example file not found!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host ".env file already exists." -ForegroundColor Green
}

# Make sure the user knows to update passwords
Write-Host "`nEnvironment setup complete!" -ForegroundColor Green
Write-Host "Remember to update all passwords in your .env file with secure values before deploying." -ForegroundColor Yellow
Write-Host "You can now run 'docker-compose up' to start the development environment." -ForegroundColor Green
