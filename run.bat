@echo off
REM ============================================================
REM  OpusMagnum · 巨作 / GreatWork - One-Click Launcher
REM  One-Person Company Command Center
REM ============================================================

set PROJECT_DIR=D:\opus-magnum
set PORT=8500

echo ==========================================
echo   OpusMagnum · 巨作 / GreatWork
echo   One-Person Company Command Center
echo   Port: %PORT%
echo ==========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH.
    pause
    exit /b 1
)

REM 检查依赖
if not exist "%PROJECT_DIR%\venv\" (
    echo [SETUP] First run: creating venv and installing dependencies...
    python -m venv "%PROJECT_DIR%\venv"
    call "%PROJECT_DIR%\venv\Scripts\activate.bat"
    python -m pip install -r "%PROJECT_DIR%\requirements.txt"
) else (
    call "%PROJECT_DIR%\venv\Scripts\activate.bat"
)

REM 复制 .env.example 为 .env（如果不存在）
if not exist "%PROJECT_DIR%\.env" (
    copy "%PROJECT_DIR%\.env.example" "%PROJECT_DIR%\.env"
    echo [SETUP] .env file created from template. Please edit it if needed.
)

REM 启动 Streamlit
echo.
echo [START] Launching OpusMagnum on port %PORT%...
cd /d "%PROJECT_DIR%"
streamlit run app.py --server.port %PORT% --server.address localhost

pause
