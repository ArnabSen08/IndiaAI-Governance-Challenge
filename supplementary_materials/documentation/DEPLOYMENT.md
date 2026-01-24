# Production Deployment Guide - Ready Tensor RAG

Complete guide for deploying RAG system to production.

---

## 📋 Pre-Deployment Checklist

- [ ] Code tested and reviewed
- [ ] Environment variables configured
- [ ] API keys secured (use secrets management)
- [ ] Vector store prepared (embedded documents)
- [ ] Monitoring and logging configured
- [ ] Backup and recovery plan ready
- [ ] Performance benchmarks established
- [ ] Security assessment completed

---

## 🚀 Deployment Options

### Option 1: Local Server Deployment (Simplest)

#### Step 1: Prepare Environment
```bash
# Clone repository
git clone https://github.com/ArnabSen08/ready-tensor.git
cd ready-tensor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

#### Step 2: Prepare Data
```bash
# Place documents in data/documents/
cp your_documents/* data/documents/

# Build vector store
python src/document_loader.py
# This creates data/vectorstore/
```

#### Step 3: Run Application
```bash
# Using Flask/FastAPI (install first)
pip install flask gunicorn

# Create app.py with RAG endpoints
python app.py

# Or run with gunicorn (production)
gunicorn app:app --workers 4 --bind 0.0.0.0:8000
```

---

### Option 2: Docker Deployment (Recommended)

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
```

#### Step 2: Build and Run
```bash
# Build image
docker build -t ready-tensor:latest .

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  -v $(pwd)/data:/app/data \
  ready-tensor:latest
```

#### Step 3: Docker Compose (Multi-container)
```yaml
version: '3.8'

services:
  rag-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

```bash
# Deploy
docker-compose up -d

# View logs
docker-compose logs -f rag-app

# Stop
docker-compose down
```

---

### Option 3: Cloud Deployment

#### AWS Lambda + API Gateway

**Setup:**
```bash
# Install serverless framework
npm install -g serverless

# Create serverless.yml
serverless deploy
```

**serverless.yml:**
```yaml
service: ready-tensor-rag

provider:
  name: aws
  runtime: python3.10
  region: us-east-1
  environment:
    OPENAI_API_KEY: ${ssm:/ready-tensor/openai-key}

functions:
  query:
    handler: src/lambda_handler.query_handler
    events:
      - http:
          path: query
          method: post
    timeout: 60
    memorySize: 3008
  
  health:
    handler: src/lambda_handler.health_handler
    events:
      - http:
          path: health
          method: get

package:
  patterns:
    - '!node_modules/**'
    - '!venv/**'
```

#### Google Cloud Run

```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/ready-tensor

# Deploy
gcloud run deploy ready-tensor \
  --image gcr.io/PROJECT_ID/ready-tensor \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk-...
```

#### Azure Container Instances

```bash
# Create resource group
az group create --name rag-rg --location eastus

# Deploy container
az container create \
  --resource-group rag-rg \
  --name ready-tensor \
  --image ready-tensor:latest \
  --cpu 2 --memory 3.5 \
  --ports 8000 \
  --environment-variables OPENAI_API_KEY=sk-...
```

---

## 🔐 Security Best Practices

### 1. API Key Management
```bash
# Use environment secrets, NOT hardcoded keys
# Option 1: Environment variables
export OPENAI_API_KEY=sk-...

# Option 2: AWS Secrets Manager
aws secretsmanager create-secret \
  --name /ready-tensor/openai-key \
  --secret-string sk-...

# Option 3: HashiCorp Vault
vault kv put secret/ready-tensor openai_key=sk-...
```

### 2. Network Security
```yaml
# Security Group Rules (AWS)
- Protocol: TCP
  Port: 8000
  Source: Load Balancer Only (not 0.0.0.0)

- Protocol: TCP
  Port: 443
  Source: 0.0.0.0/0 (HTTPS only)
```

### 3. Authentication
```python
# Add authentication to API
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/query")
async def query_endpoint(
    request: QueryRequest,
    credentials = Depends(security)
):
    # Verify API key
    if credentials.credentials != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return rag_assistant.query(request.question)
```

### 4. Data Protection
```python
# Encrypt sensitive data at rest
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt documents before storage
encrypted_data = cipher.encrypt(document.encode())

# Use HTTPS for all communications
# Implement rate limiting
# Add request validation
```

---

## 📊 Monitoring & Logging

### 1. Structured Logging
```python
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log with context
logger.info(json.dumps({
    "event": "query_processed",
    "query": query,
    "latency_ms": latency,
    "tokens_used": tokens,
    "status": "success"
}))
```

### 2. Performance Monitoring
```python
# Track key metrics
from prometheus_client import Counter, Histogram

query_counter = Counter('queries_total', 'Total queries')
latency_histogram = Histogram('query_latency_seconds', 'Query latency')

with latency_histogram.time():
    result = rag_assistant.query(question)
query_counter.inc()
```

### 3. Error Tracking
```python
# Use Sentry for error tracking
import sentry_sdk

sentry_sdk.init("YOUR_SENTRY_URL")

try:
    result = rag_assistant.query(question)
except Exception as e:
    sentry_sdk.capture_exception(e)
    raise
```

### 4. Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "vectorstore": check_vectorstore(),
        "llm_api": check_llm_connection()
    }
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test
        run: |
          pip install -r requirements.txt
          pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and Push Docker
        run: |
          docker build -t ready-tensor:latest .
          docker push gcr.io/${{ secrets.GCP_PROJECT }}/ready-tensor:latest
      
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy ready-tensor \
            --image gcr.io/${{ secrets.GCP_PROJECT }}/ready-tensor:latest \
            --region us-central1
```

---

## 📈 Scaling Strategies

### Horizontal Scaling
```yaml
# Use load balancer
- 4 instances of RAG service
- Redis cache layer
- Shared vector store (cloud storage)

Architecture:
Load Balancer
├── Instance 1 (Docker)
├── Instance 2 (Docker)
├── Instance 3 (Docker)
└── Instance 4 (Docker)
    ↓
Redis Cache (shared)
    ↓
Vector Store (cloud)
```

### Vertical Scaling
```python
# Optimize single instance
- Use GPU for faster inference
- Increase memory allocation
- Use async/concurrent processing
- Implement intelligent caching

configuration = {
    "workers": 8,  # CPU cores
    "memory_gb": 32,  # Increase memory
    "gpu_enabled": True,  # Enable GPU
    "cache_size_mb": 2048  # Larger cache
}
```

---

## 🔄 Backup & Recovery

### Backup Strategy
```bash
# Daily backup of vector store
0 2 * * * tar -czf /backups/vectorstore-$(date +%Y%m%d).tar.gz /data/vectorstore/

# Backup to S3
aws s3 sync /backups s3://my-bucket/vectorstore-backups/

# Database backups
pg_dump mydb | gzip > backup.sql.gz
aws s3 cp backup.sql.gz s3://my-bucket/db-backups/
```

### Disaster Recovery Plan
```
1. Alert & Detection (5 min)
   └─ Automated monitoring detects issue

2. Failover (5 min)
   └─ Switch to backup instance
   └─ Load balancer routes traffic

3. Restore (30 min)
   └─ Restore from backup
   └─ Verify data integrity

4. Verification (15 min)
   └─ Run tests
   └─ Verify queries work

5. Analysis (follow-up)
   └─ Investigate root cause
   └─ Implement improvements
```

---

## 📋 Production Checklist

### Before Going Live
- [ ] Load testing completed (1000+ concurrent users)
- [ ] Security audit completed
- [ ] Database backups tested
- [ ] Monitoring and alerting configured
- [ ] Runbook and playbooks created
- [ ] Team trained on deployment
- [ ] Documentation updated
- [ ] Rollback plan established

### Daily Operations
- [ ] Monitor error rates
- [ ] Check query latencies
- [ ] Verify API availability
- [ ] Review cost metrics
- [ ] Rotate logs
- [ ] Backup data

### Weekly
- [ ] Review performance trends
- [ ] Update security patches
- [ ] Test backup/recovery
- [ ] Team standup on issues

### Monthly
- [ ] Full system test
- [ ] Update documentation
- [ ] Capacity planning review
- [ ] Cost optimization review

---

## 🆘 Troubleshooting

### High Latency
```
1. Check LLM API response times
2. Monitor vector search latency
3. Review server resource utilization
4. Check network connectivity
5. Consider caching implementation
```

### Out of Memory
```
1. Reduce vector store size
2. Implement pagination
3. Increase server memory
4. Use cloud vector database
5. Enable memory profiling
```

### API Key Errors
```
1. Verify key in secrets manager
2. Check key hasn't been revoked
3. Verify API quota not exceeded
4. Test with direct API call
5. Rotate key if compromised
```

---

## 📚 Additional Resources

- [Docker Deployment](https://docs.docker.com/)
- [AWS Lambda Guide](https://aws.amazon.com/lambda/)
- [Google Cloud Run](https://cloud.google.com/run)
- [Kubernetes (if needed)](https://kubernetes.io/)

---

**Last Updated:** January 2026  
**Version:** 1.0.0
