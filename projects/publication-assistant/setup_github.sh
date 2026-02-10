#!/bin/bash
# Setup script for GitHub repository and Pages

echo "Setting up GitHub repository..."

# Check if already has remote
if git remote | grep -q origin; then
    echo "Remote 'origin' already exists"
else
    echo "Please create a GitHub repository first, then run:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/publication-assistant.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
fi

# Enable GitHub Pages (via GitHub CLI if authenticated)
if command -v gh &> /dev/null; then
    echo "Enabling GitHub Pages..."
    gh api repos/:owner/:repo/pages -X POST -f source='{"branch":"main","path":"/docs"}' || echo "Note: GitHub Pages can be enabled manually in repository settings"
else
    echo "GitHub CLI not found. Enable Pages manually:"
    echo "  1. Go to repository Settings > Pages"
    echo "  2. Select 'main' branch as source"
    echo "  3. Select '/docs' folder (or root)"
fi

echo "Setup complete!"
