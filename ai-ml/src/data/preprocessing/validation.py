import pandas as pd
from typing import Dict

def validate_data(df: pd.DataFrame, config: Dict) -> Dict:
    results = {"is_valid": True, "issues": [], "stats": {"total_rows": len(df), "total_columns": len(df.columns)}}
    schema = config.get('schema', {})
    ranges = config.get('ranges', {})
    for col in schema:
        if col not in df.columns:
            results["issues"].append(f"Missing column: {col}")
            results["is_valid"] = False
    for col, limits in ranges.items():
        if col in df.columns:
            if 'min' in limits and df[col].dtype in ['int64', 'float64']:
                if (df[col] < limits['min']).any():
                    results["issues"].append(f"Column {col} has values below {limits['min']}")
                    results["is_valid"] = False
            if 'max' in limits and df[col].dtype in ['int64', 'float64']:
                if (df[col] > limits['max']).any():
                    results["issues"].append(f"Column {col} has values above {limits['max']}")
                    results["is_valid"] = False
    return results
