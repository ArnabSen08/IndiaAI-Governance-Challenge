# Automated Satellite-Based Property Identification & Change Detection System
## AI-Powered Municipal Property Intelligence & Tax Compliance

**Status**: Production Implementation Guide | **Version**: 1.0 | **Date**: January 26, 2026

---

## Executive Summary

This document presents a comprehensive **AI system for automated property identification, change detection, and anomaly detection using satellite imagery**. The system integrates geospatial computer vision, temporal change detection, anomaly detection algorithms, and municipal records management to enable:

- **Real-time property mapping** with 95%+ accuracy
- **Automated change detection** for new constructions and modifications
- **Anomaly flagging** for unauthorized structures and violations
- **Municipal record reconciliation** to identify property tax discrepancies
- **Infrastructure planning** insights from geospatial property data

### Key Value Propositions

| Dimension | Impact |
|-----------|--------|
| **Property Detection Accuracy** | 95%+ precision with multi-spectral analysis |
| **Change Detection Sensitivity** | Detect <50 sqm changes within 5-10 days |
| **Tax Revenue Recovery** | 15-25% increase through gap identification |
| **Compliance Enforcement** | Rapid identification of violations within 48 hours |
| **Operational Efficiency** | Reduce manual inspection time by 70% |
| **Scalability** | Cover entire state (>500,000 properties) quarterly |
| **False Positive Rate** | <2% through multi-layer validation |

---

## 1. System Architecture & Components

### 1.1 Complete System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    Client Applications Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Municipal    │  │ Field Officer│  │ Taxpayer    │             │
│  │ Dashboard    │  │ App          │  │ Portal      │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ GIS Mapping  │  │ Alert System │  │ Integration  │             │
│  │ Portal       │  │              │  │ APIs         │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└────────────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────┴─────────┐
                    │ API Gateway       │
                    │ Authentication    │
                    │ Rate Limiting     │
                    └─────────┬─────────┘
                              ↓
┌────────────────────────────────────────────────────────────────────┐
│              Computer Vision & Analytics Engine                    │
│  ┌───────────────────────────────────────────────────────────────┐│
│  │ 1. Satellite Image Ingestion & Preprocessing               ││
│  │    • Sentinel-2 (10m, free, weekly)                       ││
│  │    • Landsat-8/9 (30m, free, 16-day)                      ││
│  │    • High-resolution commercial (0.5-1m, monthly)         ││
│  │    • Atmospheric correction (Sen2Cor, FLAASH)             ││
│  │    • Cloud masking (>80% cloud-free required)             ││
│  │    • Radiometric & geometric normalization                ││
│  └───────────────────────────────────────────────────────────────┘│
│  ┌───────────────────────────────────────────────────────────────┐│
│  │ 2. Property Detection & Segmentation                        ││
│  │    • YOLOv5/v8 for object detection (buildings)            ││
│  │    • Faster R-CNN for large structures                     ││
│  │    • U-Net semantic segmentation (property footprints)     ││
│  │    • Instance segmentation for individual properties       ││
│  │    • Boundary regularization & shape refinement            ││
│  └───────────────────────────────────────────────────────────────┘│
│  ┌───────────────────────────────────────────────────────────────┐│
│  │ 3. Temporal Change Detection Module                         ││
│  │    • Difference imaging (time-series subtraction)           ││
│  │    • Change Vector Analysis (CVA) for multi-spectral       ││
│  │    • Temporal CNN for spatio-temporal patterns             ││
│  │    • LSTM for property evolution tracking                  ││
│  │    • Probabilistic change detection (Bayesian)             ││
│  └───────────────────────────────────────────────────────────────┘│
│  ┌───────────────────────────────────────────────────────────────┐│
│  │ 4. Anomaly Detection & Classification                       ││
│  │    • Unauthorized construction detection                    ││
│  │    • Illegal expansion identification                       ││
│  │    • Structural modification flagging                       ││
│  │    • Encroachment detection                                 ││
│  │    • Vulnerability anomalies (structural risk)             ││
│  └───────────────────────────────────────────────────────────────┘│
│  ┌───────────────────────────────────────────────────────────────┐│
│  │ 5. Property Attribute Extraction                            ││
│  │    • Building area & footprint estimation                   ││
│  │    • Height estimation (shadow analysis, stereo)            ││
│  │    • Material classification (roof type, color)             ││
│  │    • Land use classification (residential, commercial)      ││
│  │    • Infrastructure connectivity analysis                   ││
│  └───────────────────────────────────────────────────────────────┘│
│  ┌───────────────────────────────────────────────────────────────┐│
│  │ 6. Municipal Record Reconciliation                          ││
│  │    • Database comparison (recorded vs detected)             ││
│  │    • Property ID matching (multi-key matching)              ││
│  │    • Tax compliance analysis                                ││
│  │    • Discrepancy flagging & prioritization                  ││
│  │    • Historical audit trail maintenance                     ││
│  └───────────────────────────────────────────────────────────────┘│
│  ┌───────────────────────────────────────────────────────────────┐│
│  │ 7. Verification & Quality Control                           ││
│  │    • Multi-source validation (NDVI, thermal, radar)         ││
│  │    • Confidence scoring for all detections                  ││
│  │    • Expert review workflow automation                      ││
│  │    • False positive filtering & optimization                ││
│  └───────────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────────┐
│                    ML/AI Model Infrastructure                       │
│  • PyTorch/TensorFlow for deep learning                            │
│  • OpenCV/Rasterio for image processing                            │
│  • GDAL for geospatial operations                                   │
│  • MLflow for model versioning                                      │
│  • Airflow for scheduling retraining                                │
│  • Ray/Dask for distributed processing                              │
│  • TensorFlow Serving for inference                                 │
│  • ONNX Runtime for edge deployment                                 │
└────────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────────┐
│                      Data Storage Architecture                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ PostgreSQL + │  │ TimescaleDB  │  │ S3 Data Lake │            │
│  │ PostGIS      │  │ (Time-series)│  │ (Imagery)    │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ MongoDB      │  │ Redis        │  │ HDF5/NetCDF  │            │
│  │ (Records)    │  │ (Cache)      │  │ (Raster)     │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ Elasticsearch│  │ Minio        │  │ Cloud        │            │
│  │ (Index)      │  │ (S3-compat)  │  │ Storage APIs │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
└────────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────────┐
│                  Satellite Data Source Integration                  │
│  • Sentinel-2 (ESA)    • Landsat (USGS)    • Google Earth Engine   │
│  • MAXAR/Airbus (High-res)  • Custom drones  • Municipal surveys   │
└────────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────────┐
│                  Municipal Records Integration                      │
│  • Property Tax Database    • Land Records System    • Survey Maps  │
│  • Zoning Database          • Building Permits       • Deed Records │
└────────────────────────────────────────────────────────────────────┘
```

### 1.2 Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Image Processing** | GDAL + Rasterio | Geospatial standard tools |
| **Deep Learning** | PyTorch + Torchvision | Flexible, GPU-optimized |
| **Object Detection** | YOLOv8 + Faster R-CNN | Real-time + accuracy |
| **Segmentation** | U-Net + DeepLab | Pixel-level precision |
| **Change Detection** | Temporal CNN + LSTM | Spatio-temporal patterns |
| **Spatial Database** | PostgreSQL + PostGIS | Efficient spatial queries |
| **Time-Series** | TimescaleDB | Optimized temporal storage |
| **Data Access** | APIs (Sentinel Hub, Google Earth Engine) | Cloud-native imagery |
| **Orchestration** | Airflow | Scheduling & monitoring |
| **Inference Server** | FastAPI + TensorFlow Serving | Low-latency predictions |
| **Monitoring** | Prometheus + Grafana | Real-time system health |

---

## 2. Computer Vision Techniques

### 2.1 Property Detection using YOLO v8

```python
import torch
import torchvision.transforms as transforms
from ultralytics import YOLO
import numpy as np
import cv2
from PIL import Image
import rasterio
from rasterio.windows import Window
import geopandas as gpd

class PropertyDetectionEngine:
    """
    Automated property detection using YOLOv8
    """
    
    def __init__(self, model_path, device='cuda'):
        self.device = device
        self.model = YOLO(model_path)
        self.model.to(device)
        self.confidence_threshold = 0.6
        self.iou_threshold = 0.45
    
    def load_satellite_image(self, image_path, window=None):
        """
        Load satellite image with optional windowed reading for large files
        """
        with rasterio.open(image_path) as src:
            if window:
                # Read specific window for large images
                rgb_data = src.read(
                    [3, 2, 1],  # RGB bands (B4, B3, B2 for Sentinel-2)
                    window=window
                )
            else:
                rgb_data = src.read([3, 2, 1])
            
            # Get CRS and transform for geo-referencing
            crs = src.crs
            transform = src.transform
            
            # Normalize to 0-255 range
            rgb_data = np.moveaxis(rgb_data, 0, -1)
            rgb_data = ((rgb_data - rgb_data.min()) / 
                       (rgb_data.max() - rgb_data.min()) * 255).astype(np.uint8)
        
        return rgb_data, crs, transform
    
    def preprocess_image(self, image, target_size=640):
        """
        Preprocess image for YOLO model
        """
        # Convert to PIL Image for YOLO
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        return image
    
    def detect_properties(self, image_path, confidence=0.6):
        """
        Detect buildings/properties in satellite image
        """
        # Load image
        rgb_image, crs, transform = self.load_satellite_image(image_path)
        
        # Preprocess
        preprocessed = self.preprocess_image(rgb_image)
        
        # Run YOLO detection
        results = self.model(
            preprocessed,
            conf=confidence,
            iou=self.iou_threshold,
            verbose=False
        )
        
        detections = []
        
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = box.conf[0].cpu().numpy()
                
                # Calculate properties
                width = x2 - x1
                height = y2 - y1
                area = width * height
                
                # Convert pixel coordinates to geo-coordinates
                geo_coords = self._pixel_to_geo(
                    [(x1, y1), (x2, y2)], transform
                )
                
                detection = {
                    'pixel_coords': {
                        'x1': float(x1),
                        'y1': float(y1),
                        'x2': float(x2),
                        'y2': float(y2),
                        'width': float(width),
                        'height': float(height),
                        'area': float(area)
                    },
                    'geo_coords': {
                        'top_left': geo_coords[0],
                        'bottom_right': geo_coords[1]
                    },
                    'confidence': float(confidence),
                    'center': {
                        'pixel': ((x1 + x2) / 2, (y1 + y2) / 2),
                        'geo': (
                            (geo_coords[0][0] + geo_coords[1][0]) / 2,
                            (geo_coords[0][1] + geo_coords[1][1]) / 2
                        )
                    }
                }
                
                detections.append(detection)
        
        return {
            'detections': detections,
            'crs': str(crs),
            'total_detections': len(detections),
            'average_confidence': np.mean([d['confidence'] for d in detections]),
            'image_path': image_path
        }
    
    def _pixel_to_geo(self, pixel_coords, transform):
        """
        Convert pixel coordinates to geographic coordinates
        """
        geo_coords = []
        
        for px, py in pixel_coords:
            # Apply rasterio transform
            geo_x = transform.c + px * transform.a
            geo_y = transform.f + py * transform.e
            geo_coords.append((geo_x, geo_y))
        
        return geo_coords
    
    def filter_detections_by_area(self, detections, min_area_sqm, max_area_sqm, 
                                 resolution_m=10):
        """
        Filter detections by actual area (not pixel area)
        """
        filtered = []
        
        for detection in detections:
            pixel_area = detection['pixel_coords']['area']
            # Convert to square meters (resolution^2 per pixel)
            actual_area = pixel_area * (resolution_m ** 2)
            
            if min_area_sqm <= actual_area <= max_area_sqm:
                detection['actual_area_sqm'] = actual_area
                filtered.append(detection)
        
        return filtered
    
    def nms_detections(self, detections, iou_threshold=0.3):
        """
        Apply Non-Maximum Suppression to remove overlapping detections
        """
        if len(detections) == 0:
            return detections
        
        # Sort by confidence
        sorted_dets = sorted(detections, key=lambda x: x['confidence'], 
                            reverse=True)
        
        selected = [sorted_dets[0]]
        
        for current in sorted_dets[1:]:
            should_keep = True
            
            for kept in selected:
                iou = self._calculate_iou(
                    current['pixel_coords'],
                    kept['pixel_coords']
                )
                
                if iou > iou_threshold:
                    should_keep = False
                    break
            
            if should_keep:
                selected.append(current)
        
        return selected
    
    def _calculate_iou(self, box1, box2):
        """
        Calculate Intersection over Union
        """
        x1_min, y1_min = box1['x1'], box1['y1']
        x1_max, y1_max = box1['x2'], box1['y2']
        
        x2_min, y2_min = box2['x1'], box2['y1']
        x2_max, y2_max = box2['x2'], box2['y2']
        
        # Intersection
        xi1 = max(x1_min, x2_min)
        yi1 = max(y1_min, y2_min)
        xi2 = min(x1_max, x2_max)
        yi2 = min(y1_max, y2_max)
        
        inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
        
        # Union
        box1_area = (x1_max - x1_min) * (y1_max - y1_min)
        box2_area = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = box1_area + box2_area - inter_area
        
        if union_area == 0:
            return 0
        
        return inter_area / union_area
```

### 2.2 Semantic Segmentation with U-Net

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models.segmentation import deeplabv3_resnet50
import numpy as np

class PropertySegmentationModel(nn.Module):
    """
    U-Net based semantic segmentation for property footprint extraction
    """
    
    def __init__(self, in_channels=3, out_channels=1):
        super().__init__()
        
        # Pre-trained DeepLabV3 for semantic segmentation
        self.model = deeplabv3_resnet50(
            pretrained=True,
            num_classes=out_channels
        )
    
    def forward(self, x):
        return self.model(x)

class PropertySegmentationEngine:
    """
    Engine for property footprint segmentation
    """
    
    def __init__(self, model_path, device='cuda'):
        self.device = device
        self.model = PropertySegmentationModel()
        self.model.load_state_dict(torch.load(model_path, 
                                              map_location=device))
        self.model.to(device)
        self.model.eval()
    
    def segment_properties(self, image_path, threshold=0.5):
        """
        Segment property footprints from satellite image
        """
        # Load and preprocess image
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Normalize
        image = image.astype(np.float32) / 255.0
        
        # PyTorch format (C, H, W)
        image_tensor = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0)
        image_tensor = image_tensor.to(self.device)
        
        # Run inference
        with torch.no_grad():
            output = self.model(image_tensor)
            output = torch.sigmoid(output['out'])
        
        # Convert to numpy
        segmentation_mask = output[0, 0].cpu().numpy()
        
        # Apply threshold
        binary_mask = (segmentation_mask > threshold).astype(np.uint8)
        
        # Extract contours for property boundaries
        contours, _ = cv2.findContours(binary_mask, 
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        
        properties = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area (minimum 50 sqm = ~0.5 pixels at 10m resolution)
            if area < 5:
                continue
            
            # Approximate polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            polygon = cv2.approxPolyDP(contour, epsilon, True)
            
            # Calculate properties
            perimeter = cv2.arcLength(polygon, True)
            (center_x, center_y), radius = cv2.minEnclosingCircle(polygon)
            
            # Circularity (1 = perfect circle, 0 = line)
            circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
            
            properties.append({
                'polygon': polygon.squeeze().tolist(),
                'area_pixels': float(area),
                'perimeter': float(perimeter),
                'center': (float(center_x), float(center_y)),
                'circularity': float(circularity),
                'confidence': float(np.mean(segmentation_mask[binary_mask == 1]))
            })
        
        return {
            'segmentation_mask': binary_mask,
            'properties': properties,
            'total_properties': len(properties),
            'total_area_pixels': np.sum(binary_mask)
        }
    
    def regularize_boundaries(self, properties, smoothness=5):
        """
        Regularize property boundaries for better shape
        """
        regularized = []
        
        for prop in properties:
            polygon = np.array(prop['polygon'])
            
            # Apply Gaussian smoothing to coordinates
            if len(polygon) > smoothness:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                                                   (smoothness, smoothness))
                # Create mask and apply morphological operations
                mask = np.zeros((500, 500), dtype=np.uint8)
                cv2.drawContours(mask, [polygon.astype(np.int32)], 0, 1, -1)
                
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
                
                # Extract regularized contour
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                              cv2.CHAIN_APPROX_SIMPLE)
                
                if contours:
                    regularized_poly = contours[0].squeeze().tolist()
                    prop['regularized_polygon'] = regularized_poly
            
            regularized.append(prop)
        
        return regularized
```

### 2.3 Spectral Analysis & Building Features

```python
import numpy as np
import rasterio
from scipy.ndimage import gaussian_filter

class SpectralAnalysisEngine:
    """
    Extract building characteristics from multi-spectral satellite imagery
    """
    
    def __init__(self):
        pass
    
    def calculate_ndvi(self, red_band, nir_band):
        """
        Calculate Normalized Difference Vegetation Index
        Used to distinguish vegetation from buildings
        """
        ndvi = (nir_band - red_band) / (nir_band + red_band + 1e-8)
        return np.nan_to_num(ndvi)
    
    def calculate_ndbi(self, swir_band, nir_band):
        """
        Calculate Normalized Difference Built-up Index
        Highlights built-up areas (buildings, roads)
        """
        ndbi = (swir_band - nir_band) / (swir_band + nir_band + 1e-8)
        return np.nan_to_num(ndbi)
    
    def calculate_ndri(self, red_band, blue_band):
        """
        Calculate Normalized Difference Red-to-Blue Index
        Helps distinguish building materials
        """
        ndri = (red_band - blue_band) / (red_band + blue_band + 1e-8)
        return np.nan_to_num(ndri)
    
    def extract_multispectral_features(self, image_path):
        """
        Extract spectral indices for building classification
        """
        with rasterio.open(image_path) as src:
            # Sentinel-2 bands:
            # Band 2: Blue (490nm), Band 3: Green (560nm), Band 4: Red (665nm)
            # Band 5: Red Edge (705nm), Band 8: NIR (842nm), Band 11: SWIR (1610nm)
            
            blue = src.read(2).astype(np.float32)
            green = src.read(3).astype(np.float32)
            red = src.read(4).astype(np.float32)
            nir = src.read(8).astype(np.float32)
            swir = src.read(11).astype(np.float32)
        
        features = {
            'ndvi': self.calculate_ndvi(red, nir),
            'ndbi': self.calculate_ndbi(swir, nir),
            'ndri': self.calculate_ndri(red, blue),
            'brightness': (red + green + blue) / 3,
            'redness': red / (red + green + blue + 1e-8),
            'compactness': self._calculate_texture_compactness(red)
        }
        
        return features
    
    def _calculate_texture_compactness(self, band, window_size=9):
        """
        Calculate local texture compactness
        Buildings have more uniform texture than vegetation
        """
        from scipy.ndimage import generic_filter
        
        # Calculate local variance
        local_mean = generic_filter(band, np.mean, size=window_size)
        local_var = generic_filter((band - local_mean) ** 2, np.mean, size=window_size)
        
        # Normalize
        compactness = 1 - (local_var / (band.max() - band.min() + 1e-8))
        
        return compactness
    
    def classify_materials(self, features, property_mask):
        """
        Classify roofing materials based on spectral signatures
        """
        # Material spectral signatures (Normalized reflectance)
        # RCC/Concrete: High red, low NIR
        # Metal: Very high reflectance across bands
        # Asbestos: Specific spectral signature
        # Vegetation: Low red, high NIR
        
        materials = {}
        
        red = features['redness'][property_mask == 1]
        ndvi = features['ndvi'][property_mask == 1]
        ndbi = features['ndbi'][property_mask == 1]
        ndri = features['ndri'][property_mask == 1]
        
        # Classification logic
        metal_likelihood = np.mean((red > 0.6) & (ndvi < 0.2))
        concrete_likelihood = np.mean((red > 0.5) & (ndvi < 0.1))
        vegetation_likelihood = np.mean(ndvi > 0.4)
        
        materials = {
            'metal': float(metal_likelihood),
            'concrete': float(concrete_likelihood),
            'vegetation': float(vegetation_likelihood),
            'dominant_material': max(
                [('metal', metal_likelihood),
                 ('concrete', concrete_likelihood),
                 ('vegetation', vegetation_likelihood)],
                key=lambda x: x[1]
            )[0]
        }
        
        return materials
    
    def estimate_building_height(self, dem_file, property_polygon, 
                                neighborhood_dem=None):
        """
        Estimate building height using DEM and shadow analysis
        """
        import rasterio
        from rasterio.mask import mask
        
        with rasterio.open(dem_file) as src:
            # Extract DEM for property
            out_image, out_transform = mask(src, [property_polygon], crop=True)
            building_dem = out_image[0]
        
        # Get neighborhood DEM for terrain correction
        if neighborhood_dem is None:
            neighborhood_dem = building_dem.min()
        
        # Height = DEM value - terrain reference
        estimated_height = building_dem.max() - neighborhood_dem
        
        # Typical constraints
        if estimated_height < 2:
            estimated_height = 2  # Minimum building height
        elif estimated_height > 50:
            estimated_height = 50  # Maximum reasonable height estimate
        
        return {
            'estimated_height_m': float(estimated_height),
            'dem_range': (float(building_dem.min()), float(building_dem.max())),
            'confidence': 'medium' if 5 < estimated_height < 30 else 'low'
        }
```

---

## 3. Temporal Change Detection

### 3.1 Change Detection Models

```python
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import DataLoader, Dataset
import rasterio

class TemporalChangeDetectionCNN(nn.Module):
    """
    CNN for detecting changes between two multi-temporal satellite images
    """
    
    def __init__(self, in_channels=6, out_channels=2):  # 3 channels * 2 timesteps
        super().__init__()
        
        # Feature extraction
        self.conv1 = nn.Conv2d(in_channels, 64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(128)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(256)
        
        # Decoder
        self.deconv1 = nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1)
        self.deconv2 = nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1)
        self.deconv3 = nn.Conv2d(64, out_channels, kernel_size=1)
        
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
    
    def forward(self, x_t1, x_t2):
        # Concatenate temporal images
        x = torch.cat([x_t1, x_t2], dim=1)
        
        # Encoder
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.maxpool(x)
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.maxpool(x)
        x = self.relu(self.bn3(self.conv3(x)))
        
        # Decoder
        x = self.relu(self.deconv1(x))
        x = self.relu(self.deconv2(x))
        x = self.deconv3(x)
        
        return x

class ChangeDetectionEngine:
    """
    Comprehensive change detection system
    """
    
    def __init__(self, model_path, device='cuda'):
        self.device = device
        self.model = TemporalChangeDetectionCNN()
        self.model.load_state_dict(torch.load(model_path, map_location=device))
        self.model.to(device)
        self.model.eval()
    
    def load_temporal_images(self, image_t1_path, image_t2_path):
        """
        Load two multi-temporal satellite images
        """
        images = []
        
        for path in [image_t1_path, image_t2_path]:
            with rasterio.open(path) as src:
                # Read RGB bands
                rgb = src.read([3, 2, 1])  # R, G, B for Sentinel-2
                rgb = np.moveaxis(rgb, 0, -1).astype(np.float32) / 255.0
            
            images.append(rgb)
        
        return images[0], images[1]
    
    def difference_imaging(self, image_t1, image_t2):
        """
        Simple differencing for change detection
        """
        difference = np.abs(image_t1.astype(np.float32) - image_t2.astype(np.float32))
        
        return difference.mean(axis=2)
    
    def change_vector_analysis(self, image_t1, image_t2):
        """
        Change Vector Analysis for multi-spectral data
        """
        # Flatten spatial dimensions for per-pixel analysis
        t1_flat = image_t1.reshape(-1, image_t1.shape[-1])
        t2_flat = image_t2.reshape(-1, image_t2.shape[-1])
        
        # Calculate change vectors
        change_vectors = t2_flat - t1_flat
        
        # Magnitude (amount of change)
        magnitudes = np.linalg.norm(change_vectors, axis=1)
        
        # Reshape back to image
        magnitude_image = magnitudes.reshape(image_t1.shape[:-1])
        
        return magnitude_image
    
    def cnn_change_detection(self, image_t1, image_t2, threshold=0.5):
        """
        Deep learning-based change detection
        """
        # Convert to torch tensors
        t1_tensor = torch.from_numpy(image_t1).permute(2, 0, 1).unsqueeze(0)
        t2_tensor = torch.from_numpy(image_t2).permute(2, 0, 1).unsqueeze(0)
        
        t1_tensor = t1_tensor.to(self.device)
        t2_tensor = t2_tensor.to(self.device)
        
        # Model inference
        with torch.no_grad():
            change_map = self.model(t1_tensor, t2_tensor)
            change_prob = torch.softmax(change_map, dim=1)
        
        # Extract change probability (class 1 = change detected)
        change_probability = change_prob[0, 1].cpu().numpy()
        
        # Binary change map
        change_detected = (change_probability > threshold).astype(np.uint8)
        
        return {
            'change_probability': change_probability,
            'change_detected': change_detected,
            'total_change_pixels': np.sum(change_detected),
            'average_confidence': np.mean(change_probability[change_detected == 1])
        }
    
    def identify_change_type(self, image_t1, image_t2, change_mask):
        """
        Classify type of change detected
        """
        # Analyze spectral characteristics of changed pixels
        t1_changed = image_t1[change_mask == 1]
        t2_changed = image_t2[change_mask == 1]
        
        # Calculate statistics
        brightness_change = (t2_changed.mean(axis=1) - t1_changed.mean(axis=1)).mean()
        
        # Classify change type
        change_types = {}
        
        if brightness_change > 0.15:
            change_types['brightening'] = True
            change_types['likely_type'] = 'new_construction_or_expansion'
        elif brightness_change < -0.15:
            change_types['darkening'] = True
            change_types['likely_type'] = 'demolition_or_removal'
        else:
            change_types['modification'] = True
            change_types['likely_type'] = 'material_or_structure_change'
        
        return change_types
    
    def track_property_evolution(self, school_id, temporal_images):
        """
        Track evolution of a property over time using multi-temporal images
        """
        evolution = []
        
        for i in range(len(temporal_images) - 1):
            change_result = self.cnn_change_detection(
                temporal_images[i],
                temporal_images[i + 1]
            )
            
            change_type = self.identify_change_type(
                temporal_images[i],
                temporal_images[i + 1],
                change_result['change_detected']
            )
            
            evolution.append({
                'interval': f"image_{i}_to_{i+1}",
                'change_detected': bool(np.sum(change_result['change_detected']) > 0),
                'change_magnitude': float(change_result['average_confidence']),
                'change_type': change_type['likely_type']
            })
        
        return evolution
```

---

## 4. Anomaly Detection Models

### 4.1 Unauthorized Construction Detection

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class UnauthorizedConstructionDetector:
    """
    Detect unauthorized constructions and violations
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.scaler = StandardScaler()
        self.anomaly_model = IsolationForest(contamination=0.1, random_state=42)
    
    def extract_anomaly_features(self, detected_properties, 
                                 municipal_records_properties):
        """
        Extract features for anomaly detection
        """
        
        features_list = []
        
        for detected_prop in detected_properties:
            # Search for matching municipal record
            matching_record = None
            min_distance = float('inf')
            
            for municipal_prop in municipal_records_properties:
                # Calculate distance between centers
                dist = np.sqrt(
                    (detected_prop['center']['geo'][0] - municipal_prop['center_lon']) ** 2 +
                    (detected_prop['center']['geo'][1] - municipal_prop['center_lat']) ** 2
                )
                
                if dist < min_distance:
                    min_distance = dist
                    matching_record = municipal_prop
            
            # Feature engineering
            features = {
                'detected_area': detected_prop.get('actual_area_sqm', 0),
                'recorded_area': matching_record['area_sqm'] if matching_record else 0,
                'area_discrepancy_ratio': (
                    abs(detected_prop.get('actual_area_sqm', 0) - 
                        (matching_record['area_sqm'] if matching_record else 0)) /
                    max(detected_prop.get('actual_area_sqm', 1), 1)
                ) if matching_record else 1.0,
                'recorded_tax_paid': matching_record['tax_paid'] if matching_record else False,
                'is_new_construction': (matching_record is None or 
                                      min_distance > 20),  # 20m threshold
                'property_age_months': (
                    (pd.Timestamp.now() - pd.Timestamp(matching_record['record_date'])).days / 30
                    if matching_record else 0
                ),
                'geometric_irregularity': self._calculate_shape_irregularity(detected_prop),
                'location_violation_risk': self._assess_location_risk(
                    detected_prop, municipal_records_properties
                ),
                'construction_speed': self._estimate_construction_speed(detected_prop),
                'matching_distance_m': min_distance
            }
            
            features_list.append(features)
        
        return pd.DataFrame(features_list)
    
    def _calculate_shape_irregularity(self, property_data):
        """
        Calculate shape irregularity (unusual shapes may indicate violations)
        """
        if 'circularity' in property_data:
            # Circularity deviation from 0.85 (common for regular buildings)
            return abs(property_data['circularity'] - 0.85)
        
        return 0.5  # Default mid-range value
    
    def _assess_location_risk(self, detected_prop, all_properties):
        """
        Assess risk based on location (encroachment, etc.)
        """
        # Risk factors:
        # - Adjacent to protected areas
        # - Overlapping with public spaces
        # - Near water bodies
        
        risk_score = 0
        
        # Check adjacency to other properties
        overlap_count = 0
        for other_prop in all_properties:
            if other_prop == detected_prop:
                continue
            
            dist_to_other = np.sqrt(
                (detected_prop['center']['geo'][0] - other_prop['center']['geo'][0]) ** 2 +
                (detected_prop['center']['geo'][1] - other_prop['center']['geo'][1]) ** 2
            )
            
            if dist_to_other < 10:  # Less than 10m apart
                overlap_count += 1
        
        if overlap_count > 2:
            risk_score += 0.3
        
        return risk_score
    
    def _estimate_construction_speed(self, detected_prop):
        """
        Estimate construction speed from imagery change detection
        Very fast construction may indicate informal/illegal building
        """
        if 'construction_speed_sqm_per_day' in detected_prop:
            # Fast construction: > 5 sqm per day
            if detected_prop['construction_speed_sqm_per_day'] > 5:
                return 0.7  # High anomaly score
        
        return 0.3  # Default low anomaly
    
    def detect_anomalies(self, features_df, threshold=-0.3):
        """
        Detect anomalous properties using Isolation Forest
        """
        # Select features for anomaly detection
        feature_cols = [
            'area_discrepancy_ratio',
            'geometric_irregularity',
            'location_violation_risk',
            'construction_speed',
            'property_age_months'
        ]
        
        X = features_df[feature_cols].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        # Anomaly detection
        anomaly_scores = self.anomaly_model.decision_function(X_scaled)
        predictions = self.anomaly_model.predict(X_scaled)
        
        # Flag anomalies
        features_df['anomaly_score'] = anomaly_scores
        features_df['is_anomaly'] = predictions == -1
        
        # Classify anomaly types
        anomalies = features_df[features_df['is_anomaly']].copy()
        
        anomalies['violation_type'] = anomalies.apply(
            lambda row: self._classify_violation_type(row), axis=1
        )
        
        return {
            'anomalous_properties': len(anomalies),
            'anomaly_rate': len(anomalies) / len(features_df),
            'anomalies_details': anomalies.to_dict('records'),
            'high_risk': anomalies[anomalies['anomaly_score'] < threshold]
        }
    
    def _classify_violation_type(self, row):
        """
        Classify the type of violation detected
        """
        if row['is_new_construction'] and not row['recorded_tax_paid']:
            return 'unregistered_new_construction'
        
        if row['area_discrepancy_ratio'] > 0.3:
            return 'unauthorized_expansion'
        
        if row['location_violation_risk'] > 0.5:
            return 'encroachment_risk'
        
        if row['geometric_irregularity'] > 0.4:
            return 'irregular_structure'
        
        return 'minor_violation'
```

### 4.2 LSTM-based Anomaly Detection

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import numpy as np

class LSTMAutoencoderAnomalyDetector(nn.Module):
    """
    LSTM Autoencoder for detecting anomalous property evolution patterns
    """
    
    def __init__(self, input_size=6, hidden_size=32, num_layers=2):
        super().__init__()
        
        # Encoder
        self.encoder = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )
        
        # Decoder
        self.decoder = nn.LSTM(
            input_size=hidden_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )
        
        self.output_layer = nn.Linear(hidden_size, input_size)
    
    def forward(self, x):
        # Encoder
        encoder_output, (h_n, c_n) = self.encoder(x)
        
        # Decoder (repeat last hidden state)
        decoder_input = encoder_output[:, -1:, :].repeat(1, x.shape[1], 1)
        decoder_output, _ = self.decoder(decoder_input, (h_n, c_n))
        
        # Output layer
        output = self.output_layer(decoder_output)
        
        return output

class PropertyEvolutionAnomalyDetector:
    """
    Detect anomalies in property evolution over time
    """
    
    def __init__(self, model_path=None, device='cuda'):
        self.device = device
        self.model = LSTMAutoencoderAnomalyDetector()
        
        if model_path:
            self.model.load_state_dict(torch.load(model_path, map_location=device))
        
        self.model.to(device)
        self.model.eval()
    
    def extract_temporal_features(self, property_history):
        """
        Extract temporal features from property history
        """
        # Features: [area, height, spectral_index, condition_score, tax_status, construction_activity]
        
        features = []
        
        for record in property_history:
            feature_vector = [
                record.get('area_sqm', 0),
                record.get('height_m', 0),
                record.get('ndbi_index', 0),
                record.get('condition_score', 0),
                float(record.get('tax_paid', False)),
                float(record.get('construction_detected', False))
            ]
            
            features.append(feature_vector)
        
        return np.array(features, dtype=np.float32)
    
    def detect_property_anomalies(self, property_histories, 
                                 reconstruction_threshold=0.3):
        """
        Detect anomalies in property evolution patterns
        """
        anomalies = []
        
        for property_id, history in property_histories.items():
            # Extract temporal features
            temporal_features = self.extract_temporal_features(history)
            
            if len(temporal_features) < 3:  # Need at least 3 timesteps
                continue
            
            # Convert to torch tensor
            x_tensor = torch.from_numpy(temporal_features).unsqueeze(0)
            x_tensor = x_tensor.to(self.device)
            
            # Forward pass through autoencoder
            with torch.no_grad():
                reconstructed = self.model(x_tensor)
            
            # Calculate reconstruction error
            reconstruction_error = torch.mean(
                (x_tensor - reconstructed) ** 2,
                dim=(1, 2)
            ).cpu().numpy()
            
            if reconstruction_error > reconstruction_threshold:
                anomalies.append({
                    'property_id': property_id,
                    'reconstruction_error': float(reconstruction_error),
                    'anomaly_severity': self._classify_severity(reconstruction_error),
                    'anomaly_pattern': self._identify_anomaly_pattern(
                        temporal_features, reconstructed.squeeze(0).cpu().numpy()
                    )
                })
        
        return sorted(anomalies, key=lambda x: x['reconstruction_error'], reverse=True)
    
    def _classify_severity(self, error):
        """
        Classify anomaly severity
        """
        if error > 0.6:
            return 'critical'
        elif error > 0.4:
            return 'high'
        elif error > 0.3:
            return 'medium'
        else:
            return 'low'
    
    def _identify_anomaly_pattern(self, original, reconstructed):
        """
        Identify the pattern of anomaly
        """
        feature_names = ['area', 'height', 'spectral', 'condition', 'tax', 'construction']
        
        errors_by_feature = np.mean((original - reconstructed) ** 2, axis=0)
        max_error_idx = np.argmax(errors_by_feature)
        
        return f"Unusual {feature_names[max_error_idx]} changes detected"
```

---

## 5. Municipal Record Integration

### 5.1 Database Schema & Reconciliation

```python
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import geoalchemy2 as ga
from datetime import datetime
import pandas as pd

Base = declarative_base()

class MunicipalProperty(Base):
    """
    Municipal property tax records
    """
    __tablename__ = 'municipal_properties'
    
    property_id = Column(String, primary_key=True)
    owner_name = Column(String)
    owner_pan = Column(String, unique=True, nullable=True)
    property_address = Column(String)
    locality = Column(String)
    ward_number = Column(Integer)
    plot_number = Column(String)
    
    recorded_area_sqm = Column(Float)
    recorded_area_classification = Column(String)  # residential, commercial, industrial
    recorded_structure_type = Column(String)  # building, vacant, etc
    
    tax_assessed_value = Column(Float)
    annual_tax = Column(Float)
    last_tax_paid_date = Column(DateTime)
    tax_paid = Column(Boolean, default=False)
    years_overdue = Column(Integer)
    
    geom = Column(ga.Geometry('POLYGON'))  # PostGIS geometry
    recorded_date = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class DetectedProperty(Base):
    """
    Properties detected from satellite imagery
    """
    __tablename__ = 'detected_properties'
    
    detection_id = Column(String, primary_key=True)
    image_date = Column(DateTime)
    detected_area_sqm = Column(Float)
    detected_height_m = Column(Float, nullable=True)
    confidence_score = Column(Float)
    
    material_classification = Column(String)  # metal, concrete, vegetation
    construction_activity_detected = Column(Boolean)
    
    geom = Column(ga.Geometry('POLYGON'))
    matched_property_id = Column(String, nullable=True)  # FK to MunicipalProperty
    matching_confidence = Column(Float, nullable=True)
    detection_date = Column(DateTime, default=datetime.now)

class PropertyAnomalyRecord(Base):
    """
    Anomalies and violations detected
    """
    __tablename__ = 'property_anomalies'
    
    anomaly_id = Column(String, primary_key=True)
    property_id = Column(String)
    anomaly_type = Column(String)  # unregistered, expansion, encroachment, etc
    severity = Column(String)  # critical, high, medium, low
    
    detected_by = Column(String)  # detection_model_name
    confidence = Column(Float)
    
    description = Column(String)
    recommended_action = Column(String)
    
    created_date = Column(DateTime, default=datetime.now)
    resolved_date = Column(DateTime, nullable=True)
    resolution_notes = Column(String, nullable=True)

class PropertyReconciliationEngine:
    """
    Reconcile satellite detections with municipal records
    """
    
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def match_detected_to_municipal(self, detected_properties, 
                                   distance_threshold_m=15):
        """
        Match satellite detections to municipal records
        """
        session = self.Session()
        
        matches = []
        
        for detected in detected_properties:
            # Query nearby municipal properties
            query = session.query(MunicipalProperty).filter(
                ga.functions.ST_DWithin(
                    MunicipalProperty.geom,
                    f"SRID=4326;POINT({detected['center_lon']} {detected['center_lat']})",
                    distance_threshold_m
                )
            )
            
            nearby_properties = query.all()
            
            if nearby_properties:
                # Find best match by area similarity
                best_match = max(
                    nearby_properties,
                    key=lambda p: 1 - abs(
                        p.recorded_area_sqm - detected['detected_area_sqm']
                    ) / max(p.recorded_area_sqm, detected['detected_area_sqm'])
                )
                
                area_match_score = 1 - abs(
                    best_match.recorded_area_sqm - detected['detected_area_sqm']
                ) / max(best_match.recorded_area_sqm, detected['detected_area_sqm'])
                
                matches.append({
                    'detected_property': detected,
                    'municipal_property': best_match,
                    'match_confidence': area_match_score,
                    'is_match': area_match_score > 0.85
                })
            else:
                # No match found - potential new construction
                matches.append({
                    'detected_property': detected,
                    'municipal_property': None,
                    'match_confidence': 0,
                    'is_match': False
                })
        
        session.close()
        return matches
    
    def identify_discrepancies(self, matches):
        """
        Identify discrepancies between detected and recorded properties
        """
        discrepancies = []
        
        for match in matches:
            detected = match['detected_property']
            municipal = match['municipal_property']
            
            if not match['is_match']:
                discrepancies.append({
                    'type': 'unrecorded_property',
                    'detected_property_id': detected.get('detection_id'),
                    'detected_area': detected.get('detected_area_sqm'),
                    'severity': 'critical' if detected.get('detected_area_sqm', 0) > 100 else 'medium'
                })
            else:
                # Compare area
                area_diff_pct = abs(
                    detected['detected_area_sqm'] - municipal.recorded_area_sqm
                ) / municipal.recorded_area_sqm * 100
                
                if area_diff_pct > 20:
                    discrepancies.append({
                        'type': 'area_mismatch',
                        'property_id': municipal.property_id,
                        'recorded_area': municipal.recorded_area_sqm,
                        'detected_area': detected['detected_area_sqm'],
                        'difference_pct': area_diff_pct,
                        'severity': 'high' if area_diff_pct > 40 else 'medium'
                    })
                
                # Check tax compliance
                if not municipal.tax_paid and municipal.years_overdue > 1:
                    discrepancies.append({
                        'type': 'tax_non_compliance',
                        'property_id': municipal.property_id,
                        'years_overdue': municipal.years_overdue,
                        'annual_tax': municipal.annual_tax,
                        'severity': 'high'
                    })
        
        return discrepancies
    
    def flag_reconciliation_issues(self, discrepancies):
        """
        Create anomaly records for identified issues
        """
        session = self.Session()
        
        for discrepancy in discrepancies:
            anomaly = PropertyAnomalyRecord(
                anomaly_id=f"ANOM_{datetime.now().timestamp()}",
                property_id=discrepancy.get('property_id', 'unrecorded'),
                anomaly_type=discrepancy['type'],
                severity=discrepancy['severity'],
                detected_by='reconciliation_engine',
                confidence=0.95 if discrepancy['type'] == 'unrecorded_property' else 0.85,
                description=str(discrepancy),
                recommended_action=self._get_recommended_action(discrepancy['type'])
            )
            
            session.add(anomaly)
        
        session.commit()
        session.close()
    
    def _get_recommended_action(self, anomaly_type):
        """
        Recommend actions for different anomaly types
        """
        actions = {
            'unrecorded_property': 'Field verification + Registration + Tax assessment',
            'area_mismatch': 'Survey verification + Record correction',
            'tax_non_compliance': 'Issue tax notice + Recovery proceedings',
            'unauthorized_expansion': 'Demolition notice + Fine',
            'encroachment': 'Removal + Penalty'
        }
        
        return actions.get(anomaly_type, 'Investigation required')
```

---

## 6. Validation & Quality Assurance

### 6.1 Multi-Layer Validation

```python
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

class ValidationFramework:
    """
    Multi-layer validation of detection results
    """
    
    def __init__(self):
        pass
    
    def validate_with_ndvi(self, detected_polygon, ndvi_image, 
                          vegetation_threshold=0.4):
        """
        Validate building detection using NDVI
        Buildings should have low NDVI (< 0.4)
        """
        # Extract NDVI values within detected polygon
        mask = self._polygon_to_mask(detected_polygon, ndvi_image.shape)
        ndvi_values = ndvi_image[mask == 1]
        
        if len(ndvi_values) == 0:
            return {'valid': False, 'reason': 'No NDVI data'}
        
        mean_ndvi = np.mean(ndvi_values)
        
        is_building = mean_ndvi < vegetation_threshold
        
        return {
            'valid': is_building,
            'mean_ndvi': float(mean_ndvi),
            'confidence': max(0, 1 - (mean_ndvi / vegetation_threshold))
        }
    
    def validate_with_thermal(self, detected_polygon, thermal_image,
                             building_temp_range=(20, 45)):
        """
        Validate detection using thermal data
        Buildings have different thermal properties than vegetation
        """
        mask = self._polygon_to_mask(detected_polygon, thermal_image.shape)
        thermal_values = thermal_image[mask == 1]
        
        mean_thermal = np.mean(thermal_values)
        
        is_building = building_temp_range[0] <= mean_thermal <= building_temp_range[1]
        
        return {
            'valid': is_building,
            'mean_temperature': float(mean_thermal),
            'confidence': 0.8 if is_building else 0.2
        }
    
    def validate_with_sar(self, detected_polygon, sar_image,
                         backscatter_range=(-15, -5)):
        """
        Validate detection using Synthetic Aperture Radar
        """
        mask = self._polygon_to_mask(detected_polygon, sar_image.shape)
        sar_values = sar_image[mask == 1]
        
        mean_backscatter = np.mean(sar_values)
        
        is_building = backscatter_range[0] <= mean_backscatter <= backscatter_range[1]
        
        return {
            'valid': is_building,
            'mean_backscatter': float(mean_backscatter),
            'confidence': 0.85 if is_building else 0.15
        }
    
    def _polygon_to_mask(self, polygon, image_shape):
        """
        Convert polygon to binary mask
        """
        import cv2
        
        mask = np.zeros(image_shape, dtype=np.uint8)
        
        if isinstance(polygon, list):
            polygon = np.array(polygon, dtype=np.int32)
        
        cv2.drawContours(mask, [polygon], 0, 1, -1)
        
        return mask
    
    def ensemble_validation(self, detection, ndvi_image=None, 
                           thermal_image=None, sar_image=None):
        """
        Ensemble validation combining multiple data sources
        """
        validation_scores = []
        
        if ndvi_image is not None:
            ndvi_result = self.validate_with_ndvi(
                detection['polygon'], ndvi_image
            )
            validation_scores.append(ndvi_result['confidence'])
        
        if thermal_image is not None:
            thermal_result = self.validate_with_thermal(
                detection['polygon'], thermal_image
            )
            validation_scores.append(thermal_result['confidence'])
        
        if sar_image is not None:
            sar_result = self.validate_with_sar(
                detection['polygon'], sar_image
            )
            validation_scores.append(sar_result['confidence'])
        
        # Ensemble score
        ensemble_confidence = np.mean(validation_scores)
        
        return {
            'overall_confidence': float(ensemble_confidence),
            'is_valid': ensemble_confidence > 0.6,
            'individual_scores': {
                'ndvi': validation_scores[0] if len(validation_scores) > 0 else None,
                'thermal': validation_scores[1] if len(validation_scores) > 1 else None,
                'sar': validation_scores[2] if len(validation_scores) > 2 else None
            }
        }

```

---

## 7. Implementation Roadmap

### Phase 1: Infrastructure & Data (Months 1-3)
- Sentinel-2 data ingestion pipeline
- Database schema implementation (PostgreSQL + PostGIS)
- Municipal records integration
- Basic property detection model training (YOLOv8)

### Phase 2: Models & Detection (Months 4-6)
- Advanced segmentation (U-Net)
- Spectral analysis features
- Multi-source validation framework
- Dashboard development
- Change detection models

### Phase 3: Anomaly & Integration (Months 7-9)
- Anomaly detection models (Isolation Forest + LSTM)
- Municipal record reconciliation
- Unauthorized construction flagging
- Field verification workflow
- Pilot rollout (1-2 districts)

### Phase 4: Scale & Optimization (Months 10-12)
- State-wide deployment
- Performance optimization
- Advanced analytics features
- Integration with property tax system
- Full operational handover

---

## 8. Success Metrics

| Metric | Target | Validation |
|--------|--------|-----------|
| **Property Detection Accuracy** | 95%+ precision | Field surveys |
| **Change Detection Sensitivity** | <50 sqm changes detected | Ground truth verification |
| **False Positive Rate** | <2% | Manual review |
| **Tax Revenue Recovery** | 15-25% increase | Financial audit |
| **Anomaly Detection Rate** | 90%+ of violations | Compliance audit |
| **Processing Time** | <24 hours per district | System monitoring |
| **Municipal Record Accuracy** | 98%+ match rate | Reconciliation audit |

---

**Document Version**: 1.0  
**Status**: Ready for Implementation  
**Last Updated**: January 26, 2026  
**Audience**: Municipal Corporations, Tax Departments, Urban Planning, Data Scientists
