"""
Data Normalization and Scaling
Module for normalizing and scaling numerical data
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, Normalizer
from typing import List, Optional, Union
import logging

logger = logging.getLogger(__name__)


def min_max_scaling(df: pd.DataFrame, columns: List[str], feature_range: tuple = (0, 1)) -> pd.DataFrame:
    """
    Apply Min-Max scaling to specified columns
    
    Args:
        df: Input DataFrame
        columns: List of columns to scale
        feature_range: Tuple of (min, max) for scaling range
        
    Returns:
        DataFrame with Min-Max scaled columns
    """
    df_scaled = df.copy()
    
    # Select only the specified columns
    df_subset = df_scaled[columns]
    
    # Apply Min-Max scaling
    scaler = MinMaxScaler(feature_range=feature_range)
    df_scaled[columns] = scaler.fit_transform(df_subset)
    
    logger.info(f"Min-Max scaling applied to columns: {columns}")
    return df_scaled


def standard_scaling(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Apply Standard scaling (Z-score normalization) to specified columns
    
    Args:
        df: Input DataFrame
        columns: List of columns to scale
        
    Returns:
        DataFrame with Standard scaled columns
    """
    df_scaled = df.copy()
    
    # Select only the specified columns
    df_subset = df_scaled[columns]
    
    # Apply Standard scaling
    scaler = StandardScaler()
    df_scaled[columns] = scaler.fit_transform(df_subset)
    
    logger.info(f"Standard scaling applied to columns: {columns}")
    return df_scaled


def robust_scaling(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Apply Robust scaling to specified columns (uses median and IQR)
    
    Args:
        df: Input DataFrame
        columns: List of columns to scale
        
    Returns:
        DataFrame with Robust scaled columns
    """
    df_scaled = df.copy()
    
    # Select only the specified columns
    df_subset = df_scaled[columns]
    
    # Apply Robust scaling
    scaler = RobustScaler()
    df_scaled[columns] = scaler.fit_transform(df_subset)
    
    logger.info(f"Robust scaling applied to columns: {columns}")
    return df_scaled


def unit_vector_scaling(df: pd.DataFrame, columns: List[str], norm: str = 'l2') -> pd.DataFrame:
    """
    Apply Unit Vector scaling (Normalization) to specified columns
    
    Args:
        df: Input DataFrame
        columns: List of columns to scale
        norm: Normalization type ('l1', 'l2', 'max')
        
    Returns:
        DataFrame with Unit Vector scaled columns
    """
    df_scaled = df.copy()
    
    # Select only the specified columns
    df_subset = df_scaled[columns]
    
    # Apply Unit Vector scaling
    scaler = Normalizer(norm=norm)
    df_scaled[columns] = scaler.fit_transform(df_subset)
    
    logger.info(f"Unit vector scaling ({norm}) applied to columns: {columns}")
    return df_scaled


def custom_scaling(df: pd.DataFrame, columns: List[str], scale_factor: float = 1.0) -> pd.DataFrame:
    """
    Apply custom scaling by multiplying with a factor
    
    Args:
        df: Input DataFrame
        columns: List of columns to scale
        scale_factor: Factor to multiply with
        
    Returns:
        DataFrame with custom scaled columns
    """
    df_scaled = df.copy()
    
    for col in columns:
        if col in df_scaled.columns:
            df_scaled[col] = df_scaled[col] * scale_factor
            logger.info(f"Custom scaling (factor: {scale_factor}) applied to column: {col}")
    
    return df_scaled


def normalize_data(df: pd.DataFrame, 
                  normalization_config: dict) -> pd.DataFrame:
    """
    Comprehensive data normalization pipeline
    
    Args:
        df: Input DataFrame
        normalization_config: Dictionary specifying normalization strategies
                             Example: {
                                 'min_max_cols': ['col1', 'col2'],
                                 'standard_cols': ['col3'],
                                 'robust_cols': ['col4'],
                                 'unit_vector_cols': ['col5', 'col6']
                             }
        
    Returns:
        Normalized DataFrame
    """
    logger.info("Starting data normalization pipeline")
    df_normalized = df.copy()
    
    # Apply different normalization strategies
    if 'min_max_cols' in normalization_config:
        feature_range = normalization_config.get('min_max_range', (0, 1))
        df_normalized = min_max_scaling(
            df_normalized, 
            normalization_config['min_max_cols'], 
            feature_range
        )
    
    if 'standard_cols' in normalization_config:
        df_normalized = standard_scaling(
            df_normalized, 
            normalization_config['standard_cols']
        )
    
    if 'robust_cols' in normalization_config:
        df_normalized = robust_scaling(
            df_normalized, 
            normalization_config['robust_cols']
        )
    
    if 'unit_vector_cols' in normalization_config:
        norm_type = normalization_config.get('unit_vector_norm', 'l2')
        df_normalized = unit_vector_scaling(
            df_normalized, 
            normalization_config['unit_vector_cols'], 
            norm_type
        )
    
    if 'custom_cols' in normalization_config:
        scale_factor = normalization_config.get('custom_scale_factor', 1.0)
        df_normalized = custom_scaling(
            df_normalized, 
            normalization_config['custom_cols'], 
            scale_factor
        )
    
    logger.info("Data normalization pipeline completed")
    return df_normalized