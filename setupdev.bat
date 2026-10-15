@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo Personal Knowledge Graph - Setup
echo ========================================

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not on PATH.
    exit /b 1
)

where npm >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js/npm is not installed or not on PATH.
    exit /b 1
)

if not exist env\Scripts\python.exe (
    echo Creating Python virtual environment...
    python -m venv env
    if errorlevel 1 exit /b 1
)

echo Installing backend dependencies...
call env\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

echo Applying database migrations...
call env\Scripts\alembic.exe upgrade head
if errorlevel 1 exit /b 1

echo Installing frontend dependencies...
if not exist frontend\package.json (
    echo ERROR: frontend\package.json not found.
    exit /b 1
)

cd frontend
call npm install
if errorlevel 1 exit /b 1
cd ..

echo.
echo Setup complete.
echo Run runapplication.bat to start the application.
endlocal