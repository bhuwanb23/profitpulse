"""
Data Standardization
Module for standardizing data formats, currencies, and units
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union, Callable
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def standardize_datetime_columns(df: pd.DataFrame, 
                               datetime_columns: Dict[str, str]) -> pd.DataFrame:
    """
    Standardize datetime columns to a consistent format
    
    Args:
        df: Input DataFrame
        datetime_columns: Dictionary mapping column names to desired format
                         Example: {'date_col': '%Y-%m-%d', 'datetime_col': '%Y-%m-%d %H:%M:%S'}
        
    Returns:
        DataFrame with standardized datetime columns
    """
    df_standardized = df.copy()
    
    for col, format_str in datetime_columns.items():
        if col in df_standardized.columns:
            try:
                # Convert to datetime
                df_standardized[col] = pd.to_datetime(df_standardized[col], errors='coerce')
                
                # Format to string if needed
                if format_str:
                    df_standardized[col] = df_standardized[col].dt.strftime(format_str)
                
                logger.info(f"Standardized datetime column: {col}")
            except Exception as e:
                logger.warning(f"Failed to standardize datetime column {col}: {e}")
    
    return df_standardized


def standardize_currency_columns(df: pd.DataFrame, 
                               currency_columns: List[str]) -> pd.DataFrame:
    """
    Standardize currency columns to float values (remove currency symbols)
    
    Args:
        df: Input DataFrame
        currency_columns: List of columns containing currency values
        
    Returns:
        DataFrame with standardized currency columns
    """
    df_standardized = df.copy()
    
    for col in currency_columns:
        if col in df_standardized.columns:
            try:
                # Remove currency symbols and convert to float
                df_standardized[col] = (
                    df_standardized[col]
                    .astype(str)
                    .str.replace(r'[\$,€,£,¥,₹]', '', regex=True)  # Remove common currency symbols
                    .str.replace(r'[^\d\.]', '', regex=True)      # Keep only digits and decimal points
                    .replace('', np.nan)                          # Replace empty strings with NaN
                    .astype(float)
                )
                
                logger.info(f"Standardized currency column: {col}")
            except Exception as e:
                logger.warning(f"Failed to standardize currency column {col}: {e}")
    
    return df_standardized


def standardize_categorical_values(df: pd.DataFrame, 
                                 categorical_mappings: Dict[str, Dict[str, str]]) -> pd.DataFrame:
    """
    Standardize categorical values using mapping dictionaries
    
    Args:
        df: Input DataFrame
        categorical_mappings: Dictionary mapping column names to value mappings
                             Example: {'status': {'active': 'Active', 'inactive': 'Inactive'}}
        
    Returns:
        DataFrame with standardized categorical values
    """
    df_standardized = df.copy()
    
    for col, mapping in categorical_mappings.items():
        if col in df_standardized.columns:
            try:
                # Apply mapping
                df_standardized[col] = df_standardized[col].replace(mapping)
                logger.info(f"Standardized categorical column: {col}")
            except Exception as e:
                logger.warning(f"Failed to standardize categorical column {col}: {e}")
    
    return df_standardized


def standardize_text_columns(df: pd.DataFrame, 
                           text_columns: List[str]) -> pd.DataFrame:
    """
    Standardize text columns (trim whitespace, convert to consistent case)
    
    Args:
        df: Input DataFrame
        text_columns: List of text columns to standardize
        
    Returns:
        DataFrame with standardized text columns
    """
    df_standardized = df.copy()
    
    for col in text_columns:
        if col in df_standardized.columns:
            try:
                # Trim whitespace and convert to title case
                df_standardized[col] = (
                    df_standardized[col]
                    .astype(str)
                    .str.strip()
                    .str.title()
                )
                
                logger.info(f"Standardized text column: {col}")
            except Exception as e:
                logger.warning(f"Failed to standardize text column {col}: {e}")
    
    return df_standardized


def convert_units(df: pd.DataFrame, 
                 unit_conversions: Dict[str, Dict]) -> pd.DataFrame:
    """
    Convert units in numerical columns
    
    Args:
        df: Input DataFrame
        unit_conversions: Dictionary mapping column names to conversion parameters
                         Example: {'weight_lbs': {'from_unit': 'lbs', 'to_unit': 'kg', 'conversion_factor': 0.453592}}
        
    Returns:
        DataFrame with converted units
    """
    df_standardized = df.copy()
    
    for col, conversion_params in unit_conversions.items():
        if col in df_standardized.columns:
            try:
                from_unit = conversion_params.get('from_unit', '')
                to_unit = conversion_params.get('to_unit', '')
                conversion_factor = conversion_params.get('conversion_factor', 1.0)
                
                # Apply conversion
                df_standardized[col] = df_standardized[col] * conversion_factor
                
                logger.info(f"Converted {col} from {from_unit} to {to_unit} using factor {conversion_factor}")
            except Exception as e:
                logger.warning(f"Failed to convert units for column {col}: {e}")
    
    return df_standardized


def standardize_data(df: pd.DataFrame, 
                    standardization_config: dict) -> pd.DataFrame:
    """
    Comprehensive data standardization pipeline
    
    Args:
        df: Input DataFrame
        standardization_config: Dictionary containing standardization configurations
                               Example: {
                                   'datetime_columns': {'date_col': '%Y-%m-%d'},
                                   'currency_columns': ['amount', 'price'],
                                   'categorical_mappings': {'status': {'1': 'Active', '0': 'Inactive'}},
                                   'text_columns': ['name', 'description'],
                                   'unit_conversions': {'weight': {'from_unit': 'lbs', 'to_unit': 'kg', 'conversion_factor': 0.453592}}
                               }
        
    Returns:
        Standardized DataFrame
    """
    logger.info("Starting data standardization pipeline")
    df_standardized = df.copy()
    
    # Standardize datetime columns
    if 'datetime_columns' in standardization_config:
        df_standardized = standardize_datetime_columns(
            df_standardized, 
            standardization_config['datetime_columns']
        )
    
    # Standardize currency columns
    if 'currency_columns' in standardization_config:
        df_standardized = standardize_currency_columns(
            df_standardized, 
            standardization_config['currency_columns']
        )
    
    # Standardize categorical values
    if 'categorical_mappings' in standardization_config:
        df_standardized = standardize_categorical_values(
            df_standardized, 
            standardization_config['categorical_mappings']
        )
    
    # Standardize text columns
    if 'text_columns' in standardization_config:
        df_standardized = standardize_text_columns(
            df_standardized, 
            standardization_config['text_columns']
        )
    
    # Convert units
    if 'unit_conversions' in standardization_config:
        df_standardized = convert_units(
            df_standardized, 
            standardization_config['unit_conversions']
        )
    
    logger.info("Data standardization pipeline completed")
    return df_standardized