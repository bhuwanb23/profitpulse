"""
Data Preparation for Dynamic Pricing Engine
Handles collection and preprocessing of market data, client values, and competitive pricing information
"""

import logging
import numpy as np
import pandas as pd
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class PricingDataPreparator:
    """Prepares data for dynamic pricing engine"""
    
    def __init__(self):
        """Initialize the data preparator"""
        # Path to CSV data files
        self.data_dir = "../../data/dynamic_pricing"
        logger.info("Pricing Data Preparator initialized")
    
    async def collect_market_rate_data(self, start_date: Optional[datetime] = None, 
                                    end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect market rate data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with market rate data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading market rate data from CSV files")
            csv_path = f"{self.data_dir}/market_rates.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path, parse_dates=['date'])
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_market_rate_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting market rate data: {e}")
            return self._generate_mock_market_rate_data(start_date, end_date)
    
    async def collect_client_value_data(self, start_date: Optional[datetime] = None, 
                                     end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect client value assessment data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with client value data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading client value data from CSV files")
            csv_path = f"{self.data_dir}/client_value_data.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_client_value_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting client value data: {e}")
            return self._generate_mock_client_value_data(start_date, end_date)
    
    async def collect_service_complexity_data(self, start_date: Optional[datetime] = None, 
                                           end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect service complexity metrics data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with service complexity data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading service complexity data from CSV files")
            csv_path = f"{self.data_dir}/service_complexity.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_service_complexity_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting service complexity data: {e}")
            return self._generate_mock_service_complexity_data(start_date, end_date)
    
    async def collect_competitive_pricing_data(self, start_date: Optional[datetime] = None, 
                                            end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect competitive pricing data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with competitive pricing data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading competitive pricing data from CSV files")
            csv_path = f"{self.data_dir}/competitive_pricing.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path, parse_dates=['date'])
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_competitive_pricing_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting competitive pricing data: {e}")
            return self._generate_mock_competitive_pricing_data(start_date, end_date)
    
    async def collect_pricing_history_data(self, start_date: Optional[datetime] = None, 
                                        end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect historical pricing and acceptance data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with pricing history data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading pricing history data from CSV files")
            csv_path = f"{self.data_dir}/pricing_history.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path, parse_dates=['date'])
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_pricing_history_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting pricing history data: {e}")
            return self._generate_mock_pricing_history_data(start_date, end_date)
    
    def _generate_mock_market_rate_data(self, start_date: datetime, 
                                     end_date: datetime) -> pd.DataFrame:
        """Generate mock market rate data for testing"""
        # Generate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate market rates with some trend and seasonality
        base_rate = 100
        trend = np.linspace(0, 20, len(date_range))  # Upward trend
        seasonal = 10 * np.sin(2 * np.pi * np.arange(len(date_range)) / 365)  # Annual seasonality
        noise = np.random.normal(0, 5, len(date_range))  # Random noise
        
        market_rates = base_rate + trend + seasonal + noise
        
        # Create DataFrame
        data = {
            'date': date_range,
            'service_type': np.random.choice(['managed_services', 'project_work', 'consulting'], len(date_range)),
            'market_rate': market_rates,
            'demand_index': np.random.uniform(0.5, 2.0, len(date_range)),  # Demand relative to average
            'competition_level': np.random.choice(['low', 'medium', 'high'], len(date_range))
        }
        
        return pd.DataFrame(data)
    
    def _generate_mock_client_value_data(self, start_date: datetime, 
                                      end_date: datetime) -> pd.DataFrame:
        """Generate mock client value assessment data for testing"""
        # Generate client data
        clients = []
        client_count = 100
        
        for i in range(client_count):
            client_id = f"CLIENT-{i+1:03d}"
            
            # Client value metrics
            client = {
                'client_id': client_id,
                'client_name': f"Client {i+1}",
                'revenue_contribution': np.random.uniform(1000, 50000),  # Annual revenue
                'profit_margin': np.random.uniform(0.1, 0.5),  # Profit margin
                'contract_length_months': np.random.choice([12, 24, 36, 48, 60]),  # Contract length
                'service_usage_frequency': np.random.uniform(1, 10),  # Usage frequency (times per month)
                'support_ticket_frequency': np.random.uniform(0, 5),  # Support tickets per month
                'satisfaction_score': np.random.uniform(1, 10),  # Satisfaction score
                'loyalty_score': np.random.uniform(0, 100),  # Loyalty score
                'growth_potential': np.random.uniform(0, 100),  # Growth potential score
                'price_sensitivity': np.random.uniform(0, 100),  # Price sensitivity (lower = less sensitive)
                'strategic_value': np.random.uniform(0, 100),  # Strategic value to business
                'industry': np.random.choice(['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing']),
                'company_size': np.random.choice(['Small', 'Medium', 'Large'])
            }
            clients.append(client)
        
        return pd.DataFrame(clients)
    
    def _generate_mock_service_complexity_data(self, start_date: datetime, 
                                            end_date: datetime) -> pd.DataFrame:
        """Generate mock service complexity metrics data for testing"""
        # Generate service data
        services = []
        service_count = 50
        
        for i in range(service_count):
            service_id = f"SERVICE-{i+1:03d}"
            
            # Service complexity metrics
            service = {
                'service_id': service_id,
                'service_name': f"Service {i+1}",
                'service_type': np.random.choice(['managed_services', 'project_work', 'consulting', 'support']),
                'technical_complexity': np.random.uniform(1, 10),  # Technical complexity score
                'resource_intensity': np.random.uniform(1, 10),  # Resource intensity score
                'skill_requirements': np.random.uniform(1, 10),  # Skill requirements score
                'time_sensitivity': np.random.uniform(1, 10),  # Time sensitivity score
                'customization_level': np.random.uniform(1, 10),  # Customization level score
                'integration_complexity': np.random.uniform(1, 10),  # Integration complexity score
                'regulatory_compliance': np.random.uniform(1, 10),  # Regulatory compliance score
                'maintenance_requirements': np.random.uniform(1, 10),  # Maintenance requirements score
                'scalability_index': np.random.uniform(1, 10),  # Scalability index
                'innovation_factor': np.random.uniform(1, 10)  # Innovation factor
            }
            services.append(service)
        
        return pd.DataFrame(services)
    
    def _generate_mock_competitive_pricing_data(self, start_date: datetime, 
                                             end_date: datetime) -> pd.DataFrame:
        """Generate mock competitive pricing data for testing"""
        # Generate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='W')
        
        # Generate competitive data
        competitors = []
        competitor_names = [f"Competitor {i+1}" for i in range(10)]
        service_types = ['managed_services', 'project_work', 'consulting', 'support']
        
        for date in date_range:
            for competitor in competitor_names:
                for service_type in service_types:
                    # Generate competitive pricing data
                    competitor_data = {
                        'date': date,
                        'competitor_name': competitor,
                        'service_type': service_type,
                        'avg_price': np.random.uniform(80, 150),  # Average price
                        'price_range_min': np.random.uniform(60, 120),  # Minimum price
                        'price_range_max': np.random.uniform(100, 200),  # Maximum price
                        'market_share': np.random.uniform(0.01, 0.3),  # Market share
                        'pricing_strategy': np.random.choice(['premium', 'competitive', 'value', 'penetration']),
                        'discount_offered': np.random.uniform(0, 0.3),  # Discount percentage
                        'service_quality_score': np.random.uniform(1, 10)  # Service quality score
                    }
                    competitors.append(competitor_data)
        
        return pd.DataFrame(competitors)
    
    def _generate_mock_pricing_history_data(self, start_date: datetime, 
                                         end_date: datetime) -> pd.DataFrame:
        """Generate mock pricing history and acceptance data for testing"""
        # Generate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate pricing history data
        pricing_data = []
        
        for date in date_range:
            # Generate data for different services
            for service_type in ['managed_services', 'project_work', 'consulting', 'support']:
                # Generate pricing history record
                record = {
                    'date': date,
                    'service_type': service_type,
                    'base_price': np.random.uniform(80, 150),  # Base price
                    'discount_applied': np.random.uniform(0, 0.3),  # Discount percentage
                    'final_price': np.random.uniform(60, 150),  # Final price after discount
                    'units_sold': np.random.randint(1, 100),  # Units sold
                    'revenue_generated': np.random.uniform(1000, 15000),  # Revenue generated
                    'client_acceptance_rate': np.random.uniform(0.6, 1.0),  # Acceptance rate
                    'price_elasticity': np.random.uniform(-2, -0.1),  # Price elasticity
                    'seasonal_factor': np.random.uniform(0.8, 1.2),  # Seasonal factor
                    'promotion_applied': np.random.choice([True, False], p=[0.2, 0.8])  # Promotion applied
                }
                pricing_data.append(record)
        
        return pd.DataFrame(pricing_data)


# Global instance for easy access
pricing_data_preparator_instance = None


async def get_pricing_data_preparator() -> PricingDataPreparator:
    """Get singleton pricing data preparator instance"""
    global pricing_data_preparator_instance
    if pricing_data_preparator_instance is None:
        pricing_data_preparator_instance = PricingDataPreparator()
    return pricing_data_preparator_instance