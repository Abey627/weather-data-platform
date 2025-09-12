#!/usr/bin/env python
"""
Script to generate a secure Django secret key.
"""
import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure secret key for Django settings."""
    # Define the character set to use
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    
    # Generate a secure random string
    secret_key = ''.join(secrets.choice(chars) for _ in range(length))
    
    return secret_key

if __name__ == "__main__":
    key = generate_secret_key()
    print("\nGenerated Django Secret Key:")
    print("-" * 60)
    print(key)
    print("-" * 60)
    print("\nAdd this to your .env file as:")
    print("DJANGO_SECRET_KEY=", key, sep="")
