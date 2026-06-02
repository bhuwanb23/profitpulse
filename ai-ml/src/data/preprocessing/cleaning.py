import pandas as pd

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result = result.drop_duplicates()
    result = result.dropna()
    return result
