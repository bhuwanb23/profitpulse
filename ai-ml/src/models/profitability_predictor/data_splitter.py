"""
Data Splitter for Client Profitability Prediction
Handles train/validation/test splitting with proper stratification
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta

try:
    from sklearn.model_selection import train_test_split
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    train_test_split = None

logger = logging.getLogger(__name__)


class ProfitabilityDataSplitter:
    """Splits data for client profitability prediction models"""
    
    def __init__(self):
        """Initialize the data splitter"""
        pass
        
    def time_based_split(self, features: pd.DataFrame, test_size: float = 0.15, 
                        validation_size: float = 0.15) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Split dataset using time-based approach to prevent data leakage
        
        Args:
            features: DataFrame with features
            test_size: Proportion of data for testing
            validation_size: Proportion of data for validation
            
        Returns:
            Tuple of (train_df, validation_df, test_df)
        """
        logger.info("Performing time-based data split")
        
        try:
            # Sort by contract start date if available
            if 'start_date' in features.columns:
                features_sorted = features.sort_values('start_date')
            else:
                # If no date column, use default index-based sorting
                features_sorted = features.sort_index()
            
            # Calculate split points
            total_rows = len(features_sorted)
            test_rows = int(total_rows * test_size)
            validation_rows = int(total_rows * validation_size)
            train_rows = total_rows - test_rows - validation_rows
            
            # Perform time-based split (most recent data for test)
            test_df = features_sorted.iloc[-test_rows:]
            validation_df = features_sorted.iloc[-(test_rows + validation_rows):-test_rows]
            train_df = features_sorted.iloc[:train_rows]
            
            logger.info(f"Time-based split - Train: {len(train_df)}, Validation: {len(validation_df)}, Test: {len(test_df)}")
            return train_df, validation_df, test_df
            
        except Exception as e:
            logger.error(f"Error in time-based split: {e}")
            raise
    
    def stratified_split(self, features: pd.DataFrame, target_column: str = 'profit_margin',
                        test_size: float = 0.15, validation_size: float = 0.15, 
                        random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Split dataset using stratified approach to maintain distribution
        
        Args:
            features: DataFrame with features
            target_column: Column to stratify on
            test_size: Proportion of data for testing
            validation_size: Proportion of data for validation
            random_state: Random seed for reproducibility
            
        Returns:
            Tuple of (train_df, validation_df, test_df)
        """
        logger.info("Performing stratified data split")
        
        try:
            # Create bins for stratification if target is continuous
            if target_column in features.columns:
                # Bin continuous target variable for stratification
                features_copy = features.copy()
                features_copy['_strat_bins'] = pd.qcut(
                    features_copy[target_column].rank(method='first'), 
                    q=10, 
                    labels=False,
                    duplicates='drop'
                )
                stratify_col = '_strat_bins'
            else:
                # If target column not found, use default stratification
                features_copy = features.copy()
                stratify_col = None
            
            # First split: separate test set
            if stratify_col and stratify_col in features_copy.columns:
                if train_test_split is not None:
                    train_val_df, test_df = train_test_split(
                        features_copy, 
                        test_size=test_size, 
                        stratify=features_copy[stratify_col],
                        random_state=random_state
                    )
                else:
                    raise ImportError("scikit-learn is required for stratified split but not available")
            else:
                if train_test_split is not None:
                    train_val_df, test_df = train_test_split(
                        features_copy, 
                        test_size=test_size, 
                        random_state=random_state
                    )
                else:
                    raise ImportError("scikit-learn is required for data splitting but not available")
            
            # Second split: separate train and validation sets
            # Adjust validation size to account for the first split
            adjusted_validation_size = validation_size / (1 - test_size)
            
            if stratify_col and stratify_col in train_val_df.columns:
                if train_test_split is not None:
                    train_df, validation_df = train_test_split(
                        train_val_df, 
                        test_size=adjusted_validation_size, 
                        stratify=train_val_df[stratify_col],
                        random_state=random_state
                    )
                else:
                    raise ImportError("scikit-learn is required for stratified split but not available")
            else:
                if train_test_split is not None:
                    train_df, validation_df = train_test_split(
                        train_val_df, 
                        test_size=adjusted_validation_size, 
                        random_state=random_state
                    )
                else:
                    raise ImportError("scikit-learn is required for data splitting but not available")
            
            # Remove temporary stratification column
            if '_strat_bins' in train_df.columns:
                train_df = train_df.drop('_strat_bins', axis=1)
            if '_strat_bins' in validation_df.columns:
                validation_df = validation_df.drop('_strat_bins', axis=1)
            if '_strat_bins' in test_df.columns:
                test_df = test_df.drop('_strat_bins', axis=1)
            
            logger.info(f"Stratified split - Train: {len(train_df)}, Validation: {len(validation_df)}, Test: {len(test_df)}")
            return train_df, validation_df, test_df
            
        except Exception as e:
            logger.error(f"Error in stratified split: {e}")
            raise
    
    def split_dataset(self, features: pd.DataFrame, target_column: str = 'profit_margin',
                     split_method: str = 'stratified', test_size: float = 0.15, 
                     validation_size: float = 0.15, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Split dataset into train, validation, and test sets
        
        Args:
            features: DataFrame with features
            target_column: Column to stratify on (for stratified split)
            split_method: Method to use ('time_based' or 'stratified')
            test_size: Proportion of data for testing
            validation_size: Proportion of data for validation
            random_state: Random seed for reproducibility
            
        Returns:
            Tuple of (train_df, validation_df, test_df)
        """
        logger.info(f"Splitting dataset using {split_method} method")
        
        try:
            if not SKLEARN_AVAILABLE:
                raise ImportError("scikit-learn is required for data splitting but not available")
                        
            if split_method == 'time_based':
                return self.time_based_split(features, test_size, validation_size)
            elif split_method == 'stratified':
                return self.stratified_split(features, target_column, test_size, validation_size, random_state)
            else:
                raise ValueError(f"Unknown split method: {split_method}")
                
        except Exception as e:
            logger.error(f"Error splitting dataset: {e}")
            raise


# Convenience function for easy usage
def split_profitability_data(features: pd.DataFrame, target_column: str = 'profit_margin',
                           split_method: str = 'stratified', test_size: float = 0.15, 
                           validation_size: float = 0.15, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split data for client profitability prediction
    
    Args:
        features: DataFrame with features
        target_column: Column to stratify on
        split_method: Method to use ('time_based' or 'stratified')
        test_size: Proportion of data for testing
        validation_size: Proportion of data for validation
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (train_df, validation_df, test_df)
    """
    splitter = ProfitabilityDataSplitter()
    return splitter.split_dataset(features, target_column, split_method, test_size, validation_size, random_state)