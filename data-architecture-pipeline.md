# Data Architecture & Pipeline Specification

## 1. Data Model Design

### 1.1 Entity-Relationship Diagram (ERD)

```
SHG
├── id (PK)
├── name
├── location (latitude, longitude)
├── category
├── member_count
├── production_capacity
├── certifications
├── quality_metrics
├── contact_info
├── bank_details
├── created_at
└── updated_at

Product
├── id (PK)
├── shg_id (FK)
├── name
├── category
├── description
├── unit_price
├── cost_price
├── images[]
├── certifications
├── shelf_life
├── minimum_order_quantity
├── available_quantity
├── sustainability_score
└── created_at

Buyer
├── id (PK)
├── name
├── type (Retailer/Wholesaler/Government/Aggregator)
├── location
├── category_preferences[]
├── quality_requirements
├── order_volume_range
├── price_range
├── certifications_required
├── payment_terms
└── rating

SHGBuyerMatch
├── id (PK)
├── shg_id (FK)
├── buyer_id (FK)
├── product_id[] (FK)
├── match_score
├── status (Pending/Accepted/Connected/Completed)
├── initial_message
├── last_interaction_date
└── connection_metadata

Order
├── id (PK)
├── shg_id (FK)
├── buyer_id (FK)
├── products[] (Product_id, quantity, unit_price)
├── total_value
├── order_date
├── delivery_date
├── status
├── payment_status
├── delivery_address
└── feedback

MarketData
├── id (PK)
├── product_id (FK)
├── timestamp
├── price (current market price)
├── demand_signal
├── competitor_count
├── availability_index
├── trend_direction
└── source

PricingHistory
├── id (PK)
├── product_id (FK)
├── date
├── price
├── quantity_sold
├── order_count
└── region

DemandForecast
├── id (PK)
├── product_id (FK)
├── forecast_date
├── period
├── predicted_demand
├── confidence_lower_bound
├── confidence_upper_bound
├── model_used
└── generated_at
```

### 1.2 Database Schema (PostgreSQL)

```sql
-- SHG Table
CREATE TABLE shg (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location POINT NOT NULL,  -- (latitude, longitude)
    category VARCHAR(100) NOT NULL,
    member_count INTEGER,
    production_capacity INTEGER,  -- units per month
    certifications JSON,
    quality_metrics JSON,
    contact_info JSON,
    bank_details JSON ENCRYPTED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_location (location),
    INDEX idx_category (category)
);

-- Product Table
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    shg_id INTEGER NOT NULL REFERENCES shg(id),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    unit_price DECIMAL(10, 2),
    cost_price DECIMAL(10, 2),
    images JSON,
    certifications JSON,
    shelf_life INTEGER,  -- days
    minimum_order_quantity INTEGER,
    available_quantity INTEGER,
    sustainability_score DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_shg_id (shg_id),
    INDEX idx_category (category)
);

-- Buyer Table
CREATE TABLE buyer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,  -- Retailer, Wholesaler, Government, Aggregator
    location POINT,
    category_preferences JSON,
    quality_requirements JSON,
    order_volume_range JSON,  -- {min, max}
    price_range JSON,  -- {min, max}
    certifications_required JSON,
    payment_terms VARCHAR(100),
    rating DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type (type),
    INDEX idx_location (location)
);

-- SHG-Buyer Matching Table
CREATE TABLE shg_buyer_match (
    id SERIAL PRIMARY KEY,
    shg_id INTEGER NOT NULL REFERENCES shg(id),
    buyer_id INTEGER NOT NULL REFERENCES buyer(id),
    product_ids JSON,
    match_score DECIMAL(3, 2),
    status VARCHAR(50) DEFAULT 'Pending',  -- Pending, Accepted, Connected, Completed
    initial_message TEXT,
    last_interaction_date TIMESTAMP,
    connection_metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(shg_id, buyer_id),
    INDEX idx_status (status),
    INDEX idx_match_score (match_score DESC)
);

-- Order Table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    shg_id INTEGER NOT NULL REFERENCES shg(id),
    buyer_id INTEGER NOT NULL REFERENCES buyer(id),
    products JSON NOT NULL,  -- [{product_id, quantity, unit_price}, ...]
    total_value DECIMAL(15, 2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_date TIMESTAMP,
    status VARCHAR(50),  -- Pending, Confirmed, Shipped, Delivered, Cancelled
    payment_status VARCHAR(50),  -- Pending, Paid, Refunded
    delivery_address JSON,
    feedback JSON,
    INDEX idx_shg_id (shg_id),
    INDEX idx_buyer_id (buyer_id),
    INDEX idx_status (status)
);

-- Market Data Table
CREATE TABLE market_data (
    id BIGSERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES product(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    price DECIMAL(10, 2),
    demand_signal DECIMAL(5, 2),  -- 0-10 scale
    competitor_count INTEGER,
    availability_index DECIMAL(3, 2),  -- 0-1 scale
    trend_direction VARCHAR(20),  -- UP, DOWN, STABLE
    source VARCHAR(100),
    INDEX idx_product_id (product_id),
    INDEX idx_timestamp (timestamp)
);

-- Pricing History Table
CREATE TABLE pricing_history (
    id BIGSERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES product(id),
    date DATE NOT NULL,
    price DECIMAL(10, 2),
    quantity_sold INTEGER,
    order_count INTEGER,
    region VARCHAR(100),
    INDEX idx_product_id (product_id),
    INDEX idx_date (date)
);

-- Demand Forecast Table
CREATE TABLE demand_forecast (
    id BIGSERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES product(id),
    forecast_date DATE,
    period INTEGER,  -- Number of days in forecast
    predicted_demand INTEGER,
    confidence_lower_bound INTEGER,
    confidence_upper_bound INTEGER,
    model_used VARCHAR(100),  -- LSTM, XGBoost, Prophet
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_product_id (product_id),
    INDEX idx_forecast_date (forecast_date)
);
```

---

## 2. Data Pipeline Architecture

### 2.1 Real-time Data Ingestion

```
External APIs (E-commerce, Weather, Government)
           ↓
    Message Queue (Kafka/RabbitMQ)
           ↓
    Stream Processing (Apache Spark / Flink)
           ↓
    Data Transformation & Validation
           ↓
    Real-time Database (Redis/DynamoDB)
           ↓
    Cache Layer for API Serving
```

### 2.2 Batch Data Processing

```
Daily Batch Job (Scheduled 2 AM UTC)
    ↓
Extract: Pull data from:
    - E-commerce API dump files
    - Government procurement portal
    - Web scraped market data
    ↓
Transform: 
    - Normalize formats
    - Remove duplicates
    - Validate data quality
    - Feature engineering
    ↓
Load: 
    - PostgreSQL data warehouse
    - S3 data lake
    - ML training datasets
    ↓
Trigger: ML model retraining (if applicable)
```

### 2.3 ETL Pipeline Code (PySpark)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import logging

class DataPipeline:
    """Data ETL Pipeline for SML Platform"""
    
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("SML-ETL-Pipeline") \
            .config("spark.sql.shuffle.partitions", "200") \
            .getOrCreate()
        self.logger = logging.getLogger(__name__)
    
    def extract_ecommerce_data(self, source_api_configs):
        """Extract product and pricing data from e-commerce APIs"""
        dfs = []
        for api_config in source_api_configs:
            try:
                df = self.spark.read \
                    .format("com.amazonaws.athena.spark") \
                    .option("table", api_config['table']) \
                    .load()
                dfs.append(df)
            except Exception as e:
                self.logger.error(f"Failed to extract from {api_config['name']}: {e}")
        
        return reduce(lambda x, y: x.union(y), dfs) if dfs else None
    
    def extract_government_data(self):
        """Extract government procurement data"""
        return self.spark.read \
            .format("csv") \
            .option("header", "true") \
            .load("s3://data-lake/government-procurement/*.csv")
    
    def transform_market_data(self, df_raw_market):
        """Transform and enrich market data"""
        df_transformed = df_raw_market \
            .withColumn("normalized_price", 
                when(col("price") > 0, col("price")).otherwise(None)) \
            .withColumn("timestamp", to_timestamp(col("timestamp"))) \
            .withColumn("source_hash", md5(concat(col("product_id"), col("source")))) \
            .dropDuplicates(["product_id", "timestamp", "source"]) \
            .filter(col("normalized_price").isNotNull())
        
        # Feature Engineering
        window_spec = Window.partitionBy("product_id") \
            .orderBy("timestamp") \
            .rangeBetween(-7*86400, 0)  # 7-day window
        
        df_with_features = df_transformed \
            .withColumn("price_7d_avg", 
                avg(col("normalized_price")).over(window_spec)) \
            .withColumn("price_volatility",
                stddev(col("normalized_price")).over(window_spec)) \
            .withColumn("price_change_pct",
                ((col("normalized_price") - lag("normalized_price", 1) \
                .over(Window.partitionBy("product_id").orderBy("timestamp"))) / 
                lag("normalized_price", 1).over(Window.partitionBy("product_id") \
                .orderBy("timestamp"))) * 100)
        
        return df_with_features
    
    def load_to_warehouse(self, df, table_name):
        """Load transformed data to PostgreSQL data warehouse"""
        df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://warehouse:5432/sml_db") \
            .option("dbtable", table_name) \
            .option("user", "etl_user") \
            .option("password", self.get_secret("db_password")) \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()
    
    def run_pipeline(self):
        """Execute complete ETL pipeline"""
        self.logger.info("Starting ETL Pipeline")
        
        # Extract
        df_ecommerce = self.extract_ecommerce_data([...])
        df_government = self.extract_government_data()
        
        # Transform
        df_market_transformed = self.transform_market_data(df_ecommerce)
        
        # Load
        self.load_to_warehouse(df_market_transformed, "market_data")
        self.load_to_warehouse(df_government, "government_procurement")
        
        self.logger.info("ETL Pipeline completed successfully")
```

---

## 3. Feature Engineering

### 3.1 Product-Level Features

```python
def engineer_product_features(product_id, market_data_df, sales_history_df):
    """
    Engineer ML features for product recommendations
    """
    
    features = {}
    
    # 1. Price Features
    features['price_zscore'] = (
        (current_price - historical_mean_price) / historical_std_price
    )
    features['price_vs_market'] = current_price / market_average_price
    features['price_elasticity'] = calculate_elasticity(sales_history_df)
    
    # 2. Demand Features
    features['sales_velocity'] = sales_last_7days / sales_last_30days
    features['trend_direction'] = identify_trend(sales_history_df[-30:])
    features['seasonality_factor'] = get_seasonality(product_id, current_month)
    
    # 3. Quality Features
    features['avg_rating'] = average_customer_rating
    features['review_sentiment'] = sentiment_score  # -1 to 1
    features['return_rate'] = returns / total_orders
    
    # 4. Market Features
    features['competition_level'] = number_of_competitors
    features['market_share'] = sales_volume / total_market_volume
    features['availability_score'] = stock_level / optimal_stock
    
    # 5. Temporal Features
    features['days_since_launch'] = (today - launch_date).days
    features['days_since_last_sale'] = (today - last_sale_date).days
    
    return features
```

### 3.2 SHG-Buyer Pair Features

```python
def engineer_match_features(shg_profile, buyer_profile, historical_matches_df):
    """
    Engineer features for recommendation scoring
    """
    
    features = {}
    
    # 1. Product Alignment
    features['product_category_match'] = similarity_score(
        shg_categories=shg_profile['categories'],
        buyer_categories=buyer_profile['preferred_categories']
    )
    
    # 2. Geographic Features
    distance = haversine_distance(shg_profile['location'], buyer_profile['location'])
    features['distance_km'] = distance
    features['logistics_cost_ratio'] = estimate_shipping_cost(distance) / avg_product_price
    
    # 3. Collaborative Features
    similar_successful_matches = find_similar_successful_matches(
        shg_profile, buyer_profile, historical_matches_df
    )
    features['similar_match_success_rate'] = (
        len([m for m in similar_successful_matches if m['status'] == 'Completed']) /
        len(similar_successful_matches)
    )
    
    # 4. Volume Compatibility
    features['volume_ratio'] = (
        (shg_profile['capacity'] - buyer_profile['min_order_volume']) /
        (buyer_profile['max_order_volume'] - buyer_profile['min_order_volume'])
    )
    
    # 5. Quality Fit
    features['quality_match_score'] = match_quality_requirements(
        shg_certifications=shg_profile['certifications'],
        buyer_requirements=buyer_profile['quality_requirements']
    )
    
    # 6. Price Compatibility
    features['price_overlap'] = calculate_price_overlap(
        shg_price_range=shg_profile['price_range'],
        buyer_budget=buyer_profile['budget']
    )
    
    return features
```

---

## 4. Data Quality & Validation

### 4.1 Data Quality Checks

```python
def validate_data_quality(df, quality_rules):
    """
    Validate data quality against defined rules
    """
    
    validation_results = {
        'passed': True,
        'errors': [],
        'warnings': []
    }
    
    # Check 1: Completeness
    for column in quality_rules['required_columns']:
        null_count = df.filter(col(column).isNull()).count()
        if null_count > 0:
            validation_results['errors'].append(
                f"{column} has {null_count} null values"
            )
            validation_results['passed'] = False
    
    # Check 2: Uniqueness
    for column in quality_rules['unique_columns']:
        duplicate_count = df.groupBy(column).count() \
            .filter(col("count") > 1).count()
        if duplicate_count > 0:
            validation_results['warnings'].append(
                f"{column} has {duplicate_count} duplicate values"
            )
    
    # Check 3: Value Range
    for column, (min_val, max_val) in quality_rules['value_ranges'].items():
        out_of_range = df.filter(
            (col(column) < min_val) | (col(column) > max_val)
        ).count()
        if out_of_range > 0:
            validation_results['warnings'].append(
                f"{column} has {out_of_range} values out of range"
            )
    
    # Check 4: Data Type Validation
    for column, expected_type in quality_rules['data_types'].items():
        actual_type = df.schema[column].dataType
        if str(actual_type) != expected_type:
            validation_results['errors'].append(
                f"{column} has wrong data type: {actual_type} vs {expected_type}"
            )
            validation_results['passed'] = False
    
    return validation_results
```

---

## 5. Data Governance & Metadata

### 5.1 Data Catalog (DataHub / Hudi)

```yaml
datasets:
  - name: market_data
    owner: data-team
    description: Real-time market price and demand signals
    source: E-commerce APIs, Web Scrapers
    frequency: Hourly
    retention: 3 years
    pii_columns: []
    
  - name: shg_profiles
    owner: platform-team
    description: SHG registration and profile information
    source: User input, Government records
    frequency: On-demand
    retention: As per regulatory
    pii_columns: [phone, email, bank_account]
    encryption: AES-256

  - name: demand_forecast
    owner: ml-team
    description: Predicted demand for products
    source: ML Models (LSTM, XGBoost, Prophet)
    frequency: Daily (2 AM UTC)
    retention: 1 year
    pii_columns: []
    
  - name: buyer_preferences
    owner: platform-team
    description: Buyer requirements and purchase history
    source: User input, Order history
    frequency: Real-time
    retention: As per regulatory
    pii_columns: [location, payment_info]
    encryption: AES-256
```

