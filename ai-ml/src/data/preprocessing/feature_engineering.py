"""
Feature Engineering
Module for creating new features and transforming existing ones
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from typing import List, Dict, Optional, Union, Tuple, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def one_hot_encoding(df: pd.DataFrame, columns: List[str], drop_first: bool = False) -> pd.DataFrame:
    """
    Apply one-hot encoding to categorical columns
    
    Args:
        df: Input DataFrame
        columns: List of columns to encode
        drop_first: Whether to drop the first category to avoid multicollinearity
        
    Returns:
        DataFrame with one-hot encoded columns
    """
    df_encoded = df.copy()
    
    # Select only the specified columns
    df_subset = df_encoded[columns]
    
    # Apply one-hot encoding
    encoder = OneHotEncoder(drop='first' if drop_first else None, sparse_output=False)
    encoded_array = encoder.fit_transform(df_subset)
    
    # Get feature names
    feature_names = encoder.get_feature_names_out(columns)
    
    # Create DataFrame with encoded features
    encoded_df = pd.DataFrame(encoded_array, columns=feature_names, index=df_encoded.index)
    
    # Remove original columns and add encoded columns
    df_encoded = df_encoded.drop(columns=columns)
    df_encoded = pd.concat([df_encoded, encoded_df], axis=1)
    
    logger.info(f"One-hot encoding applied to columns: {columns}")
    return df_encoded


def label_encoding(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Apply label encoding to categorical columns
    
    Args:
        df: Input DataFrame
        columns: List of columns to encode
        
    Returns:
        DataFrame with label encoded columns
    """
    df_encoded = df.copy()
    
    for col in columns:
        if col in df_encoded.columns:
            # Apply label encoding
            encoder = LabelEncoder()
            df_encoded[col] = encoder.fit_transform(df_encoded[col].astype(str))
            logger.info(f"Label encoding applied to column: {col}")
    
    return df_encoded


def create_time_based_features(df: pd.DataFrame, 
                             datetime_column: str,
                             include_features: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Create time-based features from a datetime column
    
    Args:
        df: Input DataFrame
        datetime_column: Name of the datetime column
        include_features: List of features to create (default: all)
        
    Returns:
        DataFrame with time-based features
    """
    if include_features is None:
        include_features = [
            'year', 'month', 'day', 'dayofweek', 'dayofyear', 
            'weekofyear', 'quarter', 'hour', 'minute', 'second',
            'is_weekend', 'is_month_start', 'is_month_end'
        ]
    
    df_features = df.copy()
    
    if datetime_column in df_features.columns:
        # Convert to datetime if not already
        df_features[datetime_column] = pd.to_datetime(df_features[datetime_column])
        
        dt_series = df_features[datetime_column]
        
        # Create time-based features
        if 'year' in include_features:
            df_features[f'{datetime_column}_year'] = dt_series.dt.year
        if 'month' in include_features:
            df_features[f'{datetime_column}_month'] = dt_series.dt.month
        if 'day' in include_features:
            df_features[f'{datetime_column}_day'] = dt_series.dt.day
        if 'dayofweek' in include_features:
            df_features[f'{datetime_column}_dayofweek'] = dt_series.dt.dayofweek
        if 'dayofyear' in include_features:
            df_features[f'{datetime_column}_dayofyear'] = dt_series.dt.dayofyear
        if 'weekofyear' in include_features:
            df_features[f'{datetime_column}_weekofyear'] = dt_series.dt.isocalendar().week
        if 'quarter' in include_features:
            df_features[f'{datetime_column}_quarter'] = dt_series.dt.quarter
        if 'hour' in include_features:
            df_features[f'{datetime_column}_hour'] = dt_series.dt.hour
        if 'minute' in include_features:
            df_features[f'{datetime_column}_minute'] = dt_series.dt.minute
        if 'second' in include_features:
            df_features[f'{datetime_column}_second'] = dt_series.dt.second
        if 'is_weekend' in include_features:
            df_features[f'{datetime_column}_is_weekend'] = dt_series.dt.dayofweek.isin([5, 6]).astype(int)
        if 'is_month_start' in include_features:
            df_features[f'{datetime_column}_is_month_start'] = dt_series.dt.is_month_start.astype(int)
        if 'is_month_end' in include_features:
            df_features[f'{datetime_column}_is_month_end'] = dt_series.dt.is_month_end.astype(int)
        
        logger.info(f"Time-based features created from column: {datetime_column}")
    
    return df_features


def create_ratio_features(df: pd.DataFrame, 
                         ratio_pairs: List[Tuple[str, str, str]]) -> pd.DataFrame:
    """
    Create ratio features from pairs of numerical columns
    
    Args:
        df: Input DataFrame
        ratio_pairs: List of tuples (numerator_col, denominator_col, new_feature_name)
        
    Returns:
        DataFrame with ratio features
    """
    df_features = df.copy()
    
    for numerator_col, denominator_col, new_feature_name in ratio_pairs:
        if numerator_col in df_features.columns and denominator_col in df_features.columns:
            # Avoid division by zero
            df_features[new_feature_name] = np.where(
                df_features[denominator_col] != 0,
                df_features[numerator_col] / df_features[denominator_col],
                np.nan
            )
            logger.info(f"Ratio feature created: {new_feature_name} = {numerator_col} / {denominator_col}")
    
    return df_features


def create_polynomial_features(df: pd.DataFrame, 
                             columns: List[str], 
                             degree: int = 2) -> pd.DataFrame:
    """
    Create polynomial features from numerical columns
    
    Args:
        df: Input DataFrame
        columns: List of columns to create polynomial features from
        degree: Degree of polynomial features
        
    Returns:
        DataFrame with polynomial features
    """
    df_features = df.copy()
    
    for col in columns:
        if col in df_features.columns:
            for i in range(2, degree + 1):
                new_col_name = f"{col}_pow_{i}"
                df_features[new_col_name] = df_features[col] ** i
                logger.info(f"Polynomial feature created: {new_col_name}")
    
    return df_features


def create_interaction_features(df: pd.DataFrame, 
                              interaction_pairs: List[Tuple[str, str, str]]) -> pd.DataFrame:
    """
    Create interaction features (multiplication) from pairs of columns
    
    Args:
        df: Input DataFrame
        interaction_pairs: List of tuples (col1, col2, new_feature_name)
        
    Returns:
        DataFrame with interaction features
    """
    df_features = df.copy()
    
    for col1, col2, new_feature_name in interaction_pairs:
        if col1 in df_features.columns and col2 in df_features.columns:
            df_features[new_feature_name] = df_features[col1] * df_features[col2]
            logger.info(f"Interaction feature created: {new_feature_name} = {col1} * {col2}")
    
    return df_features


def create_binned_features(df: pd.DataFrame, 
                          binning_config: Dict[str, Dict]) -> pd.DataFrame:
    """
    Create binned features from numerical columns
    
    Args:
        df: Input DataFrame
        binning_config: Dictionary mapping column names to binning parameters
                       Example: {'age': {'bins': 5, 'labels': ['Young', 'Adult', 'Middle', 'Senior', 'Elderly']}}
        
    Returns:
        DataFrame with binned features
    """
    df_features = df.copy()
    
    for col, params in binning_config.items():
        if col in df_features.columns:
            bins = params.get('bins', 5)
            labels = params.get('labels', None)
            
            df_features[f"{col}_binned"] = pd.cut(
                df_features[col], 
                bins=bins, 
                labels=labels,
                include_lowest=True
            )
            logger.info(f"Binned feature created: {col}_binned")
    
    return df_features


def engineer_features(df: pd.DataFrame, 
                     feature_engineering_config: dict) -> pd.DataFrame:
    """
    Comprehensive feature engineering pipeline
    
    Args:
        df: Input DataFrame
        feature_engineering_config: Dictionary specifying feature engineering strategies
                                   Example: {
                                       'one_hot_cols': ['category1', 'category2'],
                                       'label_cols': ['category3'],
                                       'time_based_features': {'datetime_col': 'created_at'},
                                       'ratio_features': [('revenue', 'cost', 'profit_margin')],
                                       'polynomial_features': {'cols': ['value'], 'degree': 2},
                                       'interaction_features': [('price', 'quantity', 'total_value')],
                                       'binned_features': {'age': {'bins': 5}}
                                   }
        
    Returns:
        DataFrame with engineered features
    """
    logger.info("Starting feature engineering pipeline")
    df_engineered = df.copy()
    
    # Apply one-hot encoding
    if 'one_hot_cols' in feature_engineering_config:
        drop_first = feature_engineering_config.get('one_hot_drop_first', False)
        df_engineered = one_hot_encoding(
            df_engineered, 
            feature_engineering_config['one_hot_cols'], 
            drop_first
        )
    
    # Apply label encoding
    if 'label_cols' in feature_engineering_config:
        df_engineered = label_encoding(
            df_engineered, 
            feature_engineering_config['label_cols']
        )
    
    # Create time-based features
    if 'time_based_features' in feature_engineering_config:
        datetime_col = feature_engineering_config['time_based_features'].get('datetime_col')
        include_features = feature_engineering_config['time_based_features'].get('include_features')
        if datetime_col:
            df_engineered = create_time_based_features(
                df_engineered, 
                datetime_col, 
                include_features
            )
    
    # Create ratio features
    if 'ratio_features' in feature_engineering_config:
        df_engineered = create_ratio_features(
            df_engineered, 
            feature_engineering_config['ratio_features']
        )
    
    # Create polynomial features
    if 'polynomial_features' in feature_engineering_config:
        poly_config = feature_engineering_config['polynomial_features']
        cols = poly_config.get('cols', [])
        degree = poly_config.get('degree', 2)
        df_engineered = create_polynomial_features(
            df_engineered, 
            cols, 
            degree
        )
    
    # Create interaction features
    if 'interaction_features' in feature_engineering_config:
        df_engineered = create_interaction_features(
            df_engineered, 
            feature_engineering_config['interaction_features']
        )
    
    # Create binned features
    if 'binned_features' in feature_engineering_config:
        df_engineered = create_binned_features(
            df_engineered, 
            feature_engineering_config['binned_features']
        )
    
    logger.info("Feature engineering pipeline completed")
    return df_engineered