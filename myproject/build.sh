#!/bin/bash
set -e

# Add project root to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/opt/render/project/src

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set Django settings module
export DJANGO_SETTINGS_MODULE=myproject.myproject.settings

# Run Django commands
python manage.py collectstatic --noinput
python manage.py migrate