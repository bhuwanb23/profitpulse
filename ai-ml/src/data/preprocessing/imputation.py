import pandas as pd
from typing import Dict

def impute_missing_values(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    result = df.copy()
    for column in result.columns:
        if result[column].dtype in ['int64', 'float64']:
            result[column] = result[column].fillna(result[column].median())
        elif result[column].dtype == 'object':
            result[column] = result[column].fillna('Unknown')
        elif result[column].dtype == 'datetime64[ns]':
            result[column] = result[column].ffill()
    return result


def mean_imputation(df, columns=None):
    result = df.copy()
    if columns is None:
        columns = result.select_dtypes(include='number').columns.tolist()
    else:
        missing = [c for c in columns if c not in result.columns]
        if missing:
            raise ValueError(f"Columns not found in DataFrame: {missing}")
    for col in columns:
        if result[col].dtype in ['int64', 'float64']:
            result[col] = result[col].fillna(result[col].mean())
    return result
