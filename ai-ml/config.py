"""
SuperHack AI/ML Configuration
Environment configuration and settings management
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"
FEATURE_STORE_DIR = PROJECT_ROOT / "feature_store"
MLRUNS_DIR = PROJECT_ROOT / "mlruns"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, LOGS_DIR, FEATURE_STORE_DIR, MLRUNS_DIR]:
    directory.mkdir(exist_ok=True)


class DatabaseConfig(BaseSettings):
    """Database configuration"""
    url: str = Field(default="sqlite:///./superhack_ai.db", env="DATABASE_URL")
    postgres_url: Optional[str] = Field(default=None, env="POSTGRES_URL")
    echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    class Config:
        env_file = ".env"


class BackendAPIConfig(BaseSettings):
    """Backend API configuration"""
    url: str = Field(default="http://localhost:3000", env="BACKEND_API_URL")
    api_key: Optional[str] = Field(default=None, env="BACKEND_API_KEY")
    timeout: int = Field(default=30, env="BACKEND_API_TIMEOUT")
    
    class Config:
        env_file = ".env"


class SuperOpsConfig(BaseSettings):
    """SuperOps integration configuration"""
    api_url: str = Field(default="https://api.superops.ai", env="SUPEROPS_API_URL")
    api_key: Optional[str] = Field(default=None, env="SUPEROPS_API_KEY")
    organization_id: Optional[str] = Field(default=None, env="SUPEROPS_ORGANIZATION_ID")
    timeout: int = Field(default=30, env="SUPEROPS_TIMEOUT")
    
    class Config:
        env_file = ".env"


class QuickBooksConfig(BaseSettings):
    """QuickBooks integration configuration"""
    client_id: Optional[str] = Field(default=None, env="QUICKBOOKS_CLIENT_ID")
    client_secret: Optional[str] = Field(default=None, env="QUICKBOOKS_CLIENT_SECRET")
    redirect_uri: str = Field(default="http://localhost:8000/auth/callback", env="QUICKBOOKS_REDIRECT_URI")
    sandbox_url: str = Field(default="https://sandbox-quickbooks.api.intuit.com", env="QUICKBOOKS_SANDBOX_URL")
    production_url: str = Field(default="https://quickbooks.api.intuit.com", env="QUICKBOOKS_PRODUCTION_URL")
    use_sandbox: bool = Field(default=True, env="QUICKBOOKS_USE_SANDBOX")
    
    class Config:
        env_file = ".env"


class MLflowConfig(BaseSettings):
    """MLflow configuration"""
    tracking_uri: str = Field(default="http://localhost:5000", env="MLFLOW_TRACKING_URI")
    experiment_name: str = Field(default="superhack_ai_models", env="MLFLOW_EXPERIMENT_NAME")
    artifact_root: str = Field(default=str(MLRUNS_DIR), env="MLFLOW_ARTIFACT_ROOT")
    
    class Config:
        env_file = ".env"


class WandBConfig(BaseSettings):
    """Weights & Biases configuration"""
    api_key: Optional[str] = Field(default=None, env="WANDB_API_KEY")
    project: str = Field(default="superhack-ai-models", env="WANDB_PROJECT")
    entity: Optional[str] = Field(default=None, env="WANDB_ENTITY")
    
    class Config:
        env_file = ".env"


class ModelServerConfig(BaseSettings):
    """Model serving configuration"""
    host: str = Field(default="0.0.0.0", env="MODEL_SERVER_HOST")
    port: int = Field(default=8000, env="MODEL_SERVER_PORT")
    workers: int = Field(default=4, env="MODEL_SERVER_WORKERS")
    reload: bool = Field(default=False, env="RELOAD")
    
    class Config:
        env_file = ".env"


class RedisConfig(BaseSettings):
    """Redis configuration"""
    url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    
    class Config:
        env_file = ".env"


class CeleryConfig(BaseSettings):
    """Celery configuration"""
    broker_url: str = Field(default="redis://localhost:6379/1", env="CELERY_BROKER_URL")
    result_backend: str = Field(default="redis://localhost:6379/2", env="CELERY_RESULT_BACKEND")
    
    class Config:
        env_file = ".env"


class LoggingConfig(BaseSettings):
    """Logging configuration"""
    level: str = Field(default="INFO", env="LOG_LEVEL")
    file: str = Field(default=str(LOGS_DIR / "ai_ml.log"), env="LOG_FILE")
    max_size: str = Field(default="10MB", env="LOG_MAX_SIZE")
    backup_count: int = Field(default=5, env="LOG_BACKUP_COUNT")
    
    class Config:
        env_file = ".env"


class SecurityConfig(BaseSettings):
    """Security configuration"""
    secret_key: str = Field(default="your_secret_key_change_in_production", env="SECRET_KEY")
    jwt_secret_key: str = Field(default="your_jwt_secret_key_change_in_production", env="JWT_SECRET_KEY")
    encryption_key: str = Field(default="your_encryption_key_change_in_production", env="ENCRYPTION_KEY")
    
    class Config:
        env_file = ".env"


class FeatureStoreConfig(BaseSettings):
    """Feature store configuration"""
    path: str = Field(default=str(FEATURE_STORE_DIR), env="FEATURE_STORE_PATH")
    cache_ttl: int = Field(default=3600, env="FEATURE_CACHE_TTL")  # seconds
    
    class Config:
        env_file = ".env"


class ModelConfig(BaseSettings):
    """Model configuration"""
    registry_path: str = Field(default=str(MODELS_DIR), env="MODEL_REGISTRY_PATH")
    cache_size: int = Field(default=10, env="MODEL_CACHE_SIZE")
    update_frequency: int = Field(default=24, env="MODEL_UPDATE_FREQUENCY")  # hours
    
    class Config:
        env_file = ".env"


class DataProcessingConfig(BaseSettings):
    """Data processing configuration"""
    batch_size: int = Field(default=1000, env="BATCH_SIZE")
    max_workers: int = Field(default=4, env="MAX_WORKERS")
    validation_enabled: bool = Field(default=True, env="DATA_VALIDATION_ENABLED")
    
    class Config:
        env_file = ".env"


class MonitoringConfig(BaseSettings):
    """Monitoring configuration"""
    prometheus_enabled: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    prometheus_port: int = Field(default=9090, env="PROMETHEUS_PORT")
    health_check_interval: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")  # seconds
    
    class Config:
        env_file = ".env"


class Settings(BaseSettings):
    """Main settings class that combines all configurations"""
    
    # Environment
    debug: bool = Field(default=False, env="DEBUG")
    testing: bool = Field(default=False, env="TESTING")
    
    # Sub-configurations
    database: DatabaseConfig = DatabaseConfig()
    backend_api: BackendAPIConfig = BackendAPIConfig()
    superops: SuperOpsConfig = SuperOpsConfig()
    quickbooks: QuickBooksConfig = QuickBooksConfig()
    mlflow: MLflowConfig = MLflowConfig()
    wandb: WandBConfig = WandBConfig()
    model_server: ModelServerConfig = ModelServerConfig()
    redis: RedisConfig = RedisConfig()
    celery: CeleryConfig = CeleryConfig()
    logging: LoggingConfig = LoggingConfig()
    security: SecurityConfig = SecurityConfig()
    feature_store: FeatureStoreConfig = FeatureStoreConfig()
    models: ModelConfig = ModelConfig()
    data_processing: DataProcessingConfig = DataProcessingConfig()
    monitoring: MonitoringConfig = MonitoringConfig()
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Export commonly used configurations
__all__ = [
    "settings",
    "PROJECT_ROOT",
    "DATA_DIR", 
    "MODELS_DIR",
    "LOGS_DIR",
    "FEATURE_STORE_DIR",
    "MLRUNS_DIR"
]
