# Deployment Guide - Bharat AI Hub

## Prerequisites

### Required Tools
- AWS Account with appropriate permissions
- AWS CLI configured
- Node.js 18+ and npm
- Python 3.9+
- Docker (for local development)
- Git

### AWS Services Access
Ensure you have access to:
- Amazon Bedrock (request model access)
- Amazon SageMaker
- Amazon RDS
- Amazon S3
- Amazon API Gateway
- AWS Lambda
- Amazon Cognito
- Amazon CloudWatch

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/ArnabSen08/bharat-ai-hub.git
cd bharat-ai-hub
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Configuration
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
DATABASE_URL=postgresql://user:password@localhost:5432/bharat_ai_hub
```

### 4. Database Setup

#### Option A: Local PostgreSQL
```bash
# Install PostgreSQL
# Create database
createdb bharat_ai_hub

# Run migrations
npm run migrate

# Seed data (optional)
npm run seed
```

#### Option B: Amazon RDS
```bash
# Create RDS instance via AWS Console or CLI
aws rds create-db-instance \
  --db-instance-identifier bharat-ai-hub-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YourPassword123 \
  --allocated-storage 20

# Update DATABASE_URL in .env
# Run migrations
npm run migrate
```

### 5. Start Development Server
```bash
npm run dev
```

Server will start on `http://localhost:3000`

## AWS Deployment

### Method 1: AWS CDK (Recommended)

#### 1. Install AWS CDK
```bash
npm install -g aws-cdk
```

#### 2. Bootstrap CDK
```bash
cd infrastructure
npm install
cdk bootstrap aws://ACCOUNT-ID/REGION
```

#### 3. Deploy Infrastructure
```bash
# Deploy all stacks
cdk deploy --all

# Or deploy specific stacks
cdk deploy BharatAIHub-NetworkStack
cdk deploy BharatAIHub-DatabaseStack
cdk deploy BharatAIHub-ComputeStack
cdk deploy BharatAIHub-AIStack
```

#### 4. Deploy Application
```bash
# Build application
npm run build

# Deploy to Lambda/ECS
npm run deploy
```

### Method 2: Manual Deployment

#### 1. Create S3 Bucket
```bash
aws s3 mb s3://bharat-ai-hub-storage --region ap-south-1
```

#### 2. Create RDS Instance
```bash
aws rds create-db-instance \
  --db-instance-identifier bharat-ai-hub-prod \
  --db-instance-class db.t3.small \
  --engine postgres \
  --master-username admin \
  --master-user-password SecurePassword123 \
  --allocated-storage 50 \
  --backup-retention-period 7 \
  --multi-az
```

#### 3. Create Lambda Functions
```bash
# Package application
zip -r function.zip src/ node_modules/

# Create Lambda function
aws lambda create-function \
  --function-name bharat-ai-hub-api \
  --runtime nodejs18.x \
  --role arn:aws:iam::ACCOUNT-ID:role/lambda-execution-role \
  --handler src/app.handler \
  --zip-file fileb://function.zip \
  --timeout 30 \
  --memory-size 512
```

#### 4. Create API Gateway
```bash
# Create REST API
aws apigateway create-rest-api \
  --name "Bharat AI Hub API" \
  --description "Unified AI Platform API"

# Configure routes and integrations
# (See AWS Console for detailed configuration)
```

#### 5. Configure Cognito
```bash
# Create user pool
aws cognito-idp create-user-pool \
  --pool-name bharat-ai-hub-users \
  --auto-verified-attributes email \
  --mfa-configuration OPTIONAL

# Create user pool client
aws cognito-idp create-user-pool-client \
  --user-pool-id YOUR_POOL_ID \
  --client-name bharat-ai-hub-web
```

## Docker Deployment

### 1. Build Docker Image
```bash
docker build -t bharat-ai-hub:latest .
```

### 2. Run Container Locally
```bash
docker run -p 3000:3000 \
  -e AWS_REGION=ap-south-1 \
  -e DATABASE_URL=postgresql://... \
  bharat-ai-hub:latest
```

### 3. Push to ECR
```bash
# Create ECR repository
aws ecr create-repository --repository-name bharat-ai-hub

# Login to ECR
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com

# Tag and push
docker tag bharat-ai-hub:latest ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com/bharat-ai-hub:latest
docker push ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com/bharat-ai-hub:latest
```

### 4. Deploy to ECS
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name bharat-ai-hub-cluster

# Create task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster bharat-ai-hub-cluster \
  --service-name bharat-ai-hub-service \
  --task-definition bharat-ai-hub:1 \
  --desired-count 2 \
  --launch-type FARGATE
```

## Environment-Specific Configuration

### Development
```env
NODE_ENV=development
LOG_LEVEL=debug
ENABLE_XRAY_TRACING=false
```

### Staging
```env
NODE_ENV=staging
LOG_LEVEL=info
ENABLE_XRAY_TRACING=true
```

### Production
```env
NODE_ENV=production
LOG_LEVEL=warn
ENABLE_XRAY_TRACING=true
```

## Post-Deployment Steps

### 1. Run Database Migrations
```bash
npm run migrate
```

### 2. Verify Health Endpoint
```bash
curl https://your-api-domain.com/health
```

### 3. Test AI Services
```bash
# Test Bedrock
curl -X POST https://your-api-domain.com/api/healthcare/diagnosis \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "fever, cough", "patientId": 1}'
```

### 4. Configure CloudWatch Alarms
```bash
# CPU utilization alarm
aws cloudwatch put-metric-alarm \
  --alarm-name bharat-ai-hub-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

### 5. Set Up Backup
```bash
# Enable automated RDS backups
aws rds modify-db-instance \
  --db-instance-identifier bharat-ai-hub-prod \
  --backup-retention-period 7 \
  --preferred-backup-window "03:00-04:00"

# Enable S3 versioning
aws s3api put-bucket-versioning \
  --bucket bharat-ai-hub-storage \
  --versioning-configuration Status=Enabled
```

## Monitoring & Logging

### CloudWatch Logs
```bash
# View logs
aws logs tail /aws/lambda/bharat-ai-hub-api --follow

# Create log insights query
aws logs start-query \
  --log-group-name /aws/lambda/bharat-ai-hub-api \
  --start-time $(date -d '1 hour ago' +%s) \
  --end-time $(date +%s) \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/'
```

### X-Ray Tracing
```bash
# View service map
aws xray get-service-graph \
  --start-time $(date -d '1 hour ago' +%s) \
  --end-time $(date +%s)
```

## Scaling Configuration

### Auto Scaling for ECS
```bash
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/bharat-ai-hub-cluster/bharat-ai-hub-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/bharat-ai-hub-cluster/bharat-ai-hub-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name cpu-scaling-policy \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

### Lambda Concurrency
```bash
aws lambda put-function-concurrency \
  --function-name bharat-ai-hub-api \
  --reserved-concurrent-executions 100
```

## Troubleshooting

### Common Issues

#### 1. Bedrock Access Denied
```bash
# Request model access in AWS Console
# Bedrock > Model access > Request access
```

#### 2. Database Connection Failed
```bash
# Check security group rules
# Verify DATABASE_URL format
# Test connection: psql $DATABASE_URL
```

#### 3. Lambda Timeout
```bash
# Increase timeout
aws lambda update-function-configuration \
  --function-name bharat-ai-hub-api \
  --timeout 60
```

#### 4. Out of Memory
```bash
# Increase memory
aws lambda update-function-configuration \
  --function-name bharat-ai-hub-api \
  --memory-size 1024
```

## Security Checklist

- [ ] Enable encryption at rest for RDS
- [ ] Enable encryption at rest for S3
- [ ] Configure VPC security groups
- [ ] Enable AWS WAF
- [ ] Set up AWS Shield
- [ ] Configure IAM roles with least privilege
- [ ] Enable CloudTrail logging
- [ ] Set up AWS Config rules
- [ ] Enable GuardDuty
- [ ] Configure AWS Secrets Manager for sensitive data

## Cost Optimization

### 1. Use Reserved Instances
```bash
# Purchase RDS reserved instance
aws rds purchase-reserved-db-instances-offering \
  --reserved-db-instances-offering-id offering-id
```

### 2. Enable S3 Intelligent-Tiering
```bash
aws s3api put-bucket-intelligent-tiering-configuration \
  --bucket bharat-ai-hub-storage \
  --id intelligent-tiering-config \
  --intelligent-tiering-configuration file://tiering-config.json
```

### 3. Set Up Budget Alerts
```bash
aws budgets create-budget \
  --account-id ACCOUNT-ID \
  --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

## Rollback Procedure

### 1. Identify Last Good Version
```bash
git log --oneline
```

### 2. Rollback Code
```bash
git revert <commit-hash>
git push origin master
```

### 3. Rollback Infrastructure
```bash
cdk deploy --rollback
```

### 4. Rollback Database
```bash
# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier bharat-ai-hub-restored \
  --db-snapshot-identifier snapshot-id
```

## Support

For deployment issues:
- Email: contact@bharataihub.com
- GitHub Issues: https://github.com/ArnabSen08/bharat-ai-hub/issues
- Documentation: https://github.com/ArnabSen08/bharat-ai-hub/docs
