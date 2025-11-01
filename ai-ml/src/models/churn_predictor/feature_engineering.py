"""
Feature Engineering for Client Churn Prediction
Creates features from client data for churn prediction models
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class ChurnFeatureEngineer:
    """Creates features for client churn prediction"""
    
    def __init__(self):
        """Initialize feature engineer"""
        logger.info("Churn Feature Engineer initialized")
    
    def create_temporal_features(self, client_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create temporal features from client data
        
        Args:
            client_data: DataFrame with client data
            
        Returns:
            DataFrame with temporal features added
        """
        try:
            client_data = client_data.copy()
            
            # Contract duration features
            client_data['contract_duration_days'] = (
                (client_data['contract_end_date'].fillna(datetime.now()) - client_data['contract_start_date']).dt.days
            )
            
            # Days since last interaction
            client_data['days_since_last_interaction'] = (
                datetime.now() - client_data['last_interaction_date']
            ).dt.days
            
            # Days until contract end
            client_data['days_until_contract_end'] = (
                client_data['contract_end_date'] - datetime.now()
            ).dt.days
            
            # Contract age
            client_data['contract_age_days'] = (
                datetime.now() - client_data['contract_start_date']
            ).dt.days
            
            logger.info("Created temporal features")
            return client_data
            
        except Exception as e:
            logger.error(f"Error creating temporal features: {e}")
            return client_data
    
    def create_engagement_features(self, interactions: pd.DataFrame, 
                                 client_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create engagement features from interaction data
        
        Args:
            interactions: DataFrame with client interactions
            client_data: DataFrame with client data
            
        Returns:
            DataFrame with engagement features added
        """
        try:
            # Calculate interaction frequency
            interaction_counts = interactions.groupby('client_id').size().reset_index()
            interaction_counts.columns = ['client_id', 'total_interactions']
            
            # Calculate average satisfaction score
            avg_satisfaction = interactions.groupby('client_id')['satisfaction_score'].mean().reset_index()
            avg_satisfaction.rename(columns={'satisfaction_score': 'avg_satisfaction_score'}, inplace=True)
            
            # Calculate support ticket ratio
            support_tickets = interactions[interactions['interaction_type'] == 'support_ticket']
            ticket_counts = support_tickets.groupby('client_id').size().reset_index()
            ticket_counts.columns = ['client_id', 'support_tickets']
            
            # Merge features with client data
            client_data = client_data.merge(interaction_counts, on='client_id', how='left')
            client_data = client_data.merge(avg_satisfaction, on='client_id', how='left')
            client_data = client_data.merge(ticket_counts, on='client_id', how='left')
            
            # Fill NaN values
            client_data['total_interactions'].fillna(0, inplace=True)
            client_data['avg_satisfaction_score'].fillna(0, inplace=True)
            client_data['support_tickets'].fillna(0, inplace=True)
            
            # Calculate interaction frequency (interactions per month)
            client_data['interactions_per_month'] = (
                client_data['total_interactions'] / (client_data['contract_age_days'] / 30)
            )
            client_data['interactions_per_month'].replace([np.inf, -np.inf], 0, inplace=True)
            client_data['interactions_per_month'].fillna(0, inplace=True)
            
            logger.info("Created engagement features")
            return client_data
            
        except Exception as e:
            logger.error(f"Error creating engagement features: {e}")
            return client_data
    
    def create_financial_features(self, financial_data: pd.DataFrame, 
                                client_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create financial features from payment data
        
        Args:
            financial_data: DataFrame with financial data
            client_data: DataFrame with client data
            
        Returns:
            DataFrame with financial features added
        """
        try:
            # Calculate payment behavior metrics
            payment_stats = financial_data.groupby('client_id').agg({
                'amount_paid': ['sum', 'mean', 'count'],
                'days_to_pay': ['mean', 'max'],
                'late_payment': 'sum'
            }).reset_index()
            
            # Flatten column names
            payment_stats.columns = [
                'client_id', 'total_amount_paid', 'avg_payment_amount', 'payment_count',
                'avg_days_to_pay', 'max_days_to_pay', 'late_payments'
            ]
            
            # Calculate late payment ratio
            payment_stats['late_payment_ratio'] = (
                payment_stats['late_payments'] / payment_stats['payment_count']
            )
            payment_stats['late_payment_ratio'].fillna(0, inplace=True)
            
            # Merge features with client data
            client_data = client_data.merge(payment_stats, on='client_id', how='left')
            
            # Fill NaN values
            client_data['total_amount_paid'].fillna(0, inplace=True)
            client_data['avg_payment_amount'].fillna(0, inplace=True)
            client_data['payment_count'].fillna(0, inplace=True)
            client_data['avg_days_to_pay'].fillna(0, inplace=True)
            client_data['max_days_to_pay'].fillna(0, inplace=True)
            client_data['late_payments'].fillna(0, inplace=True)
            client_data['late_payment_ratio'].fillna(0, inplace=True)
            
            logger.info("Created financial features")
            return client_data
            
        except Exception as e:
            logger.error(f"Error creating financial features: {e}")
            return client_data
    
    def create_service_features(self, service_data: pd.DataFrame, 
                              client_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create service usage features from service data
        
        Args:
            service_data: DataFrame with service usage data
            client_data: DataFrame with client data
            
        Returns:
            DataFrame with service features added
        """
        try:
            # Calculate service usage metrics
            service_stats = service_data.groupby('client_id').agg({
                'hours_used': ['sum', 'mean'],
                'satisfaction_rating': 'mean',
                'sla_breaches': 'sum',
                'support_tickets': 'sum'
            }).reset_index()
            
            # Flatten column names
            service_stats.columns = [
                'client_id', 'total_hours_used', 'avg_hours_per_session',
                'avg_service_satisfaction', 'total_sla_breaches', 'total_support_tickets_from_service'
            ]
            
            # Calculate SLA breach ratio
            service_stats['sla_breach_ratio'] = (
                service_stats['total_sla_breaches'] / 
                (service_stats['total_hours_used'] / 10)  # Normalize by usage
            )
            service_stats['sla_breach_ratio'].replace([np.inf, -np.inf], 0, inplace=True)
            service_stats['sla_breach_ratio'].fillna(0, inplace=True)
            
            # Merge features with client data
            client_data = client_data.merge(service_stats, on='client_id', how='left')
            
            # Fill NaN values
            for col in ['total_hours_used', 'avg_hours_per_session', 'avg_service_satisfaction',
                       'total_sla_breaches', 'total_support_tickets_from_service', 'sla_breach_ratio']:
                client_data[col].fillna(0, inplace=True)
            
            logger.info("Created service features")
            return client_data
            
        except Exception as e:
            logger.error(f"Error creating service features: {e}")
            return client_data
    
    def create_derived_features(self, client_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create derived features from existing features
        
        Args:
            client_data: DataFrame with client data and existing features
            
        Returns:
            DataFrame with derived features added
        """
        try:
            client_data = client_data.copy()
            
            # Payment to contract value ratio
            client_data['payment_to_contract_ratio'] = (
                client_data['total_amount_paid'] / client_data['contract_value']
            )
            client_data['payment_to_contract_ratio'].replace([np.inf, -np.inf], 0, inplace=True)
            client_data['payment_to_contract_ratio'].fillna(0, inplace=True)
            
            # Service usage efficiency
            client_data['usage_efficiency'] = (
                client_data['total_hours_used'] / client_data['contract_value']
            )
            client_data['usage_efficiency'].replace([np.inf, -np.inf], 0, inplace=True)
            client_data['usage_efficiency'].fillna(0, inplace=True)
            
            # Engagement score (combination of interactions and satisfaction)
            client_data['engagement_score'] = (
                client_data['total_interactions'] * client_data['avg_satisfaction_score'] / 100
            )
            client_data['engagement_score'].fillna(0, inplace=True)
            
            # Risk score (combination of negative factors)
            client_data['risk_score'] = (
                client_data['late_payment_ratio'] * 0.3 +
                client_data['sla_breach_ratio'] * 0.3 +
                (10 - client_data['avg_satisfaction_score']) / 10 * 0.2 +
                client_data['days_until_contract_end'].apply(lambda x: max(0, x) / 30) * 0.2
            )
            
            # Contract renewal likelihood score
            client_data['renewal_likelihood'] = 1 - client_data['risk_score']
            
            logger.info("Created derived features")
            return client_data
            
        except Exception as e:
            logger.error(f"Error creating derived features: {e}")
            return client_data
    
    def prepare_features(self, client_history: pd.DataFrame, 
                        interactions: pd.DataFrame,
                        financial_data: pd.DataFrame,
                        service_data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare all features for churn prediction
        
        Args:
            client_history: DataFrame with client history data
            interactions: DataFrame with client interactions
            financial_data: DataFrame with financial data
            service_data: DataFrame with service usage data
            
        Returns:
            DataFrame with all features prepared for modeling
        """
        try:
            # Start with client history data
            features = client_history.copy()
            
            # Create temporal features
            features = self.create_temporal_features(features)
            
            # Create engagement features
            features = self.create_engagement_features(interactions, features)
            
            # Create financial features
            features = self.create_financial_features(financial_data, features)
            
            # Create service features
            features = self.create_service_features(service_data, features)
            
            # Create derived features
            features = self.create_derived_features(features)
            
            # Fill any remaining NaN values
            features.fillna(0, inplace=True)
            
            logger.info(f"Prepared features for {len(features)} clients")
            return features
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            return client_history


# Global instance for easy access
churn_feature_engineer_instance = None


def get_churn_feature_engineer() -> ChurnFeatureEngineer:
    """Get singleton churn feature engineer instance"""
    global churn_feature_engineer_instance
    if churn_feature_engineer_instance is None:
        churn_feature_engineer_instance = ChurnFeatureEngineer()
    return churn_feature_engineer_instance