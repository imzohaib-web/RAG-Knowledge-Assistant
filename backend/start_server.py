#!/usr/bin/env python3
"""
Startup script for RAG Knowledge Assistant Backend
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python version: {sys.version}")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import pdfplumber
        import langchain
        import sentence_transformers
        import faiss
        import groq
        import numpy
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_groq_api_key():
    """Check if Groq API key is set"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Warning: GROQ_API_KEY environment variable is not set")
        print("Please set it before starting the server:")
        print("Windows: set GROQ_API_KEY=your_api_key_here")
        print("Mac/Linux: export GROQ_API_KEY=your_api_key_here")
        print("")
        print("You can get a free API key from: https://groq.com")
        return False
    print("✓ Groq API key is configured")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["uploads", "vector_store"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory ready: {directory}")

def start_server():
    """Start the FastAPI server"""
    print("\n" + "="*50)
    print("Starting RAG Knowledge Assistant Backend...")
    print("="*50)
    print("Server will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    try:
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

def main():
    """Main startup function"""
    print("RAG Knowledge Assistant Backend - Startup Check")
    print("=" * 50)
    
    # Run checks
    check_python_version()
    
    if not check_dependencies():
        sys.exit(1)
    
    groq_configured = check_groq_api_key()
    create_directories()
    
    # Warning if Groq API key is not set
    if not groq_configured:
        print("\n" + "!" * 50)
        print("WARNING: Groq API key not configured!")
        print("The server will start but chat functionality will not work.")
        print("!" * 50 + "\n")
        
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled. Please configure API key and try again.")
            sys.exit(1)
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
