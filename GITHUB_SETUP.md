# GitHub Repository Setup Instructions

Since GitHub CLI has proxy connection issues, follow these steps to set up your repository:

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `multilingual-mandi` (or your preferred name)
3. Set visibility: **Public** (required for GitHub Pages free tier)
4. **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository, run:

```powershell
# Replace 'multilingual-mandi' with your actual repository name if different
.\setup-github.ps1 -RepoName "multilingual-mandi"
```

Or manually:

```powershell
# Add remote (replace with your actual username and repo name)
git remote add origin https://github.com/ArnabSen08/multilingual-mandi.git

# Rename branch to main (if not already)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Enable GitHub Pages

### Option A: Using GitHub CLI (if proxy is fixed)
```powershell
gh api repos/ArnabSen08/multilingual-mandi/pages -X POST -f source=@{branch="main",path="/"}
```

### Option B: Using GitHub Web Interface
1. Go to: `https://github.com/ArnabSen08/multilingual-mandi/settings/pages`
2. Under "Source", select:
   - Branch: `main`
   - Folder: `/ (root)`
3. Click **Save**
4. Wait a few minutes for GitHub to build and deploy

## Step 4: Verify GitHub Pages

Your site will be available at:
- `https://arnabsen08.github.io/multilingual-mandi/`

(Note: Replace `arnabsen08` with your actual GitHub username if different)

## Additional Notes

- Make sure your project has an `index.html` file in the root for GitHub Pages to serve
- The `/.kiro` directory will be included in the repository as required
- GitHub Pages typically takes 1-2 minutes to deploy after enabling

## Troubleshooting

If you encounter issues:
1. Check repository visibility is set to **Public**
2. Ensure you've pushed at least one commit
3. Verify the branch name is `main` or `master`
4. Check GitHub Actions tab for any build errors
