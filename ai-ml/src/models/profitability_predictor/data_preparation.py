"""
Data Preparation for Client Profitability Prediction
Handles data collection, feature engineering, and dataset splitting
"""

import pandas as pd
import numpy as np
import sqlite3
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta

# Import our data extraction modules
from src.data.ingestion.comprehensive_extractor import ComprehensiveDataExtractor, ExtractionConfig

# Import our new modules
from src.models.profitability_predictor.feature_engineering import ProfitabilityFeatureEngineer
from src.models.profitability_predictor.data_splitter import ProfitabilityDataSplitter
from src.models.profitability_predictor.data_quality import ProfitabilityDataQualityAssessor

logger = logging.getLogger(__name__)


class ProfitabilityDataPreparator:
    """Prepares data for client profitability prediction models"""
    
    def __init__(self, db_path: str = "../../database/superhack.db"):
        """
        Initialize the data preparator
        
        Args:
            db_path: Path to the SQLite database
        """
        self.db_path = db_path
        # Create a simple config for the extractor
        config = ExtractionConfig(
            start_date=datetime.now() - timedelta(days=365),
            end_date=datetime.now()
        )
        self.extractor = ComprehensiveDataExtractor(config)
        self.scaler = None
        
    def collect_historical_financial_data(self) -> pd.DataFrame:
        """
        Collect historical financial data from all sources
        
        Returns:
            DataFrame with client financial data
        """
        logger.info("Collecting historical financial data")
        
        try:
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            
            # Extract client data
            clients_df = pd.read_sql_query("""
                SELECT id, name, industry, contract_type, contract_value, 
                       start_date, end_date, is_active
                FROM clients
            """, conn)
            
            # Extract invoice data
            invoices_df = pd.read_sql_query("""
                SELECT client_id, invoice_date, total_amount, status
                FROM invoices
            """, conn)
            
            # Extract ticket data
            tickets_df = pd.read_sql_query("""
                SELECT client_id, time_spent, billable_hours, hourly_rate
                FROM tickets
            """, conn)
            
            # Extract service data
            services_df = pd.read_sql_query("""
                SELECT cs.client_id, s.category, cs.custom_price, cs.quantity
                FROM client_services cs
                JOIN services s ON cs.service_id = s.id
            """, conn)
            
            conn.close()
            
            # Process and merge data
            # Calculate total revenue per client
            client_revenue = invoices_df.groupby('client_id')['total_amount'].sum().reset_index()
            client_revenue.columns = ['id', 'total_revenue']
            
            # Calculate total costs per client (from tickets)
            tickets_df['ticket_cost'] = tickets_df['time_spent'] * tickets_df['hourly_rate']
            client_costs = tickets_df.groupby('client_id')['ticket_cost'].sum().reset_index()
            client_costs.columns = ['id', 'ticket_cost']
            
            # Merge all data
            merged_df = clients_df.merge(client_revenue, on='id', how='left')
            merged_df = merged_df.merge(client_costs, on='id', how='left')
            merged_df['total_costs'] = merged_df['ticket_cost'].fillna(0)
            
            # Calculate profitability metrics
            merged_df['profit'] = merged_df['total_revenue'] - merged_df['total_costs']
            merged_df['profit_margin'] = np.where(
                merged_df['total_revenue'] > 0,
                merged_df['profit'] / merged_df['total_revenue'],
                0
            )
            
            logger.info(f"Collected financial data for {len(merged_df)} clients")
            return merged_df
            
        except Exception as e:
            logger.error(f"Error collecting historical financial data: {e}")
            raise
    
    def create_features(self, financial_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create features for profitability prediction using advanced feature engineering
        
        Args:
            financial_data: DataFrame with financial data
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("Creating features for profitability prediction using advanced feature engineering")
        
        try:
            # Use our advanced feature engineering module
            feature_engineer = ProfitabilityFeatureEngineer(self.db_path)
            features_df = feature_engineer.engineer_features(financial_data)
            
            logger.info(f"Created {len(features_df.columns)} features for {len(features_df)} clients")
            return features_df
            
        except Exception as e:
            logger.error(f"Error creating features: {e}")
            raise
    
    def split_dataset(self, features: pd.DataFrame, test_size: float = 0.15, 
                     validation_size: float = 0.15, random_state: int = 42, 
                     split_method: str = 'stratified') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Split dataset into train, validation, and test sets using our advanced splitter
        
        Args:
            features: DataFrame with features
            test_size: Proportion of data for testing
            validation_size: Proportion of data for validation
            random_state: Random seed for reproducibility
            split_method: Method to use ('time_based' or 'stratified')
            
        Returns:
            Tuple of (train_df, validation_df, test_df)
        """
        logger.info(f"Splitting dataset using {split_method} method")
        
        try:
            # Use our advanced data splitter module
            data_splitter = ProfitabilityDataSplitter()
            return data_splitter.split_dataset(
                features, 
                target_column='profit_margin',
                split_method=split_method,
                test_size=test_size, 
                validation_size=validation_size, 
                random_state=random_state
            )
            
        except Exception as e:
            logger.error(f"Error splitting dataset: {e}")
            raise
    
    def assess_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Assess the quality of the prepared data using our advanced quality assessor
        
        Args:
            data: DataFrame to assess
            
        Returns:
            Dictionary with quality metrics
        """
        logger.info("Assessing data quality using advanced quality assessor")
        
        try:
            # Use our advanced data quality assessment module
            quality_assessor = ProfitabilityDataQualityAssessor()
            return quality_assessor.assess_data_quality(data)
            
        except Exception as e:
            logger.error(f"Error assessing data quality: {e}")
            raise
    
    def prepare_dataset(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
        """
        Complete data preparation pipeline
        
        Returns:
            Tuple of (train_df, validation_df, test_df, quality_report)
        """
        logger.info("Starting complete data preparation pipeline")
        
        try:
            # 1. Collect historical financial data
            financial_data = self.collect_historical_financial_data()
            
            # 2. Create features
            features = self.create_features(financial_data)
            
            # 3. Assess data quality
            quality_report = self.assess_data_quality(features)
            
            # 4. Split dataset
            train_df, validation_df, test_df = self.split_dataset(features)
            
            logger.info("Complete data preparation pipeline finished successfully")
            return train_df, validation_df, test_df, quality_report
            
        except Exception as e:
            logger.error(f"Error in complete data preparation pipeline: {e}")
            raise


# Convenience function for easy usage
def prepare_profitability_data(db_path: str = "../../database/superhack.db") -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Prepare data for client profitability prediction
    
    Args:
        db_path: Path to the SQLite database
        
    Returns:
        Tuple of (train_df, validation_df, test_df, quality_report)
    """
    preparator = ProfitabilityDataPreparator(db_path)
    return preparator.prepare_dataset()