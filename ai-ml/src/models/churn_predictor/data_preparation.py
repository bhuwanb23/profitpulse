"""
Data Preparation for Client Churn Prediction
Handles collection and preprocessing of client historical data, interactions, and service metrics
"""

import logging
import numpy as np
import pandas as pd
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Conditional imports for data sources
try:
    # Import data extraction utilities from the project
    from ...data.ingestion.quickbooks_client import QuickBooksClient
    from ...data.ingestion.superops_client import SuperOpsClient
    QUICKBOOKS_AVAILABLE = True
    SUPEROPS_AVAILABLE = True
except ImportError:
    QuickBooksClient = None
    SuperOpsClient = None
    QUICKBOOKS_AVAILABLE = False
    SUPEROPS_AVAILABLE = False

logger = logging.getLogger(__name__)


class ChurnDataPreparator:
    """Prepares data for client churn prediction"""
    
    def __init__(self, db_path: str = "../../database/superhack.db"):
        """
        Initialize the data preparator
        
        Args:
            db_path: Path to database
        """
        self.db_path = db_path
        # Initialize clients as None, they will be initialized when needed
        self.quickbooks_client = None
        self.superops_client = None
        
        # Try to initialize clients if available
        try:
            if QUICKBOOKS_AVAILABLE and QuickBooksClient:
                from ...data.ingestion.quickbooks_client import create_quickbooks_client
                self.quickbooks_client = create_quickbooks_client()
        except Exception as e:
            logger.warning(f"Failed to initialize QuickBooks client: {e}")
            
        try:
            if SUPEROPS_AVAILABLE and SuperOpsClient:
                from ...data.ingestion.superops_client import create_superops_client
                self.superops_client = create_superops_client()
        except Exception as e:
            logger.warning(f"Failed to initialize SuperOps client: {e}")
            
        # Path to CSV data files
        self.data_dir = "../../data/churn_predictor"
        logger.info("Churn Data Preparator initialized")
    
    async def collect_client_history_data(self, start_date: Optional[datetime] = None, 
                                        end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect historical client data including contracts, renewals, and churn status
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with client history data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=730)  # 2 years
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # If clients are available, use them
            if self.quickbooks_client is not None and self.superops_client is not None:
                # In a real implementation, we would collect data from both sources
                # For now, we'll use CSV data
                logger.info("Using CSV data for client history")
                csv_path = f"{self.data_dir}/client_history_data.csv"
                if os.path.exists(csv_path):
                    return pd.read_csv(csv_path, parse_dates=['contract_start_date', 'contract_end_date', 'last_interaction_date'])
                else:
                    # Fallback to mock data
                    logger.warning("CSV files not found, returning mock data")
                    return self._generate_mock_client_history_data(start_date, end_date)
            else:
                # Return data from CSV files
                logger.info("Reading client history data from CSV files")
                csv_path = f"{self.data_dir}/client_history_data.csv"
                if os.path.exists(csv_path):
                    return pd.read_csv(csv_path, parse_dates=['contract_start_date', 'contract_end_date', 'last_interaction_date'])
                else:
                    # Fallback to mock data
                    logger.warning("CSV files not found, returning mock data")
                    return self._generate_mock_client_history_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting client history data: {e}")
            return self._generate_mock_client_history_data(start_date, end_date)
    
    async def collect_client_interactions(self, start_date: Optional[datetime] = None, 
                                        end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect client interaction data including support tickets and communications
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with client interaction data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)  # 1 year
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading client interaction data from CSV files")
            csv_path = f"{self.data_dir}/client_interactions.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path, parse_dates=['interaction_date'])
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_client_interactions(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting client interaction data: {e}")
            return self._generate_mock_client_interactions(start_date, end_date)
    
    async def collect_financial_metrics(self, start_date: Optional[datetime] = None, 
                                      end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect financial metrics for clients including payment patterns and contract values
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with financial metrics data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=730)  # 2 years
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading financial metrics data from CSV files")
            csv_path = f"{self.data_dir}/financial_metrics.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path, parse_dates=['payment_date'])
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_financial_metrics(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting financial metrics data: {e}")
            return self._generate_mock_financial_metrics(start_date, end_date)
    
    async def collect_service_usage(self, start_date: Optional[datetime] = None, 
                                  end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect service usage data for clients
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with service usage data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)  # 1 year
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading service usage data from CSV files")
            csv_path = f"{self.data_dir}/service_usage.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path, parse_dates=['usage_date'])
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_service_usage(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting service usage data: {e}")
            return self._generate_mock_service_usage(start_date, end_date)
    
    def create_churn_labels(self, client_history: pd.DataFrame) -> pd.DataFrame:
        """
        Create churn labels based on client history data
        
        Args:
            client_history: DataFrame with client history data
            
        Returns:
            DataFrame with churn labels added
        """
        try:
            # Create churn label based on contract end date and renewal status
            # Churn = 1 if contract ended and not renewed within 30 days
            # Churn = 0 if contract is active or renewed
            client_history['churn'] = 0
            
            # For clients with ended contracts, check if they renewed
            ended_contracts = client_history[
                (client_history['contract_status'] == 'ended') & 
                (client_history['contract_end_date'].notna())
            ]
            
            for idx, client in ended_contracts.iterrows():
                # Check if there's a renewal within 30 days
                end_date = client['contract_end_date']
                next_contract_start = client_history[
                    (client_history['client_id'] == client['client_id']) & 
                    (client_history['contract_start_date'] > end_date) &
                    (client_history['contract_start_date'] <= end_date + timedelta(days=30))
                ]
                
                if next_contract_start.empty:
                    client_history.loc[idx, 'churn'] = 1
                    
            logger.info(f"Created churn labels for {len(client_history)} clients")
            return client_history
            
        except Exception as e:
            logger.error(f"Error creating churn labels: {e}")
            return client_history
    
    def _generate_mock_client_history_data(self, start_date: datetime, 
                                         end_date: datetime) -> pd.DataFrame:
        """Generate mock client history data for testing"""
        # Generate client data
        clients = []
        client_count = 100
        
        for i in range(client_count):
            client_id = f"CLIENT-{i+1:03d}"
            contract_start = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
            contract_duration = int(np.random.choice([1, 2, 3]))  # Contract duration in years
            contract_end = contract_start + timedelta(days=contract_duration * 365)
            
            # Determine contract status
            if contract_end > datetime.now():
                contract_status = 'active'
            else:
                contract_status = 'ended'
            
            # Randomly determine if client churned (20% churn rate)
            churned = np.random.choice([0, 1], p=[0.8, 0.2]) if contract_status == 'ended' else 0
            
            client = {
                'client_id': client_id,
                'client_name': f"Client {i+1}",
                'contract_start_date': contract_start,
                'contract_end_date': contract_end if contract_status == 'ended' else None,
                'contract_status': contract_status,
                'contract_value': np.random.uniform(1000, 10000),
                'contract_type': np.random.choice(['managed_services', 'project', 'consulting']),
                'industry': np.random.choice(['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing']),
                'company_size': np.random.choice(['Small', 'Medium', 'Large']),
                'primary_contact': f"contact{i+1}@example.com",
                'churn': churned
            }
            clients.append(client)
        
        return pd.DataFrame(clients)
    
    def _generate_mock_client_interactions(self, start_date: datetime, 
                                         end_date: datetime) -> pd.DataFrame:
        """Generate mock client interaction data for testing"""
        interactions = []
        
        # Generate interactions for each client
        for i in range(100):
            client_id = f"CLIENT-{i+1:03d}"
            interaction_count = np.random.randint(1, 20)  # 1-20 interactions per client
            
            for j in range(interaction_count):
                interaction_date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
                interaction_type = np.random.choice(['support_ticket', 'email', 'phone_call', 'meeting'])
                satisfaction_score = np.random.uniform(1, 10) if interaction_type != 'support_ticket' else np.random.uniform(1, 8)
                
                interaction = {
                    'interaction_id': f"INT-{i+1:03d}-{j+1:02d}",
                    'client_id': client_id,
                    'interaction_date': interaction_date,
                    'interaction_type': interaction_type,
                    'satisfaction_score': satisfaction_score,
                    'resolution_time_hours': np.random.uniform(0.5, 48) if interaction_type == 'support_ticket' else None,
                    'issue_category': np.random.choice(['technical', 'billing', 'service', 'other']) if interaction_type == 'support_ticket' else None
                }
                interactions.append(interaction)
        
        return pd.DataFrame(interactions)
    
    def _generate_mock_financial_metrics(self, start_date: datetime, 
                                       end_date: datetime) -> pd.DataFrame:
        """Generate mock financial metrics data for testing"""
        metrics = []
        
        # Generate financial data for each client
        for i in range(100):
            client_id = f"CLIENT-{i+1:03d}"
            payment_count = np.random.randint(1, 12)  # 1-12 payments per client
            
            for j in range(payment_count):
                payment_date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
                amount_paid = np.random.uniform(500, 5000)
                days_to_pay = np.random.randint(1, 60)  # Days taken to pay invoice
                payment_method = np.random.choice(['credit_card', 'bank_transfer', 'check'])
                
                metric = {
                    'payment_id': f"PMT-{i+1:03d}-{j+1:02d}",
                    'client_id': client_id,
                    'payment_date': payment_date,
                    'amount_paid': amount_paid,
                    'days_to_pay': days_to_pay,
                    'payment_method': payment_method,
                    'late_payment': 1 if days_to_pay > 30 else 0
                }
                metrics.append(metric)
        
        return pd.DataFrame(metrics)
    
    def _generate_mock_service_usage(self, start_date: datetime, 
                                   end_date: datetime) -> pd.DataFrame:
        """Generate mock service usage data for testing"""
        usage = []
        
        # Generate usage data for each client
        for i in range(100):
            client_id = f"CLIENT-{i+1:03d}"
            usage_count = np.random.randint(10, 100)  # 10-100 usage records per client
            
            for j in range(usage_count):
                usage_date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
                service_type = np.random.choice(['managed_services', 'project_work', 'consulting', 'support'])
                hours_used = np.random.uniform(1, 40)  # Hours used
                satisfaction_rating = np.random.uniform(1, 10)
                sla_breaches = np.random.choice([0, 1], p=[0.9, 0.1])
                
                usage_record = {
                    'usage_id': f"USE-{i+1:03d}-{j+1:02d}",
                    'client_id': client_id,
                    'usage_date': usage_date,
                    'service_type': service_type,
                    'hours_used': hours_used,
                    'satisfaction_rating': satisfaction_rating,
                    'sla_breaches': sla_breaches,
                    'support_tickets': np.random.randint(0, 5)
                }
                usage.append(usage_record)
        
        return pd.DataFrame(usage)


# Global instance for easy access
churn_data_preparator_instance = None


async def get_churn_data_preparator() -> ChurnDataPreparator:
    """Get singleton churn data preparator instance"""
    global churn_data_preparator_instance
    if churn_data_preparator_instance is None:
        churn_data_preparator_instance = ChurnDataPreparator()
    return churn_data_preparator_instance