# Enable GitHub Pages via GitHub API
# Requires: GitHub Personal Access Token with repo permissions

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
    
    [Parameter(Mandatory=$false)]
    [string]$GitHubUsername = "ArnabSen08",
    
    [Parameter(Mandatory=$false)]
    [string]$Token = $env:GITHUB_TOKEN
)

if (-not $Token) {
    Write-Host "Error: GitHub token required!" -ForegroundColor Red
    Write-Host "Set GITHUB_TOKEN environment variable or pass -Token parameter" -ForegroundColor Yellow
    Write-Host "`nTo create a token:" -ForegroundColor Cyan
    Write-Host "1. Go to: https://github.com/settings/tokens" -ForegroundColor Yellow
    Write-Host "2. Generate new token (classic)" -ForegroundColor Yellow
    Write-Host "3. Select 'repo' scope" -ForegroundColor Yellow
    Write-Host "4. Copy the token and run:" -ForegroundColor Yellow
    Write-Host "   `$env:GITHUB_TOKEN = 'your-token-here'" -ForegroundColor Cyan
    Write-Host "   .\enable-pages.ps1 -RepoName '$RepoName'" -ForegroundColor Cyan
    exit 1
}

$headers = @{
    "Authorization" = "token $Token"
    "Accept" = "application/vnd.github.v3+json"
}

$body = @{
    source = @{
        branch = "main"
        path = "/"
    }
} | ConvertTo-Json

$url = "https://api.github.com/repos/$GitHubUsername/$RepoName/pages"

Write-Host "Enabling GitHub Pages for $GitHubUsername/$RepoName..." -ForegroundColor Green

try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body -ContentType "application/json"
    Write-Host "`nGitHub Pages enabled successfully!" -ForegroundColor Green
    Write-Host "Your site will be available at:" -ForegroundColor Cyan
    Write-Host "https://$GitHubUsername.github.io/$RepoName/" -ForegroundColor Yellow
    Write-Host "`nNote: It may take a few minutes for the site to be deployed." -ForegroundColor Yellow
} catch {
    Write-Host "`nError enabling GitHub Pages:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.Exception.Response.StatusCode -eq 404) {
        Write-Host "`nRepository not found. Make sure:" -ForegroundColor Yellow
        Write-Host "1. Repository exists: https://github.com/$GitHubUsername/$RepoName" -ForegroundColor Yellow
        Write-Host "2. Repository is public (required for free GitHub Pages)" -ForegroundColor Yellow
    } elseif ($_.Exception.Response.StatusCode -eq 422) {
        Write-Host "`nGitHub Pages might already be enabled." -ForegroundColor Yellow
        Write-Host "Check: https://github.com/$GitHubUsername/$RepoName/settings/pages" -ForegroundColor Cyan
    }
}
