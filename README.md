# Publication Assistant for AI Projects

A multi-agent system that helps improve how AI/ML projects are presented for public sharing. The system analyzes GitHub repositories and provides practical suggestions to enhance discoverability, clarity, and completeness.

## 🎯 Project Overview

This project implements a multi-agent system using LangGraph orchestration to analyze GitHub repositories and provide actionable recommendations for improving project documentation, metadata, and presentation.

## 🤖 Agents

The system consists of four specialized agents working together:

1. **Repo Analyzer Agent** - Parses and interprets README files, code structure, and repository organization
2. **Metadata Recommender Agent** - Suggests relevant tags, categories, and keywords based on project content
3. **Content Improver Agent** - Proposes better titles, summaries, and introductions
4. **Reviewer Agent** - Checks for missing sections, unclear areas, and structural issues

## 🛠️ Tools Integrated

1. **GitHub API Tool** - Fetches repository information, README content, and file structure
2. **Web Search Tool** - Searches for similar projects and best practices
3. **Keyword Extractor Tool** - Extracts and analyzes keywords from project content
4. **Text Processing Tool** - Analyzes text quality, readability, and structure

## 📋 Requirements

- Python 3.9+
- OpenAI API key (or compatible LLM provider)
- GitHub Personal Access Token (optional, for private repos)

## 🚀 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd publication-assistant
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env_example .env
   # Edit .env and add your API keys
   ```

5. **Run the system:**
   ```bash
   python main.py
   ```

## 📝 Usage Example

```python
from agents.orchestrator import MultiAgentOrchestrator

# Initialize the orchestrator
orchestrator = MultiAgentOrchestrator()

# Analyze a GitHub repository
result = orchestrator.analyze_repository(
    repo_url="https://github.com/username/repo-name",
    project_description="A machine learning project for image classification"
)

# Print recommendations
print(result)
```

## 📁 Project Structure

```
publication-assistant/
├── agents/
│   ├── __init__.py
│   ├── repo_analyzer.py
│   ├── metadata_recommender.py
│   ├── content_improver.py
│   └── reviewer.py
├── tools/
│   ├── __init__.py
│   ├── github_tool.py
│   ├── web_search_tool.py
│   ├── keyword_extractor.py
│   └── text_processor.py
├── agents/
│   ├── __init__.py
│   └── orchestrator.py
├── main.py
├── requirements.txt
├── .env_example
├── .gitignore
└── README.md
```

## 🔧 Configuration

The system uses environment variables for configuration. See `.env_example` for required variables:

- `OPENAI_API_KEY` - Your OpenAI API key
- `GITHUB_TOKEN` - GitHub Personal Access Token (optional)
- `SEARCH_API_KEY` - API key for web search (optional)

## 🎓 Learning Objectives Demonstrated

- **Multi-Agent Collaboration**: Four agents with distinct roles working together
- **Agent Orchestration**: LangGraph framework for workflow management
- **Tool Integration**: Four different tools extending agent capabilities
- **Communication Flow**: Clear coordination between agents through shared state

## 📊 Sample Output

The system provides:
- Repository analysis summary
- Metadata recommendations (tags, categories, keywords)
- Content improvement suggestions (titles, summaries, intros)
- Review feedback (missing sections, unclear areas)

## 🤝 Contributing

This is a capstone project for the Mastering AI Agents Certification Program. For questions or improvements, please open an issue or submit a pull request.

## 📄 License

This project is part of the Ready Tensor Mastering AI Agents Certification Program.

## 🙏 Acknowledgments

Built as part of the Ready Tensor Mastering AI Agents Certification Program capstone project.
