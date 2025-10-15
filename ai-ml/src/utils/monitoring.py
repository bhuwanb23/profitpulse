"""
Monitoring Service
Model performance monitoring, alerting, and drift detection
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import uuid

logger = logging.getLogger(__name__)


class MonitoringService:
    """Service for monitoring model performance and generating alerts"""
    
    def __init__(self):
        self.alert_rules: Dict[str, Dict[str, Any]] = {}
        self.alerts: Dict[str, Dict[str, Any]] = {}
        self.performance_data: Dict[str, List[Dict[str, Any]]] = {}
        self._initialized = False
    
    async def initialize(self):
        """Initialize monitoring service"""
        try:
            # Load default alert rules
            await self._load_default_alert_rules()
            self._initialized = True
            logger.info("Monitoring service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize monitoring service: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup monitoring service"""
        logger.info("Monitoring service cleaned up")
    
    async def _load_default_alert_rules(self):
        """Load default alert rules"""
        try:
            default_rules = [
                {
                    "id": "high_error_rate",
                    "name": "High Error Rate",
                    "model_name": "*",
                    "metric": "error_rate",
                    "threshold": 0.05,
                    "operator": "gt",
                    "severity": "high",
                    "enabled": True
                },
                {
                    "id": "low_accuracy",
                    "name": "Low Accuracy",
                    "model_name": "*",
                    "metric": "accuracy",
                    "threshold": 0.8,
                    "operator": "lt",
                    "severity": "medium",
                    "enabled": True
                },
                {
                    "id": "high_latency",
                    "name": "High Prediction Latency",
                    "model_name": "*",
                    "metric": "prediction_latency_ms",
                    "threshold": 1000,
                    "operator": "gt",
                    "severity": "medium",
                    "enabled": True
                }
            ]
            
            for rule in default_rules:
                self.alert_rules[rule["id"]] = rule
            
            logger.info("Default alert rules loaded")
            
        except Exception as e:
            logger.error(f"Failed to load default alert rules: {e}")
    
    async def get_metrics(self, time_range: str = "1h", 
                         model_name: Optional[str] = None) -> Dict[str, Any]:
        """Get system and model metrics"""
        try:
            # Parse time range
            time_delta = self._parse_time_range(time_range)
            cutoff_time = datetime.now() - time_delta
            
            # Generate mock metrics
            metrics = {
                "timestamp": datetime.now(),
                "metrics": {
                    "system": {
                        "cpu_usage": 45.2,
                        "memory_usage": 68.5,
                        "disk_usage": 32.1,
                        "request_count": 1250,
                        "error_count": 12,
                        "uptime_hours": 168.5
                    },
                    "models": {}
                },
                "model_metrics": {}
            }
            
            # Add model-specific metrics
            if model_name:
                metrics["model_metrics"][model_name] = await self._get_model_metrics(model_name, cutoff_time)
            else:
                # Get metrics for all models
                for model in ["client_profitability", "client_churn", "revenue_leak_detector", "dynamic_pricing"]:
                    metrics["model_metrics"][model] = await self._get_model_metrics(model, cutoff_time)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            return {"timestamp": datetime.now(), "metrics": {}, "model_metrics": {}}
    
    async def get_performance_metrics(self, model_name: Optional[str] = None,
                                    days: int = 7, limit: int = 100) -> List[Dict[str, Any]]:
        """Get model performance metrics"""
        try:
            # Generate mock performance data
            performance_data = []
            
            models = [model_name] if model_name else ["client_profitability", "client_churn", "revenue_leak_detector", "dynamic_pricing"]
            
            for model in models:
                for i in range(min(limit // len(models), 20)):
                    timestamp = datetime.now() - timedelta(days=i)
                    
                    performance = {
                        "model_name": model,
                        "accuracy": 0.85 + (i % 10) * 0.01,
                        "precision": 0.82 + (i % 8) * 0.01,
                        "recall": 0.88 + (i % 12) * 0.01,
                        "f1_score": 0.85 + (i % 9) * 0.01,
                        "auc_roc": 0.90 + (i % 6) * 0.01,
                        "prediction_latency_ms": 45.2 + (i % 15) * 2.5,
                        "throughput_per_second": 120.5 + (i % 20) * 5.2,
                        "error_rate": 0.02 + (i % 5) * 0.001,
                        "timestamp": timestamp
                    }
                    
                    performance_data.append(performance)
            
            return performance_data[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return []
    
    async def get_alerts(self, status: Optional[str] = None,
                        severity: Optional[str] = None,
                        model_name: Optional[str] = None,
                        limit: int = 50) -> List[Dict[str, Any]]:
        """Get alerts"""
        try:
            # Generate mock alerts
            alerts = []
            
            alert_templates = [
                {
                    "rule_name": "High Error Rate",
                    "model_name": "client_profitability",
                    "metric": "error_rate",
                    "current_value": 0.08,
                    "threshold": 0.05,
                    "severity": "high",
                    "status": "active",
                    "message": "Error rate exceeded threshold"
                },
                {
                    "rule_name": "Low Accuracy",
                    "model_name": "client_churn",
                    "metric": "accuracy",
                    "current_value": 0.75,
                    "threshold": 0.8,
                    "severity": "medium",
                    "status": "acknowledged",
                    "message": "Model accuracy below threshold"
                },
                {
                    "rule_name": "High Latency",
                    "model_name": "revenue_leak_detector",
                    "metric": "prediction_latency_ms",
                    "current_value": 1200,
                    "threshold": 1000,
                    "severity": "medium",
                    "status": "resolved",
                    "message": "Prediction latency exceeded threshold"
                }
            ]
            
            for i, template in enumerate(alert_templates):
                alert = {
                    "id": f"alert_{i+1}",
                    "rule_name": template["rule_name"],
                    "model_name": template["model_name"],
                    "metric": template["metric"],
                    "current_value": template["current_value"],
                    "threshold": template["threshold"],
                    "severity": template["severity"],
                    "status": template["status"],
                    "created_at": datetime.now() - timedelta(hours=i*2),
                    "resolved_at": datetime.now() - timedelta(hours=i*2-1) if template["status"] == "resolved" else None,
                    "message": template["message"]
                }
                
                # Apply filters
                if status and alert["status"] != status:
                    continue
                if severity and alert["severity"] != severity:
                    continue
                if model_name and alert["model_name"] != model_name:
                    continue
                
                alerts.append(alert)
            
            return alerts[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get alerts: {e}")
            return []
    
    async def create_alert_rule(self, rule_data: Dict[str, Any]) -> str:
        """Create a new alert rule"""
        try:
            rule_id = str(uuid.uuid4())
            rule_data["id"] = rule_id
            rule_data["created_at"] = datetime.now()
            
            self.alert_rules[rule_id] = rule_data
            
            logger.info(f"Alert rule created: {rule_id}")
            return rule_id
            
        except Exception as e:
            logger.error(f"Failed to create alert rule: {e}")
            raise
    
    async def get_alert_rules(self, model_name: Optional[str] = None,
                            enabled_only: bool = True) -> List[Dict[str, Any]]:
        """Get alert rules"""
        try:
            rules = list(self.alert_rules.values())
            
            # Apply filters
            if model_name and model_name != "*":
                rules = [rule for rule in rules if rule.get("model_name") == model_name or rule.get("model_name") == "*"]
            
            if enabled_only:
                rules = [rule for rule in rules if rule.get("enabled", True)]
            
            return rules
            
        except Exception as e:
            logger.error(f"Failed to get alert rules: {e}")
            return []
    
    async def update_alert_rule(self, rule_id: str, rule_data: Dict[str, Any]) -> bool:
        """Update an alert rule"""
        try:
            if rule_id not in self.alert_rules:
                return False
            
            rule_data["id"] = rule_id
            rule_data["updated_at"] = datetime.now()
            
            self.alert_rules[rule_id] = rule_data
            
            logger.info(f"Alert rule updated: {rule_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update alert rule {rule_id}: {e}")
            return False
    
    async def delete_alert_rule(self, rule_id: str) -> bool:
        """Delete an alert rule"""
        try:
            if rule_id not in self.alert_rules:
                return False
            
            del self.alert_rules[rule_id]
            
            logger.info(f"Alert rule deleted: {rule_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete alert rule {rule_id}: {e}")
            return False
    
    async def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        try:
            # In a real implementation, this would update the alert in a database
            logger.info(f"Alert acknowledged: {alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to acknowledge alert {alert_id}: {e}")
            return False
    
    async def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert"""
        try:
            # In a real implementation, this would update the alert in a database
            logger.info(f"Alert resolved: {alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to resolve alert {alert_id}: {e}")
            return False
    
    async def get_dashboard_data(self, time_range: str = "24h") -> Dict[str, Any]:
        """Get dashboard data for monitoring UI"""
        try:
            time_delta = self._parse_time_range(time_range)
            cutoff_time = datetime.now() - time_delta
            
            dashboard_data = {
                "summary": {
                    "total_models": 4,
                    "active_alerts": 2,
                    "total_predictions": 1250,
                    "avg_accuracy": 0.87,
                    "avg_latency_ms": 45.2
                },
                "models": await self._get_model_summaries(),
                "alerts": await self.get_alerts(limit=10),
                "performance_trends": await self._get_performance_trends(cutoff_time),
                "system_health": {
                    "status": "healthy",
                    "uptime": "99.9%",
                    "cpu_usage": 45.2,
                    "memory_usage": 68.5
                }
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Failed to get dashboard data: {e}")
            return {}
    
    async def get_model_drift(self, model_name: str, days: int = 30) -> Dict[str, Any]:
        """Get model drift analysis"""
        try:
            # Generate mock drift analysis
            drift_analysis = {
                "model_name": model_name,
                "analysis_period_days": days,
                "drift_detected": True,
                "drift_score": 0.15,
                "feature_drift": {
                    "contract_value": 0.12,
                    "hours_logged": 0.08,
                    "billing_amount": 0.18
                },
                "performance_drift": {
                    "accuracy_change": -0.03,
                    "precision_change": -0.02,
                    "recall_change": -0.01
                },
                "recommendations": [
                    "Consider retraining the model",
                    "Review feature engineering pipeline",
                    "Monitor data quality"
                ],
                "last_analyzed": datetime.now().isoformat()
            }
            
            return drift_analysis
            
        except Exception as e:
            logger.error(f"Failed to get model drift for {model_name}: {e}")
            return {}
    
    async def _get_model_metrics(self, model_name: str, cutoff_time: datetime) -> Dict[str, Any]:
        """Get metrics for a specific model"""
        return {
            "accuracy": 0.85 + (hash(model_name) % 10) * 0.01,
            "latency_ms": 45.2 + (hash(model_name) % 15) * 2.5,
            "throughput_per_second": 120.5 + (hash(model_name) % 20) * 5.2,
            "error_rate": 0.02 + (hash(model_name) % 5) * 0.001,
            "predictions_count": 250 + (hash(model_name) % 100)
        }
    
    async def _get_model_summaries(self) -> List[Dict[str, Any]]:
        """Get model summaries for dashboard"""
        models = ["client_profitability", "client_churn", "revenue_leak_detector", "dynamic_pricing"]
        summaries = []
        
        for model in models:
            summaries.append({
                "name": model,
                "status": "healthy",
                "accuracy": 0.85 + (hash(model) % 10) * 0.01,
                "latency_ms": 45.2 + (hash(model) % 15) * 2.5,
                "predictions_today": 250 + (hash(model) % 100),
                "last_prediction": datetime.now().isoformat()
            })
        
        return summaries
    
    async def _get_performance_trends(self, cutoff_time: datetime) -> Dict[str, List[float]]:
        """Get performance trends for dashboard"""
        return {
            "accuracy": [0.85, 0.86, 0.84, 0.87, 0.85, 0.88, 0.86],
            "latency": [45.2, 42.1, 48.5, 44.3, 46.8, 43.2, 45.7],
            "throughput": [120.5, 125.2, 118.8, 122.1, 119.5, 124.3, 121.8]
        }
    
    def _parse_time_range(self, time_range: str) -> timedelta:
        """Parse time range string to timedelta"""
        time_ranges = {
            "1h": timedelta(hours=1),
            "24h": timedelta(hours=24),
            "7d": timedelta(days=7),
            "30d": timedelta(days=30)
        }
        return time_ranges.get(time_range, timedelta(hours=1))
