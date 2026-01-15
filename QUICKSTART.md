# Quick Start Guide - Bharat AI Hub

Get up and running with Bharat AI Hub in 10 minutes!

## Prerequisites

- Node.js 18+ installed
- AWS Account (free tier works)
- Git installed
- Docker (optional, for local development)

## Option 1: Local Development (Fastest)

### Step 1: Clone Repository
```bash
git clone https://github.com/ArnabSen08/bharat-ai-hub.git
cd bharat-ai-hub
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` and add your AWS credentials:
```env
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

### Step 4: Set Up Database (Optional for testing)
```bash
# Skip this if you just want to test APIs
# Use SQLite or mock data for quick testing
```

### Step 5: Start Server
```bash
npm run dev
```

Server starts at `http://localhost:3000`

### Step 6: Test API
```bash
# Health check
curl http://localhost:3000/health

# Test AI diagnosis (requires AWS Bedrock access)
curl -X POST http://localhost:3000/api/healthcare/diagnosis \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "fever, cough", "patientId": 1}'
```

## Option 2: Docker (Recommended for Full Setup)

### Step 1: Clone Repository
```bash
git clone https://github.com/ArnabSen08/bharat-ai-hub.git
cd bharat-ai-hub
```

### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env with your AWS credentials
```

### Step 3: Start with Docker Compose
```bash
docker-compose up -d
```

This starts:
- PostgreSQL database
- Redis cache
- Application server

### Step 4: Run Migrations
```bash
docker-compose exec app npm run migrate
```

### Step 5: Access Application
- API: `http://localhost:3000`
- Web UI: `http://localhost:3000` (open in browser)

## Option 3: AWS Deployment

### Step 1: Install AWS CDK
```bash
npm install -g aws-cdk
```

### Step 2: Configure AWS CLI
```bash
aws configure
```

### Step 3: Deploy Infrastructure
```bash
cd infrastructure
npm install
cdk bootstrap
cdk deploy --all
```

### Step 4: Deploy Application
```bash
cd ..
npm run deploy
```

## AWS Bedrock Setup (Required for AI Features)

### 1. Request Model Access
1. Go to AWS Console → Bedrock
2. Click "Model access" in left sidebar
3. Click "Request model access"
4. Select "Anthropic Claude 3 Sonnet"
5. Submit request (usually approved instantly)

### 2. Verify Access
```bash
aws bedrock list-foundation-models --region ap-south-1
```

## Testing the Modules

### Healthcare Module
```bash
# AI Diagnosis
curl -X POST http://localhost:3000/api/healthcare/diagnosis \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": "fever, headache, body pain",
    "medicalHistory": {"age": 30, "gender": "male"},
    "patientId": 1
  }'
```

### Rural Module
```bash
# Crop Advisory
curl -X POST http://localhost:3000/api/rural/crop-advisory \
  -H "Content-Type: application/json" \
  -d '{
    "farmerId": 1,
    "farmData": {
      "soilType": "loamy",
      "location": "Punjab",
      "season": "kharif"
    },
    "language": "en"
  }'
```

### Market Prices
```bash
curl "http://localhost:3000/api/rural/market-prices?location=Punjab&cropType=rice"
```

## Troubleshooting

### Issue: "Bedrock Access Denied"
**Solution**: Request model access in AWS Console (see Bedrock Setup above)

### Issue: "Database Connection Failed"
**Solution**: 
- Check if PostgreSQL is running: `docker-compose ps`
- Verify DATABASE_URL in .env
- Restart containers: `docker-compose restart`

### Issue: "Module not found"
**Solution**: 
```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: "Port 3000 already in use"
**Solution**: 
```bash
# Change PORT in .env
PORT=3001

# Or kill process on port 3000
# Windows: netstat -ano | findstr :3000
# Linux/Mac: lsof -ti:3000 | xargs kill
```

## Next Steps

1. **Explore API Documentation**: See `docs/API_REFERENCE.md`
2. **Read Architecture**: See `docs/ARCHITECTURE.md`
3. **Deploy to Production**: See `docs/DEPLOYMENT.md`
4. **Contribute**: See `CONTRIBUTING.md`

## Demo Credentials (Development Only)

```
Email: demo@bharataihub.com
Password: Demo@123
```

## Useful Commands

```bash
# Development
npm run dev              # Start dev server
npm run build            # Build for production
npm run test             # Run tests

# Database
npm run migrate          # Run migrations
npm run seed             # Seed sample data

# Docker
docker-compose up        # Start all services
docker-compose down      # Stop all services
docker-compose logs -f   # View logs

# AWS CDK
cdk diff                 # Preview changes
cdk deploy              # Deploy infrastructure
cdk destroy             # Remove infrastructure
```

## Support

- **Documentation**: https://github.com/ArnabSen08/bharat-ai-hub/docs
- **Issues**: https://github.com/ArnabSen08/bharat-ai-hub/issues
- **Email**: beanclarksum@gmail.com

## What's Included?

✅ 6 AI-powered modules (Healthcare, Retail, Rural, Learning, Content, Community)  
✅ AWS Bedrock integration for AI  
✅ Multi-language support (22+ Indian languages)  
✅ RESTful APIs with comprehensive documentation  
✅ Docker setup for easy deployment  
✅ AWS CDK infrastructure as code  
✅ PostgreSQL + Redis + S3 storage  
✅ Production-ready architecture  

## Estimated Costs

### Development (Free Tier)
- AWS Bedrock: ~$0 (within free tier limits)
- RDS t3.micro: Free tier eligible
- Lambda: Free tier eligible
- S3: ~$0.01/month

### Production (Small Scale)
- ~$50-100/month for 1000 users
- Scales automatically with usage

---

**Ready to build the future of AI for Bharat? Let's go! 🚀**
