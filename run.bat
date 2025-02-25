@echo off
REM Exit immediately if a command exits with a non-zero status
setlocal enabledelayedexpansion

REM Activate the virtual environment
echo Activating the virtual environment...
call venv\Scripts\activate

REM Run the Flask backend in the background
echo Starting the Flask backend...
start /B python main.py

REM Wait for a few seconds to ensure the Flask server starts
timeout /t 5

REM Run the Streamlit app
echo Starting the Streamlit app...
streamlit run streamlit.py

REM Deactivate the virtual environment when done
deactivate

pause