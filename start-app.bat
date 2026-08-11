@echo off
echo ============================================================
echo  Mercer AI — Startup Sequence
echo ============================================================

echo.
echo [1/3] Cleaning up previous server processes...
powershell -Command "$p = Get-NetTCPConnection -LocalPort 3000, 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | Sort-Object -Unique; if ($p) { Stop-Process -Id $p -Force -ErrorAction SilentlyContinue }"

echo.
echo [2/3] Starting Backend Server (FastAPI on :8000)...
start "Mercer Backend" cmd /k "cd Visual-Intelligence\product\backend && uv run python -m uvicorn app.main:app --reload --reload-dir app --host 127.0.0.1 --port 8000"

echo.
echo      Waiting for backend to become healthy...
echo      (Polls /health every 1s — max 30 attempts)
echo.

set /a ATTEMPTS=0
set MAX_ATTEMPTS=30

:WAIT_LOOP
set /a ATTEMPTS+=1
if %ATTEMPTS% GTR %MAX_ATTEMPTS% (
    echo.
    echo [ERROR] Backend did not become healthy after 30s.
    echo         Check the Backend window for errors, then re-run this script.
    pause
    exit /b 1
)

powershell -Command "try { $r = Invoke-WebRequest -Uri http://127.0.0.1:8000/health -UseBasicParsing -TimeoutSec 1 -ErrorAction Stop; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if %ERRORLEVEL% EQU 0 goto BACKEND_READY

<nul set /p "=."
timeout /t 1 /nobreak >nul
goto WAIT_LOOP

:BACKEND_READY
echo.
echo      Backend is healthy after %ATTEMPTS%s.

echo.
echo [3/3] Starting Frontend Server (Next.js on :3000)...
start "Mercer Frontend" cmd /k "cd Visual-Intelligence\product\frontend && npm run dev"

echo.
echo ============================================================
echo  Both servers started.
echo  Open http://localhost:3000 in your browser.
echo ============================================================
echo.
