import pandas as pd
from typing import Dict
from sklearn.preprocessing import StandardScaler

def normalize_data(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    standard_cols = config.get('standard_cols', [])
    result = df.copy()
    existing = [c for c in standard_cols if c in result.columns and result[c].dtype in ['int64', 'float64']]
    if existing:
        scaler = StandardScaler()
        result[existing] = scaler.fit_transform(result[existing])
    return result
