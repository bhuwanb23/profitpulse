"""
Unit tests for streaming service components
"""

import unittest
import numpy as np
import pandas as pd
from datetime import datetime

from src.models.anomaly_detector.streaming_service import (
    StreamingConfig,
    DataStream,
    AnomalyStreamingService
)


class TestStreamingConfig(unittest.TestCase):
    """Test cases for StreamingConfig"""
    
    def test_initialization(self):
        """Test configuration initialization"""
        config = StreamingConfig()
        self.assertEqual(config.update_interval, 60)
        self.assertEqual(config.max_buffer_size, 1000)
        self.assertEqual(config.websocket_port, 8766)
        self.assertTrue(config.enable_websocket)
        self.assertFalse(config.enable_webhook)
        self.assertIsNone(config.webhook_url)
    
    def test_custom_initialization(self):
        """Test custom configuration initialization"""
        config = StreamingConfig(
            update_interval=30,
            max_buffer_size=500,
            websocket_port=8765,
            enable_websocket=False,
            enable_webhook=True,
            webhook_url="http://example.com/webhook"
        )
        self.assertEqual(config.update_interval, 30)
        self.assertEqual(config.max_buffer_size, 500)
        self.assertEqual(config.websocket_port, 8765)
        self.assertFalse(config.enable_websocket)
        self.assertTrue(config.enable_webhook)
        self.assertEqual(config.webhook_url, "http://example.com/webhook")


class TestDataStream(unittest.TestCase):
    """Test cases for DataStream"""
    
    def setUp(self):
        """Set up test data"""
        self.config = StreamingConfig()
        self.stream = DataStream("test_stream", "test_type", self.config)
        
        # Sample data
        self.sample_data = {
            "feature1": 1.0,
            "feature2": 2.0,
            "feature3": 3.0
        }
    
    def test_initialization(self):
        """Test stream initialization"""
        self.assertEqual(self.stream.stream_id, "test_stream")
        self.assertEqual(self.stream.stream_type, "test_type")
        self.assertEqual(self.stream.config, self.config)
        self.assertEqual(len(self.stream.buffer), 0)
        self.assertEqual(len(self.stream.subscribers), 0)
        self.assertIsNone(self.stream.last_update)
        self.assertEqual(self.stream.update_count, 0)
    
    def test_add_data(self):
        """Test adding data to stream"""
        self.stream.add_data(self.sample_data)
        
        self.assertEqual(len(self.stream.buffer), 1)
        self.assertIsNotNone(self.stream.last_update)
        self.assertEqual(self.stream.update_count, 1)
        
        # Check that timestamp was added
        buffered_data = list(self.stream.buffer)[0]
        self.assertIn("timestamp", buffered_data)
    
    def test_get_latest_data(self):
        """Test getting latest data from stream"""
        # Add multiple data points
        for i in range(5):
            data = {"value": i}
            self.stream.add_data(data)
        
        # Get latest 3
        latest = self.stream.get_latest_data(3)
        self.assertEqual(len(latest), 3)
        
        # Check that we got the most recent data
        self.assertEqual(latest[-1]["value"], 4)
        self.assertEqual(latest[-2]["value"], 3)
    
    def test_get_buffer_stats(self):
        """Test getting buffer statistics"""
        # Add some data
        self.stream.add_data(self.sample_data)
        
        stats = self.stream.get_buffer_stats()
        self.assertEqual(stats["stream_id"], "test_stream")
        self.assertEqual(stats["stream_type"], "test_type")
        self.assertEqual(stats["buffer_size"], 1)
        self.assertEqual(stats["max_buffer_size"], self.config.max_buffer_size)
        self.assertIsNotNone(stats["last_update"])
        self.assertEqual(stats["update_count"], 1)


class TestAnomalyStreamingService(unittest.TestCase):
    """Test cases for AnomalyStreamingService"""
    
    def setUp(self):
        """Set up test data"""
        self.config = StreamingConfig()
        self.service = AnomalyStreamingService(self.config)
    
    def test_initialization(self):
        """Test service initialization"""
        self.assertEqual(self.service.config, self.config)
        self.assertEqual(len(self.service.streams), 4)  # 4 default streams
        self.assertIn("system_metrics", self.service.streams)
        self.assertIn("transactions", self.service.streams)
        self.assertIn("network_traffic", self.service.streams)
        self.assertIn("user_behavior", self.service.streams)
        self.assertIsNone(self.service.websocket_server)
        self.assertEqual(len(self.service.websocket_clients), 0)
        self.assertFalse(self.service.is_running)
        self.assertEqual(len(self.service._streaming_tasks), 0)
    
    def test_get_stream_data(self):
        """Test getting stream data"""
        # Add some data to a stream
        sample_data = {"value": 42}
        self.service.streams["system_metrics"].add_data(sample_data)
        
        # Get data from stream
        data = self.service.get_stream_data("system_metrics", 10)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["value"], 42)
    
    def test_get_stream_data_invalid_stream(self):
        """Test getting data from invalid stream"""
        data = self.service.get_stream_data("invalid_stream", 10)
        self.assertEqual(len(data), 0)
    
    def test_get_stream_stats(self):
        """Test getting stream statistics"""
        stats = self.service.get_stream_stats()
        self.assertEqual(len(stats), 4)  # 4 streams
        self.assertIn("system_metrics", stats)
        self.assertIn("transactions", stats)
        self.assertIn("network_traffic", stats)
        self.assertIn("user_behavior", stats)
        
        # Check that each stream has stats
        for stream_id, stream_stats in stats.items():
            self.assertIn("stream_id", stream_stats)
            self.assertIn("stream_type", stream_stats)
            self.assertIn("buffer_size", stream_stats)
            self.assertIn("max_buffer_size", stream_stats)
            self.assertIn("last_update", stream_stats)
            self.assertIn("update_count", stream_stats)


if __name__ == '__main__':
    unittest.main()