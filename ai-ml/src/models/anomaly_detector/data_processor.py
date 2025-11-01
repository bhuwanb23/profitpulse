"""
Data Stream Processor for Anomaly Detection
Handles real-time data processing, feature extraction, and quality monitoring
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
from collections import deque
import asyncio
from functools import lru_cache

logger = logging.getLogger(__name__)


class DataProcessorConfig:
    """Configuration for data processor"""
    def __init__(self,
                 window_size: int = 100,
                 quality_threshold: float = 0.8,
                 enable_quality_monitoring: bool = True,
                 enable_feature_extraction: bool = True,
                 batch_size: int = 10,
                 enable_caching: bool = True):
        self.window_size = window_size
        self.quality_threshold = quality_threshold
        self.enable_quality_monitoring = enable_quality_monitoring
        self.enable_feature_extraction = enable_feature_extraction
        self.batch_size = batch_size
        self.enable_caching = enable_caching


class DataQualityMonitor:
    """Monitors data quality in real-time streams"""
    
    def __init__(self, config: DataProcessorConfig):
        self.config = config
        self.metrics = {
            'missing_values': 0,
            'outliers': 0,
            'duplicates': 0,
            'total_records': 0,
            'quality_score': 1.0
        }
        self.quality_history = deque(maxlen=config.window_size)
        # Batch processing optimization
        self.batch_buffer = []
        self.batch_counter = 0
        logger.info("DataQualityMonitor initialized")
    
    def assess_data_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess quality of incoming data"""
        try:
            quality_metrics = {
                'timestamp': datetime.now().isoformat(),
                'missing_values': 0,
                'outliers': 0,
                'duplicates': 0,
                'total_fields': len(data),
                'filled_fields': sum(1 for v in data.values() if v is not None and v != ''),
                'quality_score': 0.0
            }
            
            # Check for missing values
            missing_count = sum(1 for v in data.values() if v is None or v == '')
            quality_metrics['missing_values'] = missing_count
            
            # Check for obvious outliers (simplified)
            outlier_count = self._detect_simple_outliers(data)
            quality_metrics['outliers'] = outlier_count
            
            # Calculate quality score
            filled_ratio = quality_metrics['filled_fields'] / quality_metrics['total_fields'] if quality_metrics['total_fields'] > 0 else 1.0
            missing_ratio = 1.0 - (missing_count / quality_metrics['total_fields']) if quality_metrics['total_fields'] > 0 else 1.0
            outlier_ratio = 1.0 - (outlier_count / quality_metrics['total_fields']) if quality_metrics['total_fields'] > 0 else 1.0
            
            quality_metrics['quality_score'] = (filled_ratio + missing_ratio + outlier_ratio) / 3.0
            
            # Update metrics
            self.metrics['missing_values'] += missing_count
            self.metrics['outliers'] += outlier_count
            self.metrics['total_records'] += 1
            self.metrics['quality_score'] = quality_metrics['quality_score']
            
            # Add to history
            self.quality_history.append(quality_metrics)
            
            return quality_metrics
            
        except Exception as e:
            logger.error(f"Error assessing data quality: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'missing_values': 0,
                'outliers': 0,
                'duplicates': 0,
                'total_fields': len(data) if data else 0,
                'filled_fields': 0,
                'quality_score': 0.0
            }
    
    def _detect_simple_outliers(self, data: Dict[str, Any]) -> int:
        """Detect simple outliers in numeric data"""
        try:
            outlier_count = 0
            for key, value in data.items():
                # Check if it's a numeric value
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    # Simple outlier detection using z-score approach
                    # This is a simplified version - in practice, you'd use historical data
                    if abs(value) > 10000:  # Arbitrary large value threshold
                        outlier_count += 1
            return outlier_count
        except Exception as e:
            logger.error(f"Error detecting outliers: {e}")
            return 0
    
    def get_quality_report(self) -> Dict[str, Any]:
        """Get comprehensive quality report"""
        try:
            if not self.quality_history:
                return {
                    'overall_quality_score': 1.0,
                    'total_records_processed': 0,
                    'missing_values_total': 0,
                    'outliers_total': 0,
                    'quality_trend': 'stable'
                }
            
            # Calculate averages
            avg_quality = np.mean([q['quality_score'] for q in self.quality_history])
            total_missing = sum(q['missing_values'] for q in self.quality_history)
            total_outliers = sum(q['outliers'] for q in self.quality_history)
            total_records = len(self.quality_history)
            
            # Determine trend
            if len(self.quality_history) > 10:
                recent_scores = [q['quality_score'] for q in list(self.quality_history)[-10:]]
                older_scores = [q['quality_score'] for q in list(self.quality_history)[:-10]]
                recent_avg = np.mean(recent_scores)
                older_avg = np.mean(older_scores) if older_scores else recent_avg
                
                if recent_avg > older_avg + 0.1:
                    trend = 'improving'
                elif recent_avg < older_avg - 0.1:
                    trend = 'degrading'
                else:
                    trend = 'stable'
            else:
                trend = 'insufficient_data'
            
            return {
                'overall_quality_score': avg_quality,
                'total_records_processed': total_records,
                'missing_values_total': total_missing,
                'outliers_total': total_outliers,
                'quality_trend': trend
            }
            
        except Exception as e:
            logger.error(f"Error generating quality report: {e}")
            return {
                'overall_quality_score': 0.0,
                'total_records_processed': 0,
                'missing_values_total': 0,
                'outliers_total': 0,
                'quality_trend': 'error'
            }
    
    def is_quality_alert_needed(self) -> bool:
        """Check if quality alert is needed"""
        try:
            return self.metrics['quality_score'] < self.config.quality_threshold
        except Exception as e:
            logger.error(f"Error checking quality alert: {e}")
            return False


class FeatureExtractor:
    """Extracts features from streaming data for anomaly detection"""
    
    def __init__(self, config: DataProcessorConfig):
        self.config = config
        self.feature_history = deque(maxlen=config.window_size)
        # Caching for performance optimization
        self._location_cache = {}
        self._cache_counter = 0
        logger.info("FeatureExtractor initialized")
    
    def extract_features(self, data: Dict[str, Any], stream_type: str) -> Dict[str, Any]:
        """Extract features from data based on stream type"""
        try:
            features = {
                'timestamp': data.get('timestamp', datetime.now().isoformat()),
                'stream_type': stream_type
            }
            
            if stream_type == 'system_metrics':
                features.update(self._extract_system_metrics_features(data))
            elif stream_type == 'transaction':
                features.update(self._extract_transaction_features(data))
            elif stream_type == 'network_traffic':
                features.update(self._extract_network_traffic_features(data))
            elif stream_type == 'user_behavior':
                features.update(self._extract_user_behavior_features(data))
            else:
                # Generic feature extraction
                features.update(self._extract_generic_features(data))
            
            # Add to history
            self.feature_history.append(features)
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'stream_type': stream_type,
                'error': True
            }
    
    def _extract_system_metrics_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from system metrics data"""
        try:
            features = {}
            
            # CPU usage features
            cpu_usage = data.get('cpu_usage_percent', 0)
            features['cpu_usage'] = cpu_usage
            features['cpu_usage_normalized'] = cpu_usage / 100.0
            
            # Memory usage features
            memory_usage = data.get('memory_usage_percent', 0)
            features['memory_usage'] = memory_usage
            features['memory_usage_normalized'] = memory_usage / 100.0
            
            # Network features
            network_in = data.get('network_bytes_in', 0)
            network_out = data.get('network_bytes_out', 0)
            features['network_total_bytes'] = network_in + network_out
            features['network_ratio'] = network_out / network_in if network_in > 0 else 0
            
            # Error rate features
            error_rate = data.get('error_rate', 0)
            features['error_rate'] = error_rate
            features['is_high_error'] = 1 if error_rate > 0.05 else 0  # 5% threshold
            
            # Requests per second features
            req_per_sec = data.get('requests_per_second', 0)
            features['requests_per_second'] = req_per_sec
            features['is_high_traffic'] = 1 if req_per_sec > 200 else 0  # High traffic threshold
            
            # Derived features
            features['cpu_memory_correlation'] = cpu_usage * memory_usage / 10000.0
            features['network_efficiency'] = req_per_sec / (network_in + 1) if network_in > 0 else 0
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting system metrics features: {e}")
            return {}
    
    def _extract_transaction_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from transaction data"""
        try:
            features = {}
            
            # Amount features
            amount = data.get('amount', 0)
            features['transaction_amount'] = amount
            features['amount_log'] = np.log(amount + 1)  # Log transform
            
            # Transaction type features
            transaction_type = data.get('transaction_type', 'unknown')
            features['is_purchase'] = 1 if transaction_type == 'purchase' else 0
            features['is_transfer'] = 1 if transaction_type == 'transfer' else 0
            features['is_withdrawal'] = 1 if transaction_type == 'withdrawal' else 0
            features['is_deposit'] = 1 if transaction_type == 'deposit' else 0
            
            # Location features with caching
            location = data.get('location', 'unknown')
            if self.config.enable_caching and location in self._location_cache:
                location_hash = self._location_cache[location]
            else:
                location_hash = hash(location) % 1000  # Normalize location
                if self.config.enable_caching:
                    self._location_cache[location] = location_hash
                    # Limit cache size
                    if len(self._location_cache) > 100:
                        # Remove oldest entries
                        keys_to_remove = list(self._location_cache.keys())[:10]
                        for key in keys_to_remove:
                            del self._location_cache[key]
            
            features['location_hash'] = location_hash
            
            # Device features
            device_type = data.get('device_type', 'unknown')
            features['is_mobile'] = 1 if device_type == 'mobile' else 0
            features['is_desktop'] = 1 if device_type == 'desktop' else 0
            features['is_tablet'] = 1 if device_type == 'tablet' else 0
            
            # Risk features
            is_flagged = data.get('is_flagged', 0)
            features['is_flagged'] = is_flagged
            features['is_large_amount'] = 1 if amount > 1000 else 0
            features['is_suspicious_pattern'] = is_flagged  # Simplified
            
            # Time-based features (if we had more data)
            features['hour_of_day'] = datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())).hour
            features['day_of_week'] = datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())).weekday()
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting transaction features: {e}")
            return {}
    
    def _extract_network_traffic_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from network traffic data"""
        try:
            features = {}
            
            # Traffic volume features
            bytes_transferred = data.get('bytes_transferred', 0)
            features['bytes_transferred'] = bytes_transferred
            features['bytes_log'] = np.log(bytes_transferred + 1)  # Log transform
            
            # Packet features
            packets = data.get('packets', 0)
            features['packets'] = packets
            features['bytes_per_packet'] = bytes_transferred / packets if packets > 0 else 0
            
            # Protocol features
            protocol = data.get('protocol', 'unknown')
            features['is_tcp'] = 1 if protocol == 'TCP' else 0
            features['is_udp'] = 1 if protocol == 'UDP' else 0
            
            # Port features
            port = data.get('port', 0)
            features['port'] = port
            features['is_common_port'] = 1 if port in [80, 443, 22, 21, 53] else 0
            
            # Duration features
            duration = data.get('duration_seconds', 0)
            features['duration_seconds'] = duration
            features['is_long_session'] = 1 if duration > 60 else 0  # Long session threshold
            
            # Traffic type features
            traffic_type = data.get('traffic_type', 'unknown')
            features['is_web_browsing'] = 1 if traffic_type == 'web_browsing' else 0
            features['is_file_transfer'] = 1 if traffic_type == 'file_transfer' else 0
            features['is_dns_query'] = 1 if traffic_type == 'dns_query' else 0
            
            # Security features
            is_suspicious = data.get('is_suspicious', 0)
            features['is_suspicious'] = is_suspicious
            features['is_large_transfer'] = 1 if bytes_transferred > 1000000 else 0  # 1MB threshold
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting network traffic features: {e}")
            return {}
    
    def _extract_user_behavior_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from user behavior data"""
        try:
            features = {}
            
            # Activity features
            page_views = data.get('page_views', 0)
            clicks = data.get('clicks', 0)
            features['page_views'] = page_views
            features['clicks'] = clicks
            features['clicks_per_page'] = clicks / page_views if page_views > 0 else 0
            
            # Session features
            session_duration = data.get('session_duration_minutes', 0)
            features['session_duration_minutes'] = session_duration
            features['actions_per_minute'] = data.get('actions_per_minute', 0)
            features['is_long_session'] = 1 if session_duration > 30 else 0  # Long session threshold
            
            # Engagement features
            features['engagement_score'] = (page_views * clicks) / (session_duration + 1)
            
            # Login features
            login_frequency = data.get('login_frequency', 0)
            failed_logins = data.get('failed_logins', 0)
            features['login_frequency'] = login_frequency
            features['failed_logins'] = failed_logins
            features['failed_login_ratio'] = failed_logins / login_frequency if login_frequency > 0 else 0
            
            # Security features
            suspicious_activity = data.get('suspicious_activity', 0)
            features['suspicious_activity'] = suspicious_activity
            features['is_suspicious'] = suspicious_activity
            features['is_high_activity'] = 1 if page_views > 30 else 0  # High activity threshold
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting user behavior features: {e}")
            return {}
    
    def _extract_generic_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract generic features from any data"""
        try:
            features = {}
            
            # Count features
            features['field_count'] = len(data)
            features['numeric_field_count'] = sum(1 for v in data.values() if isinstance(v, (int, float)) and not isinstance(v, bool))
            features['string_field_count'] = sum(1 for v in data.values() if isinstance(v, str))
            
            # Statistical features for numeric values
            numeric_values = [v for v in data.values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
            if numeric_values:
                features['numeric_mean'] = np.mean(numeric_values)
                features['numeric_std'] = np.std(numeric_values)
                features['numeric_min'] = np.min(numeric_values)
                features['numeric_max'] = np.max(numeric_values)
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting generic features: {e}")
            return {}


class StreamDataProcessor:
    """Main processor for streaming data"""
    
    def __init__(self, config: Optional[DataProcessorConfig] = None):
        self.config = config or DataProcessorConfig()
        self.quality_monitor = DataQualityMonitor(self.config)
        self.feature_extractor = FeatureExtractor(self.config)
        self.processed_count = 0
        self.error_count = 0
        # Batch processing optimization
        self.batch_buffer = []
        self.batch_counter = 0
        logger.info("StreamDataProcessor initialized")
    
    async def process_stream_data(self, data: Dict[str, Any], stream_type: str) -> Dict[str, Any]:
        """Process streaming data with quality monitoring and feature extraction"""
        try:
            # Assess data quality
            quality_metrics = {}
            if self.config.enable_quality_monitoring:
                quality_metrics = self.quality_monitor.assess_data_quality(data)
            
            # Extract features
            features = {}
            if self.config.enable_feature_extraction:
                features = self.feature_extractor.extract_features(data, stream_type)
            
            # Combine results
            result = {
                'processed_timestamp': datetime.now().isoformat(),
                'original_data': data,
                'stream_type': stream_type,
                'quality_metrics': quality_metrics,
                'extracted_features': features,
                'processing_success': True
            }
            
            self.processed_count += 1
            return result
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Error processing stream data: {e}")
            return {
                'processed_timestamp': datetime.now().isoformat(),
                'original_data': data,
                'stream_type': stream_type,
                'quality_metrics': {},
                'extracted_features': {},
                'processing_success': False,
                'error': str(e)
            }
    
    async def process_batch_data(self, data_list: List[Dict[str, Any]], stream_type: str) -> List[Dict[str, Any]]:
        """Process batch of streaming data for better performance"""
        try:
            results = []
            for data in data_list:
                result = await self.process_stream_data(data, stream_type)
                results.append(result)
            return results
        except Exception as e:
            logger.error(f"Error processing batch data: {e}")
            return []
    
    def get_processor_stats(self) -> Dict[str, Any]:
        """Get processor statistics"""
        try:
            quality_report = self.quality_monitor.get_quality_report()
            
            return {
                'processed_count': self.processed_count,
                'error_count': self.error_count,
                'success_rate': self.processed_count / (self.processed_count + self.error_count) if (self.processed_count + self.error_count) > 0 else 1.0,
                'quality_report': quality_report,
                'batch_size': self.config.batch_size
            }
        except Exception as e:
            logger.error(f"Error getting processor stats: {e}")
            return {
                'processed_count': self.processed_count,
                'error_count': self.error_count,
                'success_rate': 0.0,
                'quality_report': {},
                'batch_size': self.config.batch_size
            }
    
    def is_quality_alert_needed(self) -> bool:
        """Check if quality alert is needed"""
        try:
            return self.quality_monitor.is_quality_alert_needed()
        except Exception as e:
            logger.error(f"Error checking quality alert: {e}")
            return False


# Factory function for creating data processor
def create_data_processor(config: Optional[DataProcessorConfig] = None) -> StreamDataProcessor:
    """Create stream data processor with configuration"""
    return StreamDataProcessor(config)