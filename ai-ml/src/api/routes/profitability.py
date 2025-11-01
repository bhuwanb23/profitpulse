"""
Profitability Prediction Routes
Client profitability prediction endpoints
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from ..models.schemas import (
    ClientProfitabilityPredictionRequest, 
    ClientProfitabilityPredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse
)
from ..dependencies import get_predictor
from ...models.profitability_predictor.profitability_predictor import ProfitabilityPredictor
from ...utils.predictor import Predictor

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=ClientProfitabilityPredictionResponse)
async def predict_client_profitability(
    request: ClientProfitabilityPredictionRequest,
    model_version: Optional[str] = Query(None, description="Specific model version to use"),
    return_confidence: bool = Query(False, description="Return confidence intervals"),
    return_explanation: bool = Query(False, description="Return SHAP explanations")
):
    """
    Predict client profitability score and provide recommendations
    
    This endpoint analyzes client data to predict profitability and provide actionable recommendations.
    The profitability score ranges from 0-100, where higher scores indicate more profitable clients.
    """
    try:
        # Initialize profitability predictor
        profitability_predictor = ProfitabilityPredictor()
        await profitability_predictor.initialize()
        
        # Prepare data for prediction
        prediction_data = {
            "client_id": request.client_id,
            **request.financial_data,
            **request.operational_data
        }
        
        # Make prediction
        prediction_result = await profitability_predictor.predict(
            client_data=prediction_data,
            model_type=model_version or "auto",
            return_confidence=return_confidence,
            return_explanation=return_explanation
        )
        
        # Convert prediction to proper format (0-100 scale)
        profitability_score = prediction_result["prediction"] * 100
        
        # Determine profitability category
        if profitability_score >= 70:
            category = "high"
        elif profitability_score >= 40:
            category = "medium"
        else:
            category = "low"
        
        # Create mock recommendations (in a real implementation, this would be based on the prediction)
        recommendations = []
        if profitability_score < 50:
            recommendations.extend([
                {"type": "service_optimization", "description": "Optimize service delivery to reduce costs"},
                {"type": "pricing_review", "description": "Review pricing strategy for this client"}
            ])
        elif profitability_score > 80:
            recommendations.extend([
                {"type": "upsell_opportunity", "description": "Identify upsell opportunities with this client"},
                {"type": "relationship_building", "description": "Invest in strengthening client relationship"}
            ])
        
        # Build response
        response = ClientProfitabilityPredictionResponse(
            prediction=profitability_score,
            model_name="client_profitability",
            model_version=model_version or prediction_result.get("model_type", "1.0.0"),
            prediction_id=prediction_result.get("prediction_id", "mock_id"),
            timestamp=datetime.fromisoformat(prediction_result["timestamp"]) if "timestamp" in prediction_result else datetime.now(),
            processing_time_ms=prediction_result.get("prediction_time_ms", 50.0),
            confidence=prediction_result.get("confidence_level", 0.85) if return_confidence else None,
            profitability_score=profitability_score,
            profitability_category=category,
            improvement_recommendations=recommendations
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Profitability prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to predict client profitability")


@router.post("/batch", response_model=BatchPredictionResponse)
async def batch_predict_profitability(
    request: BatchPredictionRequest,
    model_version: Optional[str] = Query(None, description="Specific model version to use")
):
    """
    Perform batch profitability predictions for multiple clients
    
    This endpoint allows processing multiple client predictions in a single request.
    """
    try:
        # Initialize profitability predictor
        profitability_predictor = ProfitabilityPredictor()
        await profitability_predictor.initialize()
        
        # Prepare data for batch prediction
        if request.data:
            clients_data = request.data
        else:
            # In a real implementation, we would fetch data from the provided URL
            raise HTTPException(status_code=400, detail="Batch data is required")
        
        # Make batch predictions
        predictions = await profitability_predictor.batch_predict(
            clients_data=clients_data,
            model_type=model_version or "auto"
        )
        
        # Convert predictions to proper format
        formatted_predictions = []
        for i, pred in enumerate(predictions):
            profitability_score = pred["prediction"] * 100
            
            # Determine profitability category
            if profitability_score >= 70:
                category = "high"
            elif profitability_score >= 40:
                category = "medium"
            else:
                category = "low"
            
            formatted_pred = ClientProfitabilityPredictionResponse(
                prediction=profitability_score,
                model_name="client_profitability",
                model_version=model_version or pred.get("model_type", "1.0.0"),
                prediction_id=pred.get("prediction_id", f"mock_id_{i}"),
                timestamp=datetime.fromisoformat(pred["timestamp"]) if "timestamp" in pred else datetime.now(),
                processing_time_ms=pred.get("prediction_time_ms", 50.0),
                confidence=pred.get("confidence_level", 0.85),
                profitability_score=profitability_score,
                profitability_category=category,
                improvement_recommendations=[]  # Would be populated in real implementation
            )
            formatted_predictions.append(formatted_pred)
        
        # Build batch response
        response = BatchPredictionResponse(
            predictions=formatted_predictions,
            total_predictions=len(formatted_predictions),
            processing_time_ms=sum(pred.processing_time_ms for pred in formatted_predictions),
            model_name="client_profitability",
            model_version=model_version or "1.0.0"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch profitability prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform batch profitability predictions")


@router.get("/models/{model_name}/info")
async def get_profitability_model_info(
    model_name: str = "client_profitability"
):
    """
    Get profitability model information and capabilities
    """
    try:
        # Initialize profitability predictor to get model info
        profitability_predictor = ProfitabilityPredictor()
        await profitability_predictor.initialize()
        
        model_info = {
            "name": model_name,
            "version": "1.0.0",
            "status": "ready" if profitability_predictor.is_initialized else "loading",
            "features": profitability_predictor.feature_names if profitability_predictor.feature_names else [],
            "capabilities": {
                "supports_probabilities": False,
                "supports_confidence": True,
                "supports_explanations": True,
                "supports_batch": True,
                "max_batch_size": 1000
            },
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        return model_info
        
    except Exception as e:
        logger.error(f"Failed to get profitability model info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model information")


@router.get("/models/{model_name}/health")
async def get_profitability_model_health(
    model_name: str = "client_profitability"
):
    """
    Get profitability model health status
    """
    try:
        # Initialize profitability predictor to check health
        profitability_predictor = ProfitabilityPredictor()
        await profitability_predictor.initialize()
        
        health_status = {
            "status": "healthy" if profitability_predictor.is_initialized else "unhealthy",
            "healthy": profitability_predictor.is_initialized,
            "last_check": datetime.now().isoformat(),
            "uptime": "99.9%",  # Mock uptime
            "response_time_ms": 45.2,  # Mock response time
            "error_rate": 0.01  # Mock error rate
        }
        
        return health_status
        
    except Exception as e:
        logger.error(f"Failed to get profitability model health: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model health")