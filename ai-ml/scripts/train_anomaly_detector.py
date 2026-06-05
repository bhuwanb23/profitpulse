#!/usr/bin/env python3
"""
Training script for Anomaly Detector models.
Loads CSV data, trains all 5 models, and saves them to disk.
"""

import os
import sys
import logging
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.anomaly_detector.anomaly_orchestrator import AnomalyDetectorOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'anomaly_detector')
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models', 'anomaly_detector')

CSV_FILES = [
    'network_traffic.csv',
    'system_metrics.csv',
    'transaction_data.csv',
    'user_behavior.csv',
]


def load_and_combine_data(data_dir: str) -> pd.DataFrame:
    frames = []
    for csv_file in CSV_FILES:
        file_path = os.path.join(data_dir, csv_file)
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}, skipping")
            continue
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {csv_file}: {df.shape}")
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            logger.warning(f"No numeric columns in {csv_file}, skipping")
            continue
        frames.append(numeric_df)

    if not frames:
        logger.error("No data loaded from any CSV")
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True).fillna(0)
    logger.info(f"Combined training data: {combined.shape}, columns: {list(combined.columns)}")
    return combined


def main():
    logger.info("=" * 60)
    logger.info("Anomaly Detector Training Script")
    logger.info("=" * 60)

    training_data = load_and_combine_data(DATA_DIR)
    if training_data.empty:
        logger.error("No training data available. Exiting.")
        return 1

    logger.info("Creating orchestrator and training models...")
    orchestrator = AnomalyDetectorOrchestrator()

    success = orchestrator.train_models(training_data)
    if not success:
        logger.warning("One or more models had training issues")

    os.makedirs(MODELS_DIR, exist_ok=True)
    logger.info(f"Saving models to {MODELS_DIR}...")
    save_success = orchestrator.save_models(MODELS_DIR)

    if save_success:
        logger.info("All models saved successfully")
    else:
        logger.error("Failed to save models")
        return 1

    logger.info("Training complete")
    return 0


if __name__ == '__main__':
    sys.exit(main())
