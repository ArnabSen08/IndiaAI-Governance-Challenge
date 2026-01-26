# GIS-Based AI Land Allocation System for Renewable Energy
## Conflict-Free Land Suitability and Automated Allocation Platform

---

## Executive Summary

The **GIS-Based AI Land Allocation System** is an automated solution that uses satellite imagery, geospatial analysis, and machine learning to identify optimal lands for solar and wind energy projects while preventing conflicts with stakeholders, protected areas, and existing land uses.

### Key Objectives
- 🛰️ Automated land suitability assessment using satellite data
- ⚡ Optimal site selection for solar and wind projects
- 🔍 Conflict detection with protected areas, water bodies, and settlements
- 📊 Multi-criteria analysis using geospatial and ML techniques
- 🚀 Scalable allocation system for state-wide deployment
- 📈 Data-driven decision making for renewable energy expansion

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│            Data Ingestion Layer                           │
│  ┌─ Satellite Imagery (Sentinel-1/2, Landsat)           │
│  ├─ Government Databases (Land, Water, Protected Areas) │
│  ├─ Administrative Boundaries (GeoJSON)                 │
│  ├─ Infrastructure Data (Roads, Substations)            │
│  └─ Climate Data (Solar Irradiance, Wind Speed)         │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────┐
│        Geospatial Processing Layer                        │
│  ┌─ Satellite Image Processing (GDAL/Rasterio)          │
│  ├─ Feature Extraction (NDVI, Land Cover Classification) │
│  ├─ Vector Operations (Buffering, Clipping, Overlays)    │
│  ├─ Coordinate Transformation (WGS84 → UTM)             │
│  └─ Spatial Indexing (QuadTree, R-Tree)                  │
└────────────────┬──────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────┐
│         ML Land Suitability Analysis Layer                │
│  ┌─ Land Cover Classification (CNN: U-Net)               │
│  ├─ Slope & Elevation Analysis (DEM Processing)          │
│  ├─ Multi-Criteria Suitability Scoring (ML Regression)   │
│  ├─ Conflict Detection (Classification Models)           │
│  └─ Land Fragmentation Analysis                          │
└────────────────┬──────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────┐
│         Optimization & Allocation Layer                    │
│  ┌─ Site Clustering & Grouping                           │
│  ├─ Resource Utilization Optimization                    │
│  ├─ Grid Connection Cost Analysis                        │
│  ├─ Environmental Impact Assessment                      │
│  └─ Allocation Algorithm (Linear Programming/Genetic)    │
└────────────────┬──────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────┐
│         Application Layer                                  │
│  ┌─ Web Portal (Interactive Map Visualization)           │
│  ├─ REST/GraphQL APIs (Data Access & Analysis)           │
│  ├─ Analytics Dashboard (KPIs & Reports)                 │
│  └─ Decision Support System (Recommendations)            │
└──────────────────────────────────────────────────────────┘
```

### 1.2 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Geospatial Processing** | GDAL, Rasterio, GeoPandas, Shapely |
| **ML Frameworks** | TensorFlow, PyTorch, Scikit-learn, XGBoost |
| **Satellite Data** | Sentinel Hub API, Landsat 8/9, USGS EROS |
| **Databases** | PostGIS (spatial), TimescaleDB (time series) |
| **Web Framework** | FastAPI, Flask, Django |
| **Frontend** | Mapbox GL, Leaflet, OpenLayers |
| **Cloud** | AWS (S3, EC2, SageMaker), GCP (Earth Engine) |
| **Optimization** | CVXPY, PuLP, Optuna |

---

## 2. Data Sources & Integration

### 2.1 Satellite Imagery Sources

#### Sentinel-2 Multispectral Imagery
- **Resolution**: 10-60 m
- **Bands**: 13 spectral bands (visible, NIR, SWIR)
- **Revisit**: 5 days
- **Cost**: Free
- **Use**: Land cover classification, NDVI calculation, water body detection

#### Sentinel-1 SAR Imagery
- **Resolution**: 10-20 m
- **Polarization**: VV, VH
- **Revisit**: 6 days
- **Cost**: Free
- **Use**: All-weather terrain analysis, water detection, vegetation mapping

#### Landsat 8/9
- **Resolution**: 15-100 m
- **Bands**: 11 spectral bands
- **Revisit**: 16 days
- **Cost**: Free
- **Use**: Historical analysis, NDVI time series

#### SRTM/ASTER DEM
- **Resolution**: 30 m
- **Use**: Elevation, slope, aspect analysis

### 2.2 Geospatial Datasets

```python
class GeospatialDataSources:
    """Data sources for GIS analysis"""
    
    LAND_COVER = {
        'provider': 'ESA/Copernicus',
        'dataset': 'CORINE Land Cover',
        'resolution': '100m',
        'categories': [
            'Urban',
            'Agricultural',
            'Forest',
            'Grassland',
            'Bare soil',
            'Water bodies'
        ]
    }
    
    PROTECTED_AREAS = {
        'provider': 'UNESCO/UNEP-WCMC',
        'dataset': 'World Database on Protected Areas',
        'update_frequency': 'Quarterly'
    }
    
    WATER_BODIES = {
        'provider': 'USGS',
        'dataset': 'Global Surface Water Explorer',
        'resolution': '30m'
    }
    
    FOREST_COVER = {
        'provider': 'Global Forest Watch',
        'dataset': 'Hansen Global Forest Cover',
        'resolution': '30m'
    }
    
    POWER_GRID = {
        'provider': 'National Load Despatch Center',
        'data': 'Substation locations, transmission lines'
    }
    
    CLIMATE_DATA = {
        'solar_irradiance': 'PVGIS, NASA POWER API',
        'wind_speed': 'NASA MERRA-2, Global Wind Atlas',
        'temperature': 'NOAA, WorldClim'
    }
```

### 2.3 Data Integration Pipeline

```python
import rasterio
import geopandas as gpd
from sentinelhub import SentinelHubRequest, DataCollection
import xarray as xr

class DataIntegrationPipeline:
    """Integrate multiple geospatial data sources"""
    
    def __init__(self, aoi_bounds, crs='EPSG:4326'):
        self.aoi_bounds = aoi_bounds  # (minx, miny, maxx, maxy)
        self.crs = crs
    
    def fetch_sentinel2_imagery(self, date_range):
        """Fetch Sentinel-2 imagery via Sentinel Hub API"""
        
        request = SentinelHubRequest(
            evalscript=self.get_ndvi_evalscript(),
            input_data=[
                SentinelHubRequest.input_data(
                    DataCollection.SENTINEL2_L2A,
                    time_interval=date_range
                )
            ],
            responses=[
                SentinelHubRequest.output_response('default', ResponseType.TIFF),
                SentinelHubRequest.output_response('dataMask', ResponseType.TIFF)
            ],
            bbox=self.aoi_bounds,
            resolution=(10, 10),
            data_folder='./data/sentinel2'
        )
        
        request.get_data(save_data=True)
        return request.get_array_data()
    
    def fetch_protected_areas(self):
        """Fetch protected areas from WDPA"""
        
        # Query WDPA database (via API or local GeoDatabase)
        wdpa_gdf = gpd.read_file(
            'https://www.protectedplanet.net/wdpa.json',
            bbox=self.aoi_bounds
        )
        
        return wdpa_gdf
    
    def fetch_dem_data(self):
        """Fetch Digital Elevation Model (SRTM 30m)"""
        
        dem = rasterio.open(
            'https://cloud.sdsc.edu/v1/AUTH_opentopography/Raster/'
            'SRTM_GL30/SRTM_GL30_srtm/SRTM_GL30_srtm_srtm.vrt'
        )
        
        # Clip to AOI
        dem_clipped = rasterio.mask.mask(
            dem,
            self.aoi_bounds,
            crop=True
        )
        
        return dem_clipped
    
    def fetch_power_infrastructure(self):
        """Fetch power grid infrastructure"""
        
        # Load from government databases or OpenStreetMap
        substations = gpd.read_file(
            'substations.geojson'
        )
        transmission_lines = gpd.read_file(
            'transmission_lines.geojson'
        )
        
        return substations, transmission_lines
    
    def get_ndvi_evalscript(self):
        """Evaluate Script for NDVI calculation"""
        
        return """
        //VERSION=3
        function setup() {
            return {
                input: [{
                    bands: ["B04", "B08"]
                }],
                output: {
                    bands: 1,
                    sampleType: "FLOAT32"
                }
            };
        }
        
        function evaluatePixel(sample) {
            let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
            return [ndvi];
        }
        """
```

---

## 3. Geospatial Analysis Methods

### 3.1 Land Cover Classification

#### U-Net CNN for Land Cover Segmentation

```python
import tensorflow as tf
from tensorflow.keras.layers import *
import numpy as np

class LandCoverClassifier:
    """
    Semantic segmentation of satellite imagery
    into land cover classes using U-Net
    """
    
    def __init__(self, input_shape=(256, 256, 13), num_classes=6):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = self._build_unet()
    
    def _build_unet(self):
        """Build U-Net architecture for segmentation"""
        
        inputs = Input(shape=self.input_shape)
        
        # Encoder
        conv1 = Conv2D(64, 3, padding='same', activation='relu')(inputs)
        conv1 = Conv2D(64, 3, padding='same', activation='relu')(conv1)
        pool1 = MaxPooling2D(2)(conv1)
        
        conv2 = Conv2D(128, 3, padding='same', activation='relu')(pool1)
        conv2 = Conv2D(128, 3, padding='same', activation='relu')(conv2)
        pool2 = MaxPooling2D(2)(conv2)
        
        conv3 = Conv2D(256, 3, padding='same', activation='relu')(pool2)
        conv3 = Conv2D(256, 3, padding='same', activation='relu')(conv3)
        pool3 = MaxPooling2D(2)(conv3)
        
        # Bottleneck
        conv4 = Conv2D(512, 3, padding='same', activation='relu')(pool3)
        conv4 = Conv2D(512, 3, padding='same', activation='relu')(conv4)
        
        # Decoder
        up5 = UpSampling2D(2)(conv4)
        up5 = Concatenate()([up5, conv3])
        conv5 = Conv2D(256, 3, padding='same', activation='relu')(up5)
        conv5 = Conv2D(256, 3, padding='same', activation='relu')(conv5)
        
        up6 = UpSampling2D(2)(conv5)
        up6 = Concatenate()([up6, conv2])
        conv6 = Conv2D(128, 3, padding='same', activation='relu')(up6)
        conv6 = Conv2D(128, 3, padding='same', activation='relu')(conv6)
        
        up7 = UpSampling2D(2)(conv6)
        up7 = Concatenate()([up7, conv1])
        conv7 = Conv2D(64, 3, padding='same', activation='relu')(up7)
        conv7 = Conv2D(64, 3, padding='same', activation='relu')(conv7)
        
        # Output
        outputs = Conv2D(
            self.num_classes, 
            1, 
            padding='same', 
            activation='softmax'
        )(conv7)
        
        model = tf.keras.Model(inputs, outputs)
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def classify_satellite_image(self, satellite_image):
        """
        Classify land cover in satellite imagery
        
        Args:
            satellite_image: (H, W, 13) Sentinel-2 image
            
        Returns:
            land_cover_map: (H, W) classified pixels
        """
        
        # Normalize image
        normalized = satellite_image / 10000.0  # Sentinel-2 DNs
        
        # Segment into patches
        patches = self._create_patches(normalized)
        
        # Predict on patches
        predictions = self.model.predict(patches)
        
        # Reconstruct full image
        land_cover_map = self._reconstruct_from_patches(predictions)
        
        return land_cover_map
    
    def _create_patches(self, image, patch_size=256, overlap=32):
        """Create overlapping patches from image"""
        h, w = image.shape[:2]
        patches = []
        positions = []
        
        for i in range(0, h - patch_size, patch_size - overlap):
            for j in range(0, w - patch_size, patch_size - overlap):
                patch = image[i:i+patch_size, j:j+patch_size]
                if patch.shape[0] == patch_size and patch.shape[1] == patch_size:
                    patches.append(patch)
                    positions.append((i, j))
        
        return np.array(patches), positions
    
    def _reconstruct_from_patches(self, predictions):
        """Reconstruct full image from patch predictions"""
        # Use average pooling for overlapping regions
        pass
```

### 3.2 Suitability Scoring Framework

#### Multi-Criteria Suitability Analysis

```python
import numpy as np
from scipy.ndimage import distance_transform_edt
from sklearn.preprocessing import MinMaxScaler

class SuitabilityScoringEngine:
    """
    Calculate land suitability for solar/wind projects
    using multi-criteria analysis
    """
    
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 100))
        self.weights = {
            'solar': {
                'slope': 0.15,
                'land_cover': 0.20,
                'distance_settlement': 0.15,
                'distance_road': 0.10,
                'solar_irradiance': 0.25,
                'elevation': 0.10,
                'conflicts': 0.05
            },
            'wind': {
                'slope': 0.10,
                'wind_speed': 0.35,
                'land_cover': 0.15,
                'distance_settlement': 0.15,
                'distance_road': 0.10,
                'elevation': 0.10,
                'conflicts': 0.05
            }
        }
    
    def calculate_solar_suitability(self, slope, land_cover, 
                                   distance_settlement, distance_road,
                                   solar_irradiance, elevation, 
                                   conflict_mask):
        """
        Calculate suitability for solar projects
        
        Args:
            slope: Slope in degrees (DEM derived)
            land_cover: Land cover classification
            distance_settlement: Distance to nearest settlement (m)
            distance_road: Distance to nearest road (m)
            solar_irradiance: Annual GHI (kWh/m²/year)
            elevation: Elevation in meters
            conflict_mask: Boolean array (1=conflict, 0=no conflict)
        
        Returns:
            suitability_score: (0-100) score for each pixel
        """
        
        # 1. Slope Score: Prefer flat to moderate slopes (0-15°)
        slope_score = 100 - np.clip(slope * 5, 0, 100)
        
        # 2. Land Cover Score: Prefer barren/grassland, penalize forest/water
        land_cover_suitability = {
            'urban': 0,           # Conflict
            'agricultural': 30,   # Low suitable
            'forest': 5,          # Very low
            'grassland': 80,      # High
            'bare_soil': 100,     # Optimal
            'water': 0            # Conflict
        }
        lc_score = np.array([land_cover_suitability.get(lc, 0) 
                             for lc in land_cover.flatten()]).reshape(land_cover.shape)
        
        # 3. Settlement Distance: Prefer farther, but not too far
        # Optimal: 100m - 5km from nearest settlement
        distance_settlement_norm = self.scaler.fit_transform(
            distance_settlement.flatten().reshape(-1, 1)
        ).reshape(distance_settlement.shape)
        settlement_score = 100 - np.abs(distance_settlement_norm - 60)
        
        # 4. Road Distance: Closer to roads = better (for evacuation)
        road_score = 100 - np.clip(distance_road / 50, 0, 100)
        
        # 5. Solar Irradiance: Higher is better
        # Normalize to 0-100 (assume range 1000-2000 kWh/m²/year in India)
        irradiance_score = np.clip((solar_irradiance - 1000) / 10, 0, 100)
        
        # 6. Elevation: Prefer lower elevations
        elevation_score = 100 - np.clip(elevation / 30, 0, 100)
        
        # 7. Conflict Penalty: Exclude conflict areas
        conflict_penalty = np.where(conflict_mask, 0, 1)
        
        # Calculate weighted average
        suitability = (
            self.weights['solar']['slope'] * slope_score +
            self.weights['solar']['land_cover'] * lc_score +
            self.weights['solar']['distance_settlement'] * settlement_score +
            self.weights['solar']['distance_road'] * road_score +
            self.weights['solar']['solar_irradiance'] * irradiance_score +
            self.weights['solar']['elevation'] * elevation_score
        ) * conflict_penalty
        
        return np.clip(suitability, 0, 100)
    
    def calculate_wind_suitability(self, slope, land_cover,
                                  distance_settlement, distance_road,
                                  wind_speed, elevation,
                                  conflict_mask):
        """
        Calculate suitability for wind projects
        """
        
        # 1. Slope Score: Prefer slopes 5-30° for wind farms
        slope_score = 100 - np.abs(slope - 15) * 3
        
        # 2. Wind Speed: Critical factor (minimum ~6 m/s viable)
        # Optimal: > 8 m/s
        wind_score = np.clip((wind_speed - 4) * 12.5, 0, 100)
        
        # 3. Land Cover Score: Prefer grassland, avoid forest/water
        land_cover_suitability = {
            'urban': 0,
            'agricultural': 40,
            'forest': 10,
            'grassland': 90,
            'bare_soil': 80,
            'water': 0
        }
        lc_score = np.array([land_cover_suitability.get(lc, 0) 
                             for lc in land_cover.flatten()]).reshape(land_cover.shape)
        
        # 4. Settlement Distance: Minimum 300-500m from settlements
        settlement_score = np.where(
            distance_settlement > 500,
            100 - np.clip(distance_settlement / 100, 0, 50),
            0
        )
        
        # 5. Road Distance: Access for maintenance
        road_score = 100 - np.clip(distance_road / 100, 0, 100)
        
        # 6. Elevation: Higher elevations preferred (better wind speeds)
        elevation_score = np.clip(elevation / 30, 0, 100)
        
        # 7. Conflict Penalty
        conflict_penalty = np.where(conflict_mask, 0, 1)
        
        suitability = (
            self.weights['wind']['slope'] * slope_score +
            self.weights['wind']['land_cover'] * lc_score +
            self.weights['wind']['distance_settlement'] * settlement_score +
            self.weights['wind']['distance_road'] * road_score +
            self.weights['wind']['wind_speed'] * wind_score +
            self.weights['wind']['elevation'] * elevation_score
        ) * conflict_penalty
        
        return np.clip(suitability, 0, 100)
```

### 3.3 Conflict Detection

```python
import geopandas as gpd
from shapely.geometry import box, Point
from shapely.ops import unary_union

class ConflictDetector:
    """Detect conflicts with protected areas, settlements, water bodies"""
    
    def __init__(self, aoi_bounds):
        self.aoi_bounds = aoi_bounds
        self.conflict_categories = {}
    
    def detect_all_conflicts(self, pixel_coords):
        """
        Detect all conflicts for given coordinates
        
        Returns:
            conflict_mask: (H, W) boolean array
            conflict_details: Dict of conflict types and locations
        """
        
        conflicts = {
            'protected_areas': self.detect_protected_areas(pixel_coords),
            'water_bodies': self.detect_water_bodies(pixel_coords),
            'settlements': self.detect_settlements(pixel_coords),
            'agricultural_land': self.detect_agricultural_land(pixel_coords),
            'infrastructure': self.detect_infrastructure_conflicts(pixel_coords)
        }
        
        # Combine all conflicts
        conflict_mask = np.zeros(pixel_coords[0].shape, dtype=bool)
        
        for conflict_type, mask in conflicts.items():
            conflict_mask |= mask
        
        return conflict_mask, conflicts
    
    def detect_protected_areas(self, pixel_coords):
        """Detect if land falls in protected areas"""
        
        # Load protected areas
        protected_areas = gpd.read_file('protected_areas.geojson')
        
        # Create points from pixel coordinates
        points = gpd.GeoDataFrame(
            geometry=[Point(xy) for xy in zip(pixel_coords[0].flat, 
                                             pixel_coords[1].flat)]
        )
        
        # Spatial join
        intersects = gpd.sjoin(
            points,
            protected_areas,
            how='inner',
            predicate='within'
        )
        
        # Create mask
        mask = np.zeros(pixel_coords[0].shape, dtype=bool)
        mask.flat[intersects.index.values] = True
        
        return mask
    
    def detect_water_bodies(self, pixel_coords, buffer_distance=100):
        """Detect water bodies (NDWI > threshold)"""
        
        # NDWI calculated from satellite data
        ndwi = calculate_ndwi(satellite_image)
        
        # Water pixels have NDWI > 0.3
        water_mask = ndwi > 0.3
        
        # Buffer to account for hydrogeology
        from scipy.ndimage import binary_dilation
        water_buffer = binary_dilation(water_mask, iterations=int(buffer_distance/30))
        
        return water_buffer
    
    def detect_settlements(self, pixel_coords, buffer_distance=500):
        """Detect settlements from land cover classification"""
        
        # Urban pixels identified from land cover classification
        urban_pixels = (land_cover == 'urban')
        
        # Buffer distance: 500m minimum from settlements
        from scipy.ndimage import binary_dilation
        settlement_buffer = binary_dilation(
            urban_pixels, 
            iterations=int(buffer_distance/30)
        )
        
        return settlement_buffer
    
    def detect_infrastructure_conflicts(self, pixel_coords):
        """Detect conflicts with existing energy infrastructure"""
        
        # Load power substations and transmission lines
        substations = gpd.read_file('substations.geojson')
        transmission_lines = gpd.read_file('transmission_lines.geojson')
        
        # Buffer zones around infrastructure
        substation_buffer = substations.buffer(300)  # 300m buffer
        transmission_buffer = transmission_lines.buffer(200)  # 200m buffer
        
        # Combined conflict zones
        conflict_zones = unary_union([substation_buffer, transmission_buffer])
        
        # Create mask
        points = gpd.GeoDataFrame(
            geometry=[Point(xy) for xy in zip(pixel_coords[0].flat, 
                                             pixel_coords[1].flat)]
        )
        
        mask = points.geometry.within(conflict_zones).values.reshape(
            pixel_coords[0].shape
        )
        
        return mask
```

---

## 4. Machine Learning Models

### 4.1 Land Suitability Regression Model

```python
import xgboost as xgb
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd

class LandSuitabilityModel:
    """
    XGBoost model for predicting land suitability
    """
    
    def __init__(self):
        self.model = xgb.XGBRegressor(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            objective='reg:squarederror'
        )
    
    def prepare_training_features(self, satellite_imagery, dem, 
                                 climate_data, known_sites):
        """
        Prepare features for model training
        
        Args:
            satellite_imagery: Sentinel-2 bands
            dem: Digital Elevation Model
            climate_data: Solar irradiance, wind speed
            known_sites: Labeled solar/wind sites
        
        Returns:
            X_train: Feature matrix
            y_train: Suitability labels
        """
        
        features = []
        labels = []
        
        for site_id, (lat, lon, site_type, capacity) in known_sites.items():
            pixel_features = {
                # Spectral indices
                'ndvi': calculate_ndvi(satellite_imagery),
                'ndbi': calculate_ndbi(satellite_imagery),
                'ndwi': calculate_ndwi(satellite_imagery),
                
                # Topographic features
                'elevation': get_dem_value(dem, lat, lon),
                'slope': calculate_slope(dem, lat, lon),
                'aspect': calculate_aspect(dem, lat, lon),
                'roughness': calculate_roughness(dem, lat, lon),
                
                # Climate features
                'solar_irradiance': climate_data['solar_irradiance'][lat, lon],
                'wind_speed': climate_data['wind_speed'][lat, lon],
                'temperature': climate_data['temperature'][lat, lon],
                'precipitation': climate_data['precipitation'][lat, lon],
                
                # Land cover
                'distance_water': distance_to_water(lat, lon),
                'distance_urban': distance_to_urban(lat, lon),
                'distance_road': distance_to_road(lat, lon),
                'distance_substation': distance_to_substation(lat, lon),
                
                # Site type (one-hot encoded)
                'is_solar': 1 if site_type == 'solar' else 0,
                'is_wind': 1 if site_type == 'wind' else 0,
            }
            
            # Normalize capacity to suitability score (0-100)
            # Assume capacity range 1-100 MW
            suitability_label = min(capacity / 10 * 10, 100)
            
            features.append(pixel_features)
            labels.append(suitability_label)
        
        X_train = pd.DataFrame(features)
        y_train = np.array(labels)
        
        return X_train, y_train
    
    def train(self, X_train, y_train):
        """Train suitability model"""
        
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_train, y_train)],
            early_stopping_rounds=20,
            verbose=0
        )
    
    def predict_suitability(self, features):
        """Predict suitability for given features"""
        
        suitability = self.model.predict(features)
        return np.clip(suitability, 0, 100)
    
    def get_feature_importance(self, top_n=15):
        """Get important features for suitability"""
        
        importance = self.model.feature_importances_
        indices = np.argsort(importance)[-top_n:][::-1]
        
        return [
            {
                'feature': self.model.feature_names_in_[i],
                'importance': importance[i]
            }
            for i in indices
        ]
```

### 4.2 Conflict Classification Model

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support

class ConflictClassifier:
    """
    Classify pixels as conflict/no-conflict
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=10,
            class_weight='balanced'
        )
    
    def prepare_conflict_labels(self, geospatial_layers):
        """
        Prepare labeled training data for conflicts
        """
        
        conflict_labels = np.zeros(grid_shape, dtype=bool)
        
        # Protected areas
        protected_mask = load_protected_areas_mask()
        conflict_labels |= protected_mask
        
        # Water bodies
        water_mask = load_water_bodies_mask()
        conflict_labels |= water_mask
        
        # Settlements
        urban_mask = load_urban_mask()
        conflict_labels |= urban_mask
        
        # Infrastructure
        infrastructure_mask = load_infrastructure_mask()
        conflict_labels |= infrastructure_mask
        
        return conflict_labels
    
    def train(self, features, conflict_labels):
        """Train conflict classifier"""
        
        self.model.fit(features, conflict_labels)
    
    def predict_conflicts(self, features):
        """Predict conflict probability"""
        
        probabilities = self.model.predict_proba(features)
        return probabilities[:, 1]  # Probability of conflict
```

---

## 5. Land Allocation Algorithm

### 5.1 Optimization-Based Allocation

```python
import cvxpy as cp
import numpy as np
from scipy.spatial.distance import cdist

class LandAllocationOptimizer:
    """
    Optimize land allocation for renewable energy projects
    """
    
    def __init__(self, state_config):
        self.state_config = state_config  # Target capacity, budget, etc.
    
    def allocate_lands_linear_programming(self, candidate_sites):
        """
        Linear programming approach to allocate lands
        
        Maximize: Sum of suitability scores
        Subject to:
            - No conflicts
            - Budget constraints
            - Minimum site size
            - Grid connection feasibility
            - Quota constraints (e.g., % solar vs wind)
        """
        
        n_sites = len(candidate_sites)
        
        # Decision variables: binary (allocate or not)
        x = cp.Variable(n_sites, boolean=True)
        
        # Objective: Maximize total suitability score
        suitability_scores = np.array([
            site['suitability_score'] for site in candidate_sites
        ])
        objective = cp.Maximize(suitability_scores @ x)
        
        constraints = []
        
        # Constraint 1: Total capacity target
        capacities = np.array([site['capacity_mw'] for site in candidate_sites])
        target_capacity = self.state_config['target_capacity_mw']
        constraints.append(capacities @ x >= target_capacity * 0.9)
        constraints.append(capacities @ x <= target_capacity * 1.1)
        
        # Constraint 2: Budget
        costs = np.array([site['installation_cost_cr'] for site in candidate_sites])
        budget = self.state_config['budget_cr']
        constraints.append(costs @ x <= budget)
        
        # Constraint 3: No conflicts (conflict sites must have x=0)
        for i, site in enumerate(candidate_sites):
            if site['has_conflict']:
                constraints.append(x[i] == 0)
        
        # Constraint 4: Geographical distribution
        # At least 30% in each district
        districts = set([site['district'] for site in candidate_sites])
        for district in districts:
            district_capacity = sum([
                site['capacity_mw'] for site in candidate_sites 
                if site['district'] == district
            ])
            district_indices = [
                i for i, site in enumerate(candidate_sites)
                if site['district'] == district
            ]
            if district_indices:
                district_capacities = np.array([
                    candidate_sites[i]['capacity_mw'] 
                    for i in district_indices
                ])
                constraints.append(
                    district_capacities @ x[district_indices] >= 
                    target_capacity * 0.15
                )
        
        # Constraint 5: Grid connection feasibility
        # Prefer sites closer to substations
        for i, site in enumerate(candidate_sites):
            if site['distance_to_substation_km'] > 50:
                constraints.append(x[i] <= 0.5)  # Soft constraint
        
        # Solve
        problem = cp.Problem(objective, constraints)
        problem.solve(solver=cp.GLPK, verbose=True)
        
        # Extract allocated sites
        allocated_sites = [
            candidate_sites[i] for i in range(n_sites)
            if x.value[i] > 0.5
        ]
        
        return allocated_sites, problem.value
```

### 5.2 Genetic Algorithm Approach

```python
from deap import base, creator, tools, algorithms
import random

class GeneticAllocationOptimizer:
    """
    Genetic Algorithm for land allocation
    """
    
    def __init__(self, candidate_sites, state_config):
        self.candidate_sites = candidate_sites
        self.state_config = state_config
        self.setup_deap()
    
    def setup_deap(self):
        """Setup DEAP framework for genetic algorithm"""
        
        # Fitness: maximize suitability, minimize cost
        creator.create(
            "FitnessMulti",
            base.Fitness,
            weights=(1.0, -1.0)  # Maximize suitability, minimize cost
        )
        creator.create("Individual", list, fitness=creator.FitnessMulti)
        
        self.toolbox = base.Toolbox()
        
        # Attribute: allocation (0 or 1)
        self.toolbox.register(
            "allocation",
            random.randint,
            0, 1
        )
        
        # Individual: list of allocations
        self.toolbox.register(
            "individual",
            tools.initRepeat,
            creator.Individual,
            self.toolbox.allocation,
            n=len(self.candidate_sites)
        )
        
        # Population
        self.toolbox.register(
            "population",
            tools.initRepeat,
            list,
            self.toolbox.individual
        )
        
        # Genetic operators
        self.toolbox.register("evaluate", self.evaluate_allocation)
        self.toolbox.register("mate", tools.cxBlend, alpha=0.5)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
    
    def evaluate_allocation(self, allocation):
        """
        Evaluate fitness of allocation
        
        Returns:
            (total_suitability, total_cost)
        """
        
        total_suitability = 0
        total_cost = 0
        total_capacity = 0
        
        for i, allocated in enumerate(allocation):
            if allocated:
                site = self.candidate_sites[i]
                total_suitability += site['suitability_score']
                total_cost += site['installation_cost_cr']
                total_capacity += site['capacity_mw']
        
        # Penalty for not meeting capacity target
        capacity_penalty = abs(
            total_capacity - self.state_config['target_capacity_mw']
        ) / self.state_config['target_capacity_mw']
        
        total_suitability -= capacity_penalty * 50
        
        return total_suitability, total_cost
    
    def optimize(self, population_size=100, generations=50):
        """Run genetic algorithm"""
        
        pop = self.toolbox.population(n=population_size)
        
        pop, logbook = algorithms.eaSimple(
            pop,
            self.toolbox,
            cxpb=0.7,
            mutpb=0.3,
            ngen=generations,
            verbose=True
        )
        
        # Get best solution
        best_individual = tools.selBest(pop, k=1)[0]
        
        allocated_sites = [
            self.candidate_sites[i]
            for i, allocated in enumerate(best_individual)
            if allocated
        ]
        
        return allocated_sites
```

---

## 6. Web Interface & APIs

### 6.1 FastAPI Endpoints

```python
from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import FileResponse
import geopandas as gpd

app = FastAPI(
    title="GIS Land Allocation System",
    description="Automated land suitability and allocation for renewable energy"
)

@app.post("/api/v1/suitability/calculate")
async def calculate_suitability(
    state: str,
    project_type: str = Query(..., enum=['solar', 'wind']),
    aoi_geojson: str = None
):
    """Calculate suitability maps"""
    
    pipeline = DataIntegrationPipeline(aoi_bounds=parse_geojson(aoi_geojson))
    satellite_imagery = pipeline.fetch_sentinel2_imagery(date_range)
    dem = pipeline.fetch_dem_data()
    climate_data = pipeline.fetch_climate_data()
    
    # Land cover classification
    classifier = LandCoverClassifier()
    land_cover = classifier.classify_satellite_image(satellite_imagery)
    
    # Suitability scoring
    suitability_engine = SuitabilityScoringEngine()
    
    if project_type == 'solar':
        suitability_map = suitability_engine.calculate_solar_suitability(
            slope=calculate_slope(dem),
            land_cover=land_cover,
            distance_settlement=calculate_distance_raster(urban_pixels),
            distance_road=calculate_distance_raster(road_pixels),
            solar_irradiance=climate_data['solar_irradiance'],
            elevation=dem,
            conflict_mask=conflict_detector.detect_all_conflicts()[0]
        )
    else:
        suitability_map = suitability_engine.calculate_wind_suitability(
            slope=calculate_slope(dem),
            land_cover=land_cover,
            distance_settlement=calculate_distance_raster(urban_pixels),
            distance_road=calculate_distance_raster(road_pixels),
            wind_speed=climate_data['wind_speed'],
            elevation=dem,
            conflict_mask=conflict_detector.detect_all_conflicts()[0]
        )
    
    # Save as GeoTIFF
    save_geotiff('suitability_map.tif', suitability_map)
    
    return {
        'suitability_map': 'suitability_map.tif',
        'statistics': {
            'mean': np.mean(suitability_map),
            'max': np.max(suitability_map),
            'suitable_area_percent': np.sum(suitability_map > 50) / suitability_map.size * 100
        }
    }

@app.post("/api/v1/allocation/optimize")
async def optimize_allocation(
    state: str,
    target_capacity_mw: int,
    budget_cr: float,
    suitability_map: UploadFile = File(...)
):
    """Optimize land allocation"""
    
    # Load suitability map
    suitability_raster = rasterio.open(suitability_map.file)
    
    # Identify candidate sites
    candidate_sites = identify_candidate_sites(suitability_raster)
    
    # Optimize allocation
    optimizer = LandAllocationOptimizer({
        'target_capacity_mw': target_capacity_mw,
        'budget_cr': budget_cr
    })
    
    allocated_sites, objective_value = optimizer.allocate_lands_linear_programming(
        candidate_sites
    )
    
    return {
        'allocated_sites': allocated_sites,
        'total_capacity_mw': sum([s['capacity_mw'] for s in allocated_sites]),
        'total_cost_cr': sum([s['installation_cost_cr'] for s in allocated_sites]),
        'objective_value': objective_value
    }

@app.get("/api/v1/conflicts/detect")
async def get_conflict_areas(
    state: str,
    format: str = Query('geojson', enum=['geojson', 'shapefile'])
):
    """Get conflict area boundaries"""
    
    conflict_detector = ConflictDetector(aoi_bounds=get_state_bounds(state))
    
    protected_areas = conflict_detector.detect_protected_areas(pixel_coords)
    water_bodies = conflict_detector.detect_water_bodies(pixel_coords)
    settlements = conflict_detector.detect_settlements(pixel_coords)
    
    # Convert to GeoJSON
    conflict_gdf = gpd.GeoDataFrame({
        'type': ['protected', 'water', 'settlement'],
        'geometry': [protected_areas, water_bodies, settlements]
    })
    
    if format == 'geojson':
        return conflict_gdf.to_json()
    else:
        conflict_gdf.to_file('conflicts.shapefile')
        return FileResponse('conflicts.zip')

@app.get("/api/v1/sites/recommend")
async def recommend_sites(
    state: str,
    project_type: str = Query(..., enum=['solar', 'wind']),
    top_n: int = Query(10, ge=1, le=100)
):
    """Get recommended sites for projects"""
    
    # Get pre-calculated suitability map
    suitability_map = load_suitability_map(state, project_type)
    
    # Extract top sites
    top_sites = extract_top_sites(suitability_map, top_n)
    
    # Calculate details (capacity, cost, grid connection, etc.)
    site_details = [calculate_site_details(site) for site in top_sites]
    
    return {
        'sites': site_details,
        'total_capacity_potential_mw': sum([s['capacity_potential_mw'] for s in site_details]),
        'total_area_sqkm': sum([s['area_sqkm'] for s in site_details])
    }
```

---

## 7. Implementation Roadmap

### Phase 1: Data Infrastructure (Months 1-2)
- [ ] Setup Sentinel Hub / Google Earth Engine accounts
- [ ] Create data ingestion pipelines
- [ ] Build PostGIS database
- [ ] Develop geospatial processing modules

### Phase 2: ML Model Development (Months 3-4)
- [ ] Train land cover classifier
- [ ] Develop suitability scoring models
- [ ] Implement conflict detection
- [ ] Validate on ground-truth data

### Phase 3: Optimization & Allocation (Months 5-6)
- [ ] Implement allocation algorithms
- [ ] Integrate grid connection analysis
- [ ] Develop cost estimation models
- [ ] Test allocation scenarios

### Phase 4: Web Interface & Deployment (Months 7-8)
- [ ] Develop REST APIs
- [ ] Create web portal with interactive maps
- [ ] Setup hosting and scaling
- [ ] User training and documentation

---

## 8. Success Metrics

| Metric | Target |
|--------|--------|
| Land Identification Accuracy | 90%+ |
| Conflict Detection Recall | 95%+ |
| Suitability Score RMSE | <10 points |
| Model Training Time (per state) | <24 hours |
| API Response Time | <5 seconds |
| Sites Recommended per State | 50-100 |
| Total Allocable Capacity | 10 GW+ |
| Cost Savings vs Manual Process | 70% |

