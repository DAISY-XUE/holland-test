@echo off
chcp 65001 >nul
echo ========================================
echo 诊断工具 - 检查环境配置
echo ========================================
echo.

echo [1/5] 检查 Python 安装...
python --version 2>nul
if errorlevel 1 (
    echo    [失败] Python 未安装或未添加到 PATH
    echo    解决方案: 安装 Python 3 并添加到系统 PATH
    set PYTHON_OK=0
) else (
    python --version
    echo    [成功] Python 已安装
    set PYTHON_OK=1
)

echo.
echo [2/5] 检查测试文件是否存在...
if exist "holland_test_preview.html" (
    echo    [成功] 找到 holland_test_preview.html
    set FILE_OK=1
) else (
    echo    [失败] 找不到 holland_test_preview.html
    echo    请确保文件在当前目录下
    set FILE_OK=0
)

echo.
echo [3/5] 检查 Python 脚本是否存在...
if exist "启动本地服务器.py" (
    echo    [成功] 找到 启动本地服务器.py
    set SCRIPT_OK=1
) else (
    echo    [警告] 找不到 启动本地服务器.py
    echo    可以使用 Python 内置服务器代替（不影响使用）
    set SCRIPT_OK=1
)

echo.
echo [4/5] 检查端口占用情况...
netstat -ano | findstr ":8000" >nul
if errorlevel 1 (
    echo    [可用] 端口 8000 可用
    set PORT_8000=1
) else (
    echo    [占用] 端口 8000 被占用
    echo    脚本会自动尝试其他端口 (8080, 8888, 3000, 5000)
    set PORT_8000=0
)

echo.
echo [5/5] 测试 Python 脚本语法...
if %PYTHON_OK%==1 (
    python -m py_compile "启动本地服务器.py" 2>nul
    if errorlevel 1 (
        echo    [失败] Python 脚本有语法错误
        set SYNTAX_OK=0
    ) else (
        echo    [成功] Python 脚本语法正确
        set SYNTAX_OK=1
    )
) else (
    echo    [跳过] 无法检查（Python 未安装）
    set SYNTAX_OK=0
)

echo.
echo ========================================
echo 诊断结果总结
echo ========================================
echo.

if %PYTHON_OK%==1 if %FILE_OK%==1 if %SCRIPT_OK%==1 (
    echo [总体状态] 环境配置正常，可以启动服务器
    echo.
    echo 建议操作：
    echo 1. 双击 "启动服务器.bat" 启动服务器
    echo 2. 或者运行: python "启动本地服务器.py"
    echo.
) else (
    echo [总体状态] 发现问题，需要修复
    echo.
    if %PYTHON_OK%==0 (
        echo [需要修复] Python 未安装
        echo   下载地址: https://www.python.org/downloads/
        echo   安装时请勾选 "Add Python to PATH"
        echo.
    )
    if %FILE_OK%==0 (
        echo [需要修复] 测试文件不存在
        echo   请确保 holland_test_preview.html 在当前目录
        echo.
    )
    if %SCRIPT_OK%==0 (
        echo [需要修复] Python 脚本不存在
        echo   请确保 启动本地服务器.py 在当前目录
        echo.
    )
)

echo ========================================
pause

