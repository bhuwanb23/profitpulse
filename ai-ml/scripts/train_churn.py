"""Train churn prediction models using CSV data"""

import sys
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import logging
import pandas as pd
import numpy as np
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATA_DIR = project_root / "data" / "churn_predictor"
MODEL_DIR = project_root / "models" / "churn"


def main():
    print("=" * 60)
    print("Churn Predictor Training Script")
    print("=" * 60)

    # 1. Load CSV data
    print("\n[1/5] Loading CSV data...")
    client_history = pd.read_csv(
        DATA_DIR / "client_history_data.csv",
        parse_dates=['contract_start_date', 'contract_end_date']
    )
    interactions = pd.read_csv(
        DATA_DIR / "client_interactions.csv",
        parse_dates=['interaction_date']
    )
    financial_metrics = pd.read_csv(
        DATA_DIR / "financial_metrics.csv",
        parse_dates=['payment_date']
    )
    service_usage = pd.read_csv(
        DATA_DIR / "service_usage.csv",
        parse_dates=['usage_date']
    )
    print(f"   client_history:     {client_history.shape}")
    print(f"   interactions:       {interactions.shape}")
    print(f"   financial_metrics:  {financial_metrics.shape}")
    print(f"   service_usage:      {service_usage.shape}")

    # 2. Prepare data for feature engineering
    print("\n[2/5] Preparing data for feature engineering...")

    if 'last_interaction_date' not in client_history.columns:
        last_dates = interactions.groupby('client_id')['interaction_date'].max().reset_index()
        last_dates.columns = ['client_id', 'last_interaction_date']
        client_history = client_history.merge(last_dates, on='client_id', how='left')
        client_history['last_interaction_date'] = client_history['last_interaction_date'].fillna(datetime.now())
        print("   Added last_interaction_date from interactions data")

    client_history['contract_end_date'] = client_history['contract_end_date'].fillna(
        datetime.now() + pd.Timedelta(days=365)
    )
    print("   Filled missing contract_end_date for active contracts")

    data = {
        'client_history': client_history,
        'interactions': interactions,
        'financial_data': financial_metrics,
        'service_data': service_usage
    }

    # 3. Initialize predictor and engineer features
    print("\n[3/5] Engineering features...")
    from src.models.churn_predictor.churn_predictor import ChurnPredictor
    predictor = ChurnPredictor()

    features = predictor.engineer_features(data)
    if features.empty:
        print("ERROR: Feature engineering failed - no features produced")
        sys.exit(1)

    # Keep only numeric columns plus client_id and churn
    numeric_cols = features.select_dtypes(include=[np.number]).columns.tolist()
    keep_cols = [c for c in ['client_id', 'churn'] if c in features.columns] + \
                [c for c in numeric_cols if c not in ('client_id', 'churn')]
    features = features[keep_cols]

    print(f"   Features shape: {features.shape}")
    print(f"   Feature columns: {list(features.columns)}")
    churn_counts = features['churn'].value_counts()
    print(f"   Churn distribution: {churn_counts.to_dict()}")

    # 4. Train models
    print("\n[4/5] Training models...")
    success = predictor.train_models(features)

    if not success:
        print("ERROR: Model training failed")
        sys.exit(1)

    print("   Training completed successfully!")

    # 5. Save models
    print("\n[5/5] Saving models...")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    save_success = predictor.save_models(str(MODEL_DIR))

    if save_success:
        print(f"   Models saved to: {MODEL_DIR}")

        print("\n   Verifying model loading...")
        verify_predictor = ChurnPredictor()
        load_success = verify_predictor.load_models(str(MODEL_DIR))
        if load_success and verify_predictor.is_trained:
            print("   Model verification PASSED")
        else:
            print("   WARNING: Model verification failed")
    else:
        print("   ERROR: Failed to save models")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
