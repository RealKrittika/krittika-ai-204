@echo off
REM Run the FastAPI app with reload (Windows)
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause
