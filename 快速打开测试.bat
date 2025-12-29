@echo off
chcp 65001 >nul
echo ========================================
echo 正在打开霍兰德测试页面...
echo ========================================
echo.

set "filePath=%~dp0holland_test_preview.html"

if exist "%filePath%" (
    echo 找到文件: %filePath%
    echo.
    echo 正在使用默认浏览器打开...
    start "" "%filePath%"
    echo.
    echo ✅ 已打开测试页面！
) else (
    echo ❌ 错误：找不到文件 holland_test_preview.html
    echo.
    echo 请确保此批处理文件与 holland_test_preview.html 在同一目录下
    pause
)

timeout /t 3 >nul

