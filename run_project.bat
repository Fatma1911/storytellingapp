:: Set the path to your virtual environment
set VENV_DIR=venv

:: Activate the virtual environment
call %VENV_DIR%\Scripts\activate

:: Install project dependencies
pip install -r requirements.txt

:: Run your Python script (adjust the script name as needed)
python manage.py runserver

:: Deactivate the virtual environment
deactivate

