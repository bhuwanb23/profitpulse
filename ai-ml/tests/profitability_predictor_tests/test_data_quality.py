"""
Tests for ProfitabilityDataQualityAssessor
"""

import pandas as pd
import pytest
import numpy as np
from datetime import datetime, timedelta

from src.models.profitability_predictor.data_quality import ProfitabilityDataQualityAssessor, assess_profitability_data_quality


def create_test_data_with_issues():
    """Create test data with various quality issues"""
    # Create sample data with missing values, duplicates, and outliers
    data = {
        'id': ['client_1', 'client_2', 'client_3', 'client_4', 'client_5', 'client_1'],  # Duplicate ID
        'name': ['Acme Corp', 'TechStart Inc', 'Global Solutions', None, 'DataSystems', 'Acme Corp'],  # Missing
        'industry': ['Manufacturing', 'Technology', 'Finance', 'Healthcare', 'Technology', 'Manufacturing'],
        'total_revenue': [45000.0, 6000.0, 20000.0, 15000.0, 30000.0, 45000.0],  # Duplicate values
        'total_costs': [30000.0, 4000.0, 15000.0, 10000.0, 20000.0, 30000.0],   # Duplicate values
        'profit_margin': [0.33, 0.33, 0.25, 0.33, 0.33, 0.33],
        'feature_1': [0.5, 0.7, 0.3, 0.8, 0.6, 0.5],  # Normal values
        'feature_2': [1.2, 1.5, 1.0, 2.1, 1.3, 1.2],  # Normal values
        'outlier_feature': [10, 12, 8, 15, 11, 10]   # Make one a true duplicate, one outlier
    }
    
    return pd.DataFrame(data)


def create_test_data_with_outliers():
    """Create test data with outliers for testing"""
    data = {
        'id': ['client_1', 'client_2', 'client_3', 'client_4', 'client_5'],
        'name': ['Acme Corp', 'TechStart Inc', 'Global Solutions', 'DataSystems', 'InnovateCo'],
        'industry': ['Manufacturing', 'Technology', 'Finance', 'Healthcare', 'Technology'],
        'total_revenue': [45000.0, 6000.0, 20000.0, 15000.0, 30000.0],
        'total_costs': [30000.0, 4000.0, 15000.0, 10000.0, 20000.0],
        'profit_margin': [0.33, 0.33, 0.25, 0.33, 0.33],
        'feature_1': [0.5, 0.7, 0.3, 0.8, 0.6],
        'feature_2': [1.2, 1.5, 1.0, 2.1, 1.3],
        'outlier_feature': [10, 12, 8, 15, 1000]   # Outlier (1000 is outlier)
    }
    
    return pd.DataFrame(data)


def create_clean_test_data():
    """Create clean test data without issues"""
    data = {
        'id': ['client_1', 'client_2', 'client_3', 'client_4', 'client_5'],
        'name': ['Acme Corp', 'TechStart Inc', 'Global Solutions', 'DataSystems', 'InnovateCo'],
        'industry': ['Manufacturing', 'Technology', 'Finance', 'Healthcare', 'Technology'],
        'total_revenue': [45000.0, 6000.0, 20000.0, 15000.0, 30000.0],
        'total_costs': [30000.0, 4000.0, 15000.0, 10000.0, 20000.0],
        'profit_margin': [0.33, 0.33, 0.25, 0.33, 0.33],
        'feature_1': [0.5, 0.7, 0.3, 0.8, 0.6],
        'feature_2': [1.2, 1.5, 1.0, 2.1, 1.3]
    }
    
    return pd.DataFrame(data)


def test_data_quality_assessor_initialization():
    """Test ProfitabilityDataQualityAssessor initialization"""
    assessor = ProfitabilityDataQualityAssessor()
    assert assessor is not None


def test_assess_missing_values():
    """Test missing value assessment"""
    # Create test data with missing values
    data = create_test_data_with_issues()
    
    # Create assessor
    assessor = ProfitabilityDataQualityAssessor()
    
    # Assess missing values
    missing_report = assessor.assess_missing_values(data)
    
    # Check results
    assert isinstance(missing_report, dict)
    assert 'total_records' in missing_report
    assert 'missing_counts' in missing_report
    assert 'missing_percentages' in missing_report
    assert 'columns_with_missing' in missing_report
    
    # Check specific values
    assert missing_report['total_records'] == len(data)
    assert missing_report['missing_counts']['name'] == 1  # One missing value in name column
    assert 'name' in missing_report['columns_with_missing']


def test_assess_duplicates():
    """Test duplicate assessment"""
    # Create test data with duplicates
    data = create_test_data_with_issues()
    
    # Create assessor
    assessor = ProfitabilityDataQualityAssessor()
    
    # Assess duplicates
    duplicates_report = assessor.assess_duplicates(data)
    
    # Check results
    assert isinstance(duplicates_report, dict)
    assert 'total_records' in duplicates_report
    assert 'duplicate_rows' in duplicates_report
    assert 'duplicate_percentage' in duplicates_report
    
    # Check specific values
    assert duplicates_report['total_records'] == len(data)
    assert duplicates_report['duplicate_rows'] >= 1  # At least one duplicate row
    assert duplicates_report['duplicate_percentage'] >= 0


def test_assess_data_types():
    """Test data type assessment"""
    # Create test data
    data = create_test_data_with_issues()
    
    # Create assessor
    assessor = ProfitabilityDataQualityAssessor()
    
    # Assess data types
    data_types_report = assessor.assess_data_types(data)
    
    # Check results
    assert isinstance(data_types_report, dict)
    assert 'total_columns' in data_types_report
    assert 'data_types' in data_types_report
    assert 'numerical_columns' in data_types_report
    assert 'categorical_columns' in data_types_report
    assert 'datetime_columns' in data_types_report
    
    # Check specific values
    assert data_types_report['total_columns'] == len(data.columns)
    assert 'id' in data_types_report['categorical_columns']
    assert 'total_revenue' in data_types_report['numerical_columns']


def test_assess_outliers():
    """Test outlier assessment"""
    # Create test data with outliers
    data = create_test_data_with_outliers()
    
    # Create assessor
    assessor = ProfitabilityDataQualityAssessor()
    
    # Assess outliers
    outliers_report = assessor.assess_outliers(data, ['outlier_feature'])
    
    # Check results
    assert isinstance(outliers_report, dict)
    assert 'total_outliers' in outliers_report
    assert 'total_records' in outliers_report
    assert 'outlier_percentage' in outliers_report
    assert 'column_outliers' in outliers_report
    
    # Check that outlier was detected
    assert outliers_report['total_outliers'] > 0
    assert 'outlier_feature' in outliers_report['column_outliers']
    
    # Check specific outlier metrics
    outlier_metrics = outliers_report['column_outliers']['outlier_feature']
    assert 'outlier_count' in outlier_metrics
    assert 'outlier_percentage' in outlier_metrics
    assert 'lower_bound' in outlier_metrics
    assert 'upper_bound' in outlier_metrics


def test_assess_data_quality():
    """Test complete data quality assessment"""
    # Create test data
    data = create_test_data_with_issues()
    
    # Create assessor
    assessor = ProfitabilityDataQualityAssessor()
    
    # Assess data quality
    quality_report = assessor.assess_data_quality(data)
    
    # Check results
    assert isinstance(quality_report, dict)
    assert 'timestamp' in quality_report
    assert 'missing_values' in quality_report
    assert 'duplicates' in quality_report
    assert 'data_types' in quality_report
    assert 'outliers' in quality_report
    assert 'summary' in quality_report
    
    # Check summary
    summary = quality_report['summary']
    assert 'total_records' in summary
    assert 'total_columns' in summary
    assert 'columns_with_missing' in summary
    assert 'duplicate_rows' in summary
    assert 'numerical_columns' in summary
    assert 'categorical_columns' in summary
    assert 'total_outliers' in summary


def test_convenience_function():
    """Test the convenience function"""
    # Create test data
    data = create_clean_test_data()
    
    # Test convenience function
    quality_report = assess_profitability_data_quality(data)
    
    # Check results
    assert isinstance(quality_report, dict)
    assert 'timestamp' in quality_report
    assert 'missing_values' in quality_report
    assert 'duplicates' in quality_report
    assert 'data_types' in quality_report
    assert 'outliers' in quality_report
    assert 'summary' in quality_report
    
    # Check that clean data has no issues
    assert quality_report['missing_values']['columns_with_missing'] == {}
    assert quality_report['duplicates']['duplicate_rows'] == 0


if __name__ == "__main__":
    pytest.main([__file__])