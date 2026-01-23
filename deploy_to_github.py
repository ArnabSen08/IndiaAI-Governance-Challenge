#!/usr/bin/env python3
"""
GitHub deployment helper script.
Guides you through setting up the repository on GitHub and enabling GitHub Pages.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return None, e.stderr

def check_git_status():
    """Check if git is initialized and configured."""
    print("🔍 Checking Git status...")
    
    # Check if git is installed
    stdout, stderr = run_command("git --version", check=False)
    if stdout is None:
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    print(f"✅ Git version: {stdout}")
    
    # Check if repository is initialized
    if not Path(".git").exists():
        print("📁 Initializing Git repository...")
        run_command("git init")
        print("✅ Git repository initialized")
    
    # Check git configuration
    stdout, _ = run_command("git config user.name", check=False)
    if not stdout:
        print("⚠️  Git user.name not configured")
        name = input("Enter your name for Git commits: ")
        run_command(f'git config user.name "{name}"')
    
    stdout, _ = run_command("git config user.email", check=False)
    if not stdout:
        print("⚠️  Git user.email not configured")
        email = input("Enter your email for Git commits: ")
        run_command(f'git config user.email "{email}"')
    
    return True

def prepare_repository():
    """Prepare the repository for GitHub."""
    print("\n📦 Preparing repository...")
    
    # Add all files
    print("Adding files to Git...")
    run_command("git add .")
    
    # Check if there are changes to commit
    stdout, _ = run_command("git status --porcelain", check=False)
    if stdout:
        print("Committing changes...")
        run_command('git commit -m "Initial commit: Production-ready multi-agent AI system"')
        print("✅ Changes committed")
    else:
        print("✅ No changes to commit")
    
    # Check if main branch exists
    stdout, _ = run_command("git branch --show-current", check=False)
    if stdout != "main":
        print("Creating main branch...")
        run_command("git branch -M main")
        print("✅ Main branch created")

def setup_github_remote():
    """Set up GitHub remote repository."""
    print("\n🌐 Setting up GitHub remote...")
    
    # Check if remote already exists
    stdout, _ = run_command("git remote get-url origin", check=False)
    if stdout:
        print(f"✅ Remote origin already configured: {stdout}")
        return stdout
    
    print("\n📋 GitHub Repository Setup Instructions:")
    print("1. Go to https://github.com/new")
    print("2. Create a new repository named 'multi-agent-ai-system'")
    print("3. Do NOT initialize with README, .gitignore, or license")
    print("4. Copy the repository URL (e.g., https://github.com/username/multi-agent-ai-system.git)")
    
    repo_url = input("\nEnter your GitHub repository URL: ").strip()
    
    if not repo_url:
        print("❌ No repository URL provided")
        return None
    
    # Add remote
    run_command(f"git remote add origin {repo_url}")
    print("✅ Remote origin added")
    
    return repo_url

def push_to_github():
    """Push code to GitHub."""
    print("\n🚀 Pushing to GitHub...")
    
    try:
        # Push to main branch
        stdout, stderr = run_command("git push -u origin main")
        print("✅ Code pushed to GitHub successfully")
        return True
    except:
        print("❌ Failed to push to GitHub")
        print("This might be due to:")
        print("- Authentication issues (set up SSH keys or personal access token)")
        print("- Repository doesn't exist on GitHub")
        print("- Network connectivity issues")
        return False

def setup_github_pages():
    """Instructions for setting up GitHub Pages."""
    print("\n📄 GitHub Pages Setup Instructions:")
    print("=" * 50)
    print("1. Go to your repository on GitHub")
    print("2. Click on 'Settings' tab")
    print("3. Scroll down to 'Pages' section")
    print("4. Under 'Source', select 'Deploy from a branch'")
    print("5. Select 'main' branch and '/docs' folder")
    print("6. Click 'Save'")
    print("7. Your site will be available at: https://your-username.github.io/multi-agent-ai-system/")
    print("\nAlternatively, you can use the web interface at docs/web/index.html")
    print("=" * 50)

def update_readme_links():
    """Update README with actual GitHub links."""
    print("\n🔗 Updating documentation links...")
    
    username = input("Enter your GitHub username: ").strip()
    if not username:
        print("⚠️  Skipping link updates")
        return
    
    # Update files with actual GitHub username
    files_to_update = [
        "README.md",
        "docs/index.md", 
        "docs/web/index.html",
        "docs/web/api.html"
    ]
    
    for file_path in files_to_update:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace placeholder with actual username
                content = content.replace('your-username', username)
                content = content.replace('https://github.com/username/', f'https://github.com/{username}/')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Updated {file_path}")
            except Exception as e:
                print(f"⚠️  Failed to update {file_path}: {e}")

def main():
    """Main deployment function."""
    print("🚀 GitHub Deployment Helper")
    print("=" * 50)
    print("This script will help you deploy your Multi-Agent AI System to GitHub")
    print("and set up GitHub Pages for documentation.")
    print("=" * 50)
    
    # Check prerequisites
    if not check_git_status():
        return False
    
    # Update links with actual username
    update_readme_links()
    
    # Prepare repository
    prepare_repository()
    
    # Set up GitHub remote
    repo_url = setup_github_remote()
    if not repo_url:
        return False
    
    # Push to GitHub
    if not push_to_github():
        print("\n⚠️  Manual push required:")
        print("Run: git push -u origin main")
        print("Make sure you have proper authentication set up.")
    
    # GitHub Pages setup instructions
    setup_github_pages()
    
    print("\n🎉 Deployment preparation complete!")
    print("\nNext steps:")
    print("1. Verify your code is on GitHub")
    print("2. Set up GitHub Pages as instructed above")
    print("3. Your documentation will be available online")
    print("4. Share your project URL for certification review")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)