"""
Data Preparation for Revenue Leak Detection
Handles collection and preprocessing of invoice, billing, and service delivery data
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


class RevenueLeakDataPreparator:
    """Prepares data for revenue leak detection"""
    
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
        self.data_dir = "../../data/revenue_leak_detector"
        logger.info("Revenue Leak Data Preparator initialized")
    
    async def collect_invoice_data(self, start_date: Optional[datetime] = None, 
                                 end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect invoice and billing data from QuickBooks or CSV files
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with invoice data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=90)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # If QuickBooks client is available, use it
            try:
                if self.quickbooks_client is not None:
                    # QuickBooks client returns invoices and payments
                    data = await self.quickbooks_client.get_invoices_and_payments(
                        start_date=start_date,
                        end_date=end_date
                    )
                    return pd.DataFrame(data.get('invoices', []))
                else:
                    # Return data from CSV files
                    logger.info("QuickBooks client not available, reading from CSV files")
                    csv_path = f"{self.data_dir}/invoice_data.csv"
                    if os.path.exists(csv_path):
                        return pd.read_csv(csv_path, parse_dates=['invoice_date', 'due_date'])
                    else:
                        # Fallback to mock data if CSV files don't exist
                        logger.warning("CSV files not found, returning mock data")
                        return self._generate_mock_invoice_data(start_date, end_date)
            except Exception as e:
                logger.error(f"Error collecting invoice data: {e}")
                # Fallback to mock data
                return self._generate_mock_invoice_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting invoice data: {e}")
            return self._generate_mock_invoice_data(start_date, end_date)
    
    async def collect_time_log_data(self, start_date: Optional[datetime] = None, 
                                  end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect time log data from SuperOps or CSV files
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with time log data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=90)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # If SuperOps client is available, use it
            try:
                if self.superops_client is not None:
                    # For now, we'll use mock data since we don't have a specific time logs method
                    logger.warning("SuperOps client available but using CSV data for time logs")
                    csv_path = f"{self.data_dir}/time_log_data.csv"
                    if os.path.exists(csv_path):
                        return pd.read_csv(csv_path, parse_dates=['start_time', 'end_time'])
                    else:
                        # Fallback to mock data if CSV files don't exist
                        logger.warning("CSV files not found, returning mock data")
                        return self._generate_mock_time_log_data(start_date, end_date)
                else:
                    # Return data from CSV files
                    logger.info("SuperOps client not available, reading from CSV files")
                    csv_path = f"{self.data_dir}/time_log_data.csv"
                    if os.path.exists(csv_path):
                        return pd.read_csv(csv_path, parse_dates=['start_time', 'end_time'])
                    else:
                        # Fallback to mock data if CSV files don't exist
                        logger.warning("CSV files not found, returning mock data")
                        return self._generate_mock_time_log_data(start_date, end_date)
            except Exception as e:
                logger.error(f"Error collecting time log data: {e}")
                # Fallback to mock data
                return self._generate_mock_time_log_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting time log data: {e}")
            return self._generate_mock_time_log_data(start_date, end_date)
    
    async def collect_service_delivery_data(self, start_date: Optional[datetime] = None, 
                                          end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect service delivery metrics from SuperOps or CSV files
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with service delivery data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=90)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # If SuperOps client is available, use it
            try:
                if self.superops_client is not None:
                    # Convert ServiceDeliveryMetrics objects to dictionaries
                    metrics = await self.superops_client.get_service_delivery_metrics(
                        start_date=start_date,
                        end_date=end_date
                    )
                    service_data = [vars(metric) for metric in metrics]
                    return pd.DataFrame(service_data)
                else:
                    # Return data from CSV files
                    logger.info("SuperOps client not available, reading from CSV files")
                    csv_path = f"{self.data_dir}/service_data.csv"
                    if os.path.exists(csv_path):
                        return pd.read_csv(csv_path, parse_dates=['service_date'])
                    else:
                        # Fallback to mock data if CSV files don't exist
                        logger.warning("CSV files not found, returning mock data")
                        return self._generate_mock_service_data(start_date, end_date)
            except Exception as e:
                logger.error(f"Error collecting service delivery data: {e}")
                # Fallback to mock data
                return self._generate_mock_service_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting service delivery data: {e}")
            return self._generate_mock_service_data(start_date, end_date)
    
    def _generate_mock_invoice_data(self, start_date: datetime, 
                                  end_date: datetime) -> pd.DataFrame:
        """Generate mock invoice data for testing"""
        # Generate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate mock data
        data = []
        for date in date_range:
            for i in range(np.random.randint(1, 10)):  # 1-10 invoices per day
                data.append({
                    'invoice_id': f'INV-{date.strftime("%Y%m%d")}-{i:03d}',
                    'client_id': f'CLIENT-{np.random.randint(1, 100):03d}',
                    'invoice_date': date,
                    'due_date': date + timedelta(days=30),
                    'amount': np.random.uniform(100, 5000),
                    'paid_amount': np.random.uniform(0, 5000),
                    'status': np.random.choice(['paid', 'unpaid', 'overdue'], p=[0.7, 0.2, 0.1]),
                    'service_type': np.random.choice(['managed_services', 'project_work', 'consulting']),
                    'billing_period': f'{date.strftime("%Y-%m")}'
                })
        
        return pd.DataFrame(data)
    
    def _generate_mock_time_log_data(self, start_date: datetime, 
                                   end_date: datetime) -> pd.DataFrame:
        """Generate mock time log data for testing"""
        # Generate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate mock data
        data = []
        for date in date_range:
            for i in range(np.random.randint(5, 50)):  # 5-50 time logs per day
                data.append({
                    'time_log_id': f'TL-{date.strftime("%Y%m%d")}-{i:03d}',
                    'technician_id': f'TECH-{np.random.randint(1, 20):02d}',
                    'client_id': f'CLIENT-{np.random.randint(1, 100):03d}',
                    'ticket_id': f'TKT-{np.random.randint(1, 1000):04d}',
                    'start_time': datetime.combine(date, datetime.min.time()) + timedelta(hours=np.random.randint(8, 18)),
                    'end_time': datetime.combine(date, datetime.min.time()) + timedelta(hours=np.random.randint(18, 22)),
                    'hours_logged': np.random.uniform(0.5, 8),
                    'service_type': np.random.choice(['managed_services', 'project_work', 'consulting', 'support']),
                    'billable': np.random.choice([True, False], p=[0.85, 0.15])
                })
        
        return pd.DataFrame(data)
    
    def _generate_mock_service_data(self, start_date: datetime, 
                                  end_date: datetime) -> pd.DataFrame:
        """Generate mock service delivery data for testing"""
        # Generate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate mock data
        data = []
        for date in date_range:
            for i in range(np.random.randint(10, 100)):  # 10-100 service records per day
                data.append({
                    'service_id': f'SVC-{date.strftime("%Y%m%d")}-{i:03d}',
                    'client_id': f'CLIENT-{np.random.randint(1, 100):03d}',
                    'ticket_id': f'TKT-{np.random.randint(1, 1000):04d}',
                    'service_date': date,
                    'service_type': np.random.choice(['managed_services', 'project_work', 'consulting', 'support']),
                    'hours_billed': np.random.uniform(0, 8),
                    'hours_actual': np.random.uniform(0, 10),
                    'rate': np.random.uniform(50, 200),
                    'total_billed': np.random.uniform(0, 1600),
                    'sla_met': np.random.choice([True, False], p=[0.9, 0.1]),
                    'technician_id': f'TECH-{np.random.randint(1, 20):02d}'
                })
        
        return pd.DataFrame(data)
    
    def identify_historical_anomalies(self, invoice_data: pd.DataFrame, 
                                    time_log_data: pd.DataFrame,
                                    service_data: pd.DataFrame) -> pd.DataFrame:
        """
        Identify historical anomaly patterns in the data
        
        Args:
            invoice_data: Invoice data
            time_log_data: Time log data
            service_data: Service delivery data
            
        Returns:
            DataFrame with identified anomalies
        """
        try:
            anomalies = []
            
            # Identify invoice anomalies (unpaid invoices, discrepancies)
            invoice_anomalies = self._find_invoice_anomalies(invoice_data)
            anomalies.extend(invoice_anomalies)
            
            # Identify time log anomalies (unbilled time, excessive hours)
            time_log_anomalies = self._find_time_log_anomalies(time_log_data)
            anomalies.extend(time_log_anomalies)
            
            # Identify service delivery anomalies (underbilled services)
            service_anomalies = self._find_service_anomalies(service_data)
            anomalies.extend(service_anomalies)
            
            return pd.DataFrame(anomalies)
            
        except Exception as e:
            logger.error(f"Error identifying historical anomalies: {e}")
            return pd.DataFrame()
    
    def _find_invoice_anomalies(self, invoice_data: pd.DataFrame) -> List[Dict]:
        """Find anomalies in invoice data"""
        anomalies = []
        
        # Unpaid invoices
        unpaid_invoices = invoice_data[invoice_data['status'] == 'unpaid']
        for _, invoice in unpaid_invoices.iterrows():
            anomalies.append({
                'anomaly_type': 'unpaid_invoice',
                'client_id': invoice['client_id'],
                'amount': invoice['amount'],
                'description': f"Unpaid invoice {invoice['invoice_id']}",
                'severity': 'medium',
                'potential_loss': invoice['amount'] - invoice['paid_amount']
            })
        
        # Overdue invoices
        overdue_invoices = invoice_data[invoice_data['status'] == 'overdue']
        for _, invoice in overdue_invoices.iterrows():
            anomalies.append({
                'anomaly_type': 'overdue_invoice',
                'client_id': invoice['client_id'],
                'amount': invoice['amount'],
                'description': f"Overdue invoice {invoice['invoice_id']}",
                'severity': 'high',
                'potential_loss': invoice['amount'] - invoice['paid_amount']
            })
        
        return anomalies
    
    def _find_time_log_anomalies(self, time_log_data: pd.DataFrame) -> List[Dict]:
        """Find anomalies in time log data"""
        anomalies = []
        
        # Unbilled time logs
        unbilled_logs = time_log_data[~time_log_data['billable']]
        for _, log in unbilled_logs.iterrows():
            anomalies.append({
                'anomaly_type': 'unbilled_time',
                'client_id': log['client_id'],
                'amount': log['hours_logged'] * 100,  # Assuming $100/hour rate
                'description': f"Unbilled time log {log['time_log_id']}",
                'severity': 'medium',
                'potential_loss': log['hours_logged'] * 100
            })
        
        # Excessive hours
        excessive_hours = time_log_data[time_log_data['hours_logged'] > 8]
        for _, log in excessive_hours.iterrows():
            anomalies.append({
                'anomaly_type': 'excessive_hours',
                'client_id': log['client_id'],
                'amount': log['hours_logged'] * 100,
                'description': f"Excessive hours in time log {log['time_log_id']}",
                'severity': 'low',
                'potential_loss': 0  # Not necessarily a loss
            })
        
        return anomalies
    
    def _find_service_anomalies(self, service_data: pd.DataFrame) -> List[Dict]:
        """Find anomalies in service delivery data"""
        anomalies = []
        
        # Underbilled services (actual hours > billed hours)
        underbilled = service_data[service_data['hours_actual'] > service_data['hours_billed']]
        for _, service in underbilled.iterrows():
            unbilled_hours = service['hours_actual'] - service['hours_billed']
            anomalies.append({
                'anomaly_type': 'underbilled_service',
                'client_id': service['client_id'],
                'amount': unbilled_hours * service['rate'],
                'description': f"Underbilled service {service['service_id']}",
                'severity': 'medium',
                'potential_loss': unbilled_hours * service['rate']
            })
        
        return anomalies
    
    def prepare_features(self, invoice_data: pd.DataFrame, 
                        time_log_data: pd.DataFrame,
                        service_data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for anomaly detection
        
        Args:
            invoice_data: Invoice data
            time_log_data: Time log data
            service_data: Service delivery data
            
        Returns:
            DataFrame with prepared features
        """
        try:
            # Create client-level features
            features = []
            
            # Get unique clients
            clients = set()
            clients.update(invoice_data['client_id'].unique() if 'client_id' in invoice_data.columns else [])
            clients.update(time_log_data['client_id'].unique() if 'client_id' in time_log_data.columns else [])
            clients.update(service_data['client_id'].unique() if 'client_id' in service_data.columns else [])
            
            for client_id in clients:
                client_features = self._extract_client_features(
                    client_id, invoice_data, time_log_data, service_data
                )
                features.append(client_features)
            
            return pd.DataFrame(features)
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            return pd.DataFrame()
    
    def _extract_client_features(self, client_id: str, 
                               invoice_data: pd.DataFrame,
                               time_log_data: pd.DataFrame,
                               service_data: pd.DataFrame) -> Dict[str, Any]:
        """Extract features for a specific client"""
        features = {'client_id': client_id}
        
        # Invoice features
        client_invoices = invoice_data[invoice_data['client_id'] == client_id] if 'client_id' in invoice_data.columns else pd.DataFrame()
        features['total_invoiced'] = client_invoices['amount'].sum() if 'amount' in client_invoices.columns else 0  # type: ignore
        features['total_paid'] = client_invoices['paid_amount'].sum() if 'paid_amount' in client_invoices.columns else 0  # type: ignore
        features['unpaid_amount'] = features['total_invoiced'] - features['total_paid']  # type: ignore
        features['unpaid_invoice_count'] = len(client_invoices[client_invoices['status'] == 'unpaid']) if 'status' in client_invoices.columns else 0  # type: ignore
        features['overdue_invoice_count'] = len(client_invoices[client_invoices['status'] == 'overdue']) if 'status' in client_invoices.columns else 0  # type: ignore
        
        # Time log features
        client_time_logs = time_log_data[time_log_data['client_id'] == client_id] if 'client_id' in time_log_data.columns else pd.DataFrame()
        features['total_hours_logged'] = client_time_logs['hours_logged'].sum() if 'hours_logged' in client_time_logs.columns else 0  # type: ignore
        features['unbilled_hours'] = client_time_logs[~client_time_logs['billable']]['hours_logged'].sum() if 'billable' in client_time_logs.columns and 'hours_logged' in client_time_logs.columns else 0  # type: ignore
        features['excessive_hours_count'] = len(client_time_logs[client_time_logs['hours_logged'] > 8]) if 'hours_logged' in client_time_logs.columns else 0  # type: ignore
        
        # Service delivery features
        client_services = service_data[service_data['client_id'] == client_id] if 'client_id' in service_data.columns else pd.DataFrame()
        features['total_service_hours_billed'] = client_services['hours_billed'].sum() if 'hours_billed' in client_services.columns else 0  # type: ignore
        features['total_service_hours_actual'] = client_services['hours_actual'].sum() if 'hours_actual' in client_services.columns else 0  # type: ignore
        features['underbilled_hours'] = features['total_service_hours_actual'] - features['total_service_hours_billed']  # type: ignore
        features['sla_violation_count'] = len(client_services[~client_services['sla_met']]) if 'sla_met' in client_services.columns else 0  # type: ignore
        
        # Derived features
        total_invoiced = float(features['total_invoiced'])
        total_paid = float(features['total_paid'])
        total_hours_logged = float(features['total_hours_logged'])
        total_service_hours_billed = float(features['total_service_hours_billed'])
        
        features['payment_ratio'] = total_paid / total_invoiced if total_invoiced > 0 else 0  # type: ignore
        features['billing_efficiency'] = total_service_hours_billed / total_hours_logged if total_hours_logged > 0 else 0  # type: ignore
        features['revenue_leak_score'] = (
            float(features['unpaid_amount']) + 
            float(features['unbilled_hours']) * 100 +  # Assuming $100/hour
            float(features['underbilled_hours']) * 100  # Assuming $100/hour
        )  # type: ignore
        
        return features


# Global instance for easy access
data_preparator_instance = None


async def get_data_preparator() -> RevenueLeakDataPreparator:
    """Get singleton data preparator instance"""
    global data_preparator_instance
    if data_preparator_instance is None:
        data_preparator_instance = RevenueLeakDataPreparator()
    return data_preparator_instance
