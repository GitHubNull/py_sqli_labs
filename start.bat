@echo off
chcp 65001 >nul
REM ================================================
REM Flask SQLi-Labs 快速启动脚本 (Windows版)
REM ================================================

echo.
echo 🚀 启动 Flask SQLi-Labs...
echo.

REM 检查虚拟环境是否存在
if not exist .venv (
    echo ❌ 虚拟环境不存在，请先运行 setup.bat 安装环境
    pause
    exit /b 1
)

REM 激活虚拟环境并启动应用
call .venv\Scripts\activate.bat
echo ✅ 虚拟环境已激活
echo 📡 启动Flask应用服务器...
echo.
python app.py