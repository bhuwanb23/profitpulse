"""
Model Registry
MLflow-based model registry for versioning and deployment management
"""

import logging
import mlflow
import mlflow.sklearn
import mlflow.tensorflow
import mlflow.xgboost
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

from config import settings

logger = logging.getLogger(__name__)


class ModelRegistry:
    """MLflow-based model registry for managing model versions and deployments"""
    
    def __init__(self):
        self.mlflow_client = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._initialized = False
    
    async def initialize(self):
        """Initialize the model registry"""
        try:
            # Set MLflow tracking URI
            mlflow.set_tracking_uri(settings.mlflow.tracking_uri)
            
            # Create MLflow client
            self.mlflow_client = mlflow.tracking.MlflowClient()
            
            # Set experiment
            experiment = mlflow.get_experiment_by_name(settings.mlflow.experiment_name)
            if not experiment:
                experiment_id = mlflow.create_experiment(settings.mlflow.experiment_name)
                logger.info(f"Created new experiment: {settings.mlflow.experiment_name}")
            else:
                experiment_id = experiment.experiment_id
                logger.info(f"Using existing experiment: {settings.mlflow.experiment_name}")
            
            mlflow.set_experiment(settings.mlflow.experiment_name)
            
            self._initialized = True
            logger.info("Model registry initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize model registry: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.executor:
            self.executor.shutdown(wait=True)
        logger.info("Model registry cleaned up")
    
    async def list_models(self, status: Optional[str] = None, 
                         limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """List all registered models"""
        try:
            if not self._initialized:
                await self.initialize()
            
            # Get all registered models
            models = self.mlflow_client.search_registered_models()
            
            # Convert to our format
            model_list = []
            for model in models[offset:offset + limit]:
                model_info = {
                    "name": model.name,
                    "version": model.latest_versions[0].version if model.latest_versions else "unknown",
                    "status": model.latest_versions[0].status if model.latest_versions else "unknown",
                    "created_at": datetime.fromtimestamp(model.creation_timestamp / 1000),
                    "updated_at": datetime.fromtimestamp(model.last_updated_timestamp / 1000),
                    "performance": {},
                    "metadata": model.tags or {}
                }
                
                # Get performance metrics for latest version
                if model.latest_versions:
                    latest_version = model.latest_versions[0]
                    try:
                        run = self.mlflow_client.get_run(latest_version.run_id)
                        model_info["performance"] = run.data.metrics or {}
                    except Exception as e:
                        logger.warning(f"Failed to get metrics for model {model.name}: {e}")
                
                # Filter by status if specified
                if status and model_info["status"] != status:
                    continue
                
                model_list.append(model_info)
            
            return model_list
            
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    async def get_model(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific model"""
        try:
            if not self._initialized:
                await self.initialize()
            
            # Get model details
            model = self.mlflow_client.get_registered_model(model_name)
            
            # Get latest version
            latest_version = model.latest_versions[0] if model.latest_versions else None
            
            if not latest_version:
                return None
            
            # Get performance metrics
            performance = {}
            try:
                run = self.mlflow_client.get_run(latest_version.run_id)
                performance = run.data.metrics or {}
            except Exception as e:
                logger.warning(f"Failed to get metrics for model {model_name}: {e}")
            
            return {
                "name": model.name,
                "version": latest_version.version,
                "status": latest_version.status,
                "created_at": datetime.fromtimestamp(model.creation_timestamp / 1000),
                "updated_at": datetime.fromtimestamp(model.last_updated_timestamp / 1000),
                "performance": performance,
                "metadata": model.tags or {}
            }
            
        except Exception as e:
            logger.error(f"Failed to get model {model_name}: {e}")
            return None
    
    async def list_model_versions(self, model_name: str, limit: int = 50) -> List[Dict[str, Any]]:
        """List all versions of a specific model"""
        try:
            if not self._initialized:
                await self.initialize()
            
            # Get model versions
            versions = self.mlflow_client.search_model_versions(f"name='{model_name}'")
            
            version_list = []
            for version in versions[:limit]:
                # Get performance metrics
                performance = {}
                try:
                    run = self.mlflow_client.get_run(version.run_id)
                    performance = run.data.metrics or {}
                except Exception as e:
                    logger.warning(f"Failed to get metrics for version {version.version}: {e}")
                
                version_info = {
                    "version": version.version,
                    "status": version.status,
                    "created_at": datetime.fromtimestamp(version.creation_timestamp / 1000),
                    "performance": performance,
                    "metadata": version.tags or {},
                    "is_active": version.status == "Production"
                }
                
                version_list.append(version_info)
            
            return version_list
            
        except Exception as e:
            logger.error(f"Failed to list versions for model {model_name}: {e}")
            return []
    
    async def get_model_version(self, model_name: str, version: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model version"""
        try:
            if not self._initialized:
                await self.initialize()
            
            # Get version details
            model_version = self.mlflow_client.get_model_version(model_name, version)
            
            # Get performance metrics
            performance = {}
            try:
                run = self.mlflow_client.get_run(model_version.run_id)
                performance = run.data.metrics or {}
            except Exception as e:
                logger.warning(f"Failed to get metrics for version {version}: {e}")
            
            return {
                "version": model_version.version,
                "status": model_version.status,
                "created_at": datetime.fromtimestamp(model_version.creation_timestamp / 1000),
                "performance": performance,
                "metadata": model_version.tags or {},
                "is_active": model_version.status == "Production"
            }
            
        except Exception as e:
            logger.error(f"Failed to get model version {model_name}:{version}: {e}")
            return None
    
    async def deploy_model(self, model_name: str, version: str, 
                          config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy a model version"""
        try:
            if not self._initialized:
                await self.initialize()
            
            # Transition model version to Production
            self.mlflow_client.transition_model_version_stage(
                name=model_name,
                version=version,
                stage="Production"
            )
            
            # Create deployment record
            deployment_id = f"{model_name}_{version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            deployment = {
                "deployment_id": deployment_id,
                "model_name": model_name,
                "version": version,
                "status": "deployed",
                "created_at": datetime.now(),
                "endpoints": [f"/api/predictions/{model_name}"]
            }
            
            logger.info(f"Model {model_name}:{version} deployed successfully")
            return deployment
            
        except Exception as e:
            logger.error(f"Failed to deploy model {model_name}:{version}: {e}")
            raise
    
    async def undeploy_model(self, model_name: str, version: str) -> bool:
        """Undeploy a model version"""
        try:
            if not self._initialized:
                await self.initialize()
            
            # Transition model version to Archived
            self.mlflow_client.transition_model_version_stage(
                name=model_name,
                version=version,
                stage="Archived"
            )
            
            logger.info(f"Model {model_name}:{version} undeployed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to undeploy model {model_name}:{version}: {e}")
            return False
    
    async def rollback_model(self, model_name: str, version: str) -> bool:
        """Rollback model to a specific version"""
        try:
            if not self._initialized:
                await self.initialize()
            
            # Get current production version
            current_prod = self.mlflow_client.get_latest_versions(
                model_name, stages=["Production"]
            )
            
            # Archive current production version
            for prod_version in current_prod:
                self.mlflow_client.transition_model_version_stage(
                    name=model_name,
                    version=prod_version.version,
                    stage="Archived"
                )
            
            # Promote target version to Production
            self.mlflow_client.transition_model_version_stage(
                name=model_name,
                version=version,
                stage="Production"
            )
            
            logger.info(f"Model {model_name} rolled back to version {version}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to rollback model {model_name} to {version}: {e}")
            return False
    
    async def get_model_performance(self, model_name: str, days: int = 7) -> Dict[str, Any]:
        """Get model performance metrics"""
        try:
            if not self._initialized:
                await self.initialize()
            
            # Get production version
            prod_versions = self.mlflow_client.get_latest_versions(
                model_name, stages=["Production"]
            )
            
            if not prod_versions:
                return {}
            
            # Get run metrics
            run = self.mlflow_client.get_run(prod_versions[0].run_id)
            metrics = run.data.metrics or {}
            
            # Add mock performance data for demonstration
            performance = {
                "accuracy": metrics.get("accuracy", 0.85),
                "precision": metrics.get("precision", 0.82),
                "recall": metrics.get("recall", 0.88),
                "f1_score": metrics.get("f1_score", 0.85),
                "auc_roc": metrics.get("auc_roc", 0.90),
                "prediction_latency_ms": metrics.get("prediction_latency_ms", 45.2),
                "throughput_per_second": metrics.get("throughput_per_second", 120.5),
                "error_rate": metrics.get("error_rate", 0.02),
                "last_updated": datetime.now().isoformat()
            }
            
            return performance
            
        except Exception as e:
            logger.error(f"Failed to get performance for model {model_name}: {e}")
            return {}
    
    async def retrain_model(self, model_name: str, config: Dict[str, Any]) -> str:
        """Trigger model retraining"""
        try:
            # Generate job ID
            job_id = f"retrain_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # In a real implementation, this would trigger a background job
            logger.info(f"Model retraining job {job_id} started for {model_name}")
            
            # Simulate async retraining
            asyncio.create_task(self._simulate_retraining(job_id, model_name, config))
            
            return job_id
            
        except Exception as e:
            logger.error(f"Failed to start retraining for model {model_name}: {e}")
            raise
    
    async def _simulate_retraining(self, job_id: str, model_name: str, config: Dict[str, Any]):
        """Simulate model retraining process"""
        try:
            logger.info(f"Retraining job {job_id} in progress...")
            
            # Simulate retraining time
            await asyncio.sleep(30)  # 30 seconds simulation
            
            # Create new model version
            with mlflow.start_run():
                # Log mock metrics
                mlflow.log_metric("accuracy", 0.87)
                mlflow.log_metric("precision", 0.84)
                mlflow.log_metric("recall", 0.89)
                mlflow.log_metric("f1_score", 0.86)
                
                # Log model
                mlflow.sklearn.log_model(
                    sk_model=None,  # Would be actual model in real implementation
                    artifact_path="model",
                    registered_model_name=model_name
                )
            
            logger.info(f"Retraining job {job_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Retraining job {job_id} failed: {e}")
