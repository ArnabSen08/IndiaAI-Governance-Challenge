# Script to push using Personal Access Token
# Usage: .\push_with_token.ps1 -Token "your_github_token_here"

param(
    [Parameter(Mandatory=$false)]
    [string]$Token
)

Write-Host "Attempting to push to GitHub..." -ForegroundColor Green

# Clear all proxy settings
$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""
$env:http_proxy = ""
$env:https_proxy = ""
$env:NO_PROXY = "*"

# If token provided, use it in URL
if ($Token) {
    Write-Host "Using Personal Access Token for authentication..." -ForegroundColor Yellow
    git remote set-url origin "https://${Token}@github.com/ArnabSen08/publication-assistant.git"
    git push -u origin main
    # Reset to normal URL after push
    git remote set-url origin "https://github.com/ArnabSen08/publication-assistant.git"
} else {
    Write-Host "No token provided. Attempting push with stored credentials..." -ForegroundColor Yellow
    Write-Host "If this fails, run: .\push_with_token.ps1 -Token 'your_token'" -ForegroundColor Cyan
    
    # Try with credential helper
    git config --local credential.helper manager
    git push -u origin main
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "Repository: https://github.com/ArnabSen08/publication-assistant" -ForegroundColor Cyan
} else {
    Write-Host "`n✗ Push failed. Try one of these:" -ForegroundColor Red
    Write-Host "1. Get a Personal Access Token from: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "2. Run: .\push_with_token.ps1 -Token 'your_token_here'" -ForegroundColor White
    Write-Host "3. Use GitHub Desktop or VS Code" -ForegroundColor White
}
