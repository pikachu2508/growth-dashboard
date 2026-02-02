# 自动发布脚本
$ErrorActionPreference = "Stop"

Write-Host "🚀 开始自动发布流程..." -ForegroundColor Cyan

# 1. 添加所有变更
Write-Host "📦 添加文件变更..."
git add .

# 2. 提交变更
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMsg = "Auto-publish: $timestamp"
Write-Host "💾 提交变更: $commitMsg"
git commit -m "$commitMsg"

# 3. 推送到远程
Write-Host "☁️ 推送到 GitHub..."
git push origin main

Write-Host "✅ 发布成功！" -ForegroundColor Green
Write-Host "🌍 访问地址: https://pikachu2508.github.io/growth-dashboard/" -ForegroundColor Green