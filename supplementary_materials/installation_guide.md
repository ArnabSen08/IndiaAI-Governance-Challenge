# Installation Guide

Complete step-by-step installation instructions for the Publication Assistant system.

## Prerequisites

Before installing, ensure you have:

- **Python 3.9 or higher** installed
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **Internet connection** (for downloading packages and API access)

## Step 1: Clone the Repository

```bash
git clone https://github.com/ArnabSen08/publication-assistant.git
cd publication-assistant
```

## Step 2: Create Virtual Environment

### Windows
```powershell
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- langchain
- langchain-openai
- langgraph
- python-dotenv
- requests
- beautifulsoup4
- PyGithub
- yake
- textstat
- pydantic

## Step 4: Set Up Environment Variables

### Copy the example file:
```bash
# Windows
copy .env_example .env

# macOS/Linux
cp .env_example .env
```

### Edit `.env` file:

Open `.env` in a text editor and add your API keys:

```env
# OpenAI API Configuration (Required)
OPENAI_API_KEY=your_openai_api_key_here

# GitHub API Configuration (Optional, for private repos)
GITHUB_TOKEN=your_github_token_here

# Web Search API Configuration (Optional)
SEARCH_API_KEY=your_search_api_key_here

# Model Configuration
MODEL_NAME=gpt-4-turbo-preview
TEMPERATURE=0.7
```

### Getting API Keys:

1. **OpenAI API Key**:
   - Go to https://platform.openai.com/api-keys
   - Sign in or create an account
   - Click "Create new secret key"
   - Copy and paste into `.env`

2. **GitHub Token** (Optional):
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `public_repo` (for public repos)
   - Copy and paste into `.env`

3. **Search API Key** (Optional):
   - Not required for basic functionality
   - DuckDuckGo search works without API key
   - Can add SerpAPI or Google Custom Search API key for better results

## Step 5: Verify Installation

Run a quick test to ensure everything is installed correctly:

```bash
python -c "from orchestrator import MultiAgentOrchestrator; print('Installation successful!')"
```

If you see "Installation successful!", you're ready to go!

## Step 6: Run the System

### Interactive Mode:
```bash
python main.py
```

### Programmatic Usage:
```python
from orchestrator import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator()
result = orchestrator.analyze_repository(
    repo_url="https://github.com/username/repo-name",
    project_description="Optional description"
)
print(result["report"])
```

## Troubleshooting

### Issue: "Module not found" errors

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "OPENAI_API_KEY not found"

**Solution**: 
1. Check that `.env` file exists
2. Verify API key is correctly set in `.env`
3. Ensure `.env` is in the project root directory

### Issue: GitHub API rate limits

**Solution**: 
- Add GitHub token to `.env` for higher rate limits
- Wait for rate limit reset (usually 1 hour)
- Use authenticated requests for better limits

### Issue: Import errors

**Solution**: 
- Ensure Python 3.9+ is being used: `python --version`
- Reinstall dependencies: `pip install --upgrade -r requirements.txt`
- Check virtual environment is activated

### Issue: Proxy/Network errors

**Solution**:
- Check internet connection
- Configure proxy settings if behind corporate firewall
- Try from different network

## System Requirements

### Minimum Requirements:
- Python 3.9+
- 2GB RAM
- Internet connection
- 500MB disk space

### Recommended:
- Python 3.10+
- 4GB RAM
- Stable internet connection
- 1GB disk space

## Platform-Specific Notes

### Windows
- Use PowerShell or Command Prompt
- Path separators: `\` or `/` both work
- Virtual environment activation: `venv\Scripts\activate`

### macOS/Linux
- Use Terminal
- Path separators: `/`
- Virtual environment activation: `source venv/bin/activate`

## Next Steps

After installation:
1. Read the README.md for usage examples
2. Try analyzing a sample repository
3. Review the example output in supplementary materials
4. Customize agent prompts if needed

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review error messages carefully
3. Check GitHub Issues: https://github.com/ArnabSen08/publication-assistant/issues
4. Review documentation in README.md

## Uninstallation

To remove the system:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Remove repository (optional)
cd ..
rm -rf publication-assistant
```
