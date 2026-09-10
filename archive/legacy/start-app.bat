@echo off
echo Cleaning up previous server processes...
powershell -Command "$p = Get-NetTCPConnection -LocalPort 3000, 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | Sort-Object -Unique; if ($p) { Stop-Process -Id $p -Force -ErrorAction SilentlyContinue }"

echo Starting Backend Server...
start "Backend Server" cmd /k "cd Visual-Intelligence\product\backend && python -m uvicorn main:app --reload --reload-dir app --host localhost"

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd Visual-Intelligence\product\frontend && npm run dev"

echo Both servers are starting in separate windows.
echo Please wait a few seconds, then open http://localhost:3000 in your browser.
