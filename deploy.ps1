# deploy.ps1 — 将 md2html_batch 推送到 GitHub
# 仓库: https://github.com/lcfactorization/md2html-batch
# 用法: .\deploy.ps1  或  .\deploy.ps1 -Message "自定义提交信息"

param(
    [string]$Message = "Update md2html-batch",
    [string]$Branch = "main",
    [string]$RepoUrl = "https://github.com/lcfactorization/md2html-batch.git"
)

$ErrorActionPreference = "Stop"
$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " md2html-batch 部署脚本" -ForegroundColor Cyan
Write-Host " 仓库: $RepoUrl" -ForegroundColor Cyan
Write-Host " 分支: $Branch" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Set-Location $RepoDir

# [1/5] 初始化
Write-Host "[1/5] 初始化 Git 仓库..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    git remote add origin $RepoUrl
} else {
    Write-Host "  Git 仓库已存在，跳过初始化"
}
# 确保 remote URL 正确
$currentUrl = git remote get-url origin 2>$null
if ($currentUrl -ne $RepoUrl) {
    Write-Host "  更新 remote URL: $currentUrl -> $RepoUrl"
    git remote set-url origin $RepoUrl
}

# [2/5] 添加文件
Write-Host ""
Write-Host "[2/5] 添加文件..." -ForegroundColor Yellow
git add md2html_batch.py md2html.bat README.md README.html

# [3/5] 查看变更
Write-Host ""
Write-Host "[3/5] 查看变更..." -ForegroundColor Yellow
git status

# [4/5] 提交
Write-Host ""
Write-Host "[4/5] 提交: $Message" -ForegroundColor Yellow
git commit -m $Message

# [5/5] 推送
Write-Host ""
Write-Host "[5/5] 推送到 $Branch..." -ForegroundColor Yellow
git push -u origin $Branch

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[成功] 已推送到 $RepoUrl" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[失败] 推送出错，请检查网络或认证" -ForegroundColor Red
}
