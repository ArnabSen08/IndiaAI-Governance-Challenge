# Ready Tensor Projects - GitHub Repository Setup Guide

## Issue
The Ready Tensor team reported 404 errors when trying to access your project repositories. This means the repositories either don't exist yet or are set to private.

## Solution
Follow these steps to create and publish your three Ready Tensor certification projects to GitHub.

---

## Prerequisites

1. **GitHub CLI (gh)** - Install from https://cli.github.com/
2. **Git** - Should already be installed
3. **GitHub Account** - Logged in as ArnabSen08

---

## Quick Setup (Automated)

### Step 1: Authenticate with GitHub CLI

Open PowerShell and run:

```powershell
gh auth login
```

Follow the prompts:
- Choose: **GitHub.com**
- Protocol: **HTTPS**
- Authenticate: **Login with a web browser**
- Copy the one-time code and paste it in your browser

### Step 2: Run the Setup Script

```powershell
cd IndiaAI-Governance-Challenge
.\setup-ready-tensor-repos.ps1
```

This script will:
- ✅ Create 3 public GitHub repositories
- ✅ Push all project code
- ✅ Enable GitHub Pages
- ✅ Add relevant topics/tags
- ✅ Ensure repositories are public

### Step 3: Verify Setup

After the script completes, verify each repository:

1. **Agentic AI Production System**
   - Repository: https://github.com/ArnabSen08/agentic-ai-production-system
   - GitHub Pages: https://arnabsen08.github.io/agentic-ai-production-system/

2. **Ready Tensor (RAG Assistant)**
   - Repository: https://github.com/ArnabSen08/ready-tensor
   - GitHub Pages: https://arnabsen08.github.io/ready-tensor/

3. **Publication Assistant**
   - Repository: https://github.com/ArnabSen08/publication-assistant
   - GitHub Pages: https://arnabsen08.github.io/publication-assistant/

---

## Manual Setup (If Script Fails)

### For Each Project

#### 1. Navigate to Project Directory

```powershell
cd IndiaAI-Governance-Challenge/projects/agentic-ai-production-system
```

#### 2. Initialize Git (if needed)

```powershell
git init
git add .
git commit -m "Initial commit: Ready Tensor certification project"
```

#### 3. Create GitHub Repository

```powershell
gh repo create ArnabSen08/agentic-ai-production-system --public --source=. --remote=origin --description="Production-Ready Multi-Agent AI System - Ready Tensor Certification"
```

#### 4. Push to GitHub

```powershell
git branch -M main
git push -u origin main
```

#### 5. Enable GitHub Pages

**Option A: Using GitHub CLI**
```powershell
gh api repos/ArnabSen08/agentic-ai-production-system/pages -X POST -f "source[branch]=main" -f "source[path]=/docs"
```

**Option B: Manual (Recommended)**
1. Go to https://github.com/ArnabSen08/agentic-ai-production-system/settings/pages
2. Under "Source":
   - Branch: **main**
   - Folder: **/docs** (or **/ (root)** if no docs folder)
3. Click **Save**

#### 6. Ensure Repository is Public

```powershell
gh repo edit ArnabSen08/agentic-ai-production-system --visibility public
```

Or manually:
1. Go to repository Settings
2. Scroll to "Danger Zone"
3. Click "Change visibility" → "Make public"

#### 7. Repeat for Other Projects

- `ready-tensor`
- `publication-assistant`

---

## Update Ready Tensor Publications

Once all repositories are live, update your Ready Tensor publications with these URLs:

### Publication 1: Production-Ready Multi-Agent AI System

**Code Links:**
```
https://github.com/ArnabSen08/agentic-ai-production-system
https://arnabsen08.github.io/agentic-ai-production-system/
```

### Publication 2: Agentic AI Essentials (RAG System)

**Code Links:**
```
https://github.com/ArnabSen08/ready-tensor
https://arnabsen08.github.io/ready-tensor/
```

**Dataset Links (if applicable):**
```
https://github.com/ArnabSen08/ready-tensor/tree/main/supplementary_materials/data
```

### Publication 3: Multi-Agent Publication Assistant

**Code Links:**
```
https://github.com/ArnabSen08/publication-assistant
https://arnabsen08.github.io/publication-assistant/
```

---

## Verification Checklist

Before notifying Ready Tensor team:

- [ ] All 3 repositories are created
- [ ] All repositories are set to **PUBLIC**
- [ ] Code is pushed to main branch
- [ ] README.md is visible on each repository
- [ ] GitHub Pages is enabled
- [ ] GitHub Pages URLs are accessible (wait 2-3 minutes after enabling)
- [ ] Repository URLs are updated in Ready Tensor publications

---

## Troubleshooting

### Issue: "gh: command not found"
**Solution:** Install GitHub CLI from https://cli.github.com/

### Issue: "authentication required"
**Solution:** Run `gh auth login` and follow the prompts

### Issue: "repository already exists"
**Solution:** 
```powershell
# Delete existing repository
gh repo delete ArnabSen08/REPO_NAME --yes

# Or update remote URL
git remote set-url origin https://github.com/ArnabSen08/REPO_NAME.git
git push -u origin main --force
```

### Issue: "GitHub Pages not building"
**Solution:**
1. Check repository Settings → Pages
2. Ensure source is set correctly
3. Wait 2-3 minutes for build
4. Check for build errors in Actions tab

### Issue: "404 on GitHub Pages URL"
**Solution:**
1. Verify GitHub Pages is enabled
2. Check if index.html or README.md exists in the source folder
3. Wait a few minutes for deployment
4. Check repository Actions tab for deployment status

---

## Contact Ready Tensor Team

After setup is complete, reply to their email with:

```
Dear Ready Tensor Team,

Thank you for bringing this to my attention. I have now published all three project repositories and ensured they are publicly accessible.

Project Repository Links:

1. Production-Ready Multi-Agent AI System
   - Repository: https://github.com/ArnabSen08/agentic-ai-production-system
   - Live Demo: https://arnabsen08.github.io/agentic-ai-production-system/

2. Agentic AI Essentials: RAG-Based Question-Answering System
   - Repository: https://github.com/ArnabSen08/ready-tensor
   - Live Demo: https://arnabsen08.github.io/ready-tensor/

3. Multi-Agent Publication Assistant
   - Repository: https://github.com/ArnabSen08/publication-assistant
   - Live Demo: https://arnabsen08.github.io/publication-assistant/

All repositories are now public and accessible. I have also updated the publication links accordingly.

Please let me know if you need any additional information.

Best regards,
Arnab Sen
```

---

## Additional Notes

- **GitHub Pages Build Time:** Allow 2-3 minutes after enabling for the site to become available
- **Repository Visibility:** Double-check all repos are PUBLIC, not private
- **README Files:** Ensure each project has a comprehensive README.md
- **License Files:** Consider adding LICENSE files if not already present
- **Topics/Tags:** Add relevant topics to improve discoverability

---

## Quick Reference Commands

```powershell
# Check authentication
gh auth status

# List your repositories
gh repo list ArnabSen08

# View repository details
gh repo view ArnabSen08/agentic-ai-production-system

# Check if repository is public
gh repo view ArnabSen08/agentic-ai-production-system --json visibility

# Make repository public
gh repo edit ArnabSen08/agentic-ai-production-system --visibility public
```

---

**Last Updated:** February 11, 2026
**Status:** Ready for deployment
