# PowerShell script to verify Ready Tensor repositories are accessible

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Ready Tensor Repositories - Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repos = @(
    "agentic-ai-production-system",
    "ready-tensor",
    "publication-assistant"
)

$allGood = $true

foreach ($repo in $repos) {
    Write-Host "Checking: $repo" -ForegroundColor Yellow
    
    # Check if repository exists and is public
    $repoInfo = gh repo view "ArnabSen08/$repo" --json visibility,url,isPrivate 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        $repoData = $repoInfo | ConvertFrom-Json
        
        if ($repoData.isPrivate -eq $false) {
            Write-Host "  ✓ Repository exists and is PUBLIC" -ForegroundColor Green
            Write-Host "    URL: $($repoData.url)" -ForegroundColor Gray
        } else {
            Write-Host "  ✗ Repository exists but is PRIVATE!" -ForegroundColor Red
            Write-Host "    Run: gh repo edit ArnabSen08/$repo --visibility public" -ForegroundColor Yellow
            $allGood = $false
        }
        
        # Check GitHub Pages
        $pagesInfo = gh api "repos/ArnabSen08/$repo/pages" 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pagesData = $pagesInfo | ConvertFrom-Json
            Write-Host "  ✓ GitHub Pages enabled" -ForegroundColor Green
            Write-Host "    URL: $($pagesData.html_url)" -ForegroundColor Gray
        } else {
            Write-Host "  ✗ GitHub Pages not enabled" -ForegroundColor Red
            Write-Host "    Enable at: https://github.com/ArnabSen08/$repo/settings/pages" -ForegroundColor Yellow
            $allGood = $false
        }
    } else {
        Write-Host "  ✗ Repository does not exist!" -ForegroundColor Red
        Write-Host "    Create it by running: .\setup-ready-tensor-repos.ps1" -ForegroundColor Yellow
        $allGood = $false
    }
    
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "✓ All repositories are properly configured!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now update your Ready Tensor publications with:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Repository URLs:" -ForegroundColor Yellow
    Write-Host "  https://github.com/ArnabSen08/agentic-ai-production-system" -ForegroundColor White
    Write-Host "  https://github.com/ArnabSen08/ready-tensor" -ForegroundColor White
    Write-Host "  https://github.com/ArnabSen08/publication-assistant" -ForegroundColor White
    Write-Host ""
    Write-Host "GitHub Pages URLs:" -ForegroundColor Yellow
    Write-Host "  https://arnabsen08.github.io/agentic-ai-production-system/" -ForegroundColor White
    Write-Host "  https://arnabsen08.github.io/ready-tensor/" -ForegroundColor White
    Write-Host "  https://arnabsen08.github.io/publication-assistant/" -ForegroundColor White
} else {
    Write-Host "✗ Some issues found. Please fix them before updating publications." -ForegroundColor Red
}
Write-Host "========================================" -ForegroundColor Cyan
