"""
Simple example usage of the Client Profitability Predictor data preparation modules
"""

import pandas as pd
import sys
import os

# Add the ai-ml directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.profitability_predictor.historical_data_collector import HistoricalDataCollector
from src.models.profitability_predictor.feature_engineering import ProfitabilityFeatureEngineer
from src.models.profitability_predictor.data_splitter import ProfitabilityDataSplitter
from src.models.profitability_predictor.data_quality import ProfitabilityDataQualityAssessor


def create_sample_financial_data():
    """Create sample financial data for demonstration"""
    data = {
        'id': ['client_1', 'client_2', 'client_3', 'client_4', 'client_5'],
        'name': ['Acme Corp', 'TechStart Inc', 'Global Solutions', 'DataSystems', 'InnovateCo'],
        'industry': ['Manufacturing', 'Technology', 'Finance', 'Healthcare', 'Technology'],
        'contract_type': ['annual', 'monthly', 'quarterly', 'annual', 'monthly'],
        'contract_value': [50000.0, 5000.0, 25000.0, 30000.0, 7500.0],
        'start_date': ['2023-01-01', '2023-03-01', '2023-02-01', '2023-01-15', '2023-04-01'],
        'end_date': ['2023-12-31', None, '2023-11-30', '2023-12-15', None],
        'is_active': [True, True, False, True, True],
        'total_revenue': [45000.0, 6000.0, 20000.0, 25000.0, 7000.0],
        'total_costs': [30000.0, 4000.0, 15000.0, 18000.0, 5000.0],
        'profit': [15000.0, 2000.0, 5000.0, 7000.0, 2000.0],
        'profit_margin': [0.33, 0.33, 0.25, 0.28, 0.29],
        'service_count': [10, 5, 8, 7, 3],
        'total_service_value': [10000.0, 5000.0, 8000.0, 6000.0, 2000.0],
        'total_quantity': [100, 50, 80, 60, 20],
        'revenue_per_service': [4500.0, 1200.0, 2500.0, 3571.0, 2333.0],
        'cost_per_service': [3000.0, 800.0, 1875.0, 2571.0, 1667.0]
    }
    
    return pd.DataFrame(data)


def main():
    """Main example function"""
    print("=== Client Profitability Predictor Data Preparation Example ===")
    
    # Create sample financial data
    print("\n1. Creating sample financial data...")
    financial_data = create_sample_financial_data()
    print(f"Created data for {len(financial_data)} clients")
    print("Sample data:")
    print(financial_data.head())
    
    # 2. Engineer features
    print("\n2. Engineering features...")
    feature_engineer = ProfitabilityFeatureEngineer()
    features_df = feature_engineer.engineer_features(financial_data)
    print(f"Engineered {len(features_df.columns)} features for {len(features_df)} clients")
    print("Feature columns:", list(features_df.columns[:10]), "...")
    
    # 3. Assess data quality
    print("\n3. Assessing data quality...")
    quality_assessor = ProfitabilityDataQualityAssessor()
    quality_report = quality_assessor.assess_data_quality(features_df)
    print("Data quality summary:")
    print(f"  - Total records: {quality_report['summary']['total_records']}")
    print(f"  - Total features: {quality_report['summary']['total_columns']}")
    print(f"  - Columns with missing values: {quality_report['summary']['columns_with_missing']}")
    print(f"  - Duplicate rows: {quality_report['summary']['duplicate_rows']}")
    print(f"  - Numerical columns: {quality_report['summary']['numerical_columns']}")
    print(f"  - Categorical columns: {quality_report['summary']['categorical_columns']}")
    
    # 4. Split data
    print("\n4. Splitting data...")
    data_splitter = ProfitabilityDataSplitter()
    try:
        # Try stratified split first
        train_df, validation_df, test_df = data_splitter.split_dataset(
            features_df, 
            target_column='profit_margin',
            split_method='stratified',
            test_size=0.2, 
            validation_size=0.2,
            random_state=42
        )
    except ValueError as e:
        print(f"Stratified split failed: {e}")
        print("Using time-based split instead...")
        # Fall back to time-based split
        train_df, validation_df, test_df = data_splitter.split_dataset(
            features_df, 
            target_column='profit_margin',
            split_method='time_based',
            test_size=0.2, 
            validation_size=0.2
        )
    print(f"Data split - Train: {len(train_df)}, Validation: {len(validation_df)}, Test: {len(test_df)}")
    
    print("\n=== Example completed successfully ===")


if __name__ == "__main__":
    main()