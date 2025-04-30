#!/bin/bash
set -e

# Add project root to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/opt/render/project/src

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set Django settings module
export DJANGO_SETTINGS_MODULE=myproject.settings

# Reset database and migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
rm -f db.sqlite3

# Run Django commands
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py collectstatic --noinput