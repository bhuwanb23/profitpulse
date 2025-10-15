"""
Admin Service
Administrative functions, A/B testing, and system management
"""

import logging
import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json

logger = logging.getLogger(__name__)


class AdminService:
    """Service for administrative functions and system management"""
    
    def __init__(self):
        self.ab_tests: Dict[str, Dict[str, Any]] = {}
        self.retrain_jobs: Dict[str, Dict[str, Any]] = {}
        self.system_config: Dict[str, Any] = {}
        self._initialized = False
    
    async def initialize(self):
        """Initialize admin service"""
        try:
            # Load default system configuration
            await self._load_default_config()
            self._initialized = True
            logger.info("Admin service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize admin service: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup admin service"""
        logger.info("Admin service cleaned up")
    
    async def _load_default_config(self):
        """Load default system configuration"""
        try:
            self.system_config = {
                "max_concurrent_predictions": 100,
                "prediction_timeout_seconds": 30,
                "model_cache_size": 10,
                "auto_retrain_enabled": True,
                "retrain_threshold": 0.05,
                "monitoring_enabled": True,
                "alerting_enabled": True,
                "maintenance_mode": False,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            
            logger.info("Default system configuration loaded")
            
        except Exception as e:
            logger.error(f"Failed to load default configuration: {e}")
    
    async def get_system_config(self) -> Dict[str, Any]:
        """Get current system configuration"""
        try:
            return self.system_config.copy()
        except Exception as e:
            logger.error(f"Failed to get system config: {e}")
            return {}
    
    async def update_system_config(self, config: Dict[str, Any]) -> bool:
        """Update system configuration"""
        try:
            # Validate configuration
            if not self._validate_config(config):
                return False
            
            # Update configuration
            self.system_config.update(config)
            self.system_config["updated_at"] = datetime.now()
            
            logger.info("System configuration updated")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update system config: {e}")
            return False
    
    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate system configuration"""
        try:
            # Validate numeric values
            if "max_concurrent_predictions" in config:
                if not isinstance(config["max_concurrent_predictions"], int) or config["max_concurrent_predictions"] <= 0:
                    return False
            
            if "prediction_timeout_seconds" in config:
                if not isinstance(config["prediction_timeout_seconds"], int) or config["prediction_timeout_seconds"] <= 0:
                    return False
            
            if "model_cache_size" in config:
                if not isinstance(config["model_cache_size"], int) or config["model_cache_size"] <= 0:
                    return False
            
            if "retrain_threshold" in config:
                if not isinstance(config["retrain_threshold"], (int, float)) or not 0 <= config["retrain_threshold"] <= 1:
                    return False
            
            # Validate boolean values
            boolean_fields = ["auto_retrain_enabled", "monitoring_enabled", "alerting_enabled", "maintenance_mode"]
            for field in boolean_fields:
                if field in config and not isinstance(config[field], bool):
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    async def list_ab_tests(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """List A/B tests"""
        try:
            tests = list(self.ab_tests.values())
            
            # Apply filters
            if status:
                tests = [test for test in tests if test.get("status") == status]
            
            return tests[:limit]
            
        except Exception as e:
            logger.error(f"Failed to list A/B tests: {e}")
            return []
    
    async def create_ab_test(self, test_config: Dict[str, Any]) -> str:
        """Create a new A/B test"""
        try:
            test_id = str(uuid.uuid4())
            
            ab_test = {
                "test_id": test_id,
                "test_name": test_config["test_name"],
                "model_a": test_config["model_a"],
                "model_b": test_config["model_b"],
                "traffic_split": test_config.get("traffic_split", 0.5),
                "success_metric": test_config.get("success_metric", "accuracy"),
                "minimum_sample_size": test_config.get("minimum_sample_size", 1000),
                "max_duration_days": test_config.get("max_duration_days", 30),
                "enabled": test_config.get("enabled", True),
                "status": "running",
                "created_at": datetime.now(),
                "started_at": datetime.now(),
                "model_a_performance": {},
                "model_b_performance": {},
                "statistical_significance": 0.0,
                "winner": None,
                "confidence_level": 0.0,
                "sample_size": 0
            }
            
            self.ab_tests[test_id] = ab_test
            
            # Start A/B test simulation
            asyncio.create_task(self._simulate_ab_test(test_id))
            
            logger.info(f"A/B test created: {test_id}")
            return test_id
            
        except Exception as e:
            logger.error(f"Failed to create A/B test: {e}")
            raise
    
    async def get_ab_test(self, test_id: str) -> Optional[Dict[str, Any]]:
        """Get A/B test details"""
        try:
            return self.ab_tests.get(test_id)
        except Exception as e:
            logger.error(f"Failed to get A/B test {test_id}: {e}")
            return None
    
    async def stop_ab_test(self, test_id: str) -> bool:
        """Stop an A/B test"""
        try:
            if test_id not in self.ab_tests:
                return False
            
            self.ab_tests[test_id]["status"] = "stopped"
            self.ab_tests[test_id]["ended_at"] = datetime.now()
            
            logger.info(f"A/B test stopped: {test_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop A/B test {test_id}: {e}")
            return False
    
    async def _simulate_ab_test(self, test_id: str):
        """Simulate A/B test execution"""
        try:
            test = self.ab_tests[test_id]
            
            # Simulate test running for a few seconds
            await asyncio.sleep(5)
            
            # Generate mock results
            test["model_a_performance"] = {
                "accuracy": 0.85,
                "precision": 0.82,
                "recall": 0.88,
                "f1_score": 0.85,
                "latency_ms": 45.2,
                "sample_size": 500
            }
            
            test["model_b_performance"] = {
                "accuracy": 0.87,
                "precision": 0.84,
                "recall": 0.89,
                "f1_score": 0.86,
                "latency_ms": 42.1,
                "sample_size": 500
            }
            
            test["statistical_significance"] = 0.95
            test["confidence_level"] = 0.95
            test["sample_size"] = 1000
            test["winner"] = "model_b"
            test["status"] = "completed"
            test["ended_at"] = datetime.now()
            
            logger.info(f"A/B test {test_id} completed")
            
        except Exception as e:
            logger.error(f"A/B test simulation failed for {test_id}: {e}")
    
    async def list_retrain_jobs(self, model_name: Optional[str] = None,
                               status: Optional[str] = None,
                               limit: int = 50) -> List[Dict[str, Any]]:
        """List model retraining jobs"""
        try:
            jobs = list(self.retrain_jobs.values())
            
            # Apply filters
            if model_name:
                jobs = [job for job in jobs if job.get("model_name") == model_name]
            if status:
                jobs = [job for job in jobs if job.get("status") == status]
            
            return jobs[:limit]
            
        except Exception as e:
            logger.error(f"Failed to list retrain jobs: {e}")
            return []
    
    async def get_retrain_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get retraining job details"""
        try:
            return self.retrain_jobs.get(job_id)
        except Exception as e:
            logger.error(f"Failed to get retrain job {job_id}: {e}")
            return None
    
    async def cancel_retrain_job(self, job_id: str) -> bool:
        """Cancel a retraining job"""
        try:
            if job_id not in self.retrain_jobs:
                return False
            
            self.retrain_jobs[job_id]["status"] = "cancelled"
            self.retrain_jobs[job_id]["completed_at"] = datetime.now()
            
            logger.info(f"Retrain job cancelled: {job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cancel retrain job {job_id}: {e}")
            return False
    
    async def explain_prediction(self, model_name: str, version: str, 
                                prediction_id: str) -> Optional[Dict[str, Any]]:
        """Get model prediction explanation"""
        try:
            # Generate mock explanation
            explanation = {
                "prediction_id": prediction_id,
                "model_name": model_name,
                "version": version,
                "explanation": {
                    "feature_importance": {
                        "contract_value": 0.35,
                        "hours_logged": 0.28,
                        "billing_amount": 0.22,
                        "ticket_count": 0.15
                    },
                    "shap_values": {
                        "contract_value": 0.12,
                        "hours_logged": -0.08,
                        "billing_amount": 0.15,
                        "ticket_count": 0.05
                    },
                    "decision_path": [
                        "Contract value > $10,000",
                        "Hours logged < 50",
                        "Billing amount > $5,000"
                    ],
                    "confidence_factors": [
                        "High contract value increases profitability",
                        "Low hours logged improves efficiency",
                        "High billing amount indicates good revenue"
                    ]
                },
                "generated_at": datetime.now().isoformat()
            }
            
            return explanation
            
        except Exception as e:
            logger.error(f"Failed to explain prediction {prediction_id}: {e}")
            return None
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        try:
            status = {
                "overall_status": "healthy",
                "components": {
                    "api_server": "healthy",
                    "model_registry": "healthy",
                    "metrics_collector": "healthy",
                    "monitoring": "healthy",
                    "database": "healthy"
                },
                "metrics": {
                    "uptime_hours": 168.5,
                    "total_requests": 12500,
                    "error_rate": 0.02,
                    "avg_response_time_ms": 45.2,
                    "active_models": 4,
                    "active_alerts": 2
                },
                "last_updated": datetime.now().isoformat()
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {"overall_status": "error", "components": {}, "metrics": {}}
    
    async def start_maintenance_mode(self, duration_minutes: int) -> bool:
        """Start system maintenance mode"""
        try:
            self.system_config["maintenance_mode"] = True
            self.system_config["maintenance_until"] = datetime.now() + timedelta(minutes=duration_minutes)
            self.system_config["updated_at"] = datetime.now()
            
            logger.info(f"Maintenance mode started for {duration_minutes} minutes")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start maintenance mode: {e}")
            return False
    
    async def stop_maintenance_mode(self) -> bool:
        """Stop system maintenance mode"""
        try:
            self.system_config["maintenance_mode"] = False
            if "maintenance_until" in self.system_config:
                del self.system_config["maintenance_until"]
            self.system_config["updated_at"] = datetime.now()
            
            logger.info("Maintenance mode stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop maintenance mode: {e}")
            return False
