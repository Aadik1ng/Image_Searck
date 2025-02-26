@echo off
REM Check if virtual environment exists; if not, create it
IF NOT EXIST "venv\Scripts\activate" (
    echo Virtual environment not found. Creating virtual environment...
    python -m venv venv
) ELSE (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Check if the required packages are installed by attempting to import them
echo Checking if required packages are installed...
python -c "import pkg_resources; pkg_resources.require(['flask', 'streamlit'])" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Required packages are missing. Installing...
    pip install -r requirements.txt
) ELSE (
    echo All required packages are already installed.
)

REM Set the PYTHONPATH to the current directory for relative imports
set PYTHONPATH=%cd%

REM Database has been initialized
python init\initialize.py

REM Start the Flask API in a new window
echo Starting Flask API
start cmd /k "python main.py"

REM Start the Streamlit app in a new window
echo Starting Streamlit App
start cmd /k "streamlit run image_api_test.py"

echo All processes checked.
pause
