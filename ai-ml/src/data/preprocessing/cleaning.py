"""
Data Cleaning Algorithms
Module for cleaning and preprocessing raw data
"""

import pandas as pd
import numpy as np
import logging
from typing import List, Optional, Union

logger = logging.getLogger(__name__)


def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Remove duplicate rows from DataFrame
    
    Args:
        df: Input DataFrame
        subset: Optional list of columns to consider for duplicates
        
    Returns:
        DataFrame with duplicates removed
    """
    initial_rows = len(df)
    df_cleaned = df.drop_duplicates(subset=subset)
    removed_rows = initial_rows - len(df_cleaned)
    
    if removed_rows > 0:
        logger.info(f"Removed {removed_rows} duplicate rows")
    
    return df_cleaned


def clean_text_columns(df: pd.DataFrame, text_columns: List[str]) -> pd.DataFrame:
    """
    Clean text columns by removing special characters and normalizing case
    
    Args:
        df: Input DataFrame
        text_columns: List of column names to clean
        
    Returns:
        DataFrame with cleaned text columns
    """
    df_cleaned = df.copy()
    
    for col in text_columns:
        if col in df_cleaned.columns:
            # Remove leading/trailing whitespace
            df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
            
            # Convert to lowercase
            df_cleaned[col] = df_cleaned[col].str.lower()
            
            # Remove special characters (keep alphanumeric, spaces, and common punctuation)
            df_cleaned[col] = df_cleaned[col].str.replace(r'[^a-zA-Z0-9\s\-\_\.\,\!\?]', '', regex=True)
            
            logger.info(f"Cleaned text column: {col}")
    
    return df_cleaned


def validate_data_types(df: pd.DataFrame, expected_types: dict) -> pd.DataFrame:
    """
    Validate and convert data types
    
    Args:
        df: Input DataFrame
        expected_types: Dictionary mapping column names to expected data types
        
    Returns:
        DataFrame with validated data types
    """
    df_validated = df.copy()
    
    for col, expected_type in expected_types.items():
        if col in df_validated.columns:
            try:
                if expected_type == 'datetime':
                    df_validated[col] = pd.to_datetime(df_validated[col], errors='coerce')
                elif expected_type == 'numeric':
                    df_validated[col] = pd.to_numeric(df_validated[col], errors='coerce')
                else:
                    df_validated[col] = df_validated[col].astype(expected_type)
                    
                logger.info(f"Converted column {col} to {expected_type}")
            except Exception as e:
                logger.warning(f"Failed to convert column {col} to {expected_type}: {e}")
    
    return df_validated


def remove_invalid_entries(df: pd.DataFrame, validation_rules: dict) -> pd.DataFrame:
    """
    Remove entries that don't meet validation criteria
    
    Args:
        df: Input DataFrame
        validation_rules: Dictionary of validation rules for columns
        
    Returns:
        DataFrame with invalid entries removed
    """
    df_filtered = df.copy()
    initial_rows = len(df_filtered)
    
    for col, rule in validation_rules.items():
        if col in df_filtered.columns:
            if rule['type'] == 'range':
                # Remove values outside specified range
                lower_bound = rule.get('min', float('-inf'))
                upper_bound = rule.get('max', float('inf'))
                df_filtered = df_filtered[
                    (df_filtered[col] >= lower_bound) & 
                    (df_filtered[col] <= upper_bound)
                ]
            elif rule['type'] == 'whitelist':
                # Keep only values in whitelist
                whitelist = rule.get('values', [])
                df_filtered = df_filtered[df_filtered[col].isin(whitelist)]
            elif rule['type'] == 'non_null':
                # Remove null values
                df_filtered = df_filtered.dropna(subset=[col])
    
    removed_rows = initial_rows - len(df_filtered)
    if removed_rows > 0:
        logger.info(f"Removed {removed_rows} invalid entries")
    
    return df_filtered


def clean_dataframe(df: pd.DataFrame, 
                   text_columns: Optional[List[str]] = None,
                   expected_types: Optional[dict] = None,
                   validation_rules: Optional[dict] = None,
                   remove_duplicates_subset: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Comprehensive data cleaning pipeline
    
    Args:
        df: Input DataFrame
        text_columns: List of text columns to clean
        expected_types: Dictionary of expected data types
        validation_rules: Dictionary of validation rules
        remove_duplicates_subset: Columns to consider for duplicate removal
        
    Returns:
        Cleaned DataFrame
    """
    logger.info("Starting comprehensive data cleaning pipeline")
    
    # Remove duplicates
    if remove_duplicates_subset is not None:
        df = remove_duplicates(df, subset=remove_duplicates_subset)
    
    # Clean text columns
    if text_columns:
        df = clean_text_columns(df, text_columns)
    
    # Validate data types
    if expected_types:
        df = validate_data_types(df, expected_types)
    
    # Remove invalid entries
    if validation_rules:
        df = remove_invalid_entries(df, validation_rules)
    
    logger.info("Data cleaning pipeline completed")
    return df