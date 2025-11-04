"""
Database utilities for the AI/ML system
Provides database operations for scheduled runs, performance metrics, and other features.
"""

import sqlite3
import logging
import asyncio
import aiosqlite
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database manager for AI/ML system"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.database.url.replace("sqlite:///", "")
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Ensure database file exists"""
        db_path = Path(self.db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create database file if it doesn't exist
        if not db_path.exists():
            db_path.touch()
            logger.info(f"Created database file: {self.db_path}")
    
    def initialize_tables(self):
        """Initialize all required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Create scheduled_runs table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS scheduled_runs (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        schedule TEXT NOT NULL,
                        enabled BOOLEAN DEFAULT TRUE,
                        parameters TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_run TIMESTAMP,
                        next_run TIMESTAMP
                    )
                """)
                
                # Create indexes for better performance
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_scheduled_runs_model_name 
                    ON scheduled_runs (model_name)
                """)
                
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_scheduled_runs_next_run 
                    ON scheduled_runs (next_run)
                """)
                
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_scheduled_runs_enabled 
                    ON scheduled_runs (enabled)
                """)
                
                # Create model_performance table for performance reporting
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS model_performance (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        model_version TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        accuracy REAL,
                        precision REAL,
                        recall REAL,
                        f1_score REAL,
                        rmse REAL,
                        mae REAL,
                        r_squared REAL,
                        prediction_count INTEGER,
                        error_count INTEGER,
                        average_prediction_time_ms REAL
                    )
                """)
                
                # Create indexes for model_performance
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_model_performance_model_name 
                    ON model_performance (model_name)
                """)
                
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_model_performance_timestamp 
                    ON model_performance (timestamp)
                """)
                
                # Create data_drift_reports table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS data_drift_reports (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        drift_score REAL,
                        drifted_features TEXT,
                        drift_detection_method TEXT,
                        severity TEXT,
                        report_data TEXT
                    )
                """)
                
                # Create concept_drift_reports table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS concept_drift_reports (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        drift_score REAL,
                        performance_degradation REAL,
                        drift_detection_method TEXT,
                        severity TEXT,
                        report_data TEXT
                    )
                """)
                
                # Create historical_predictions table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS historical_predictions (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        prediction REAL,
                        actual_value REAL,
                        confidence REAL,
                        features TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        client_id TEXT,
                        model_version TEXT,
                        prediction_time_ms REAL,
                        status TEXT DEFAULT 'completed'
                    )
                """)
                
                # Create indexes for historical_predictions
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_historical_predictions_model_name 
                    ON historical_predictions (model_name)
                """)
                
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_historical_predictions_timestamp 
                    ON historical_predictions (timestamp)
                """)
                
                # Create retraining_jobs table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS retraining_jobs (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        status TEXT DEFAULT 'pending',
                        triggered_by TEXT,
                        trigger_type TEXT,
                        parameters TEXT,
                        started_at TIMESTAMP,
                        completed_at TIMESTAMP,
                        error_message TEXT,
                        model_version_before TEXT,
                        model_version_after TEXT
                    )
                """)
                
                # Create retraining_triggers table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS retraining_triggers (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        trigger_type TEXT NOT NULL,
                        trigger_condition TEXT,
                        enabled BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("Database tables initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize database tables: {e}")
            raise
    
    # Scheduled Runs Methods
    def create_scheduled_run(self, run_data: Dict[str, Any]) -> str:
        """Create a new scheduled run"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                run_id = run_data.get("id", f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(run_data)) % 10000}")
                
                conn.execute("""
                    INSERT INTO scheduled_runs 
                    (id, model_name, schedule, enabled, parameters, created_at, updated_at, next_run)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    run_id,
                    run_data["model_name"],
                    run_data["schedule"],
                    run_data.get("enabled", True),
                    run_data.get("parameters", "{}"),
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    run_data.get("next_run")
                ))
                
                conn.commit()
                logger.info(f"Created scheduled run: {run_id}")
                return run_id
                
        except Exception as e:
            logger.error(f"Failed to create scheduled run: {e}")
            raise
    
    def get_scheduled_runs(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all scheduled runs"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM scheduled_runs
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                """, (limit, offset))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Failed to get scheduled runs: {e}")
            raise
    
    def get_scheduled_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific scheduled run"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM scheduled_runs WHERE id = ?
                """, (run_id,))
                
                row = cursor.fetchone()
                return dict(row) if row else None
                
        except Exception as e:
            logger.error(f"Failed to get scheduled run {run_id}: {e}")
            raise
    
    def update_scheduled_run(self, run_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a scheduled run"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Build dynamic update query
                set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
                values = list(update_data.values()) + [run_id]
                
                conn.execute(f"""
                    UPDATE scheduled_runs 
                    SET {set_clause}, updated_at = ?
                    WHERE id = ?
                """, values + [datetime.now().isoformat(), run_id])
                
                conn.commit()
                updated = conn.total_changes > 0
                if updated:
                    logger.info(f"Updated scheduled run: {run_id}")
                return updated
                
        except Exception as e:
            logger.error(f"Failed to update scheduled run {run_id}: {e}")
            raise
    
    def delete_scheduled_run(self, run_id: str) -> bool:
        """Delete a scheduled run"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    DELETE FROM scheduled_runs WHERE id = ?
                """, (run_id,))
                
                conn.commit()
                deleted = conn.total_changes > 0
                if deleted:
                    logger.info(f"Deleted scheduled run: {run_id}")
                return deleted
                
        except Exception as e:
            logger.error(f"Failed to delete scheduled run {run_id}: {e}")
            raise
    
    def get_due_scheduled_runs(self) -> List[Dict[str, Any]]:
        """Get all enabled scheduled runs that are due to run"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM scheduled_runs 
                    WHERE enabled = TRUE AND next_run <= ?
                    ORDER BY next_run ASC
                """, (datetime.now().isoformat(),))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Failed to get due scheduled runs: {e}")
            raise
    
    # Performance Metrics Methods
    def save_model_performance(self, performance_data: Dict[str, Any]) -> str:
        """Save model performance metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                perf_id = performance_data.get("id", f"perf_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(performance_data)) % 10000}")
                
                conn.execute("""
                    INSERT INTO model_performance 
                    (id, model_name, model_version, timestamp, accuracy, precision, recall, 
                     f1_score, rmse, mae, r_squared, prediction_count, error_count, average_prediction_time_ms)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    perf_id,
                    performance_data["model_name"],
                    performance_data.get("model_version"),
                    performance_data.get("timestamp", datetime.now().isoformat()),
                    performance_data.get("accuracy"),
                    performance_data.get("precision"),
                    performance_data.get("recall"),
                    performance_data.get("f1_score"),
                    performance_data.get("rmse"),
                    performance_data.get("mae"),
                    performance_data.get("r_squared"),
                    performance_data.get("prediction_count", 0),
                    performance_data.get("error_count", 0),
                    performance_data.get("average_prediction_time_ms", 0.0)
                ))
                
                conn.commit()
                logger.info(f"Saved model performance: {perf_id}")
                return perf_id
                
        except Exception as e:
            logger.error(f"Failed to save model performance: {e}")
            raise
    
    # Historical Predictions Methods
    def save_historical_prediction(self, prediction_data: Dict[str, Any]) -> str:
        """Save historical prediction data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                pred_id = prediction_data.get("id", f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(prediction_data)) % 10000}")
                
                conn.execute("""
                    INSERT INTO historical_predictions 
                    (id, model_name, prediction, actual_value, confidence, features, timestamp, 
                     client_id, model_version, prediction_time_ms, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pred_id,
                    prediction_data["model_name"],
                    prediction_data["prediction"],
                    prediction_data.get("actual_value"),
                    prediction_data.get("confidence"),
                    prediction_data.get("features", "{}"),
                    prediction_data.get("timestamp", datetime.now().isoformat()),
                    prediction_data.get("client_id"),
                    prediction_data.get("model_version"),
                    prediction_data.get("prediction_time_ms", 0.0),
                    prediction_data.get("status", "completed")
                ))
                
                conn.commit()
                logger.info(f"Saved historical prediction: {pred_id}")
                return pred_id
                
        except Exception as e:
            logger.error(f"Failed to save historical prediction: {e}")
            raise
    
    def get_historical_predictions(self, model_name: str, days: int = 30, limit: int = 1000) -> List[Dict[str, Any]]:
        """Get historical predictions for a model"""
        try:
            from datetime import datetime, timedelta
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM historical_predictions 
                    WHERE model_name = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (model_name, cutoff_date, limit))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Failed to get historical predictions for {model_name}: {e}")
            raise
    
    def get_prediction_statistics(self, model_name: str, days: int = 30) -> Dict[str, Any]:
        """Get prediction statistics for a model"""
        try:
            from datetime import datetime, timedelta
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT 
                        COUNT(*) as total_predictions,
                        AVG(confidence) as average_confidence,
                        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_predictions,
                        COUNT(CASE WHEN status = 'error' THEN 1 END) as error_predictions
                    FROM historical_predictions 
                    WHERE model_name = ? AND timestamp >= ?
                """, (model_name, cutoff_date))
                
                row = cursor.fetchone()
                if row:
                    stats = dict(row)
                    stats["error_rate"] = stats["error_predictions"] / max(stats["total_predictions"], 1)
                    return stats
                return {}
                
        except Exception as e:
            logger.error(f"Failed to get prediction statistics for {model_name}: {e}")
            raise
    
    def get_model_performance_reports(self, model_name: str, days: int = 30, limit: int = 100) -> List[Dict[str, Any]]:
        """Get model performance reports"""
        try:
            from datetime import datetime, timedelta
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM model_performance 
                    WHERE model_name = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (model_name, cutoff_date, limit))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Failed to get model performance reports for {model_name}: {e}")
            raise
    
    def create_retraining_trigger(self, trigger_data: Dict[str, Any]) -> str:
        """Create a new retraining trigger"""
        try:
            from datetime import datetime
            with sqlite3.connect(self.db_path) as conn:
                trigger_id = trigger_data.get("id", f"trigger_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(trigger_data)) % 10000}")
                
                conn.execute("""
                    INSERT INTO retraining_triggers 
                    (id, model_name, trigger_type, trigger_condition, enabled, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    trigger_id,
                    trigger_data["model_name"],
                    trigger_data["trigger_type"],
                    trigger_data.get("trigger_condition", "{}"),
                    trigger_data.get("enabled", True),
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
                
                conn.commit()
                logger.info(f"Created retraining trigger: {trigger_id}")
                return trigger_id
                
        except Exception as e:
            logger.error(f"Failed to create retraining trigger: {e}")
            raise
    
    def get_retraining_triggers(self, model_name: str) -> List[Dict[str, Any]]:
        """Get all retraining triggers for a model"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM retraining_triggers WHERE model_name = ?
                    ORDER BY created_at DESC
                """, (model_name,))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Failed to get retraining triggers for {model_name}: {e}")
            raise
    
    def update_retraining_trigger(self, trigger_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a retraining trigger"""
        try:
            from datetime import datetime
            with sqlite3.connect(self.db_path) as conn:
                # Build dynamic update query
                set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
                values = list(update_data.values()) + [trigger_id]
                
                conn.execute(f"""
                    UPDATE retraining_triggers 
                    SET {set_clause}, updated_at = ?
                    WHERE id = ?
                """, values + [datetime.now().isoformat(), trigger_id])
                
                conn.commit()
                updated = conn.total_changes > 0
                if updated:
                    logger.info(f"Updated retraining trigger: {trigger_id}")
                return updated
                
        except Exception as e:
            logger.error(f"Failed to update retraining trigger {trigger_id}: {e}")
            raise
    
    def delete_retraining_trigger(self, trigger_id: str) -> bool:
        """Delete a retraining trigger"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    DELETE FROM retraining_triggers WHERE id = ?
                """, (trigger_id,))
                
                conn.commit()
                deleted = conn.total_changes > 0
                if deleted:
                    logger.info(f"Deleted retraining trigger: {trigger_id}")
                return deleted
                
        except Exception as e:
            logger.error(f"Failed to delete retraining trigger {trigger_id}: {e}")
            raise
    
    def create_retraining_job(self, job_data: Dict[str, Any]) -> str:
        """Create a new retraining job"""
        try:
            from datetime import datetime
            with sqlite3.connect(self.db_path) as conn:
                job_id = job_data.get("id", f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(job_data)) % 10000}")
                
                conn.execute("""
                    INSERT INTO retraining_jobs 
                    (id, model_name, status, triggered_by, trigger_type, parameters, started_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    job_id,
                    job_data["model_name"],
                    job_data.get("status", "pending"),
                    job_data.get("triggered_by", "manual"),
                    job_data.get("trigger_type", "manual"),
                    job_data.get("parameters", "{}"),
                    datetime.now().isoformat()
                ))
                
                conn.commit()
                logger.info(f"Created retraining job: {job_id}")
                return job_id
                
        except Exception as e:
            logger.error(f"Failed to create retraining job: {e}")
            raise
    
    def update_retraining_job(self, job_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a retraining job"""
        try:
            from datetime import datetime
            with sqlite3.connect(self.db_path) as conn:
                # Build dynamic update query
                set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
                values = list(update_data.values()) + [job_id]
                
                conn.execute(f"""
                    UPDATE retraining_jobs 
                    SET {set_clause}
                    WHERE id = ?
                """, values + [job_id])
                
                conn.commit()
                updated = conn.total_changes > 0
                if updated:
                    logger.info(f"Updated retraining job: {job_id}")
                return updated
                
        except Exception as e:
            logger.error(f"Failed to update retraining job {job_id}: {e}")
            raise
    
    def get_retraining_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific retraining job"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM retraining_jobs WHERE id = ?
                """, (job_id,))
                
                row = cursor.fetchone()
                return dict(row) if row else None
                
        except Exception as e:
            logger.error(f"Failed to get retraining job {job_id}: {e}")
            raise
    
    def get_retraining_history(self, model_name: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get retraining history for a model"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM retraining_jobs 
                    WHERE model_name = ?
                    ORDER BY started_at DESC
                    LIMIT ?
                """, (model_name, limit))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Failed to get retraining history for {model_name}: {e}")
            raise


# Async version of DatabaseManager
class AsyncDatabaseManager:
    """Async database manager for AI/ML system"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.database.url.replace("sqlite:///", "")
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Ensure database file exists"""
        db_path = Path(self.db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create database file if it doesn't exist
        if not db_path.exists():
            db_path.touch()
            logger.info(f"Created database file: {self.db_path}")
    
    async def initialize_tables(self):
        """Initialize all required tables"""
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                # Create scheduled_runs table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS scheduled_runs (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        schedule TEXT NOT NULL,
                        enabled BOOLEAN DEFAULT TRUE,
                        parameters TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_run TIMESTAMP,
                        next_run TIMESTAMP
                    )
                """)
                
                # Create indexes for better performance
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_scheduled_runs_model_name 
                    ON scheduled_runs (model_name)
                """)
                
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_scheduled_runs_next_run 
                    ON scheduled_runs (next_run)
                """)
                
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_scheduled_runs_enabled 
                    ON scheduled_runs (enabled)
                """)
                
                # Create model_performance table for performance reporting
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS model_performance (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        model_version TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        accuracy REAL,
                        precision REAL,
                        recall REAL,
                        f1_score REAL,
                        rmse REAL,
                        mae REAL,
                        r_squared REAL,
                        prediction_count INTEGER,
                        error_count INTEGER,
                        average_prediction_time_ms REAL
                    )
                """)
                
                # Create indexes for model_performance
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_model_performance_model_name 
                    ON model_performance (model_name)
                """)
                
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_model_performance_timestamp 
                    ON model_performance (timestamp)
                """)
                
                # Create data_drift_reports table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS data_drift_reports (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        drift_score REAL,
                        drifted_features TEXT,
                        drift_detection_method TEXT,
                        severity TEXT,
                        report_data TEXT
                    )
                """)
                
                # Create concept_drift_reports table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS concept_drift_reports (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        drift_score REAL,
                        performance_degradation REAL,
                        drift_detection_method TEXT,
                        severity TEXT,
                        report_data TEXT
                    )
                """)
                
                # Create historical_predictions table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS historical_predictions (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        prediction REAL,
                        actual_value REAL,
                        confidence REAL,
                        features TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        client_id TEXT,
                        model_version TEXT,
                        prediction_time_ms REAL,
                        status TEXT DEFAULT 'completed'
                    )
                """)
                
                # Create indexes for historical_predictions
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_historical_predictions_model_name 
                    ON historical_predictions (model_name)
                """)
                
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_historical_predictions_timestamp 
                    ON historical_predictions (timestamp)
                """)
                
                # Create retraining_jobs table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS retraining_jobs (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        status TEXT DEFAULT 'pending',
                        triggered_by TEXT,
                        trigger_type TEXT,
                        parameters TEXT,
                        started_at TIMESTAMP,
                        completed_at TIMESTAMP,
                        error_message TEXT,
                        model_version_before TEXT,
                        model_version_after TEXT
                    )
                """)
                
                # Create retraining_triggers table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS retraining_triggers (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        trigger_type TEXT NOT NULL,
                        trigger_condition TEXT,
                        enabled BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                await conn.commit()
                logger.info("Database tables initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize database tables: {e}")
            raise


# Factory function
def create_database_manager() -> DatabaseManager:
    """Create database manager instance"""
    return DatabaseManager()


def create_async_database_manager() -> AsyncDatabaseManager:
    """Create async database manager instance"""
    return AsyncDatabaseManager()