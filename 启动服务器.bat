@echo off
chcp 65001 >nul
echo ========================================
echo 启动本地服务器打开测试页面
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python！
    echo.
    echo 请确保：
    echo 1. 已安装 Python 3
    echo 2. Python 已添加到系统 PATH
    echo.
    echo 下载 Python: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo 正在启动服务器...
echo 提示：如果端口被占用，会自动尝试其他端口
echo.

python "启动本地服务器.py"

if errorlevel 1 (
    echo.
    echo [错误] 启动失败！
    echo.
    echo 可能的原因：
    echo 1. Python 脚本执行出错
    echo 2. 所有常用端口都被占用
    echo 3. 文件路径问题
    echo.
    echo 请尝试：
    echo 1. 检查 holland_test_preview.html 文件是否存在
    echo 2. 关闭其他可能占用端口的程序
    echo 3. 查看上方的错误信息
    echo.
    pause
)

