# GitHub Repository Setup Guide

## Step 1: Authenticate with GitHub CLI

If you haven't already, authenticate with GitHub:

```bash
gh auth login
```

Follow the prompts to authenticate.

## Step 2: Create GitHub Repository

Run the following command to create the repository:

```bash
gh repo create publication-assistant --public --source=. --remote=origin --description="Multi-agent system for improving AI/ML project publications using LangGraph orchestration"
```

Or manually:
1. Go to https://github.com/new
2. Repository name: `publication-assistant`
3. Description: "Multi-agent system for improving AI/ML project publications using LangGraph orchestration"
4. Set to Public
5. Don't initialize with README (we already have one)
6. Click "Create repository"

Then add the remote:
```bash
git remote add origin https://github.com/YOUR_USERNAME/publication-assistant.git
git branch -M main
git push -u origin main
```

## Step 3: Enable GitHub Pages

### Option A: Using GitHub CLI
```bash
gh api repos/:owner/:repo/pages -X POST -f source='{"branch":"main","path":"/docs"}'
```

### Option B: Manual Setup
1. Go to your repository on GitHub
2. Click on "Settings"
3. Scroll down to "Pages" in the left sidebar
4. Under "Source", select:
   - Branch: `main`
   - Folder: `/docs`
5. Click "Save"

Your site will be available at: `https://YOUR_USERNAME.github.io/publication-assistant/`

## Step 4: Verify Setup

After pushing, verify:
- ✅ Repository is created and code is pushed
- ✅ GitHub Pages is enabled
- ✅ Documentation is accessible at the Pages URL

## Troubleshooting

If you encounter authentication issues:
```bash
gh auth logout
gh auth login
```

If the repository already exists:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/publication-assistant.git
git push -u origin main
```
