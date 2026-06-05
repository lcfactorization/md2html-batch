@echo off
chcp 65001 >nul 2>&1
REM ============================================================
REM  deploy.bat — 将 md2html_batch 推送到 GitHub
REM  仓库: https://github.com/lcfactorization/md2html-batch
REM  用法: 双击运行，或在 cmd 中执行
REM ============================================================

set REPO_DIR=%~dp0
set REPO_URL=https://github.com/lcfactorization/md2html-batch.git
set BRANCH=main

echo ============================================
echo  md2html-batch 部署脚本
echo  仓库: %REPO_URL%
echo  分支: %BRANCH%
echo ============================================
echo.

cd /d "%REPO_DIR%"

REM 检查 git 是否已初始化
if not exist ".git" (
    echo [1/5] 初始化 Git 仓库...
    git init
    git remote add origin %REPO_URL%
) else (
    echo [1/5] Git 仓库已存在，跳过初始化
)

REM 检查 remote 是否正确
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    git remote add origin %REPO_URL%
) else (
    for /f "tokens=*" %%i in ('git remote get-url origin') do set CURRENT_URL=%%i
    if not "%CURRENT_URL%"=="%REPO_URL%" (
        echo 更新 remote URL: %CURRENT_URL% -^> %REPO_URL%
        git remote set-url origin %REPO_URL%
    )
)

echo.
echo [2/5] 添加文件...
git add md2html_batch.py md2html.bat README.md README.html

echo.
echo [3/5] 查看变更...
git status

echo.
echo [4/5] 提交...
git commit -m "Update md2html-batch"

echo.
echo [5/5] 推送到 %BRANCH%...
git push -u origin %BRANCH%

echo.
if errorlevel 1 (
    echo [失败] 推送出错，请检查网络或认证
) else (
    echo [成功] 已推送到 %REPO_URL%
)

echo.
pause
