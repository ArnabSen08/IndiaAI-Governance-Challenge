# Script to merge multiple repositories into IndiaAI-Governance-Challenge
# Each repo will be merged into its own subdirectory

$repos = @(
    "agentic-ai-production-system",
    "multilingual-mandi",
    "publication-assistant",
    "ready-tensor",
    "gemini3-hackathon",
    "bharat-ai-hub",
    "elastic-aviation-rag-blog",
    "little-lemon-restaurant",
    "blockchain-lottery-dapp",
    "coursera-portfolio",
    "the-referee",
    "data-weaver-dashboard",
    "smart-desktop-organizer",
    "devtoolkit",
    "bangalore-tech-culture-assistant"
)

foreach ($repo in $repos) {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Processing: $repo" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    
    # Add remote
    Write-Host "Adding remote for $repo..." -ForegroundColor Yellow
    git remote add $repo "https://github.com/ArnabSen08/$repo.git"
    
    # Fetch the repository
    Write-Host "Fetching $repo..." -ForegroundColor Yellow
    git fetch $repo
    
    # Create a subdirectory for this repo
    $subdir = "projects/$repo"
    
    # Merge using subtree strategy
    Write-Host "Merging $repo into $subdir..." -ForegroundColor Yellow
    git merge -s ours --no-commit --allow-unrelated-histories "$repo/master" 2>$null
    if ($LASTEXITCODE -ne 0) {
        git merge -s ours --no-commit --allow-unrelated-histories "$repo/main" 2>$null
    }
    
    git read-tree --prefix="$subdir/" -u "$repo/master" 2>$null
    if ($LASTEXITCODE -ne 0) {
        git read-tree --prefix="$subdir/" -u "$repo/main" 2>$null
    }
    
    git commit -m "Merge $repo into $subdir"
    
    # Remove remote to keep things clean
    git remote remove $repo
    
    Write-Host "Completed: $repo" -ForegroundColor Green
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "All repositories merged successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
