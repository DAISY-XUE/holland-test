@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   最简单的方法 - 直接打开文件
echo ========================================
echo.

REM 方法1: 直接打开文件
echo [方法1] 尝试直接打开文件...
start "" "holland_test_preview.html"
timeout /t 2 >nul

echo.
echo 如果文件已经在浏览器中打开，说明成功了！
echo.
echo 如果文件没有打开，请尝试：
echo 1. 右键点击 holland_test_preview.html
echo 2. 选择"打开方式"
echo 3. 选择浏览器（Chrome、Edge、Firefox等）
echo 4. 勾选"始终使用此应用打开.html文件"
echo.
pause

