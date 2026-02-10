# PowerShell script for GitHub repository setup

Write-Host "Setting up GitHub repository..." -ForegroundColor Green

# Check if already has remote
$hasRemote = git remote | Select-String -Pattern "origin"
if ($hasRemote) {
    Write-Host "Remote 'origin' already exists" -ForegroundColor Yellow
} else {
    Write-Host "Please create a GitHub repository first, then run:" -ForegroundColor Cyan
    Write-Host "  git remote add origin https://github.com/YOUR_USERNAME/publication-assistant.git" -ForegroundColor White
    Write-Host "  git branch -M main" -ForegroundColor White
    Write-Host "  git push -u origin main" -ForegroundColor White
}

# Check GitHub CLI
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "`nAttempting to enable GitHub Pages..." -ForegroundColor Green
    gh api repos/:owner/:repo/pages -X POST -f source='{"branch":"main","path":"/docs"}' 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Note: GitHub Pages can be enabled manually in repository settings" -ForegroundColor Yellow
        Write-Host "  1. Go to repository Settings > Pages" -ForegroundColor White
        Write-Host "  2. Select 'main' branch as source" -ForegroundColor White
        Write-Host "  3. Select '/docs' folder (or root)" -ForegroundColor White
    }
} else {
    Write-Host "`nGitHub CLI not found. Enable Pages manually:" -ForegroundColor Yellow
    Write-Host "  1. Go to repository Settings > Pages" -ForegroundColor White
    Write-Host "  2. Select 'main' branch as source" -ForegroundColor White
    Write-Host "  3. Select '/docs' folder (or root)" -ForegroundColor White
}

Write-Host "`nSetup complete!" -ForegroundColor Green
