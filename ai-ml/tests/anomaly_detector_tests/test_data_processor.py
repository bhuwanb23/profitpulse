"""
Unit tests for data processor components
"""

import unittest
import numpy as np
import pandas as pd
from datetime import datetime

from src.models.anomaly_detector.data_processor import (
    DataProcessorConfig,
    DataQualityMonitor,
    FeatureExtractor,
    StreamDataProcessor
)


class TestDataProcessorConfig(unittest.TestCase):
    """Test cases for DataProcessorConfig"""
    
    def test_initialization(self):
        """Test configuration initialization"""
        config = DataProcessorConfig()
        self.assertEqual(config.window_size, 100)
        self.assertEqual(config.quality_threshold, 0.8)
        self.assertTrue(config.enable_quality_monitoring)
        self.assertTrue(config.enable_feature_extraction)
        self.assertEqual(config.batch_size, 10)
        self.assertTrue(config.enable_caching)
    
    def test_custom_initialization(self):
        """Test custom configuration initialization"""
        config = DataProcessorConfig(
            window_size=200,
            quality_threshold=0.9,
            enable_quality_monitoring=False,
            enable_feature_extraction=False,
            batch_size=20,
            enable_caching=False
        )
        self.assertEqual(config.window_size, 200)
        self.assertEqual(config.quality_threshold, 0.9)
        self.assertFalse(config.enable_quality_monitoring)
        self.assertFalse(config.enable_feature_extraction)
        self.assertEqual(config.batch_size, 20)
        self.assertFalse(config.enable_caching)


class TestDataQualityMonitor(unittest.TestCase):
    """Test cases for DataQualityMonitor"""
    
    def setUp(self):
        """Set up test data"""
        self.config = DataProcessorConfig()
        self.monitor = DataQualityMonitor(self.config)
        
        # Sample data
        self.sample_data = {
            'feature1': 1.0,
            'feature2': 2.0,
            'feature3': None,
            'feature4': '',
            'feature5': 5.0
        }
    
    def test_initialization(self):
        """Test monitor initialization"""
        self.assertIsNotNone(self.monitor)
        self.assertEqual(self.monitor.config, self.config)
        self.assertEqual(len(self.monitor.metrics), 5)  # 5 metrics
        self.assertEqual(len(self.monitor.quality_history), 0)
    
    def test_assess_data_quality(self):
        """Test data quality assessment"""
        quality_metrics = self.monitor.assess_data_quality(self.sample_data)
        
        self.assertIn('timestamp', quality_metrics)
        self.assertIn('missing_values', quality_metrics)
        self.assertIn('outliers', quality_metrics)
        self.assertIn('duplicates', quality_metrics)
        self.assertIn('total_fields', quality_metrics)
        self.assertIn('filled_fields', quality_metrics)
        self.assertIn('quality_score', quality_metrics)
        
        # Check values
        self.assertEqual(quality_metrics['total_fields'], 5)
        self.assertEqual(quality_metrics['missing_values'], 2)  # None and ''
        self.assertEqual(quality_metrics['filled_fields'], 3)
    
    def test_get_quality_report(self):
        """Test quality report generation"""
        # Add some data to history
        self.monitor.assess_data_quality(self.sample_data)
        self.monitor.assess_data_quality(self.sample_data)
        
        report = self.monitor.get_quality_report()
        self.assertIn('overall_quality_score', report)
        self.assertIn('total_records_processed', report)
        self.assertIn('missing_values_total', report)
        self.assertIn('outliers_total', report)
        self.assertIn('quality_trend', report)
    
    def test_is_quality_alert_needed(self):
        """Test quality alert check"""
        # Test with high quality score
        result = self.monitor.is_quality_alert_needed()
        self.assertIsInstance(result, bool)


class TestFeatureExtractor(unittest.TestCase):
    """Test cases for FeatureExtractor"""
    
    def setUp(self):
        """Set up test data"""
        self.config = DataProcessorConfig()
        self.extractor = FeatureExtractor(self.config)
        
        # Sample data for different stream types
        self.system_metrics_data = {
            'type': 'system_metrics',
            'timestamp': datetime.now().isoformat(),
            'cpu_usage_percent': 45.0,
            'memory_usage_percent': 68.0,
            'disk_io_ops': 1200,
            'network_bytes_in': 2500000,
            'network_bytes_out': 1800000,
            'error_rate': 0.02,
            'requests_per_second': 150
        }
        
        self.transaction_data = {
            'type': 'transaction',
            'timestamp': datetime.now().isoformat(),
            'transaction_id': 'txn_00001',
            'user_id': 'user_1001',
            'amount': 125.50,
            'transaction_type': 'purchase',
            'ip_address': '192.168.1.105',
            'location': 'New York',
            'currency': 'USD',
            'device_type': 'mobile',
            'is_flagged': 0
        }
    
    def test_initialization(self):
        """Test extractor initialization"""
        self.assertIsNotNone(self.extractor)
        self.assertEqual(self.extractor.config, self.config)
        self.assertEqual(len(self.extractor.feature_history), 0)
    
    def test_extract_system_metrics_features(self):
        """Test system metrics feature extraction"""
        features = self.extractor.extract_features(self.system_metrics_data, 'system_metrics')
        
        self.assertIn('timestamp', features)
        self.assertIn('stream_type', features)
        self.assertIn('cpu_usage', features)
        self.assertIn('memory_usage', features)
        self.assertIn('network_total_bytes', features)
        self.assertIn('error_rate', features)
        self.assertIn('requests_per_second', features)
    
    def test_extract_transaction_features(self):
        """Test transaction feature extraction"""
        features = self.extractor.extract_features(self.transaction_data, 'transaction')
        
        self.assertIn('timestamp', features)
        self.assertIn('stream_type', features)
        self.assertIn('transaction_amount', features)
        self.assertIn('is_purchase', features)
        self.assertIn('location_hash', features)
        self.assertIn('is_mobile', features)
        self.assertIn('is_flagged', features)


class TestStreamDataProcessor(unittest.TestCase):
    """Test cases for StreamDataProcessor"""
    
    def setUp(self):
        """Set up test data"""
        self.config = DataProcessorConfig()
        self.processor = StreamDataProcessor(self.config)
        
        # Sample data
        self.sample_data = {
            'feature1': 1.0,
            'feature2': 2.0,
            'feature3': 3.0
        }
    
    def test_initialization(self):
        """Test processor initialization"""
        self.assertIsNotNone(self.processor)
        self.assertEqual(self.processor.config, self.config)
        self.assertEqual(self.processor.processed_count, 0)
        self.assertEqual(self.processor.error_count, 0)
    
    def test_process_stream_data(self):
        """Test stream data processing"""
        import asyncio
        
        # This is an async method, so we need to run it in an event loop
        async def test_async():
            result = await self.processor.process_stream_data(self.sample_data, 'generic')
            return result
        
        result = asyncio.run(test_async())
        
        self.assertIn('processed_timestamp', result)
        self.assertIn('original_data', result)
        self.assertIn('stream_type', result)
        self.assertIn('quality_metrics', result)
        self.assertIn('extracted_features', result)
        self.assertIn('processing_success', result)
        
        # Check that processing was successful
        self.assertTrue(result['processing_success'])
    
    def test_get_processor_stats(self):
        """Test processor statistics"""
        stats = self.processor.get_processor_stats()
        
        self.assertIn('processed_count', stats)
        self.assertIn('error_count', stats)
        self.assertIn('success_rate', stats)
        self.assertIn('quality_report', stats)
        self.assertIn('batch_size', stats)
        
        # Check initial values
        self.assertEqual(stats['processed_count'], 0)
        self.assertEqual(stats['error_count'], 0)
        self.assertEqual(stats['success_rate'], 1.0)  # 0/0 = 1.0 (no failures)
        self.assertEqual(stats['batch_size'], self.config.batch_size)


if __name__ == '__main__':
    unittest.main()