@echo off
echo ========================================
echo RAG Knowledge Assistant - Quick Start
echo ========================================
echo.

echo [1/4] Checking dependencies...
cd /d "%~dp0backend"
python -c "import fastapi, uvicorn, pdfplumber, langchain, sentence_transformers, faiss, groq" 2>nul
if errorlevel 1 (
    echo Installing missing dependencies...
    pip install -r requirements.txt
)

echo [2/4] Setting up directories...
if not exist uploads mkdir uploads
if not exist vector_store mkdir vector_store

echo [3/4] Starting Backend Server...
start "Backend Server" cmd /k "echo Backend starting on http://localhost:8000 && python main.py"

echo [4/4] Starting Frontend Server...
cd /d "%~dp0rag-ui"
start "Frontend Server" cmd /k "echo Frontend starting... && npm run dev"

echo.
echo ========================================
echo SYSTEM STARTING UP...
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo API Docs:    http://localhost:8000/docs
echo Frontend:    http://localhost:5173 (or 3000)
echo.
echo IMPORTANT: Set your Groq API key before using chat:
echo   set GROQ_API_KEY=your_api_key_here
echo.
echo Both servers are starting in separate windows...
echo.
pause
