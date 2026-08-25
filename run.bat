@echo off
echo Starting iGOT Adapter and Recommendation Engine for SIH (Desktop SIH)...
python -m pip install -r requirements.txt
python -m uvicorn server:app --reload --host 127.0.0.1 --port 8000
pause
