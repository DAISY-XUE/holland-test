@echo off
chcp 65001 >nul
title 启动霍兰德测试服务器
color 0A

echo.
echo ========================================
echo   启动霍兰德测试服务器
echo ========================================
echo.

REM 检查文件是否存在（使用相对路径）
if not exist "holland_test_preview.html" (
    echo [错误] 找不到测试文件！
    echo.
    echo 请确保 holland_test_preview.html 在当前目录
    echo 当前目录: %CD%
    echo.
    pause
    exit /b 1
)

echo [检查] 测试文件存在
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装或未添加到 PATH
    echo.
    echo 解决方案：
    echo 1. 安装 Python 3: https://www.python.org/downloads/
    echo 2. 安装时勾选 "Add Python to PATH"
    echo.
    echo 或者尝试直接打开文件：
    echo   右键点击 holland_test_preview.html
    echo   选择"打开方式" → 选择浏览器
    echo.
    pause
    exit /b 1
)

echo [检查] Python 已安装
python --version
echo.

REM 尝试启动服务器
echo [启动] 正在启动服务器...
echo.

REM 先启动服务器（在后台）
start /B python -m http.server 8000

REM 等待服务器启动
echo [等待] 等待服务器启动...
timeout /t 3 /nobreak >nul

REM 检查服务器是否启动成功
netstat -ano | findstr ":8000" >nul
if errorlevel 1 (
    echo [错误] 服务器启动失败
    echo.
    echo 尝试备用方案：直接打开文件
    echo.
    start "" "holland_test_preview.html"
    echo [完成] 已尝试直接打开文件
    echo.
    echo 如果文件没有打开，请手动操作：
    echo 1. 右键点击 holland_test_preview.html
    echo 2. 选择"打开方式" → 选择浏览器
    echo.
    pause
    exit /b 1
)

echo [成功] 服务器已启动
echo.
echo [打开] 正在打开浏览器...
start http://localhost:8000/holland_test_preview.html

echo.
echo ========================================
echo 服务器运行中
echo ========================================
echo.
echo 服务器地址: http://localhost:8000
echo 测试页面: http://localhost:8000/holland_test_preview.html
echo.
echo 提示：
echo - 浏览器应该已经自动打开
echo - 如果浏览器没有打开，请手动访问上面的地址
echo - 关闭此窗口会停止服务器
echo - 按 Ctrl+C 也可以停止服务器
echo.
echo ========================================
echo.

REM 保持窗口打开，运行服务器
python -m http.server 8000

if errorlevel 1 (
    echo.
    echo [错误] 服务器启动失败
    echo.
    echo 可能的原因：
    echo 1. 端口 8000 被占用
    echo 2. 权限问题
    echo.
    echo 请尝试：
    echo 1. 关闭其他使用端口 8000 的程序
    echo 2. 或者直接打开文件（右键 → 打开方式 → 浏览器）
    echo.
    pause
)

