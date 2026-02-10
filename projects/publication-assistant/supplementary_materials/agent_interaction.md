# Agent Interaction and Communication Patterns

## Agent Communication Model

The multi-agent system uses a **shared state** communication model where agents communicate through a centralized state dictionary managed by the LangGraph orchestrator.

## Communication Flow

### 1. Sequential Information Flow

```
Repo Analyzer → Metadata Recommender → Content Improver → Reviewer
     │                  │                     │                │
     └──────────────────┴─────────────────────┴────────────────┘
                              │
                         Shared State
```

### 2. State Sharing Mechanism

Each agent reads from and writes to the shared `AgentState`:

```python
AgentState = {
    "repo_url": str,                    # Input from user
    "project_description": str,         # Input from user
    "repo_analysis": str,               # Output from Repo Analyzer
    "project_content": str,              # Output from Repo Analyzer
    "metadata_recommendations": str,      # Output from Metadata Recommender
    "content_improvements": str,          # Output from Content Improver
    "review_feedback": str,              # Output from Reviewer
    "final_report": str,                 # Output from Report Generator
    "step": str,                         # Current workflow step
    "errors": List[str]                  # Error tracking
}
```

## Agent Responsibilities

### Repo Analyzer Agent
**Input**: repo_url, project_description  
**Output**: repo_analysis, project_content  
**Tools Used**: GitHubTool, TextProcessorTool  
**Information Provided To**: All subsequent agents

**Key Outputs**:
- Repository structure analysis
- README content summary
- Technology stack identification
- Documentation quality assessment

### Metadata Recommender Agent
**Input**: project_content, repo_analysis  
**Output**: metadata_recommendations  
**Tools Used**: KeywordExtractorTool, WebSearchTool  
**Information Consumed From**: Repo Analyzer  
**Information Provided To**: Content Improver, Reviewer

**Key Outputs**:
- Suggested tags (10-15)
- Category recommendations
- Keywords for search optimization
- Similar project patterns

### Content Improver Agent
**Input**: project_content, repo_analysis  
**Output**: content_improvements  
**Tools Used**: TextProcessorTool, WebSearchTool  
**Information Consumed From**: Repo Analyzer, Metadata Recommender  
**Information Provided To**: Reviewer

**Key Outputs**:
- Alternative title suggestions
- Improved project descriptions
- Introduction section recommendations
- Structural improvement suggestions

### Reviewer Agent
**Input**: project_content, suggestions (metadata + content), repo_url  
**Output**: review_feedback  
**Tools Used**: TextProcessorTool, GitHubTool  
**Information Consumed From**: All previous agents  
**Information Provided To**: Report Generator

**Key Outputs**:
- Missing section identification
- Unclear area detection
- Suggestion validation
- Completeness assessment

## Information Dependency Graph

```
                    User Input
                    (repo_url)
                         │
                         ▼
              ┌──────────────────────┐
              │   Repo Analyzer    │
              │  (Independent)     │
              └──────────┬─────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Metadata   │  │   Content    │  │   Reviewer   │
│ Recommender  │  │  Improver    │  │   (waits)    │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                  │
       └─────────────────┴──────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   Reviewer   │
                  │  (validates) │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │    Report    │
                  │  Generator   │
                  └──────────────┘
```

## Coordination Patterns

### 1. Sequential Processing
Agents execute in a fixed order, with each building upon previous results.

### 2. State Accumulation
Each agent adds to the shared state without overwriting previous information.

### 3. Error Propagation
Errors are collected in the state and don't stop the workflow.

### 4. Context Preservation
All agent outputs are preserved for final report generation.

## Tool Sharing

While agents have access to different tools, some tools are shared:

- **TextProcessorTool**: Used by Repo Analyzer, Content Improver, and Reviewer
- **GitHubTool**: Used by Repo Analyzer and Reviewer
- **WebSearchTool**: Used by Metadata Recommender and Content Improver
- **KeywordExtractorTool**: Used exclusively by Metadata Recommender

## Benefits of This Architecture

1. **Clear Separation of Concerns**: Each agent has a specific role
2. **Information Reuse**: Agents build upon previous analyses
3. **Modularity**: Agents can be modified independently
4. **Traceability**: All information flows through shared state
5. **Error Resilience**: Failures in one agent don't break the workflow
