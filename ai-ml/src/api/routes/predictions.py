"""
Prediction Routes
Model inference and prediction endpoints
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import BaseModel, Field

from ..dependencies import get_model_registry, get_metrics_collector
from ...utils.predictor import Predictor

logger = logging.getLogger(__name__)
router = APIRouter()


class PredictionRequest(BaseModel):
    """Base prediction request model"""
    data: Dict[str, Any] = Field(..., description="Input data for prediction")
    model_version: Optional[str] = Field(None, description="Specific model version to use")
    return_probabilities: bool = Field(False, description="Whether to return prediction probabilities")
    return_confidence: bool = Field(False, description="Whether to return confidence scores")


class PredictionResponse(BaseModel):
    """Base prediction response model"""
    prediction: Union[float, int, str, List[Any]]
    model_name: str
    model_version: str
    prediction_id: str
    timestamp: datetime
    processing_time_ms: float
    confidence: Optional[float] = None
    probabilities: Optional[Dict[str, float]] = None


class BatchPredictionRequest(BaseModel):
    """Batch prediction request model"""
    data: List[Dict[str, Any]] = Field(..., description="List of input data for predictions")
    model_version: Optional[str] = Field(None, description="Specific model version to use")
    return_probabilities: bool = Field(False, description="Whether to return prediction probabilities")
    return_confidence: bool = Field(False, description="Whether to return confidence scores")


class BatchPredictionResponse(BaseModel):
    """Batch prediction response model"""
    predictions: List[PredictionResponse]
    total_predictions: int
    processing_time_ms: float
    model_name: str
    model_version: str


class ProfitabilityPredictionRequest(BaseModel):
    """Client profitability prediction request"""
    client_id: str
    contract_value: float
    hours_logged: float
    billing_amount: float
    ticket_count: int
    satisfaction_score: Optional[float] = None
    last_contact_days: Optional[int] = None
    service_types: Optional[List[str]] = None


class ChurnPredictionRequest(BaseModel):
    """Client churn prediction request"""
    client_id: str
    contract_value: float
    last_contact_days: int
    ticket_frequency: float
    satisfaction_score: Optional[float] = None
    payment_delays: int = 0
    service_issues: int = 0


class RevenueLeakDetectionRequest(BaseModel):
    """Revenue leak detection request"""
    invoice_data: Dict[str, Any]
    ticket_data: Dict[str, Any]
    time_period_days: int = 30


@router.post("/profitability", response_model=PredictionResponse)
async def predict_profitability(
    request: ProfitabilityPredictionRequest,
    model_version: Optional[str] = Query(None, description="Specific model version to use")
):
    """Predict client profitability"""
    try:
        predictor = Predictor()
        
        # Convert request to prediction format
        prediction_data = {
            "client_id": request.client_id,
            "contract_value": request.contract_value,
            "hours_logged": request.hours_logged,
            "billing_amount": request.billing_amount,
            "ticket_count": request.ticket_count,
            "satisfaction_score": request.satisfaction_score or 0.0,
            "last_contact_days": request.last_contact_days or 0,
            "service_types": request.service_types or []
        }
        
        prediction = await predictor.predict(
            model_name="client_profitability",
            data=prediction_data,
            model_version=model_version,
            return_confidence=True
        )
        
        return prediction
        
    except Exception as e:
        logger.error(f"Profitability prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to predict profitability")


@router.post("/churn", response_model=PredictionResponse)
async def predict_churn(
    request: ChurnPredictionRequest,
    model_version: Optional[str] = Query(None, description="Specific model version to use")
):
    """Predict client churn risk"""
    try:
        predictor = Predictor()
        
        # Convert request to prediction format
        prediction_data = {
            "client_id": request.client_id,
            "contract_value": request.contract_value,
            "last_contact_days": request.last_contact_days,
            "ticket_frequency": request.ticket_frequency,
            "satisfaction_score": request.satisfaction_score or 0.0,
            "payment_delays": request.payment_delays,
            "service_issues": request.service_issues
        }
        
        prediction = await predictor.predict(
            model_name="client_churn",
            data=prediction_data,
            model_version=model_version,
            return_probabilities=True,
            return_confidence=True
        )
        
        return prediction
        
    except Exception as e:
        logger.error(f"Churn prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to predict churn")


@router.post("/revenue-leak", response_model=PredictionResponse)
async def detect_revenue_leak(
    request: RevenueLeakDetectionRequest,
    model_version: Optional[str] = Query(None, description="Specific model version to use")
):
    """Detect potential revenue leaks"""
    try:
        predictor = Predictor()
        
        # Combine invoice and ticket data
        prediction_data = {
            **request.invoice_data,
            **request.ticket_data,
            "time_period_days": request.time_period_days
        }
        
        prediction = await predictor.predict(
            model_name="revenue_leak_detector",
            data=prediction_data,
            model_version=model_version,
            return_confidence=True
        )
        
        return prediction
        
    except Exception as e:
        logger.error(f"Revenue leak detection failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to detect revenue leaks")


@router.post("/pricing", response_model=PredictionResponse)
async def recommend_pricing(
    request: Dict[str, Any],
    model_version: Optional[str] = Query(None, description="Specific model version to use")
):
    """Get dynamic pricing recommendations"""
    try:
        predictor = Predictor()
        
        prediction = await predictor.predict(
            model_name="dynamic_pricing",
            data=request,
            model_version=model_version,
            return_confidence=True
        )
        
        return prediction
        
    except Exception as e:
        logger.error(f"Pricing recommendation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get pricing recommendations")


@router.post("/batch", response_model=BatchPredictionResponse)
async def batch_predict(
    request: BatchPredictionRequest,
    model_name: str = Query(..., description="Name of the model to use")
):
    """Perform batch predictions"""
    try:
        predictor = Predictor()
        
        predictions = await predictor.batch_predict(
            model_name=model_name,
            data_list=request.data,
            model_version=request.model_version,
            return_probabilities=request.return_probabilities,
            return_confidence=request.return_confidence
        )
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_predictions=len(predictions),
            processing_time_ms=sum(p.processing_time_ms for p in predictions),
            model_name=model_name,
            model_version=predictions[0].model_version if predictions else "unknown"
        )
        
    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform batch predictions")


@router.get("/models/{model_name}/info")
async def get_model_info(
    model_name: str = Path(..., description="Name of the model")
):
    """Get model information and capabilities"""
    try:
        predictor = Predictor()
        model_info = await predictor.get_model_info(model_name)
        
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")
        
        return model_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get model info for {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model information")


@router.get("/models/{model_name}/health")
async def get_model_health(
    model_name: str = Path(..., description="Name of the model")
):
    """Get model health status"""
    try:
        predictor = Predictor()
        health_status = await predictor.get_model_health(model_name)
        
        return health_status
        
    except Exception as e:
        logger.error(f"Failed to get model health for {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model health")
