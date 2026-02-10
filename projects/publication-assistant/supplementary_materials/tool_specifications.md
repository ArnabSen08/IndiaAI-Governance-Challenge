# Tool Specifications

Detailed specifications for all tools integrated into the multi-agent system.

## 1. GitHub API Tool

### Purpose
Fetches repository information, README content, and file structure from GitHub.

### Implementation
- **Library**: PyGithub
- **Authentication**: Optional (GitHub Personal Access Token)
- **Rate Limits**: Subject to GitHub API limits (5000 requests/hour for authenticated)

### Actions Supported

#### `readme`
- Fetches and decodes README file content
- Returns UTF-8 decoded text
- Handles missing README gracefully

#### `structure`
- Lists repository structure (first 20 items)
- Shows file/directory types
- Provides overview of project organization

#### `files`
- Lists key files (Python, Markdown, Text, JSON)
- Limited to first 15 files
- Focuses on documentation and code files

#### `info`
- Retrieves repository metadata:
  - Name, description
  - Primary language
  - Star and fork counts
  - Topics/tags
  - Creation and update dates

### Input Schema
```python
{
    "repo_url": str,  # GitHub repository URL
    "action": str     # "readme", "structure", "files", or "info"
}
```

### Error Handling
- Invalid URL format detection
- Missing repository handling
- API rate limit awareness
- Graceful degradation when token not provided

---

## 2. Web Search Tool

### Purpose
Searches the web for similar projects and best practices.

### Implementation
- **Provider**: DuckDuckGo HTML search (no API key required)
- **Fallback**: Can be extended with paid APIs (SerpAPI, Google Custom Search)
- **Results**: Up to 5 results per query

### Features
- Extracts title, URL, and snippet from search results
- No authentication required
- Free to use
- Can be upgraded to paid APIs for better results

### Input Schema
```python
{
    "query": str,        # Search query string
    "max_results": int   # Maximum results (default: 5)
}
```

### Output Format
```
Web Search Results for 'query':
Title: [title]
URL: [url]
Snippet: [description]

---
[Next result...]
```

### Limitations
- HTML parsing may be fragile
- Limited to 5 results
- No advanced search features
- Rate limits may apply

### Future Enhancements
- Integration with SerpAPI for better results
- Support for image search
- Advanced query options

---

## 3. Keyword Extractor Tool

### Purpose
Extracts relevant keywords and key phrases from text content.

### Implementation
- **Algorithm**: YAKE (Yet Another Keyword Extractor)
- **Language**: Configurable (default: English)
- **N-gram Size**: 3
- **Deduplication Limit**: 0.7

### Features
- Unsupervised keyword extraction
- No training data required
- Language-agnostic (supports multiple languages)
- Configurable keyword count

### Input Schema
```python
{
    "text": str,           # Text content to analyze
    "max_keywords": int,    # Maximum keywords (default: 10)
    "language": str         # Language code (default: "en")
}
```

### Output Format
```
Extracted Keywords:
  - keyword1 (score: 0.0234)
  - keyword2 (score: 0.0187)
  ...
```

### Algorithm Details
- YAKE uses statistical features:
  - Term frequency
  - Term position
  - Term relatedness to context
  - Term different sentence
- Lower scores indicate better keywords

### Use Cases
- Tag generation
- Search optimization
- Content categorization
- Topic identification

---

## 4. Text Processor Tool

### Purpose
Analyzes text quality, readability, and structural elements.

### Implementation
- **Library**: TextStat
- **Metrics**: Multiple readability indices
- **Analysis Types**: Readability, Statistics, Structure

### Analysis Types

#### Readability Analysis
- **Flesch Reading Ease**: 0-100 scale
  - 90-100: Very Easy
  - 80-89: Easy
  - 70-79: Fairly Easy
  - 60-69: Standard
  - 50-59: Fairly Difficult
  - 30-49: Difficult
  - 0-29: Very Difficult

- **Flesch-Kincaid Grade Level**: U.S. school grade level
- **SMOG Index**: Estimates years of education needed

#### Statistics Analysis
- Character count
- Word count
- Sentence count
- Syllable count
- Average words per sentence

#### Structure Analysis
- Common README sections detection:
  - Installation
  - Usage
  - Features
  - Requirements
  - Contributing
  - License
  - Examples
  - Documentation
- Heading presence
- Code block presence
- Link presence

### Input Schema
```python
{
    "text": str,              # Text to analyze
    "analysis_type": str      # "readability", "statistics", "structure", or "all"
}
```

### Output Format
```
Readability Metrics:
  - Flesch Reading Ease: 65.23 (Standard)
  - Flesch-Kincaid Grade Level: 8.5
  - SMOG Index: 9.2

Text Statistics:
  - Characters: 5,234
  - Words: 892
  - Sentences: 45
  - Syllables: 1,234
  - Avg words per sentence: 19.82

Structure Analysis:
  - Common sections found: installation, usage, features
  - Has headings: Yes
  - Has code blocks: Yes
  - Has links: Yes
```

### Use Cases
- Documentation quality assessment
- Readability improvement
- Structure completeness checking
- Content analysis

---

## Tool Integration Summary

| Tool | Used By Agents | Primary Purpose | Dependencies |
|------|---------------|-----------------|--------------|
| GitHub API | Repo Analyzer, Reviewer | Repository data access | PyGithub, GitHub Token (optional) |
| Web Search | Metadata Recommender, Content Improver | External information | requests, beautifulsoup4 |
| Keyword Extractor | Metadata Recommender | Keyword extraction | yake |
| Text Processor | Repo Analyzer, Content Improver, Reviewer | Text analysis | textstat |

## Error Handling Strategy

All tools implement:
- Try-catch blocks for API failures
- Graceful degradation when services unavailable
- Clear error messages returned to agents
- No exceptions propagated to orchestration layer

## Performance Considerations

- **GitHub API**: Rate limits require careful usage
- **Web Search**: Network latency may affect response time
- **Keyword Extractor**: Fast, local processing
- **Text Processor**: Fast, local processing

## Future Tool Additions

Potential tools for extension:
- Image Generator (for diagrams)
- ArXiv/Scholar API (for research papers)
- RAG Retriever (for knowledge base queries)
- File Parser (for code analysis)
