import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

class DataSourcer:
    """
    Simulates sourcing of data from external markets and regulatory bodies.
    """
    
    def __init__(self):
        pass
    
    def fetch_market_data(self, company_symbol: str, days: int = 365) -> pd.DataFrame:
        """
        Simulate fetching daily stock price data.
        """
        # Generate mock date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='B') # Business days
        
        # Simulate price movement with random walk
        np.random.seed(42)
        base_price = 1000.0
        returns = np.random.normal(0.001, 0.02, len(dates))
        prices = base_price * (1 + returns).cumprod()
        
        volumes = np.random.randint(10000, 1000000, len(dates))
        
        df = pd.DataFrame({
            'Date': dates,
            'Close': prices,
            'Volume': volumes,
            'Company': company_symbol
        })
        
        return df

    def fetch_audit_history(self, company_id: str) -> List[Dict]:
        """
        Simulate fetching audit history
        """
        return [
            {
                'Year': 2024,
                'Auditor': 'Big Firm LLP',
                'Opinion': 'Unmodified',
                'Remarks': 'None'
            },
            {
                'Year': 2023,
                'Auditor': 'Big Firm LLP',
                'Opinion': 'Unmodified',
                'Remarks': 'None'
            },
            {
                'Year': 2022,
                'Auditor': 'MidSize & Co',
                'Opinion': 'Qualified',
                'Remarks': 'Inventory valuation issue detected'
            }
        ]
    
    def fetch_governance_data(self, company_id: str) -> Dict:
        """
        Simulate fetching governance structure
        """
        return {
            'board_members': [
                {'name': 'Person A', 'role': 'Chairman', 'type': 'Promoter'},
                {'name': 'Person B', 'role': 'CEO', 'type': 'Executive'},
                {'name': 'Person C', 'role': 'Director', 'type': 'Independent'},
                {'name': 'Person D', 'role': 'Director', 'type': 'Independent'}
            ],
            'committees': {
                'Audit': ['Person C', 'Person D'],
                'Risk': ['Person B', 'Person C']
            }
        }
