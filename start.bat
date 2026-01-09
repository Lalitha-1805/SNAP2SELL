@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  AgriSmart - AI-Powered Agriculture E-Commerce Platform     ║
echo ║                   Startup Script                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found. Please install Python 3.10+
    exit /b 1
)

REM Create virtual environment if not exists
if not exist "backend\venv" (
    echo Creating Python virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

REM Activate virtual environment
echo Activating Python virtual environment...
call backend\venv\Scripts\activate.bat

REM Install backend dependencies
echo Installing backend dependencies...
cd backend
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ✗ Failed to install backend dependencies
    exit /b 1
)
cd ..

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Node.js not found. Please install Node.js 16+
    exit /b 1
)

REM Install frontend dependencies
echo Installing frontend dependencies...
cd frontend
if not exist "node_modules" (
    npm install >nul 2>&1
    if errorlevel 1 (
        echo ✗ Failed to install frontend dependencies
        exit /b 1
    )
)
cd ..

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  ✓ Setup Complete! Starting servers...                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Starting Backend Server (Port 5000)...
echo Starting Frontend Server (Port 5173)...
echo.
echo Open in your browser:
echo - Frontend: http://localhost:5173
echo - Backend API: http://localhost:5000/api/info
echo.

REM Start backend in new window
start "AgriSmart Backend" cmd /k "cd backend && python app.py"

REM Start frontend in new window
timeout /t 3 /nobreak
start "AgriSmart Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ✓ Both servers started successfully!
echo Press Ctrl+C in any window to stop the server.
echo.
