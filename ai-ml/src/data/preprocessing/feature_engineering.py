import pandas as pd
from typing import Dict
from datetime import datetime

def engineer_features(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    result = df.copy()
    if 'billing_amount' in result.columns and 'hours_logged' in result.columns:
        result['revenue_per_hour'] = result['billing_amount'] / (result['hours_logged'] + 1e-6)
    if 'created_at' in result.columns:
        created = pd.to_datetime(result['created_at'], errors='coerce')
        result['ticket_age_days'] = (datetime.now() - created).dt.days
    if 'created_at' in result.columns and 'resolved_at' in result.columns:
        created = pd.to_datetime(result['created_at'], errors='coerce')
        resolved = pd.to_datetime(result['resolved_at'], errors='coerce')
        result['resolution_time_hours'] = (resolved - created).dt.total_seconds() / 3600
        result['resolution_time_hours'] = result['resolution_time_hours'].clip(lower=0)
    if 'contract_value' in result.columns:
        result['client_value_tier'] = pd.cut(
            result['contract_value'],
            bins=[0, 5000, 15000, 50000, float('inf')],
            labels=['Bronze', 'Silver', 'Gold', 'Platinum']
        )
    return result
