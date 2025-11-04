"""
Model Retraining Routes
API endpoints for managing model retraining triggers and jobs
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
import json

from ..models.schemas import (
    PredictionRequest
)
from ..dependencies import get_predictor
from ...utils.database import DatabaseManager

logger = logging.getLogger(__name__)
router = APIRouter()


def get_database_manager():
    """Get database manager instance"""
    return DatabaseManager()


@router.post("/triggers", response_model=Dict[str, Any])
async def create_retraining_trigger(
    model_name: str = Body(..., description="Model name to create trigger for"),
    trigger_type: str = Body(..., description="Type of trigger (performance, data_drift, scheduled, manual)"),
    trigger_condition: Dict[str, Any] = Body(..., description="Condition that triggers retraining"),
    enabled: bool = Body(True, description="Whether the trigger is enabled"),
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    Create a new model retraining trigger
    
    This endpoint creates a trigger that automatically initiates model retraining
    when certain conditions are met.
    """
    try:
        # Validate trigger type
        valid_trigger_types = ["performance", "data_drift", "scheduled", "manual"]
        if trigger_type not in valid_trigger_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid trigger type. Must be one of: {valid_trigger_types}"
            )
        
        # Prepare trigger data
        trigger_data = {
            "model_name": model_name,
            "trigger_type": trigger_type,
            "trigger_condition": json.dumps(trigger_condition),
            "enabled": enabled
        }
        
        # Save to database
        trigger_id = db.create_retraining_trigger(trigger_data)
        
        # Get the created trigger
        triggers = db.get_retraining_triggers(model_name)
        created_trigger = next((t for t in triggers if t["id"] == trigger_id), None)
        
        if created_trigger:
            # Convert trigger_condition back to dict for response
            try:
                created_trigger["trigger_condition"] = json.loads(created_trigger["trigger_condition"])
            except:
                created_trigger["trigger_condition"] = {}
        
        response = {
            "trigger_id": trigger_id,
            "message": "Retraining trigger created successfully",
            "trigger_details": created_trigger or {
                "id": trigger_id,
                "model_name": model_name,
                "trigger_type": trigger_type,
                "trigger_condition": trigger_condition,
                "enabled": enabled,
                "created_at": datetime.now().isoformat()
            }
        }
        
        logger.info(f"Created retraining trigger {trigger_id} for model {model_name}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create retraining trigger: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create retraining trigger"
        )


@router.get("/triggers/{model_name}", response_model=List[Dict[str, Any]])
async def list_retraining_triggers(
    model_name: str,
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    List all retraining triggers for a model
    
    This endpoint returns all retraining triggers configured for a specific model.
    """
    try:
        # Get triggers from database
        triggers = db.get_retraining_triggers(model_name)
        
        # Process triggers for response
        processed_triggers = []
        for trigger in triggers:
            # Convert trigger_condition back to dict
            try:
                if isinstance(trigger.get("trigger_condition"), str):
                    trigger["trigger_condition"] = json.loads(trigger["trigger_condition"])
            except:
                trigger["trigger_condition"] = {}
            processed_triggers.append(trigger)
        
        logger.info(f"Retrieved {len(processed_triggers)} retraining triggers for model {model_name}")
        return processed_triggers
        
    except Exception as e:
        logger.error(f"Failed to list retraining triggers for {model_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to list retraining triggers"
        )


@router.put("/triggers/{trigger_id}", response_model=Dict[str, Any])
async def update_retraining_trigger(
    trigger_id: str,
    trigger_data: Dict[str, Any] = Body(..., description="Updated trigger data"),
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    Update a retraining trigger
    
    This endpoint updates an existing retraining trigger configuration.
    """
    try:
        # Prepare update data
        update_data = trigger_data.copy()
        
        # Convert trigger_condition to JSON string if it's a dict
        if "trigger_condition" in update_data and isinstance(update_data["trigger_condition"], dict):
            update_data["trigger_condition"] = json.dumps(update_data["trigger_condition"])
        
        # Update in database
        updated = db.update_retraining_trigger(trigger_id, update_data)
        
        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Retraining trigger not found"
            )
        
        # Get the updated trigger
        # This is a simplification - in a real implementation, you would have a better way to retrieve it
        response = {
            "trigger_id": trigger_id,
            "message": "Retraining trigger updated successfully",
            "trigger_details": trigger_data
        }
        
        logger.info(f"Updated retraining trigger {trigger_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update retraining trigger {trigger_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to update retraining trigger"
        )


@router.delete("/triggers/{trigger_id}")
async def delete_retraining_trigger(
    trigger_id: str,
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    Delete a retraining trigger
    
    This endpoint deletes a retraining trigger, preventing automatic retraining.
    """
    try:
        # Delete from database
        deleted = db.delete_retraining_trigger(trigger_id)
        
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Retraining trigger not found"
            )
        
        response = {
            "message": "Retraining trigger deleted successfully",
            "trigger_id": trigger_id
        }
        
        logger.info(f"Deleted retraining trigger {trigger_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete retraining trigger {trigger_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete retraining trigger"
        )


@router.post("/jobs", response_model=Dict[str, Any])
async def trigger_manual_retraining(
    model_name: str = Body(..., description="Model name to retrain"),
    parameters: Dict[str, Any] = Body(default_factory=dict, description="Retraining parameters"),
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    Trigger manual model retraining
    
    This endpoint manually initiates model retraining with specified parameters.
    """
    try:
        # Prepare job data
        job_data = {
            "model_name": model_name,
            "status": "pending",
            "triggered_by": "manual",
            "trigger_type": "manual",
            "parameters": json.dumps(parameters) if parameters else "{}"
        }
        
        # Save to database
        job_id = db.create_retraining_job(job_data)
        
        # Get the created job
        job = db.get_retraining_job(job_id)
        
        if job:
            # Convert parameters back to dict for response
            try:
                if isinstance(job.get("parameters"), str):
                    job["parameters"] = json.loads(job["parameters"])
            except:
                job["parameters"] = {}
        
        response = {
            "job_id": job_id,
            "message": "Retraining job initiated successfully",
            "job_details": job or {
                "id": job_id,
                "model_name": model_name,
                "status": "pending",
                "triggered_by": "manual",
                "trigger_type": "manual",
                "parameters": parameters,
                "started_at": datetime.now().isoformat()
            }
        }
        
        logger.info(f"Initiated manual retraining job {job_id} for model {model_name}")
        return response
        
    except Exception as e:
        logger.error(f"Failed to initiate manual retraining for {model_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to initiate manual retraining"
        )


@router.get("/jobs/{job_id}", response_model=Dict[str, Any])
async def get_retraining_job_status(
    job_id: str,
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    Get retraining job status
    
    This endpoint returns the current status of a retraining job.
    """
    try:
        # Get job from database
        job = db.get_retraining_job(job_id)
        
        if not job:
            raise HTTPException(
                status_code=404,
                detail="Retraining job not found"
            )
        
        # Process job data for response
        # Convert parameters back to dict
        try:
            if isinstance(job.get("parameters"), str):
                job["parameters"] = json.loads(job["parameters"])
        except:
            job["parameters"] = {}
        
        logger.info(f"Retrieved retraining job status for {job_id}")
        return job
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get retraining job status for {job_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get retraining job status"
        )


@router.get("/jobs/{model_name}/history", response_model=List[Dict[str, Any]])
async def get_retraining_history(
    model_name: str,
    limit: int = Query(50, description="Maximum number of jobs to return"),
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    Get retraining job history for a model
    
    This endpoint returns the history of retraining jobs for a specific model.
    """
    try:
        # Get history from database
        history = db.get_retraining_history(model_name, limit)
        
        # Process history for response
        processed_history = []
        for job in history:
            # Convert parameters back to dict
            try:
                if isinstance(job.get("parameters"), str):
                    job["parameters"] = json.loads(job["parameters"])
            except:
                job["parameters"] = {}
            processed_history.append(job)
        
        logger.info(f"Retrieved {len(processed_history)} retraining jobs for model {model_name}")
        return processed_history
        
    except Exception as e:
        logger.error(f"Failed to get retraining history for {model_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get retraining history"
        )