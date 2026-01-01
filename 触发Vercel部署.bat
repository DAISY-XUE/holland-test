@echo off
chcp 65001 >nul
echo ========================================
echo 触发 Vercel 部署
echo ========================================
echo.

echo [1/3] 检查 Git 状态...
git status --short
echo.

echo [2/3] 创建空提交以触发部署...
git commit --allow-empty -m "Trigger Vercel deployment - Update test page"

if errorlevel 1 (
    echo [错误] 提交失败
    pause
    exit /b 1
)

echo [成功] 提交已创建
echo.

echo [3/3] 推送到 GitHub...
git push origin main

if errorlevel 1 (
    echo [错误] 推送失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 完成！
echo ========================================
echo.
echo [成功] 更改已推送到 GitHub
echo.
echo Vercel 应该会自动检测到更改并开始部署
echo.
echo 下一步：
echo 1. 访问 Vercel 控制台: https://vercel.com/dashboard
echo 2. 找到项目 "holland-test"
echo 3. 查看最新的部署状态
echo 4. 等待 1-2 分钟完成部署
echo 5. 访问: https://holland-test.snowshadow.com.cn/
echo.
pause

