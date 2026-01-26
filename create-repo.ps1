# Create GitHub Repository and Setup Script
# This script creates the repository via GitHub API

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
    
    [Parameter(Mandatory=$false)]
    [string]$GitHubUsername = "ArnabSen08",
    
    [Parameter(Mandatory=$false)]
    [string]$Token = $env:GITHUB_TOKEN,
    
    [Parameter(Mandatory=$false)]
    [switch]$Public = $true
)

if (-not $Token) {
    Write-Host "GitHub Personal Access Token required!" -ForegroundColor Red
    Write-Host "`nTo create a token:" -ForegroundColor Cyan
    Write-Host "1. Go to: https://github.com/settings/tokens/new" -ForegroundColor Yellow
    Write-Host "2. Name: 'Repository Management'" -ForegroundColor Yellow
    Write-Host "3. Select scopes: 'repo' (full control)" -ForegroundColor Yellow
    Write-Host "4. Generate token and copy it" -ForegroundColor Yellow
    Write-Host "`nThen run:" -ForegroundColor Cyan
    Write-Host "`$env:GITHUB_TOKEN = 'your-token-here'" -ForegroundColor Yellow
    Write-Host ".\create-repo.ps1 -RepoName '$RepoName'" -ForegroundColor Yellow
    exit 1
}

$headers = @{
    "Authorization" = "token $Token"
    "Accept" = "application/vnd.github.v3+json"
}

$body = @{
    name = $RepoName
    description = "A web platform for local vendors with AI-driven price discovery and negotiation tools"
    private = -not $Public
    auto_init = $false
} | ConvertTo-Json

$url = "https://api.github.com/user/repos"

Write-Host "Creating repository: $RepoName..." -ForegroundColor Green

try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body -ContentType "application/json"
    
    Write-Host "`nRepository created successfully!" -ForegroundColor Green
    Write-Host "Repository URL: $($response.html_url)" -ForegroundColor Cyan
    
    # Add remote and push
    Write-Host "`nSetting up remote and pushing code..." -ForegroundColor Yellow
    
    $remoteUrl = $response.clone_url
    git remote add origin $remoteUrl
    git branch -M main
    git push -u origin main
    
    Write-Host "`nCode pushed successfully!" -ForegroundColor Green
    
    # Enable GitHub Pages
    Write-Host "`nEnabling GitHub Pages..." -ForegroundColor Yellow
    
    $pagesBody = @{
        source = @{
            branch = "main"
            path = "/"
        }
    } | ConvertTo-Json
    
    $pagesUrl = "https://api.github.com/repos/$GitHubUsername/$RepoName/pages"
    
    try {
        $pagesResponse = Invoke-RestMethod -Uri $pagesUrl -Method Post -Headers $headers -Body $pagesBody -ContentType "application/json"
        Write-Host "GitHub Pages enabled!" -ForegroundColor Green
    } catch {
        Write-Host "Note: GitHub Pages may need to be enabled manually" -ForegroundColor Yellow
        Write-Host "Go to: $($response.html_url)/settings/pages" -ForegroundColor Cyan
    }
    
    Write-Host "`n" + "="*60 -ForegroundColor Green
    Write-Host "Setup Complete!" -ForegroundColor Green
    Write-Host "="*60 -ForegroundColor Green
    Write-Host "Repository: $($response.html_url)" -ForegroundColor Cyan
    Write-Host "Pages URL: https://$GitHubUsername.github.io/$RepoName/" -ForegroundColor Cyan
    Write-Host "(May take 1-2 minutes to be live)" -ForegroundColor Yellow
    
} catch {
    Write-Host "`nError:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody" -ForegroundColor Red
    }
    
    if ($_.Exception.Response.StatusCode -eq 422) {
        Write-Host "`nRepository might already exist. Try:" -ForegroundColor Yellow
        Write-Host ".\setup-github.ps1 -RepoName '$RepoName'" -ForegroundColor Cyan
    }
}
