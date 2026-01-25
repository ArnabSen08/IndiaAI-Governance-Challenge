# System Architecture Diagram

## Multi-Agent System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Multi-Agent Orchestrator                  │
│                      (LangGraph Framework)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ State Management
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Repo Analyzer │    │   Metadata    │    │   Content    │
│    Agent      │───▶│ Recommender   │───▶│  Improver     │
│               │    │    Agent      │    │    Agent      │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                     │
        │ Tools:             │ Tools:              │ Tools:
        │ - GitHub API      │ - Keyword Extractor │ - Text Processor
        │ - Text Processor  │ - Web Search        │ - Web Search
        └───────────────────┴─────────────────────┘
                              │
                              ▼
                    ┌───────────────┐
                    │  Reviewer     │
                    │    Agent      │
                    └───────┬───────┘
                            │
                            │ Tools:
                            │ - Text Processor
                            │ - GitHub API
                            │
                            ▼
                    ┌───────────────┐
                    │  Final Report  │
                    │   Generation  │
                    └───────────────┘
```

## Component Details

### Orchestrator Layer
- **Framework**: LangGraph
- **State Management**: Typed dictionary (AgentState)
- **Workflow**: Sequential with state sharing

### Agent Layer
1. **Repo Analyzer**: Initial analysis and information extraction
2. **Metadata Recommender**: Tag and keyword suggestions
3. **Content Improver**: Title and description enhancements
4. **Reviewer**: Validation and completeness checking

### Tool Layer
- **GitHub API Tool**: Repository data access
- **Web Search Tool**: External information retrieval
- **Keyword Extractor**: YAKE-based keyword extraction
- **Text Processor**: Readability and structure analysis

## Data Flow

1. User provides repository URL → Orchestrator
2. Orchestrator → Repo Analyzer (with URL)
3. Repo Analyzer → Tools (GitHub API, Text Processor)
4. Analysis results → State
5. State → Metadata Recommender
6. Metadata Recommender → Tools (Keyword Extractor, Web Search)
7. Recommendations → State
8. State → Content Improver
9. Content Improver → Tools (Text Processor, Web Search)
10. Improvements → State
11. State → Reviewer
12. Reviewer → Tools (Text Processor, GitHub API)
13. Review → State
14. State → Final Report Generation
15. Report → User
