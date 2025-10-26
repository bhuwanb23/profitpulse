"""
Outlier Detection and Removal
Module for detecting and removing outliers and anomalies in datasets
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Tuple, Union
import logging

logger = logging.getLogger(__name__)


def zscore_outlier_detection(df: pd.DataFrame, 
                            columns: List[str], 
                            threshold: float = 3.0) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detect outliers using Z-score method
    
    Args:
        df: Input DataFrame
        columns: List of columns to check for outliers
        threshold: Z-score threshold for outlier detection
        
    Returns:
        Tuple of (cleaned DataFrame, outliers DataFrame)
    """
    df_cleaned = df.copy()
    outliers_list = []
    
    for col in columns:
        if col in df_cleaned.columns:
            # Calculate Z-scores
            z_scores = np.abs((df_cleaned[col] - df_cleaned[col].mean()) / df_cleaned[col].std())
            
            # Identify outliers
            outlier_mask = z_scores > threshold
            outliers = df_cleaned[outlier_mask]
            outliers_list.append(outliers)
            
            # Remove outliers
            df_cleaned = df_cleaned[~outlier_mask]
            
            logger.info(f"Z-score outlier detection: Removed {outlier_mask.sum()} outliers from {col}")
    
    # Combine all outliers
    if outliers_list:
        outliers_combined = pd.concat(outliers_list, ignore_index=True)
    else:
        outliers_combined = pd.DataFrame()
    
    return df_cleaned, outliers_combined


def iqr_outlier_detection(df: pd.DataFrame, 
                         columns: List[str], 
                         multiplier: float = 1.5) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detect outliers using Interquartile Range (IQR) method
    
    Args:
        df: Input DataFrame
        columns: List of columns to check for outliers
        multiplier: IQR multiplier for outlier detection
        
    Returns:
        Tuple of (cleaned DataFrame, outliers DataFrame)
    """
    df_cleaned = df.copy()
    outliers_list = []
    
    for col in columns:
        if col in df_cleaned.columns:
            # Calculate Q1, Q3, and IQR
            Q1 = df_cleaned[col].quantile(0.25)
            Q3 = df_cleaned[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define outlier bounds
            lower_bound = Q1 - multiplier * IQR
            upper_bound = Q3 + multiplier * IQR
            
            # Identify outliers
            outlier_mask = (df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound)
            outliers = df_cleaned[outlier_mask]
            outliers_list.append(outliers)
            
            # Remove outliers
            df_cleaned = df_cleaned[~outlier_mask]
            
            logger.info(f"IQR outlier detection: Removed {outlier_mask.sum()} outliers from {col}")
    
    # Combine all outliers
    if outliers_list:
        outliers_combined = pd.concat(outliers_list, ignore_index=True)
    else:
        outliers_combined = pd.DataFrame()
    
    return df_cleaned, outliers_combined


def percentile_outlier_detection(df: pd.DataFrame, 
                               columns: List[str], 
                               lower_percentile: float = 1.0, 
                               upper_percentile: float = 99.0) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detect outliers using percentile method
    
    Args:
        df: Input DataFrame
        columns: List of columns to check for outliers
        lower_percentile: Lower percentile threshold
        upper_percentile: Upper percentile threshold
        
    Returns:
        Tuple of (cleaned DataFrame, outliers DataFrame)
    """
    df_cleaned = df.copy()
    outliers_list = []
    
    for col in columns:
        if col in df_cleaned.columns:
            # Calculate percentile bounds
            lower_bound = df_cleaned[col].quantile(lower_percentile / 100)
            upper_bound = df_cleaned[col].quantile(upper_percentile / 100)
            
            # Identify outliers
            outlier_mask = (df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound)
            outliers = df_cleaned[outlier_mask]
            outliers_list.append(outliers)
            
            # Remove outliers
            df_cleaned = df_cleaned[~outlier_mask]
            
            logger.info(f"Percentile outlier detection: Removed {outlier_mask.sum()} outliers from {col}")
    
    # Combine all outliers
    if outliers_list:
        outliers_combined = pd.concat(outliers_list, ignore_index=True)
    else:
        outliers_combined = pd.DataFrame()
    
    return df_cleaned, outliers_combined


def isolation_forest_outlier_detection(df: pd.DataFrame, 
                                     columns: List[str], 
                                     contamination: float = 0.1) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detect outliers using Isolation Forest algorithm
    
    Args:
        df: Input DataFrame
        columns: List of columns to check for outliers
        contamination: Expected proportion of outliers in the dataset
        
    Returns:
        Tuple of (cleaned DataFrame, outliers DataFrame)
    """
    try:
        from sklearn.ensemble import IsolationForest
    except ImportError:
        logger.warning("scikit-learn not installed. Skipping Isolation Forest outlier detection.")
        return df, pd.DataFrame()
    
    df_cleaned = df.copy()
    
    # Select only the specified columns
    df_subset = df_cleaned[columns].dropna()
    
    # Apply Isolation Forest
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    outlier_labels = iso_forest.fit_predict(df_subset)
    
    # Identify outliers (labeled as -1)
    outlier_mask = outlier_labels == -1
    outliers = df_subset[outlier_mask]
    
    # Remove outliers from original dataframe
    # This is a bit tricky since we need to match indices
    outlier_indices = df_subset[outlier_mask].index
    df_cleaned = df_cleaned.drop(outlier_indices)
    
    logger.info(f"Isolation Forest outlier detection: Removed {outlier_mask.sum()} outliers")
    
    return df_cleaned, outliers


def remove_outliers(df: pd.DataFrame, 
                   outlier_strategy: dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Comprehensive outlier detection and removal pipeline
    
    Args:
        df: Input DataFrame
        outlier_strategy: Dictionary specifying outlier detection strategies
                         Example: {
                             'zscore_cols': ['col1', 'col2'],
                             'iqr_cols': ['col3'],
                             'percentile_cols': ['col4'],
                             'isolation_forest_cols': ['col5', 'col6']
                         }
        
    Returns:
        Tuple of (cleaned DataFrame, outliers DataFrame)
    """
    logger.info("Starting outlier detection and removal pipeline")
    df_cleaned = df.copy()
    all_outliers = []
    
    # Apply different outlier detection strategies
    if 'zscore_cols' in outlier_strategy:
        threshold = outlier_strategy.get('zscore_threshold', 3.0)
        df_cleaned, zscore_outliers = zscore_outlier_detection(
            df_cleaned, 
            outlier_strategy['zscore_cols'], 
            threshold
        )
        if not zscore_outliers.empty:
            all_outliers.append(zscore_outliers)
    
    if 'iqr_cols' in outlier_strategy:
        multiplier = outlier_strategy.get('iqr_multiplier', 1.5)
        df_cleaned, iqr_outliers = iqr_outlier_detection(
            df_cleaned, 
            outlier_strategy['iqr_cols'], 
            multiplier
        )
        if not iqr_outliers.empty:
            all_outliers.append(iqr_outliers)
    
    if 'percentile_cols' in outlier_strategy:
        lower_percentile = outlier_strategy.get('lower_percentile', 1.0)
        upper_percentile = outlier_strategy.get('upper_percentile', 99.0)
        df_cleaned, percentile_outliers = percentile_outlier_detection(
            df_cleaned, 
            outlier_strategy['percentile_cols'], 
            lower_percentile, 
            upper_percentile
        )
        if not percentile_outliers.empty:
            all_outliers.append(percentile_outliers)
    
    if 'isolation_forest_cols' in outlier_strategy:
        contamination = outlier_strategy.get('contamination', 0.1)
        df_cleaned, iso_forest_outliers = isolation_forest_outlier_detection(
            df_cleaned, 
            outlier_strategy['isolation_forest_cols'], 
            contamination
        )
        if not iso_forest_outliers.empty:
            all_outliers.append(iso_forest_outliers)
    
    # Combine all outliers
    if all_outliers:
        outliers_combined = pd.concat(all_outliers, ignore_index=True)
    else:
        outliers_combined = pd.DataFrame()
    
    logger.info("Outlier detection and removal pipeline completed")
    return df_cleaned, outliers_combined