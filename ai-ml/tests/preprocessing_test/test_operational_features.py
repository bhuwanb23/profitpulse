"""
Test suite for operational features engine
"""

import pandas as pd
import numpy as np
import pytest
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'data'))

# Import the operational features module
operational_features = __import__('preprocessing.modular_feature_engineering.operational_features', fromlist=['*'])

calculate_ticket_resolution_time = operational_features.calculate_ticket_resolution_time
calculate_sla_compliance = operational_features.calculate_sla_compliance
calculate_technician_productivity = operational_features.calculate_technician_productivity
assess_service_delivery_quality = operational_features.assess_service_delivery_quality
calculate_client_satisfaction = operational_features.calculate_client_satisfaction
analyze_ticket_frequency = operational_features.analyze_ticket_frequency
track_service_level_trends = operational_features.track_service_level_trends
calculate_resource_utilization = operational_features.calculate_resource_utilization


def create_sample_operational_data():
    """Create sample operational data for testing"""
    data = {
        'ticket_id': ['T001', 'T002', 'T003', 'T004', 'T005', 'T006'],
        'created_date': ['2023-01-15 09:00:00', '2023-01-16 10:30:00', '2023-02-10 11:15:00', '2023-02-15 14:20:00', '2023-03-05 08:45:00', '2023-03-10 16:30:00'],
        'resolved_date': ['2023-01-15 11:30:00', '2023-01-16 12:00:00', '2023-02-10 14:45:00', '2023-02-15 15:30:00', '2023-03-05 12:15:00', '2023-03-10 18:45:00'],
        'sla_target_hours': [4.0, 2.0, 6.0, 1.0, 8.0, 3.0],
        'actual_resolution_hours': [2.5, 1.5, 3.5, 1.2, 3.5, 2.25],
        'technician_id': ['Tech001', 'Tech002', 'Tech001', 'Tech003', 'Tech002', 'Tech001'],
        'tickets_handled': [10, 8, 12, 5, 9, 11],
        'total_hours_worked': [40, 32, 48, 20, 36, 44],
        'tickets_resolved': [9, 8, 11, 5, 8, 10],
        'service_id': ['S001', 'S002', 'S001', 'S003', 'S002', 'S001'],
        'quality_score': [8.5, 7.2, 9.1, 6.8, 8.0, 8.7],
        'customer_rating': [4.5, 3.8, 4.8, 3.5, 4.2, 4.6],
        'first_time_fix': [True, False, True, False, True, True],
        'client_id': ['C001', 'C002', 'C001', 'C003', 'C002', 'C001'],
        'ticket_date': ['2023-01-15', '2023-01-16', '2023-02-10', '2023-02-15', '2023-03-05', '2023-03-10'],
        'ticket_type': ['Incident', 'Service Request', 'Incident', 'Problem', 'Incident', 'Service Request'],
        'date': ['2023-01-15', '2023-01-16', '2023-02-10', '2023-02-15', '2023-03-05', '2023-03-10'],
        'performance_score': [8.2, 7.5, 9.0, 6.5, 8.1, 8.5],
        'resource_id': ['R001', 'R002', 'R001', 'R003', 'R002', 'R001'],
        'allocated_hours': [35, 28, 42, 18, 32, 40],
        'used_hours': [32, 25, 38, 16, 29, 36],
        'capacity_hours': [40, 32, 48, 20, 36, 44]
    }
    return pd.DataFrame(data)


def test_calculate_ticket_resolution_time():
    """Test ticket resolution time calculation"""
    df = create_sample_operational_data()
    result = calculate_ticket_resolution_time(df)
    
    assert len(result) > 0
    assert 'ticket_id' in result.columns
    assert 'resolution_time_hours' in result.columns


def test_calculate_sla_compliance():
    """Test SLA compliance calculation"""
    df = create_sample_operational_data()
    result = calculate_sla_compliance(df)
    
    assert len(result) > 0
    assert 'ticket_id' in result.columns
    assert 'sla_compliance_rate' in result.columns
    assert 'sla_breach_rate' in result.columns


def test_calculate_technician_productivity():
    """Test technician productivity calculation"""
    df = create_sample_operational_data()
    result = calculate_technician_productivity(df)
    
    assert len(result) > 0
    assert 'technician_id' in result.columns
    assert 'productivity_score' in result.columns
    assert 'tickets_per_hour' in result.columns


def test_assess_service_delivery_quality():
    """Test service delivery quality assessment"""
    df = create_sample_operational_data()
    result = assess_service_delivery_quality(df)
    
    assert len(result) > 0
    assert 'service_id' in result.columns
    assert 'avg_quality_score' in result.columns
    assert 'quality_index' in result.columns


def test_calculate_client_satisfaction():
    """Test client satisfaction calculation"""
    df = create_sample_operational_data()
    # Add required columns for satisfaction calculation
    df['satisfaction_score'] = [4.5, 3.8, 4.8, 3.5, 4.2, 4.6]
    df['feedback_count'] = [10, 8, 12, 5, 9, 11]
    df['positive_feedback_count'] = [8, 6, 10, 4, 8, 9]
    
    result = calculate_client_satisfaction(df)
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'avg_satisfaction_score' in result.columns
    assert 'satisfaction_rate' in result.columns


def test_analyze_ticket_frequency():
    """Test ticket frequency analysis"""
    df = create_sample_operational_data()
    result = analyze_ticket_frequency(df)
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'total_tickets' in result.columns
    assert 'avg_tickets_per_month' in result.columns


def test_track_service_level_trends():
    """Test service level trends tracking"""
    df = create_sample_operational_data()
    result = track_service_level_trends(df)
    
    assert len(result) > 0
    assert 'service_id' in result.columns
    assert 'period_type' in result.columns
    assert 'monthly_trend' in result.columns or 'quarterly_trend' in result.columns


def test_calculate_resource_utilization():
    """Test resource utilization calculation"""
    df = create_sample_operational_data()
    result = calculate_resource_utilization(df)
    
    assert len(result) > 0
    assert 'resource_id' in result.columns
    assert 'utilization_rate' in result.columns
    assert 'utilization_score' in result.columns


if __name__ == '__main__':
    pytest.main([__file__])