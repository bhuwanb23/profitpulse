"""
Forecasting Models for Service Demand Forecaster
Implements LSTM neural network, ARIMA, Prophet, and seasonal decomposition algorithms
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Try to import machine learning libraries
try:
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    MinMaxScaler = None
    logging.warning("Scikit-learn not available, some features will be limited")

# Try to import deep learning libraries
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    Sequential = None
    LSTM = None
    Dense = None
    Dropout = None
    logging.warning("TensorFlow not available, LSTM features will be limited")

# Try to import statistical libraries
try:
    from statsmodels.tsa.arima.model import ARIMA as StatsARIMA
    from statsmodels.tsa.seasonal import seasonal_decompose
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    StatsARIMA = None
    seasonal_decompose = None
    logging.warning("Statsmodels not available, ARIMA and seasonal decomposition features will be limited")

logger = logging.getLogger(__name__)


class LSTMForecaster:
    """LSTM neural network forecaster for demand prediction"""
    
    def __init__(self, sequence_length: int = 60, epochs: int = 50, batch_size: int = 32):
        """
        Initialize LSTM forecaster
        
        Args:
            sequence_length: Number of time steps to look back
            epochs: Number of training epochs
            batch_size: Batch size for training
        """
        self.sequence_length = sequence_length
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1)) if SKLEARN_AVAILABLE and MinMaxScaler else None
        self.available = TENSORFLOW_AVAILABLE and SKLEARN_AVAILABLE
        logger.info("LSTM Forecaster initialized")
    
    def prepare_data(self, data: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare data for LSTM training
        
        Args:
            data: Time series data
            
        Returns:
            Tuple of (X, y) arrays for training
        """
        if not self.available:
            logger.warning("Required libraries not available for LSTM")
            return np.array([]), np.array([])
        
        # Scale the data
        if self.scaler is not None:
            scaled_data = self.scaler.fit_transform(data.values.astype(float).reshape(-1, 1))
        else:
            scaled_data = data.values.astype(float).reshape(-1, 1)
        
        # Create sequences
        X, y = [], []
        for i in range(self.sequence_length, len(scaled_data)):
            X.append(scaled_data[i-self.sequence_length:i, 0])
            y.append(scaled_data[i, 0])
        
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape: Tuple[int, int]) -> Any:
        """
        Build LSTM model
        
        Args:
            input_shape: Shape of input data
            
        Returns:
            Compiled LSTM model
        """
        if not self.available:
            logger.warning("TensorFlow not available for LSTM model building")
            return None
        
        if Sequential and LSTM and Dropout and Dense:
            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=input_shape),
                Dropout(0.2),
                LSTM(50, return_sequences=False),
                Dropout(0.2),
                Dense(25),
                Dense(1)
            ])
        else:
            model = None
        
        if model is not None:
            model.compile(optimizer='adam', loss='mean_squared_error')
        return model
    
    def train(self, data: pd.Series) -> Dict[str, Any]:
        """
        Train LSTM model on time series data
        
        Args:
            data: Time series data for training
            
        Returns:
            Dictionary with training results
        """
        if not self.available:
            logger.warning("Required libraries not available for LSTM training")
            return {
                'success': False,
                'message': 'Required libraries not available',
                'model': None
            }
        
        try:
            # Prepare data
            X, y = self.prepare_data(data)
            
            if len(X) == 0:
                return {
                    'success': False,
                    'message': 'Insufficient data for training',
                    'model': None
                }
            
            # Reshape data for LSTM
            X = np.reshape(X, (X.shape[0], X.shape[1], 1))
            
            # Build model
            self.model = self.build_model((X.shape[1], 1))
            
            # Train model
            history = self.model.fit(
                X, y,
                batch_size=self.batch_size,
                epochs=self.epochs,
                verbose=0
            )
            
            logger.info("LSTM model training completed")
            return {
                'success': True,
                'message': 'Training completed',
                'model': self.model,
                'training_history': history.history
            }
            
        except Exception as e:
            logger.error(f"Error training LSTM model: {e}")
            return {
                'success': False,
                'message': f'Training error: {str(e)}',
                'model': None
            }
    
    def predict(self, data: pd.Series, steps: int = 30) -> Dict[str, Any]:
        """
        Make predictions using trained LSTM model
        
        Args:
            data: Time series data for prediction
            steps: Number of steps to predict
            
        Returns:
            Dictionary with predictions
        """
        if not self.available or self.model is None:
            logger.warning("LSTM model not available for prediction")
            return {
                'success': False,
                'message': 'Model not trained or available',
                'predictions': []
            }
        
        try:
            # Prepare last sequence
            last_sequence = data.values[-self.sequence_length:]
            if self.scaler is not None:
                last_sequence_scaled = self.scaler.transform(last_sequence.astype(float).reshape(-1, 1))
            else:
                last_sequence_scaled = last_sequence.astype(float).reshape(-1, 1)
            
            # Make predictions
            predictions = []
            current_sequence = last_sequence_scaled.reshape(1, -1)
            
            for _ in range(steps):
                # Predict next value
                next_pred = self.model.predict(current_sequence.reshape(1, self.sequence_length, 1), verbose=0)
                predictions.append(next_pred[0, 0])
                
                # Update sequence
                current_sequence = np.append(current_sequence[:, 1:], next_pred[0, 0]).reshape(1, -1)
            
            # Inverse transform predictions
            predictions = np.array(predictions).reshape(-1, 1)
            if self.scaler is not None:
                predictions = self.scaler.inverse_transform(predictions).flatten()
            else:
                predictions = predictions.flatten()
            
            logger.info(f"LSTM prediction completed for {steps} steps")
            return {
                'success': True,
                'message': 'Prediction completed',
                'predictions': predictions.tolist(),
                'prediction_steps': steps
            }
            
        except Exception as e:
            logger.error(f"Error making LSTM predictions: {e}")
            return {
                'success': False,
                'message': f'Prediction error: {str(e)}',
                'predictions': []
            }


class ARIMAForecaster:
    """ARIMA forecaster for demand prediction"""
    
    def __init__(self, order: Tuple[int, int, int] = (1, 1, 1)):
        """
        Initialize ARIMA forecaster
        
        Args:
            order: (p, d, q) order for ARIMA model
        """
        self.order = order
        self.model = None
        self.available = STATSMODELS_AVAILABLE
        logger.info("ARIMA Forecaster initialized")
    
    def train(self, data: pd.Series) -> Dict[str, Any]:
        """
        Train ARIMA model on time series data
        
        Args:
            data: Time series data for training
            
        Returns:
            Dictionary with training results
        """
        if not self.available:
            logger.warning("Statsmodels not available for ARIMA training")
            return {
                'success': False,
                'message': 'Statsmodels not available',
                'model': None
            }
        
        try:
            # Fit ARIMA model
            if StatsARIMA:
                self.model = StatsARIMA(data, order=self.order)
            else:
                self.model = None
            if self.model is not None:
                fitted_model = self.model.fit()
            else:
                fitted_model = None
            
            logger.info("ARIMA model training completed")
            return {
                'success': True,
                'message': 'Training completed',
                'model': fitted_model,
                'aic': fitted_model.aic if fitted_model is not None else None,
                'bic': fitted_model.bic if fitted_model is not None else None
            }
            
        except Exception as e:
            logger.error(f"Error training ARIMA model: {e}")
            return {
                'success': False,
                'message': f'Training error: {str(e)}',
                'model': None
            }
    
    def predict(self, steps: int = 30) -> Dict[str, Any]:
        """
        Make predictions using trained ARIMA model
        
        Args:
            steps: Number of steps to predict
            
        Returns:
            Dictionary with predictions
        """
        if not self.available or self.model is None:
            logger.warning("ARIMA model not available for prediction")
            return {
                'success': False,
                'message': 'Model not trained or available',
                'predictions': []
            }
        
        try:
            # Make predictions
            forecast = self.model.forecast(steps=steps)
            
            logger.info(f"ARIMA prediction completed for {steps} steps")
            return {
                'success': True,
                'message': 'Prediction completed',
                'predictions': forecast.tolist(),
                'prediction_steps': steps
            }
            
        except Exception as e:
            logger.error(f"Error making ARIMA predictions: {e}")
            return {
                'success': False,
                'message': f'Prediction error: {str(e)}',
                'predictions': []
            }


class ProphetForecaster:
    """Prophet forecaster for demand prediction"""
    
    def __init__(self):
        """Initialize Prophet forecaster"""
        self.model = None
        self.available = False
        
        # Try to import Prophet
        try:
            from prophet import Prophet
            self.Prophet = Prophet
            self.available = True
            logger.info("Prophet Forecaster initialized")
        except ImportError:
            logger.warning("Prophet not available, Prophet features will be limited")
    
    def train(self, data: pd.DataFrame, date_column: str = 'ds', value_column: str = 'y') -> Dict[str, Any]:
        """
        Train Prophet model on time series data
        
        Args:
            data: DataFrame with time series data
            date_column: Name of date column
            value_column: Name of value column
            
        Returns:
            Dictionary with training results
        """
        if not self.available:
            logger.warning("Prophet not available for training")
            return {
                'success': False,
                'message': 'Prophet not available',
                'model': None
            }
        
        try:
            # Prepare data for Prophet
            prophet_data = data[[date_column, value_column]].copy()
            prophet_data.columns = ['ds', 'y']
            
            # Convert date column to datetime
            prophet_data['ds'] = pd.to_datetime(prophet_data['ds'])
            
            # Fit Prophet model
            self.model = self.Prophet()
            self.model.fit(prophet_data)
            
            logger.info("Prophet model training completed")
            return {
                'success': True,
                'message': 'Training completed',
                'model': self.model
            }
            
        except Exception as e:
            logger.error(f"Error training Prophet model: {e}")
            return {
                'success': False,
                'message': f'Training error: {str(e)}',
                'model': None
            }
    
    def predict(self, periods: int = 30) -> Dict[str, Any]:
        """
        Make predictions using trained Prophet model
        
        Args:
            periods: Number of periods to predict
            
        Returns:
            Dictionary with predictions
        """
        if not self.available or self.model is None:
            logger.warning("Prophet model not available for prediction")
            return {
                'success': False,
                'message': 'Model not trained or available',
                'predictions': [],
                'forecast': None
            }
        
        try:
            # Create future dataframe
            future = self.model.make_future_dataframe(periods=periods)
            
            # Make predictions
            forecast = self.model.predict(future)
            
            # Extract predictions for future periods
            future_predictions = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
            
            logger.info(f"Prophet prediction completed for {periods} periods")
            return {
                'success': True,
                'message': 'Prediction completed',
                'predictions': future_predictions['yhat'].tolist(),
                'forecast': future_predictions.to_dict('records'),
                'prediction_periods': periods
            }
            
        except Exception as e:
            logger.error(f"Error making Prophet predictions: {e}")
            return {
                'success': False,
                'message': f'Prediction error: {str(e)}',
                'predictions': [],
                'forecast': None
            }


class SeasonalDecomposer:
    """Seasonal decomposition for time series analysis"""
    
    def __init__(self, model: str = 'additive', period: Optional[int] = None):
        """
        Initialize seasonal decomposer
        
        Args:
            model: Type of seasonal decomposition ('additive' or 'multiplicative')
            period: Period of the series (None for automatic detection)
        """
        self.model = model
        self.period = period
        self.available = STATSMODELS_AVAILABLE
        logger.info("Seasonal Decomposer initialized")
    
    def decompose(self, data: pd.Series) -> Dict[str, Any]:
        """
        Perform seasonal decomposition on time series data
        
        Args:
            data: Time series data for decomposition
            
        Returns:
            Dictionary with decomposition results
        """
        if not self.available:
            logger.warning("Statsmodels not available for seasonal decomposition")
            return {
                'success': False,
                'message': 'Statsmodels not available',
                'trend': None,
                'seasonal': None,
                'residual': None,
                'observed': None
            }
        
        try:
            # Perform seasonal decomposition
            if seasonal_decompose:
                decomposition = seasonal_decompose(data, model=self.model, period=self.period)
            else:
                decomposition = None
            
            logger.info("Seasonal decomposition completed")
            return {
                'success': True,
                'message': 'Decomposition completed',
                'trend': decomposition.trend.tolist() if decomposition is not None else None,
                'seasonal': decomposition.seasonal.tolist() if decomposition is not None else None,
                'residual': decomposition.resid.tolist() if decomposition is not None else None,
                'observed': decomposition.observed.tolist() if decomposition is not None else None
            }
            
        except Exception as e:
            logger.error(f"Error in seasonal decomposition: {e}")
            return {
                'success': False,
                'message': f'Decomposition error: {str(e)}',
                'trend': None,
                'seasonal': None,
                'residual': None,
                'observed': None
            }


# Global instances for easy access
lstm_forecaster_instance = None
arima_forecaster_instance = None
prophet_forecaster_instance = None
seasonal_decomposer_instance = None


def get_lstm_forecaster(sequence_length: int = 60, epochs: int = 50, batch_size: int = 32) -> LSTMForecaster:
    """Get singleton LSTM forecaster instance"""
    global lstm_forecaster_instance
    if lstm_forecaster_instance is None:
        lstm_forecaster_instance = LSTMForecaster(sequence_length, epochs, batch_size)
    return lstm_forecaster_instance


def get_arima_forecaster(order: Tuple[int, int, int] = (1, 1, 1)) -> ARIMAForecaster:
    """Get singleton ARIMA forecaster instance"""
    global arima_forecaster_instance
    if arima_forecaster_instance is None:
        arima_forecaster_instance = ARIMAForecaster(order)
    return arima_forecaster_instance


def get_prophet_forecaster() -> ProphetForecaster:
    """Get singleton Prophet forecaster instance"""
    global prophet_forecaster_instance
    if prophet_forecaster_instance is None:
        prophet_forecaster_instance = ProphetForecaster()
    return prophet_forecaster_instance


def get_seasonal_decomposer(model: str = 'additive', period: Optional[int] = None) -> SeasonalDecomposer:
    """Get singleton seasonal decomposer instance"""
    global seasonal_decomposer_instance
    if seasonal_decomposer_instance is None:
        seasonal_decomposer_instance = SeasonalDecomposer(model, period)
    return seasonal_decomposer_instance