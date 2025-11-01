"""
Data Preparation for Service Demand Forecaster
Handles collection and preprocessing of time series data, historical tickets, seasonal patterns, and external factors
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


class DemandDataPreparator:
    """Prepares data for demand forecasting model"""
    
    def __init__(self):
        """Initialize the data preparator"""
        # Path to CSV data files
        self.data_dir = "../../data/demand_forecaster"
        logger.info("Demand Data Preparator initialized")
    
    async def collect_historical_ticket_data(self, start_date: Optional[datetime] = None, 
                                         end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect historical ticket data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with historical ticket data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=730)  # 2 years
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading historical ticket data from CSV files")
            csv_path = f"{self.data_dir}/historical_tickets.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_ticket_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting historical ticket data: {e}")
            return self._generate_mock_ticket_data(start_date, end_date)
    
    async def collect_client_growth_data(self, start_date: Optional[datetime] = None, 
                                     end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect client growth data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with client growth data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=730)  # 2 years
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading client growth data from CSV files")
            csv_path = f"{self.data_dir}/client_growth_data.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_client_growth_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting client growth data: {e}")
            return self._generate_mock_client_growth_data(start_date, end_date)
    
    async def collect_seasonal_pattern_data(self, start_date: Optional[datetime] = None, 
                                        end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect seasonal pattern data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with seasonal pattern data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=730)  # 2 years
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading seasonal pattern data from CSV files")
            csv_path = f"{self.data_dir}/seasonal_patterns.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_seasonal_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting seasonal pattern data: {e}")
            return self._generate_mock_seasonal_data(start_date, end_date)
    
    async def collect_external_factor_data(self, start_date: Optional[datetime] = None, 
                                       end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect external factor data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with external factor data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=730)  # 2 years
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading external factor data from CSV files")
            csv_path = f"{self.data_dir}/external_factors.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_external_factor_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting external factor data: {e}")
            return self._generate_mock_external_factor_data(start_date, end_date)
    
    async def collect_resource_capacity_data(self, start_date: Optional[datetime] = None, 
                                         end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect resource capacity data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with resource capacity data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=730)  # 2 years
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading resource capacity data from CSV files")
            csv_path = f"{self.data_dir}/resource_capacity.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_resource_capacity_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting resource capacity data: {e}")
            return self._generate_mock_resource_capacity_data(start_date, end_date)
    
    def _generate_mock_ticket_data(self, start_date: datetime, 
                               end_date: datetime) -> pd.DataFrame:
        """Generate mock historical ticket data for testing"""
        # Generate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate ticket data with realistic patterns
        tickets = []
        
        for date in date_range:
            # Base ticket count with trend and seasonality
            base_tickets = 20  # Average daily tickets
            
            # Add trend (growth over time)
            days_since_start = (date - start_date).days
            trend = 0.02 * days_since_start  # 2% growth per 100 days
            
            # Add seasonality (weekly pattern)
            day_of_week = date.weekday()
            weekly_pattern = [0.7, 0.8, 1.0, 1.1, 1.2, 0.9, 0.6]  # Monday-Friday peak, weekend low
            weekly_effect = weekly_pattern[day_of_week]
            
            # Add some randomness
            noise = np.random.normal(0, 3)
            
            # Calculate final ticket count
            ticket_count = max(0, int(base_tickets * (1 + trend/100) * weekly_effect + noise))
            
            # Ticket types
            ticket_types = ['Bug Fix', 'Feature Request', 'Consultation', 'Maintenance', 'Emergency']
            ticket_type = np.random.choice(ticket_types, p=[0.3, 0.25, 0.2, 0.15, 0.1])
            
            # Priority levels
            priorities = ['Low', 'Medium', 'High', 'Critical']
            priority = np.random.choice(priorities, p=[0.4, 0.35, 0.2, 0.05])
            
            # Client categories
            client_categories = ['Enterprise', 'Mid-Market', 'SMB', 'Startup']
            client_category = np.random.choice(client_categories, p=[0.2, 0.3, 0.35, 0.15])
            
            ticket = {
                'date': date.strftime('%Y-%m-%d'),
                'ticket_count': ticket_count,
                'ticket_type': ticket_type,
                'priority': priority,
                'client_category': client_category,
                'avg_resolution_time_hours': np.random.uniform(2, 24),
                'satisfaction_score': np.random.uniform(1, 10)
            }
            tickets.append(ticket)
        
        return pd.DataFrame(tickets)
    
    def _generate_mock_client_growth_data(self, start_date: datetime, 
                                      end_date: datetime) -> pd.DataFrame:
        """Generate mock client growth data for testing"""
        # Generate monthly data points
        date_range = pd.date_range(start=start_date, end=end_date, freq='M')
        
        clients = []
        base_client_count = 50
        
        for i, date in enumerate(date_range):
            # Add growth trend
            growth = 0.05 * i  # 5% growth per month
            client_count = int(base_client_count * (1 + growth))
            
            # Add some randomness
            client_count += np.random.randint(-5, 10)
            client_count = max(0, client_count)
            
            # Client segments
            segments = ['Enterprise', 'Mid-Market', 'SMB', 'Startup']
            segment_distribution = {
                'Enterprise': int(client_count * 0.15),
                'Mid-Market': int(client_count * 0.30),
                'SMB': int(client_count * 0.40),
                'Startup': int(client_count * 0.15)
            }
            
            client = {
                'date': date.strftime('%Y-%m-%d'),
                'total_clients': client_count,
                'enterprise_clients': segment_distribution['Enterprise'],
                'mid_market_clients': segment_distribution['Mid-Market'],
                'smb_clients': segment_distribution['SMB'],
                'startup_clients': segment_distribution['Startup'],
                'new_clients': np.random.randint(0, 10),
                'churned_clients': np.random.randint(0, 3),
                'expansion_revenue': np.random.uniform(5000, 50000)
            }
            clients.append(client)
        
        return pd.DataFrame(clients)
    
    def _generate_mock_seasonal_data(self, start_date: datetime, 
                                 end_date: datetime) -> pd.DataFrame:
        """Generate mock seasonal pattern data for testing"""
        # Generate weekly data points
        date_range = pd.date_range(start=start_date, end=end_date, freq='W')
        
        patterns = []
        
        for date in date_range:
            # Seasonal factors for different periods
            month = date.month
            day_of_week = date.weekday()
            
            # Monthly seasonality
            if month in [11, 12]:  # Holiday season
                monthly_factor = 1.3
            elif month in [6, 7, 8]:  # Summer
                monthly_factor = 0.8
            else:
                monthly_factor = 1.0
            
            # Weekly seasonality
            weekly_pattern = [0.7, 0.8, 1.0, 1.1, 1.2, 0.9, 0.6]  # Monday-Friday peak, weekend low
            weekly_factor = weekly_pattern[day_of_week]
            
            pattern = {
                'date': date.strftime('%Y-%m-%d'),
                'monthly_seasonality': monthly_factor,
                'weekly_seasonality': weekly_factor,
                'business_days_factor': 1.0 if day_of_week < 5 else 0.3,
                'quarterly_trend': 1.0 + (date.quarter - 2) * 0.05,  # Q2 baseline, Q1/Q3 variations
                'holiday_effect': 1.0 + (0.5 if month == 12 and date.day > 20 else 0),
                'vacation_season': 0.8 if month in [7, 8] else 1.0
            }
            patterns.append(pattern)
        
        return pd.DataFrame(patterns)
    
    def _generate_mock_external_factor_data(self, start_date: datetime, 
                                        end_date: datetime) -> pd.DataFrame:
        """Generate mock external factor data for testing"""
        # Generate daily data points
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        factors = []
        
        for date in date_range:
            # Economic indicators
            gdp_growth = np.random.normal(2.5, 0.5)  # GDP growth rate
            inflation_rate = np.random.normal(2.0, 0.3)  # Inflation rate
            unemployment_rate = np.random.normal(4.0, 0.4)  # Unemployment rate
            
            # Market conditions
            market_volatility = np.random.uniform(0, 2)
            competitor_activity = np.random.uniform(0, 10)
            
            # Events
            is_holiday = date.weekday() >= 5 or (date.month == 12 and date.day > 24)
            is_conference = np.random.random() < 0.02  # 2% chance of conference
            is_product_launch = np.random.random() < 0.01  # 1% chance of product launch
            
            factor = {
                'date': date.strftime('%Y-%m-%d'),
                'gdp_growth_rate': gdp_growth,
                'inflation_rate': inflation_rate,
                'unemployment_rate': unemployment_rate,
                'market_volatility_index': market_volatility,
                'competitor_activity_score': competitor_activity,
                'is_holiday': int(is_holiday),
                'is_conference': int(is_conference),
                'is_product_launch': int(is_product_launch),
                'economic_sentiment': np.random.uniform(-1, 1),
                'industry_growth': np.random.uniform(-0.05, 0.1)
            }
            factors.append(factor)
        
        return pd.DataFrame(factors)
    
    def _generate_mock_resource_capacity_data(self, start_date: datetime, 
                                          end_date: datetime) -> pd.DataFrame:
        """Generate mock resource capacity data for testing"""
        # Generate monthly data points
        date_range = pd.date_range(start=start_date, end=end_date, freq='M')
        
        capacities = []
        
        for date in date_range:
            # Resource types
            resource_types = ['Developer', 'Designer', 'QA Engineer', 'DevOps', 'Support']
            
            for resource_type in resource_types:
                # Base capacity
                base_capacity = np.random.uniform(100, 200)  # Hours per month
                
                # Seasonal adjustments
                month = date.month
                if month in [11, 12]:  # Holiday season
                    capacity_factor = 0.8
                elif month in [6, 7, 8]:  # Summer vacation
                    capacity_factor = 0.9
                else:
                    capacity_factor = 1.0
                
                # Trend adjustments
                days_since_start = (date - start_date).days
                trend = 0.01 * (days_since_start / 30)  # 1% growth per month
                
                available_capacity = base_capacity * capacity_factor * (1 + trend)
                utilized_capacity = available_capacity * np.random.uniform(0.6, 0.95)
                
                capacity = {
                    'date': date.strftime('%Y-%m-%d'),
                    'resource_type': resource_type,
                    'available_capacity_hours': available_capacity,
                    'utilized_capacity_hours': utilized_capacity,
                    'utilization_rate': utilized_capacity / available_capacity,
                    'planned_expansion': np.random.uniform(0, 20),
                    'training_hours': np.random.uniform(0, 40)
                }
                capacities.append(capacity)
        
        return pd.DataFrame(capacities)


# Global instance for easy access
demand_data_preparator_instance = None


async def get_demand_data_preparator() -> DemandDataPreparator:
    """Get singleton demand data preparator instance"""
    global demand_data_preparator_instance
    if demand_data_preparator_instance is None:
        demand_data_preparator_instance = DemandDataPreparator()
    return demand_data_preparator_instance