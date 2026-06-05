"""
Training script for Dynamic Pricing RL Engine
Loads CSV data, runs Q-learning optimization, and saves trained models
"""

import os
import sys
import json
import logging
import asyncio
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.models.dynamic_pricing.dynamic_pricing_engine import DynamicPricingEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "dynamic_pricing")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models", "dynamic_pricing")


def load_csv(filename: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, filename)
    try:
        if not os.path.exists(path):
            logger.warning(f"File not found: {path}, returning empty DataFrame")
            return pd.DataFrame()
        df = pd.read_csv(path)
        logger.info(f"Loaded {filename}: {len(df)} rows, columns={list(df.columns)}")
        return df
    except Exception as e:
        logger.error(f"Failed to load {filename}: {e}")
        return pd.DataFrame()


async def train():
    logger.info("=" * 60)
    logger.info("Dynamic Pricing RL Training")
    logger.info("=" * 60)

    # 1. Load CSV data
    logger.info("Step 1: Loading CSV data")
    client_data = load_csv("client_value_data.csv")
    market_data = load_csv("market_rates.csv")
    competitor_data = load_csv("competitive_pricing.csv")

    if client_data.empty:
        logger.error("client_value_data.csv is empty or could not be loaded. Aborting.")
        return False

    if market_data.empty:
        logger.warning("market_rates.csv is empty — RL will use fallback values")

    if competitor_data.empty:
        logger.warning("competitive_pricing.csv is empty — RL will use fallback values")

    # 2. Initialize engine and run RL optimization
    logger.info("Step 2: Running RL pricing optimization (episodes=100)")
    engine = DynamicPricingEngine()

    results = await engine.optimize_pricing_with_rl(
        client_data=client_data,
        market_data=market_data,
        competitor_data=competitor_data,
        episodes=100,
    )

    if not results:
        logger.error("RL optimization returned empty results. Aborting.")
        return False

    logger.info(
        f"RL optimization complete: "
        f"{results.get('total_episodes')} episodes, "
        f"{results.get('q_table_size')} Q-table states, "
        f"avg final reward={results.get('average_final_reward'):.2f}"
    )

    # 3. Save models
    logger.info("Step 3: Saving trained models")
    os.makedirs(MODEL_DIR, exist_ok=True)

    engine.save_models(MODEL_DIR)

    # 4. Save training metadata
    meta = {
        "episodes": results.get("total_episodes"),
        "q_table_size": results.get("q_table_size"),
        "average_final_reward": results.get("average_final_reward"),
        "timestamp": str(pd.Timestamp.now()),
    }
    meta_path = os.path.join(MODEL_DIR, "training_meta.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    logger.info(f"Training metadata saved to {meta_path}")

    # 5. Verify by loading back
    logger.info("Step 4: Verifying model persistence (load_models)")
    loaded = engine.load_models(MODEL_DIR)
    logger.info(f"Model verification: {'SUCCESS' if loaded else 'FAILED'}")

    logger.info("=" * 60)
    logger.info("Training completed successfully")
    logger.info("=" * 60)
    return True


if __name__ == "__main__":
    success = asyncio.run(train())
    sys.exit(0 if success else 1)
