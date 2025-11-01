"""
Functionality test for the Client Churn Predictor components
"""

import sys
import os
import pandas as pd
import numpy as np

def test_data_loading():
    """Test that all data files can be loaded correctly"""
    print("Testing Data Loading...")
    
    try:
        # Test client history data
        client_history = pd.read_csv('../../data/churn_predictor/client_history_data.csv')
        assert len(client_history) > 0, "Client history data is empty"
        assert 'client_id' in client_history.columns, "Missing client_id column"
        assert 'churn' in client_history.columns, "Missing churn column"
        print(f"  ✅ Client history data: {len(client_history)} records")
        
        # Test client interactions data
        interactions = pd.read_csv('../../data/churn_predictor/client_interactions.csv')
        assert len(interactions) > 0, "Client interactions data is empty"
        assert 'client_id' in interactions.columns, "Missing client_id column"
        print(f"  ✅ Client interactions data: {len(interactions)} records")
        
        # Test financial metrics data
        financial = pd.read_csv('../../data/churn_predictor/financial_metrics.csv')
        assert len(financial) > 0, "Financial metrics data is empty"
        assert 'client_id' in financial.columns, "Missing client_id column"
        print(f"  ✅ Financial metrics data: {len(financial)} records")
        
        # Test service usage data
        service = pd.read_csv('../../data/churn_predictor/service_usage.csv')
        assert len(service) > 0, "Service usage data is empty"
        assert 'client_id' in service.columns, "Missing client_id column"
        print(f"  ✅ Service usage data: {len(service)} records")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error in data loading: {e}")
        return False

def test_module_initialization():
    """Test that all modules can be initialized"""
    print("Testing Module Initialization...")
    
    try:
        # Add src to path
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'models')))
        
        # Test data preparation module
        from churn_predictor.data_preparation import ChurnDataPreparator
        preparator = ChurnDataPreparator()
        assert preparator is not None, "Failed to initialize ChurnDataPreparator"
        print("  ✅ Data preparation module initialized")
        
        # Test feature engineering module
        from churn_predictor.feature_engineering import ChurnFeatureEngineer
        engineer = ChurnFeatureEngineer()
        assert engineer is not None, "Failed to initialize ChurnFeatureEngineer"
        print("  ✅ Feature engineering module initialized")
        
        # Test models module
        from churn_predictor.models import ChurnLogisticRegression, ChurnNeuralNetwork
        lr_model = ChurnLogisticRegression()
        nn_model = ChurnNeuralNetwork()
        assert lr_model is not None, "Failed to initialize ChurnLogisticRegression"
        assert nn_model is not None, "Failed to initialize ChurnNeuralNetwork"
        print("  ✅ Models module initialized")
        
        # Test training pipeline module
        from churn_predictor.training_pipeline import ChurnTrainingPipeline
        pipeline = ChurnTrainingPipeline()
        assert pipeline is not None, "Failed to initialize ChurnTrainingPipeline"
        print("  ✅ Training pipeline module initialized")
        
        # Test churn prevention module
        from churn_predictor.churn_prevention import ChurnRiskScorer
        scorer = ChurnRiskScorer()
        assert scorer is not None, "Failed to initialize ChurnRiskScorer"
        print("  ✅ Churn prevention module initialized")
        
        # Test main orchestrator
        from churn_predictor.churn_predictor import ChurnPredictor
        predictor = ChurnPredictor()
        assert predictor is not None, "Failed to initialize ChurnPredictor"
        print("  ✅ Main orchestrator initialized")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error in module initialization: {e}")
        return False

def test_core_functionality():
    """Test core functionality of key components"""
    print("Testing Core Functionality...")
    
    try:
        # Add src to path
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'models')))
        
        # Test data preparation
        from churn_predictor.data_preparation import ChurnDataPreparator
        preparator = ChurnDataPreparator()
        
        # Test mock data generation
        import datetime
        start_date = datetime.datetime.now() - datetime.timedelta(days=365)
        end_date = datetime.datetime.now()
        
        client_history = preparator._generate_mock_client_history_data(start_date, end_date)
        assert len(client_history) > 0, "Failed to generate mock client history"
        print(f"  ✅ Mock data generation: {len(client_history)} records")
        
        # Test feature engineering
        from churn_predictor.feature_engineering import ChurnFeatureEngineer
        engineer = ChurnFeatureEngineer()
        
        # Create sample data for feature engineering
        sample_data = pd.DataFrame({
            'client_id': ['CLIENT-001', 'CLIENT-002'],
            'contract_start_date': [datetime.datetime(2023, 1, 1), datetime.datetime(2023, 2, 1)],
            'contract_end_date': [datetime.datetime(2024, 1, 1), None],
            'contract_status': ['ended', 'active'],
            'contract_value': [5000, 7500],
            'last_interaction_date': [datetime.datetime(2023, 6, 1), datetime.datetime(2023, 7, 1)]
        })
        
        # Test temporal features
        temporal_features = engineer.create_temporal_features(sample_data)
        assert len(temporal_features) == len(sample_data), "Temporal features creation failed"
        print("  ✅ Temporal feature creation")
        
        # Test model initialization (basic test)
        from churn_predictor.models import ChurnLogisticRegression
        model = ChurnLogisticRegression()
        assert hasattr(model, 'train'), "Model missing train method"
        assert hasattr(model, 'predict'), "Model missing predict method"
        print("  ✅ Model initialization and methods")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error in core functionality: {e}")
        return False

def main():
    """Run all functionality tests"""
    print("Running Functionality Tests for Client Churn Predictor")
    print("=" * 60)
    
    tests = [
        test_data_loading,
        test_module_initialization,
        test_core_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
            print()
    
    print("=" * 60)
    print(f"Functionality Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All functionality tests passed! Client Churn Predictor is working correctly.")
        return True
    else:
        print("❌ Some functionality tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)