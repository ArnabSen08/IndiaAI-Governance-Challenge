# GitHub Repository Setup Script
# Run this script after creating the repository on GitHub

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
    
    [Parameter(Mandatory=$false)]
    [string]$GitHubUsername = "ArnabSen08"
)

Write-Host "Setting up GitHub repository: $RepoName" -ForegroundColor Green

# Add remote origin
$remoteUrl = "https://github.com/$GitHubUsername/$RepoName.git"
Write-Host "Adding remote: $remoteUrl" -ForegroundColor Yellow
git remote add origin $remoteUrl

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

# Enable GitHub Pages via API (requires GitHub token)
Write-Host "`nTo enable GitHub Pages, run:" -ForegroundColor Cyan
Write-Host "gh api repos/$GitHubUsername/$RepoName/pages -X POST -f source=@{branch=`"main`",path=`"/`"}" -ForegroundColor Yellow

Write-Host "`nOr enable it manually:" -ForegroundColor Cyan
Write-Host "1. Go to: https://github.com/$GitHubUsername/$RepoName/settings/pages" -ForegroundColor Yellow
Write-Host "2. Select 'main' branch as source" -ForegroundColor Yellow
Write-Host "3. Select '/ (root)' as folder" -ForegroundColor Yellow
Write-Host "4. Click Save" -ForegroundColor Yellow

Write-Host "`nYour site will be available at:" -ForegroundColor Green
Write-Host "https://$GitHubUsername.github.io/$RepoName/" -ForegroundColor Cyan
