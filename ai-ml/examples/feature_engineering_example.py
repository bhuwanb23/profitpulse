"""
Example usage of the Feature Engineering System
"""

import pandas as pd
import numpy as np
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'data'))

def create_sample_data():
    """Create sample MSP data for demonstration"""
    # Sample financial data
    financial_data = {
        'client_id': ['C001', 'C001', 'C002', 'C002', 'C003', 'C003', 'C001', 'C002'],
        'service_type': ['Managed Services', 'Consulting', 'Managed Services', 'Support', 
                        'Consulting', 'Managed Services', 'Managed Services', 'Support'],
        'revenue': [10000, 5000, 8000, 2000, 12000, 9000, 11000, 2500],
        'cost': [6000, 3000, 5000, 1200, 7000, 5500, 6500, 1300],
        'date': ['2023-01-15', '2023-01-20', '2023-02-10', '2023-02-15', 
                '2023-03-05', '2023-03-10', '2023-04-15', '2023-04-20'],
        'billed_amount': [10000, 5000, 8000, 2000, 12000, 9000, 11000, 2500],
        'actual_cost': [6000, 3000, 5000, 1200, 7000, 5500, 6500, 1300],
        'expected_amount': [9500, 5200, 8200, 1900, 11800, 9200, 10800, 2400],
        'ticket_id': ['T001', 'T002', 'T003', 'T004', 'T005', 'T006', 'T007', 'T008'],
        'resolution_time_hours': [2.5, 1.0, 3.0, 0.5, 4.0, 2.0, 2.2, 0.8],
        'service_id': ['S001', 'S002', 'S001', 'S003', 'S002', 'S001', 'S001', 'S003'],
        'usage_hours': [100, 50, 120, 30, 80, 90, 110, 35],
        'available_hours': [120, 60, 140, 40, 100, 110, 130, 45],
        'payment_date': ['2023-01-20', '2023-01-25', '2023-02-15', '2023-02-20', 
                        '2023-03-10', '2023-03-15', '2023-04-20', '2023-04-25'],
        'payment_amount': [10000, 5000, 8000, 2000, 12000, 9000, 11000, 2500],
        'due_date': ['2023-01-15', '2023-01-20', '2023-02-10', '2023-02-15', 
                    '2023-03-05', '2023-03-10', '2023-04-15', '2023-04-20'],
        'expenses': [1000, 500, 800, 200, 1200, 900, 1100, 250],
        'total_assets': [50000, 25000, 40000, 10000, 60000, 45000, 55000, 12000]
    }
    
    # Sample operational data
    operational_data = {
        'ticket_id': ['T001', 'T002', 'T003', 'T004', 'T005', 'T006', 'T007', 'T008'],
        'created_date': ['2023-01-15 09:00:00', '2023-01-16 10:30:00', '2023-02-10 11:15:00', '2023-02-15 14:20:00',
                        '2023-03-05 08:45:00', '2023-03-10 16:30:00', '2023-04-15 09:15:00', '2023-04-20 10:45:00'],
        'resolved_date': ['2023-01-15 11:30:00', '2023-01-16 12:00:00', '2023-02-10 14:45:00', '2023-02-15 15:30:00',
                         '2023-03-05 12:15:00', '2023-03-10 18:45:00', '2023-04-15 11:30:00', '2023-04-20 11:30:00'],
        'sla_target_hours': [4.0, 2.0, 6.0, 1.0, 8.0, 3.0, 4.0, 1.0],
        'actual_resolution_hours': [2.5, 1.5, 3.5, 1.2, 3.5, 2.25, 2.2, 0.75],
        'technician_id': ['Tech001', 'Tech002', 'Tech001', 'Tech003', 'Tech002', 'Tech001', 'Tech001', 'Tech003'],
        'tickets_handled': [10, 8, 12, 5, 9, 11, 13, 6],
        'total_hours_worked': [40, 32, 48, 20, 36, 44, 52, 24],
        'tickets_resolved': [9, 8, 11, 5, 8, 10, 12, 6],
        'quality_score': [8.5, 7.2, 9.1, 6.8, 8.0, 8.7, 8.9, 7.0],
        'customer_rating': [4.5, 3.8, 4.8, 3.5, 4.2, 4.6, 4.7, 3.8],
        'first_time_fix': [True, False, True, False, True, True, True, False],
        'performance_score': [8.2, 7.5, 9.0, 6.5, 8.1, 8.5, 8.8, 7.2],
        'resource_id': ['R001', 'R002', 'R001', 'R003', 'R002', 'R001', 'R001', 'R003'],
        'allocated_hours': [35, 28, 42, 18, 32, 40, 45, 20],
        'used_hours': [32, 25, 38, 16, 29, 36, 40, 18],
        'capacity_hours': [40, 32, 48, 20, 36, 44, 50, 22]
    }
    
    # Sample behavioral data
    behavioral_data = {
        'client_id': ['C001', 'C002', 'C003'],
        'login_count': [50, 30, 70],
        'support_request_count': [5, 2, 8],
        'feature_usage_count': [15, 8, 20],
        'engagement_score': [0.8, 0.4, 0.9],
        'support_ticket_count': [5, 15, 3],
        'contract_renewal_likelihood': ['High', 'Low', 'High'],
        'payment_delinquency_rate': [0.05, 0.3, 0.02]
    }
    
    return (
        pd.DataFrame(financial_data),
        pd.DataFrame(operational_data),
        pd.DataFrame(behavioral_data)
    )


def demonstrate_financial_features():
    """Demonstrate financial feature extraction"""
    print("=== Financial Features Demonstration ===")
    
    financial_df, _, _ = create_sample_data()
    
    # Import financial features module
    financial_features = __import__('preprocessing.modular_feature_engineering.financial_features', fromlist=['*'])
    
    # Calculate revenue per client
    revenue_per_client = financial_features.calculate_revenue_per_client(
        financial_df, frequency='monthly'
    )
    print("Revenue per client (monthly):")
    print(revenue_per_client.head())
    print()
    
    # Calculate profit margins by service
    profit_margins = financial_features.calculate_profit_margins_by_service(financial_df)
    print("Profit margins by service:")
    print(profit_margins.head())
    print()
    
    # Calculate profitability ratios
    profitability_ratios = financial_features.calculate_profitability_ratios(financial_df)
    print("Profitability ratios (first 3 rows):")
    print(profitability_ratios[['revenue', 'gross_profit_margin', 'net_profit_margin']].head(3))
    print()


def demonstrate_operational_features():
    """Demonstrate operational feature extraction"""
    print("=== Operational Features Demonstration ===")
    
    _, operational_df, _ = create_sample_data()
    
    # Import operational features module
    operational_features = __import__('preprocessing.modular_feature_engineering.operational_features', fromlist=['*'])
    
    # Calculate ticket resolution time
    resolution_time = operational_features.calculate_ticket_resolution_time(operational_df)
    print("Ticket resolution time:")
    print(resolution_time.head())
    print()
    
    # Calculate SLA compliance
    sla_compliance = operational_features.calculate_sla_compliance(operational_df)
    print("SLA compliance:")
    print(sla_compliance.head())
    print()
    
    # Calculate technician productivity
    technician_productivity = operational_features.calculate_technician_productivity(operational_df)
    print("Technician productivity:")
    print(technician_productivity.head())
    print()


def demonstrate_behavioral_features():
    """Demonstrate behavioral feature extraction"""
    print("=== Behavioral Features Demonstration ===")
    
    _, _, behavioral_df = create_sample_data()
    
    # Import behavioral features module
    behavioral_features = __import__('preprocessing.modular_feature_engineering.behavioral_features', fromlist=['*'])
    
    # Measure client engagement
    client_engagement = behavioral_features.measure_client_engagement(behavioral_df)
    print("Client engagement:")
    print(client_engagement.head())
    print()
    
    # Calculate churn risk
    churn_risk = behavioral_features.calculate_churn_risk(behavioral_df)
    print("Churn risk:")
    print(churn_risk.head())
    print()


def demonstrate_orchestrator():
    """Demonstrate the feature engineering orchestrator"""
    print("=== Feature Engineering Orchestrator Demonstration ===")
    
    financial_df, _, _ = create_sample_data()
    
    # Import orchestrator
    orchestrator = __import__('preprocessing.modular_feature_engineering.orchestrator', fromlist=['*'])
    
    # Configure feature extraction
    feature_config = {
        'financial_features': True,
        'financial_config': {
            'revenue_per_client': True,
            'profit_margins_by_service': True,
            'revenue_per_client_config': {
                'frequency': 'monthly'
            }
        }
    }
    
    # Extract features using orchestrator
    enhanced_df = orchestrator.extract_all_features(financial_df, feature_config)
    print("Enhanced DataFrame shape:", enhanced_df.shape)
    print("Columns in enhanced DataFrame:")
    print(list(enhanced_df.columns))
    print()


def demonstrate_integration_with_main_pipeline():
    """Demonstrate integration with the main feature engineering pipeline"""
    print("=== Integration with Main Pipeline Demonstration ===")
    
    financial_df, _, _ = create_sample_data()
    
    # Import main feature engineering module
    feature_engineering_module = __import__('preprocessing.feature_engineering', fromlist=['engineer_features'])
    engineer_features = feature_engineering_module.engineer_features
    
    # Configure the modular system
    config = {
        'use_modular_system': True,
        'financial_features': True,
        'financial_config': {
            'revenue_per_client': True,
            'profit_margins_by_service': True,
            'revenue_per_client_config': {
                'frequency': 'monthly'
            }
        }
    }
    
    # Engineer features using the new modular system
    engineered_df = engineer_features(financial_df, config)
    print("Engineered DataFrame shape:", engineered_df.shape)
    print("Sample of engineered features:")
    print(engineered_df.head())
    print()


if __name__ == "__main__":
    print("Feature Engineering System Examples")
    print("=" * 40)
    print()
    
    try:
        demonstrate_financial_features()
        demonstrate_operational_features()
        demonstrate_behavioral_features()
        demonstrate_orchestrator()
        demonstrate_integration_with_main_pipeline()
        
        print("All demonstrations completed successfully!")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()