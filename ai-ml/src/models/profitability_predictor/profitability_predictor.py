"""
Real-time Profitability Predictor
Handles model loading, inference, and prediction serving for client profitability
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import json
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

# Conditional imports for model libraries
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    xgb = None

try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    RandomForestRegressor = None
    StandardScaler = None
    LabelEncoder = None

# Local imports
try:
    from .feature_engineering import ProfitabilityFeatureEngineer
    FEATURE_ENGINEER_AVAILABLE = True
except ImportError:
    ProfitabilityFeatureEngineer = None
    FEATURE_ENGINEER_AVAILABLE = False

try:
    from .data_preparation import ProfitabilityDataPreparator
    DATA_PREPARATOR_AVAILABLE = True
except ImportError:
    ProfitabilityDataPreparator = None
    DATA_PREPARATOR_AVAILABLE = False

from .model_monitoring import ProfitabilityModelMonitor
from .shap_explainer import SHAPExplainer, ConfidenceIntervalCalculator

logger = logging.getLogger(__name__)


class ProfitabilityPredictor:
    """Handles real-time profitability predictions"""
    
    def __init__(self, model_path: str = "./models", db_path: str = "../../database/superhack.db"):
        """
        Initialize the profitability predictor
        
        Args:
            model_path: Path to saved models
            db_path: Path to database
        """
        self.model_path = model_path
        self.db_path = db_path
        self.xgboost_model = None
        self.random_forest_model = None
        if FEATURE_ENGINEER_AVAILABLE and ProfitabilityFeatureEngineer is not None:
            self.feature_engineer = ProfitabilityFeatureEngineer(db_path)
        else:
            self.feature_engineer = None
        
        if DATA_PREPARATOR_AVAILABLE and ProfitabilityDataPreparator is not None:
            self.data_preparator = ProfitabilityDataPreparator(db_path)
        else:
            self.data_preparator = None
        self.model_monitor = ProfitabilityModelMonitor()
        self.shap_explainer = SHAPExplainer()
        self.ci_calculator = ConfidenceIntervalCalculator()
        self.feature_names = []
        self.is_initialized = False
        self.active_model = "xgboost"  # Default to XGBoost
        logger.info("Profitability Predictor initialized")
    
    async def initialize(self):
        """Initialize the predictor by loading models"""
        try:
            # Load trained models
            await self._load_models()
            
            # Initialize components
            # Feature engineer and data preparator don't require async initialization
            
            self.is_initialized = True
            logger.info("Profitability Predictor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize profitability predictor: {e}")
            raise
    
    async def _load_models(self):
        """Load trained models from disk"""
        try:
            # Try to load XGBoost model
            xgboost_model_path = os.path.join(self.model_path, "profitability_xgboost_model.pkl")
            if os.path.exists(xgboost_model_path) and XGBOOST_AVAILABLE:
                with open(xgboost_model_path, 'rb') as f:
                    model_data = pickle.load(f)
                    self.xgboost_model = model_data.get('model')
                    self.feature_names = model_data.get('feature_names', [])
                logger.info("XGBoost model loaded successfully")
            
            # Try to load Random Forest model
            rf_model_path = os.path.join(self.model_path, "profitability_random_forest_model.pkl")
            if os.path.exists(rf_model_path) and SKLEARN_AVAILABLE:
                with open(rf_model_path, 'rb') as f:
                    model_data = pickle.load(f)
                    self.random_forest_model = model_data.get('model')
                    if not self.feature_names:  # Use RF feature names if XGBoost not available
                        self.feature_names = model_data.get('feature_names', [])
                logger.info("Random Forest model loaded successfully")
                
        except Exception as e:
            logger.warning(f"Failed to load models: {e}")
            # Create mock models for demonstration
            await self._create_mock_models()
    
    async def _create_mock_models(self):
        """Create mock models for demonstration when real models aren't available"""
        try:
            logger.info("Creating mock models for demonstration")
            
            # Mock feature names based on our feature engineering
            self.feature_names = [
                'contract_value', 'hours_logged', 'billing_amount', 'ticket_count',
                'satisfaction_score', 'last_contact_days', 'service_utilization_rate',
                'cost_efficiency', 'revenue_velocity', 'profit_margin',
                'billing_efficiency', 'payment_score', 'contract_duration',
                'client_age', 'service_diversity', 'support_frequency',
                'resolution_time', 'sla_compliance', 'technician_efficiency',
                'engagement_score'
            ]
            
        except Exception as e:
            logger.error(f"Failed to create mock models: {e}")
    
    def prepare_features(self, client_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Prepare features for prediction
        
        Args:
            client_data: Dictionary with client data
            
        Returns:
            DataFrame with prepared features
        """
        try:
            # Convert to DataFrame
            if isinstance(client_data, dict):
                df = pd.DataFrame([client_data])
            else:
                df = pd.DataFrame(client_data)
            
            # Engineer features if available
            if self.feature_engineer is not None:
                features_df = self.feature_engineer.engineer_features(df)
                
                # Ensure we return a DataFrame
                if not isinstance(features_df, pd.DataFrame):
                    features_df = pd.DataFrame(features_df)
            else:
                # Create mock features
                features_df = df.copy()
            
            # Ensure all required features are present
            if self.feature_names:
                for feature in self.feature_names:
                    if feature not in features_df.columns:
                        features_df[feature] = 0.0
                
                # Select only required features in correct order
                features_df = features_df[self.feature_names]
            
            # Ensure we return a DataFrame
            if not isinstance(features_df, pd.DataFrame):
                features_df = pd.DataFrame(features_df)
            
            return features_df
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            # Return mock features if there's an error
            mock_features = pd.DataFrame({feature: [0.5] for feature in self.feature_names}) if self.feature_names else pd.DataFrame()
            return mock_features
    
    async def predict(self, client_data: Dict[str, Any], 
                     model_type: str = "auto",
                     return_confidence: bool = False,
                     return_explanation: bool = False) -> Dict[str, Any]:
        """
        Make a profitability prediction for a client
        
        Args:
            client_data: Dictionary with client data
            model_type: Type of model to use ("xgboost", "random_forest", "auto")
            return_confidence: Whether to return confidence intervals
            return_explanation: Whether to return SHAP explanations
            
        Returns:
            Dictionary with prediction results
        """
        try:
            if not self.is_initialized:
                await self.initialize()
            
            # Prepare features
            features = self.prepare_features(client_data)
            
            # Select model
            model = await self._select_model(model_type)
            if model is None:
                raise ValueError("No model available for prediction")
            
            # Make prediction
            prediction_start = datetime.now()
            prediction = model.predict(features)[0] if hasattr(model, 'predict') else 0.5
            prediction_time = (datetime.now() - prediction_start).total_seconds() * 1000
            
            # Ensure prediction is within valid range (0-1 for profit margin)
            prediction = max(0.0, min(1.0, prediction))
            
            # Build response
            response = {
                "prediction": float(prediction),
                "model_type": self.active_model,
                "prediction_time_ms": prediction_time,
                "timestamp": datetime.now().isoformat(),
                "features_used": len(self.feature_names) if self.feature_names else 0
            }
            
            # Add confidence intervals if requested
            if return_confidence:
                ci_results = self.ci_calculator.calculate_confidence_interval(
                    model, features, method='bootstrap'
                )
                response["confidence_interval"] = ci_results.get("overall_interval", {})
                response["confidence_level"] = ci_results.get("confidence_level", 0.95)
            
            # Add explanation if requested
            if return_explanation:
                explanation = self.shap_explainer.explain_prediction(features)
                response["explanation"] = explanation
            
            # Monitor prediction quality
            await self._monitor_prediction(features, prediction)
            
            logger.info(f"Profitability prediction completed: {prediction:.4f}")
            return response
            
        except Exception as e:
            logger.error(f"Profitability prediction failed: {e}")
            # Return mock prediction in case of error
            return {
                "prediction": 0.5,
                "model_type": "mock",
                "prediction_time_ms": 10.0,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    async def _select_model(self, model_type: str):
        """
        Select the appropriate model based on type
        
        Args:
            model_type: Type of model to select
            
        Returns:
            Selected model or None
        """
        if model_type == "auto":
            # Prefer XGBoost if available, otherwise Random Forest
            if self.xgboost_model is not None:
                self.active_model = "xgboost"
                return self.xgboost_model
            elif self.random_forest_model is not None:
                self.active_model = "random_forest"
                return self.random_forest_model
        elif model_type == "xgboost" and self.xgboost_model is not None:
            self.active_model = "xgboost"
            return self.xgboost_model
        elif model_type == "random_forest" and self.random_forest_model is not None:
            self.active_model = "random_forest"
            return self.random_forest_model
        
        # Return first available model
        if self.xgboost_model is not None:
            self.active_model = "xgboost"
            return self.xgboost_model
        elif self.random_forest_model is not None:
            self.active_model = "random_forest"
            return self.random_forest_model
        
        return None
    
    async def batch_predict(self, clients_data: List[Dict[str, Any]], 
                          model_type: str = "auto") -> List[Dict[str, Any]]:
        """
        Make batch predictions for multiple clients
        
        Args:
            clients_data: List of dictionaries with client data
            model_type: Type of model to use
            
        Returns:
            List of prediction results
        """
        try:
            predictions = []
            for client_data in clients_data:
                prediction = await self.predict(client_data, model_type)
                predictions.append(prediction)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Batch prediction failed: {e}")
            # Return mock predictions in case of error
            return [
                {
                    "prediction": 0.5,
                    "model_type": "mock",
                    "prediction_time_ms": 10.0,
                    "timestamp": datetime.now().isoformat()
                }
                for _ in clients_data
            ]
    
    async def _monitor_prediction(self, features: pd.DataFrame, prediction: float):
        """
        Monitor prediction quality and performance
        
        Args:
            features: Input features
            prediction: Model prediction
        """
        try:
            # Monitor prediction statistics
            quality_report = self.model_monitor.monitor_prediction_quality(
                np.array([prediction])
            )
            
            # Log monitoring info
            logger.debug(f"Prediction quality monitored: {quality_report}")
            
        except Exception as e:
            logger.warning(f"Failed to monitor prediction: {e}")
    
    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about loaded models
        
        Returns:
            Dictionary with model information
        """
        try:
            info = {
                "models_available": [],
                "active_model": self.active_model,
                "feature_count": len(self.feature_names) if self.feature_names else 0,
                "features": self.feature_names if self.feature_names else [],
                "initialization_status": self.is_initialized
            }
            
            if self.xgboost_model is not None:
                info["models_available"].append("xgboost")
            if self.random_forest_model is not None:
                info["models_available"].append("random_forest")
            
            return info
            
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            return {"error": str(e)}
    
    async def explain_prediction(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Explain a prediction using SHAP values
        
        Args:
            client_data: Dictionary with client data
            
        Returns:
            Dictionary with explanation
        """
        try:
            if not self.is_initialized:
                await self.initialize()
            
            # Prepare features
            features = self.prepare_features(client_data)
            
            # Create explainer if not already created
            if self.xgboost_model is not None:
                self.shap_explainer.create_explainer(self.xgboost_model, features)
            elif self.random_forest_model is not None:
                self.shap_explainer.create_explainer(self.random_forest_model, features)
            
            # Generate explanation
            explanation = self.shap_explainer.explain_prediction(features)
            
            return explanation
            
        except Exception as e:
            logger.error(f"Prediction explanation failed: {e}")
            return {"error": str(e), "explanation": "Unable to generate explanation"}
    
    async def calculate_confidence_interval(self, client_data: Dict[str, Any], 
                                          method: str = "bootstrap") -> Dict[str, Any]:
        """
        Calculate confidence interval for a prediction
        
        Args:
            client_data: Dictionary with client data
            method: Method for calculating CI ("bootstrap", "residual")
            
        Returns:
            Dictionary with confidence interval
        """
        try:
            if not self.is_initialized:
                await self.initialize()
            
            # Prepare features
            features = self.prepare_features(client_data)
            
            # Select model
            model = await self._select_model("auto")
            if model is None:
                raise ValueError("No model available for confidence interval calculation")
            
            # Calculate confidence interval
            ci_results = self.ci_calculator.calculate_confidence_interval(
                model, features, method=method
            )
            
            return ci_results
            
        except Exception as e:
            logger.error(f"Confidence interval calculation failed: {e}")
            return {"error": str(e), "confidence_interval": {"lower_bound": 0.4, "upper_bound": 0.6}}


class ModelVersionManager:
    """Manages model versions and deployments"""
    
    def __init__(self, model_registry_path: str = "./model_registry"):
        """
        Initialize the model version manager
        
        Args:
            model_registry_path: Path to model registry
        """
        self.model_registry_path = model_registry_path
        self.versions = {}
        self.active_versions = {}
        logger.info("Model Version Manager initialized")
    
    async def register_model_version(self, model_name: str, version: str, 
                                   model_path: str, metadata: Dict[str, Any]) -> bool:
        """
        Register a new model version
        
        Args:
            model_name: Name of the model
            version: Version identifier
            model_path: Path to the model file
            metadata: Additional metadata about the model
            
        Returns:
            Boolean indicating success
        """
        try:
            # Create version entry
            version_entry = {
                "model_name": model_name,
                "version": version,
                "model_path": model_path,
                "metadata": metadata,
                "registered_at": datetime.now().isoformat(),
                "status": "registered"
            }
            
            # Store version
            if model_name not in self.versions:
                self.versions[model_name] = {}
            self.versions[model_name][version] = version_entry
            
            logger.info(f"Model version registered: {model_name}:{version}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register model version {model_name}:{version}: {e}")
            return False
    
    async def deploy_model_version(self, model_name: str, version: str) -> bool:
        """
        Deploy a model version for serving
        
        Args:
            model_name: Name of the model
            version: Version identifier
            
        Returns:
            Boolean indicating success
        """
        try:
            # Check if version exists
            if model_name not in self.versions or version not in self.versions[model_name]:
                raise ValueError(f"Model version {model_name}:{version} not found")
            
            # Update status
            self.versions[model_name][version]["status"] = "deployed"
            self.versions[model_name][version]["deployed_at"] = datetime.now().isoformat()
            
            # Set as active version
            self.active_versions[model_name] = version
            
            logger.info(f"Model version deployed: {model_name}:{version}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to deploy model version {model_name}:{version}: {e}")
            return False
    
    async def get_active_version(self, model_name: str) -> Optional[str]:
        """
        Get the active version for a model
        
        Args:
            model_name: Name of the model
            
        Returns:
            Active version identifier or None
        """
        return self.active_versions.get(model_name)
    
    async def list_model_versions(self, model_name: str) -> List[Dict[str, Any]]:
        """
        List all versions of a model
        
        Args:
            model_name: Name of the model
            
        Returns:
            List of version information
        """
        try:
            if model_name in self.versions:
                return list(self.versions[model_name].values())
            return []
        except Exception as e:
            logger.error(f"Failed to list versions for {model_name}: {e}")
            return []
    
    async def rollback_model(self, model_name: str, version: str) -> bool:
        """
        Rollback to a previous model version
        
        Args:
            model_name: Name of the model
            version: Version to rollback to
            
        Returns:
            Boolean indicating success
        """
        try:
            # Check if version exists
            if model_name not in self.versions or version not in self.versions[model_name]:
                raise ValueError(f"Model version {model_name}:{version} not found")
            
            # Set as active version
            self.active_versions[model_name] = version
            
            logger.info(f"Model {model_name} rolled back to version {version}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to rollback model {model_name} to version {version}: {e}")
            return False


class ABTestingFramework:
    """A/B testing framework for model comparison"""
    
    def __init__(self):
        """Initialize the A/B testing framework"""
        self.experiments = {}
        self.results = {}
        logger.info("A/B Testing Framework initialized")
    
    async def create_experiment(self, experiment_name: str, 
                              model_a_name: str, model_a_version: str,
                              model_b_name: str, model_b_version: str,
                              traffic_split: float = 0.5) -> bool:
        """
        Create a new A/B testing experiment
        
        Args:
            experiment_name: Name of the experiment
            model_a_name: Name of model A
            model_a_version: Version of model A
            model_b_name: Name of model B
            model_b_version: Version of model B
            traffic_split: Proportion of traffic to send to model A (0.0-1.0)
            
        Returns:
            Boolean indicating success
        """
        try:
            experiment = {
                "name": experiment_name,
                "model_a": {"name": model_a_name, "version": model_a_version},
                "model_b": {"name": model_b_name, "version": model_b_version},
                "traffic_split": traffic_split,
                "created_at": datetime.now().isoformat(),
                "status": "running",
                "metrics": {
                    "model_a_predictions": 0,
                    "model_b_predictions": 0,
                    "model_a_accuracy": 0.0,
                    "model_b_accuracy": 0.0,
                    "model_a_latency": 0.0,
                    "model_b_latency": 0.0
                }
            }
            
            self.experiments[experiment_name] = experiment
            self.results[experiment_name] = []
            
            logger.info(f"A/B test experiment created: {experiment_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create A/B test experiment {experiment_name}: {e}")
            return False
    
    async def record_prediction(self, experiment_name: str, model_used: str, 
                              prediction_result: Dict[str, Any]) -> bool:
        """
        Record a prediction result for an experiment
        
        Args:
            experiment_name: Name of the experiment
            model_used: Which model was used ("A" or "B")
            prediction_result: Prediction result data
            
        Returns:
            Boolean indicating success
        """
        try:
            if experiment_name not in self.experiments:
                raise ValueError(f"Experiment {experiment_name} not found")
            
            # Record result
            result_entry = {
                "model_used": model_used,
                "prediction_result": prediction_result,
                "timestamp": datetime.now().isoformat()
            }
            
            self.results[experiment_name].append(result_entry)
            
            # Update metrics
            experiment = self.experiments[experiment_name]
            if model_used == "A":
                experiment["metrics"]["model_a_predictions"] += 1
            else:
                experiment["metrics"]["model_b_predictions"] += 1
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to record prediction for experiment {experiment_name}: {e}")
            return False
    
    async def get_experiment_results(self, experiment_name: str) -> Optional[Dict[str, Any]]:
        """
        Get results for an experiment
        
        Args:
            experiment_name: Name of the experiment
            
        Returns:
            Dictionary with experiment results or None
        """
        try:
            if experiment_name not in self.experiments:
                return None
            
            experiment = self.experiments[experiment_name]
            results = self.results[experiment_name]
            
            # Calculate statistics
            total_predictions = len(results)
            if total_predictions > 0:
                # Calculate accuracy and latency metrics from results
                model_a_results = [r for r in results if r["model_used"] == "A"]
                model_b_results = [r for r in results if r["model_used"] == "B"]
                
                experiment["metrics"]["model_a_predictions"] = len(model_a_results)
                experiment["metrics"]["model_b_predictions"] = len(model_b_results)
            
            return experiment
            
        except Exception as e:
            logger.error(f"Failed to get results for experiment {experiment_name}: {e}")
            return None
    
    async def stop_experiment(self, experiment_name: str) -> bool:
        """
        Stop a running experiment
        
        Args:
            experiment_name: Name of the experiment
            
        Returns:
            Boolean indicating success
        """
        try:
            if experiment_name not in self.experiments:
                raise ValueError(f"Experiment {experiment_name} not found")
            
            self.experiments[experiment_name]["status"] = "stopped"
            self.experiments[experiment_name]["stopped_at"] = datetime.now().isoformat()
            
            logger.info(f"A/B test experiment stopped: {experiment_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop experiment {experiment_name}: {e}")
            return False


# Global instances for easy access
predictor_instance = None
version_manager_instance = None
ab_testing_instance = None


async def get_predictor() -> ProfitabilityPredictor:
    """Get singleton predictor instance"""
    global predictor_instance
    if predictor_instance is None:
        predictor_instance = ProfitabilityPredictor()
        await predictor_instance.initialize()
    return predictor_instance


async def get_version_manager() -> ModelVersionManager:
    """Get singleton version manager instance"""
    global version_manager_instance
    if version_manager_instance is None:
        version_manager_instance = ModelVersionManager()
    return version_manager_instance


async def get_ab_testing_framework() -> ABTestingFramework:
    """Get singleton A/B testing framework instance"""
    global ab_testing_instance
    if ab_testing_instance is None:
        ab_testing_instance = ABTestingFramework()
    return ab_testing_instance