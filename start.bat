@echo off 
echo Starting CoffeeFlow Production Server... 
 
venv\Scripts\activate 
python manage.py collectstatic --noinput 
python manage.py migrate 
gunicorn milkflow.wsgi:application --bind 0.0.0.0:8000 --workers 3 
pause 
