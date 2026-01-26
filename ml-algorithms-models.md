# Machine Learning Algorithms & Models

## 1. Recommendation Engine Models

### 1.1 Hybrid Recommendation System Architecture

```
┌─────────────────────────────────────────────────┐
│      User Query: Match SHG with Buyers          │
└────────────┬────────────────────────────────────┘
             │
    ┌────────┴────────┬────────────┬──────────┐
    │                 │            │          │
    ▼                 ▼            ▼          ▼
Content-Based    Collaborative  Context-   Knowledge
Filtering        Filtering       Based      Graph
(30%)             (30%)          (25%)      (15%)
    │                 │            │          │
    └────────┬────────┴────────────┴──────────┘
             │
             ▼
    Scoring & Ranking
    (Weighted Combination)
             │
             ▼
    ┌─────────────────────┐
    │ Top N Matches       │
    │ with Confidence     │
    └─────────────────────┘
```

### 1.2 Content-Based Filtering

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class ContentBasedRecommender:
    """
    Content-based filtering using product and buyer features
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500)
        self.shg_profiles_embedded = None
        self.buyer_profiles_embedded = None
    
    def extract_shg_content_features(self, shg_profiles):
        """
        Extract content features from SHG profiles
        
        Features:
        - Product descriptions (TF-IDF)
        - Category tags
        - Certifications
        - Geographic attributes
        - Quality metrics
        """
        
        features = []
        for shg in shg_profiles:
            feature_text = ' '.join([
                shg['category'].lower(),
                shg['product_description'].lower(),
                ' '.join(shg.get('certifications', [])),
                shg['location']['state'].lower(),
                str(shg.get('quality_score', 0))
            ])
            features.append(feature_text)
        
        # Convert to TF-IDF vectors
        content_vectors = self.vectorizer.fit_transform(features)
        return content_vectors
    
    def extract_buyer_content_features(self, buyer_profiles):
        """Extract content features from buyer preferences"""
        
        features = []
        for buyer in buyer_profiles:
            feature_text = ' '.join([
                ' '.join(buyer['category_preferences']),
                buyer['type'].lower(),
                ' '.join(buyer.get('required_certifications', [])),
                buyer['location']['state'].lower(),
                f"quality_level_{buyer.get('quality_requirement', 'standard')}"
            ])
            features.append(feature_text)
        
        # Use same vectorizer
        buyer_vectors = self.vectorizer.transform(features)
        return buyer_vectors
    
    def compute_content_similarity(self, shg_vectors, buyer_vectors):
        """Compute cosine similarity between SHG and buyer content"""
        
        similarity_matrix = cosine_similarity(shg_vectors, buyer_vectors)
        return similarity_matrix
    
    def recommend_content_based(self, target_shg_idx, buyer_vectors, top_n=10):
        """Get content-based recommendations"""
        
        # Use pre-computed SHG vectors
        similarity_scores = cosine_similarity(
            self.shg_profiles_embedded[target_shg_idx:target_shg_idx+1],
            buyer_vectors
        )[0]
        
        # Get top N recommendations
        top_buyer_indices = np.argsort(similarity_scores)[-top_n:][::-1]
        
        return [
            {
                'buyer_index': idx,
                'similarity_score': similarity_scores[idx]
            }
            for idx in top_buyer_indices
        ]
```

### 1.3 Collaborative Filtering

```python
from surprise import Dataset, Reader, SVD, NMF
from surprise.model_selection import cross_validate
import numpy as np

class CollaborativeFilteringRecommender:
    """
    Collaborative filtering using matrix factorization
    """
    
    def __init__(self):
        self.model = SVD(n_factors=50, lr_all=0.005, reg_all=0.02)
        self.interaction_matrix = None
        self.shg_factors = None
        self.buyer_factors = None
    
    def build_interaction_matrix(self, interactions_df):
        """
        Build user-item interaction matrix
        
        Interactions include:
        - Successful matches
        - Order history
        - Inquiry responses
        - Connection acceptance
        """
        
        # Create sparse interaction matrix
        reader = Reader(rating_scale=(0, 5))
        data = Dataset.load_from_df(
            interactions_df[['shg_id', 'buyer_id', 'interaction_score']],
            reader
        )
        
        return data
    
    def train_collaborative_model(self, interaction_data):
        """Train SVD model on interaction data"""
        
        # Cross-validation
        cross_validate(self.model, interaction_data, measures=['RMSE', 'MAE'], cv=5)
        
        # Train on full data
        trainset = interaction_data.build_full_trainset()
        self.model.fit(trainset)
        
        return self.model
    
    def get_collaborative_recommendations(self, shg_id, top_n=10):
        """Get recommendations based on collaborative filtering"""
        
        all_buyers = get_all_buyers()
        predictions = []
        
        for buyer_id in all_buyers:
            pred = self.model.predict(shg_id, buyer_id)
            predictions.append({
                'buyer_id': buyer_id,
                'predicted_score': pred.est
            })
        
        # Sort by predicted score
        recommendations = sorted(
            predictions,
            key=lambda x: x['predicted_score'],
            reverse=True
        )[:top_n]
        
        return recommendations
```

### 1.4 Context-Based Filtering

```python
class ContextBasedRecommender:
    """
    Context-based filtering using contextual features
    """
    
    def __init__(self):
        self.context_weights = {
            'geographic_proximity': 0.40,
            'logistics_compatibility': 0.30,
            'volume_compatibility': 0.20,
            'quality_match': 0.10
        }
    
    def calculate_geographic_similarity(self, shg_location, buyer_location):
        """
        Calculate geographic proximity score
        
        Factors:
        - Distance (Haversine formula)
        - Same state/region (bonus)
        - Transportation infrastructure
        """
        from math import radians, cos, sin, asin, sqrt
        
        def haversine(lon1, lat1, lon2, lat2):
            """Calculate distance between two points on Earth"""
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            km = 6371 * c
            return km
        
        distance_km = haversine(
            shg_location['lon'], shg_location['lat'],
            buyer_location['lon'], buyer_location['lat']
        )
        
        # Normalize distance to 0-1 score (max distance 3000 km)
        distance_score = max(0, 1 - (distance_km / 3000))
        
        # Bonus for same state
        same_state_bonus = 0.2 if shg_location['state'] == buyer_location['state'] else 0
        
        geo_score = min(1.0, distance_score + same_state_bonus)
        
        return geo_score
    
    def calculate_logistics_compatibility(self, shg_capacity, buyer_order_volume, 
                                         distance_km, shipping_cost_ratio_limit=0.1):
        """
        Calculate logistics compatibility
        """
        
        # Volume compatibility
        if buyer_order_volume <= shg_capacity:
            volume_compatibility = 1.0
        elif buyer_order_volume <= shg_capacity * 1.5:
            volume_compatibility = 0.8
        else:
            volume_compatibility = 0.5
        
        # Shipping cost estimation
        estimated_shipping_cost = distance_km * 0.5  # Simplified: ₹0.5 per km
        avg_product_value = 500  # Assume ₹500 average product value
        cost_ratio = estimated_shipping_cost / (buyer_order_volume * avg_product_value)
        
        if cost_ratio <= shipping_cost_ratio_limit:
            shipping_score = 1.0
        elif cost_ratio <= shipping_cost_ratio_limit * 2:
            shipping_score = 0.7
        else:
            shipping_score = 0.3
        
        logistics_score = 0.5 * volume_compatibility + 0.5 * shipping_score
        
        return logistics_score
    
    def calculate_context_score(self, shg_profile, buyer_profile, distance_km):
        """Calculate overall context-based score"""
        
        geo_score = self.calculate_geographic_similarity(
            shg_profile['location'],
            buyer_profile['location']
        )
        
        logistics_score = self.calculate_logistics_compatibility(
            shg_capacity=shg_profile['capacity'],
            buyer_order_volume=buyer_profile['avg_order_volume'],
            distance_km=distance_km
        )
        
        # Volume compatibility
        volume_score = min(
            shg_profile['capacity'] / buyer_profile['avg_order_volume'],
            1.0
        )
        
        # Quality match
        quality_matches = len(set(shg_profile['certifications']) & 
                             set(buyer_profile['required_certifications']))
        quality_score = quality_matches / max(
            len(buyer_profile['required_certifications']), 1
        )
        
        context_score = (
            self.context_weights['geographic_proximity'] * geo_score +
            self.context_weights['logistics_compatibility'] * logistics_score +
            self.context_weights['volume_compatibility'] * volume_score +
            self.context_weights['quality_match'] * quality_score
        )
        
        return context_score
```

---

## 2. Demand Forecasting Models

### 2.1 LSTM RNN Model

```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

class LSTMDemandForecaster:
    """
    LSTM RNN model for demand forecasting
    """
    
    def __init__(self, sequence_length=30, forecast_steps=7):
        self.sequence_length = sequence_length
        self.forecast_steps = forecast_steps
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = self._build_model()
    
    def _build_model(self):
        """Build LSTM model architecture"""
        
        model = Sequential([
            LSTM(units=50, return_sequences=True, 
                 input_shape=(self.sequence_length, 1)),
            Dropout(0.2),
            LSTM(units=50, return_sequences=True),
            Dropout(0.2),
            LSTM(units=50, return_sequences=False),
            Dropout(0.2),
            Dense(units=25),
            Dense(units=1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model
    
    def prepare_data(self, sales_data):
        """
        Prepare data for LSTM
        
        Args:
            sales_data: Array of historical sales
            
        Returns:
            X_train, y_train: Sequences and targets
        """
        
        # Normalize data
        scaled_data = self.scaler.fit_transform(sales_data.reshape(-1, 1))
        
        # Create sequences
        X, y = [], []
        for i in range(len(scaled_data) - self.sequence_length):
            X.append(scaled_data[i:(i + self.sequence_length), 0])
            y.append(scaled_data[i + self.sequence_length, 0])
        
        return np.array(X).reshape(-1, self.sequence_length, 1), np.array(y)
    
    def train(self, sales_data, epochs=50, batch_size=32):
        """Train the LSTM model"""
        
        X_train, y_train = self.prepare_data(sales_data)
        
        self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=0
        )
    
    def forecast(self, recent_sales, steps=7):
        """
        Generate demand forecast
        
        Args:
            recent_sales: Last 30 days of sales data
            steps: Number of days to forecast
            
        Returns:
            forecast: Predicted demand values
        """
        
        scaled_data = self.scaler.transform(recent_sales.reshape(-1, 1))
        
        forecast = []
        current_sequence = scaled_data[-self.sequence_length:].copy()
        
        for _ in range(steps):
            # Predict next value
            next_pred = self.model.predict(
                current_sequence.reshape(1, self.sequence_length, 1),
                verbose=0
            )[0, 0]
            forecast.append(next_pred)
            
            # Update sequence
            current_sequence = np.append(current_sequence[1:], next_pred)
        
        # Inverse transform
        forecast_unscaled = self.scaler.inverse_transform(
            np.array(forecast).reshape(-1, 1)
        ).flatten()
        
        return forecast_unscaled
```

### 2.2 XGBoost Model

```python
import xgboost as xgb
from sklearn.model_selection import train_test_split

class XGBoostDemandForecaster:
    """
    XGBoost model for demand forecasting with external features
    """
    
    def __init__(self):
        self.model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )
        self.feature_names = None
    
    def extract_features(self, product_data, external_data):
        """
        Extract features for XGBoost
        
        Features:
        - Lagged sales (1d, 7d, 30d)
        - Day of week, month, quarter
        - Weather (temperature, rainfall)
        - Holiday indicator
        - Competitor activity
        - Marketing spend
        """
        
        features = []
        
        for i in range(len(product_data)):
            feature_dict = {
                # Temporal features
                'day_of_week': product_data[i]['date'].weekday(),
                'month': product_data[i]['date'].month,
                'quarter': (product_data[i]['date'].month - 1) // 3 + 1,
                'is_holiday': external_data[i].get('is_holiday', 0),
                
                # Lagged sales
                'sales_lag_1d': product_data[i-1]['sales'] if i > 0 else 0,
                'sales_lag_7d': product_data[i-7]['sales'] if i > 7 else 0,
                'sales_lag_30d': product_data[i-30]['sales'] if i > 30 else 0,
                
                # Moving averages
                'sales_ma_7d': np.mean([
                    product_data[j]['sales'] for j in range(max(0, i-7), i)
                ]),
                'sales_ma_30d': np.mean([
                    product_data[j]['sales'] for j in range(max(0, i-30), i)
                ]),
                
                # External features
                'temperature': external_data[i].get('temperature', 25),
                'rainfall': external_data[i].get('rainfall', 0),
                'competitor_count': external_data[i].get('competitor_count', 5),
                'marketing_spend': external_data[i].get('marketing_spend', 0),
                
                # Target
                'target_sales': product_data[i]['sales']
            }
            features.append(feature_dict)
        
        return pd.DataFrame(features)
    
    def train(self, features_df):
        """Train XGBoost model"""
        
        X = features_df.drop('target_sales', axis=1)
        y = features_df['target_sales']
        
        self.feature_names = X.columns.tolist()
        
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=10,
            verbose=0
        )
    
    def forecast(self, features_df):
        """Generate forecast using XGBoost"""
        
        X = features_df.drop('target_sales', axis=1)
        predictions = self.model.predict(X)
        
        return predictions
    
    def get_feature_importance(self, top_n=10):
        """Get feature importance"""
        
        importance = self.model.feature_importances_
        indices = np.argsort(importance)[-top_n:][::-1]
        
        return [
            {
                'feature': self.feature_names[i],
                'importance': importance[i]
            }
            for i in indices
        ]
```

### 2.3 Facebook Prophet Model

```python
from fbprophet import Prophet

class ProphetDemandForecaster:
    """
    Facebook Prophet for time series forecasting
    """
    
    def __init__(self, yearly_seasonality=True, weekly_seasonality=True):
        self.model = Prophet(
            yearly_seasonality=yearly_seasonality,
            weekly_seasonality=weekly_seasonality,
            daily_seasonality=False
        )
    
    def prepare_prophet_data(self, sales_data_with_dates):
        """
        Prepare data in Prophet format
        
        Args:
            sales_data_with_dates: List of {'ds': date, 'y': sales}
        """
        
        df = pd.DataFrame(sales_data_with_dates)
        df['ds'] = pd.to_datetime(df['ds'])
        
        return df
    
    def add_regressors(self, df, external_features):
        """
        Add external features as regressors
        
        Args:
            df: Prophet DataFrame
            external_features: Dict of feature_name -> values
        """
        
        for feature_name, values in external_features.items():
            df[feature_name] = values
            self.model.add_regressor(feature_name)
        
        return df
    
    def train(self, df):
        """Train Prophet model"""
        
        self.model.fit(df)
    
    def forecast(self, periods=30):
        """
        Generate forecast
        
        Args:
            periods: Number of periods to forecast
            
        Returns:
            forecast_df: DataFrame with forecast
        """
        
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
```

---

## 3. Ensemble Methods

### 3.1 Weighted Ensemble Forecasting

```python
class EnsembleDemandForecaster:
    """
    Ensemble method combining multiple forecasting models
    """
    
    def __init__(self, lstm_weight=0.4, xgboost_weight=0.35, prophet_weight=0.25):
        self.lstm_model = LSTMDemandForecaster()
        self.xgboost_model = XGBoostDemandForecaster()
        self.prophet_model = ProphetDemandForecaster()
        
        self.weights = {
            'lstm': lstm_weight,
            'xgboost': xgboost_weight,
            'prophet': prophet_weight
        }
    
    def train_all_models(self, historical_sales, features_df, prophet_df):
        """Train all models"""
        
        self.lstm_model.train(historical_sales)
        self.xgboost_model.train(features_df)
        self.prophet_model.train(prophet_df)
    
    def ensemble_forecast(self, recent_sales, features_df, periods=30):
        """
        Generate ensemble forecast
        
        Returns ensemble of predictions from all models
        """
        
        # Get predictions from each model
        lstm_forecast = self.lstm_model.forecast(recent_sales, steps=periods)
        xgboost_forecast = self.xgboost_model.forecast(features_df)
        prophet_forecast = self.prophet_model.forecast(periods=periods)['yhat'].values
        
        # Weighted ensemble
        ensemble_forecast = (
            self.weights['lstm'] * lstm_forecast +
            self.weights['xgboost'] * xgboost_forecast +
            self.weights['prophet'] * prophet_forecast
        )
        
        # Calculate confidence intervals
        std_dev = np.std([lstm_forecast, xgboost_forecast, prophet_forecast], axis=0)
        confidence_lower = ensemble_forecast - 1.96 * std_dev
        confidence_upper = ensemble_forecast + 1.96 * std_dev
        
        return {
            'forecast': ensemble_forecast,
            'lower_bound': confidence_lower,
            'upper_bound': confidence_upper,
            'std_dev': std_dev
        }
```

---

## 4. Price Optimization Models

### 4.1 Dynamic Pricing Algorithm

```python
from scipy.optimize import minimize

class DynamicPricingOptimizer:
    """
    Optimize product pricing using demand elasticity
    """
    
    def __init__(self):
        self.elasticity_model = self._build_elasticity_model()
    
    def _build_elasticity_model(self):
        """Build price elasticity model using historical data"""
        
        # Placeholder: would use actual model trained on data
        def elasticity_function(price, base_price=100, elasticity=-1.5):
            return elasticity * (price - base_price) / base_price
        
        return elasticity_function
    
    def calculate_optimal_price(self, product_id, current_inventory, 
                                cost, demand_forecast):
        """
        Calculate optimal price to maximize revenue or profit
        
        Objective function: Maximize Revenue = Price × Quantity
        Constraint: Inventory limits
        """
        
        def revenue_function(price):
            # Estimated quantity sold at given price
            quantity = demand_forecast * (1 + self.elasticity_model(price))
            quantity = min(max(quantity, 0), current_inventory)
            
            # Revenue
            return -price * quantity  # Negative because we minimize
        
        # Optimization bounds
        min_price = cost * 1.1  # Minimum 10% margin
        max_price = cost * 3.0  # Maximum 3x markup
        
        # Find optimal price
        result = minimize(
            revenue_function,
            x0=cost * 1.5,
            bounds=[(min_price, max_price)],
            method='L-BFGS-B'
        )
        
        optimal_price = result.x[0]
        expected_revenue = -result.fun
        
        return {
            'optimal_price': optimal_price,
            'expected_revenue': expected_revenue,
            'expected_quantity': demand_forecast * (1 + self.elasticity_model(optimal_price))
        }
```

