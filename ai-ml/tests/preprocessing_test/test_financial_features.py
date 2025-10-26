"""
Test suite for financial features engine
"""

import pandas as pd
import numpy as np
import pytest
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'data'))

# Import the financial features module
financial_features = __import__('preprocessing.modular_feature_engineering.financial_features', fromlist=['*'])

calculate_revenue_per_client = financial_features.calculate_revenue_per_client
calculate_profit_margins_by_service = financial_features.calculate_profit_margins_by_service
calculate_billing_efficiency = financial_features.calculate_billing_efficiency
calculate_cost_per_ticket_resolution = financial_features.calculate_cost_per_ticket_resolution
calculate_service_utilization_rates = financial_features.calculate_service_utilization_rates
analyze_payment_behavior = financial_features.analyze_payment_behavior
calculate_revenue_growth_trends = financial_features.calculate_revenue_growth_trends
calculate_profitability_ratios = financial_features.calculate_profitability_ratios


def create_sample_financial_data():
    """Create sample financial data for testing"""
    data = {
        'client_id': ['C001', 'C001', 'C002', 'C002', 'C003', 'C003'],
        'service_type': ['Managed Services', 'Consulting', 'Managed Services', 'Support', 'Consulting', 'Managed Services'],
        'revenue': [10000, 5000, 8000, 2000, 12000, 9000],
        'cost': [6000, 3000, 5000, 1200, 7000, 5500],
        'date': ['2023-01-15', '2023-01-20', '2023-02-10', '2023-02-15', '2023-03-05', '2023-03-10'],
        'billed_amount': [10000, 5000, 8000, 2000, 12000, 9000],
        'actual_cost': [6000, 3000, 5000, 1200, 7000, 5500],
        'expected_amount': [9500, 5200, 8200, 1900, 11800, 9200],
        'ticket_id': ['T001', 'T002', 'T003', 'T004', 'T005', 'T006'],
        'resolution_time_hours': [2.5, 1.0, 3.0, 0.5, 4.0, 2.0],
        'service_id': ['S001', 'S002', 'S001', 'S003', 'S002', 'S001'],
        'usage_hours': [100, 50, 120, 30, 80, 90],
        'available_hours': [120, 60, 140, 40, 100, 110],
        'payment_date': ['2023-01-20', '2023-01-25', '2023-02-15', '2023-02-20', '2023-03-10', '2023-03-15'],
        'payment_amount': [10000, 5000, 8000, 2000, 12000, 9000],
        'due_date': ['2023-01-15', '2023-01-20', '2023-02-10', '2023-02-15', '2023-03-05', '2023-03-10'],
        'expenses': [1000, 500, 800, 200, 1200, 900],
        'total_assets': [50000, 25000, 40000, 10000, 60000, 45000]
    }
    return pd.DataFrame(data)


def test_calculate_revenue_per_client():
    """Test revenue per client calculation"""
    df = create_sample_financial_data()
    result = calculate_revenue_per_client(df, frequency='monthly')
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'period' in result.columns
    assert 'monthly_revenue' in result.columns


def test_calculate_profit_margins_by_service():
    """Test profit margins by service calculation"""
    df = create_sample_financial_data()
    result = calculate_profit_margins_by_service(df)
    
    assert len(result) > 0
    assert 'service_type' in result.columns
    assert 'profit_margin' in result.columns
    assert 'profit' in result.columns


def test_calculate_billing_efficiency():
    """Test billing efficiency calculation"""
    df = create_sample_financial_data()
    result = calculate_billing_efficiency(df)
    
    assert len(result) > 0
    assert 'billing_accuracy' in result.columns
    assert 'cost_recovery_ratio' in result.columns
    assert 'billing_efficiency_score' in result.columns


def test_calculate_cost_per_ticket_resolution():
    """Test cost per ticket resolution calculation"""
    df = create_sample_financial_data()
    result = calculate_cost_per_ticket_resolution(df)
    
    assert len(result) > 0
    assert 'ticket_id' in result.columns
    assert 'avg_cost_per_hour' in result.columns


def test_calculate_service_utilization_rates():
    """Test service utilization rates calculation"""
    df = create_sample_financial_data()
    result = calculate_service_utilization_rates(df)
    
    assert len(result) > 0
    assert 'service_id' in result.columns
    assert 'utilization_rate' in result.columns


def test_analyze_payment_behavior():
    """Test payment behavior analysis"""
    df = create_sample_financial_data()
    result = analyze_payment_behavior(df)
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'total_payments' in result.columns
    assert 'late_payment_rate' in result.columns


def test_calculate_revenue_growth_trends():
    """Test revenue growth trends calculation"""
    df = create_sample_financial_data()
    result = calculate_revenue_growth_trends(df, period='month')
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'period' in result.columns
    assert 'growth_rate' in result.columns


def test_calculate_profitability_ratios():
    """Test profitability ratios calculation"""
    df = create_sample_financial_data()
    result = calculate_profitability_ratios(df)
    
    assert len(result) > 0
    assert 'gross_profit_margin' in result.columns
    assert 'net_profit_margin' in result.columns
    assert 'return_on_assets' in result.columns


if __name__ == '__main__':
    pytest.main([__file__])