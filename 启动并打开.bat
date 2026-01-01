@echo off
chcp 65001 >nul
title 启动测试服务器

echo.
echo ========================================
echo   启动测试服务器并打开浏览器
echo ========================================
echo.

REM 检查文件
if not exist "holland_test_preview.html" (
    echo [错误] 找不到测试文件
    pause
    exit /b 1
)

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装
    echo 尝试直接打开文件...
    start "" "holland_test_preview.html"
    pause
    exit /b 1
)

echo [1/3] 启动服务器...
start /B cmd /c "python -m http.server 8000"

echo [2/3] 等待服务器就绪...
timeout /t 4 /nobreak >nul

echo [3/3] 打开浏览器...
start http://localhost:8000/holland_test_preview.html

echo.
echo [完成] 服务器已启动，浏览器应该已打开
echo.
echo 如果浏览器没有打开，请手动访问：
echo http://localhost:8000/holland_test_preview.html
echo.
echo 注意：服务器窗口在后台运行
echo 要停止服务器，请关闭此窗口或按 Ctrl+C
echo.
pause


