# Complete GitHub Setup Script
# Run this after fixing GitHub authentication/proxy issues

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Repository Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if remote exists
$hasRemote = git remote | Select-String -Pattern "origin"
if ($hasRemote) {
    Write-Host "Remote 'origin' already exists. Updating..." -ForegroundColor Yellow
    $currentRemote = git remote get-url origin
    Write-Host "Current remote: $currentRemote" -ForegroundColor Gray
} else {
    Write-Host "No remote configured. Let's set it up..." -ForegroundColor Yellow
}

# Try to get GitHub username
Write-Host "`nAttempting to get GitHub username..." -ForegroundColor Green
try {
    $username = gh api user --jq .login 2>$null
    if ($username) {
        Write-Host "GitHub username: $username" -ForegroundColor Green
        $repoUrl = "https://github.com/$username/publication-assistant.git"
    } else {
        throw "Could not get username"
    }
} catch {
    Write-Host "Could not automatically detect username." -ForegroundColor Yellow
    $username = Read-Host "Please enter your GitHub username"
    $repoUrl = "https://github.com/$username/publication-assistant.git"
}

# Create repository
Write-Host "`nCreating GitHub repository..." -ForegroundColor Green
try {
    gh repo create publication-assistant --public --source=. --remote=origin --description="Multi-agent system for improving AI/ML project publications using LangGraph orchestration" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Repository created successfully!" -ForegroundColor Green
    } else {
        throw "Repository creation failed"
    }
} catch {
    Write-Host "Could not create repository automatically." -ForegroundColor Yellow
    Write-Host "Please create it manually at: https://github.com/new" -ForegroundColor Cyan
    Write-Host "Then run:" -ForegroundColor Cyan
    Write-Host "  git remote add origin $repoUrl" -ForegroundColor White
    Write-Host "  git push -u origin main" -ForegroundColor White
    exit 1
}

# Push code
Write-Host "`nPushing code to GitHub..." -ForegroundColor Green
git push -u origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Code pushed successfully!" -ForegroundColor Green
} else {
    Write-Host "Push failed. Please check your authentication." -ForegroundColor Red
    exit 1
}

# Enable GitHub Pages
Write-Host "`nEnabling GitHub Pages..." -ForegroundColor Green
try {
    gh api repos/$username/publication-assistant/pages -X POST -f source='{"branch":"main","path":"/docs"}' 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ GitHub Pages enabled!" -ForegroundColor Green
    } else {
        Write-Host "Could not enable Pages automatically." -ForegroundColor Yellow
        Write-Host "Enable manually: Settings > Pages > Source: main branch, /docs folder" -ForegroundColor Cyan
    }
} catch {
    Write-Host "Enable Pages manually: Settings > Pages > Source: main branch, /docs folder" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Repository: https://github.com/$username/publication-assistant" -ForegroundColor Cyan
Write-Host "Pages URL: https://$username.github.io/publication-assistant/" -ForegroundColor Cyan
Write-Host ""
