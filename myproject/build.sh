#!/bin/bash
set -e

# Install dependencies
pip install -r requirements.txt

# Set correct Django settings module 
export DJANGO_SETTINGS_MODULE=myproject.settings  # Change to your actual project name

# Run Django commands
python manage.py collectstatic --noinput
python manage.py migrate