"""
Client Churn Prediction Routes
Client churn prediction and prevention endpoints
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from ..models.schemas import (
    ClientChurnPredictionRequest, 
    ClientChurnPredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse
)
from ..dependencies import get_predictor
from ...models.churn_predictor.churn_predictor import ChurnPredictor
from ...utils.predictor import Predictor

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=ClientChurnPredictionResponse)
async def predict_client_churn(
    request: ClientChurnPredictionRequest,
    model_version: Optional[str] = Query(None, description="Specific model version to use"),
    return_confidence: bool = Query(False, description="Return confidence intervals")
):
    """
    Predict client churn probability and provide risk assessment
    
    This endpoint analyzes client data to predict the probability of churn and provide risk assessment.
    The churn probability ranges from 0-1, where higher values indicate higher risk of churn.
    """
    try:
        # Initialize churn predictor
        churn_predictor = ChurnPredictor()
        
        # Prepare data for prediction
        prediction_data = {
            "client_id": request.client_id,
            **request.features
        }
        
        # In a real implementation, we would use the churn predictor's predict method
        # For now, we'll use the generic predictor with mock data
        
        # Make prediction using generic predictor
        predictor = Predictor()
        prediction_result = await predictor.predict(
            model_name="client_churn",
            data=prediction_data,
            model_version=model_version,
            return_probabilities=True,
            return_confidence=return_confidence
        )
        
        # Extract churn probability
        churn_probability = prediction_result["prediction"]
        
        # Determine risk level
        if churn_probability >= 0.7:
            risk_level = "high"
        elif churn_probability >= 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Create mock interventions (in a real implementation, this would be based on the prediction)
        interventions = []
        if churn_probability > 0.5:
            interventions.extend([
                {"type": "engagement_campaign", "description": "Launch targeted engagement campaign"},
                {"type": "discount_offer", "description": "Provide special discount offer"},
                {"type": "account_review", "description": "Schedule account review meeting"}
            ])
        elif churn_probability > 0.3:
            interventions.extend([
                {"type": "check_in_call", "description": "Schedule check-in call with client"},
                {"type": "service_review", "description": "Review service delivery quality"}
            ])
        
        # Build response
        response = ClientChurnPredictionResponse(
            prediction=churn_probability,
            model_name="client_churn",
            model_version=model_version or prediction_result.get("model_version", "1.0.0"),
            prediction_id=prediction_result.get("prediction_id", "mock_id"),
            timestamp=prediction_result.get("timestamp", datetime.now()),
            processing_time_ms=prediction_result.get("processing_time_ms", 50.0),
            confidence=prediction_result.get("confidence", 0.85) if return_confidence else None,
            churn_probability=churn_probability,
            risk_level=risk_level,
            intervention_recommendations=interventions
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Churn prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to predict client churn")


@router.post("/batch", response_model=BatchPredictionResponse)
async def batch_predict_churn(
    request: BatchPredictionRequest,
    model_version: Optional[str] = Query(None, description="Specific model version to use")
):
    """
    Perform batch churn predictions for multiple clients
    
    This endpoint allows processing multiple client predictions in a single request.
    """
    try:
        # Initialize predictor
        predictor = Predictor()
        
        # Prepare data for batch prediction
        if request.data:
            clients_data = request.data
        else:
            # In a real implementation, we would fetch data from the provided URL
            raise HTTPException(status_code=400, detail="Batch data is required")
        
        # Make batch predictions
        predictions = await predictor.batch_predict(
            model_name="client_churn",
            data_list=clients_data,
            model_version=model_version,
            return_probabilities=True,
            return_confidence=True
        )
        
        # Convert predictions to proper format
        formatted_predictions = []
        for pred in predictions:
            churn_probability = pred["prediction"]
            
            # Determine risk level
            if churn_probability >= 0.7:
                risk_level = "high"
            elif churn_probability >= 0.4:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            formatted_pred = ClientChurnPredictionResponse(
                prediction=churn_probability,
                model_name="client_churn",
                model_version=model_version or pred.get("model_version", "1.0.0"),
                prediction_id=pred.get("prediction_id", "mock_id"),
                timestamp=pred.get("timestamp", datetime.now()),
                processing_time_ms=pred.get("processing_time_ms", 50.0),
                confidence=pred.get("confidence", 0.85),
                churn_probability=churn_probability,
                risk_level=risk_level,
                intervention_recommendations=[]  # Would be populated in real implementation
            )
            formatted_predictions.append(formatted_pred)
        
        # Build batch response
        response = BatchPredictionResponse(
            predictions=formatted_predictions,
            total_predictions=len(formatted_predictions),
            processing_time_ms=sum(pred.processing_time_ms for pred in formatted_predictions),
            model_name="client_churn",
            model_version=model_version or "1.0.0"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch churn prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform batch churn predictions")


@router.get("/models/{model_name}/info")
async def get_churn_model_info(
    model_name: str = "client_churn"
):
    """
    Get churn model information and capabilities
    """
    try:
        predictor = Predictor()
        model_info = await predictor.get_model_info(model_name)
        
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")
        
        return model_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get churn model info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model information")


@router.get("/models/{model_name}/health")
async def get_churn_model_health(
    model_name: str = "client_churn"
):
    """
    Get churn model health status
    """
    try:
        predictor = Predictor()
        health_status = await predictor.get_model_health(model_name)
        
        return health_status
        
    except Exception as e:
        logger.error(f"Failed to get churn model health: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model health")