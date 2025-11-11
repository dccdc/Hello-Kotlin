@echo off
REM 一键推送脚本 - Windows

echo 🚀 推送项目到 GitHub
echo ====================
echo.
echo 目标仓库: https://github.com/dccdc/mouse-controller.git
echo.

REM 检查是否在正确的目录
if not exist "main.py" (
    echo ❌ 错误：请在 mouse_recorder 目录下运行此脚本
    pause
    exit /b 1
)

REM 检查 git 状态
echo 📊 检查 Git 状态...
git status
echo.

echo 📤 准备推送...
echo.

REM 推送到远程仓库
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ 推送成功！
    echo.
    echo 🎉 访问你的项目：
    echo    https://github.com/dccdc/mouse-controller
    echo.
) else (
    echo.
    echo ❌ 推送失败
    echo.
    echo 💡 可能需要：
    echo    1. 确保仓库已在 GitHub 创建
    echo    2. 配置 GitHub 认证（Personal Access Token）
    echo    3. 检查网络连接
    echo.
    echo 📖 详细说明请查看: PUSH_TO_GITHUB.md
    pause
    exit /b 1
)

pause
