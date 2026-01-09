@echo off
REM Simple startup script for AgriSmart
echo.
echo Starting AgriSmart Platform...
echo.

REM Check if backend venv exists
if not exist "backend\venv\Scripts\python.exe" (
    echo Creating Python virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

REM Install backend dependencies silently
echo Installing backend dependencies...
cd backend
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
cd ..

REM Install frontend dependencies if needed
echo Installing frontend dependencies...
cd frontend
if not exist "node_modules" (
    call npm install --silent
)
cd ..

echo.
echo ====================================================================
echo AgriSmart - Startup Complete!
echo ====================================================================
echo.
echo Opening servers in new windows...
echo.

REM Start backend
start "AgriSmart Backend" cmd /k "cd backend && venv\Scripts\activate.bat && python app.py"

REM Wait a moment
timeout /t 2 /nobreak

REM Start frontend
start "AgriSmart Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Servers started!
echo - Frontend: http://localhost:5173
echo - Backend: http://localhost:5000/api
echo.
pause
