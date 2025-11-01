"""
Data Preparation for Budget Optimization Model
Handles collection and preprocessing of budget data, service costs, client priorities, and ROI information
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


class BudgetDataPreparator:
    """Prepares data for budget optimization model"""
    
    def __init__(self):
        """Initialize the data preparator"""
        # Path to CSV data files
        self.data_dir = "../../data/budget_optimizer"
        logger.info("Budget Data Preparator initialized")
    
    async def collect_budget_data(self, start_date: Optional[datetime] = None, 
                              end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect budget data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with budget data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading budget data from CSV files")
            csv_path = f"{self.data_dir}/budget_data.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_budget_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting budget data: {e}")
            return self._generate_mock_budget_data(start_date, end_date)
    
    async def collect_service_cost_data(self, start_date: Optional[datetime] = None, 
                                    end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect service cost analysis data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with service cost data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading service cost data from CSV files")
            csv_path = f"{self.data_dir}/service_costs.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_service_cost_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting service cost data: {e}")
            return self._generate_mock_service_cost_data(start_date, end_date)
    
    async def collect_client_priority_data(self, start_date: Optional[datetime] = None, 
                                       end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect client priority assessment data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with client priority data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading client priority data from CSV files")
            csv_path = f"{self.data_dir}/client_priorities.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_client_priority_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting client priority data: {e}")
            return self._generate_mock_client_priority_data(start_date, end_date)
    
    async def collect_roi_data(self, start_date: Optional[datetime] = None, 
                           end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect ROI data for optimization
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with ROI data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading ROI data from CSV files")
            csv_path = f"{self.data_dir}/roi_data.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_roi_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting ROI data: {e}")
            return self._generate_mock_roi_data(start_date, end_date)
    
    async def collect_resource_data(self, start_date: Optional[datetime] = None, 
                                end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Collect resource availability and cost data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            DataFrame with resource data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
            
        try:
            # Return data from CSV files
            logger.info("Reading resource data from CSV files")
            csv_path = f"{self.data_dir}/resource_data.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                # Fallback to mock data
                logger.warning("CSV files not found, returning mock data")
                return self._generate_mock_resource_data(start_date, end_date)
                
        except Exception as e:
            logger.error(f"Error collecting resource data: {e}")
            return self._generate_mock_resource_data(start_date, end_date)
    
    def _generate_mock_budget_data(self, start_date: datetime, 
                               end_date: datetime) -> pd.DataFrame:
        """Generate mock budget data for testing"""
        # Generate budget data
        budgets = []
        budget_count = 20
        
        for i in range(budget_count):
            budget_id = f"BUDGET-{i+1:03d}"
            
            # Budget constraints
            budget = {
                'budget_id': budget_id,
                'department': np.random.choice(['IT', 'Marketing', 'Sales', 'Operations', 'HR']),
                'fiscal_year': np.random.choice([2024, 2025, 2026]),
                'total_budget': np.random.uniform(50000, 500000),  # Total budget amount
                'allocated_amount': np.random.uniform(30000, 400000),  # Already allocated
                'remaining_budget': np.random.uniform(10000, 150000),  # Remaining budget
                'budget_category': np.random.choice(['Salaries', 'Equipment', 'Software', 'Training', 'Travel']),
                'priority_level': np.random.choice(['High', 'Medium', 'Low']),
                'budget_owner': f"Manager {i+1}",
                'approval_status': np.random.choice(['Approved', 'Pending', 'Rejected']),
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
            budgets.append(budget)
        
        return pd.DataFrame(budgets)
    
    def _generate_mock_service_cost_data(self, start_date: datetime, 
                                     end_date: datetime) -> pd.DataFrame:
        """Generate mock service cost data for testing"""
        # Generate service data
        services = []
        service_count = 30
        
        for i in range(service_count):
            service_id = f"SERVICE-{i+1:03d}"
            
            # Service costs
            service = {
                'service_id': service_id,
                'service_name': f"Service {i+1}",
                'service_type': np.random.choice(['Managed Services', 'Project Work', 'Consulting', 'Support']),
                'unit_cost': np.random.uniform(50, 500),  # Cost per unit
                'average_duration_hours': np.random.uniform(10, 200),  # Average service duration
                'resource_requirements': np.random.randint(1, 10),  # Number of resources needed
                'complexity_score': np.random.uniform(1, 10),  # Complexity rating
                'profit_margin': np.random.uniform(0.1, 0.5),  # Target profit margin
                'market_rate': np.random.uniform(100, 1000),  # Market rate for service
                'historical_cost': np.random.uniform(40, 450),  # Historical cost
                'cost_variance': np.random.uniform(-0.2, 0.3),  # Cost variance from historical
                'department': np.random.choice(['IT', 'Marketing', 'Sales', 'Operations'])
            }
            services.append(service)
        
        return pd.DataFrame(services)
    
    def _generate_mock_client_priority_data(self, start_date: datetime, 
                                        end_date: datetime) -> pd.DataFrame:
        """Generate mock client priority data for testing"""
        # Generate client data
        clients = []
        client_count = 50
        
        for i in range(client_count):
            client_id = f"CLIENT-{i+1:03d}"
            
            # Client priorities
            client = {
                'client_id': client_id,
                'client_name': f"Client {i+1}",
                'revenue_contribution': np.random.uniform(10000, 200000),  # Annual revenue
                'profit_margin': np.random.uniform(0.15, 0.45),  # Profit margin
                'contract_value': np.random.uniform(50000, 500000),  # Total contract value
                'contract_length_months': np.random.choice([12, 24, 36, 48, 60]),  # Contract length
                'strategic_importance': np.random.uniform(1, 10),  # Strategic importance score
                'client_satisfaction': np.random.uniform(1, 10),  # Satisfaction score
                'loyalty_score': np.random.uniform(1, 100),  # Loyalty score
                'growth_potential': np.random.uniform(1, 100),  # Growth potential
                'service_usage_frequency': np.random.uniform(1, 20),  # Service usage per month
                'support_ticket_frequency': np.random.uniform(0, 10),  # Support tickets per month
                'priority_score': np.random.uniform(1, 100),  # Overall priority score
                'industry': np.random.choice(['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing']),
                'company_size': np.random.choice(['Small', 'Medium', 'Large'])
            }
            clients.append(client)
        
        return pd.DataFrame(clients)
    
    def _generate_mock_roi_data(self, start_date: datetime, 
                            end_date: datetime) -> pd.DataFrame:
        """Generate mock ROI data for testing"""
        # Generate ROI data
        roi_data = []
        item_count = 40
        
        for i in range(item_count):
            item_id = f"ITEM-{i+1:03d}"
            
            # ROI metrics
            item = {
                'item_id': item_id,
                'item_name': f"Investment {i+1}",
                'investment_type': np.random.choice(['Software', 'Equipment', 'Training', 'Marketing', 'Infrastructure']),
                'initial_investment': np.random.uniform(5000, 100000),  # Initial investment amount
                'expected_return': np.random.uniform(10000, 200000),  # Expected return
                'actual_return': np.random.uniform(5000, 180000),  # Actual return (if available)
                'roi_percentage': np.random.uniform(-0.2, 2.0),  # ROI percentage
                'payback_period_months': np.random.uniform(6, 36),  # Payback period in months
                'net_present_value': np.random.uniform(-10000, 150000),  # NPV
                'internal_rate_of_return': np.random.uniform(0.05, 0.3),  # IRR
                'risk_score': np.random.uniform(1, 10),  # Risk assessment score
                'department': np.random.choice(['IT', 'Marketing', 'Sales', 'Operations']),
                'fiscal_year': np.random.choice([2024, 2025, 2026])
            }
            roi_data.append(item)
        
        return pd.DataFrame(roi_data)
    
    def _generate_mock_resource_data(self, start_date: datetime, 
                                 end_date: datetime) -> pd.DataFrame:
        """Generate mock resource data for testing"""
        # Generate resource data
        resources = []
        resource_count = 25
        
        for i in range(resource_count):
            resource_id = f"RESOURCE-{i+1:03d}"
            
            # Resource information
            resource = {
                'resource_id': resource_id,
                'resource_name': f"Resource {i+1}",
                'resource_type': np.random.choice(['Personnel', 'Equipment', 'Software', 'Facility']),
                'hourly_rate': np.random.uniform(20, 200),  # Hourly cost
                'monthly_cost': np.random.uniform(1000, 15000),  # Monthly cost
                'availability_hours_per_week': np.random.uniform(20, 40),  # Available hours per week
                'utilization_rate': np.random.uniform(0.5, 1.0),  # Current utilization rate
                'skill_level': np.random.choice(['Junior', 'Mid-level', 'Senior', 'Expert']),
                'department': np.random.choice(['IT', 'Marketing', 'Sales', 'Operations']),
                'specialization': np.random.choice(['Development', 'Design', 'Analysis', 'Management', 'Support']),
                'efficiency_score': np.random.uniform(1, 10),  # Efficiency rating
                'capacity_utilization_target': np.random.uniform(0.7, 0.95)  # Target utilization
            }
            resources.append(resource)
        
        return pd.DataFrame(resources)


# Global instance for easy access
budget_data_preparator_instance = None


async def get_budget_data_preparator() -> BudgetDataPreparator:
    """Get singleton budget data preparator instance"""
    global budget_data_preparator_instance
    if budget_data_preparator_instance is None:
        budget_data_preparator_instance = BudgetDataPreparator()
    return budget_data_preparator_instance