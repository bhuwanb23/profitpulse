"""
Train Revenue Leak Detection Models
Loads CSV data, prepares features, trains the ensemble, and saves models to disk.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

from src.models.revenue_leak_detector.revenue_leak_predictor import RevenueLeakPredictor


async def main():
    data_dir = PROJECT_ROOT / 'data' / 'revenue_leak_detector'
    models_dir = PROJECT_ROOT / 'models' / 'revenue_leak'
    models_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Revenue Leak Detector - Model Training")
    print("=" * 60)

    # Step 1: Initialize predictor
    print("\n[1/6] Initializing Revenue Leak Predictor...")
    predictor = RevenueLeakPredictor()
    await predictor.initialize()
    print("  Predictor initialized")

    # Step 2: Load CSV data
    print("\n[2/6] Loading CSV data...")
    invoice_path = data_dir / 'invoice_data.csv'
    service_path = data_dir / 'service_data.csv'
    timelog_path = data_dir / 'time_log_data.csv'

    csv_files_exist = all(p.exists() for p in [invoice_path, service_path, timelog_path])

    if csv_files_exist:
        invoice_data = pd.read_csv(invoice_path, parse_dates=['invoice_date', 'due_date'])
        service_data = pd.read_csv(service_path, parse_dates=['service_date'])
        time_log_data = pd.read_csv(timelog_path, parse_dates=['start_time', 'end_time'])
        print(f"  Loaded {len(invoice_data)} invoices, {len(time_log_data)} time logs, {len(service_data)} service records")
    else:
        print("  CSV files not found, using mock data generation...")
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 3, 31)
        invoice_data = await predictor.data_preparator.collect_invoice_data(start_date, end_date)
        time_log_data = await predictor.data_preparator.collect_time_log_data(start_date, end_date)
        service_data = await predictor.data_preparator.collect_service_delivery_data(start_date, end_date)
        print(f"  Generated mock data: {len(invoice_data)} invoices, {len(time_log_data)} time logs, {len(service_data)} service records")

    # Step 3: Prepare features
    print("\n[3/6] Preparing features...")
    features = predictor.data_preparator.prepare_features(invoice_data, time_log_data, service_data)

    if features.empty:
        print("  No features could be prepared from the data")
        return False

    feature_cols = [c for c in features.columns if c != 'client_id']
    X = features[feature_cols]
    print(f"  Features shape: {X.shape}")
    print(f"  Feature columns: {list(X.columns)}")

    # Step 4: Split data into train/test
    print("\n[4/6] Splitting data into train/test sets...")
    X_train, X_test = predictor.training_pipeline.prepare_data(X)
    print(f"  Train: {len(X_train)} samples, Test: {len(X_test)} samples")

    # Step 5: Train ensemble model (trains IsolationForest, Autoencoder, DBSCAN, OneClassSVM)
    print("\n[5/6] Training ensemble model...")
    ensemble = predictor.anomaly_models['ensemble']
    success = ensemble.train(X_train)

    if success:
        print("  Ensemble model trained successfully")
    else:
        print("  Some models in the ensemble failed to train (TensorFlow may be missing)")
        print("  Trained sub-models will still be saved")

    # Step 6: Save models to disk
    print(f"\n[6/6] Saving models to {models_dir}...")
    save_success = predictor.save_models(str(models_dir))

    if save_success:
        print("  Models saved successfully")
    else:
        print("  Failed to save models")
        return False

    # Verify loaded models
    print("\n" + "-" * 60)
    print("Verification")
    print("-" * 60)
    verify = RevenueLeakPredictor()
    load_success = verify.load_models(str(models_dir))
    if load_success:
        print("  Models loaded and verified successfully")
        for name, model in verify.anomaly_models.items():
            status = "trained" if getattr(model, 'is_trained', False) else "untrained"
            print(f"    - {name}: {status}")
    else:
        print("  Model verification FAILED")
        return False

    print("\n" + "=" * 60)
    print("Training complete!")
    print(f"Models saved to: {models_dir}")
    print("=" * 60)
    return True


if __name__ == '__main__':
    success = asyncio.run(main())
    if not success:
        print("\nTraining failed")
        sys.exit(1)
