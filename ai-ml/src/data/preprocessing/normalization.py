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


def min_max_scaling(df, columns=None, feature_range=(0, 1)):
    result = df.copy()
    if columns is None:
        columns = result.select_dtypes(include='number').columns.tolist()
    else:
        missing = [c for c in columns if c not in result.columns]
        if missing:
            raise ValueError(f"Columns not found in DataFrame: {missing}")
    lo, hi = feature_range
    for col in columns:
        if result[col].dtype in ['int64', 'float64']:
            cmin, cmax = result[col].min(), result[col].max()
            if cmax == cmin:
                result[col] = lo
            else:
                result[col] = lo + (result[col] - cmin) * (hi - lo) / (cmax - cmin)
    return result
