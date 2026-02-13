# ML Algorithms for Land Suitability & Conflict Detection
## Advanced Machine Learning Models for Renewable Energy Land Allocation

---

## 1. Land Suitability Prediction Models

### 1.1 Ensemble Random Forest for Suitability

```python
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

class EnsembleLandSuitabilityModel:
    """
    Ensemble of Random Forest and Gradient Boosting for land suitability
    """
    
    def __init__(self, project_type='solar'):
        self.project_type = project_type
        self.rf_model = RandomForestRegressor(
            n_estimators=200,
            max_depth=25,
            min_samples_split=10,
            min_samples_leaf=4,
            n_jobs=-1,
            random_state=42
        )
        self.gb_model = GradientBoostingRegressor(
            n_estimators=150,
            max_depth=10,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.feature_names = None
    
    def prepare_features(self, satellite_data, dem_data, climate_data, 
                        infrastructure_data, labels_df):
        """
        Prepare comprehensive feature set
        
        Args:
            satellite_data: Dict of spectral indices
            dem_data: Dict of topographic features
            climate_data: Dict of climate variables
            infrastructure_data: Dict of distance to features
            labels_df: DataFrame with ground truth labels
        
        Returns:
            X_train, X_test, y_train, y_test
        """
        
        features = []
        
        # Spectral features
        spectral_features = [
            'ndvi', 'ndbi', 'ndwi', 'ndii', 'bsi',
            'evi', 'gci', 'dvi'
        ]
        
        # Topographic features
        topographic_features = [
            'elevation', 'slope', 'aspect', 'roughness',
            'twi', 'tpi', 'terrain_curvature'
        ]
        
        # Climate features
        climate_features = [
            'solar_irradiance' if self.project_type == 'solar' else 'wind_speed',
            'temperature', 'precipitation', 'humidity'
        ]
        
        # Infrastructure/Distance features
        infrastructure_features = [
            'distance_substation_km',
            'distance_transmission_line_km',
            'distance_road_km',
            'distance_water_km',
            'distance_urban_km'
        ]
        
        # Land cover features
        landcover_features = [
            'landcover_barren',
            'landcover_grassland',
            'landcover_agriculture',
            'landcover_forest',
            'landcover_water'
        ]
        
        # Combine all features
        all_features = (
            spectral_features + topographic_features + 
            climate_features + infrastructure_features + landcover_features
        )
        
        # Create feature matrix
        feature_matrix = np.column_stack([
            satellite_data.get(f, np.zeros(labels_df.shape[0]))
            for f in spectral_features
        ] + [
            dem_data.get(f, np.zeros(labels_df.shape[0]))
            for f in topographic_features
        ] + [
            climate_data.get(f, np.zeros(labels_df.shape[0]))
            for f in climate_features
        ] + [
            infrastructure_data.get(f, np.zeros(labels_df.shape[0]))
            for f in infrastructure_features
        ] + [
            labels_df.get(f, np.zeros(labels_df.shape[0]))
            for f in landcover_features
        ])
        
        self.feature_names = all_features
        X = pd.DataFrame(feature_matrix, columns=all_features)
        y = labels_df['suitability_score'].values
        
        # Remove NaN and infinite values
        valid_idx = ~(np.isnan(X).any(axis=1) | np.isinf(X).any(axis=1))
        X = X[valid_idx]
        y = y[valid_idx]
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42
        )
        
        return X_train, X_test, y_train, y_test
    
    def train(self, X_train, y_train):
        """Train ensemble models"""
        
        # Normalize features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train Random Forest
        self.rf_model.fit(X_train_scaled, y_train)
        
        # Train Gradient Boosting
        self.gb_model.fit(X_train_scaled, y_train)
        
        # Cross-validation scores
        rf_scores = cross_val_score(
            self.rf_model, X_train_scaled, y_train,
            cv=5, scoring='r2'
        )
        
        gb_scores = cross_val_score(
            self.gb_model, X_train_scaled, y_train,
            cv=5, scoring='r2'
        )
        
        print(f"RF CV R²: {rf_scores.mean():.4f} (+/- {rf_scores.std():.4f})")
        print(f"GB CV R²: {gb_scores.mean():.4f} (+/- {gb_scores.std():.4f})")
    
    def predict(self, X):
        """
        Predict land suitability using ensemble
        
        Args:
            X: Feature matrix
        
        Returns:
            predictions: Suitability scores (0-100)
        """
        
        X_scaled = self.scaler.transform(X)
        
        # Weighted ensemble: 60% RF, 40% GB
        rf_pred = self.rf_model.predict(X_scaled)
        gb_pred = self.gb_model.predict(X_scaled)
        
        ensemble_pred = 0.6 * rf_pred + 0.4 * gb_pred
        
        # Clip to valid range
        ensemble_pred = np.clip(ensemble_pred, 0, 100)
        
        return ensemble_pred
    
    def get_feature_importance(self, top_n=20):
        """Get most important features"""
        
        rf_importance = self.rf_model.feature_importances_
        gb_importance = self.gb_model.feature_importances_
        
        # Weighted importance
        ensemble_importance = 0.6 * rf_importance + 0.4 * gb_importance
        
        top_indices = np.argsort(ensemble_importance)[-top_n:][::-1]
        
        return [
            {
                'feature': self.feature_names[i],
                'importance': ensemble_importance[i]
            }
            for i in top_indices
        ]
```

### 1.2 Deep Learning CNN for Spatial Context

```python
import tensorflow as tf
from tensorflow.keras import layers, models

class SpatialContextCNN:
    """
    Convolutional Neural Network to capture spatial context
    """
    
    def __init__(self, input_shape=(64, 64, 13)):
        """
        Args:
            input_shape: (spatial_size, spatial_size, num_bands)
        """
        self.input_shape = input_shape
        self.model = self._build_model()
    
    def _build_model(self):
        """Build CNN architecture"""
        
        model = models.Sequential([
            # Input
            layers.Input(shape=self.input_shape),
            
            # Normalization
            layers.Lambda(lambda x: x / 10000.0),  # Normalize Sentinel-2 DN
            
            # Block 1
            layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.2),
            
            # Block 2
            layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.2),
            
            # Block 3
            layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.3),
            
            # Global pooling
            layers.GlobalAveragePooling2D(),
            
            # Dense layers
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            # Output: suitability score (0-100)
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def train(self, X_train, y_train, X_val, y_val, epochs=50):
        """Train CNN model"""
        
        # Data augmentation
        augmentation = tf.keras.Sequential([
            layers.RandomRotation(0.2),
            layers.RandomZoom(0.2),
            layers.RandomFlip('horizontal'),
            layers.RandomFlip('vertical')
        ])
        
        # Augment training data
        X_train_augmented = np.concatenate([
            X_train,
            augmentation(X_train[:len(X_train)//2])
        ])
        y_train_augmented = np.concatenate([
            y_train,
            y_train[:len(y_train)//2]
        ])
        
        # Callbacks
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6
        )
        
        history = self.model.fit(
            X_train_augmented, y_train_augmented * 100,  # Scale to 0-100
            validation_data=(X_val, y_val * 100),
            epochs=epochs,
            batch_size=32,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        return history
    
    def predict(self, X):
        """Predict suitability"""
        predictions = self.model.predict(X) * 100  # Scale to 0-100
        return np.clip(predictions.flatten(), 0, 100)
```

---

## 2. Conflict Detection Models

### 2.1 Multi-Class Conflict Classifier

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score

class ConflictDetectionModel:
    """
    Multi-class classifier for conflict types:
    - 0: No conflict
    - 1: Protected area
    - 2: Water body
    - 3: Urban/Settlement
    - 4: Agricultural (high-value)
    - 5: Forest
    - 6: Infrastructure
    """
    
    CONFLICT_CLASSES = {
        0: 'no_conflict',
        1: 'protected_area',
        2: 'water_body',
        3: 'urban',
        4: 'agriculture',
        5: 'forest',
        6: 'infrastructure'
    }
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=20,
            min_samples_leaf=10,
            class_weight='balanced',
            n_jobs=-1,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.feature_names = None
    
    def prepare_conflict_labels(self, geospatial_layers):
        """
        Prepare labeled training data
        
        Args:
            geospatial_layers: Dict of conflict layers with masks
        
        Returns:
            X_train, y_train: Training data and labels
        """
        
        conflict_labels = np.zeros(geospatial_layers['grid_shape'], dtype=np.uint8)
        
        # Assign conflict classes (priority order)
        if 'protected_areas' in geospatial_layers:
            protected = geospatial_layers['protected_areas']
            conflict_labels[protected] = 1
        
        if 'water_bodies' in geospatial_layers:
            water = geospatial_layers['water_bodies']
            conflict_labels[water] = 2
        
        if 'urban_areas' in geospatial_layers:
            urban = geospatial_layers['urban_areas']
            conflict_labels[urban] = 3
        
        if 'high_value_agriculture' in geospatial_layers:
            agriculture = geospatial_layers['high_value_agriculture']
            conflict_labels[agriculture] = 4
        
        if 'forest_cover' in geospatial_layers:
            forest = geospatial_layers['forest_cover']
            conflict_labels[forest] = 5
        
        if 'power_infrastructure' in geospatial_layers:
            infrastructure = geospatial_layers['power_infrastructure']
            conflict_labels[infrastructure] = 6
        
        return conflict_labels
    
    def train(self, X_train, y_train):
        """Train conflict classifier"""
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        self.model.fit(X_train_scaled, y_train)
        
        # Cross-validation
        scores = cross_val_score(
            self.model, X_train_scaled, y_train,
            cv=5, scoring='weighted_f1'
        )
        
        print(f"Conflict Classifier CV F1: {scores.mean():.4f} (+/- {scores.std():.4f})")
    
    def predict_conflicts(self, X):
        """
        Predict conflict class
        
        Returns:
            conflict_classes: (N,) array of conflict types
            conflict_probabilities: (N, 7) array of probabilities
        """
        
        X_scaled = self.scaler.transform(X)
        
        classes = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        
        return classes, probabilities
    
    def get_conflict_probability_maps(self, X):
        """Get probability maps for each conflict class"""
        
        X_scaled = self.scaler.transform(X)
        probabilities = self.model.predict_proba(X_scaled)
        
        probability_maps = {}
        for class_id, class_name in self.CONFLICT_CLASSES.items():
            probability_maps[class_name] = probabilities[:, class_id]
        
        return probability_maps
```

### 2.2 Anomaly Detection for Unknown Conflicts

```python
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope

class AnomalyConflictDetector:
    """
    Detect potential conflicts not captured in training data
    using anomaly detection
    """
    
    def __init__(self):
        self.isolation_forest = IsolationForest(
            contamination=0.05,
            random_state=42,
            n_jobs=-1
        )
        self.elliptic_envelope = EllipticEnvelope(
            contamination=0.05,
            random_state=42
        )
    
    def train(self, X_known_safe):
        """Train on known safe areas"""
        
        self.isolation_forest.fit(X_known_safe)
        self.elliptic_envelope.fit(X_known_safe)
    
    def detect_anomalies(self, X):
        """Detect anomalous pixels"""
        
        # Combine both methods
        if_scores = self.isolation_forest.score_samples(X)
        ee_scores = self.elliptic_envelope.score_samples(X)
        
        # Ensemble anomaly score
        anomaly_scores = -0.5 * (if_scores + ee_scores)
        
        return anomaly_scores
    
    def identify_potential_conflicts(self, X, threshold=0.5):
        """Identify pixels with potential unknown conflicts"""
        
        anomaly_scores = self.detect_anomalies(X)
        
        # Normalize scores to 0-1
        normalized_scores = (anomaly_scores - anomaly_scores.min()) / \
                           (anomaly_scores.max() - anomaly_scores.min())
        
        potential_conflicts = normalized_scores > threshold
        
        return potential_conflicts, normalized_scores
```

---

## 3. Advanced Suitability Optimization

### 3.1 Multi-Objective Optimization

```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination

class RenewableEnergyAllocationProblem(Problem):
    """
    Multi-objective land allocation problem
    
    Objectives:
    1. Maximize total suitability score
    2. Minimize installation cost
    3. Maximize grid connectivity score
    4. Maximize environmental impact score
    """
    
    def __init__(self, candidate_sites, state_config):
        self.candidate_sites = candidate_sites
        self.state_config = state_config
        
        n_sites = len(candidate_sites)
        
        super().__init__(
            n_var=n_sites,
            n_obj=4,
            n_constr=3,
            type_var=int,
            xl=0,
            xu=1
        )
    
    def _evaluate(self, x, out, *args, **kwargs):
        """
        Evaluate objectives and constraints
        
        Args:
            x: Binary allocation vector
        """
        
        # Objective 1: Maximize suitability
        suitability_scores = np.array([
            site['suitability_score'] for site in self.candidate_sites
        ])
        obj1 = -np.sum(suitability_scores * x)  # Negative for minimization
        
        # Objective 2: Minimize cost
        costs = np.array([
            site['installation_cost_cr'] for site in self.candidate_sites
        ])
        obj2 = np.sum(costs * x)
        
        # Objective 3: Maximize grid connectivity
        grid_scores = np.array([
            100 - min(site['distance_to_substation_km'] / 0.5, 100)
            for site in self.candidate_sites
        ])
        obj3 = -np.sum(grid_scores * x)
        
        # Objective 4: Maximize environmental benefit
        env_scores = np.array([
            site.get('environmental_benefit_score', 50)
            for site in self.candidate_sites
        ])
        obj4 = -np.sum(env_scores * x)
        
        # Constraint 1: Capacity target (±10%)
        capacities = np.array([
            site['capacity_mw'] for site in self.candidate_sites
        ])
        total_capacity = np.sum(capacities * x)
        target = self.state_config['target_capacity_mw']
        
        c1 = abs(total_capacity - target) / target - 0.1
        
        # Constraint 2: Budget limit
        total_cost = np.sum(costs * x)
        budget = self.state_config['budget_cr']
        c2 = total_cost - budget
        
        # Constraint 3: Geographic distribution (30% min in each district)
        districts = set([site['district'] for site in self.candidate_sites])
        c3 = 0
        for district in districts:
            district_sites = [i for i, site in enumerate(self.candidate_sites)
                             if site['district'] == district]
            district_capacity = sum([
                self.candidate_sites[i]['capacity_mw']
                for i in district_sites
            ]) * np.sum(x[district_sites])
            min_district_capacity = target * 0.15
            c3 += max(0, min_district_capacity - district_capacity)
        
        out['F'] = np.column_stack([obj1, obj2, obj3, obj4])
        out['G'] = np.column_stack([c1, c2, c3])


class MultiObjectiveOptimizer:
    """Solve multi-objective allocation problem"""
    
    def __init__(self, problem):
        self.problem = problem
    
    def optimize(self, pop_size=100, generations=50):
        """Run NSGA-II optimization"""
        
        algorithm = NSGA2(
            pop_size=pop_size,
            sampling=FloatRandomSampling(),
            crossover=SBX(prob=0.9, eta=15),
            mutation=PM(eta=20),
            eliminate_duplicates=True
        )
        
        res = minimize(
            self.problem,
            algorithm,
            get_termination("n_gen", generations),
            seed=1,
            verbose=True
        )
        
        return res
    
    def extract_pareto_solutions(self, res, n_solutions=10):
        """Extract Pareto-optimal solutions"""
        
        # Select most diverse solutions from Pareto front
        from sklearn.cluster import KMeans
        
        pareto_front = res.F
        
        if len(pareto_front) <= n_solutions:
            return pareto_front
        
        # K-means clustering to select diverse solutions
        kmeans = KMeans(n_clusters=n_solutions, random_state=42)
        kmeans.fit(pareto_front)
        
        # Select closest to cluster centers
        distances = np.min(
            np.linalg.norm(pareto_front[:, np.newaxis] - kmeans.cluster_centers_, axis=2),
            axis=1
        )
        selected_indices = np.argsort(distances)[:n_solutions]
        
        return pareto_front[selected_indices]
```

### 3.2 Explainability & Interpretability

```python
import shap

class ModelExplainability:
    """Explain ML predictions using SHAP"""
    
    def __init__(self, model, X_background):
        """
        Args:
            model: Trained ML model
            X_background: Background data for SHAP
        """
        self.model = model
        self.explainer = shap.TreeExplainer(model)
        self.X_background = X_background
    
    def explain_prediction(self, X_single):
        """
        Explain single prediction
        
        Returns:
            shap_values: Feature contributions
            base_value: Model baseline
        """
        
        shap_values = self.explainer.shap_values(X_single)
        
        return {
            'shap_values': shap_values,
            'base_value': self.explainer.expected_value,
            'prediction': self.model.predict(X_single)[0]
        }
    
    def get_feature_contributions(self, X):
        """Get mean SHAP values for all features"""
        
        shap_values = self.explainer.shap_values(X)
        
        # Mean absolute SHAP values
        mean_abs_shap = np.mean(np.abs(shap_values), axis=0)
        
        return sorted(
            zip(mean_abs_shap, self.model.feature_names_in_),
            reverse=True
        )
    
    def create_force_plot(self, X_single):
        """Create force plot for single prediction"""
        
        shap_values = self.explainer.shap_values(X_single)
        
        return shap.force_plot(
            self.explainer.expected_value,
            shap_values[0],
            X_single,
            feature_names=self.model.feature_names_in_
        )
    
    def create_dependence_plot(self, X, feature_name):
        """Create dependence plot for feature"""
        
        shap_values = self.explainer.shap_values(X)
        feature_idx = list(self.model.feature_names_in_).index(feature_name)
        
        return shap.dependence_plot(
            feature_idx,
            shap_values,
            X,
            feature_names=self.model.feature_names_in_
        )
```

---

## 4. Uncertainty Quantification

### 4.1 Bayesian Ensemble with Uncertainty

```python
from sklearn.ensemble import BaggingRegressor
from sklearn.tree import DecisionTreeRegressor
import scipy.stats as stats

class UncertaintyQuantifier:
    """
    Quantify prediction uncertainty using bootstrap
    """
    
    def __init__(self, n_models=100):
        self.n_models = n_models
        self.models = []
    
    def train_ensemble(self, X_train, y_train):
        """Train bootstrap ensemble"""
        
        for i in range(self.n_models):
            # Bootstrap sample
            indices = np.random.choice(len(X_train), len(X_train), replace=True)
            X_boot = X_train[indices]
            y_boot = y_train[indices]
            
            # Train model
            model = RandomForestRegressor(
                n_estimators=50,
                max_depth=15,
                random_state=i
            )
            model.fit(X_boot, y_boot)
            self.models.append(model)
    
    def predict_with_uncertainty(self, X):
        """
        Predict with uncertainty bands
        
        Returns:
            predictions: Mean prediction
            lower_bound: 5th percentile
            upper_bound: 95th percentile
            uncertainty: Standard deviation
        """
        
        all_predictions = np.array([
            model.predict(X) for model in self.models
        ])
        
        predictions = np.mean(all_predictions, axis=0)
        uncertainty = np.std(all_predictions, axis=0)
        
        lower_bound = np.percentile(all_predictions, 5, axis=0)
        upper_bound = np.percentile(all_predictions, 95, axis=0)
        
        return {
            'predictions': predictions,
            'uncertainty': uncertainty,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'confidence_interval': upper_bound - lower_bound
        }
```

---

## 5. Model Performance Metrics

### 5.1 Custom Evaluation Metrics

```python
class AllocationMetrics:
    """
    Metrics specific to renewable energy land allocation
    """
    
    @staticmethod
    def capacity_utilization_rate(allocated_sites, target_capacity):
        """
        Calculate how close allocation is to target capacity
        
        Returns:
            rate: (0-1) where 1.0 = exact target
        """
        
        total_capacity = sum([site['capacity_mw'] for site in allocated_sites])
        
        return min(total_capacity, target_capacity) / target_capacity
    
    @staticmethod
    def cost_efficiency_score(allocated_sites, budget):
        """
        Calculate cost efficiency (capacity per rupee)
        
        Returns:
            score: MW per crore
        """
        
        total_capacity = sum([site['capacity_mw'] for site in allocated_sites])
        total_cost = sum([site['installation_cost_cr'] for site in allocated_sites])
        
        return total_capacity / total_cost if total_cost > 0 else 0
    
    @staticmethod
    def geographic_distribution_score(allocated_sites, districts):
        """
        Calculate geographic distribution fairness
        
        Uses Gini coefficient: 0 = perfect equality, 1 = perfect inequality
        """
        
        district_capacities = {}
        for site in allocated_sites:
            district = site['district']
            if district not in district_capacities:
                district_capacities[district] = 0
            district_capacities[district] += site['capacity_mw']
        
        capacities = list(district_capacities.values())
        capacities.sort()
        
        n = len(capacities)
        cumsum = np.cumsum(capacities)
        
        gini = (2 * np.sum((np.arange(1, n+1)) * capacities)) / (n * np.sum(capacities)) - (n + 1) / n
        
        # Convert to fairness score (0-1)
        fairness_score = 1 - gini
        
        return fairness_score
    
    @staticmethod
    def environmental_impact_score(allocated_sites):
        """
        Calculate overall environmental impact
        
        Higher score = lower environmental impact
        """
        
        scores = [site.get('environmental_benefit_score', 50) for site in allocated_sites]
        
        return np.mean(scores) if scores else 0
    
    @staticmethod
    def implementation_feasibility_score(allocated_sites):
        """
        Calculate feasibility of implementation
        Considers: grid connection, land availability, administrative clearance
        """
        
        feasibility_scores = []
        
        for site in allocated_sites:
            # Grid connection feasibility (inversely proportional to distance)
            grid_feasibility = max(0, 100 - (site['distance_to_substation_km'] * 2))
            
            # Land availability (based on parcel size)
            land_feasibility = min(100, site['area_sqkm'] / 10 * 20)
            
            # Administrative readiness
            admin_feasibility = site.get('administrative_readiness_score', 50)
            
            combined = (grid_feasibility + land_feasibility + admin_feasibility) / 3
            feasibility_scores.append(combined)
        
        return np.mean(feasibility_scores) if feasibility_scores else 0
```

