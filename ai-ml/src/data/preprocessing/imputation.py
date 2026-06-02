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
