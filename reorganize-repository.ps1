# Repository Reorganization Script
# This script organizes the IndiaAI-Governance-Challenge repository structure

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Repository Reorganization Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Safety check
Write-Host "⚠️  WARNING: This script will reorganize your repository structure!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Before proceeding, ensure you have:" -ForegroundColor Yellow
Write-Host "  1. Committed all current changes" -ForegroundColor White
Write-Host "  2. Created a backup branch" -ForegroundColor White
Write-Host ""
$confirm = Read-Host "Do you want to continue? (yes/no)"

if ($confirm -ne "yes") {
    Write-Host "Operation cancelled." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "Creating backup branch..." -ForegroundColor Cyan
git branch backup-before-reorganization
Write-Host "✓ Backup branch created: backup-before-reorganization" -ForegroundColor Green
Write-Host ""

# Create new directory structure
Write-Host "Creating new directory structure..." -ForegroundColor Cyan

$directories = @(
    "docs/governance-proposals",
    "docs/implementation-guides",
    "docs/project-summaries",
    "docs/ready-tensor",
    "docs/github-profile",
    "scripts"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✓ Created: $dir" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Moving files to new structure..." -ForegroundColor Cyan

# Move governance proposal documents
$governanceDocs = @(
    "AI-AYUSH-INTEGRATED-HEALTH-SYSTEM.md",
    "AI-FINANCIAL-COMPLIANCE-VALIDATION-ENGINE.md",
    "AI-POWERED-LAST-MILE-DELIVERY-SYSTEM.md",
    "AI-VENDOR-MATCHING-MSME-SYSTEM.md",
    "AI-VIRTUAL-NEGOTIATION-ASSISTANT.md",
    "BRIDGE-FLYOVER-DECISION-SUPPORT-SYSTEM.md",
    "SATELLITE-PROPERTY-INTELLIGENCE-SYSTEM.md",
    "SCHOOL-INFRASTRUCTURE-FORECASTING-SYSTEM.md"
)

Write-Host "  Moving governance proposals..." -ForegroundColor Yellow
foreach ($file in $governanceDocs) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "docs/governance-proposals/" -Force
        Write-Host "    ✓ Moved: $file" -ForegroundColor Gray
    }
}

# Move implementation guides
$implementationDocs = @(
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

Write-Host "  Moving implementation guides..." -ForegroundColor Yellow
foreach ($file in $implementationDocs) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "docs/implementation-guides/" -Force
        Write-Host "    ✓ Moved: $file" -ForegroundColor Gray
    }
}

# Move project summaries
$projectSummaries = @(
    "DELIVERY-SUMMARY.md",
    "GIS-COMPLETION-REPORT.md",
    "GIS-PROJECT-SUMMARY.md",
    "MERGE_SUMMARY.md",
    "PORTFOLIO_TRANSFORMATION.md",
    "PROJECT-SUMMARY.md",
    "REDESIGN_SUMMARY.md"
)

Write-Host "  Moving project summaries..." -ForegroundColor Yellow
foreach ($file in $projectSummaries) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "docs/project-summaries/" -Force
        Write-Host "    ✓ Moved: $file" -ForegroundColor Gray
    }
}

# Move Ready Tensor documentation
$readyTensorDocs = @(
    "FINAL_READY_TENSOR_LINKS.md",
    "PROFILE_UPDATE_COMPLETE.md",
    "PUBLICATION_CHECKLIST.md",
    "QUICK_START_REPOS.md",
    "READY_TENSOR_REPO_SETUP.md",
    "READY_TENSOR_RESPONSE.md",
    "READY_TENSOR_UPDATED_LINKS.md"
)

Write-Host "  Moving Ready Tensor documentation..." -ForegroundColor Yellow
foreach ($file in $readyTensorDocs) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "docs/ready-tensor/" -Force
        Write-Host "    ✓ Moved: $file" -ForegroundColor Gray
    }
}

# Move GitHub profile documentation
$githubProfileDocs = @(
    "GITHUB_PROFILE_FEATURED_PROJECTS.md",
    "UPDATED_FEATURED_PROJECTS.md"
)

Write-Host "  Moving GitHub profile documentation..." -ForegroundColor Yellow
foreach ($file in $githubProfileDocs) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "docs/github-profile/" -Force
        Write-Host "    ✓ Moved: $file" -ForegroundColor Gray
    }
}

# Move scripts
$scriptFiles = @(
    "merge-repos.ps1",
    "setup-ready-tensor-repos.ps1",
    "verify-repos.ps1"
)

Write-Host "  Moving scripts..." -ForegroundColor Yellow
foreach ($file in $scriptFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "scripts/" -Force
        Write-Host "    ✓ Moved: $file" -ForegroundColor Gray
    }
}

# Move legacy projects to projects folder
Write-Host "  Moving legacy projects..." -ForegroundColor Yellow

if (Test-Path "financial_compliance_engine") {
    Move-Item -Path "financial_compliance_engine" -Destination "projects/financial-compliance-engine" -Force
    Write-Host "    ✓ Moved: financial_compliance_engine → projects/" -ForegroundColor Gray
}

if (Test-Path "india_ai_challenge_web") {
    Move-Item -Path "india_ai_challenge_web" -Destination "projects/india-ai-challenge-web" -Force
    Write-Host "    ✓ Moved: india_ai_challenge_web → projects/" -ForegroundColor Gray
}

# Create archive folder for misc files
Write-Host "  Creating archive for miscellaneous files..." -ForegroundColor Yellow
if (-not (Test-Path "archive")) {
    New-Item -ItemType Directory -Path "archive" -Force | Out-Null
}

$archiveFiles = @(
    "Andhra.txt"
)

foreach ($file in $archiveFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "archive/" -Force
        Write-Host "    ✓ Archived: $file" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Creating documentation index..." -ForegroundColor Cyan

# Create docs/README.md
$docsReadme = @"
# Documentation Index

This directory contains all documentation for the IndiaAI Governance Challenge repository.

## 📁 Directory Structure

### Governance Proposals
Location: \`governance-proposals/\`

AI-powered solutions for government and public sector challenges:
- AI-AYUSH Integrated Health System
- AI Financial Compliance Validation Engine
- AI-Powered Last Mile Delivery System
- AI Vendor Matching MSME System
- AI Virtual Negotiation Assistant
- Bridge/Flyover Decision Support System
- Satellite Property Intelligence System
- School Infrastructure Forecasting System

### Implementation Guides
Location: \`implementation-guides/\`

Technical implementation documentation:
- Data architecture and pipelines
- E-commerce integration guides
- GIS implementation
- ML algorithms and models
- Satellite geospatial processing
- Urban infrastructure planning

### Project Summaries
Location: \`project-summaries/\`

Project completion reports and summaries:
- Delivery summaries
- GIS project reports
- Portfolio transformation
- Merge summaries

### Ready Tensor Certification
Location: \`ready-tensor/\`

Documentation for Ready Tensor certification projects:
- Repository setup guides
- Publication checklists
- Response templates
- Project links

### GitHub Profile
Location: \`github-profile/\`

GitHub profile content and featured projects:
- Featured projects section
- Profile updates

## 🔗 Quick Links

- [Main README](../README.md)
- [Projects Index](../PROJECTS_INDEX.md)
- [Repository Optimization Guide](../REPOSITORY_OPTIMIZATION_GUIDE.md)

---

*Last Updated: $(Get-Date -Format "MMMM dd, yyyy")*
"@

Set-Content -Path "docs/README.md" -Value $docsReadme -Encoding UTF8
Write-Host "  ✓ Created: docs/README.md" -ForegroundColor Green

# Create scripts/README.md
$scriptsReadme = @"
# Automation Scripts

This directory contains automation scripts for repository management.

## Available Scripts

### merge-repos.ps1
Merges multiple repositories into the main repository structure.

### setup-ready-tensor-repos.ps1
Sets up Ready Tensor certification project repositories on GitHub.

### verify-repos.ps1
Verifies that all repositories are properly configured and accessible.

### reorganize-repository.ps1
Reorganizes the repository structure for better organization.

## Usage

Run scripts from the repository root:

\`\`\`powershell
.\scripts\script-name.ps1
\`\`\`

---

*Last Updated: $(Get-Date -Format "MMMM dd, yyyy")*
"@

Set-Content -Path "scripts/README.md" -Value $scriptsReadme -Encoding UTF8
Write-Host "  ✓ Created: scripts/README.md" -ForegroundColor Green

Write-Host ""
Write-Host "Updating .gitignore..." -ForegroundColor Cyan

# Enhanced .gitignore
$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.pytest_cache/
.coverage
htmlcov/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.eslintcache

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local
.env.*.local

# Build outputs
dist/
build/
*.log

# Temporary files
*.tmp
*.temp
temp/
tmp/

# OS
Thumbs.db
.DS_Store
"@

Set-Content -Path ".gitignore" -Value $gitignoreContent -Encoding UTF8
Write-Host "  ✓ Updated: .gitignore" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Reorganization Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Summary of changes:" -ForegroundColor Yellow
Write-Host "  ✓ Created organized directory structure" -ForegroundColor White
Write-Host "  ✓ Moved documentation files to docs/" -ForegroundColor White
Write-Host "  ✓ Moved scripts to scripts/" -ForegroundColor White
Write-Host "  ✓ Moved legacy projects to projects/" -ForegroundColor White
Write-Host "  ✓ Created documentation indexes" -ForegroundColor White
Write-Host "  ✓ Updated .gitignore" -ForegroundColor White
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review the changes: git status" -ForegroundColor White
Write-Host "  2. Test that everything works" -ForegroundColor White
Write-Host "  3. Commit changes: git add . && git commit -m 'Reorganize repository structure'" -ForegroundColor White
Write-Host "  4. Push to GitHub: git push origin master" -ForegroundColor White
Write-Host ""
Write-Host "  If you need to rollback: git checkout backup-before-reorganization" -ForegroundColor Yellow
Write-Host ""
