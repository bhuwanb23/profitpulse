import pandas as pd

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result = result.drop_duplicates()
    result = result.dropna()
    return result


def remove_duplicates(df, subset=None, keep='first'):
    return df.drop_duplicates(subset=subset, keep=keep)
