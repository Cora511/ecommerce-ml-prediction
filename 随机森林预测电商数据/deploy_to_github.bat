@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🚀 电商数据科学项目 - GitHub部署脚本
echo ========================================
echo.

:: 检查Git是否安装
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未检测到Git，请先安装Git
    echo 下载地址：https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git已安装
echo.

:: 获取用户输入
set /p GITHUB_USERNAME="请输入你的GitHub用户名: "
if "%GITHUB_USERNAME%"=="" (
    echo ❌ 错误：GitHub用户名不能为空
    pause
    exit /b 1
)

set /p REPO_NAME="请输入仓库名称 [默认: ecommerce-ml-prediction]: "
if "%REPO_NAME%"=="" set REPO_NAME=ecommerce-ml-prediction

echo.
echo 📋 部署信息确认：
echo    GitHub用户名: %GITHUB_USERNAME%
echo    仓库名称: %REPO_NAME%
echo    项目目录: %CD%
echo.
set /p CONFIRM="确认部署？(y/N): "
if /i not "%CONFIRM%"=="y" (
    echo 🚫 部署已取消
    pause
    exit /b 0
)

echo.
echo 🔄 开始部署...
echo.

:: 初始化Git仓库
echo 📁 初始化Git仓库...
git init
if %errorlevel% neq 0 (
    echo ❌ Git初始化失败
    pause
    exit /b 1
)

:: 添加所有文件
echo 📦 添加项目文件...
git add .
if %errorlevel% neq 0 (
    echo ❌ 文件添加失败
    pause
    exit /b 1
)

:: 提交文件
echo 💾 提交文件到本地仓库...
git commit -m "🎯 初始提交：完整的电商数据科学项目

✨ 功能特性：
- 🤖 随机森林机器学习预测模型
- 📊 专业投资人报告（莫兰迪紫色系设计）
- 📈 交互式数据可视化仪表板
- 💾 MySQL数据库集成
- 📱 响应式Web界面
- 🎨 高端UI/UX设计

🚀 技术栈：
- Python 3.8+ (scikit-learn, pandas, numpy)
- 数据可视化 (matplotlib, seaborn, plotly)
- Web技术 (HTML5, CSS3, JavaScript)
- 数据库 (MySQL, SQLAlchemy)

📋 项目结构完整，包含：
- 完整的源代码和模型文件
- 专业的文档和使用指南
- 自动化部署配置
- 开源协议和贡献指南"
if %errorlevel% neq 0 (
    echo ❌ 文件提交失败
    pause
    exit /b 1
)

:: 设置主分支
echo 🌿 设置主分支...
git branch -M main

:: 添加远程仓库
echo 🔗 添加远程仓库...
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
if %errorlevel% neq 0 (
    echo ❌ 远程仓库添加失败
    echo 💡 请确保已在GitHub上创建了仓库：%REPO_NAME%
    echo 🌐 GitHub创建仓库地址：https://github.com/new
    pause
    exit /b 1
)

:: 推送到GitHub
echo 🚀 推送到GitHub...
git push -u origin main
if %errorlevel% neq 0 (
    echo ❌ 推送失败
    echo 💡 可能的原因：
    echo    1. 仓库不存在，请先在GitHub创建仓库
    echo    2. 没有推送权限，请检查GitHub认证
    echo    3. 网络连接问题
    echo.
    echo 🔧 手动推送命令：
    echo    git push -u origin main
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🎉 部署成功！
echo ========================================
echo.
echo 📋 你的项目信息：
echo    🌐 仓库地址：https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo    🏠 项目主页：https://%GITHUB_USERNAME%.github.io/%REPO_NAME%/
echo    📊 投资人报告：https://%GITHUB_USERNAME%.github.io/%REPO_NAME%/reports/investor_report/投资人专业报告.html
echo    📈 数据仪表板：https://%GITHUB_USERNAME%.github.io/%REPO_NAME%/charts/交互式仪表板.html
echo.
echo 📝 下一步操作：
echo    1. 访问GitHub仓库设置GitHub Pages
echo    2. 等待5-10分钟让GitHub Pages部署完成
echo    3. 访问上面的链接查看你的项目
echo.
echo 🎯 GitHub Pages设置步骤：
echo    1. 打开：https://github.com/%GITHUB_USERNAME%/%REPO_NAME%/settings/pages
echo    2. Source选择：Deploy from a branch
echo    3. Branch选择：main
echo    4. Folder选择：/ (root)
echo    5. 点击Save
echo.
echo 🚀 恭喜！你的电商数据科学项目现在可以在线访问了！
echo.
pause