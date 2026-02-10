# Script to push code and enable GitHub Pages
# Run this script to complete the setup

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Pushing Code and Enabling GitHub Pages" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Try to push code
Write-Host "Step 1: Pushing code to GitHub..." -ForegroundColor Green
Write-Host "If this fails due to proxy, please use GitHub Desktop or VS Code to push manually." -ForegroundColor Yellow
Write-Host ""

# Clear proxy environment variables
$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""
$env:http_proxy = ""
$env:https_proxy = ""

# Try pushing
git push -u origin main
$pushSuccess = $LASTEXITCODE -eq 0

if (-not $pushSuccess) {
    Write-Host "`nPush failed. Please try one of these options:" -ForegroundColor Yellow
    Write-Host "1. Use GitHub Desktop: Open the repo and click 'Push origin'" -ForegroundColor White
    Write-Host "2. Use VS Code: Open the repo and use the Source Control panel to push" -ForegroundColor White
    Write-Host "3. Fix proxy settings and try again" -ForegroundColor White
    Write-Host "`nAfter pushing, run this script again to enable Pages." -ForegroundColor Cyan
    exit 1
}

Write-Host "✓ Code pushed successfully!" -ForegroundColor Green
Write-Host ""

# Step 2: Enable GitHub Pages
Write-Host "Step 2: Enabling GitHub Pages..." -ForegroundColor Green

# Create JSON config
$pagesConfig = @{
    source = @{
        branch = "main"
        path = "/docs"
    }
} | ConvertTo-Json -Compress

# Write to temp file
$tempFile = "pages_config_temp.json"
$pagesConfig | Out-File -FilePath $tempFile -Encoding utf8

try {
    gh api repos/ArnabSen08/publication-assistant/pages -X POST --input $tempFile
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ GitHub Pages enabled successfully!" -ForegroundColor Green
        Write-Host "`nYour site will be available at:" -ForegroundColor Cyan
        Write-Host "https://arnabsen08.github.io/publication-assistant/" -ForegroundColor Yellow
        Write-Host "`n(It may take 2-5 minutes to deploy)" -ForegroundColor Gray
    } else {
        Write-Host "Could not enable Pages via API. Enable manually:" -ForegroundColor Yellow
        Write-Host "1. Go to: https://github.com/ArnabSen08/publication-assistant/settings/pages" -ForegroundColor White
        Write-Host "2. Source: Branch 'main', Folder '/docs'" -ForegroundColor White
        Write-Host "3. Click Save" -ForegroundColor White
    }
} catch {
    Write-Host "Error enabling Pages: $_" -ForegroundColor Red
    Write-Host "Enable manually at: https://github.com/ArnabSen08/publication-assistant/settings/pages" -ForegroundColor Yellow
} finally {
    if (Test-Path $tempFile) {
        Remove-Item $tempFile
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
