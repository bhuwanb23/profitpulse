import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
import pandas as pd
from datetime import datetime, timedelta


class TestPreprocessingSubmodules:
    def test_all_submodules_importable(self):
        from src.data.preprocessing import cleaning, imputation, outlier_detection
        from src.data.preprocessing import standardization, normalization
        from src.data.preprocessing import feature_engineering, aggregation, validation
        assert cleaning is not None

    def test_cleaning_clean_dataframe(self):
        from src.data.preprocessing import cleaning
        df = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, None]})
        result = cleaning.clean_dataframe(df)
        assert isinstance(result, pd.DataFrame)

    def test_imputation(self):
        from src.data.preprocessing import imputation
        df = pd.DataFrame({"value": [1.0, None, 3.0]})
        result = imputation.impute_missing_values(df, {})
        assert result["value"].isnull().sum() == 0

    def test_outlier_detection(self):
        from src.data.preprocessing import outlier_detection
        df = pd.DataFrame({"value": [1.0, 2.0, 1.5, 100.0, 2.5]})
        cleaned, outliers = outlier_detection.remove_outliers(df, {"zscore_cols": ["value"], "zscore_threshold": 1.5})
        assert len(cleaned) < len(df)
        assert len(outliers) > 0

    def test_standardization(self):
        from src.data.preprocessing import standardization
        df = pd.DataFrame({"name": ["  Alice  ", "BOB  "], "amount": [100.555, 200.777]})
        result = standardization.standardize_data(df, {"text_columns": ["name"], "currency_columns": ["amount"]})
        assert result["name"].iloc[0] == "alice"
        assert result["amount"].iloc[0] == 100.56

    def test_normalization(self):
        from src.data.preprocessing import normalization
        df = pd.DataFrame({"value": [10.0, 20.0, 30.0]})
        result = normalization.normalize_data(df, {"standard_cols": ["value"]})
        assert abs(result["value"].mean()) < 1e-10
        assert abs(result["value"].std() - 1.0) < 0.5

    def test_feature_engineering(self):
        from src.data.preprocessing import feature_engineering
        df = pd.DataFrame({
            "billing_amount": [100.0, 200.0],
            "hours_logged": [10.0, 20.0],
            "created_at": [datetime.now().isoformat(), (datetime.now() - timedelta(days=5)).isoformat()],
            "contract_value": [10000.0, 50000.0]
        })
        result = feature_engineering.engineer_features(df, {})
        assert "revenue_per_hour" in result.columns
        assert "ticket_age_days" in result.columns
        assert "client_value_tier" in result.columns

    def test_validation(self):
        from src.data.preprocessing import validation
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        result = validation.validate_data(df, {"schema": {"a": "int", "b": "int"}, "ranges": {"a": {"min": 0}}})
        assert result["is_valid"] is True

    def test_validation_fails_on_missing_column(self):
        from src.data.preprocessing import validation
        df = pd.DataFrame({"a": [1]})
        result = validation.validate_data(df, {"schema": {"a": "int", "b": "int"}})
        assert result["is_valid"] is False

    def test_pipeline_convenience_function(self):
        from src.data.pipeline import preprocess_data
        df = pd.DataFrame({
            "id": ["t1", "t2"],
            "title": ["Fix bug", "Deploy"],
            "status": ["Open", "Closed"],
            "priority": ["High", "Low"],
            "created_at": [datetime.now().isoformat(), (datetime.now() - timedelta(days=1)).isoformat()],
            "hours_logged": [5.0, 2.0],
            "billing_amount": [300.0, 120.0]
        })
        result, validation = preprocess_data(df, "ticket")
        assert isinstance(result, pd.DataFrame)
        assert isinstance(validation, dict)


class TestDatabaseSQLInjection:
    def test_update_scheduled_run_filters_columns(self):
        from src.utils.database import DatabaseManager
        import tempfile, os
        fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        try:
            mgr = DatabaseManager(db_path)
            mgr.initialize_tables()
            run_id = mgr.create_scheduled_run({
                "model_name": "test_model",
                "schedule": "0 * * * *",
                "enabled": True,
                "parameters": "{}"
            })
            injected_data = {
                "model_name": "safe",
                "enabled; DROP TABLE scheduled_runs; --": "evil"
            }
            result = mgr.update_scheduled_run(run_id, injected_data)
            assert result is True
            runs = mgr.get_scheduled_runs()
            assert len(runs) == 1
            assert runs[0]["model_name"] == "safe"
        finally:
            try:
                Path(db_path).unlink(missing_ok=True)
            except PermissionError:
                pass

    def test_update_retraining_trigger_filters_columns(self):
        from src.utils.database import DatabaseManager
        import tempfile, os
        fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        try:
            mgr = DatabaseManager(db_path)
            mgr.initialize_tables()
            trigger_id = mgr.create_retraining_trigger({
                "model_name": "test",
                "trigger_type": "drift",
                "trigger_condition": "accuracy < 0.8",
                "enabled": True
            })
            injected = {"trigger_type": "performance", "evil_column": "drop"}
            result = mgr.update_retraining_trigger(trigger_id, injected)
            assert result is True
            triggers = mgr.get_retraining_triggers("test")
            assert triggers[0]["trigger_type"] == "performance"
        finally:
            try:
                Path(db_path).unlink(missing_ok=True)
            except PermissionError:
                pass

    def test_update_retraining_job_filters_columns(self):
        from src.utils.database import DatabaseManager
        import tempfile, os
        fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        try:
            mgr = DatabaseManager(db_path)
            mgr.initialize_tables()
            job_id = mgr.create_retraining_job({
                "model_name": "test",
                "triggered_by": "system",
                "trigger_type": "schedule",
                "parameters": "{}"
            })
            injected = {"status": "running", "DROP TABLE retraining_jobs": "evil"}
            result = mgr.update_retraining_job(job_id, injected)
            assert result is True
            job = mgr.get_retraining_job(job_id)
            assert job["status"] == "running"
        finally:
            try:
                Path(db_path).unlink(missing_ok=True)
            except PermissionError:
                pass


class TestAuthPackage:
    def test_auth_init_exists(self):
        import src.auth
        assert hasattr(src.auth, "TokenManager") or hasattr(src.auth, "QuickBooksOAuth")


class TestDBPathResolution:
    def test_churn_predictor_uses_default_path(self):
        from src.models.churn_predictor.churn_predictor import ChurnPredictor
        predictor = ChurnPredictor()
        assert "database" in predictor.db_path
        assert predictor.db_path.endswith("superhack.db")

    def test_revenue_leak_predictor_uses_default_path(self):
        from src.models.revenue_leak_detector.revenue_leak_predictor import RevenueLeakPredictor
        predictor = RevenueLeakPredictor()
        assert "database" in predictor.db_path
        assert predictor.db_path.endswith("superhack.db")

    def test_profitability_predictor_uses_default_path(self):
        from src.models.profitability_predictor.profitability_predictor import ProfitabilityPredictor
        predictor = ProfitabilityPredictor()
        assert "database" in predictor.db_path
        assert predictor.db_path.endswith("superhack.db")
