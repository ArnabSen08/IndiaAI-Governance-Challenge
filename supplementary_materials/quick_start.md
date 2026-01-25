# Quick Start Guide

Get up and running with the Publication Assistant in 5 minutes!

## Prerequisites Check

```bash
python --version  # Should be 3.9 or higher
```

## Installation (3 steps)

```bash
# 1. Clone and enter directory
git clone https://github.com/ArnabSen08/publication-assistant.git
cd publication-assistant

# 2. Create virtual environment and install
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Set up API key
cp .env_example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here
```

## Basic Usage

### Option 1: Interactive Mode

```bash
python main.py
# Enter repository URL when prompted
```

### Option 2: Python Script

```python
from orchestrator import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator()
result = orchestrator.analyze_repository(
    repo_url="https://github.com/langchain-ai/langchain"
)

print(result["report"])
```

## Example Output

The system will provide:
- ✅ Repository analysis
- ✅ Metadata recommendations (tags, keywords)
- ✅ Content improvements (titles, descriptions)
- ✅ Review feedback (missing sections, unclear areas)

## Common Commands

```bash
# Run example
python example_usage.py

# Check installation
python -c "from orchestrator import MultiAgentOrchestrator; print('OK')"

# View help
python main.py --help
```

## Next Steps

- Read full README.md for detailed documentation
- Check supplementary_materials/ for examples
- Customize agent prompts in agents/ directory
- Add your own tools in tools/ directory

## Troubleshooting

**No API key?** Get one at https://platform.openai.com/api-keys  
**Import errors?** Run `pip install -r requirements.txt`  
**Proxy issues?** See PUSH_AND_PAGES_GUIDE.md

---

**That's it!** You're ready to analyze GitHub repositories. 🚀
