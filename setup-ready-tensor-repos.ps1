# PowerShell script to create and publish Ready Tensor certification projects
# This script will create GitHub repositories for the three certification projects

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Ready Tensor Projects - GitHub Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub CLI is installed
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: GitHub CLI (gh) is not installed!" -ForegroundColor Red
    Write-Host "Please install it from: https://cli.github.com/" -ForegroundColor Yellow
    Write-Host "After installation, run: gh auth login" -ForegroundColor Yellow
    exit 1
}

# Check if authenticated
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Not authenticated with GitHub!" -ForegroundColor Red
    Write-Host "Please run: gh auth login" -ForegroundColor Yellow
    exit 1
}

Write-Host "GitHub CLI is installed and authenticated!" -ForegroundColor Green
Write-Host ""

# Define projects
$projects = @(
    @{
        Name = "agentic-ai-production-system"
        Path = "IndiaAI-Governance-Challenge/projects/agentic-ai-production-system"
        Description = "Production-Ready Multi-Agent AI System: From Prototype to Professional Deployment - Ready Tensor Certification Capstone"
        Topics = @("ai", "multi-agent-system", "langchain", "production-ready", "ready-tensor", "certification", "agentic-ai")
    },
    @{
        Name = "ready-tensor"
        Path = "IndiaAI-Governance-Challenge/projects/ready-tensor"
        Description = "RAG-Based AI Assistant: Vector-Powered Question-Answering System - Ready Tensor Agentic AI Essentials Certification"
        Topics = @("rag", "langchain", "vector-database", "ai-assistant", "ready-tensor", "certification", "question-answering")
    },
    @{
        Name = "publication-assistant"
        Path = "IndiaAI-Governance-Challenge/projects/publication-assistant"
        Description = "Multi-Agent Publication Assistant: AI-Powered GitHub Repository Analysis and Enhancement - Ready Tensor Certification"
        Topics = @("multi-agent", "langgraph", "github-api", "ai-agents", "ready-tensor", "certification", "repository-analysis")
    }
)

# Function to create and setup repository
function Setup-Repository {
    param (
        [string]$Name,
        [string]$Path,
        [string]$Description,
        [array]$Topics
    )
    
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "Setting up: $Name" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    
    # Navigate to project directory
    if (-not (Test-Path $Path)) {
        Write-Host "ERROR: Project path not found: $Path" -ForegroundColor Red
        return $false
    }
    
    Push-Location $Path
    
    # Initialize git if needed
    if (-not (Test-Path ".git")) {
        Write-Host "Initializing git repository..." -ForegroundColor Cyan
        git init
        git add .
        git commit -m "Initial commit: Ready Tensor certification project"
    }
    
    # Check if repository already exists on GitHub
    Write-Host "Checking if repository exists on GitHub..." -ForegroundColor Cyan
    $repoExists = gh repo view "ArnabSen08/$Name" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Repository already exists on GitHub!" -ForegroundColor Yellow
        Write-Host "Updating remote URL..." -ForegroundColor Cyan
        git remote remove origin 2>$null
        git remote add origin "https://github.com/ArnabSen08/$Name.git"
    } else {
        Write-Host "Creating new GitHub repository..." -ForegroundColor Cyan
        gh repo create "ArnabSen08/$Name" --public --description "$Description" --source=. --remote=origin
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: Failed to create repository!" -ForegroundColor Red
            Pop-Location
            return $false
        }
    }
    
    # Set main branch
    Write-Host "Setting main branch..." -ForegroundColor Cyan
    git branch -M main
    
    # Push to GitHub
    Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
    git push -u origin main --force
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to push to GitHub!" -ForegroundColor Red
        Pop-Location
        return $false
    }
    
    # Add topics
    Write-Host "Adding repository topics..." -ForegroundColor Cyan
    foreach ($topic in $Topics) {
        gh repo edit "ArnabSen08/$Name" --add-topic $topic 2>$null
    }
    
    # Enable GitHub Pages
    Write-Host "Enabling GitHub Pages..." -ForegroundColor Cyan
    
    # Try /docs folder first
    $pagesResult = gh api "repos/ArnabSen08/$Name/pages" -X POST -f "source[branch]=main" -f "source[path]=/docs" 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        # Try root folder
        $pagesResult = gh api "repos/ArnabSen08/$Name/pages" -X POST -f "source[branch]=main" -f "source[path]=/" 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Note: GitHub Pages may already be enabled or needs manual setup" -ForegroundColor Yellow
            Write-Host "Visit: https://github.com/ArnabSen08/$Name/settings/pages" -ForegroundColor Cyan
        }
    }
    
    # Make repository public (ensure it's public)
    Write-Host "Ensuring repository is public..." -ForegroundColor Cyan
    gh repo edit "ArnabSen08/$Name" --visibility public
    
    Write-Host ""
    Write-Host "✓ Repository created: https://github.com/ArnabSen08/$Name" -ForegroundColor Green
    Write-Host "✓ GitHub Pages: https://arnabsen08.github.io/$Name/" -ForegroundColor Green
    Write-Host ""
    
    Pop-Location
    return $true
}

# Setup each project
$successCount = 0
foreach ($project in $projects) {
    $result = Setup-Repository -Name $project.Name -Path $project.Path -Description $project.Description -Topics $project.Topics
    if ($result) {
        $successCount++
    }
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Successfully setup $successCount out of $($projects.Count) repositories" -ForegroundColor Green
Write-Host ""
Write-Host "Repository URLs:" -ForegroundColor Yellow
Write-Host "1. https://github.com/ArnabSen08/agentic-ai-production-system" -ForegroundColor White
Write-Host "2. https://github.com/ArnabSen08/ready-tensor" -ForegroundColor White
Write-Host "3. https://github.com/ArnabSen08/publication-assistant" -ForegroundColor White
Write-Host ""
Write-Host "GitHub Pages URLs:" -ForegroundColor Yellow
Write-Host "1. https://arnabsen08.github.io/agentic-ai-production-system/" -ForegroundColor White
Write-Host "2. https://arnabsen08.github.io/ready-tensor/" -ForegroundColor White
Write-Host "3. https://arnabsen08.github.io/publication-assistant/" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Verify all repositories are public" -ForegroundColor White
Write-Host "2. Check GitHub Pages are enabled in repository settings" -ForegroundColor White
Write-Host "3. Update your Ready Tensor publications with these URLs" -ForegroundColor White
Write-Host "4. Wait 2-3 minutes for GitHub Pages to build" -ForegroundColor White
Write-Host ""
