"""
Example script demonstrating how to use the Revenue Leak Detector with real CSV data
"""

import pandas as pd
import sys
import os
import numpy as np
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.revenue_leak_detector.data_preparation import RevenueLeakDataPreparator
from src.models.revenue_leak_detector.anomaly_models import EnsembleAnomalyDetector
from src.models.revenue_leak_detector.recovery_system import LeakClassifier, RecoveryAmountEstimator, RecommendationEngine

def main():
    print("Revenue Leak Detector Example")
    print("=" * 40)
    
    # Initialize the data preparator
    preparator = RevenueLeakDataPreparator()
    
    # Load data from CSV files (this will automatically use the CSV files we created)
    print("Loading data from CSV files...")
    
    # For this example, we'll load the data directly from CSV files to show how it works
    data_dir = "data/revenue_leak_detector"
    
    invoice_data = pd.read_csv(f"{data_dir}/invoice_data.csv", parse_dates=['invoice_date', 'due_date'])
    time_log_data = pd.read_csv(f"{data_dir}/time_log_data.csv", parse_dates=['start_time', 'end_time'])
    service_data = pd.read_csv(f"{data_dir}/service_data.csv", parse_dates=['service_date'])
    
    print(f"Loaded {len(invoice_data)} invoice records")
    print(f"Loaded {len(time_log_data)} time log records")
    print(f"Loaded {len(service_data)} service records")
    
    # Prepare features for anomaly detection
    print("\nPreparing features for anomaly detection...")
    features = preparator.prepare_features(invoice_data, time_log_data, service_data)
    print(f"Prepared features for {len(features)} clients")
    
    # Display some of the features
    print("\nSample features:")
    sample_features = features[['client_id', 'total_invoiced', 'unpaid_amount', 'unbilled_hours', 'revenue_leak_score']].head()
    print(sample_features)
    
    # Run anomaly detection
    print("\nRunning anomaly detection...")
    detector = EnsembleAnomalyDetector(contamination=0.1)
    
    # Use the revenue leak score as the feature for anomaly detection
    # We need to train the detector first
    revenue_scores = [[score] for score in features['revenue_leak_score'].tolist()]
    X_train = pd.DataFrame({'revenue_leak_score': features['revenue_leak_score'].tolist()})
    detector.train(X_train)
    
    # Now predict anomalies
    anomalies = detector.predict(X_train)
    
    # Add anomaly results to the features dataframe
    features_with_anomalies = features.copy()
    features_with_anomalies['anomaly'] = anomalies
    
    # Show clients identified as anomalies
    anomaly_clients = features_with_anomalies[features_with_anomalies['anomaly'] == -1]
    print(f"\nFound {len(anomaly_clients)} clients with potential revenue leaks:")
    if len(anomaly_clients) > 0:
        anomaly_display = anomaly_clients[['client_id', 'revenue_leak_score']]
        print(anomaly_display)
    
    # Use the recovery system to classify leaks and provide recommendations
    print("\nAnalyzing revenue leaks...")
    leak_classifier = LeakClassifier()
    recovery_estimator = RecoveryAmountEstimator()
    recommendation_engine = RecommendationEngine()
    
    # Create a simple anomalies dataframe for classification
    if len(anomaly_clients) > 0:
        client_ids = list(anomaly_clients['client_id'])
        leak_scores = list(anomaly_clients['revenue_leak_score'])
        
        anomalies_df = pd.DataFrame({
            'client_id': client_ids,
            'anomaly_type': ['revenue_leak'] * len(anomaly_clients),
            'potential_loss': leak_scores,
            'description': ['High revenue leak score'] * len(anomaly_clients),
            'severity': ['high'] * len(anomaly_clients)
        })
        
        # Classify the types of leaks for anomalous clients
        classified_leaks = leak_classifier.classify_leaks(anomalies_df, features)
        print(f"\nClassified {len(classified_leaks)} leaks:")
        
        for _, leak in classified_leaks.iterrows():
            client_id = leak['client_id']
            leak_type = leak['leak_type']
            potential_loss = leak['potential_loss']
            
            print(f"\nClient {client_id}:")
            print(f"  Leak Type: {leak_type}")
            print(f"  Potential Loss: ${potential_loss:.2f}")
            
            # Generate recommendations (simplified)
            print("  Recommendations:")
            print("    - Review billing records for accuracy")
            print("    - Follow up on overdue invoices")
            print("    - Verify time tracking entries")
    else:
        print("No anomalies detected in this dataset.")
    
    print("\nExample completed successfully!")

if __name__ == "__main__":
    main()