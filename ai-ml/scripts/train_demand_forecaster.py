"""
Training script for the Demand Forecaster model.
Loads CSV data, trains LSTM and ARIMA models, generates forecasts,
and saves the trained models to disk.
"""

import asyncio
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from src.models.demand_forecaster.demand_forecaster import DemandForecaster

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('train_demand_forecaster')

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'demand_forecaster')
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models', 'demand_forecaster')


def load_csv(filename: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, filename)
    logger.info(f"Loading {path}")
    if not os.path.exists(path):
        logger.error(f"File not found: {path}")
        return pd.DataFrame()
    df = pd.read_csv(path)
    logger.info(f"  -> {len(df)} rows, columns: {list(df.columns)}")
    return df


async def train():
    # 1. Load all CSV data
    ticket_data = load_csv('historical_tickets.csv')
    load_csv('client_growth_data.csv')
    load_csv('external_factors.csv')
    load_csv('resource_capacity.csv')
    load_csv('seasonal_patterns.csv')

    if ticket_data.empty:
        logger.error("No ticket data loaded - cannot train")
        return None, None, None, None

    # 2. Create the forecaster
    forecaster = DemandForecaster()

    # 3. Train LSTM
    logger.info("Training LSTM model...")
    lstm_result = await forecaster.train_lstm_model(ticket_data)
    logger.info(f"LSTM result: success={lstm_result.get('success')}, "
                f"msg={lstm_result.get('message')}")

    # 4. Train ARIMA
    logger.info("Training ARIMA model...")
    arima_result = await forecaster.train_arima_model(ticket_data)
    logger.info(f"ARIMA result: success={arima_result.get('success')}, "
                f"msg={arima_result.get('message')}")

    # 5. Generate forecast
    logger.info("Generating demand forecast (horizon=30)...")
    forecast_result = await forecaster.generate_demand_forecast(ticket_data, forecast_horizon=30)
    logger.info(f"Forecast result: success={forecast_result.get('success')}, "
                f"msg={forecast_result.get('message')}")
    preds = forecast_result.get('ensemble_predictions', [])
    if preds:
        logger.info(f"  Predictions: min={min(preds):.1f}, max={max(preds):.1f}, "
                    f"avg={sum(preds) / len(preds):.1f}, count={len(preds)}")

    # 6. Save models
    os.makedirs(MODELS_DIR, exist_ok=True)
    logger.info(f"Saving models to {MODELS_DIR}...")
    save_result = forecaster.save_models(MODELS_DIR)
    for model_name, ok in save_result.items():
        status = "OK" if ok else "SKIPPED"
        logger.info(f"  {model_name}: {status}")

    return forecaster, lstm_result, arima_result, forecast_result


def main():
    logger.info("=" * 60)
    logger.info("Demand Forecaster Training Script")
    logger.info("=" * 60)
    logger.info(f"Data dir:  {DATA_DIR}")
    logger.info(f"Models dir: {MODELS_DIR}")

    try:
        forecaster, lstm_result, arima_result, forecast_result = asyncio.run(train())

        if forecaster is None:
            logger.error("Training failed - no forecaster created")
            sys.exit(1)

        any_success = (
            (lstm_result or {}).get('success', False) or
            (arima_result or {}).get('success', False)
        )
        if any_success:
            logger.info("Training completed successfully")
        else:
            logger.warning("No models trained successfully")

        # Verify saved models can be loaded
        logger.info("Verifying model loading...")
        loaded = forecaster.load_models(MODELS_DIR)
        logger.info(f"Model loading verification: {loaded}")

    except Exception as e:
        logger.error(f"Training failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
