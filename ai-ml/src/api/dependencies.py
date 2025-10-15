"""
API Dependencies
Dependency injection for services and utilities
"""

import logging
from functools import lru_cache
from typing import Optional

from src.utils.model_registry import ModelRegistry
from src.utils.metrics_collector import MetricsCollector
from src.utils.predictor import Predictor
from src.utils.monitoring import MonitoringService
from src.utils.admin import AdminService
from src.utils.health_checker import HealthChecker

logger = logging.getLogger(__name__)

# Global instances
_model_registry: Optional[ModelRegistry] = None
_metrics_collector: Optional[MetricsCollector] = None
_predictor: Optional[Predictor] = None
_monitoring_service: Optional[MonitoringService] = None
_admin_service: Optional[AdminService] = None
_health_checker: Optional[HealthChecker] = None


@lru_cache()
def get_model_registry() -> ModelRegistry:
    """Get model registry instance"""
    global _model_registry
    if _model_registry is None:
        _model_registry = ModelRegistry()
        logger.info("Model registry initialized")
    return _model_registry


@lru_cache()
def get_metrics_collector() -> MetricsCollector:
    """Get metrics collector instance"""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
        logger.info("Metrics collector initialized")
    return _metrics_collector


@lru_cache()
def get_predictor() -> Predictor:
    """Get predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = Predictor()
        logger.info("Predictor initialized")
    return _predictor


@lru_cache()
def get_monitoring_service() -> MonitoringService:
    """Get monitoring service instance"""
    global _monitoring_service
    if _monitoring_service is None:
        _monitoring_service = MonitoringService()
        logger.info("Monitoring service initialized")
    return _monitoring_service


@lru_cache()
def get_admin_service() -> AdminService:
    """Get admin service instance"""
    global _admin_service
    if _admin_service is None:
        _admin_service = AdminService()
        logger.info("Admin service initialized")
    return _admin_service


@lru_cache()
def get_health_checker() -> HealthChecker:
    """Get health checker instance"""
    global _health_checker
    if _health_checker is None:
        _health_checker = HealthChecker()
        logger.info("Health checker initialized")
    return _health_checker


def cleanup_dependencies():
    """Cleanup all dependency instances"""
    global _model_registry, _metrics_collector, _predictor
    global _monitoring_service, _admin_service, _health_checker
    
    if _model_registry:
        _model_registry.cleanup()
        _model_registry = None
    
    if _metrics_collector:
        _metrics_collector.cleanup()
        _metrics_collector = None
    
    if _predictor:
        _predictor.cleanup()
        _predictor = None
    
    if _monitoring_service:
        _monitoring_service.cleanup()
        _monitoring_service = None
    
    if _admin_service:
        _admin_service.cleanup()
        _admin_service = None
    
    if _health_checker:
        _health_checker.cleanup()
        _health_checker = None
    
    logger.info("All dependencies cleaned up")
