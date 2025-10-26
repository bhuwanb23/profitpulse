"""
Data Validation
Module for validating data quality and integrity
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union, Tuple
import logging

logger = logging.getLogger(__name__)


def validate_data_schema(df: pd.DataFrame, 
                        expected_schema: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Validate DataFrame schema against expected schema
    
    Args:
        df: Input DataFrame
        expected_schema: Dictionary mapping column names to expected data types
        
    Returns:
        Dictionary with validation results
    """
    validation_results = {
        'missing_columns': [],
        'extra_columns': [],
        'type_mismatches': [],
        'validation_passed': True
    }
    
    # Check for missing columns
    missing_columns = set(expected_schema.keys()) - set(df.columns)
    validation_results['missing_columns'] = list(missing_columns)
    
    # Check for extra columns
    extra_columns = set(df.columns) - set(expected_schema.keys())
    validation_results['extra_columns'] = list(extra_columns)
    
    # Check data types
    for col, expected_type in expected_schema.items():
        if col in df.columns:
            try:
                # Try to convert to expected type
                if expected_type == 'datetime':
                    pd.to_datetime(df[col], errors='raise')
                elif expected_type == 'numeric':
                    pd.to_numeric(df[col], errors='raise')
                else:
                    df[col].astype(expected_type)
            except Exception:
                validation_results['type_mismatches'].append(col)
                validation_results['validation_passed'] = False
    
    # Update validation status
    if missing_columns or extra_columns or validation_results['type_mismatches']:
        validation_results['validation_passed'] = False
    
    logger.info(f"Schema validation completed. Passed: {validation_results['validation_passed']}")
    return validation_results


def validate_data_ranges(df: pd.DataFrame, 
                        range_constraints: Dict[str, Dict]) -> Dict[str, List[str]]:
    """
    Validate data values against range constraints
    
    Args:
        df: Input DataFrame
        range_constraints: Dictionary mapping column names to range constraints
                          Example: {'age': {'min': 0, 'max': 120}, 'salary': {'min': 0}}
        
    Returns:
        Dictionary with validation results
    """
    validation_results = {
        'out_of_range_values': {},
        'validation_passed': True
    }
    
    for col, constraints in range_constraints.items():
        if col in df.columns:
            out_of_range_mask = pd.Series([True] * len(df))
            
            # Apply minimum constraint
            if 'min' in constraints:
                out_of_range_mask &= (df[col] >= constraints['min'])
            
            # Apply maximum constraint
            if 'max' in constraints:
                out_of_range_mask &= (df[col] <= constraints['max'])
            
            # Identify out-of-range values
            out_of_range_indices = df[~out_of_range_mask].index.tolist()
            if out_of_range_indices:
                validation_results['out_of_range_values'][col] = out_of_range_indices
                validation_results['validation_passed'] = False
    
    logger.info(f"Range validation completed. Passed: {validation_results['validation_passed']}")
    return validation_results


def validate_data_completeness(df: pd.DataFrame, 
                              completeness_requirements: Dict[str, float]) -> Dict[str, Dict]:
    """
    Validate data completeness for specified columns
    
    Args:
        df: Input DataFrame
        completeness_requirements: Dictionary mapping column names to minimum completeness ratio (0-1)
        
    Returns:
        Dictionary with validation results
    """
    validation_results = {
        'completeness_scores': {},
        'below_threshold_columns': [],
        'validation_passed': True
    }
    
    for col, min_completeness in completeness_requirements.items():
        if col in df.columns:
            # Calculate completeness ratio
            completeness_ratio = 1 - (df[col].isnull().sum() / len(df))
            validation_results['completeness_scores'][col] = completeness_ratio
            
            # Check if below threshold
            if completeness_ratio < min_completeness:
                validation_results['below_threshold_columns'].append(col)
                validation_results['validation_passed'] = False
    
    logger.info(f"Completeness validation completed. Passed: {validation_results['validation_passed']}")
    return validation_results


def validate_cross_field_constraints(df: pd.DataFrame, 
                                   cross_field_rules: List[Dict]) -> Dict[str, List[int]]:
    """
    Validate cross-field constraints
    
    Args:
        df: Input DataFrame
        cross_field_rules: List of cross-field validation rules
                          Example: [{'expr': 'df["end_date"] >= df["start_date"]', 'error_msg': 'End date must be after start date'}]
        
    Returns:
        Dictionary with validation results
    """
    validation_results = {
        'constraint_violations': {},
        'validation_passed': True
    }
    
    for i, rule in enumerate(cross_field_rules):
        try:
            # Evaluate the constraint expression
            constraint_result = eval(rule['expr'])
            
            # Identify rows that violate the constraint
            violation_indices = df[~constraint_result].index.tolist()
            
            if violation_indices:
                validation_results['constraint_violations'][f'rule_{i}'] = violation_indices
                validation_results['validation_passed'] = False
                
        except Exception as e:
            logger.warning(f"Failed to evaluate cross-field constraint: {e}")
    
    logger.info(f"Cross-field validation completed. Passed: {validation_results['validation_passed']}")
    return validation_results


def calculate_data_quality_score(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate overall data quality score
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with quality scores
    """
    quality_scores = {}
    
    # Completeness score (percentage of non-null values)
    completeness = (df.count().sum() / (len(df) * len(df.columns))) * 100
    quality_scores['completeness'] = completeness
    
    # Uniqueness score (percentage of unique rows)
    uniqueness = (df.drop_duplicates().shape[0] / df.shape[0]) * 100
    quality_scores['uniqueness'] = uniqueness
    
    # Consistency score (based on data types)
    consistent_cols = 0
    for col in df.columns:
        # Simple consistency check - assume all columns are consistent for now
        consistent_cols += 1
    consistency = (consistent_cols / len(df.columns)) * 100
    quality_scores['consistency'] = consistency
    
    # Overall quality score
    quality_scores['overall'] = (completeness + uniqueness + consistency) / 3
    
    logger.info(f"Data quality scores calculated: {quality_scores}")
    return quality_scores


def validate_data(df: pd.DataFrame, 
                 validation_config: dict) -> Dict[str, Dict]:
    """
    Comprehensive data validation pipeline
    
    Args:
        df: Input DataFrame
        validation_config: Dictionary specifying validation strategies
                          Example: {
                              'schema': {'col1': 'int', 'col2': 'float'},
                              'ranges': {'age': {'min': 0, 'max': 120}},
                              'completeness': {'col1': 0.95, 'col2': 0.90},
                              'cross_field': [{'expr': 'df["end_date"] >= df["start_date"]', 'error_msg': '...'}]
                          }
        
    Returns:
        Dictionary with all validation results
    """
    logger.info("Starting data validation pipeline")
    validation_results = {}
    
    # Validate schema
    if 'schema' in validation_config:
        validation_results['schema'] = validate_data_schema(
            df, 
            validation_config['schema']
        )
    
    # Validate ranges
    if 'ranges' in validation_config:
        validation_results['ranges'] = validate_data_ranges(
            df, 
            validation_config['ranges']
        )
    
    # Validate completeness
    if 'completeness' in validation_config:
        validation_results['completeness'] = validate_data_completeness(
            df, 
            validation_config['completeness']
        )
    
    # Validate cross-field constraints
    if 'cross_field' in validation_config:
        validation_results['cross_field'] = validate_cross_field_constraints(
            df, 
            validation_config['cross_field']
        )
    
    # Calculate quality scores
    validation_results['quality_scores'] = calculate_data_quality_score(df)
    
    # Overall validation status
    all_passed = all(
        result.get('validation_passed', True) 
        for result in validation_results.values() 
        if isinstance(result, dict) and 'validation_passed' in result
    )
    validation_results['overall_validation_passed'] = all_passed
    
    logger.info(f"Data validation pipeline completed. Overall passed: {all_passed}")
    return validation_results