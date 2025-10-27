"""
Feature Engineering for Client Profitability Prediction
Creates advanced features from financial and operational data
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta

from src.models.profitability_predictor.historical_data_collector import HistoricalDataCollector

logger = logging.getLogger(__name__)


class ProfitabilityFeatureEngineer:
    """Engineers features for client profitability prediction models"""
    
    def __init__(self, db_path: str = "../../database/superhack.db"):
        """
        Initialize the feature engineer
        
        Args:
            db_path: Path to the SQLite database
        """
        self.db_path = db_path
        self.data_collector = HistoricalDataCollector(db_path)
        
    def create_financial_features(self, financial_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create financial features for profitability prediction
        
        Args:
            financial_data: DataFrame with financial data
            
        Returns:
            DataFrame with financial features
        """
        logger.info("Creating financial features")
        
        try:
            features_df = financial_data.copy()
            
            # Basic financial ratios
            features_df['revenue_to_contract_value_ratio'] = np.where(
                features_df['contract_value'] > 0,
                features_df['total_revenue'] / features_df['contract_value'],
                0
            )
            
            features_df['cost_to_revenue_ratio'] = np.where(
                features_df['total_revenue'] > 0,
                features_df['total_costs'] / features_df['total_revenue'],
                0
            )
            
            # Revenue stability metrics
            features_df['revenue_stability_score'] = np.where(
                features_df['total_revenue'] > 0,
                1 - abs(features_df['profit_margin'] - features_df['profit_margin'].mean()) / features_df['profit_margin'].std(),
                0
            )
            
            # Contract value efficiency
            features_df['contract_value_efficiency'] = np.where(
                features_df['contract_value'] > 0,
                features_df['total_revenue'] / features_df['contract_value'],
                0
            )
            
            # Service profitability
            features_df['avg_service_profitability'] = np.where(
                features_df['service_count'] > 0,
                features_df['profit'] / features_df['service_count'],
                0
            )
            
            # Revenue concentration risk (higher means more concentrated)
            features_df['revenue_concentration_risk'] = np.where(
                features_df['total_revenue'] > 0,
                features_df['total_revenue'] / features_df['total_revenue'].sum(),
                0
            )
            
            logger.info(f"Created {len([col for col in features_df.columns if col not in financial_data.columns])} financial features")
            return features_df
            
        except Exception as e:
            logger.error(f"Error creating financial features: {e}")
            raise
    
    def create_operational_features(self, financial_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create operational features for profitability prediction
        
        Args:
            financial_data: DataFrame with financial data
            
        Returns:
            DataFrame with operational features
        """
        logger.info("Creating operational features")
        
        try:
            features_df = financial_data.copy()
            
            # Service utilization efficiency
            features_df['service_utilization_efficiency'] = np.where(
                features_df['total_quantity'] > 0,
                features_df['service_count'] / features_df['total_quantity'],
                0
            )
            
            # Cost efficiency per service
            features_df['cost_efficiency_per_service'] = np.where(
                features_df['service_count'] > 0,
                features_df['total_costs'] / features_df['service_count'],
                0
            )
            
            # Revenue efficiency per service
            features_df['revenue_efficiency_per_service'] = np.where(
                features_df['service_count'] > 0,
                features_df['total_revenue'] / features_df['service_count'],
                0
            )
            
            # Service diversity (number of different service types)
            # This would require service category data in a full implementation
            
            logger.info(f"Created {len([col for col in features_df.columns if col not in financial_data.columns])} operational features")
            return features_df
            
        except Exception as e:
            logger.error(f"Error creating operational features: {e}")
            raise
    
    def create_temporal_features(self, financial_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create temporal features for profitability prediction
        
        Args:
            financial_data: DataFrame with financial data
            
        Returns:
            DataFrame with temporal features
        """
        logger.info("Creating temporal features")
        
        try:
            features_df = financial_data.copy()
            
            # Contract duration features
            features_df['contract_duration_days'] = (
                pd.to_datetime(features_df['end_date']).fillna(pd.to_datetime('today')) - 
                pd.to_datetime(features_df['start_date'])
            ).dt.days
            
            # Contract age (days since start)
            features_df['contract_age_days'] = (
                pd.to_datetime('today') - pd.to_datetime(features_df['start_date'])
            ).dt.days
            
            # Contract nearing end (days until end)
            features_df['days_until_contract_end'] = (
                pd.to_datetime(features_df['end_date']).fillna(pd.to_datetime('today')) - 
                pd.to_datetime('today')
            ).dt.days
            
            # Revenue velocity (revenue per day of contract)
            features_df['revenue_velocity'] = np.where(
                features_df['contract_duration_days'] > 0,
                features_df['total_revenue'] / features_df['contract_duration_days'],
                0
            )
            
            logger.info(f"Created {len([col for col in features_df.columns if col not in financial_data.columns])} temporal features")
            return features_df
            
        except Exception as e:
            logger.error(f"Error creating temporal features: {e}")
            raise
    
    def create_categorical_features(self, financial_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create categorical features for profitability prediction
        
        Args:
            financial_data: DataFrame with financial data
            
        Returns:
            DataFrame with categorical features
        """
        logger.info("Creating categorical features")
        
        try:
            features_df = financial_data.copy()
            
            # Contract type encoding
            contract_type_dummies = pd.get_dummies(features_df['contract_type'], prefix='contract_type')
            features_df = pd.concat([features_df, contract_type_dummies], axis=1)
            
            # Industry encoding
            industry_dummies = pd.get_dummies(features_df['industry'], prefix='industry')
            features_df = pd.concat([features_df, industry_dummies], axis=1)
            
            # Active status as binary feature
            features_df['is_active_binary'] = features_df['is_active'].astype(int)
            
            logger.info(f"Created {len([col for col in features_df.columns if col not in financial_data.columns])} categorical features")
            return features_df
            
        except Exception as e:
            logger.error(f"Error creating categorical features: {e}")
            raise
    
    def create_interaction_features(self, financial_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create interaction features for profitability prediction
        
        Args:
            financial_data: DataFrame with financial data
            
        Returns:
            DataFrame with interaction features
        """
        logger.info("Creating interaction features")
        
        try:
            features_df = financial_data.copy()
            
            # Revenue and cost interaction
            features_df['revenue_cost_interaction'] = (
                features_df['total_revenue'] * features_df['total_costs']
            )
            
            # Profit and contract value interaction
            features_df['profit_contract_interaction'] = (
                features_df['profit'] * features_df['contract_value']
            )
            
            # Margin and service count interaction
            features_df['margin_service_interaction'] = (
                features_df['profit_margin'] * features_df['service_count']
            )
            
            logger.info(f"Created {len([col for col in features_df.columns if col not in financial_data.columns])} interaction features")
            return features_df
            
        except Exception as e:
            logger.error(f"Error creating interaction features: {e}")
            raise
    
    def engineer_features(self, financial_data: pd.DataFrame) -> pd.DataFrame:
        """
        Complete feature engineering pipeline
        
        Args:
            financial_data: DataFrame with financial data
            
        Returns:
            DataFrame with all engineered features
        """
        logger.info("Starting complete feature engineering pipeline")
        
        try:
            # Apply all feature engineering steps
            features_df = self.create_financial_features(financial_data)
            features_df = self.create_operational_features(features_df)
            features_df = self.create_temporal_features(features_df)
            features_df = self.create_categorical_features(features_df)
            features_df = self.create_interaction_features(features_df)
            
            logger.info(f"Complete feature engineering pipeline finished - Total features: {len(features_df.columns)}")
            return features_df
            
        except Exception as e:
            logger.error(f"Error in complete feature engineering pipeline: {e}")
            raise


# Convenience function for easy usage
def engineer_profitability_features(financial_data: pd.DataFrame, db_path: str = "../../database/superhack.db") -> pd.DataFrame:
    """
    Engineer features for client profitability prediction
    
    Args:
        financial_data: DataFrame with financial data
        db_path: Path to the SQLite database
        
    Returns:
        DataFrame with engineered features
    """
    engineer = ProfitabilityFeatureEngineer(db_path)
    return engineer.engineer_features(financial_data)