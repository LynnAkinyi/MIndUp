#!/bin/bash
set -e

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set Django settings
export DJANGO_SETTINGS_MODULE=myproject.settings

# Run Django commands
python manage.py collectstatic --noinput
python manage.py migrate