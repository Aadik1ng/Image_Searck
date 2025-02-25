@echo off
REM Exit immediately if a command exits with a non-zero status
setlocal enabledelayedexpansion

REM Create a virtual environment
echo Creating a virtual environment...
python -m venv venv

REM Activate the virtual environment
echo Activating the virtual environment...
call venv\Scripts\activate

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt
pip install git+https://github.com/openai/CLIP.git
pip install streamlit

REM Create necessary directories
echo Creating necessary directories...
mkdir static\images

REM Run the initializer script
echo Running the initializer script...
python setup\initializer.py

REM Deactivate the virtual environment when done
deactivate

echo Setup completed successfully!
pause