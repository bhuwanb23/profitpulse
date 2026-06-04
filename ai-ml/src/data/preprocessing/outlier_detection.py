import pandas as pd
import numpy as np
from typing import Dict, Tuple

def remove_outliers(df: pd.DataFrame, config: Dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    zscore_cols = config.get('zscore_cols', [])
    threshold = config.get('zscore_threshold', 3.0)
    outlier_mask = pd.Series(False, index=df.index)
    for col in zscore_cols:
        if col in df.columns and df[col].dtype in ['int64', 'float64']:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                zscores = np.abs((df[col] - mean) / std)
                outlier_mask = outlier_mask | (zscores > threshold)
    cleaned = df[~outlier_mask]
    outliers = df[outlier_mask]
    return cleaned, outliers


def zscore_outlier_detection(df, columns=None, threshold=3):
    result = pd.Series(False, index=df.index)
    if columns is None:
        columns = df.select_dtypes(include='number').columns.tolist()
    else:
        missing = [c for c in columns if c not in df.columns]
        if missing:
            raise ValueError(f"Columns not found in DataFrame: {missing}")
    for col in columns:
        if df[col].dtype in ['int64', 'float64']:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                zscores = np.abs((df[col] - mean) / std)
                result = result | (zscores > threshold)
    return result
