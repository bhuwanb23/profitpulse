"""
Data Aggregation
Module for aggregating data across different dimensions
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union, Callable, Any
import logging

logger = logging.getLogger(__name__)


def groupby_aggregation(df: pd.DataFrame, 
                       groupby_columns: List[str],
                       aggregation_functions: Dict[str, Union[str, List[str], Callable]]) -> pd.DataFrame:
    """
    Perform groupby aggregation on specified columns
    
    Args:
        df: Input DataFrame
        groupby_columns: List of columns to group by
        aggregation_functions: Dictionary mapping columns to aggregation functions
                              Example: {'sales': 'sum', 'quantity': ['mean', 'std']}
        
    Returns:
        Aggregated DataFrame
    """
    # Perform groupby aggregation
    aggregated_df = df.groupby(groupby_columns).agg(aggregation_functions).reset_index()
    
    logger.info(f"Groupby aggregation performed on columns: {groupby_columns}")
    return aggregated_df


def time_series_resampling(df: pd.DataFrame,
                          datetime_column: str,
                          resampling_frequency: str,
                          aggregation_functions: Dict[str, Union[str, List[str], Callable]]) -> pd.DataFrame:
    """
    Resample time series data to a different frequency
    
    Args:
        df: Input DataFrame
        datetime_column: Name of the datetime column
        resampling_frequency: Frequency for resampling (e.g., 'D', 'W', 'M', 'Q', 'Y')
        aggregation_functions: Dictionary mapping columns to aggregation functions
        
    Returns:
        Resampled DataFrame
    """
    # Set datetime column as index
    df_resampled = df.set_index(datetime_column)
    
    # Resample and aggregate
    df_resampled = df_resampled.resample(resampling_frequency).agg(aggregation_functions)
    
    # Reset index to make datetime a column again
    df_resampled = df_resampled.reset_index()
    
    logger.info(f"Time series resampled to {resampling_frequency} frequency")
    return df_resampled


def rolling_window_aggregation(df: pd.DataFrame,
                              groupby_columns: List[str],
                              value_columns: List[str],
                              window_size: int,
                              aggregation_functions: Union[str, List[str], Dict[str, str]]) -> pd.DataFrame:
    """
    Perform rolling window aggregation
    
    Args:
        df: Input DataFrame
        groupby_columns: List of columns to group by
        value_columns: List of columns to apply rolling aggregation to
        window_size: Size of the rolling window
        aggregation_functions: Aggregation functions to apply
        
    Returns:
        DataFrame with rolling window aggregations
    """
    df_rolling = df.copy()
    
    # Sort by groupby columns and any datetime column if present
    sort_columns = groupby_columns.copy()
    if 'date' in df_rolling.columns:
        sort_columns.append('date')
    elif 'datetime' in df_rolling.columns:
        sort_columns.append('datetime')
    
    df_rolling = df_rolling.sort_values(sort_columns)
    
    # Apply rolling window aggregation for each group
    for col in value_columns:
        if col in df_rolling.columns:
            for group_cols, group_df in df_rolling.groupby(groupby_columns):
                # Get indices for this group
                group_indices = group_df.index
                
                # Apply rolling window
                rolling_result = df_rolling.loc[group_indices, col].rolling(
                    window=window_size, 
                    min_periods=1
                ).agg(aggregation_functions)
                
                # Update the original dataframe
                df_rolling.loc[group_indices, f'{col}_rolling_{window_size}'] = rolling_result
    
    logger.info(f"Rolling window aggregation applied with window size {window_size}")
    return df_rolling


def pivot_table_aggregation(df: pd.DataFrame,
                           index_columns: List[str],
                           column_columns: List[str],
                           value_columns: List[str],
                           aggfunc: Any = 'mean') -> pd.DataFrame:
    """
    Create pivot table aggregation
    
    Args:
        df: Input DataFrame
        index_columns: Columns to use as index
        column_columns: Columns to use as columns
        value_columns: Columns to aggregate
        aggfunc: Aggregation function(s) to use
        
    Returns:
        Pivot table DataFrame
    """
    # Create pivot table
    pivot_df = df.pivot_table(
        index=index_columns,
        columns=column_columns,
        values=value_columns,
        aggfunc=aggfunc,
        fill_value=0
    )
    
    # Flatten column names if multi-level
    if isinstance(pivot_df.columns, pd.MultiIndex):
        pivot_df.columns = ['_'.join(col).strip() for col in pivot_df.columns.values]
    
    # Reset index to make index columns regular columns
    pivot_df = pivot_df.reset_index()
    
    logger.info("Pivot table aggregation created")
    return pivot_df


def custom_aggregation(df: pd.DataFrame,
                      groupby_columns: List[str],
                      custom_functions: Dict[str, Callable]) -> pd.DataFrame:
    """
    Apply custom aggregation functions
    
    Args:
        df: Input DataFrame
        groupby_columns: List of columns to group by
        custom_functions: Dictionary mapping column names to custom functions
        
    Returns:
        DataFrame with custom aggregations
    """
    # Apply custom aggregation functions
    aggregated_df = df.groupby(groupby_columns).agg(custom_functions).reset_index()
    
    logger.info("Custom aggregation applied")
    return aggregated_df


def aggregate_data(df: pd.DataFrame,
                  aggregation_config: dict) -> pd.DataFrame:
    """
    Comprehensive data aggregation pipeline
    
    Args:
        df: Input DataFrame
        aggregation_config: Dictionary specifying aggregation strategies
                           Example: {
                               'groupby': {
                                   'groupby_columns': ['category'],
                                   'aggregation_functions': {'sales': 'sum', 'quantity': 'mean'}
                               },
                               'resampling': {
                                   'datetime_column': 'date',
                                   'frequency': 'M',
                                   'aggregation_functions': {'sales': 'sum'}
                               },
                               'rolling': {
                                   'groupby_columns': ['category'],
                                   'value_columns': ['sales'],
                                   'window_size': 7,
                                   'aggregation_functions': 'mean'
                               }
                           }
        
    Returns:
        Aggregated DataFrame
    """
    logger.info("Starting data aggregation pipeline")
    df_aggregated = df.copy()
    
    # Apply groupby aggregation
    if 'groupby' in aggregation_config:
        groupby_config = aggregation_config['groupby']
        df_aggregated = groupby_aggregation(
            df_aggregated,
            groupby_config['groupby_columns'],
            groupby_config['aggregation_functions']
        )
    
    # Apply time series resampling
    if 'resampling' in aggregation_config:
        resampling_config = aggregation_config['resampling']
        df_aggregated = time_series_resampling(
            df_aggregated,
            resampling_config['datetime_column'],
            resampling_config['frequency'],
            resampling_config['aggregation_functions']
        )
    
    # Apply rolling window aggregation
    if 'rolling' in aggregation_config:
        rolling_config = aggregation_config['rolling']
        df_aggregated = rolling_window_aggregation(
            df_aggregated,
            rolling_config['groupby_columns'],
            rolling_config['value_columns'],
            rolling_config['window_size'],
            rolling_config['aggregation_functions']
        )
    
    # Apply pivot table aggregation
    if 'pivot' in aggregation_config:
        pivot_config = aggregation_config['pivot']
        df_aggregated = pivot_table_aggregation(
            df_aggregated,
            pivot_config['index_columns'],
            pivot_config['column_columns'],
            pivot_config['value_columns'],
            pivot_config.get('aggfunc', 'mean')
        )
    
    # Apply custom aggregation
    if 'custom' in aggregation_config:
        custom_config = aggregation_config['custom']
        df_aggregated = custom_aggregation(
            df_aggregated,
            custom_config['groupby_columns'],
            custom_config['custom_functions']
        )
    
    logger.info("Data aggregation pipeline completed")
    return df_aggregated