# Quick Start Guide

## 🚀 Complete Setup in 3 Steps

### Step 1: Fix GitHub Authentication (if needed)

If you see proxy errors, try:

```powershell
# Option 1: Login with token
gh auth login --with-token < token.txt

# Option 2: Login via web (if proxy is fixed)
gh auth login --web

# Option 3: Use manual setup (see below)
```

### Step 2: Create Repository

**Automatic (if GitHub CLI works):**
```powershell
gh repo create publication-assistant --public --source=. --remote=origin --description="Multi-agent system for improving AI/ML project publications using LangGraph orchestration"
git branch -M main
git push -u origin main
```

**Manual:**
1. Go to https://github.com/new
2. Repository name: `publication-assistant`
3. Description: "Multi-agent system for improving AI/ML project publications using LangGraph orchestration"
4. Set to **Public**
5. **Don't** initialize with README
6. Click "Create repository"
7. Then run:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/publication-assistant.git
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Pages

**Via GitHub CLI:**
```powershell
gh api repos/:owner/:repo/pages -X POST -f source='{"branch":"main","path":"/docs"}'
```

**Via Web Interface:**
1. Go to repository Settings > Pages
2. Source: Branch `main`, Folder `/docs`
3. Click Save

Your site will be live at: `https://YOUR_USERNAME.github.io/publication-assistant/`

## ✅ Verification Checklist

- [ ] Repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] GitHub Pages enabled
- [ ] Documentation accessible at Pages URL
- [ ] All files committed locally

## 🎉 You're Done!

Your multi-agent publication assistant is now on GitHub with Pages enabled!
