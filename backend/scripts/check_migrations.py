#!/usr/bin/env python3
"""
Script to check for pending Django migrations.

This script:
1. Checks if any model changes need new migrations (makemigrations)
2. Checks if there are any pending migrations that need to be applied (migrate)

Exit codes:
- 0: No issues found (no migrations needed)
- 1: New migrations need to be created (makemigrations needed)
- 2: Pending migrations need to be applied (migrate needed)
- 3: Both new migrations need to be created and pending migrations need to be applied
"""

import os
import sys
import django
import subprocess
from django.core.management import call_command
from io import StringIO

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weatherapi.settings')
django.setup()


def check_makemigrations_needed():
    """Check if makemigrations is needed."""
    output = StringIO()
    call_command('makemigrations', '--dry-run', '--check', stdout=output)
    output_str = output.getvalue()
    
    # If there are no migrations to be made, output will indicate that
    return 'No changes detected' not in output_str


def check_migrate_needed():
    """Check if migrate is needed."""
    output = StringIO()
    call_command('showmigrations', stdout=output)
    output_str = output.getvalue()
    
    # If all migrations are applied, there will be no [ ] (unchecked) items
    return '[ ]' in output_str


def main():
    """Run migration checks and return appropriate exit code."""
    makemigrations_needed = check_makemigrations_needed()
    migrate_needed = check_migrate_needed()
    
    if makemigrations_needed and migrate_needed:
        print("ACTION REQUIRED: Both new migrations need to be created and pending migrations need to be applied.")
        print("Run 'python manage.py makemigrations' and then 'python manage.py migrate'")
        return 3
    elif makemigrations_needed:
        print("ACTION REQUIRED: New migrations need to be created.")
        print("Run 'python manage.py makemigrations'")
        return 1
    elif migrate_needed:
        print("ACTION REQUIRED: Pending migrations need to be applied.")
        print("Run 'python manage.py migrate'")
        return 2
    else:
        print("No migration issues found. Database schema is up to date.")
        return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)