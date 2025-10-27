"""
Historical Financial Data Collector for Client Profitability Prediction
Collects and processes historical financial data from multiple sources
"""

import pandas as pd
import numpy as np
import sqlite3
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class HistoricalDataCollector:
    """Collects historical financial data from all sources"""
    
    def __init__(self, db_path: str = "../../database/superhack.db"):
        """
        Initialize the data collector
        
        Args:
            db_path: Path to the SQLite database
        """
        self.db_path = db_path
        
    def collect_client_data(self) -> pd.DataFrame:
        """
        Collect client profile data
        
        Returns:
            DataFrame with client data
        """
        logger.info("Collecting client data")
        
        try:
            conn = sqlite3.connect(self.db_path)
            clients_df = pd.read_sql_query("""
                SELECT id, name, industry, contract_type, contract_value, 
                       start_date, end_date, is_active
                FROM clients
            """, conn)
            conn.close()
            
            logger.info(f"Collected data for {len(clients_df)} clients")
            return clients_df
            
        except Exception as e:
            logger.error(f"Error collecting client data: {e}")
            raise
    
    def collect_invoice_data(self) -> pd.DataFrame:
        """
        Collect invoice data
        
        Returns:
            DataFrame with invoice data
        """
        logger.info("Collecting invoice data")
        
        try:
            conn = sqlite3.connect(self.db_path)
            invoices_df = pd.read_sql_query("""
                SELECT client_id, invoice_date, total_amount, status
                FROM invoices
            """, conn)
            conn.close()
            
            logger.info(f"Collected {len(invoices_df)} invoice records")
            return invoices_df
            
        except Exception as e:
            logger.error(f"Error collecting invoice data: {e}")
            raise
    
    def collect_ticket_data(self) -> pd.DataFrame:
        """
        Collect ticket data
        
        Returns:
            DataFrame with ticket data
        """
        logger.info("Collecting ticket data")
        
        try:
            conn = sqlite3.connect(self.db_path)
            tickets_df = pd.read_sql_query("""
                SELECT client_id, time_spent, billable_hours, hourly_rate
                FROM tickets
            """, conn)
            conn.close()
            
            logger.info(f"Collected {len(tickets_df)} ticket records")
            return tickets_df
            
        except Exception as e:
            logger.error(f"Error collecting ticket data: {e}")
            raise
    
    def collect_service_data(self) -> pd.DataFrame:
        """
        Collect service data
        
        Returns:
            DataFrame with service data
        """
        logger.info("Collecting service data")
        
        try:
            conn = sqlite3.connect(self.db_path)
            services_df = pd.read_sql_query("""
                SELECT cs.client_id, s.category, cs.custom_price, cs.quantity
                FROM client_services cs
                JOIN services s ON cs.service_id = s.id
            """, conn)
            conn.close()
            
            logger.info(f"Collected {len(services_df)} service records")
            return services_df
            
        except Exception as e:
            logger.error(f"Error collecting service data: {e}")
            raise
    
    def aggregate_financial_metrics(self) -> pd.DataFrame:
        """
        Aggregate all financial data into client-level metrics
        
        Returns:
            DataFrame with aggregated financial metrics per client
        """
        logger.info("Aggregating financial metrics")
        
        try:
            # Collect all data
            clients_df = self.collect_client_data()
            invoices_df = self.collect_invoice_data()
            tickets_df = self.collect_ticket_data()
            services_df = self.collect_service_data()
            
            # Calculate total revenue per client
            client_revenue = invoices_df.groupby('client_id')['total_amount'].sum().reset_index()
            client_revenue.columns = ['id', 'total_revenue']
            
            # Calculate total costs per client (from tickets)
            tickets_df['ticket_cost'] = tickets_df['time_spent'] * tickets_df['hourly_rate']
            client_costs = tickets_df.groupby('client_id')['ticket_cost'].sum().reset_index()
            client_costs.columns = ['id', 'ticket_cost']
            
            # Calculate service utilization metrics
            service_metrics = services_df.groupby('client_id').agg({
                'custom_price': ['count', 'sum'],
                'quantity': 'sum'
            }).reset_index()
            service_metrics.columns = ['id', 'service_count', 'total_service_value', 'total_quantity']
            
            # Merge all data
            merged_df = clients_df.merge(client_revenue, on='id', how='left')
            merged_df = merged_df.merge(client_costs, on='id', how='left')
            merged_df = merged_df.merge(service_metrics, on='id', how='left')
            
            # Fill NaN values
            merged_df['total_costs'] = merged_df['ticket_cost'].fillna(0)
            merged_df['service_count'] = merged_df['service_count'].fillna(0)
            merged_df['total_service_value'] = merged_df['total_service_value'].fillna(0)
            merged_df['total_quantity'] = merged_df['total_quantity'].fillna(0)
            
            # Calculate profitability metrics
            merged_df['profit'] = merged_df['total_revenue'] - merged_df['total_costs']
            merged_df['profit_margin'] = np.where(
                merged_df['total_revenue'] > 0,
                merged_df['profit'] / merged_df['total_revenue'],
                0
            )
            
            # Calculate additional metrics
            merged_df['revenue_per_service'] = np.where(
                merged_df['service_count'] > 0,
                merged_df['total_revenue'] / merged_df['service_count'],
                0
            )
            
            merged_df['cost_per_service'] = np.where(
                merged_df['service_count'] > 0,
                merged_df['total_costs'] / merged_df['service_count'],
                0
            )
            
            logger.info(f"Aggregated financial metrics for {len(merged_df)} clients")
            return merged_df
            
        except Exception as e:
            logger.error(f"Error aggregating financial metrics: {e}")
            raise


# Convenience function for easy usage
def collect_historical_financial_data(db_path: str = "../../database/superhack.db") -> pd.DataFrame:
    """
    Collect and aggregate historical financial data
    
    Args:
        db_path: Path to the SQLite database
        
    Returns:
        DataFrame with aggregated financial metrics per client
    """
    collector = HistoricalDataCollector(db_path)
    return collector.aggregate_financial_metrics()