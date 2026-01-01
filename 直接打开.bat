@echo off
chcp 65001 >nul
echo ========================================
echo 尝试直接打开测试页面
echo ========================================
echo.

set "filePath=%~dp0holland_test_preview.html"

if not exist "%filePath%" (
    echo ❌ 错误：找不到文件
    echo    文件路径: %filePath%
    echo.
    pause
    exit /b 1
)

echo 找到文件: %filePath%
echo.
echo 正在尝试使用默认程序打开...
echo.

REM 方法1: 使用 start 命令
start "" "%filePath%"

REM 等待一下，检查是否成功
timeout /t 2 >nul

REM 方法2: 如果方法1失败，尝试使用浏览器
echo 如果浏览器没有打开，请尝试：
echo 1. 右键点击 holland_test_preview.html
echo 2. 选择"打开方式"
echo 3. 选择浏览器（Chrome、Edge等）
echo.
echo 或者使用"启动服务器.bat"来通过本地服务器打开
echo.

pause


