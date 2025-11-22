@echo off
echo Starting Dental AI Clinic...
echo Opening browser at http://127.0.0.1:8000/static/index.html
start http://127.0.0.1:8000/static/index.html
uvicorn interfaz.main:app --reload
pause
