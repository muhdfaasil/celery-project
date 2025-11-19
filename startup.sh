#!/bin/bash

# Azure App Service startup script for Django Celery project
# This script runs when the app starts on Azure

echo "Starting Django application..."

# Change to the app directory
cd /tmp/8de27351fb5c391

# Run migrations (if needed)
echo "Running database migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

# Collect static files (if not already collected)
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Static files collection failed, continuing..."

# Start Gunicorn (Azure will use this if configured)
# Uncomment and configure if you want to use Gunicorn instead of default server
# gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2

echo "Startup script completed."

