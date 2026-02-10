# API Reference

## Overview

The Multi-Agent AI System provides a comprehensive API for interacting with specialized AI agents through a coordinated workflow system.

## Core Components

### CoordinatorAgent

The main orchestrator that manages workflow execution and agent communication.

#### Methods

##### `process(input_data: Dict[str, Any]) -> Dict[str, Any]`

Processes a task through the multi-agent workflow.

**Parameters:**
- `input_data`: Dictionary containing task information
  - `task` (str): The main task description
  - `context` (dict, optional): Additional context information

**Returns:**
- Dictionary with workflow results:
  - `success` (bool): Whether the workflow completed successfully
  - `result` (dict): Workflow execution results
  - `workflow_plan` (dict): The executed workflow plan
  - `agent` (str): Agent identifier

**Example:**
```python
input_data = {
    "task": "Explain machine learning basics",
    "context": {"audience": "beginners"}
}
result = await coordinator.process(input_data)
```

##### `get_all_agent_metrics() -> Dict[str, Any]`

Returns performance metrics for all agents in the system.

##### `health_check_all_agents() -> Dict[str, Any]`

Performs health checks on all agents and returns system status.

### ResearchAgent

Specialized agent for information gathering and analysis.

#### Methods

##### `process(input_data: Dict[str, Any]) -> Dict[str, Any]`

Performs research based on the input query.

**Parameters:**
- `input_data`: Dictionary containing research parameters
  - `query` (str): Research query
  - `research_type` (str): Type of research ("general", "factual", "analytical", "comparative")

**Returns:**
- Dictionary with research results:
  - `success` (bool): Whether research completed successfully
  - `findings` (str): Research findings
  - `confidence` (str): Confidence level ("high", "medium", "low")

### ContentAgent

Specialized agent for content generation and refinement.

#### Methods

##### `process(input_data: Dict[str, Any]) -> Dict[str, Any]`

Generates content based on the input request.

**Parameters:**
- `input_data`: Dictionary containing content parameters
  - `content_request` (str): Content generation request
  - `content_type` (str): Type of content ("explanation", "summary", "analysis", "creative", "technical")
  - `style` (str): Writing style ("professional", "casual", "academic", "technical", "creative")
  - `length` (str): Content length ("short", "medium", "long", "extended")

**Returns:**
- Dictionary with generated content:
  - `success` (bool): Whether content generation completed successfully
  - `content` (str): Generated content
  - `word_count` (int): Number of words in generated content

##### `refine_content(content: str, refinement_instructions: str) -> Dict[str, Any]`

Refines existing content based on specific instructions.

### ValidationAgent

Specialized agent for quality assurance and safety validation.

#### Methods

##### `process(input_data: Dict[str, Any]) -> Dict[str, Any]`

Validates content for safety and quality.

**Parameters:**
- `input_data`: Dictionary containing validation parameters
  - `content` (str): Content to validate
  - `validation_type` (str): Type of validation ("safety", "quality", "technical", "comprehensive")
  - `strict_mode` (bool): Whether to use strict validation rules

**Returns:**
- Dictionary with validation results:
  - `success` (bool): Whether validation completed successfully
  - `validation_passed` (bool): Whether content passed validation
  - `safety_score` (float): Safety score (0-100)
  - `quality_score` (float): Quality score (0-100)
  - `issues` (list): List of identified issues
  - `recommendations` (list): Improvement recommendations

## Configuration

### Config Class

Manages system configuration with validation and environment variable support.

#### Key Parameters

- `openai_api_key` (str): OpenAI API key (required)
- `openai_model` (str): Model to use (default: "gpt-4")
- `max_retries` (int): Maximum retry attempts (default: 3)
- `timeout_seconds` (int): Request timeout (default: 30)
- `log_level` (str): Logging level (default: "INFO")
- `enable_input_validation` (bool): Enable input validation (default: True)
- `enable_output_filtering` (bool): Enable output filtering (default: True)

## Health Monitoring

### HealthChecker Class

Provides comprehensive system health monitoring.

#### Methods

##### `check_system_health() -> Dict[str, Any]`

Performs comprehensive system health check including:
- API connectivity
- System resources (memory, disk, CPU)
- File system permissions
- Configuration validation

##### `get_system_metrics() -> Dict[str, Any]`

Returns current system resource metrics.

## Error Handling

The system implements comprehensive error handling:

### Retry Logic
- Automatic retry with exponential backoff
- Configurable retry limits
- Graceful degradation on persistent failures

### Input Validation
- Type checking and format validation
- Length limits and content filtering
- Sanitization of user inputs

### Output Filtering
- Safety pattern detection
- Content filtering for sensitive information
- Quality assurance checks

## Usage Examples

### Basic Usage

```python
from src.agents.coordinator_agent import CoordinatorAgent
from src.core.config import Config
from src.utils.logger import setup_logger

# Initialize system
config = Config(openai_api_key="your_api_key")
logger = setup_logger()
coordinator = CoordinatorAgent(config, logger)

# Process a task
input_data = {"task": "Explain renewable energy benefits"}
result = await coordinator.process(input_data)

if result["success"]:
    print(result["result"]["final_output"])
```

### Research-Specific Usage

```python
from src.agents.research_agent import ResearchAgent

research_agent = ResearchAgent(config, logger)

# Factual research
research_input = {
    "query": "Current renewable energy statistics",
    "research_type": "factual"
}
result = await research_agent.process(research_input)
```

### Content Generation

```python
from src.agents.content_agent import ContentAgent

content_agent = ContentAgent(config, logger)

# Generate technical documentation
content_input = {
    "content_request": "API documentation for user authentication",
    "content_type": "technical",
    "style": "technical",
    "length": "long"
}
result = await content_agent.process(content_input)
```

### Content Validation

```python
from src.agents.validation_agent import ValidationAgent

validation_agent = ValidationAgent(config, logger)

# Comprehensive validation
validation_input = {
    "content": "Content to validate...",
    "validation_type": "comprehensive",
    "strict_mode": True
}
result = await validation_agent.process(validation_input)
```

## Rate Limiting and Performance

### Rate Limiting
- Configurable request limits per time window
- Automatic throttling to prevent API overuse
- Queue management for high-volume scenarios

### Performance Optimization
- Response caching for research queries
- Efficient resource utilization
- Concurrent request handling

### Monitoring
- Real-time performance metrics
- Success/failure rate tracking
- Response time monitoring
- Resource usage statistics

## Security Considerations

### Input Security
- Input sanitization and validation
- Length limits and type checking
- Pattern-based content filtering

### Output Security
- Sensitive information detection
- Content safety validation
- Audit logging for compliance

### API Security
- Secure API key management
- Request authentication
- Rate limiting protection