"""
Real-time Data Streaming Service for Anomaly Detection
Handles real-time data streaming with WebSocket support for anomaly detection
"""

import logging
import asyncio
import json
import websockets
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, AsyncGenerator, Callable
from dataclasses import asdict
import aiohttp
from collections import deque
import threading
import time
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class StreamingConfig:
    """Configuration for real-time streaming"""
    def __init__(self, 
                 update_interval: int = 60,
                 max_buffer_size: int = 1000,
                 websocket_port: int = 8766,
                 enable_websocket: bool = True,
                 enable_webhook: bool = False,
                 webhook_url: Optional[str] = None):
        self.update_interval = update_interval
        self.max_buffer_size = max_buffer_size
        self.websocket_port = websocket_port
        self.enable_websocket = enable_websocket
        self.enable_webhook = enable_webhook
        self.webhook_url = webhook_url


class DataStream:
    """Individual data stream with buffering and filtering"""
    
    def __init__(self, stream_id: str, stream_type: str, config: StreamingConfig):
        self.stream_id = stream_id
        self.stream_type = stream_type
        self.config = config
        self.buffer = deque(maxlen=config.max_buffer_size)
        self.subscribers: List[Callable] = []
        self.last_update = None
        self.update_count = 0
        logger.info(f"DataStream {stream_id} initialized")
    
    def add_data(self, data: Dict[str, Any]):
        """Add data to the stream buffer"""
        try:
            # Add timestamp if not present
            if "timestamp" not in data:
                data["timestamp"] = datetime.now().isoformat()
            
            # Add to buffer
            self.buffer.append(data)
            self.last_update = datetime.now()
            self.update_count += 1
            
            # Notify subscribers
            self._notify_subscribers(data)
            
        except Exception as e:
            logger.error(f"Error adding data to stream {self.stream_id}: {e}")
    
    def _notify_subscribers(self, data: Dict[str, Any]):
        """Notify all subscribers of new data"""
        for callback in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(data))
                else:
                    callback(data)
            except Exception as e:
                logger.error(f"Error notifying subscriber: {e}")
    
    def subscribe(self, callback: Callable):
        """Subscribe to stream updates"""
        self.subscribers.append(callback)
        logger.info(f"Added subscriber to stream {self.stream_id}")
    
    def unsubscribe(self, callback: Callable):
        """Unsubscribe from stream updates"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)
            logger.info(f"Removed subscriber from stream {self.stream_id}")
    
    def get_latest_data(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get latest data from buffer"""
        try:
            # Return last 'count' items
            return list(self.buffer)[-count:]
        except Exception as e:
            logger.error(f"Error getting latest data from stream {self.stream_id}: {e}")
            return []
    
    def get_buffer_stats(self) -> Dict[str, Any]:
        """Get stream buffer statistics"""
        return {
            "stream_id": self.stream_id,
            "stream_type": self.stream_type,
            "buffer_size": len(self.buffer),
            "max_buffer_size": self.buffer.maxlen,
            "last_update": self.last_update.isoformat() if self.last_update else None,
            "update_count": self.update_count
        }


class AnomalyStreamingService:
    """Real-time data streaming service for anomaly detection"""
    
    def __init__(self, config: StreamingConfig):
        self.config = config
        self.streams: Dict[str, DataStream] = {}
        self.websocket_server = None
        self.websocket_clients: set = set()
        self.is_running = False
        self._streaming_tasks: List[asyncio.Task] = []
        
        # Initialize streams
        self._initialize_streams()
    
    def _initialize_streams(self):
        """Initialize data streams"""
        try:
            # System metrics stream
            self.streams["system_metrics"] = DataStream(
                "system_metrics", 
                "metrics", 
                self.config
            )
            
            # Transaction data stream
            self.streams["transactions"] = DataStream(
                "transactions", 
                "financial", 
                self.config
            )
            
            # Network traffic stream
            self.streams["network_traffic"] = DataStream(
                "network_traffic", 
                "network", 
                self.config
            )
            
            # User behavior stream
            self.streams["user_behavior"] = DataStream(
                "user_behavior", 
                "behavioral", 
                self.config
            )
            
            logger.info(f"Initialized {len(self.streams)} data streams")
            
        except Exception as e:
            logger.error(f"Failed to initialize streams: {e}")
            raise
    
    async def start(self):
        """Start the streaming service"""
        try:
            logger.info("Starting real-time streaming service...")
            
            # Start streaming tasks
            self._streaming_tasks = [
                asyncio.create_task(self._stream_system_metrics()),
                asyncio.create_task(self._stream_transactions()),
                asyncio.create_task(self._stream_network_traffic()),
                asyncio.create_task(self._stream_user_behavior())
            ]
            
            # Start WebSocket server if enabled
            if self.config.enable_websocket:
                self._streaming_tasks.append(
                    asyncio.create_task(self._start_websocket_server())
                )
            
            self.is_running = True
            logger.info("Real-time streaming service started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start streaming service: {e}")
            raise
    
    async def stop(self):
        """Stop the streaming service"""
        try:
            logger.info("Stopping real-time streaming service...")
            
            self.is_running = False
            
            # Cancel all streaming tasks
            for task in self._streaming_tasks:
                task.cancel()
            
            # Wait for tasks to complete
            await asyncio.gather(*self._streaming_tasks, return_exceptions=True)
            
            # Close WebSocket server
            if self.websocket_server:
                self.websocket_server.close()
                await self.websocket_server.wait_closed()
            
            logger.info("Real-time streaming service stopped")
            
        except Exception as e:
            logger.error(f"Error stopping streaming service: {e}")
    
    async def _stream_system_metrics(self):
        """Stream system metrics data"""
        try:
            while self.is_running:
                try:
                    # Generate mock system metrics data
                    system_data = self._generate_system_metrics()
                    
                    # Add to stream
                    self.streams["system_metrics"].add_data(system_data)
                    
                    # Send webhook if enabled
                    if self.config.enable_webhook and self.config.webhook_url:
                        await self._send_webhook("system_metrics", system_data)
                    
                    await asyncio.sleep(self.config.update_interval)
                    
                except Exception as e:
                    logger.error(f"Error in system metrics streaming: {e}")
                    await asyncio.sleep(self.config.update_interval)
                    
        except asyncio.CancelledError:
            logger.info("System metrics streaming cancelled")
    
    async def _stream_transactions(self):
        """Stream transaction data"""
        try:
            while self.is_running:
                try:
                    # Generate mock transaction data
                    transaction_data = self._generate_transaction_data()
                    
                    # Add to stream
                    self.streams["transactions"].add_data(transaction_data)
                    
                    await asyncio.sleep(self.config.update_interval * 1.5)  # Less frequent updates
                    
                except Exception as e:
                    logger.error(f"Error in transaction streaming: {e}")
                    await asyncio.sleep(self.config.update_interval * 1.5)
                    
        except asyncio.CancelledError:
            logger.info("Transaction streaming cancelled")
    
    async def _stream_network_traffic(self):
        """Stream network traffic data"""
        try:
            while self.is_running:
                try:
                    # Generate mock network traffic data
                    network_data = self._generate_network_traffic()
                    
                    # Add to stream
                    self.streams["network_traffic"].add_data(network_data)
                    
                    await asyncio.sleep(self.config.update_interval * 2)  # Less frequent updates
                    
                except Exception as e:
                    logger.error(f"Error in network traffic streaming: {e}")
                    await asyncio.sleep(self.config.update_interval * 2)
                    
        except asyncio.CancelledError:
            logger.info("Network traffic streaming cancelled")
    
    async def _stream_user_behavior(self):
        """Stream user behavior data"""
        try:
            while self.is_running:
                try:
                    # Generate mock user behavior data
                    behavior_data = self._generate_user_behavior()
                    
                    # Add to stream
                    self.streams["user_behavior"].add_data(behavior_data)
                    
                    await asyncio.sleep(self.config.update_interval * 1.2)  # Less frequent updates
                    
                except Exception as e:
                    logger.error(f"Error in user behavior streaming: {e}")
                    await asyncio.sleep(self.config.update_interval * 1.2)
                    
        except asyncio.CancelledError:
            logger.info("User behavior streaming cancelled")
    
    def _generate_system_metrics(self) -> Dict[str, Any]:
        """Generate mock system metrics data"""
        try:
            # Generate realistic system metrics
            timestamp = datetime.now()
            
            # CPU usage with some variation
            cpu_usage = 45.0 + np.random.normal(0, 5)
            cpu_usage = max(0, min(100, cpu_usage))  # Clamp between 0-100
            
            # Memory usage with some variation
            memory_usage = 68.0 + np.random.normal(0, 4)
            memory_usage = max(0, min(100, memory_usage))  # Clamp between 0-100
            
            # Disk I/O operations
            disk_io_ops = 1000 + np.random.poisson(300)
            
            # Network traffic
            network_in = 2000000 + np.random.poisson(500000)
            network_out = 1500000 + np.random.poisson(400000)
            
            # Error rate
            error_rate = np.random.exponential(0.02)
            error_rate = min(1.0, error_rate)  # Clamp to 0-1
            
            # Requests per second
            requests_per_second = 100 + np.random.poisson(50)
            
            return {
                "type": "system_metrics",
                "timestamp": timestamp.isoformat(),
                "cpu_usage_percent": round(cpu_usage, 2),
                "memory_usage_percent": round(memory_usage, 2),
                "disk_io_ops": disk_io_ops,
                "network_bytes_in": network_in,
                "network_bytes_out": network_out,
                "error_rate": round(error_rate, 4),
                "requests_per_second": requests_per_second
            }
            
        except Exception as e:
            logger.error(f"Error generating system metrics: {e}")
            return {
                "type": "system_metrics",
                "timestamp": datetime.now().isoformat(),
                "cpu_usage_percent": 45.0,
                "memory_usage_percent": 68.0,
                "disk_io_ops": 1200,
                "network_bytes_in": 2500000,
                "network_bytes_out": 1800000,
                "error_rate": 0.02,
                "requests_per_second": 150
            }
    
    def _generate_transaction_data(self) -> Dict[str, Any]:
        """Generate mock transaction data"""
        try:
            timestamp = datetime.now()
            
            # Generate transaction ID
            transaction_id = f"txn_{np.random.randint(10000, 99999):05d}"
            
            # Generate user ID
            user_id = f"user_{np.random.randint(1000, 2000)}"
            
            # Generate amount (log-normal distribution for realistic financial data)
            amount = np.random.lognormal(4, 1)
            amount = round(max(1, min(10000, amount)), 2)
            
            # Transaction types
            transaction_types = ["purchase", "transfer", "withdrawal", "deposit"]
            transaction_type = np.random.choice(transaction_types, p=[0.7, 0.2, 0.05, 0.05])
            
            # IP addresses (mock)
            ip_addresses = [
                "192.168.1.105", "10.20.30.45", "172.16.254.1", "203.0.113.5",
                "198.51.100.22", "192.0.2.1", "192.0.2.45", "192.0.2.100"
            ]
            ip_address = np.random.choice(ip_addresses)
            
            # Locations
            locations = ["New York", "London", "Paris", "Tokyo", "Sydney", "Berlin", "Madrid"]
            location = np.random.choice(locations)
            
            # Currency
            currency = "USD"
            
            # Device types
            device_types = ["mobile", "desktop", "tablet"]
            device_type = np.random.choice(device_types, p=[0.6, 0.35, 0.05])
            
            # Flag for suspicious activity (rare)
            is_flagged = int(np.random.random() < 0.05)  # 5% chance of being flagged
            
            return {
                "type": "transaction",
                "timestamp": timestamp.isoformat(),
                "transaction_id": transaction_id,
                "user_id": user_id,
                "amount": amount,
                "transaction_type": transaction_type,
                "ip_address": ip_address,
                "location": location,
                "currency": currency,
                "device_type": device_type,
                "is_flagged": is_flagged
            }
            
        except Exception as e:
            logger.error(f"Error generating transaction data: {e}")
            return {
                "type": "transaction",
                "timestamp": datetime.now().isoformat(),
                "transaction_id": "txn_00001",
                "user_id": "user_1001",
                "amount": 125.50,
                "transaction_type": "purchase",
                "ip_address": "192.168.1.105",
                "location": "New York",
                "currency": "USD",
                "device_type": "mobile",
                "is_flagged": 0
            }
    
    def _generate_network_traffic(self) -> Dict[str, Any]:
        """Generate mock network traffic data"""
        try:
            timestamp = datetime.now()
            
            # Source and destination IPs (mock)
            ip_addresses = [
                "192.168.1.105", "10.20.30.45", "172.16.254.1", "203.0.113.5",
                "198.51.100.22", "192.0.2.1", "192.0.2.45", "192.0.2.100"
            ]
            source_ip = np.random.choice(ip_addresses)
            destination_ip = np.random.choice(ip_addresses)
            
            # Bytes transferred (exponential distribution for realistic network data)
            bytes_transferred = int(np.random.exponential(50000))
            bytes_transferred = max(1000, min(15000000, bytes_transferred))
            
            # Packets
            packets = max(10, int(bytes_transferred / np.random.uniform(100, 2000)))
            
            # Protocols
            protocols = ["TCP", "UDP"]
            protocol = np.random.choice(protocols, p=[0.85, 0.15])
            
            # Ports
            ports = [80, 443, 22, 21, 53, 25, 110]
            port = np.random.choice(ports)
            
            # Duration
            duration_seconds = np.random.exponential(30)
            duration_seconds = max(1, min(300, duration_seconds))
            
            # Traffic types
            traffic_types = ["web_browsing", "file_transfer", "dns_query", "email", "streaming"]
            traffic_type = np.random.choice(traffic_types, p=[0.5, 0.2, 0.15, 0.1, 0.05])
            
            # Suspicious flag (rare)
            is_suspicious = int(np.random.random() < 0.03)  # 3% chance of being suspicious
            
            return {
                "type": "network_traffic",
                "timestamp": timestamp.isoformat(),
                "source_ip": source_ip,
                "destination_ip": destination_ip,
                "bytes_transferred": bytes_transferred,
                "packets": packets,
                "protocol": protocol,
                "port": port,
                "duration_seconds": round(duration_seconds, 1),
                "traffic_type": traffic_type,
                "is_suspicious": is_suspicious
            }
            
        except Exception as e:
            logger.error(f"Error generating network traffic data: {e}")
            return {
                "type": "network_traffic",
                "timestamp": datetime.now().isoformat(),
                "source_ip": "192.168.1.105",
                "destination_ip": "104.28.12.45",
                "bytes_transferred": 15420,
                "packets": 120,
                "protocol": "TCP",
                "port": 443,
                "duration_seconds": 5.2,
                "traffic_type": "web_browsing",
                "is_suspicious": 0
            }
    
    def _generate_user_behavior(self) -> Dict[str, Any]:
        """Generate mock user behavior data"""
        try:
            timestamp = datetime.now()
            
            # User ID
            user_id = f"user_{np.random.randint(1000, 2000)}"
            
            # Page views (Poisson distribution)
            page_views = max(1, np.random.poisson(15))
            
            # Clicks (correlated with page views)
            clicks = max(1, int(np.random.normal(page_views * 2, page_views * 0.5)))
            
            # Session duration (exponential distribution in minutes)
            session_duration_minutes = np.random.exponential(20)
            session_duration_minutes = max(1, min(120, session_duration_minutes))
            
            # Actions per minute
            actions_per_minute = max(0.5, np.random.normal(1.5, 0.3))
            
            # Login frequency (per session)
            login_frequency = 1  # Always 1 for a session
            
            # Failed logins (rare)
            failed_logins = int(np.random.random() < 0.02)  # 2% chance
            
            # Suspicious activity flag (very rare)
            suspicious_activity = int(np.random.random() < 0.01)  # 1% chance
            
            return {
                "type": "user_behavior",
                "timestamp": timestamp.isoformat(),
                "user_id": user_id,
                "page_views": page_views,
                "clicks": clicks,
                "session_duration_minutes": round(session_duration_minutes, 1),
                "actions_per_minute": round(actions_per_minute, 1),
                "login_frequency": login_frequency,
                "failed_logins": failed_logins,
                "suspicious_activity": suspicious_activity
            }
            
        except Exception as e:
            logger.error(f"Error generating user behavior data: {e}")
            return {
                "type": "user_behavior",
                "timestamp": datetime.now().isoformat(),
                "user_id": "user_1001",
                "page_views": 15,
                "clicks": 42,
                "session_duration_minutes": 28,
                "actions_per_minute": 1.5,
                "login_frequency": 1,
                "failed_logins": 0,
                "suspicious_activity": 0
            }
    
    async def _send_webhook(self, stream_type: str, data: Dict[str, Any]):
        """Send data via webhook"""
        try:
            if not self.config.webhook_url:
                return
            
            async with aiohttp.ClientSession() as session:
                payload = {
                    "stream_type": stream_type,
                    "data": data
                }
                async with session.post(self.config.webhook_url, json=payload) as response:
                    if response.status != 200:
                        logger.warning(f"Webhook failed with status {response.status}")
        except Exception as e:
            logger.error(f"Error sending webhook: {e}")
    
    async def _start_websocket_server(self):
        """Start WebSocket server for real-time data"""
        try:
            async def handle_client(websocket):
                """Handle WebSocket client connection"""
                self.websocket_clients.add(websocket)
                logger.info(f"WebSocket client connected: {websocket.remote_address}")
                
                try:
                    # Send initial data
                    for stream_id, stream in self.streams.items():
                        latest_data = stream.get_latest_data(10)
                        if latest_data:
                            await websocket.send(json.dumps({
                                "type": "initial_data",
                                "stream_id": stream_id,
                                "data": latest_data
                            }))
                    
                    # Keep connection alive and send updates
                    async for message in websocket:
                        try:
                            data = json.loads(message)
                            await self._handle_websocket_message(websocket, data)
                        except json.JSONDecodeError:
                            await websocket.send(json.dumps({"error": "Invalid JSON"}))
                        except Exception as e:
                            logger.error(f"Error handling WebSocket message: {e}")
                            
                except websockets.exceptions.ConnectionClosed:
                    logger.info(f"WebSocket client disconnected: {websocket.remote_address}")
                except Exception as e:
                    logger.error(f"Error in WebSocket connection: {e}")
                finally:
                    self.websocket_clients.discard(websocket)
            
            self.websocket_server = await websockets.serve(
                handle_client, 
                "localhost", 
                self.config.websocket_port
            )
            
            logger.info(f"WebSocket server started on port {self.config.websocket_port}")
            await self.websocket_server.wait_closed()
            
        except Exception as e:
            logger.error(f"Error starting WebSocket server: {e}")
    
    async def _handle_websocket_message(self, websocket, data: Dict[str, Any]):
        """Handle WebSocket message from client"""
        try:
            message_type = data.get("type")
            
            if message_type == "subscribe":
                stream_id = data.get("stream_id")
                if stream_id in self.streams:
                    # Add websocket as subscriber
                    self.streams[stream_id].subscribe(
                        lambda d: asyncio.create_task(
                            self._send_websocket_update(websocket, stream_id, d)
                        )
                    )
                    await websocket.send(json.dumps({
                        "type": "subscription_confirmed",
                        "stream_id": stream_id
                    }))
                else:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Stream {stream_id} not found"
                    }))
            else:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": f"Unknown message type: {message_type}"
                }))
                
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Internal server error"
            }))
    
    async def _send_websocket_update(self, websocket, stream_id: str, data: Dict[str, Any]):
        """Send update to WebSocket client"""
        try:
            await websocket.send(json.dumps({
                "type": "stream_update",
                "stream_id": stream_id,
                "data": data
            }))
        except websockets.exceptions.ConnectionClosed:
            # Client disconnected, remove from clients
            self.websocket_clients.discard(websocket)
        except Exception as e:
            logger.error(f"Error sending WebSocket update: {e}")
    
    def get_stream_data(self, stream_id: str, count: int = 10) -> List[Dict[str, Any]]:
        """Get data from a specific stream"""
        try:
            if stream_id in self.streams:
                return self.streams[stream_id].get_latest_data(count)
            else:
                logger.warning(f"Stream {stream_id} not found")
                return []
        except Exception as e:
            logger.error(f"Error getting stream data for {stream_id}: {e}")
            return []
    
    def get_stream_stats(self) -> Dict[str, Any]:
        """Get statistics for all streams"""
        try:
            stats = {}
            for stream_id, stream in self.streams.items():
                stats[stream_id] = stream.get_buffer_stats()
            return stats
        except Exception as e:
            logger.error(f"Error getting stream stats: {e}")
            return {}


# Factory function for creating streaming service
def create_anomaly_streaming_service(config: Optional[StreamingConfig] = None) -> AnomalyStreamingService:
    """Create anomaly detection streaming service with configuration"""
    if config is None:
        config = StreamingConfig()
    return AnomalyStreamingService(config)