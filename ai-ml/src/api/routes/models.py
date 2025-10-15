"""
Model Management Routes
Model registry, versioning, deployment, and management endpoints
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import BaseModel, Field

from ..dependencies import get_model_registry

logger = logging.getLogger(__name__)
router = APIRouter()


class ModelInfo(BaseModel):
    """Model information model"""
    name: str
    version: str
    status: str
    created_at: datetime
    updated_at: datetime
    performance: Dict[str, float]
    metadata: Dict[str, Any]


class ModelVersion(BaseModel):
    """Model version information"""
    version: str
    status: str
    created_at: datetime
    performance: Dict[str, float]
    metadata: Dict[str, Any]
    is_active: bool


class ModelDeployment(BaseModel):
    """Model deployment configuration"""
    model_name: str
    version: str
    environment: str = "production"
    replicas: int = 1
    resources: Dict[str, Any] = Field(default_factory=dict)
    config: Dict[str, Any] = Field(default_factory=dict)


class ModelDeploymentResponse(BaseModel):
    """Model deployment response"""
    deployment_id: str
    model_name: str
    version: str
    status: str
    created_at: datetime
    endpoints: List[str]


@router.get("/", response_model=List[ModelInfo])
async def list_models(
    status: Optional[str] = Query(None, description="Filter by model status"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of models to return"),
    offset: int = Query(0, ge=0, description="Number of models to skip")
):
    """List all available models"""
    try:
        model_registry = get_model_registry()
        models = await model_registry.list_models(status=status, limit=limit, offset=offset)
        
        return models
        
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(status_code=500, detail="Failed to list models")


@router.get("/{model_name}", response_model=ModelInfo)
async def get_model(
    model_name: str = Path(..., description="Name of the model")
):
    """Get detailed information about a specific model"""
    try:
        model_registry = get_model_registry()
        model_info = await model_registry.get_model(model_name)
        
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")
        
        return model_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get model {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model")


@router.get("/{model_name}/versions", response_model=List[ModelVersion])
async def list_model_versions(
    model_name: str = Path(..., description="Name of the model"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of versions to return")
):
    """List all versions of a specific model"""
    try:
        model_registry = get_model_registry()
        versions = await model_registry.list_model_versions(model_name, limit=limit)
        
        return versions
        
    except Exception as e:
        logger.error(f"Failed to list versions for model {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to list model versions")


@router.get("/{model_name}/versions/{version}", response_model=ModelVersion)
async def get_model_version(
    model_name: str = Path(..., description="Name of the model"),
    version: str = Path(..., description="Version of the model")
):
    """Get information about a specific model version"""
    try:
        model_registry = get_model_registry()
        version_info = await model_registry.get_model_version(model_name, version)
        
        if not version_info:
            raise HTTPException(status_code=404, detail="Model version not found")
        
        return version_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get model version {model_name}:{version}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model version")


@router.post("/{model_name}/versions/{version}/deploy", response_model=ModelDeploymentResponse)
async def deploy_model(
    model_name: str = Path(..., description="Name of the model"),
    version: str = Path(..., description="Version of the model"),
    deployment_config: ModelDeployment = None
):
    """Deploy a specific model version"""
    try:
        model_registry = get_model_registry()
        
        # Use provided config or create default
        if not deployment_config:
            deployment_config = ModelDeployment(
                model_name=model_name,
                version=version
            )
        
        deployment = await model_registry.deploy_model(
            model_name=model_name,
            version=version,
            config=deployment_config.dict()
        )
        
        return ModelDeploymentResponse(**deployment)
        
    except Exception as e:
        logger.error(f"Failed to deploy model {model_name}:{version}: {e}")
        raise HTTPException(status_code=500, detail="Failed to deploy model")


@router.delete("/{model_name}/versions/{version}/deploy")
async def undeploy_model(
    model_name: str = Path(..., description="Name of the model"),
    version: str = Path(..., description="Version of the model")
):
    """Undeploy a specific model version"""
    try:
        model_registry = get_model_registry()
        success = await model_registry.undeploy_model(model_name, version)
        
        if not success:
            raise HTTPException(status_code=404, detail="Model deployment not found")
        
        return {"message": "Model undeployed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to undeploy model {model_name}:{version}: {e}")
        raise HTTPException(status_code=500, detail="Failed to undeploy model")


@router.post("/{model_name}/versions/{version}/rollback")
async def rollback_model(
    model_name: str = Path(..., description="Name of the model"),
    version: str = Path(..., description="Version to rollback to")
):
    """Rollback model to a specific version"""
    try:
        model_registry = get_model_registry()
        success = await model_registry.rollback_model(model_name, version)
        
        if not success:
            raise HTTPException(status_code=404, detail="Model or version not found")
        
        return {"message": f"Model {model_name} rolled back to version {version}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to rollback model {model_name} to {version}: {e}")
        raise HTTPException(status_code=500, detail="Failed to rollback model")


@router.get("/{model_name}/performance", response_model=Dict[str, Any])
async def get_model_performance(
    model_name: str = Path(..., description="Name of the model"),
    days: int = Query(7, ge=1, le=365, description="Number of days to look back")
):
    """Get model performance metrics"""
    try:
        model_registry = get_model_registry()
        performance = await model_registry.get_model_performance(model_name, days=days)
        
        return performance
        
    except Exception as e:
        logger.error(f"Failed to get performance for model {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model performance")


@router.post("/{model_name}/retrain")
async def retrain_model(
    model_name: str = Path(..., description="Name of the model"),
    config: Dict[str, Any] = None
):
    """Trigger model retraining"""
    try:
        model_registry = get_model_registry()
        job_id = await model_registry.retrain_model(model_name, config or {})
        
        return {"message": "Model retraining started", "job_id": job_id}
        
    except Exception as e:
        logger.error(f"Failed to retrain model {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrain model")
