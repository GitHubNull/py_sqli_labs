@echo off
chcp 65001 >nul
REM ================================================
REM Flask SQLi-Labs 环境安装脚本 (Windows版)
REM 功能: 检查并安装uv包管理器和项目依赖
REM 版本: 1.0
REM 日期: 2025-06-04
REM ================================================

echo.
echo ========================================
echo  Flask SQLi-Labs 环境安装脚本
echo ========================================
echo.

REM 检查Python是否安装
echo [1/5] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python已安装: %PYTHON_VERSION%
)

echo.

REM 检查pip是否可用
echo [2/5] 检查pip包管理器...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: pip不可用，请检查Python安装
    pause
    exit /b 1
) else (
    echo ✅ pip可用
)

echo.

REM 检查uv是否安装
echo [3/5] 检查uv包管理器...
uv --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  uv未安装，正在安装...
    
    REM 尝试通过pip安装uv
    python -m pip install uv
    if errorlevel 1 (
        echo ❌ 通过pip安装uv失败，尝试官方安装方式...
        
        REM 使用PowerShell安装uv
        powershell -Command "irm https://astral.sh/uv/install.ps1 | iex" 2>nul
        if errorlevel 1 (
            echo ❌ uv安装失败，请手动安装
            echo 安装命令: pip install uv
            echo 或访问: https://github.com/astral-sh/uv
            pause
            exit /b 1
        )
    )
    
    REM 重新检查uv安装
    uv --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ uv安装失败，请重启命令行后重试
        pause
        exit /b 1
    ) else (
        echo ✅ uv安装成功
    )
) else (
    for /f "tokens=2" %%i in ('uv --version 2^>^&1') do set UV_VERSION=%%i
    echo ✅ uv已安装: %UV_VERSION%
)

echo.

REM 检查requirements.txt是否存在
echo [4/5] 检查项目依赖文件...
if not exist requirements.txt (
    echo ❌ 错误: 未找到requirements.txt文件
    echo 请确保在项目根目录下运行此脚本
    pause
    exit /b 1
) else (
    echo ✅ 找到requirements.txt
)

echo.

REM 创建虚拟环境并安装依赖
echo [5/5] 安装项目依赖...

REM 检查是否已存在虚拟环境
if exist .venv (
    echo ℹ️  虚拟环境已存在，跳过创建
) else (
    echo 📦 创建虚拟环境...
    uv venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
)

echo 📥 安装项目依赖...
uv pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败，尝试传统方式...
    REM 激活虚拟环境并使用pip安装
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo ✅ 依赖安装成功
)

echo.
echo ========================================
echo ✅ 环境安装完成！
echo ========================================
echo.
echo 📋 接下来的步骤:
echo 1. 激活虚拟环境: .venv\Scripts\activate.bat
echo 2. 启动应用: python app.py
echo 3. 访问地址: http://localhost:5000
echo.
echo 💡 提示: 可以直接运行 start.bat 启动应用
echo.

REM 询问是否立即启动
set /p START_APP="是否现在启动应用？(y/N): "
if /i "%START_APP%"=="y" (
    echo.
    echo 🚀 启动应用...
    call .venv\Scripts\activate.bat
    python app.py
) else (
    echo.
    echo 👋 安装完成，随时可以启动应用！
)

pause 