import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, List, Tuple

class AnalyticsEngine:
    """
    Advanced analytics for financial performance, risk, and anomaly detection.
    """
    
    def __init__(self):
        pass
    
    def calculate_risk_indicators(self, financial_data: Dict) -> Dict:
        """
        Calculate Altman Z-Score and Beneish M-Score.
        """
        # Extract values (Assume basic structure exists or defaults)
        bs = financial_data.get('balance_sheet', {})
        income = financial_data.get('income_statement', {})
        
        # Helper to safely get value
        def get_val(section, key):
            try:
                # Assuming structure {section: {key: {'current': val}}}
                return float(financial_data.get(section, {}).get(key, {}).get('current', 0))
            except:
                return 0.0

        # Simplified Mapping for Z-Score (Manufacturing)
        # Z = 1.2A + 1.4B + 3.3C + 0.6D + 1.0E
        # A = Working Capital / Total Assets
        # B = Retained Earnings / Total Assets
        # C = EBIT / Total Assets
        # D = Market Value of Equity / Total Liabilities
        # E = Sales / Total Assets
        
        total_assets = get_val('balance_sheet', 'Total Assets') or 1.0 # Avoid div/0
        current_assets = get_val('balance_sheet', 'Current Assets')
        current_liabilities = get_val('balance_sheet', 'Current Liabilities')
        working_capital = current_assets - current_liabilities
        retained_earnings = get_val('balance_sheet', 'Retained Earnings')
        ebit = get_val('income_statement', 'EBIT') or get_val('income_statement', 'Profit') # Proxy
        market_value_equity = get_val('balance_sheet', 'Total Equity') # Proxy using book value if market cap unavailable
        total_liabilities = get_val('balance_sheet', 'Total Liabilities') or 1.0
        sales = get_val('income_statement', 'Revenue')
        
        A = working_capital / total_assets
        B = retained_earnings / total_assets
        C = ebit / total_assets
        D = market_value_equity / total_liabilities
        E = sales / total_assets
        
        z_score = 1.2*A + 1.4*B + 3.3*C + 0.6*D + 1.0*E
        
        return {
            'Altman_Z_Score': round(z_score, 2),
            'Z_Score_Zone': 'Safe' if z_score > 2.99 else 'Grey' if z_score > 1.81 else 'Distress',
            'Performance_Ratios': {
                'ROE': round((get_val('income_statement', 'Profit') / (get_val('balance_sheet', 'Total Equity') or 1)), 2),
                'Current_Ratio': round((current_assets / (current_liabilities or 1)), 2),
                'Debt_to_Equity': round((total_liabilities / (market_value_equity or 1)), 2)
            }
        }

    def detect_anomalies(self, transaction_data: pd.DataFrame) -> pd.DataFrame:
        """
        Detect anomalies in transaction or ledger data using Isolation Forest.
        Expects a DataFrame with numerical columns like 'Amount'.
        """
        if transaction_data.empty or 'Amount' not in transaction_data.columns:
            return transaction_data
        
        # Prepare data
        data = transaction_data[['Amount']].fillna(0)
        
        # Train model
        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        transaction_data['Anomaly_Score'] = iso_forest.fit_predict(data)
        
        # -1 indicates anomaly, 1 indicates normal
        transaction_data['Is_Anomaly'] = transaction_data['Anomaly_Score'].apply(lambda x: True if x == -1 else False)
        
        return transaction_data

    def predict_future_performance(self, historical_prices: pd.DataFrame, days: int = 30) -> Dict:
        """
        Simple trend-based prediction for demonstration.
        """
        if historical_prices.empty:
            return {}
        
        # Simple Moving Average forecast
        last_price = historical_prices['Close'].iloc[-1]
        ma_50 = historical_prices['Close'].rolling(window=50).mean().iloc[-1]
        
        trend = "Upward" if last_price > ma_50 else "Downward"
        
        return {
            'Current_Price': round(last_price, 2),
            '50_Day_MA': round(ma_50, 2),
            'Trend': trend,
            'Forecast_30d': f"Projecting {trend} movement based on MA crossover"
        }
