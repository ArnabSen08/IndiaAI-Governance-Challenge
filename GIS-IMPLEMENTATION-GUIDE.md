# Implementation Guide: GIS Land Allocation System
## Step-by-Step Setup and Deployment

---

## 1. Environment Setup

### 1.1 Python Environment Configuration

```bash
# Create virtual environment
python -m venv gis_land_allocation_env

# Activate
# On Windows:
gis_land_allocation_env\Scripts\activate
# On Linux/Mac:
source gis_land_allocation_env/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### 1.2 Install Dependencies

```bash
# Geospatial libraries
pip install rasterio==1.3.8
pip install geopandas==0.13.2
pip install shapely==2.0.1
pip install fiona==1.9.4
pip install gdal==3.7.1

# ML libraries
pip install scikit-learn==1.3.2
pip install xgboost==2.0.1
pip install tensorflow==2.13.0
pip install torch==2.0.1
pip install pytorch-lightning==2.0.9

# Data processing
pip install pandas==2.0.3
pip install numpy==1.24.3
pip install scipy==1.11.2
pip install xarray==2023.9.2
pip install netCDF4==1.6.4

# Optimization
pip install cvxpy==1.3.2
pip install pulp==2.7.0
pip install pymoo==0.6.0
pip install optuna==3.13.0

# Web framework
pip install fastapi==0.103.1
pip install uvicorn==0.23.2
pip install pydantic==2.3.0
pip install python-multipart==0.0.6

# Remote sensing
pip install sentinelhub==3.18.0
pip install google-cloud-storage==2.10.0
pip install boto3==1.28.35

# Visualization
pip install matplotlib==3.8.0
pip install folium==0.14.0
pip install plotly==5.17.0

# Utilities
pip install python-dotenv==1.0.0
pip install tqdm==4.66.1
pip install requests==2.31.0
pip install shapely==2.0.1
pip install fiona==1.9.4

# Database
pip install psycopg2-binary==2.9.7
pip install sqlalchemy==2.0.21
pip install alembic==1.12.0

# Testing & monitoring
pip install pytest==7.4.2
pip install pytest-cov==4.1.0
pip install prometheus-client==0.17.1
```

### 1.3 Requirements File

```
# requirements.txt

# Geospatial
rasterio==1.3.8
geopandas==0.13.2
shapely==2.0.1
fiona==1.9.4
gdal==3.7.1
pyproj==3.6.0

# ML/DL
scikit-learn==1.3.2
xgboost==2.0.1
tensorflow==2.13.0
torch==2.0.1
torchvision==0.15.1
pytorch-lightning==2.0.9

# Data
pandas==2.0.3
numpy==1.24.3
scipy==1.11.2
xarray==2023.9.2
netCDF4==1.6.4

# Optimization
cvxpy==1.3.2
pulp==2.7.0
pymoo==0.6.0
optuna==3.13.0

# Web
fastapi==0.103.1
uvicorn==0.23.2
pydantic==2.3.0
python-multipart==0.0.6

# Remote Sensing
sentinelhub==3.18.0
google-cloud-storage==2.10.0
boto3==1.28.35

# Visualization
matplotlib==3.8.0
folium==0.14.0
plotly==5.17.0
shap==0.42.1

# Database
psycopg2-binary==2.9.7
sqlalchemy==2.0.21
alembic==1.12.0

# Utilities
python-dotenv==1.0.0
tqdm==4.66.1
requests==2.31.0

# Testing
pytest==7.4.2
pytest-cov==4.1.0
```

---

## 2. Database Setup

### 2.1 PostgreSQL with PostGIS

```sql
-- Create database
CREATE DATABASE gis_land_allocation;

-- Connect to database
\c gis_land_allocation

-- Create PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS hstore;

-- Create schemas
CREATE SCHEMA raw_data;
CREATE SCHEMA processed;
CREATE SCHEMA results;

-- Table 1: Candidate Sites
CREATE TABLE processed.candidate_sites (
    site_id SERIAL PRIMARY KEY,
    site_name VARCHAR(255),
    state VARCHAR(100),
    district VARCHAR(100),
    location GEOMETRY(POINT, 4326),
    area_sqkm FLOAT,
    capacity_mw FLOAT,
    project_type VARCHAR(50),  -- 'solar' or 'wind'
    suitability_score FLOAT,
    installation_cost_cr FLOAT,
    distance_to_substation_km FLOAT,
    distance_to_transmission_km FLOAT,
    distance_to_road_km FLOAT,
    distance_to_water_km FLOAT,
    distance_to_urban_km FLOAT,
    has_conflict BOOLEAN,
    conflict_type VARCHAR(255),
    environmental_benefit_score FLOAT,
    administrative_readiness_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sites_location ON processed.candidate_sites USING GIST(location);
CREATE INDEX idx_sites_state_district ON processed.candidate_sites(state, district);

-- Table 2: Suitability Map (Raster)
CREATE TABLE processed.suitability_maps (
    map_id SERIAL PRIMARY KEY,
    state VARCHAR(100),
    project_type VARCHAR(50),
    raster_data BYTEA,
    crs VARCHAR(50),
    resolution_m FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table 3: Conflict Zones
CREATE TABLE processed.conflict_zones (
    zone_id SERIAL PRIMARY KEY,
    conflict_type VARCHAR(100),
    zone_name VARCHAR(255),
    geometry GEOMETRY(POLYGON, 4326),
    state VARCHAR(100),
    severity_level INT,  -- 1-5
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conflict_zones_geom ON processed.conflict_zones USING GIST(geometry);

-- Table 4: Allocation Results
CREATE TABLE results.allocations (
    allocation_id SERIAL PRIMARY KEY,
    allocation_name VARCHAR(255),
    state VARCHAR(100),
    project_type VARCHAR(50),
    scenario_name VARCHAR(255),
    target_capacity_mw FLOAT,
    achieved_capacity_mw FLOAT,
    total_cost_cr FLOAT,
    num_sites INT,
    allocation_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table 5: Allocated Sites (Many-to-one with Allocations)
CREATE TABLE results.allocated_sites (
    allocation_site_id SERIAL PRIMARY KEY,
    allocation_id INT REFERENCES results.allocations(allocation_id),
    site_id INT REFERENCES processed.candidate_sites(site_id),
    rank INT,
    suitability_score FLOAT,
    allocation_probability FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table 6: Performance Metrics
CREATE TABLE results.allocation_metrics (
    metric_id SERIAL PRIMARY KEY,
    allocation_id INT REFERENCES results.allocations(allocation_id),
    capacity_utilization_rate FLOAT,
    cost_efficiency_mw_per_cr FLOAT,
    geographic_distribution_score FLOAT,
    environmental_impact_score FLOAT,
    implementation_feasibility_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 2.2 Database Connection

```python
import os
from sqlalchemy import create_engine, Pool
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    """Database configuration"""
    
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'gis_land_allocation')
    
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    @staticmethod
    def get_engine():
        """Create SQLAlchemy engine"""
        
        return create_engine(
            DatabaseConfig.DATABASE_URL,
            poolclass=Pool,
            pool_size=10,
            max_overflow=20,
            echo=False
        )

# Create engine
engine = DatabaseConfig.get_engine()

# Test connection
def test_connection():
    """Test database connection"""
    
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("Database connection successful!")
        return True
```

---

## 3. Core Processing Pipeline

### 3.1 Data Pipeline Orchestration

```python
import logging
from datetime import datetime
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessingPipeline:
    """
    Orchestrate entire GIS land allocation processing
    """
    
    def __init__(self, state, project_type='solar'):
        self.state = state
        self.project_type = project_type
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(f"outputs/{state}/{self.timestamp}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.data_processor = Sentinel2Processor(config)
        self.dem_analyzer = DEMAnalyzer(dem_data)
        self.suitability_engine = SuitabilityScoringEngine()
        self.conflict_detector = ConflictDetector(aoi_bounds)
        self.ml_model = EnsembleLandSuitabilityModel(project_type)
        self.optimizer = LandAllocationOptimizer(state_config)
    
    def run_full_pipeline(self, aoi_bounds, date_range):
        """Execute complete processing pipeline"""
        
        try:
            logger.info(f"Starting pipeline for {self.state}...")
            
            # Step 1: Data collection
            logger.info("Step 1: Fetching satellite data...")
            satellite_data = self.fetch_satellite_data(aoi_bounds, date_range)
            
            # Step 2: Preprocessing
            logger.info("Step 2: Preprocessing satellite imagery...")
            processed_imagery = self.preprocess_imagery(satellite_data)
            
            # Step 3: Feature extraction
            logger.info("Step 3: Extracting features...")
            features = self.extract_features(processed_imagery)
            
            # Step 4: ML prediction
            logger.info("Step 4: Running suitability model...")
            suitability_map = self.predict_suitability(features)
            
            # Step 5: Conflict detection
            logger.info("Step 5: Detecting conflicts...")
            conflict_mask = self.detect_conflicts(aoi_bounds)
            
            # Step 6: Site identification
            logger.info("Step 6: Identifying candidate sites...")
            candidate_sites = self.identify_sites(suitability_map, conflict_mask)
            
            # Step 7: Optimization
            logger.info("Step 7: Optimizing allocation...")
            allocated_sites = self.optimize_allocation(candidate_sites)
            
            # Step 8: Save results
            logger.info("Step 8: Saving results...")
            self.save_results(suitability_map, conflict_mask, allocated_sites)
            
            logger.info("Pipeline completed successfully!")
            
            return {
                'status': 'success',
                'suitability_map': str(self.output_dir / 'suitability_map.tif'),
                'conflict_mask': str(self.output_dir / 'conflict_mask.tif'),
                'allocated_sites': allocated_sites,
                'num_sites': len(allocated_sites),
                'total_capacity_mw': sum([s['capacity_mw'] for s in allocated_sites])
            }
        
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise
    
    def fetch_satellite_data(self, aoi_bounds, date_range):
        """Fetch satellite imagery"""
        
        sentinel2_data = self.data_processor.fetch_sentinel2_image(
            aoi_bounds,
            date_range,
            self.output_dir / 'sentinel2_raw.tif'
        )
        
        return {'sentinel2': sentinel2_data}
    
    def preprocess_imagery(self, satellite_data):
        """Preprocess imagery"""
        
        sentinel2 = satellite_data['sentinel2']
        
        # Cloud masking
        valid_pixels = CloudMasking.sentinel2_cloud_mask(sentinel2)
        sentinel2[~valid_pixels] = 0
        
        return {'sentinel2': sentinel2}
    
    def extract_features(self, processed_imagery):
        """Extract spectral and topographic features"""
        
        sentinel2 = processed_imagery['sentinel2']
        
        # Spectral indices
        features = {
            'ndvi': self.data_processor.calculate_ndvi(sentinel2),
            'ndbi': self.data_processor.calculate_ndbi(sentinel2),
            'ndwi': self.data_processor.calculate_ndwi(sentinel2),
            'bsi': self.data_processor.calculate_bsi(sentinel2)
        }
        
        # Topographic features
        dem = self.dem_analyzer.dem
        features.update({
            'slope': self.dem_analyzer.calculate_slope(),
            'aspect': self.dem_analyzer.calculate_aspect(),
            'elevation': dem
        })
        
        return features
    
    def predict_suitability(self, features):
        """Predict land suitability"""
        
        # Prepare feature matrix
        feature_matrix = np.dstack([features[key] for key in features.keys()])
        
        # Reshape for prediction
        h, w = feature_matrix.shape[:2]
        X = feature_matrix.reshape(-1, feature_matrix.shape[2])
        
        # Predict
        suitability_scores = self.ml_model.predict(X)
        suitability_map = suitability_scores.reshape(h, w)
        
        # Save
        self.save_raster(
            self.output_dir / 'suitability_map.tif',
            suitability_map
        )
        
        return suitability_map
    
    def detect_conflicts(self, aoi_bounds):
        """Detect conflict zones"""
        
        conflict_mask, conflict_details = self.conflict_detector.detect_all_conflicts(
            aoi_bounds
        )
        
        # Save
        self.save_raster(
            self.output_dir / 'conflict_mask.tif',
            conflict_mask.astype(np.uint8)
        )
        
        # Save details
        with open(self.output_dir / 'conflict_details.json', 'w') as f:
            # Convert to JSON-serializable format
            json_details = {
                k: v.tolist() if isinstance(v, np.ndarray) else str(v)
                for k, v in conflict_details.items()
            }
            json.dump(json_details, f, indent=2)
        
        return conflict_mask
    
    def identify_sites(self, suitability_map, conflict_mask):
        """Identify candidate sites"""
        
        # Threshold: suitability > 50 and no conflicts
        valid_pixels = (suitability_map > 50) & ~conflict_mask
        
        # Extract patches
        fragmentation = FragmentationAnalyzer()
        patches = fragmentation.identify_land_parcels(suitability_map, threshold=50)
        merged_patches = fragmentation.merge_nearby_patches(patches)
        
        # Convert to candidate sites
        candidate_sites = []
        for i, patch in enumerate(merged_patches):
            candidate_sites.append({
                'site_id': i,
                'patch_id': patch.get('id'),
                'area_sqkm': patch['size_hectares'] / 100,
                'capacity_mw': patch['size_hectares'] / 2.5,  # ~2.5 hectares per MW
                'suitability_score': patch['mean_suitability'],
                'district': 'TBD',  # Will be assigned during geocoding
                'has_conflict': False
            })
        
        return candidate_sites
    
    def optimize_allocation(self, candidate_sites):
        """Optimize land allocation"""
        
        allocated_sites, obj_value = self.optimizer.allocate_lands_linear_programming(
            candidate_sites
        )
        
        return allocated_sites
    
    def save_results(self, suitability_map, conflict_mask, allocated_sites):
        """Save all results"""
        
        # Save GeoTIFFs
        self.save_raster(
            self.output_dir / 'final_suitability.tif',
            suitability_map
        )
        
        # Save sites as GeoJSON
        import geopandas as gpd
        from shapely.geometry import Point
        
        sites_gdf = gpd.GeoDataFrame(
            allocated_sites,
            geometry=[Point(s.get('longitude', 0), s.get('latitude', 0)) 
                     for s in allocated_sites]
        )
        sites_gdf.to_file(self.output_dir / 'allocated_sites.geojson', driver='GeoJSON')
        
        # Save summary report
        summary = {
            'state': self.state,
            'project_type': self.project_type,
            'timestamp': self.timestamp,
            'total_sites': len(allocated_sites),
            'total_capacity_mw': sum([s['capacity_mw'] for s in allocated_sites]),
            'total_cost_cr': sum([s.get('installation_cost_cr', 0) for s in allocated_sites]),
            'mean_suitability': float(np.mean([s['suitability_score'] for s in allocated_sites]))
        }
        
        with open(self.output_dir / 'summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
    
    @staticmethod
    def save_raster(filepath, array, crs='EPSG:4326', transform=None):
        """Save array as GeoTIFF"""
        
        import rasterio
        from rasterio.transform import Affine
        
        if transform is None:
            # Simple default transform
            transform = Affine.identity()
        
        with rasterio.open(
            filepath,
            'w',
            driver='GTiff',
            height=array.shape[0],
            width=array.shape[1],
            count=1,
            dtype=array.dtype,
            crs=crs,
            transform=transform
        ) as dst:
            dst.write(array, 1)
```

### 3.2 API Implementation

```python
from fastapi import FastAPI, File, UploadFile, Query, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import asyncio

app = FastAPI(
    title="GIS Land Allocation System",
    description="Automated renewable energy land suitability and allocation",
    version="1.0.0"
)

@app.post("/api/v1/pipeline/run")
async def run_pipeline(
    state: str,
    project_type: str = Query(..., enum=['solar', 'wind']),
    target_capacity_mw: int = Query(100),
    budget_cr: float = Query(500.0),
    background_tasks: BackgroundTasks = None
):
    """Run complete GIS analysis pipeline"""
    
    try:
        # Get AOI bounds for state
        aoi_bounds = get_state_aoi_bounds(state)
        date_range = ('2023-01-01', '2023-12-31')
        
        # Create pipeline instance
        pipeline = DataProcessingPipeline(state, project_type)
        
        # Run pipeline (async)
        result = pipeline.run_full_pipeline(aoi_bounds, date_range)
        
        return {
            'status': 'success',
            'message': 'Pipeline completed',
            'data': result
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'error': str(e)}
        )

@app.get("/api/v1/results/{state}/{project_type}")
async def get_results(
    state: str,
    project_type: str = Query(..., enum=['solar', 'wind'])
):
    """Get allocation results for state"""
    
    # Query database
    session = SessionLocal()
    
    allocation = session.query(Allocation).filter(
        Allocation.state == state,
        Allocation.project_type == project_type
    ).order_by(Allocation.created_at.desc()).first()
    
    if not allocation:
        return JSONResponse(
            status_code=404,
            content={'error': 'No results found'}
        )
    
    return {
        'allocation': allocation.to_dict(),
        'metrics': get_allocation_metrics(allocation.allocation_id)
    }

@app.get("/api/v1/suitability-map/{state}")
async def download_suitability_map(state: str):
    """Download suitability map GeoTIFF"""
    
    filepath = f"outputs/{state}/latest/suitability_map.tif"
    
    return FileResponse(
        filepath,
        media_type='image/tiff',
        filename=f'{state}_suitability_map.tif'
    )

@app.get("/api/v1/sites/recommended")
async def get_recommended_sites(
    state: str,
    top_n: int = Query(10, ge=1, le=100)
):
    """Get top recommended sites"""
    
    session = SessionLocal()
    
    sites = session.query(CandidateSite).filter(
        CandidateSite.state == state
    ).order_by(CandidateSite.suitability_score.desc()).limit(top_n).all()
    
    return [site.to_dict() for site in sites]
```

---

## 4. Testing & Validation

### 4.1 Unit Tests

```python
import pytest
import numpy as np
from pathlib import Path

class TestDEMAnalyzer:
    """Test DEM analysis functions"""
    
    @pytest.fixture
    def sample_dem(self):
        """Create sample DEM"""
        return np.random.rand(100, 100) * 1000
    
    def test_slope_calculation(self, sample_dem):
        """Test slope calculation"""
        
        analyzer = DEMAnalyzer(sample_dem)
        slope = analyzer.calculate_slope()
        
        assert slope.shape == sample_dem.shape
        assert np.all(slope >= 0)
        assert np.all(slope <= 90)
    
    def test_aspect_calculation(self, sample_dem):
        """Test aspect calculation"""
        
        analyzer = DEMAnalyzer(sample_dem)
        aspect = analyzer.calculate_aspect()
        
        assert aspect.shape == sample_dem.shape
        assert np.all(aspect >= 0)
        assert np.all(aspect <= 360)

class TestSuitabilityScoringEngine:
    """Test suitability scoring"""
    
    def test_solar_suitability_range(self):
        """Test solar suitability scores are in valid range"""
        
        engine = SuitabilityScoringEngine()
        
        slope = np.random.rand(50, 50) * 30
        land_cover = np.zeros((50, 50))
        distance_settlement = np.random.rand(50, 50) * 5000
        distance_road = np.random.rand(50, 50) * 10000
        solar_irradiance = np.random.rand(50, 50) * 1000 + 1500
        elevation = np.random.rand(50, 50) * 2000
        conflict_mask = np.zeros((50, 50), dtype=bool)
        
        suitability = engine.calculate_solar_suitability(
            slope, land_cover, distance_settlement, distance_road,
            solar_irradiance, elevation, conflict_mask
        )
        
        assert suitability.shape == (50, 50)
        assert np.all(suitability >= 0)
        assert np.all(suitability <= 100)

class TestConflictDetector:
    """Test conflict detection"""
    
    def test_conflict_mask_binary(self):
        """Test conflict mask is binary"""
        
        detector = ConflictDetector(aoi_bounds=(0, 0, 1, 1))
        
        conflict_mask, _ = detector.detect_all_conflicts(pixel_coords)
        
        assert conflict_mask.dtype == bool
        assert conflict_mask.shape == pixel_coords[0].shape
```

### 4.2 Integration Tests

```python
def test_full_pipeline():
    """Test complete pipeline"""
    
    state = 'Andhra Pradesh'
    project_type = 'solar'
    
    pipeline = DataProcessingPipeline(state, project_type)
    
    aoi_bounds = (13.0, 77.0, 20.0, 84.0)  # AP bounds
    date_range = ('2023-01-01', '2023-03-31')
    
    result = pipeline.run_full_pipeline(aoi_bounds, date_range)
    
    assert result['status'] == 'success'
    assert result['num_sites'] > 0
    assert result['total_capacity_mw'] > 0
```

---

## 5. Deployment

### 5.1 Docker Setup

```dockerfile
# Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV GDAL_CONFIG=/usr/bin/gdal-config
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.2 Docker Compose

```yaml
# docker-compose.yml

version: '3.8'

services:
  postgres:
    image: postgis/postgis:15-3.3
    environment:
      POSTGRES_USER: gis_user
      POSTGRES_PASSWORD: gis_password
      POSTGRES_DB: gis_land_allocation
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DB_HOST: postgres
      DB_USER: gis_user
      DB_PASSWORD: gis_password
      DB_NAME: gis_land_allocation
    depends_on:
      - postgres
    volumes:
      - ./outputs:/app/outputs
      - ./data:/app/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

---

## 6. Performance Optimization

### 6.1 Caching Strategy

```python
from functools import lru_cache
import redis
import pickle

class CacheManager:
    """Manage caching for expensive operations"""
    
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379)
    
    def cache_satellite_data(self, state, date_range, ttl=86400*7):
        """Cache fetched satellite data (1 week TTL)"""
        
        cache_key = f"satellite_{state}_{date_range[0]}_{date_range[1]}"
        
        satellite_data = self.redis_client.get(cache_key)
        if satellite_data:
            return pickle.loads(satellite_data)
        
        # Fetch fresh data
        processor = Sentinel2Processor(config)
        data = processor.fetch_sentinel2_image(...)
        
        # Cache
        self.redis_client.setex(
            cache_key,
            ttl,
            pickle.dumps(data)
        )
        
        return data

@lru_cache(maxsize=128)
def get_dem_data_cached(state):
    """Cache DEM data"""
    
    return load_dem_data(state)
```

### 6.2 Parallel Processing

```python
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, as_completed

class ParallelProcessor:
    """Parallel processing of raster data"""
    
    @staticmethod
    def process_districts_parallel(state, districts, process_func):
        """Process multiple districts in parallel"""
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(process_func, district): district
                for district in districts
            }
            
            results = {}
            for future in as_completed(futures):
                district = futures[future]
                try:
                    results[district] = future.result()
                except Exception as e:
                    print(f"Error processing {district}: {str(e)}")
        
        return results
    
    @staticmethod
    def batch_raster_processing(raster_data, batch_size=1000):
        """Process large rasters in batches"""
        
        h, w = raster_data.shape[:2]
        
        for i in range(0, h, batch_size):
            for j in range(0, w, batch_size):
                batch = raster_data[
                    i:min(i+batch_size, h),
                    j:min(j+batch_size, w)
                ]
                yield batch, (i, j)
```

