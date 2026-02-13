# Satellite Imagery & Geospatial Analysis Guide
## Processing Remote Sensing Data for Land Suitability Assessment

---

## 1. Satellite Data Processing Pipeline

### 1.1 Sentinel-2 Multispectral Processing

```python
import rasterio
from rasterio.plot import show
import numpy as np
import geopandas as gpd
from sentinelhub import SentinelHubRequest, DataCollection, MimeType, CRS

class Sentinel2Processor:
    """Process Sentinel-2 multispectral imagery"""
    
    # Sentinel-2 bands
    BANDS = {
        'B2': {'name': 'Blue', 'resolution': 10},
        'B3': {'name': 'Green', 'resolution': 10},
        'B4': {'name': 'Red', 'resolution': 10},
        'B5': {'name': 'VRE1', 'resolution': 20},
        'B6': {'name': 'VRE2', 'resolution': 20},
        'B7': {'name': 'VRE3', 'resolution': 20},
        'B8': {'name': 'NIR', 'resolution': 10},
        'B11': {'name': 'SWIR1', 'resolution': 20},
        'B12': {'name': 'SWIR2', 'resolution': 20}
    }
    
    def __init__(self, config):
        self.config = config
        self.sh_config = {
            'instance_id': config['sentinelhub_instance_id'],
            'client_id': config['sentinelhub_client_id'],
            'client_secret': config['sentinelhub_client_secret']
        }
    
    def fetch_sentinel2_image(self, bbox, date_range, output_path):
        """
        Fetch Sentinel-2 image for given area and date
        
        Args:
            bbox: (minx, miny, maxx, maxy) in WGS84
            date_range: ('2024-01-01', '2024-03-31')
            output_path: Save location
        """
        
        # Evalscript to get all bands
        evalscript = """
        //VERSION=3
        function setup() {
            return {
                input: [{
                    bands: ["B2", "B3", "B4", "B5", "B6", "B7", "B8", "B11", "B12", "SCL"],
                    units: "DN"
                }],
                output: {
                    bands: 10,
                    sampleType: "UINT16"
                }
            };
        }
        
        function evaluatePixel(sample) {
            if (sample.SCL == 3 || sample.SCL == 8 || sample.SCL == 9 || sample.SCL == 10 || sample.SCL == 11) {
                return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];  // Skip clouds/shadows
            }
            return [sample.B2, sample.B3, sample.B4, sample.B5, sample.B6, sample.B7, 
                    sample.B8, sample.B11, sample.B12, 1];
        }
        """
        
        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    DataCollection.SENTINEL2_L2A,
                    time_interval=date_range
                )
            ],
            responses=[
                SentinelHubRequest.output_response('default', MimeType.TIFF),
            ],
            bbox=bbox,
            resolution=(10, 10),
            config=self.sh_config
        )
        
        data = request.get_data()
        
        # Save as GeoTIFF
        with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=data.shape[1],
            width=data.shape[2],
            count=10,
            dtype=data.dtype
        ) as dst:
            for i in range(10):
                dst.write(data[0, i], i+1)
        
        return data
    
    def calculate_ndvi(self, sentinel2_image):
        """
        Calculate NDVI (Normalized Difference Vegetation Index)
        NDVI = (NIR - Red) / (NIR + Red)
        """
        
        red = sentinel2_image[:, :, 2].astype(float)  # B4
        nir = sentinel2_image[:, :, 6].astype(float)  # B8
        
        ndvi = (nir - red) / (nir + red + 1e-8)
        return ndvi
    
    def calculate_ndbi(self, sentinel2_image):
        """
        Calculate NDBI (Normalized Difference Built-up Index)
        NDBI = (SWIR1 - NIR) / (SWIR1 + NIR)
        """
        
        nir = sentinel2_image[:, :, 6].astype(float)   # B8
        swir1 = sentinel2_image[:, :, 7].astype(float) # B11
        
        ndbi = (swir1 - nir) / (swir1 + nir + 1e-8)
        return ndbi
    
    def calculate_ndwi(self, sentinel2_image):
        """
        Calculate NDWI (Normalized Difference Water Index)
        NDWI = (NIR - SWIR1) / (NIR + SWIR1)
        """
        
        nir = sentinel2_image[:, :, 6].astype(float)   # B8
        swir1 = sentinel2_image[:, :, 7].astype(float) # B11
        
        ndwi = (nir - swir1) / (nir + swir1 + 1e-8)
        return ndwi
    
    def calculate_ndii(self, sentinel2_image):
        """
        Calculate NDII (Normalized Difference Moisture Index)
        NDII = (NIR - SWIR1) / (NIR + SWIR1)
        """
        
        nir = sentinel2_image[:, :, 6].astype(float)   # B8
        swir2 = sentinel2_image[:, :, 8].astype(float) # B12
        
        ndii = (nir - swir2) / (nir + swir2 + 1e-8)
        return ndii
    
    def calculate_bsi(self, sentinel2_image):
        """
        Calculate BSI (Bare Soil Index)
        BSI = (SWIR1 + Red - NIR - Blue) / (SWIR1 + Red + NIR + Blue)
        """
        
        blue = sentinel2_image[:, :, 0].astype(float)  # B2
        red = sentinel2_image[:, :, 2].astype(float)   # B4
        nir = sentinel2_image[:, :, 6].astype(float)   # B8
        swir1 = sentinel2_image[:, :, 7].astype(float) # B11
        
        bsi = (swir1 + red - nir - blue) / (swir1 + red + nir + blue + 1e-8)
        return bsi
    
    def classify_land_cover(self, spectral_indices):
        """
        Classify land cover using spectral indices
        
        Categories:
            1. Water: NDWI > 0.3
            2. Dense vegetation: NDVI > 0.6
            3. Urban/Built-up: NDBI > 0.1
            4. Bare soil: BSI > 0.1 and NDVI < 0.4
            5. Agricultural: 0.4 < NDVI < 0.6
            6. Other
        """
        
        classification = np.zeros(spectral_indices['ndvi'].shape, dtype=np.uint8)
        
        # Water
        classification[spectral_indices['ndwi'] > 0.3] = 1
        
        # Dense vegetation
        classification[spectral_indices['ndvi'] > 0.6] = 2
        
        # Urban
        classification[spectral_indices['ndbi'] > 0.1] = 3
        
        # Bare soil
        bare_soil_mask = (spectral_indices['bsi'] > 0.1) & (spectral_indices['ndvi'] < 0.4)
        classification[bare_soil_mask] = 4
        
        # Agricultural
        agricultural_mask = (spectral_indices['ndvi'] > 0.4) & (spectral_indices['ndvi'] < 0.6)
        classification[agricultural_mask] = 5
        
        # Other
        classification[classification == 0] = 6
        
        return classification
```

### 1.2 Sentinel-1 SAR Processing

```python
import numpy as np
from scipy import ndimage

class Sentinel1Processor:
    """Process Sentinel-1 Synthetic Aperture Radar imagery"""
    
    def __init__(self, config):
        self.config = config
    
    def fetch_sentinel1_image(self, bbox, date_range, output_path):
        """Fetch Sentinel-1 VV/VH data"""
        
        evalscript = """
        //VERSION=3
        function setup() {
            return {
                input: [{
                    bands: ["VV", "VH"]
                }],
                output: {
                    bands: 2,
                    sampleType: "FLOAT32"
                }
            };
        }
        
        function evaluatePixel(sample) {
            return [sample.VV, sample.VH];
        }
        """
        
        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    DataCollection.SENTINEL1_IW,
                    time_interval=date_range
                )
            ],
            responses=[
                SentinelHubRequest.output_response('default', MimeType.TIFF),
            ],
            bbox=bbox,
            resolution=(10, 10)
        )
        
        return request.get_data()
    
    def calculate_vratio(self, vv, vh):
        """V-ratio for water detection"""
        return vh / (vv + 1e-8)
    
    def calculate_coherence(self, vv_t1, vv_t2, vh_t1, vh_t2):
        """Calculate coherence between two acquisitions"""
        numerator = np.abs(vv_t1 * np.conj(vv_t2) + vh_t1 * np.conj(vh_t2))
        denominator = np.sqrt(np.abs(vv_t1)**2 + np.abs(vh_t1)**2) * \
                     np.sqrt(np.abs(vv_t2)**2 + np.abs(vh_t2)**2)
        return numerator / (denominator + 1e-8)
    
    def detect_water_bodies_sar(self, vv, vh):
        """Detect water bodies from SAR backscatter"""
        # Water has low backscatter (dark in SAR)
        # Threshold tuned empirically
        
        water_mask = vv < -15  # dB threshold
        
        # Morphological cleanup
        water_mask = ndimage.binary_erosion(water_mask, iterations=2)
        water_mask = ndimage.binary_dilation(water_mask, iterations=2)
        
        return water_mask
```

---

## 2. Digital Elevation Model (DEM) Processing

### 2.1 DEM Analysis

```python
import numpy as np
from scipy.ndimage import sobel, gaussian_filter

class DEMAnalyzer:
    """Analyze topography from DEM"""
    
    def __init__(self, dem_raster):
        """
        Args:
            dem_raster: (H, W) elevation in meters
        """
        self.dem = dem_raster.astype(float)
    
    def calculate_slope(self, method='degrees'):
        """
        Calculate slope from DEM
        
        Args:
            method: 'degrees' or 'percent'
        
        Returns:
            slope: (H, W) array
        """
        
        # Compute gradients using Sobel filter
        sx = sobel(self.dem, axis=0)  # x-gradient
        sy = sobel(self.dem, axis=1)  # y-gradient
        
        # Slope in radians
        slope_rad = np.arctan(np.sqrt(sx**2 + sy**2))
        
        if method == 'degrees':
            return np.degrees(slope_rad)
        else:  # percent
            return np.tan(slope_rad) * 100
    
    def calculate_aspect(self):
        """
        Calculate aspect (direction of slope) in degrees
        
        Returns:
            aspect: (H, W) array [0-360]
        """
        
        sx = sobel(self.dem, axis=0)
        sy = sobel(self.dem, axis=1)
        
        aspect = np.degrees(np.arctan2(sy, sx))
        aspect[aspect < 0] += 360
        
        return aspect
    
    def calculate_roughness(self, window_size=3):
        """Calculate surface roughness"""
        
        roughness = np.zeros_like(self.dem)
        
        for i in range(window_size, self.dem.shape[0] - window_size):
            for j in range(window_size, self.dem.shape[1] - window_size):
                window = self.dem[
                    i-window_size:i+window_size+1,
                    j-window_size:j+window_size+1
                ]
                roughness[i, j] = np.std(window)
        
        return roughness
    
    def calculate_topographic_wetness_index(self):
        """Calculate TWI for moisture analysis"""
        
        # Flow accumulation (simplified)
        flow_acc = self._compute_flow_accumulation()
        slope = self.calculate_slope(method='degrees')
        
        # Avoid division by zero
        slope[slope < 0.1] = 0.1
        
        twi = np.log((flow_acc + 1) / (slope + 1e-8))
        
        return twi
    
    def calculate_terrain_position_index(self, window_size=5):
        """
        Calculate TPI (Terrain Position Index)
        TPI = Elevation - Mean elevation of surrounding pixels
        """
        
        mean_elevation = gaussian_filter(self.dem, sigma=window_size)
        tpi = self.dem - mean_elevation
        
        return tpi
    
    def _compute_flow_accumulation(self):
        """Compute D8 flow accumulation"""
        
        # Simplified: distance to nearest water body
        # In production, use proper flow direction algorithm
        
        flow_acc = np.zeros_like(self.dem)
        h, w = self.dem.shape
        
        for i in range(1, h-1):
            for j in range(1, w-1):
                neighbors = self.dem[i-1:i+2, j-1:j+2].flatten()
                flow_acc[i, j] = np.sum(neighbors < self.dem[i, j])
        
        return flow_acc
```

### 2.2 Solar Irradiance Calculation

```python
import numpy as np
from datetime import datetime, timedelta

class SolarIrradianceCalculator:
    """Calculate solar irradiance from DEM and climate data"""
    
    def __init__(self, dem, latitude, longitude, altitude):
        """
        Args:
            dem: Digital Elevation Model
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            altitude: Reference altitude in meters
        """
        self.dem = dem
        self.lat = np.radians(latitude)
        self.lon = np.radians(longitude)
        self.altitude = altitude
    
    def calculate_annual_ghi(self, clearness_index=0.65):
        """
        Calculate Annual Global Horizontal Irradiance (GHI)
        
        Args:
            clearness_index: Atmospheric clarity (0.6-0.75 for India)
        
        Returns:
            ghi: (H, W) annual irradiance in kWh/m²/year
        """
        
        # Use Liu-Jordan model for GHI calculation
        # Simplified: use latitude-based estimation
        
        solar_constant = 1361  # W/m²
        
        # Declination angle throughout year
        days = np.arange(1, 366)
        declination = 23.45 * np.sin(2 * np.pi * (days - 81) / 365)
        
        hourly_ghi = np.zeros(shape=(len(days), self.dem.shape[0], self.dem.shape[1]))
        
        for day_idx, day in enumerate(days):
            # Hour angle
            for hour in range(24):
                hour_angle = 15 * (hour - 12)  # degrees
                
                # Solar elevation
                sin_elevation = (
                    np.sin(self.lat) * np.sin(np.radians(declination[day_idx])) +
                    np.cos(self.lat) * np.cos(np.radians(declination[day_idx])) *
                    np.cos(np.radians(hour_angle))
                )
                
                # Only daytime hours
                if sin_elevation > 0:
                    air_mass = 1 / sin_elevation
                    # Clear sky GHI
                    ghi_clear = solar_constant * sin_elevation * \
                               np.exp(-0.75 * air_mass ** 0.678)
                    # Account for clearness
                    ghi = ghi_clear * clearness_index
                    hourly_ghi[day_idx] += ghi / 1000  # Convert to kW/m²
        
        # Annual sum (accounting for elevation and terrain)
        annual_ghi = np.sum(hourly_ghi, axis=0)
        
        # Elevation correction
        elevation_factor = 1 + (0.0001 * (self.dem - self.altitude))
        annual_ghi *= elevation_factor
        
        return annual_ghi
    
    def calculate_solar_angles(self, latitude, declination, hour_angle):
        """Calculate solar elevation and azimuth"""
        
        sin_elevation = (
            np.sin(np.radians(latitude)) * np.sin(np.radians(declination)) +
            np.cos(np.radians(latitude)) * np.cos(np.radians(declination)) *
            np.cos(np.radians(hour_angle))
        )
        
        elevation = np.degrees(np.arcsin(np.clip(sin_elevation, -1, 1)))
        
        cos_azimuth = (
            (np.sin(np.radians(declination)) * np.cos(np.radians(latitude)) -
             np.cos(np.radians(declination)) * np.sin(np.radians(latitude)) *
             np.cos(np.radians(hour_angle))) / np.cos(np.radians(elevation))
        )
        
        azimuth = np.degrees(np.arccos(np.clip(cos_azimuth, -1, 1)))
        
        return elevation, azimuth
```

### 2.3 Wind Speed Estimation

```python
class WindSpeedCalculator:
    """Calculate wind speed from roughness and elevation"""
    
    @staticmethod
    def estimate_wind_speed_at_hub_height(
        reference_speed, 
        reference_height, 
        hub_height,
        roughness_length,
        stability_class='D'
    ):
        """
        Log wind profile for wind speed extrapolation
        
        Args:
            reference_speed: Wind speed at reference height (m/s)
            reference_height: Reference height (m), typically 10m
            hub_height: Turbine hub height (m)
            roughness_length: Surface roughness (m)
            stability_class: Pasquill stability class
        
        Returns:
            wind_speed: Estimated wind speed at hub height
        """
        
        # Log profile
        wind_speed = reference_speed * (
            np.log(hub_height / roughness_length) /
            np.log(reference_height / roughness_length)
        )
        
        return wind_speed
    
    @staticmethod
    def terrain_roughness_classification(land_cover):
        """
        Get roughness length for different land cover types
        
        Returns dict of land cover -> roughness_length (m)
        """
        
        roughness_map = {
            'water': 0.0002,
            'barren': 0.01,
            'grassland': 0.05,
            'shrubland': 0.10,
            'agricultural': 0.15,
            'forest': 0.5,
            'urban': 1.0
        }
        
        return roughness_map
```

---

## 3. Geospatial Vector Operations

### 3.1 Buffer and Overlay Operations

```python
import geopandas as gpd
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
import pandas as pd

class VectorOperations:
    """Vector-based geospatial operations"""
    
    @staticmethod
    def create_conflict_buffers(gdf, buffer_distances):
        """
        Create buffer zones around geographical features
        
        Args:
            gdf: GeoDataFrame with geometries
            buffer_distances: Dict {feature_type: buffer_m}
        
        Returns:
            buffered_gdf: GeoDataFrame with buffer zones
        """
        
        buffered = gdf.copy()
        
        for idx, row in gdf.iterrows():
            feature_type = row.get('type', 'unknown')
            buffer_dist = buffer_distances.get(feature_type, 0)
            
            # Convert buffer distance to degrees (approximate)
            buffer_deg = buffer_dist / 111000  # 1 degree ≈ 111 km
            buffered.loc[idx, 'geometry'] = row['geometry'].buffer(buffer_deg)
        
        return buffered
    
    @staticmethod
    def spatial_join_with_aggregation(candidate_sites, conflict_zones):
        """
        Identify which candidate sites fall in conflict zones
        
        Returns:
            sites_with_conflicts: GeoDataFrame with conflict flags
        """
        
        # Spatial join
        sites_with_conflicts = gpd.sjoin(
            candidate_sites,
            conflict_zones,
            how='left',
            predicate='intersects'
        )
        
        # Aggregate conflicts by site
        conflict_summary = sites_with_conflicts.groupby('site_id').agg({
            'conflict_type': lambda x: list(x.dropna().unique()),
            'geometry': 'first'
        }).reset_index()
        
        conflict_summary['has_conflict'] = conflict_summary['conflict_type'].apply(len) > 0
        
        return conflict_summary
    
    @staticmethod
    def nearest_feature_distance(sites, features):
        """Calculate distance to nearest feature"""
        
        sites_copy = sites.copy()
        distances = []
        
        for site_geom in sites_copy.geometry:
            min_dist = min([
                site_geom.distance(feat_geom) * 111000  # Convert to meters
                for feat_geom in features.geometry
            ])
            distances.append(min_dist)
        
        sites_copy['distance_to_feature_m'] = distances
        
        return sites_copy
    
    @staticmethod
    def rasterize_vector(gdf, pixel_size, bounds):
        """Convert vector data to raster"""
        
        from rasterio.features import rasterize
        
        # Create shapes from geometries
        shapes = [(geom, 1) for geom in gdf.geometry]
        
        # Calculate raster dimensions
        minx, miny, maxx, maxy = bounds
        width = int((maxx - minx) / pixel_size)
        height = int((maxy - miny) / pixel_size)
        
        # Rasterize
        raster = rasterize(
            shapes,
            out_shape=(height, width),
            transform=rasterio.transform.from_bounds(
                minx, miny, maxx, maxy, width, height
            )
        )
        
        return raster
    
    @staticmethod
    def distance_raster(points_gdf, bounds, pixel_size):
        """Create distance raster from points"""
        
        from scipy.ndimage import distance_transform_edt
        
        # Create raster of points
        points_raster = VectorOperations.rasterize_vector(
            points_gdf, pixel_size, bounds
        )
        
        # Distance transform
        distance_raster = distance_transform_edt(1 - points_raster)
        distance_raster *= pixel_size  # Convert to real distance units
        
        return distance_raster
```

### 3.2 Fragmentation Analysis

```python
class FragmentationAnalyzer:
    """Analyze land fragmentation patterns"""
    
    @staticmethod
    def identify_land_parcels(suitability_raster, threshold=50):
        """
        Identify contiguous patches of suitable land
        
        Returns:
            patches: List of patch objects with properties
        """
        
        from scipy.ndimage import label, find_objects
        
        # Identify suitable pixels
        suitable = suitability_raster > threshold
        
        # Label connected components
        labeled, num_features = label(suitable)
        
        patches = []
        for i in range(1, num_features + 1):
            patch_mask = labeled == i
            patch_size = np.sum(patch_mask)
            
            # Only consider patches > 10 hectares (100 pixels at 30m resolution)
            if patch_size > 100:
                # Calculate centroid
                coords = np.where(patch_mask)
                centroid_y, centroid_x = np.mean(coords, axis=1)
                
                # Calculate shape metrics
                perimeter = np.sum(np.gradient(patch_mask.astype(float)) != 0)
                compactness = 4 * np.pi * patch_size / (perimeter ** 2 + 1e-8)
                
                patches.append({
                    'id': i,
                    'size_hectares': patch_size * 0.09,  # 30m pixels
                    'centroid': (centroid_y, centroid_x),
                    'perimeter_pixels': perimeter,
                    'compactness': compactness,
                    'mean_suitability': np.mean(
                        suitability_raster[patch_mask]
                    )
                })
        
        return patches
    
    @staticmethod
    def merge_nearby_patches(patches, merge_distance=1000):
        """Merge patches within merge_distance"""
        
        from scipy.spatial.distance import pdist, squareform
        
        # Calculate distances between patch centroids
        centroids = np.array([p['centroid'] for p in patches])
        distances = squareform(pdist(centroids))
        
        # Identify clusters
        from scipy.cluster.hierarchy import linkage, fcluster
        
        linkage_matrix = linkage(distances, method='average')
        clusters = fcluster(
            linkage_matrix,
            merge_distance / 30,  # Convert to pixels
            criterion='distance'
        )
        
        # Merge patches in same cluster
        merged_patches = []
        for cluster_id in np.unique(clusters):
            cluster_patches = [
                patches[i] for i, c in enumerate(clusters)
                if c == cluster_id
            ]
            
            # Combine metrics
            total_area = sum(p['size_hectares'] for p in cluster_patches)
            mean_suitability = np.mean([
                p['mean_suitability'] for p in cluster_patches
            ])
            
            merged_patches.append({
                'size_hectares': total_area,
                'num_patches': len(cluster_patches),
                'mean_suitability': mean_suitability,
                'component_ids': [p['id'] for p in cluster_patches]
            })
        
        return merged_patches
```

---

## 4. Time Series Analysis

### 4.1 Seasonal Analysis

```python
class SeasonalAnalysis:
    """Analyze seasonal patterns in satellite data"""
    
    @staticmethod
    def time_series_ndvi(sentinel2_images, dates):
        """
        Calculate NDVI time series
        
        Args:
            sentinel2_images: List of (H, W, 13) arrays
            dates: List of datetime objects
        
        Returns:
            ndvi_timeseries: (T, H, W) time series
        """
        
        ndvi_series = np.zeros((len(sentinel2_images), *sentinel2_images[0].shape[:2]))
        
        for t, img in enumerate(sentinel2_images):
            red = img[:, :, 2].astype(float)
            nir = img[:, :, 6].astype(float)
            ndvi_series[t] = (nir - red) / (nir + red + 1e-8)
        
        return ndvi_series, dates
    
    @staticmethod
    def crop_calendar_detection(ndvi_timeseries, dates):
        """
        Detect crop growth stages from NDVI
        
        Returns:
            crop_calendar: Dict of season -> (start_date, end_date, NDVI_change)
        """
        
        # Smooth time series
        from scipy.ndimage import gaussian_filter1d
        smoothed = gaussian_filter1d(
            ndvi_timeseries,
            sigma=3,
            axis=0
        )
        
        # Identify peaks (harvest) and valleys (planting)
        crop_calendar = []
        
        for h in range(smoothed.shape[1]):
            for w in range(smoothed.shape[2]):
                pixel_series = smoothed[:, h, w]
                
                # Find local minima and maxima
                from scipy.signal import argrelextrema
                
                minima = argrelextrema(pixel_series, np.less, order=5)[0]
                maxima = argrelextrema(pixel_series, np.greater, order=5)[0]
                
                # Create crop calendar events
                for i in range(len(minima) - 1):
                    plant_date = dates[minima[i]]
                    harvest_date = dates[maxima[i]] if i < len(maxima) else None
                    
                    if harvest_date:
                        crop_calendar.append({
                            'pixel': (h, w),
                            'plant_date': plant_date,
                            'harvest_date': harvest_date,
                            'growth_ndvi': pixel_series[maxima[i]] - pixel_series[minima[i]]
                        })
        
        return crop_calendar
```

---

## 5. Data Quality & Validation

### 5.1 Cloud Masking

```python
class CloudMasking:
    """Remove clouds and shadows from satellite imagery"""
    
    @staticmethod
    def sentinel2_cloud_mask(sentinel2_image):
        """
        Use Sentinel-2 scene classification to mask clouds
        
        Cloud probability classifier approach:
        - Clouds: SCL = 8, 9, 10, 11
        - Shadows: SCL = 3
        - Valid data: SCL = 4, 5, 6
        """
        
        scl_band = sentinel2_image[:, :, 9]  # Scene Classification Layer
        
        # Mask definition
        cloud_shadow_mask = np.isin(scl_band, [3, 8, 9, 10, 11])
        valid_pixels = ~cloud_shadow_mask
        
        return valid_pixels
    
    @staticmethod
    def sentinel1_speckle_filter(sar_image, window_size=5):
        """Apply Lee speckle filter to SAR data"""
        
        from scipy.ndimage import uniform_filter, uniform_filter1d
        from scipy.ndimage import minimum_filter, maximum_filter
        
        vv = sar_image[:, :, 0]
        vh = sar_image[:, :, 1]
        
        filtered = np.zeros_like(sar_image)
        
        for band_idx, band in [vv, vh]:
            # Lee filter
            mean = uniform_filter(band, window_size)
            variance = uniform_filter(band**2, window_size) - mean**2
            
            variance[variance == 0] = 1e-8  # Avoid division by zero
            ci = np.sqrt(variance) / (mean + 1e-8)
            
            w = 1 - ci / (1 + ci)
            filtered[:, :, band_idx] = mean + w * (band - mean)
        
        return filtered
```

---

## 6. Accuracy Assessment

### 6.1 Validation Metrics

```python
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, jaccard_score
import matplotlib.pyplot as plt

class AccuracyAssessment:
    """Assess accuracy of classifications"""
    
    @staticmethod
    def compare_with_ground_truth(predicted, ground_truth):
        """
        Compare predictions with ground truth
        
        Returns:
            metrics: Overall accuracy, producer's accuracy, user's accuracy
        """
        
        # Flatten arrays
        pred_flat = predicted.flatten()
        truth_flat = ground_truth.flatten()
        
        # Confusion matrix
        cm = confusion_matrix(truth_flat, pred_flat)
        
        # Overall accuracy
        oa = accuracy_score(truth_flat, pred_flat)
        
        # Producer's accuracy (recall)
        pa = np.diag(cm) / cm.sum(axis=1)
        
        # User's accuracy (precision)
        ua = np.diag(cm) / cm.sum(axis=0)
        
        # F1 score
        f1 = f1_score(truth_flat, pred_flat, average='weighted')
        
        # Kappa coefficient
        po = np.trace(cm) / cm.sum()
        pe = np.sum(np.outer(cm.sum(axis=0), cm.sum(axis=1))) / (cm.sum() ** 2)
        kappa = (po - pe) / (1 - pe)
        
        return {
            'overall_accuracy': oa,
            'producers_accuracy': pa,
            'users_accuracy': ua,
            'f1_score': f1,
            'kappa': kappa,
            'confusion_matrix': cm
        }
    
    @staticmethod
    def plot_confusion_matrix(cm, class_names):
        """Visualize confusion matrix"""
        
        plt.figure(figsize=(10, 8))
        plt.imshow(cm, interpolation='nearest', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.colorbar()
        
        tick_marks = np.arange(len(class_names))
        plt.xticks(tick_marks, class_names, rotation=45)
        plt.yticks(tick_marks, class_names)
        
        # Add values
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, str(cm[i, j]), ha='center', va='center')
        
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.tight_layout()
        plt.show()
```

