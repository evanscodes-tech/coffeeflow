@echo off 
echo =============================================== 
echo      CoffeeFlow - Complete Setup              
echo =============================================== 
echo. 
echo [1/7] Checking Python installation... 
python --version 
if errorlevel 1 ( 
  echo ERROR: Python 3.8+ is required! 
  echo Download from: https://python.org 
  pause 
  exit /b 1 
) 
echo. 
echo [2/7] Creating virtual environment... 
python -m venv venv 
if errorlevel 1 ( 
  echo ERROR: Failed to create virtual environment 
  echo Try: pip install virtualenv 
  pause 
  exit /b 1 
) 
echo. 
echo [3/7] Activating virtual environment... 
call venv\Scripts\activate 
echo. 
echo [4/7] Installing dependencies... 
echo This may take a few minutes... 
pip install --upgrade pip 
pip install -r requirements.txt 
if errorlevel 1 ( 
  echo WARNING: Some packages failed to install 
  echo Trying with no-deps flag... 
  pip install -r requirements.txt --no-deps 
) 
echo. 
echo [5/7] Applying Django migrations... 
python manage.py migrate 
echo. 
echo [6/7] Collecting static files... 
python manage.py collectstatic --noinput 
echo. 
echo [7/7] Setup Options: 
echo. 
echo 1. Create superuser (admin) 
echo 2. Load sample data 
echo 3. Skip additional setup 
echo. 
set /p choice="Enter choice (1, 2, or 3): " 
if "!choice!"=="1" ( 
  python manage.py createsuperuser 
) else if "!choice!"=="2" ( 
  echo Loading sample data... 
  if exist milkflow/fixtures/ ( 
    python manage.py loaddata milkflow/fixtures/*.json 
  ) 
  if exist core/fixtures/ ( 
    python manage.py loaddata core/fixtures/*.json 
  ) 
) 
echo. 
echo =============================================== 
echo            SETUP COMPLETE!                     
echo =============================================== 
echo. 
echo NEXT STEPS: 
echo ----------- 
echo 1. Activate environment: venv\Scripts\activate 
echo 2. Run Django server: python manage.py runserver 
echo 3. Open browser: http://localhost:8000 
echo. 
echo Optional: 
echo - Run hardware simulator: python simulate_hardware.py 
echo - Start Jupyter: jupyter notebook 
echo. 
pause 
