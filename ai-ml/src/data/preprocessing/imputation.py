"""
Missing Value Imputation
Module for handling missing values in datasets
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from typing import List, Optional, Union
import logging

logger = logging.getLogger(__name__)


def mean_imputation(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Impute missing values using mean for numerical columns
    
    Args:
        df: Input DataFrame
        columns: List of columns to impute
        
    Returns:
        DataFrame with imputed values
    """
    df_imputed = df.copy()
    
    for col in columns:
        if col in df_imputed.columns:
            imputer = SimpleImputer(strategy='mean')
            df_imputed[col] = imputer.fit_transform(df_imputed[[col]])
            logger.info(f"Mean imputation applied to column: {col}")
    
    return df_imputed


def median_imputation(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Impute missing values using median for numerical columns
    
    Args:
        df: Input DataFrame
        columns: List of columns to impute
        
    Returns:
        DataFrame with imputed values
    """
    df_imputed = df.copy()
    
    for col in columns:
        if col in df_imputed.columns:
            imputer = SimpleImputer(strategy='median')
            df_imputed[col] = imputer.fit_transform(df_imputed[[col]])
            logger.info(f"Median imputation applied to column: {col}")
    
    return df_imputed


def mode_imputation(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Impute missing values using mode for categorical columns
    
    Args:
        df: Input DataFrame
        columns: List of columns to impute
        
    Returns:
        DataFrame with imputed values
    """
    df_imputed = df.copy()
    
    for col in columns:
        if col in df_imputed.columns:
            # For mode imputation, we can use pandas mode directly
            mode_value = df_imputed[col].mode()
            if not mode_value.empty:
                # Convert to Python native type to avoid issues
                fill_value = mode_value.iloc[0]
                df_imputed[col] = df_imputed[col].fillna(fill_value)
            logger.info(f"Mode imputation applied to column: {col}")
    
    return df_imputed


def forward_fill_imputation(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Impute missing values using forward fill (useful for time series)
    
    Args:
        df: Input DataFrame
        columns: List of columns to impute
        
    Returns:
        DataFrame with imputed values
    """
    df_imputed = df.copy()
    
    for col in columns:
        if col in df_imputed.columns:
            df_imputed[col] = df_imputed[col].fillna(method='ffill')
            logger.info(f"Forward fill imputation applied to column: {col}")
    
    return df_imputed


def backward_fill_imputation(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Impute missing values using backward fill (useful for time series)
    
    Args:
        df: Input DataFrame
        columns: List of columns to impute
        
    Returns:
        DataFrame with imputed values
    """
    df_imputed = df.copy()
    
    for col in columns:
        if col in df_imputed.columns:
            df_imputed[col] = df_imputed[col].fillna(method='bfill')
            logger.info(f"Backward fill imputation applied to column: {col}")
    
    return df_imputed


def knn_imputation(df: pd.DataFrame, columns: List[str], n_neighbors: int = 5) -> pd.DataFrame:
    """
    Impute missing values using KNN imputation
    
    Args:
        df: Input DataFrame
        columns: List of columns to impute
        n_neighbors: Number of neighbors to use for imputation
        
    Returns:
        DataFrame with imputed values
    """
    df_imputed = df.copy()
    
    # Select only the columns to impute
    df_subset = df_imputed[columns]
    
    # Apply KNN imputation
    imputer = KNNImputer(n_neighbors=n_neighbors)
    df_imputed[columns] = imputer.fit_transform(df_subset)
    
    logger.info(f"KNN imputation applied to columns: {columns}")
    return df_imputed


def custom_value_imputation(df: pd.DataFrame, columns: List[str], fill_value) -> pd.DataFrame:
    """
    Impute missing values with a custom value
    
    Args:
        df: Input DataFrame
        columns: List of columns to impute
        fill_value: Value to use for imputation
        
    Returns:
        DataFrame with imputed values
    """
    df_imputed = df.copy()
    
    for col in columns:
        if col in df_imputed.columns:
            df_imputed[col] = df_imputed[col].fillna(fill_value)
            logger.info(f"Custom value imputation ({fill_value}) applied to column: {col}")
    
    return df_imputed


def impute_missing_values(df: pd.DataFrame, 
                         imputation_strategy: dict) -> pd.DataFrame:
    """
    Comprehensive missing value imputation pipeline
    
    Args:
        df: Input DataFrame
        imputation_strategy: Dictionary mapping columns to imputation strategies
                            Example: {
                                'mean_cols': ['col1', 'col2'],
                                'median_cols': ['col3'],
                                'mode_cols': ['col4'],
                                'knn_cols': ['col5', 'col6']
                            }
        
    Returns:
        DataFrame with imputed values
    """
    logger.info("Starting missing value imputation pipeline")
    df_imputed = df.copy()
    
    # Apply different imputation strategies
    if 'mean_cols' in imputation_strategy:
        df_imputed = mean_imputation(df_imputed, imputation_strategy['mean_cols'])
    
    if 'median_cols' in imputation_strategy:
        df_imputed = median_imputation(df_imputed, imputation_strategy['median_cols'])
    
    if 'mode_cols' in imputation_strategy:
        df_imputed = mode_imputation(df_imputed, imputation_strategy['mode_cols'])
    
    if 'forward_fill_cols' in imputation_strategy:
        df_imputed = forward_fill_imputation(df_imputed, imputation_strategy['forward_fill_cols'])
    
    if 'backward_fill_cols' in imputation_strategy:
        df_imputed = backward_fill_imputation(df_imputed, imputation_strategy['backward_fill_cols'])
    
    if 'knn_cols' in imputation_strategy:
        n_neighbors = imputation_strategy.get('knn_neighbors', 5)
        df_imputed = knn_imputation(df_imputed, imputation_strategy['knn_cols'], n_neighbors)
    
    if 'custom_cols' in imputation_strategy:
        fill_value = imputation_strategy.get('custom_value', 0)
        custom_cols = imputation_strategy['custom_cols']
        df_imputed = custom_value_imputation(df_imputed, custom_cols, fill_value)
    
    logger.info("Missing value imputation pipeline completed")
    return df_imputed