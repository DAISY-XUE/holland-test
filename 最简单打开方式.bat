@echo off
chcp 65001 >nul
echo ========================================
echo 最简单的打开方式
echo ========================================
echo.

REM 方法1: 尝试直接打开文件
echo [方法1] 尝试直接打开文件...
start "" "holland_test_preview.html" 2>nul
timeout /t 2 >nul

REM 检查是否成功（简单检查）
tasklist | findstr /i "chrome.exe msedge.exe firefox.exe" >nul
if not errorlevel 1 (
    echo [成功] 文件已在浏览器中打开
    echo.
    echo 如果看到测试页面，说明成功了！
    echo 如果没有看到，请尝试方法2
    echo.
    pause
    exit /b 0
)

echo [方法1失败] 继续尝试方法2...
echo.

REM 方法2: 使用Python简单服务器
echo [方法2] 使用Python启动简单服务器...
python -m http.server 8000 >nul 2>&1 &
timeout /t 1 >nul

REM 尝试打开浏览器
start http://localhost:8000/holland_test_preview.html
timeout /t 2 >nul

echo [方法2] 服务器已启动
echo.
echo 如果浏览器已打开，请访问:
echo http://localhost:8000/holland_test_preview.html
echo.
echo 按 Ctrl+C 可以停止服务器（在服务器窗口）
echo.
echo 提示: 如果方法2也失败，请运行 "诊断问题.bat" 检查环境
echo.
pause


