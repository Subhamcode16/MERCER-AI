@echo off
title Fieldwork React Workspace

echo ========================================================
echo Starting Fieldwork React Workspace...
echo ========================================================

cd /d "%~dp0"

:: Add Node.js paths to process PATH if node.exe exists
if exist "%USERPROFILE%\.nodejs\node.exe" set "PATH=%USERPROFILE%\.nodejs;%PATH%"
if exist "C:\Users\User\.nodejs\node.exe" set "PATH=C:\Users\User\.nodejs;%PATH%"
if exist "C:\Program Files\nodejs\node.exe" set "PATH=C:\Program Files\nodejs;%PATH%"
if exist "C:\Program Files (x86)\nodejs\node.exe" set "PATH=C:\Program Files (x86)\nodejs;%PATH%"
if exist "%LocalAppData%\Programs\node\node.exe" set "PATH=%LocalAppData%\Programs\node;%PATH%"
if exist "%AppData%\npm" set "PATH=%AppData%\npm;%PATH%"

:: Check if Node.js works
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js was not detected.
    echo Please install Node.js from https://nodejs.org/ and try again.
    pause
    exit /b 1
)

:: Run dev server with pnpm or npm
call pnpm --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using pnpm dev server...
    call pnpm dev
) else (
    echo Using npm dev server...
    call npm run dev
)
