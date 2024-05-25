@echo off
REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Install requirements
pip install -r requirements.txt

REM Create settings.json
echo {^
    "AWS_ACCESS_KEY": ["AWS Access Key", "AKIA[0-9A-Z]{16}"],^
    "AWS_SECRET_KEY": ["AWS Secret Key", "[A-Za-z0-9+/]{40}"]^
} > settings.json

REM Run the Python script
python main.py

REM Deactivate virtual environment
deactivate
