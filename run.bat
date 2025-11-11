@echo off
REM Windows 运行脚本

echo 🖱️  鼠标录制回放工具
echo ====================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

REM 检查依赖
python -c "import pynput" >nul 2>&1
if errorlevel 1 (
    echo 📦 正在安装依赖...
    pip install -r requirements.txt
)

REM 运行程序
echo 🚀 启动程序...
python main.py
