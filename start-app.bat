@echo off
echo Cleaning up previous server processes...
powershell -Command "Get-NetTCPConnection -LocalPort 3000, 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | Sort-Object -Unique | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }"

echo Starting Backend Server...
start "Backend Server" cmd /k "cd Visual-Intelligence\product\backend && .venv\Scripts\activate && python -m uvicorn app.main:app --reload"

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd Visual-Intelligence\product\frontend && npm run dev"

echo Both servers are starting in separate windows.
echo Please wait a few seconds, then open http://localhost:3000 in your browser.
