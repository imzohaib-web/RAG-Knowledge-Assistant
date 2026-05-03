@echo off
echo Starting RAG Knowledge Assistant...
echo.

echo [1/3] Setting up environment...
cd /d "%~dp0backend"

echo [2/3] Starting Backend Server...
start "Backend Server" cmd /k "python main.py"

echo [3/3] Starting Frontend Server...
cd /d "%~dp0rag-ui"
start "Frontend Server" cmd /k "npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173 (or http://localhost:3000)
echo.
echo Press any key to exit...
pause > nul
