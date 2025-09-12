#!/bin/bash
# Setup Environment Script for Unix-based systems
# Run this script to set up your development environment

echo -e "\033[0;32mSetting up Weather Data Platform environment...\033[0m"

# Check if .env file exists
if [ ! -f ".env" ]; then
    # Copy example .env file
    if [ -f ".env.example" ]; then
        echo -e "\033[0;33mCreating .env file from example...\033[0m"
        cp .env.example .env
        
        # Generate a secure Django secret key
        if [ -f "scripts/generate_secret_key.py" ]; then
            echo -e "\033[0;33mGenerating secure Django secret key...\033[0m"
            SECRET_KEY=$(python scripts/generate_secret_key.py | tail -3 | head -1)
            
            # Update the secret key in .env file
            sed -i "s/DJANGO_SECRET_KEY=change-this-to-a-random-secure-string/DJANGO_SECRET_KEY=$SECRET_KEY/" .env
        else
            echo -e "\033[0;31mWarning: Secret key generator script not found!\033[0m"
            echo -e "\033[0;33mPlease manually update the DJANGO_SECRET_KEY in your .env file.\033[0m"
        fi
        
        echo -e "\033[0;33m\nPlease update the passwords in your .env file with secure values.\033[0m"
    else
        echo -e "\033[0;31mError: .env.example file not found!\033[0m"
        exit 1
    fi
else
    echo -e "\033[0;32m.env file already exists.\033[0m"
fi

# Make sure the user knows to update passwords
echo -e "\033[0;32m\nEnvironment setup complete!\033[0m"
echo -e "\033[0;33mRemember to update all passwords in your .env file with secure values before deploying.\033[0m"
echo -e "\033[0;32mYou can now run 'docker-compose up' to start the development environment.\033[0m"
