"""
Simple Model Registry
Mock model registry for testing without MLflow dependency
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import asyncio

logger = logging.getLogger(__name__)


class SimpleModelRegistry:
    """Simple model registry for testing without MLflow dependency"""
    
    def __init__(self):
        self._initialized = False
        # Mock models data
        self._models = {
            "client_profitability": {
                "name": "client_profitability",
                "latest_version": "1.0.0",
                "status": "Production",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "performance": {
                    "accuracy": 0.85,
                    "precision": 0.82,
                    "recall": 0.88,
                    "f1_score": 0.85
                },
                "metadata": {"type": "regression", "framework": "xgboost"}
            },
            "client_churn": {
                "name": "client_churn",
                "latest_version": "1.0.0",
                "status": "Production",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "performance": {
                    "accuracy": 0.87,
                    "precision": 0.84,
                    "recall": 0.89,
                    "f1_score": 0.86
                },
                "metadata": {"type": "classification", "framework": "xgboost"}
            }
        }
    
    async def initialize(self):
        """Initialize the model registry"""
        self._initialized = True
        logger.info("Simple model registry initialized successfully")
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("Simple model registry cleaned up")
    
    async def list_models(self, status: Optional[str] = None, 
                         limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """List all registered models"""
        if not self._initialized:
            await self.initialize()
        
        model_list = []
        for model in list(self._models.values())[offset:offset + limit]:
            if status and model["status"] != status:
                continue
            model_list.append(model)
        
        return model_list
    
    async def get_model(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific model"""
        if not self._initialized:
            await self.initialize()
        
        return self._models.get(model_name)
    
    async def list_model_versions(self, model_name: str, limit: int = 50) -> List[Dict[str, Any]]:
        """List all versions of a specific model"""
        if not self._initialized:
            await self.initialize()
        
        model = self._models.get(model_name)
        if not model:
            return []
        
        return [{
            "version": model["latest_version"],
            "status": model["status"],
            "created_at": model["created_at"],
            "performance": model["performance"],
            "metadata": model["metadata"],
            "is_active": model["status"] == "Production"
        }]
    
    async def get_model_version(self, model_name: str, version: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model version"""
        if not self._initialized:
            await self.initialize()
        
        model = self._models.get(model_name)
        if not model or model["latest_version"] != version:
            return None
        
        return {
            "version": model["latest_version"],
            "status": model["status"],
            "created_at": model["created_at"],
            "performance": model["performance"],
            "metadata": model["metadata"],
            "is_active": model["status"] == "Production"
        }
    
    async def deploy_model(self, model_name: str, version: str, 
                          config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy a model version"""
        if not self._initialized:
            await self.initialize()
        
        model = self._models.get(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        
        model["status"] = "Production"
        model["updated_at"] = datetime.now()
        
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
    
    async def undeploy_model(self, model_name: str, version: str) -> bool:
        """Undeploy a model version"""
        if not self._initialized:
            await self.initialize()
        
        model = self._models.get(model_name)
        if not model or model["latest_version"] != version:
            return False
        
        model["status"] = "Archived"
        model["updated_at"] = datetime.now()
        
        logger.info(f"Model {model_name}:{version} undeployed successfully")
        return True
    
    async def rollback_model(self, model_name: str, version: str) -> bool:
        """Rollback model to a specific version"""
        if not self._initialized:
            await self.initialize()
        
        model = self._models.get(model_name)
        if not model or model["latest_version"] != version:
            return False
        
        model["status"] = "Production"
        model["updated_at"] = datetime.now()
        
        logger.info(f"Model {model_name} rolled back to version {version}")
        return True
    
    async def get_model_performance(self, model_name: str, days: int = 7) -> Dict[str, Any]:
        """Get model performance metrics"""
        if not self._initialized:
            await self.initialize()
        
        model = self._models.get(model_name)
        if not model:
            return {}
        
        return model["performance"]
    
    async def retrain_model(self, model_name: str, config: Dict[str, Any]) -> str:
        """Trigger model retraining"""
        if not self._initialized:
            await self.initialize()
        
        job_id = f"retrain_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"Model retraining job {job_id} started for {model_name}")
        asyncio.create_task(self._simulate_retraining(job_id, model_name, config))
        return job_id
    
    async def _simulate_retraining(self, job_id: str, model_name: str, config: Dict[str, Any]):
        """Simulate model retraining process"""
        try:
            logger.info(f"Retraining job {job_id} in progress...")
            await asyncio.sleep(5)  # 5 seconds simulation
            logger.info(f"Retraining job {job_id} completed successfully")
        except Exception as e:
            logger.error(f"Retraining job {job_id} failed: {e}")