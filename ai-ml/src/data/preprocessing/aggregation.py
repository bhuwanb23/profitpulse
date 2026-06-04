import pandas as pd
from typing import Dict

def aggregate_data(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    return df


def groupby_aggregation(df, groupby_col, agg_col, agg_func='mean'):
    if df.empty:
        return df
    if groupby_col not in df.columns:
        raise ValueError(f"Column '{groupby_col}' not found in DataFrame")
    if agg_col not in df.columns:
        raise ValueError(f"Column '{agg_col}' not found in DataFrame")
    return df.groupby(groupby_col)[agg_col].agg(agg_func).reset_index()
