import pandas as pd
from typing import Dict

def standardize_data(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    result = df.copy()
    text_columns = config.get('text_columns', [])
    for col in text_columns:
        if col in result.columns:
            result[col] = result[col].astype(str).str.strip().str.lower()
    currency_columns = config.get('currency_columns', [])
    for col in currency_columns:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors='coerce').round(2)
    return result
