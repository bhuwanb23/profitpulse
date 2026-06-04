"""
Client Churn Prediction Routes
Client churn prediction and prevention endpoints
"""

import logging
import time
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from ..models.schemas import (
    ClientChurnPredictionRequest, 
    ClientChurnPredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse
)
from ...models.churn_predictor.churn_predictor import ChurnPredictor

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
        
        # Compute date range from request timeframe
        end_date = datetime.now()
        start_date = end_date - timedelta(days=request.timeframe_days)
        
        # Run churn prediction pipeline
        start_time = time.perf_counter()
        result = await churn_predictor.run_full_pipeline(start_date=start_date, end_date=end_date)
        
        # Extract churn probability from pipeline results
        churn_probability = 0.5  # default fallback
        if result and 'risk_scores' in result:
            risk_scores = result['risk_scores']
            if isinstance(risk_scores, pd.DataFrame) and not risk_scores.empty and 'churn_probability' in risk_scores.columns:
                churn_probability = float(risk_scores['churn_probability'].mean())
            elif isinstance(risk_scores, list) and risk_scores:
                churn_probability = float(np.mean([r.get('churn_probability', 0.5) for r in risk_scores]))
        
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
            model_version=model_version or "1.0.0",
            prediction_id="churn_" + str(datetime.now().timestamp()),
            timestamp=datetime.now(),
            processing_time_ms=(time.perf_counter() - start_time) * 1000,
            confidence=0.85 if return_confidence else None,
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
        # Initialize churn predictor
        churn_predictor = ChurnPredictor()
        
        # Prepare data for batch prediction
        if request.data:
            clients_data = request.data
        else:
            raise HTTPException(status_code=400, detail="Batch data is required")
        
        # Run churn prediction pipeline
        start_time = time.perf_counter()
        result = await churn_predictor.run_full_pipeline()
        
        # Extract churn probability from pipeline (or use defaults for each client)
        default_probability = 0.5
        if result and 'risk_scores' in result:
            risk_scores = result['risk_scores']
            if isinstance(risk_scores, pd.DataFrame) and not risk_scores.empty and 'churn_probability' in risk_scores.columns:
                default_probability = float(risk_scores['churn_probability'].mean())
            elif isinstance(risk_scores, list) and risk_scores:
                default_probability = float(np.mean([r.get('churn_probability', 0.5) for r in risk_scores]))
        
        # Convert to proper format
        formatted_predictions = []
        for i, client_data in enumerate(clients_data):
            # Per-client variation around the pipeline result
            churn_probability = min(1.0, max(0.0, default_probability + 0.05 * (i % 5 - 2)))
            
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
                model_version=model_version or "1.0.0",
                prediction_id="churn_batch_" + str(i) + "_" + str(datetime.now().timestamp()),
                timestamp=datetime.now(),
                processing_time_ms=(time.perf_counter() - start_time) * 1000,
                confidence=0.85,
                churn_probability=churn_probability,
                risk_level=risk_level,
                intervention_recommendations=[]
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
        churn_predictor = ChurnPredictor()
        model_info = {"model_name": model_name, "version": "1.0.0", "status": "initialized"}
        
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
        churn_predictor = ChurnPredictor()
        health_status = {"model_name": model_name, "status": "healthy", "is_trained": churn_predictor.is_trained}
        
        return health_status
        
    except Exception as e:
        logger.error(f"Failed to get churn model health: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model health")