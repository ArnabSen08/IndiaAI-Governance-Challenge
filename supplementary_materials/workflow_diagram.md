# LangGraph Workflow Diagram

## State Machine Workflow

```
                    START
                      │
                      ▼
        ┌─────────────────────────┐
        │   Initialize State      │
        │  - repo_url             │
        │  - project_description  │
        │  - errors = []          │
        └─────────────┬───────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │  analyze_repo_node      │
        │  (Repo Analyzer Agent)  │
        │  - Fetch README         │
        │  - Analyze structure    │
        │  - Extract info         │
        └─────────────┬───────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │ recommend_metadata_node │
        │ (Metadata Recommender)  │
        │  - Extract keywords     │
        │  - Search similar       │
        │  - Suggest tags         │
        └─────────────┬───────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │ improve_content_node    │
        │  (Content Improver)     │
        │  - Analyze quality      │
        │  - Propose titles       │
        │  - Improve descriptions │
        └─────────────┬───────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │    review_node          │
        │    (Reviewer Agent)     │
        │  - Validate suggestions │
        │  - Check completeness   │
        │  - Verify accuracy      │
        └─────────────┬───────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │ generate_report_node    │
        │  - Consolidate results  │
        │  - Format output        │
        │  - Include errors       │
        └─────────────┬───────────┘
                      │
                      ▼
                     END
```

## State Transitions

### State Dictionary Structure
```python
{
    "repo_url": str,
    "project_description": str,
    "repo_analysis": str,
    "project_content": str,
    "metadata_recommendations": str,
    "content_improvements": str,
    "review_feedback": str,
    "final_report": str,
    "step": str,
    "errors": List[str]
}
```

### Node Execution Flow

1. **analyze_repo_node**
   - Input: repo_url, project_description
   - Output: repo_analysis, project_content
   - Tools: GitHubTool, TextProcessorTool

2. **recommend_metadata_node**
   - Input: project_content, repo_analysis
   - Output: metadata_recommendations
   - Tools: KeywordExtractorTool, WebSearchTool

3. **improve_content_node**
   - Input: project_content, repo_analysis
   - Output: content_improvements
   - Tools: TextProcessorTool, WebSearchTool

4. **review_node**
   - Input: project_content, suggestions, repo_url
   - Output: review_feedback
   - Tools: TextProcessorTool, GitHubTool

5. **generate_report_node**
   - Input: All previous outputs
   - Output: final_report
   - No tools required

## Error Handling

- Each node catches exceptions
- Errors added to state["errors"] list
- Workflow continues even if individual nodes fail
- Final report includes error summary
