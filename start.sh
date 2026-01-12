#!/bin/bash 
# Activate virtual environment 
source venv/bin/activate 
 
# Collect static files 
python manage.py collectstatic --noinput 
 
# Apply database migrations 
python manage.py migrate 
 
# Start Gunicorn 
gunicorn milkflow.wsgi:application --bind 0.0.0.0:8000 --workers 3 
