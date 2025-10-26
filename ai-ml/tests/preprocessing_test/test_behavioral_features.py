"""
Test suite for behavioral features engine
"""

import pandas as pd
import numpy as np
import pytest
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'data'))

# Import the behavioral features module
behavioral_features = __import__('preprocessing.modular_feature_engineering.behavioral_features', fromlist=['*'])

measure_client_engagement = behavioral_features.measure_client_engagement
analyze_communication_patterns = behavioral_features.analyze_communication_patterns
track_service_changes = behavioral_features.track_service_changes
predict_contract_renewal = behavioral_features.predict_contract_renewal
analyze_support_requests = behavioral_features.analyze_support_requests
analyze_feedback_sentiment = behavioral_features.analyze_feedback_sentiment
identify_usage_patterns = behavioral_features.identify_usage_patterns
calculate_churn_risk = behavioral_features.calculate_churn_risk


def create_sample_behavioral_data():
    """Create sample behavioral data for testing"""
    data = {
        'client_id': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006'],
        'login_count': [50, 30, 70, 20, 60, 40],
        'support_request_count': [5, 2, 8, 1, 6, 3],
        'feature_usage_count': [15, 8, 20, 4, 18, 12],
        'communication_date': ['2023-01-15', '2023-01-16', '2023-02-10', '2023-02-15', '2023-03-05', '2023-03-10'],
        'communication_type': ['Email', 'Phone', 'Email', 'Chat', 'Email', 'Phone'],
        'response_time_hours': [2.5, 1.0, 3.0, 0.5, 4.0, 2.0],
        'service_type': ['Managed Services', 'Consulting', 'Managed Services', 'Support', 'Consulting', 'Managed Services'],
        'change_type': ['upgrade', 'downgrade', 'upgrade', 'upgrade', 'downgrade', 'upgrade'],
        'change_date': ['2023-01-20', '2023-01-25', '2023-02-15', '2023-02-20', '2023-03-10', '2023-03-15'],
        'contract_end_date': ['2024-01-15', '2023-07-16', '2024-02-10', '2023-08-15', '2023-09-05', '2024-03-10'],
        'renewal_probability': [0.9, 0.3, 0.8, 0.2, 0.4, 0.7],
        'engagement_score': [0.8, 0.4, 0.9, 0.2, 0.5, 0.6],
        'request_date': ['2023-01-15', '2023-01-16', '2023-02-10', '2023-02-15', '2023-03-05', '2023-03-10'],
        'request_type': ['Incident', 'Service Request', 'Incident', 'Problem', 'Incident', 'Service Request'],
        'resolution_satisfaction': [4.5, 3.8, 4.8, 3.5, 4.2, 4.6],
        'feedback_date': ['2023-01-15', '2023-01-16', '2023-02-10', '2023-02-15', '2023-03-05', '2023-03-10'],
        'sentiment_score': [0.8, -0.2, 0.9, -0.5, 0.3, 0.6],
        'feedback_category': ['Positive', 'Negative', 'Positive', 'Negative', 'Neutral', 'Positive'],
        'usage_date': ['2023-01-15', '2023-01-16', '2023-02-10', '2023-02-15', '2023-03-05', '2023-03-10'],
        'feature_name': ['Dashboard', 'Reports', 'Dashboard', 'Alerts', 'Reports', 'Dashboard'],
        'usage_duration_minutes': [30, 15, 45, 10, 40, 25],
        'support_ticket_count': [5, 15, 3, 20, 12, 8],
        'contract_renewal_likelihood': ['High', 'Low', 'High', 'Low', 'Medium', 'High'],
        'payment_delinquency_rate': [0.05, 0.3, 0.02, 0.4, 0.2, 0.1]
    }
    return pd.DataFrame(data)


def test_measure_client_engagement():
    """Test client engagement measurement"""
    df = create_sample_behavioral_data()
    result = measure_client_engagement(df)
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'engagement_score' in result.columns
    assert 'engagement_level' in result.columns


def test_analyze_communication_patterns():
    """Test communication patterns analysis"""
    df = create_sample_behavioral_data()
    result = analyze_communication_patterns(df)
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'total_communications' in result.columns
    assert 'avg_response_time' in result.columns


def test_track_service_changes():
    """Test service changes tracking"""
    df = create_sample_behavioral_data()
    result = track_service_changes(df)
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'total_service_changes' in result.columns
    assert 'upgrade_count' in result.columns
    assert 'downgrade_count' in result.columns


def test_predict_contract_renewal():
    """Test contract renewal prediction"""
    df = create_sample_behavioral_data()
    result = predict_contract_renewal(df)
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'days_until_end' in result.columns
    assert 'renewal_score' in result.columns
    assert 'renewal_likelihood' in result.columns


def test_analyze_support_requests():
    """Test support request analysis"""
    df = create_sample_behavioral_data()
    result = analyze_support_requests(df)
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'total_requests' in result.columns
    assert 'avg_satisfaction' in result.columns


def test_analyze_feedback_sentiment():
    """Test feedback sentiment analysis"""
    df = create_sample_behavioral_data()
    result = analyze_feedback_sentiment(df)
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'total_feedbacks' in result.columns
    assert 'avg_sentiment' in result.columns
    assert 'sentiment_trend' in result.columns


def test_identify_usage_patterns():
    """Test usage pattern identification"""
    df = create_sample_behavioral_data()
    result = identify_usage_patterns(df)
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'total_sessions' in result.columns
    assert 'avg_session_duration' in result.columns
    assert 'usage_intensity' in result.columns


def test_calculate_churn_risk():
    """Test churn risk calculation"""
    df = create_sample_behavioral_data()
    result = calculate_churn_risk(df)
    
    assert len(result) > 0
    assert 'client_id' in result.columns
    assert 'churn_risk_score' in result.columns
    assert 'churn_risk_level' in result.columns


if __name__ == '__main__':
    pytest.main([__file__])