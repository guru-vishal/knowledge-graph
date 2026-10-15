@echo off
setlocal
cd /d "%~dp0"

if not exist env\Scripts\python.exe (
    echo ERROR: Run setupdev.bat first.
    exit /b 1
)

if not exist frontend\node_modules (
    echo ERROR: Frontend dependencies are missing.
    echo Run setupdev.bat first.
    exit /b 1
)

echo Starting Personal Knowledge Graph...

start "Knowledge Graph Backend" cmd /k "cd /d %~dp0 && call env\Scripts\activate.bat && python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000"

start "Knowledge Graph Frontend" cmd /k "cd /d %~dp0frontend && npm run dev -- --host 127.0.0.1"

echo.
echo Backend:  http://127.0.0.1:8000
echo Swagger:  http://127.0.0.1:8000/docs
echo Frontend: http://127.0.0.1:5173
echo.
echo Close the two application windows to stop the services.
endlocal