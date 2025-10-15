"""
Logging Configuration
Centralized logging setup for the AI/ML system
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from config import settings

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)


def setup_logging(
    level: str = None,
    log_file: str = None,
    max_size: str = "10MB",
    backup_count: int = 5,
    include_console: bool = True
) -> None:
    """
    Set up logging configuration for the application
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        max_size: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        include_console: Whether to include console logging
    """
    try:
        # Use settings if not provided
        if level is None:
            level = settings.logging.level
        if log_file is None:
            log_file = settings.logging.file
        
        # Convert level string to logging constant
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(numeric_level)
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Console handler
        if include_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(numeric_level)
            console_handler.setFormatter(simple_formatter)
            root_logger.addHandler(console_handler)
        
        # File handler with rotation
        if log_file:
            # Parse max_size (e.g., "10MB" -> 10 * 1024 * 1024)
            size_bytes = _parse_size(max_size)
            
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file,
                maxBytes=size_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(detailed_formatter)
            root_logger.addHandler(file_handler)
        
        # Set specific logger levels
        _configure_logger_levels()
        
        # Log successful setup
        logger = logging.getLogger(__name__)
        logger.info(f"Logging configured - Level: {level}, File: {log_file}")
        
    except Exception as e:
        print(f"Failed to setup logging: {e}", file=sys.stderr)
        # Fallback to basic logging
        logging.basicConfig(level=logging.INFO)


def _parse_size(size_str: str) -> int:
    """Parse size string like '10MB' to bytes"""
    try:
        size_str = size_str.upper()
        if size_str.endswith('KB'):
            return int(float(size_str[:-2]) * 1024)
        elif size_str.endswith('MB'):
            return int(float(size_str[:-2]) * 1024 * 1024)
        elif size_str.endswith('GB'):
            return int(float(size_str[:-2]) * 1024 * 1024 * 1024)
        else:
            return int(float(size_str))
    except (ValueError, AttributeError):
        return 10 * 1024 * 1024  # Default to 10MB


def _configure_logger_levels():
    """Configure specific logger levels"""
    # Reduce noise from third-party libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
    
    # Set our loggers to INFO by default
    logging.getLogger('src').setLevel(logging.INFO)
    logging.getLogger('src.api').setLevel(logging.INFO)
    logging.getLogger('src.data').setLevel(logging.INFO)
    logging.getLogger('src.models').setLevel(logging.INFO)
    logging.getLogger('src.utils').setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(name)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        return logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)


def log_function_call(func):
    """Decorator to log function calls"""
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed with error: {e}")
            raise
    return wrapper


def log_async_function_call(func):
    """Decorator to log async function calls"""
    async def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Calling async {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = await func(*args, **kwargs)
            logger.debug(f"Async {func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Async {func.__name__} failed with error: {e}")
            raise
    return wrapper


class StructuredLogger:
    """Structured logging for better log analysis"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def log_event(self, event: str, level: str = "INFO", **kwargs):
        """Log a structured event"""
        log_data = {
            "event": event,
            "timestamp": logging.Formatter().formatTime(logging.LogRecord(
                name="", level=0, pathname="", lineno=0, msg="", args=(), exc_info=None
            )),
            **kwargs
        }
        
        log_message = f"EVENT: {event} | DATA: {log_data}"
        
        if level.upper() == "DEBUG":
            self.logger.debug(log_message)
        elif level.upper() == "INFO":
            self.logger.info(log_message)
        elif level.upper() == "WARNING":
            self.logger.warning(log_message)
        elif level.upper() == "ERROR":
            self.logger.error(log_message)
        elif level.upper() == "CRITICAL":
            self.logger.critical(log_message)
        else:
            self.logger.info(log_message)
    
    def log_prediction(self, model_name: str, prediction_id: str, 
                      processing_time_ms: float, **kwargs):
        """Log a prediction event"""
        self.log_event(
            "prediction",
            level="INFO",
            model_name=model_name,
            prediction_id=prediction_id,
            processing_time_ms=processing_time_ms,
            **kwargs
        )
    
    def log_model_deployment(self, model_name: str, version: str, 
                           deployment_id: str, **kwargs):
        """Log a model deployment event"""
        self.log_event(
            "model_deployment",
            level="INFO",
            model_name=model_name,
            version=version,
            deployment_id=deployment_id,
            **kwargs
        )
    
    def log_error(self, error_type: str, error_message: str, 
                 context: dict = None, **kwargs):
        """Log an error event"""
        self.log_event(
            "error",
            level="ERROR",
            error_type=error_type,
            error_message=error_message,
            context=context or {},
            **kwargs
        )
