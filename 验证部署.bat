@echo off
chcp 65001 >nul
echo ========================================
echo 验证 Vercel 部署
echo ========================================
echo.

echo [1/3] 检查 GitHub 提交状态...
git log --oneline -1
echo.

echo [2/3] 检查远程仓库状态...
git fetch origin
git status
echo.

echo [3/3] 部署验证说明
echo.
echo ========================================
echo 部署验证步骤
echo ========================================
echo.
echo 1. 访问 Vercel 控制台：
echo    https://vercel.com/dashboard
echo.
echo 2. 找到项目 "holland-test"
echo.
echo 3. 查看 "Deployments" 标签
echo    最新部署应该显示为：
echo    - "Building" (正在构建)
echo    - "Ready" (部署成功)
echo    - "Error" (部署失败)
echo.
echo 4. 等待 1-2 分钟完成部署
echo.
echo 5. 访问网站验证：
echo    https://holland-test.snowshadow.com.cn/
echo.
echo ========================================
echo 如果部署失败
echo ========================================
echo.
echo 1. 在 Vercel 控制台查看部署日志
echo 2. 检查错误信息
echo 3. 参考 "检查部署状态.md" 文档
echo 4. 或使用 "触发Vercel部署.bat" 重新部署
echo.
echo ========================================
pause

