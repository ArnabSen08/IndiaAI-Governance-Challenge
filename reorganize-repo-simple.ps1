# Simple Repository Reorganization Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Repository Reorganization Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create backup branch
Write-Host "Creating backup branch..." -ForegroundColor Cyan
git branch backup-before-reorganization 2>$null
Write-Host "Backup branch created: backup-before-reorganization" -ForegroundColor Green
Write-Host ""

# Create new directory structure
Write-Host "Creating new directory structure..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "docs/governance-proposals" -Force | Out-Null
New-Item -ItemType Directory -Path "docs/implementation-guides" -Force | Out-Null
New-Item -ItemType Directory -Path "docs/project-summaries" -Force | Out-Null
New-Item -ItemType Directory -Path "docs/ready-tensor" -Force | Out-Null
New-Item -ItemType Directory -Path "docs/github-profile" -Force | Out-Null
New-Item -ItemType Directory -Path "scripts" -Force | Out-Null
New-Item -ItemType Directory -Path "archive" -Force | Out-Null
Write-Host "Directories created" -ForegroundColor Green
Write-Host ""

# Move governance proposals
Write-Host "Moving governance proposals..." -ForegroundColor Yellow
$govFiles = @(
    "AI-AYUSH-INTEGRATED-HEALTH-SYSTEM.md",
    "AI-FINANCIAL-COMPLIANCE-VALIDATION-ENGINE.md",
    "AI-POWERED-LAST-MILE-DELIVERY-SYSTEM.md",
    "AI-VENDOR-MATCHING-MSME-SYSTEM.md",
    "AI-VIRTUAL-NEGOTIATION-ASSISTANT.md",
    "BRIDGE-FLYOVER-DECISION-SUPPORT-SYSTEM.md",
    "SATELLITE-PROPERTY-INTELLIGENCE-SYSTEM.md",
    "SCHOOL-INFRASTRUCTURE-FORECASTING-SYSTEM.md"
)
foreach ($file in $govFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "docs/governance-proposals/" -Force
        Write-Host "  Moved: $file" -ForegroundColor Gray
    }
}

# Move implementation guides
Write-Host "Moving implementation guides..." -ForegroundColor Yellow
$implFiles = @(
    "data-architecture-pipeline.md",
    "ecommerce-integration-guide.md",
    "GIS-IMPLEMENTATION-GUIDE.md",
    "IMPLEMENTATION-GUIDE.md",
    "last-mile-delivery-optimization.md",
    "ml-algorithms-conflict-detection.md",
    "ml-algorithms-models.md",
    "satellite-geospatial-processing.md",
    "school-infrastructure-validation.md",
    "smart-market-linkage-design.md",
    "urban-infrastructure-planning.md",
    "gis-land-allocation-design.md"
)
foreach ($file in $implFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "docs/implementation-guides/" -Force
        Write-Host "  Moved: $file" -ForegroundColor Gray
    }
}

# Move project summaries
Write-Host "Moving project summaries..." -ForegroundColor Yellow
$summaryFiles = @(
    "DELIVERY-SUMMARY.md",
    "GIS-COMPLETION-REPORT.md",
    "GIS-PROJECT-SUMMARY.md",
    "MERGE_SUMMARY.md",
    "PORTFOLIO_TRANSFORMATION.md",
    "PROJECT-SUMMARY.md",
    "REDESIGN_SUMMARY.md"
)
foreach ($file in $summaryFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "docs/project-summaries/" -Force
        Write-Host "  Moved: $file" -ForegroundColor Gray
    }
}

# Move Ready Tensor docs
Write-Host "Moving Ready Tensor documentation..." -ForegroundColor Yellow
$rtFiles = @(
    "FINAL_READY_TENSOR_LINKS.md",
    "PROFILE_UPDATE_COMPLETE.md",
    "PUBLICATION_CHECKLIST.md",
    "QUICK_START_REPOS.md",
    "READY_TENSOR_REPO_SETUP.md",
    "READY_TENSOR_RESPONSE.md",
    "READY_TENSOR_UPDATED_LINKS.md"
)
foreach ($file in $rtFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "docs/ready-tensor/" -Force
        Write-Host "  Moved: $file" -ForegroundColor Gray
    }
}

# Move GitHub profile docs
Write-Host "Moving GitHub profile documentation..." -ForegroundColor Yellow
$ghFiles = @(
    "GITHUB_PROFILE_FEATURED_PROJECTS.md",
    "UPDATED_FEATURED_PROJECTS.md"
)
foreach ($file in $ghFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "docs/github-profile/" -Force
        Write-Host "  Moved: $file" -ForegroundColor Gray
    }
}

# Move scripts
Write-Host "Moving scripts..." -ForegroundColor Yellow
$scriptFiles = @(
    "merge-repos.ps1",
    "setup-ready-tensor-repos.ps1",
    "verify-repos.ps1"
)
foreach ($file in $scriptFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "scripts/" -Force
        Write-Host "  Moved: $file" -ForegroundColor Gray
    }
}

# Move legacy projects
Write-Host "Moving legacy projects..." -ForegroundColor Yellow
if (Test-Path "financial_compliance_engine") {
    Move-Item -Path "financial_compliance_engine" -Destination "projects/financial-compliance-engine" -Force
    Write-Host "  Moved: financial_compliance_engine" -ForegroundColor Gray
}
if (Test-Path "india_ai_challenge_web") {
    Move-Item -Path "india_ai_challenge_web" -Destination "projects/india-ai-challenge-web" -Force
    Write-Host "  Moved: india_ai_challenge_web" -ForegroundColor Gray
}

# Archive misc files
Write-Host "Archiving miscellaneous files..." -ForegroundColor Yellow
if (Test-Path "Andhra.txt") {
    Move-Item -Path "Andhra.txt" -Destination "archive/" -Force
    Write-Host "  Archived: Andhra.txt" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Reorganization Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review changes: git status" -ForegroundColor White
Write-Host "  2. Commit: git add . ; git commit -m 'Reorganize repository structure'" -ForegroundColor White
Write-Host "  3. Push: git push origin master" -ForegroundColor White
Write-Host ""
