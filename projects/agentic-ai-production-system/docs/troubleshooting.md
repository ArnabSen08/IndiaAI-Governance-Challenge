# Troubleshooting Guide

## Overview

This guide helps diagnose and resolve common issues with the Multi-Agent AI System.

## Quick Diagnostics

### System Health Check

Run the built-in health check to identify issues:

```python
from src.core.health import HealthChecker
from src.core.config import Config

config = Config()
health_checker = HealthChecker(config)
health_status = health_checker.check_system_health()

print(f"System Healthy: {health_status['healthy']}")
if not health_status['healthy']:
    print(f"Issues: {health_status['issues']}")
```

### Log Analysis

Check application logs for errors:

```bash
# View recent logs
tail -f logs/app.log

# Search for errors
grep -i error logs/app.log

# Search for specific patterns
grep -i "timeout\|failed\|exception" logs/app.log
```

## Common Issues and Solutions

### 1. API Connection Issues

#### Symptoms
- "API connectivity failed" in health check
- Connection timeout errors
- Authentication failures

#### Causes and Solutions

**Invalid API Key**
```
Error: "OpenAI API key must be provided" or "Incorrect API key"
```

*Solution:*
1. Verify your API key in `.env` file
2. Ensure no extra spaces or characters
3. Check API key permissions on OpenAI platform
4. Regenerate API key if necessary

```bash
# Check current API key (first few characters)
echo $OPENAI_API_KEY | cut -c1-10
```

**Network Connectivity Issues**
```
Error: "Connection timeout" or "Network unreachable"
```

*Solution:*
1. Check internet connection
2. Verify firewall settings
3. Check proxy configuration
4. Test direct API access:

```bash
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

**Rate Limiting**
```
Error: "Rate limit exceeded" or "Too many requests"
```

*Solution:*
1. Reduce request frequency
2. Implement exponential backoff
3. Check your API usage limits
4. Upgrade API plan if needed

```python
# Adjust rate limiting in config
MAX_RETRIES=5
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW=60
```

### 2. Memory and Performance Issues

#### Symptoms
- Slow response times
- Out of memory errors
- High CPU usage
- Application crashes

#### Causes and Solutions

**Insufficient Memory**
```
Error: "MemoryError" or "System resources low"
```

*Solution:*
1. Check system memory usage:
```bash
# Linux/macOS
free -h
top

# Windows
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory
```

2. Increase available memory:
   - Close unnecessary applications
   - Increase container memory limits
   - Add swap space if needed

3. Optimize application memory usage:
```python
# Clear agent caches periodically
coordinator.research_agent.clear_cache()

# Reduce batch sizes
MAX_ITERATIONS=5  # Reduce from default 10
```

**High CPU Usage**
```
Symptom: CPU usage consistently above 90%
```

*Solution:*
1. Monitor CPU usage:
```bash
# Check CPU usage
htop  # or top on basic systems
```

2. Optimize processing:
   - Reduce concurrent requests
   - Increase timeout values
   - Use async processing where possible

```python
# Adjust configuration
TIMEOUT_SECONDS=60  # Increase from 30
MAX_ITERATIONS=3    # Reduce complexity
```

**Disk Space Issues**
```
Error: "No space left on device" or "Disk full"
```

*Solution:*
1. Check disk usage:
```bash
df -h
du -sh logs/
```

2. Clean up space:
```bash
# Rotate logs
find logs/ -name "*.log" -mtime +7 -delete

# Clean temporary files
rm -rf /tmp/streamlit-*
```

3. Configure log rotation:
```python
# In logging configuration
'file': {
    'class': 'logging.handlers.RotatingFileHandler',
    'maxBytes': 10485760,  # 10MB
    'backupCount': 5
}
```

### 3. Configuration Issues

#### Symptoms
- "Configuration issues" in health check
- Validation errors on startup
- Unexpected behavior

#### Causes and Solutions

**Missing Environment Variables**
```
Error: "Missing required configuration"
```

*Solution:*
1. Check `.env` file exists and is properly formatted:
```bash
# Verify .env file
cat .env | grep -v "^#" | grep "="
```

2. Ensure all required variables are set:
```bash
# Required variables checklist
echo "OPENAI_API_KEY: ${OPENAI_API_KEY:+SET}"
echo "LOG_LEVEL: ${LOG_LEVEL:-INFO}"
```

**Invalid Configuration Values**
```
Error: "Invalid log level" or "Value out of range"
```

*Solution:*
1. Validate configuration values:
```python
# Check valid log levels
valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# Check numeric ranges
assert 1 <= MAX_RETRIES <= 10
assert 5 <= TIMEOUT_SECONDS <= 300
```

2. Reset to defaults if needed:
```bash
# Reset problematic values
export LOG_LEVEL=INFO
export MAX_RETRIES=3
export TIMEOUT_SECONDS=30
```

### 4. Agent Processing Issues

#### Symptoms
- Agents returning errors
- Workflow failures
- Inconsistent results

#### Causes and Solutions

**Agent Initialization Failures**
```
Error: "Agent failed to initialize"
```

*Solution:*
1. Check agent dependencies:
```python
# Test individual agent initialization
from src.agents.research_agent import ResearchAgent
from src.core.config import Config
from src.utils.logger import setup_logger

config = Config(openai_api_key="test_key")
logger = setup_logger()

try:
    agent = ResearchAgent(config, logger)
    print("Agent initialized successfully")
except Exception as e:
    print(f"Agent initialization failed: {e}")
```

2. Verify configuration compatibility:
```python
# Check agent-specific requirements
assert config.max_input_length > 0
assert config.enable_input_validation in [True, False]
```

**Input Validation Failures**
```
Error: "Invalid input data" or "Input too long"
```

*Solution:*
1. Check input format:
```python
# Correct input format
valid_input = {
    "task": "Your task description",
    "context": {"key": "value"}  # Optional
}

# Check input length
assert len(input_data.get("task", "")) <= config.max_input_length
```

2. Sanitize inputs:
```python
def sanitize_input(text):
    # Remove excessive whitespace
    text = " ".join(text.split())
    # Limit length
    if len(text) > 10000:
        text = text[:10000] + "..."
    return text
```

**LLM Request Failures**
```
Error: "LLM request failed" or "Timeout"
```

*Solution:*
1. Check request parameters:
```python
# Verify message format
messages = [
    {"role": "system", "content": "System prompt"},
    {"role": "user", "content": "User message"}
]

# Check for empty or invalid content
for msg in messages:
    assert msg.get("content", "").strip()
```

2. Adjust timeout and retry settings:
```python
# Increase timeouts for complex requests
TIMEOUT_SECONDS=60
MAX_RETRIES=5
```

### 5. Web Interface Issues

#### Symptoms
- Streamlit errors
- UI not loading
- Session state issues

#### Causes and Solutions

**Streamlit Port Conflicts**
```
Error: "Port 8501 is already in use"
```

*Solution:*
1. Find and kill existing processes:
```bash
# Find process using port 8501
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

2. Use different port:
```bash
streamlit run app.py --server.port 8502
```

**Session State Issues**
```
Error: Session state corruption or unexpected behavior
```

*Solution:*
1. Clear session state:
```python
# In Streamlit app
if st.button("Clear Session"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
```

2. Reset application:
```bash
# Restart Streamlit
Ctrl+C  # Stop current session
streamlit run app.py  # Restart
```

**Import Errors**
```
Error: "ModuleNotFoundError" or "ImportError"
```

*Solution:*
1. Check Python path:
```python
import sys
print(sys.path)

# Add src to path if needed
sys.path.append("src")
```

2. Verify package installation:
```bash
pip list | grep streamlit
pip install -r requirements.txt --upgrade
```

### 6. Testing Issues

#### Symptoms
- Test failures
- Import errors in tests
- Mocking issues

#### Causes and Solutions

**Test Environment Setup**
```
Error: Tests failing due to missing dependencies
```

*Solution:*
1. Install test dependencies:
```bash
pip install pytest pytest-cov pytest-asyncio
```

2. Set up test environment:
```bash
# Create test configuration
export OPENAI_API_KEY=test_key_for_testing
export LOG_LEVEL=DEBUG
```

**Async Test Issues**
```
Error: "RuntimeError: This event loop is already running"
```

*Solution:*
1. Use proper async test decorators:
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

2. Handle event loops properly:
```python
import asyncio

# For non-pytest environments
def test_with_event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(async_function())
        assert result is not None
    finally:
        loop.close()
```

## Debugging Techniques

### 1. Enable Debug Logging

```python
# Set debug level
import logging
logging.basicConfig(level=logging.DEBUG)

# Or via environment
export LOG_LEVEL=DEBUG
export DEBUG_MODE=true
```

### 2. Add Diagnostic Prints

```python
# Add debug prints to trace execution
def debug_process(self, input_data):
    print(f"DEBUG: Processing input: {input_data}")
    result = self.original_process(input_data)
    print(f"DEBUG: Result: {result}")
    return result
```

### 3. Use Python Debugger

```python
# Add breakpoint for debugging
import pdb; pdb.set_trace()

# Or use modern debugger
import ipdb; ipdb.set_trace()
```

### 4. Monitor Resource Usage

```python
import psutil
import time

def monitor_resources():
    while True:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        print(f"CPU: {cpu}%, Memory: {memory}%")
        time.sleep(5)
```

## Performance Optimization

### 1. Identify Bottlenecks

```python
import time
import functools

def timing_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

# Apply to agent methods
@timing_decorator
async def process(self, input_data):
    # ... existing code
```

### 2. Optimize Memory Usage

```python
# Clear caches periodically
def cleanup_caches():
    for agent in self.agents.values():
        if hasattr(agent, 'clear_cache'):
            agent.clear_cache()

# Limit history size
def limit_history(self, max_size=100):
    if len(self.workflow_history) > max_size:
        self.workflow_history = self.workflow_history[-max_size:]
```

### 3. Implement Caching

```python
from functools import lru_cache
import hashlib

class CachedAgent:
    def __init__(self):
        self.cache = {}
    
    def get_cache_key(self, input_data):
        return hashlib.md5(str(input_data).encode()).hexdigest()
    
    async def process_with_cache(self, input_data):
        cache_key = self.get_cache_key(input_data)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = await self.process(input_data)
        self.cache[cache_key] = result
        return result
```

## Monitoring and Alerting

### 1. Set Up Health Monitoring

```python
import time
import threading

class HealthMonitor:
    def __init__(self, system, interval=30):
        self.system = system
        self.interval = interval
        self.running = False
    
    def start_monitoring(self):
        self.running = True
        thread = threading.Thread(target=self._monitor_loop)
        thread.daemon = True
        thread.start()
    
    def _monitor_loop(self):
        while self.running:
            health = self.system.check_health()
            if not health['healthy']:
                self._send_alert(health['issues'])
            time.sleep(self.interval)
    
    def _send_alert(self, issues):
        print(f"ALERT: System issues detected: {issues}")
        # Implement actual alerting (email, Slack, etc.)
```

### 2. Log Analysis

```bash
# Create log analysis script
#!/bin/bash

# Count errors by type
grep -i error logs/app.log | cut -d' ' -f4- | sort | uniq -c | sort -nr

# Find performance issues
grep -i "timeout\|slow\|failed" logs/app.log | tail -20

# Monitor memory usage
grep -i "memory" logs/app.log | tail -10
```

## Recovery Procedures

### 1. Automatic Recovery

```python
class AutoRecovery:
    def __init__(self, system):
        self.system = system
        self.recovery_attempts = 0
        self.max_attempts = 3
    
    async def attempt_recovery(self, error):
        if self.recovery_attempts >= self.max_attempts:
            raise Exception("Max recovery attempts exceeded")
        
        self.recovery_attempts += 1
        
        if "memory" in str(error).lower():
            await self._recover_memory()
        elif "api" in str(error).lower():
            await self._recover_api()
        else:
            await self._generic_recovery()
    
    async def _recover_memory(self):
        # Clear caches, restart components
        self.system.clear_all_caches()
        
    async def _recover_api(self):
        # Reset connections, check credentials
        await self.system.reset_api_connections()
```

### 2. Manual Recovery Steps

1. **System Restart**
```bash
# Stop application
pkill -f "streamlit run app.py"

# Clear temporary files
rm -rf /tmp/streamlit-*

# Restart application
streamlit run app.py
```

2. **Configuration Reset**
```bash
# Backup current config
cp .env .env.backup

# Reset to defaults
cp .env.sample .env

# Edit with correct values
nano .env
```

3. **Database/Cache Reset**
```python
# Clear all caches
coordinator.research_agent.clear_cache()
coordinator.workflow_history.clear()

# Reset metrics
for agent in coordinator.agents.values():
    agent.metrics = {
        "requests": 0,
        "successes": 0,
        "failures": 0,
        "total_time": 0.0
    }
```

## Getting Help

### 1. Collect Diagnostic Information

Before seeking help, collect:

```bash
# System information
python --version
pip list > installed_packages.txt

# Configuration (sanitized)
env | grep -E "(LOG_|MAX_|TIMEOUT_|ENABLE_)" > config_info.txt

# Recent logs
tail -100 logs/app.log > recent_logs.txt

# Health check results
python -c "
from src.core.health import HealthChecker
from src.core.config import Config
health = HealthChecker(Config()).check_system_health()
print(health)
" > health_status.txt
```

### 2. Create Minimal Reproduction

```python
# Create minimal test case
from src.agents.coordinator_agent import CoordinatorAgent
from src.core.config import Config
from src.utils.logger import setup_logger

# Minimal configuration
config = Config(openai_api_key="test_key")
logger = setup_logger()
coordinator = CoordinatorAgent(config, logger)

# Simple test case
input_data = {"task": "Simple test"}
try:
    result = await coordinator.process(input_data)
    print("Success:", result)
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
```

### 3. Support Channels

- GitHub Issues: For bug reports and feature requests
- Documentation: Check API reference and deployment guide
- Community Forums: For general questions and discussions
- Email Support: For urgent production issues

### 4. Issue Template

When reporting issues, include:

```
**Environment:**
- OS: [e.g., Ubuntu 20.04, Windows 10, macOS 12]
- Python Version: [e.g., 3.9.7]
- Package Version: [e.g., 1.0.0]

**Configuration:**
- Model: [e.g., gpt-4]
- Deployment: [e.g., local, Docker, cloud]

**Issue Description:**
[Clear description of the problem]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. [Third step]

**Expected Behavior:**
[What you expected to happen]

**Actual Behavior:**
[What actually happened]

**Logs:**
```
[Relevant log entries]
```

**Additional Context:**
[Any other relevant information]
```