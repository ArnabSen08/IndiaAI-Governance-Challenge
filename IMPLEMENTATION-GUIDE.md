# Smart Market Linkage Platform - Implementation Guide

## Getting Started

This guide provides step-by-step instructions to implement the Smart Market Linkage AI Platform for SHGs.

---

## Part 1: Environment Setup

### 1.1 Prerequisites
```bash
# Required software versions
- Python 3.10+
- Node.js 16+
- PostgreSQL 14+
- Docker 20.10+
- Docker Compose 2.0+
- Git 2.30+
```

### 1.2 Development Environment Setup

#### Backend Setup
```bash
# Clone repository
git clone https://github.com/ArnabSen08/IndiaAI-Governance-Challenge.git
cd IndiaAI-Governance-Challenge

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install ML/Data dependencies
pip install tensorflow torch xgboost fbprophet
pip install scikit-learn pandas numpy scipy
pip install sqlalchemy psycopg2-binary pymongo redis
pip install fastapi uvicorn pydantic
pip install kafka-python requests
```

#### Frontend Setup
```bash
# Install Node dependencies
npm install

# Install React/Next.js specific packages
npm install react react-dom next
npm install axios recharts lodash
```

### 1.3 Database Setup

#### PostgreSQL Setup
```sql
-- Create database
CREATE DATABASE sml_platform;

-- Create tables (from data-architecture-pipeline.md)
-- Tables: shg, product, buyer, shg_buyer_match, orders, market_data, etc.

-- Create indexes for performance
CREATE INDEX idx_shg_location ON shg USING GIST(location);
CREATE INDEX idx_product_category ON product(category);
CREATE INDEX idx_market_data_timestamp ON market_data(timestamp DESC);
```

#### Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: sml_platform
      POSTGRES_USER: sml_user
      POSTGRES_PASSWORD: secure_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  kafka:
    image: confluentinc/cp-kafka:7.0.0
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092

  zookeeper:
    image: confluentinc/cp-zookeeper:7.0.0
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

volumes:
  postgres_data:
  mongodb_data:
```

Run with:
```bash
docker-compose up -d
```

---

## Part 2: Core Module Implementation

### 2.1 Market Intelligence Module

#### File: `backend/modules/market_intelligence.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import numpy as np

router = APIRouter(prefix="/api/v1/market", tags=["market"])

@router.get("/opportunities/{shg_id}")
async def discover_opportunities(shg_id: int, db: Session = Depends(get_db)):
    """
    Discover market opportunities for SHG
    """
    
    shg = db.query(SHG).filter(SHG.id == shg_id).first()
    
    # Find similar SHGs and their successful products
    similar_shgs = find_similar_shgs(
        db, 
        location=shg.location,
        category=shg.category,
        capacity=shg.production_capacity
    )
    
    # Extract successful products
    successful_products = extract_successful_products(db, similar_shgs)
    
    # Filter for unsold products
    new_opportunities = [
        p for p in successful_products 
        if p.id not in [sp.id for sp in shg.products]
    ]
    
    # Score and rank
    scored_opportunities = []
    for opp in new_opportunities:
        score = calculate_opportunity_score(
            demand=get_market_demand(db, opp.id),
            feasibility=assess_production_feasibility(shg, opp),
            profit=estimate_profit_margin(db, opp)
        )
        scored_opportunities.append({
            'product': opp,
            'score': score,
            'demand_level': 'HIGH' if score > 0.7 else 'MEDIUM' if score > 0.4 else 'LOW'
        })
    
    # Sort and return top 10
    return sorted(scored_opportunities, key=lambda x: x['score'], reverse=True)[:10]

@router.get("/trends/{category}")
async def get_market_trends(category: str, days: int = 30, db: Session = Depends(get_db)):
    """
    Get market trends for product category
    """
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    trend_data = db.query(MarketData)\
        .join(Product)\
        .filter(
            Product.category == category,
            MarketData.timestamp >= cutoff_date
        )\
        .order_by(MarketData.timestamp)\
        .all()
    
    # Calculate trend metrics
    prices = [d.price for d in trend_data]
    demand_signals = [d.demand_signal for d in trend_data]
    
    return {
        'category': category,
        'period_days': days,
        'price_avg': np.mean(prices),
        'price_trend': 'UPWARD' if prices[-1] > prices[0] else 'DOWNWARD',
        'demand_avg': np.mean(demand_signals),
        'competition_count': len(set([d.competitor_count for d in trend_data])),
        'data_points': len(trend_data)
    }
```

### 2.2 Recommendation Engine

#### File: `backend/modules/recommendation_engine.py`

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecommendationEngine:
    """Hybrid recommendation system for SHG-Buyer matching"""
    
    def __init__(self, db: Session):
        self.db = db
        self.weights = {
            'content': 0.30,
            'collaborative': 0.30,
            'context': 0.25,
            'knowledge': 0.15
        }
    
    def recommend_buyers_for_shg(self, shg_id: int, top_n: int = 10):
        """Get buyer recommendations for SHG"""
        
        shg = self.db.query(SHG).filter(SHG.id == shg_id).first()
        all_buyers = self.db.query(Buyer).all()
        
        scores = []
        
        for buyer in all_buyers:
            # Content-based score
            content_score = self._calculate_content_score(shg, buyer)
            
            # Collaborative score
            collab_score = self._calculate_collaborative_score(shg, buyer)
            
            # Context-based score
            context_score = self._calculate_context_score(shg, buyer)
            
            # Knowledge graph score
            knowledge_score = self._calculate_knowledge_score(shg, buyer)
            
            # Weighted combination
            final_score = (
                self.weights['content'] * content_score +
                self.weights['collaborative'] * collab_score +
                self.weights['context'] * context_score +
                self.weights['knowledge'] * knowledge_score
            )
            
            scores.append({
                'buyer_id': buyer.id,
                'buyer_name': buyer.name,
                'final_score': final_score,
                'confidence': min(1.0, final_score * 1.2),  # Normalize confidence
                'component_scores': {
                    'content': content_score,
                    'collaborative': collab_score,
                    'context': context_score,
                    'knowledge': knowledge_score
                }
            })
        
        # Sort and return top N
        return sorted(scores, key=lambda x: x['final_score'], reverse=True)[:top_n]
    
    def _calculate_content_score(self, shg, buyer):
        """Calculate product-buyer alignment score"""
        # Implementation from ml-algorithms-models.md
        pass
    
    def _calculate_collaborative_score(self, shg, buyer):
        """Calculate collaborative filtering score"""
        # Implementation from ml-algorithms-models.md
        pass
    
    def _calculate_context_score(self, shg, buyer):
        """Calculate context-based score"""
        # Implementation from ml-algorithms-models.md
        pass
    
    def _calculate_knowledge_score(self, shg, buyer):
        """Calculate knowledge graph score"""
        # Implementation from ml-algorithms-models.md
        pass
```

### 2.3 Price Optimization Module

#### File: `backend/modules/price_optimization.py`

```python
from scipy.optimize import minimize
import numpy as np

class PriceOptimizer:
    """Dynamic pricing optimization"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def recommend_price(self, product_id: int):
        """Get price recommendation"""
        
        product = self.db.query(Product).filter(Product.id == product_id).first()
        
        # Base cost calculation
        base_cost = product.cost_price
        min_margin = 0.20
        base_price = base_cost * (1 + min_margin)
        
        # Get competitor prices
        competitor_prices = self._get_competitor_prices(product)
        market_avg = np.mean(competitor_prices)
        
        # Demand elasticity
        elasticity = self._calculate_elasticity(product_id)
        
        # Seasonal adjustment
        seasonal_factor = self._get_seasonal_factor(product)
        
        # Inventory adjustment
        inventory_adjustment = self._get_inventory_adjustment(product)
        
        # Optimal price calculation
        recommended_price = (
            base_price * 0.2 +
            (market_avg * elasticity) * 0.4 +
            (market_avg * seasonal_factor) * 0.25 +
            (market_avg * inventory_adjustment) * 0.15
        )
        
        return {
            'product_id': product_id,
            'minimum': max(base_price, market_avg * 0.8),
            'recommended': recommended_price,
            'maximum': market_avg * 1.2,
            'components': {
                'base_cost': base_cost,
                'market_average': market_avg,
                'elasticity_factor': elasticity,
                'seasonal_factor': seasonal_factor,
                'inventory_factor': inventory_adjustment
            }
        }
    
    def _get_competitor_prices(self, product):
        """Get competitor pricing"""
        # Query market_data table
        pass
    
    def _calculate_elasticity(self, product_id):
        """Calculate price elasticity"""
        # Use historical sales data
        pass
    
    def _get_seasonal_factor(self, product):
        """Get seasonal demand factor"""
        # Based on product category and current month
        pass
    
    def _get_inventory_adjustment(self, product):
        """Get inventory-based price adjustment"""
        # Higher prices for low inventory, lower for high inventory
        pass
```

### 2.4 Demand Forecasting

#### File: `backend/modules/demand_forecasting.py`

```python
import tensorflow as tf
import xgboost as xgb
from fbprophet import Prophet
import numpy as np

class DemandForecaster:
    """Ensemble demand forecasting"""
    
    def __init__(self, db: Session):
        self.db = db
        self.lstm_model = None
        self.xgboost_model = None
        self.prophet_model = None
    
    def forecast_demand(self, product_id: int, periods: int = 12):
        """Get demand forecast"""
        
        # Get historical sales
        historical_sales = self._get_sales_history(product_id)
        
        # Get external features
        external_features = self._get_external_features(product_id)
        
        # Get LSTM forecast
        lstm_forecast = self._lstm_forecast(
            historical_sales, 
            periods
        )
        
        # Get XGBoost forecast
        xgboost_forecast = self._xgboost_forecast(
            historical_sales,
            external_features,
            periods
        )
        
        # Get Prophet forecast
        prophet_forecast = self._prophet_forecast(
            historical_sales,
            periods
        )
        
        # Ensemble
        ensemble_forecast = (
            0.35 * lstm_forecast +
            0.35 * xgboost_forecast +
            0.30 * prophet_forecast
        )
        
        # Calculate confidence intervals
        std_dev = np.std([lstm_forecast, xgboost_forecast, prophet_forecast], axis=0)
        
        return {
            'product_id': product_id,
            'forecast': ensemble_forecast.tolist(),
            'lower_bound': (ensemble_forecast - 1.96 * std_dev).tolist(),
            'upper_bound': (ensemble_forecast + 1.96 * std_dev).tolist(),
            'periods': periods,
            'confidence': 0.95
        }
    
    def _get_sales_history(self, product_id: int, days: int = 730):
        """Get historical sales data"""
        # Query orders table
        pass
    
    def _get_external_features(self, product_id: int):
        """Get external features for forecasting"""
        # Weather, holidays, competitor activity, etc.
        pass
    
    def _lstm_forecast(self, sales_data, periods):
        """LSTM model forecast"""
        # Implementation from ml-algorithms-models.md
        pass
    
    def _xgboost_forecast(self, sales_data, features, periods):
        """XGBoost model forecast"""
        # Implementation from ml-algorithms-models.md
        pass
    
    def _prophet_forecast(self, sales_data, periods):
        """Prophet model forecast"""
        # Implementation from ml-algorithms-models.md
        pass
```

---

## Part 3: Database Operations

### 3.1 Create Database Models

#### File: `backend/models.py`

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, POINT
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SHG(Base):
    __tablename__ = "shg"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    location = Column(POINT, nullable=False)
    category = Column(String(100), nullable=False)
    member_count = Column(Integer)
    production_capacity = Column(Integer)
    certifications = Column(JSON)
    quality_metrics = Column(JSON)
    contact_info = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True)
    shg_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(String)
    unit_price = Column(Float)
    cost_price = Column(Float)
    available_quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class Buyer(Base):
    __tablename__ = "buyer"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50))
    location = Column(POINT)
    category_preferences = Column(JSON)
    rating = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# More models in complete implementation...
```

---

## Part 4: API Development

### 4.1 Main Application

#### File: `backend/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.market_intelligence import router as market_router
from modules.recommendation_engine import router as recommend_router
from modules.price_optimization import router as price_router

# Initialize FastAPI app
app = FastAPI(
    title="Smart Market Linkage Platform",
    description="AI Platform for SHG Market Access",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = "postgresql://user:password@localhost/sml_platform"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Include routers
app.include_router(market_router)
app.include_router(recommend_router)
app.include_router(price_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run with:
```bash
python backend/main.py
```

---

## Part 5: Testing & Validation

### 5.1 Unit Tests

#### File: `tests/test_recommendation.py`

```python
import pytest
from backend.modules.recommendation_engine import RecommendationEngine

def test_content_score_calculation():
    """Test content-based similarity calculation"""
    # Mock SHG and Buyer
    # Verify score is between 0 and 1
    pass

def test_hybrid_recommendation():
    """Test hybrid recommendation output"""
    # Test with sample data
    # Verify top N recommendations returned
    # Verify scores are weighted correctly
    pass
```

### 5.2 Integration Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=backend/
```

---

## Part 6: Deployment

### 6.1 Docker Deployment

#### File: `Dockerfile`

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "backend/main.py"]
```

### 6.2 Kubernetes Deployment

#### File: `k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sml-platform
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sml-platform
  template:
    metadata:
      labels:
        app: sml-platform
    spec:
      containers:
      - name: sml-platform
        image: sml-platform:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

Deploy with:
```bash
kubectl apply -f k8s/deployment.yaml
```

---

## Part 7: Monitoring & Logging

### 7.1 Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Request counter
request_count = Counter(
    'sml_requests_total',
    'Total requests',
    ['method', 'endpoint']
)

# Response time histogram
response_time = Histogram(
    'sml_response_seconds',
    'Response time in seconds',
    ['endpoint']
)

# Active connections gauge
active_connections = Gauge(
    'sml_active_connections',
    'Active connections'
)
```

### 7.2 ELK Stack Integration

```python
from pythonjsonlogger import jsonlogger
import logging

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
```

---

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL status
psql -U sml_user -d sml_platform -h localhost

# Test Redis connection
redis-cli ping

# Check Kafka topics
kafka-topics --list --bootstrap-server localhost:9092
```

### API Issues
```bash
# Check API health
curl http://localhost:8000/health

# View API documentation
curl http://localhost:8000/docs
```

---

## Quick Start Commands

```bash
# 1. Setup environment
docker-compose up -d

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python backend/scripts/init_db.py

# 4. Start backend
python backend/main.py

# 5. Start frontend
npm run dev

# 6. Access application
# Backend API: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

---

**Ready to deploy!**

For more details, refer to:
- Architecture: `smart-market-linkage-design.md`
- Data Setup: `data-architecture-pipeline.md`
- E-commerce: `ecommerce-integration-guide.md`
- ML Models: `ml-algorithms-models.md`

