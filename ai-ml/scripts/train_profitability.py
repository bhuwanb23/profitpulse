"""
Training script for Profitability Predictor models.
Generates synthetic data if DB is empty, runs the training pipeline,
and fixes model file paths for the predictor.
"""

import sys
import os
import shutil
import logging
from pathlib import Path

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("train_profitability")

OUTPUT_DIR = project_root / "models" / "profitability"
DB_DIR = project_root / "database"
DB_PATH = DB_DIR / "superhack.db"


def ensure_database():
    """Create database directory and populate synthetic data if tables are missing."""
    import sqlite3

    DB_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients'")
    if cursor.fetchone():
        # Tables exist – do nothing
        row_count = cursor.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
        logger.info("Database already has %d client records, skipping synthetic data generation", row_count)
        conn.close()
        return

    logger.info("Database empty – generating synthetic data…")
    _generate_synthetic_data(conn)
    conn.commit()
    conn.close()
    logger.info("Synthetic data written to %s", DB_PATH)


def _generate_synthetic_data(conn):
    """Populate the database with realistic synthetic MSP data."""
    import random
    from datetime import datetime, timedelta

    random.seed(42)

    industries = ["Technology", "Healthcare", "Finance", "Education", "Retail",
                  "Manufacturing", "Legal", "Real Estate", "Nonprofit", "Government"]
    contract_types = ["monthly", "quarterly", "annual", "biennial"]
    invoice_statuses = ["paid", "pending", "overdue"]
    service_categories = ["Cloud", "Security", "Support", "Networking", "Consulting",
                          "Backup", "Compliance", "Infrastructure", "DevOps", "Analytics"]
    first_names = ["Acme", "Global", "Premier", "Vertex", "Nova", "Apex", "Zenith",
                   "Pinnacle", "Summit", "Titan", "Core", "Elite", "Prime", "Fusion", "Dynamo"]
    last_names = ["Tech", "Solutions", "Systems", "Services", "Consulting", "Group",
                  "Industries", "Partners", "Corp", "Enterprises", "Associates", "Logistics"]

    today = datetime.now()
    client_ids = []

    # ── Clients ──────────────────────────────────────────────────────────
    for cid in range(1, 101):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        industry = random.choice(industries)
        ctype = random.choice(contract_types)
        cv = round(random.uniform(10000, 500000), 2)

        start = today - timedelta(days=random.randint(30, 800))
        end = start + timedelta(days={
            "monthly": 30, "quarterly": 90, "annual": 365, "biennial": 730
        }[ctype]) if ctype != "biennial" else start + timedelta(days=random.choice([365, 730]))
        active = 1 if end > today else 0

        conn.execute(
            "INSERT INTO clients (id, name, industry, contract_type, contract_value, start_date, end_date, is_active) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (cid, name, industry, ctype, cv, start.isoformat(), end.isoformat(), active),
        )
        client_ids.append(cid)

    # ── Services ─────────────────────────────────────────────────────────
    for sid in range(1, 11):
        conn.execute("INSERT INTO services (id, category) VALUES (?, ?)",
                     (sid, service_categories[sid - 1]))

    # ── Invoices ─────────────────────────────────────────────────────────
    invoices = []
    for cid in client_ids:
        num_invoices = random.randint(3, 24)
        for _ in range(num_invoices):
            inv_date = today - timedelta(days=random.randint(1, 365))
            amount = round(random.uniform(500, 50000), 2)
            status = random.choices(invoice_statuses, weights=[70, 20, 10])[0]
            invoices.append((cid, inv_date.isoformat(), amount, status))

    conn.executemany(
        "INSERT INTO invoices (client_id, invoice_date, total_amount, status) VALUES (?, ?, ?, ?)",
        invoices,
    )

    # ── Tickets ──────────────────────────────────────────────────────────
    tickets = []
    for cid in client_ids:
        num_tickets = random.randint(5, 50)
        for _ in range(num_tickets):
            hours = round(random.uniform(0.5, 20), 1)
            billable = random.choice([0, 1])
            rate = round(random.uniform(75, 250), 2)
            tickets.append((cid, hours, billable, rate))

    conn.executemany(
        "INSERT INTO tickets (client_id, time_spent, billable_hours, hourly_rate) VALUES (?, ?, ?, ?)",
        tickets,
    )

    # ── Client Services ──────────────────────────────────────────────────
    client_services = []
    for cid in client_ids:
        num_services = random.randint(1, 6)
        assigned = set()
        for _ in range(num_services):
            sid = random.randint(1, 10)
            if sid in assigned:
                continue
            assigned.add(sid)
            price = round(random.uniform(500, 25000), 2)
            qty = random.randint(1, 10)
            client_services.append((cid, sid, price, qty))

    conn.executemany(
        "INSERT INTO client_services (client_id, service_id, custom_price, quantity) VALUES (?, ?, ?, ?)",
        client_services,
    )

    logger.info(
        "Synthetic data: 100 clients, %d invoices, %d tickets, %d client-service links",
        len(invoices), len(tickets), len(client_services),
    )


def rename_models_to_predictor_format(output_dir: Path):
    """The pipeline saves xgboost_model.pkl / random_forest_model.pkl
    but the predictor looks for profitability_xgboost_model.pkl /
    profitability_random_forest_model.pkl."""
    for stem in ("xgboost", "random_forest"):
        old = output_dir / f"{stem}_model.pkl"
        new = output_dir / f"profitability_{stem}_model.pkl"
        if old.exists():
            shutil.move(str(old), str(new))
            logger.info("Renamed %s -> %s", old.name, new.name)


def main():
    logger.info("=" * 60)
    logger.info("Profitability Predictor – Training Script")
    logger.info("=" * 60)

    # Step 1 – ensure DB with synthetic data
    ensure_database()

    # Step 2 – run the complete training pipeline
    from src.models.profitability_predictor.training_pipeline import ProfitabilityTrainingPipeline

    pipeline = ProfitabilityTrainingPipeline(db_path=str(DB_PATH))
    results = pipeline.run_complete_pipeline(
        save_models=True,
        output_dir=str(OUTPUT_DIR),
    )

    # Step 3 – rename saved models so the predictor can find them
    rename_models_to_predictor_format(OUTPUT_DIR)

    # Step 4 – summary
    saved = results.get("saved_models", {})
    final_eval = results.get("final_evaluation", {})

    print()
    logger.info("=" * 60)
    logger.info("TRAINING COMPLETE")
    logger.info("=" * 60)
    logger.info("Data split:  train=%d  val=%d  test=%d",
                results["data_preparation"]["train_samples"],
                results["data_preparation"]["validation_samples"],
                results["data_preparation"]["test_samples"])
    logger.info("Best model:  %s", results["model_training"].get("best_model", "N/A"))

    for name in ("xgboost", "random_forest"):
        if name in final_eval:
            m = final_eval[name]["metrics"]
            logger.info("  %-14s  R²=%.4f  MAE=%.4f  RMSE=%.4f",
                        name.upper(), m["r2"], m["mae"], m["mae"])

    logger.info("Models saved to: %s", OUTPUT_DIR)
    logger.info("  xgboost  -> profitability_xgboost_model.pkl")
    logger.info("  rf       -> profitability_random_forest_model.pkl")
    print()

    return results


if __name__ == "__main__":
    main()
