# Deployment Guide

## Overview

This guide covers deploying the Multi-Agent AI System in various environments, from local development to production cloud deployments.

## Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **Memory**: Minimum 2GB RAM, recommended 4GB+
- **Storage**: Minimum 1GB free space
- **Network**: Internet connection for API access

### Dependencies

- OpenAI API key
- Python package manager (pip)
- Git (for cloning repository)

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/multi-agent-ai-system.git
cd multi-agent-ai-system
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.sample .env

# Edit .env file with your configuration
# Required: Set your OpenAI API key
OPENAI_API_KEY=your_actual_api_key_here
```

### 5. Run Application

```bash
# Start the Streamlit application
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Production Deployment

### Docker Deployment

#### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/health || exit 1

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### 2. Build and Run Container

```bash
# Build Docker image
docker build -t multi-agent-ai-system .

# Run container
docker run -d \
    --name multi-agent-ai \
    -p 8501:8501 \
    -e OPENAI_API_KEY=your_api_key \
    -v $(pwd)/logs:/app/logs \
    multi-agent-ai-system
```

### Docker Compose Deployment

#### docker-compose.yml

```yaml
version: '3.8'

services:
  multi-agent-ai:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LOG_LEVEL=INFO
      - ENABLE_METRICS=true
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - multi-agent-ai
    restart: unless-stopped
```

#### Deploy with Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Cloud Deployment

#### AWS Deployment

##### Using AWS ECS

1. **Create ECR Repository**
```bash
aws ecr create-repository --repository-name multi-agent-ai-system
```

2. **Build and Push Image**
```bash
# Get login token
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com

# Build and tag image
docker build -t multi-agent-ai-system .
docker tag multi-agent-ai-system:latest 123456789012.dkr.ecr.us-west-2.amazonaws.com/multi-agent-ai-system:latest

# Push image
docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/multi-agent-ai-system:latest
```

3. **Create ECS Task Definition**
```json
{
  "family": "multi-agent-ai-system",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "multi-agent-ai",
      "image": "123456789012.dkr.ecr.us-west-2.amazonaws.com/multi-agent-ai-system:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENAI_API_KEY",
          "value": "your_api_key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/multi-agent-ai-system",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

##### Using AWS Lambda (Serverless)

For serverless deployment, create a Lambda-compatible version:

```python
# lambda_handler.py
import json
import asyncio
from src.agents.coordinator_agent import CoordinatorAgent
from src.core.config import Config
from src.utils.logger import setup_logger

def lambda_handler(event, context):
    """AWS Lambda handler for the multi-agent system."""
    
    try:
        # Initialize system
        config = Config()
        logger = setup_logger()
        coordinator = CoordinatorAgent(config, logger)
        
        # Process request
        input_data = json.loads(event['body'])
        result = asyncio.run(coordinator.process(input_data))
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }
```

#### Google Cloud Platform

##### Using Cloud Run

1. **Create Dockerfile** (same as above)

2. **Deploy to Cloud Run**
```bash
# Build and deploy
gcloud run deploy multi-agent-ai-system \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars OPENAI_API_KEY=your_api_key
```

#### Azure Deployment

##### Using Azure Container Instances

```bash
# Create resource group
az group create --name multi-agent-ai-rg --location eastus

# Deploy container
az container create \
    --resource-group multi-agent-ai-rg \
    --name multi-agent-ai-system \
    --image your-registry/multi-agent-ai-system:latest \
    --dns-name-label multi-agent-ai \
    --ports 8501 \
    --environment-variables OPENAI_API_KEY=your_api_key
```

## Configuration Management

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | Yes |
| `OPENAI_MODEL` | Model to use | gpt-4 | No |
| `MAX_RETRIES` | Maximum retry attempts | 3 | No |
| `TIMEOUT_SECONDS` | Request timeout | 30 | No |
| `LOG_LEVEL` | Logging level | INFO | No |
| `ENABLE_METRICS` | Enable metrics collection | true | No |

### Secrets Management

#### AWS Secrets Manager

```python
import boto3
import json

def get_secret(secret_name, region_name="us-west-2"):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    except Exception as e:
        raise e

# Usage
secrets = get_secret("multi-agent-ai-secrets")
openai_api_key = secrets["OPENAI_API_KEY"]
```

#### Azure Key Vault

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)

# Retrieve secret
openai_api_key = client.get_secret("openai-api-key").value
```

## Monitoring and Logging

### Application Monitoring

#### Health Checks

The application provides health check endpoints:

- `/health` - Basic health status
- `/metrics` - Performance metrics
- `/ready` - Readiness probe

#### Logging Configuration

```python
# Production logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'json': {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
```

### Infrastructure Monitoring

#### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Metrics
REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('request_duration_seconds', 'Request latency')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active connections')

# Start metrics server
start_http_server(8000)
```

## Security Considerations

### Network Security

- Use HTTPS in production
- Implement proper firewall rules
- Use VPC/private networks where possible
- Enable DDoS protection

### Application Security

- Validate all inputs
- Implement rate limiting
- Use secure headers
- Regular security updates

### API Key Security

- Never commit API keys to version control
- Use environment variables or secrets management
- Rotate keys regularly
- Monitor API usage

## Scaling and Performance

### Horizontal Scaling

#### Load Balancer Configuration (Nginx)

```nginx
upstream multi_agent_backend {
    server multi-agent-ai-1:8501;
    server multi-agent-ai-2:8501;
    server multi-agent-ai-3:8501;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://multi_agent_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /health {
        access_log off;
        proxy_pass http://multi_agent_backend;
    }
}
```

### Performance Optimization

- Enable response caching
- Use connection pooling
- Implement request queuing
- Monitor resource usage

### Auto-scaling

#### Kubernetes HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: multi-agent-ai-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: multi-agent-ai-system
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Troubleshooting

### Common Issues

#### API Connection Errors
- Verify API key is correct
- Check network connectivity
- Verify rate limits

#### Memory Issues
- Monitor memory usage
- Adjust container limits
- Check for memory leaks

#### Performance Issues
- Review logs for bottlenecks
- Monitor response times
- Check resource utilization

### Debugging

#### Enable Debug Logging

```bash
export LOG_LEVEL=DEBUG
export DEBUG_MODE=true
```

#### Container Debugging

```bash
# Access running container
docker exec -it multi-agent-ai /bin/bash

# View logs
docker logs multi-agent-ai

# Monitor resources
docker stats multi-agent-ai
```

## Backup and Recovery

### Data Backup

- Regular backup of logs
- Configuration backup
- Database backup (if applicable)

### Disaster Recovery

- Multi-region deployment
- Automated failover
- Regular recovery testing

## Maintenance

### Regular Tasks

- Update dependencies
- Rotate API keys
- Review logs
- Performance monitoring
- Security updates

### Monitoring Checklist

- [ ] Application health checks
- [ ] Resource utilization
- [ ] Error rates
- [ ] Response times
- [ ] API usage limits
- [ ] Security alerts