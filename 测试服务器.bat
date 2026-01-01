@echo off
chcp 65001 >nul
echo ========================================
echo 测试服务器连接
echo ========================================
echo.

echo 检查 Python 安装...
python --version
if errorlevel 1 (
    echo [错误] Python 未安装或未添加到 PATH
    pause
    exit /b 1
)

echo.
echo 检查文件是否存在...
if exist "holland_test_preview.html" (
    echo [OK] 找到 holland_test_preview.html
) else (
    echo [错误] 找不到 holland_test_preview.html
    pause
    exit /b 1
)

echo.
echo 检查端口占用情况...
echo 正在检查端口 8000, 8080, 8888...
netstat -ano | findstr ":8000 :8080 :8888" >nul
if errorlevel 1 (
    echo [OK] 常用端口可用
) else (
    echo [警告] 部分端口可能被占用，脚本会自动尝试其他端口
)

echo.
echo ========================================
echo 测试完成，准备启动服务器...
echo ========================================
echo.
pause

call "启动服务器.bat"


