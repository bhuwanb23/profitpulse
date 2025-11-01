"""
Test the functionality of churn predictor modules
"""

import sys
import os
import pytest
import pandas as pd
import numpy as np

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'models'))


def test_data_preparator_functionality():
    """Test that the data preparator can generate mock data"""
    from churn_predictor.data_preparation import ChurnDataPreparator
    import datetime
    
    preparator = ChurnDataPreparator()
    
    # Test mock data generation
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    end_date = datetime.datetime.now()
    
    # Test client history generation
    client_history = preparator._generate_mock_client_history_data(start_date, end_date)
    assert isinstance(client_history, pd.DataFrame)
    assert len(client_history) > 0
    assert 'client_id' in client_history.columns
    assert 'churn' in client_history.columns
    
    # Test interactions generation
    interactions = preparator._generate_mock_client_interactions(start_date, end_date)
    assert isinstance(interactions, pd.DataFrame)
    assert len(interactions) >= 0  # Can be empty
    if len(interactions) > 0:
        assert 'client_id' in interactions.columns
        assert 'interaction_date' in interactions.columns
    
    # Test financial metrics generation
    financial_data = preparator._generate_mock_financial_metrics(start_date, end_date)
    assert isinstance(financial_data, pd.DataFrame)
    assert len(financial_data) >= 0  # Can be empty
    if len(financial_data) > 0:
        assert 'client_id' in financial_data.columns
        assert 'payment_date' in financial_data.columns
    
    # Test service usage generation
    service_data = preparator._generate_mock_service_usage(start_date, end_date)
    assert isinstance(service_data, pd.DataFrame)
    assert len(service_data) >= 0  # Can be empty
    if len(service_data) > 0:
        assert 'client_id' in service_data.columns
        assert 'usage_date' in service_data.columns


def test_feature_engineer_functionality():
    """Test that the feature engineer can create features"""
    from churn_predictor.feature_engineering import ChurnFeatureEngineer
    import datetime
    
    engineer = ChurnFeatureEngineer()
    
    # Create sample data
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
    assert isinstance(temporal_features, pd.DataFrame)
    assert len(temporal_features) == len(sample_data)
    # Check that new temporal columns were added
    assert 'contract_duration_days' in temporal_features.columns
    
    # Test derived features (with minimal data)
    derived_features = engineer.create_derived_features(sample_data)
    assert isinstance(derived_features, pd.DataFrame)
    assert len(derived_features) == len(sample_data)


def test_model_initialization():
    """Test that ML models can be initialized"""
    from churn_predictor.models import (
        ChurnLogisticRegression, ChurnNeuralNetwork, 
        ChurnGradientBoosting, ChurnEnsembleModel
    )
    
    # Test Logistic Regression
    lr_model = ChurnLogisticRegression()
    assert lr_model is not None
    assert hasattr(lr_model, 'train')
    assert hasattr(lr_model, 'predict')
    
    # Test Neural Network
    nn_model = ChurnNeuralNetwork()
    assert nn_model is not None
    assert hasattr(nn_model, 'train')
    assert hasattr(nn_model, 'predict')
    
    # Test Gradient Boosting (XGBoost)
    xgb_model = ChurnGradientBoosting(model_type='xgboost')
    assert xgb_model is not None
    assert hasattr(xgb_model, 'train')
    assert hasattr(xgb_model, 'predict')
    
    # Test Gradient Boosting (Random Forest)
    rf_model = ChurnGradientBoosting(model_type='random_forest')
    assert rf_model is not None
    assert hasattr(rf_model, 'train')
    assert hasattr(rf_model, 'predict')
    
    # Test Ensemble Model
    ensemble_model = ChurnEnsembleModel()
    assert ensemble_model is not None
    assert hasattr(ensemble_model, 'train')
    assert hasattr(ensemble_model, 'predict')


def test_training_pipeline():
    """Test that the training pipeline can be initialized"""
    from churn_predictor.training_pipeline import ChurnTrainingPipeline, ChurnModelOptimizer
    
    # Test training pipeline
    pipeline = ChurnTrainingPipeline()
    assert pipeline is not None
    assert hasattr(pipeline, 'create_train_test_split')
    assert hasattr(pipeline, 'handle_class_imbalance')
    
    # Test model optimizer
    optimizer = ChurnModelOptimizer()
    assert optimizer is not None
    assert hasattr(optimizer, 'select_features')
    assert hasattr(optimizer, 'optimize_hyperparameters')


def test_churn_prevention_system():
    """Test that the churn prevention system can be initialized"""
    from churn_predictor.churn_prevention import (
        ChurnRiskScorer, ChurnRecommendationEngine, 
        ChurnEarlyWarningSystem, ChurnInterventionTracker
    )
    
    # Test risk scorer
    risk_scorer = ChurnRiskScorer()
    assert risk_scorer is not None
    assert hasattr(risk_scorer, 'calculate_risk_score')
    
    # Test recommendation engine
    recommender = ChurnRecommendationEngine()
    assert recommender is not None
    assert hasattr(recommender, 'generate_recommendations')
    
    # Test early warning system
    early_warning = ChurnEarlyWarningSystem()
    assert early_warning is not None
    assert hasattr(early_warning, 'identify_high_risk_clients')
    
    # Test intervention tracker
    tracker = ChurnInterventionTracker()
    assert tracker is not None
    assert hasattr(tracker, 'log_intervention')
    assert hasattr(tracker, 'update_intervention_outcome')


def test_main_orchestrator():
    """Test that the main orchestrator can be initialized"""
    from churn_predictor.churn_predictor import ChurnPredictor
    
    # Test main predictor
    predictor = ChurnPredictor()
    assert predictor is not None
    assert hasattr(predictor, 'prepare_data')
    assert hasattr(predictor, 'engineer_features')
    assert hasattr(predictor, 'train_models')
    assert hasattr(predictor, 'predict_churn')