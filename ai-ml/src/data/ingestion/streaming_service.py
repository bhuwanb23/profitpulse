"""
Real-time Data Streaming Service
Handles real-time data streaming from SuperOps with WebSocket support
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

from .data_extractor import DataExtractor, create_data_extractor
from config import settings

logger = logging.getLogger(__name__)


class StreamingConfig:
    """Configuration for real-time streaming"""
    def __init__(self, 
                 update_interval: int = 60,
                 max_buffer_size: int = 1000,
                 websocket_port: int = 8765,
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
        self.is_active = False
        self.last_update = None
        self.update_count = 0
    
    def add_data(self, data: Dict[str, Any]):
        """Add data to stream buffer"""
        try:
            # Add metadata
            data["stream_metadata"] = {
                "stream_id": self.stream_id,
                "stream_type": self.stream_type,
                "timestamp": datetime.now().isoformat(),
                "update_count": self.update_count
            }
            
            self.buffer.append(data)
            self.last_update = datetime.now()
            self.update_count += 1
            
            # Notify subscribers
            self._notify_subscribers(data)
            
        except Exception as e:
            logger.error(f"Failed to add data to stream {self.stream_id}: {e}")
    
    def get_latest_data(self, count: int = 1) -> List[Dict[str, Any]]:
        """Get latest data from buffer"""
        return list(self.buffer)[-count:] if self.buffer else []
    
    def get_all_data(self) -> List[Dict[str, Any]]:
        """Get all data from buffer"""
        return list(self.buffer)
    
    def subscribe(self, callback: Callable):
        """Subscribe to stream updates"""
        self.subscribers.append(callback)
    
    def unsubscribe(self, callback: Callable):
        """Unsubscribe from stream updates"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)
    
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


class RealTimeStreamingService:
    """Real-time data streaming service for SuperOps data"""
    
    def __init__(self, config: StreamingConfig):
        self.config = config
        self.data_extractor = create_data_extractor()
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
            # Real-time metrics stream
            self.streams["realtime_metrics"] = DataStream(
                "realtime_metrics", 
                "metrics", 
                self.config
            )
            
            # Ticket updates stream
            self.streams["ticket_updates"] = DataStream(
                "ticket_updates", 
                "tickets", 
                self.config
            )
            
            # SLA alerts stream
            self.streams["sla_alerts"] = DataStream(
                "sla_alerts", 
                "alerts", 
                self.config
            )
            
            # Technician activity stream
            self.streams["technician_activity"] = DataStream(
                "technician_activity", 
                "activity", 
                self.config
            )
            
            # System health stream
            self.streams["system_health"] = DataStream(
                "system_health", 
                "health", 
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
            
            # Initialize data extractor
            await self.data_extractor.initialize()
            
            # Start streaming tasks
            self._streaming_tasks = [
                asyncio.create_task(self._stream_realtime_metrics()),
                asyncio.create_task(self._stream_ticket_updates()),
                asyncio.create_task(self._stream_sla_alerts()),
                asyncio.create_task(self._stream_technician_activity()),
                asyncio.create_task(self._stream_system_health())
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
            
            # Close data extractor
            await self.data_extractor.close()
            
            logger.info("Real-time streaming service stopped")
            
        except Exception as e:
            logger.error(f"Error stopping streaming service: {e}")
    
    async def _stream_realtime_metrics(self):
        """Stream real-time metrics data"""
        try:
            while self.is_running:
                try:
                    # Get real-time data from SuperOps
                    realtime_data = await self.data_extractor.superops_client.get_real_time_data()
                    
                    # Add to stream
                    self.streams["realtime_metrics"].add_data(realtime_data)
                    
                    # Send webhook if enabled
                    if self.config.enable_webhook and self.config.webhook_url:
                        await self._send_webhook("realtime_metrics", realtime_data)
                    
                    await asyncio.sleep(self.config.update_interval)
                    
                except Exception as e:
                    logger.error(f"Error in real-time metrics streaming: {e}")
                    await asyncio.sleep(self.config.update_interval)
                    
        except asyncio.CancelledError:
            logger.info("Real-time metrics streaming cancelled")
    
    async def _stream_ticket_updates(self):
        """Stream ticket updates"""
        try:
            last_check = datetime.now()
            
            while self.is_running:
                try:
                    # Get recent ticket updates
                    recent_tickets = await self.data_extractor.extract_ticket_data(
                        start_date=last_check - timedelta(minutes=5),
                        end_date=datetime.now()
                    )
                    
                    # Process new/updated tickets
                    for ticket in recent_tickets:
                        ticket_update = {
                            "type": "ticket_update",
                            "ticket": ticket,
                            "update_timestamp": datetime.now().isoformat()
                        }
                        
                        self.streams["ticket_updates"].add_data(ticket_update)
                    
                    last_check = datetime.now()
                    await asyncio.sleep(self.config.update_interval)
                    
                except Exception as e:
                    logger.error(f"Error in ticket updates streaming: {e}")
                    await asyncio.sleep(self.config.update_interval)
                    
        except asyncio.CancelledError:
            logger.info("Ticket updates streaming cancelled")
    
    async def _stream_sla_alerts(self):
        """Stream SLA alerts and breaches"""
        try:
            while self.is_running:
                try:
                    # Get recent SLA metrics
                    recent_sla_metrics = await self.data_extractor.extract_sla_metrics(
                        start_date=datetime.now() - timedelta(hours=1),
                        end_date=datetime.now()
                    )
                    
                    # Check for SLA breaches
                    for sla_metric in recent_sla_metrics:
                        if sla_metric.get("status") == "Breached":
                            alert = {
                                "type": "sla_breach",
                                "sla_metric": sla_metric,
                                "severity": "high",
                                "alert_timestamp": datetime.now().isoformat()
                            }
                            
                            self.streams["sla_alerts"].add_data(alert)
                    
                    await asyncio.sleep(self.config.update_interval)
                    
                except Exception as e:
                    logger.error(f"Error in SLA alerts streaming: {e}")
                    await asyncio.sleep(self.config.update_interval)
                    
        except asyncio.CancelledError:
            logger.info("SLA alerts streaming cancelled")
    
    async def _stream_technician_activity(self):
        """Stream technician activity updates"""
        try:
            while self.is_running:
                try:
                    # Get technician productivity data
                    productivity_data = await self.data_extractor.extract_technician_productivity()
                    
                    # Process activity updates
                    activity_update = {
                        "type": "technician_activity",
                        "productivity": productivity_data,
                        "update_timestamp": datetime.now().isoformat()
                    }
                    
                    self.streams["technician_activity"].add_data(activity_update)
                    
                    await asyncio.sleep(self.config.update_interval * 2)  # Less frequent updates
                    
                except Exception as e:
                    logger.error(f"Error in technician activity streaming: {e}")
                    await asyncio.sleep(self.config.update_interval * 2)
                    
        except asyncio.CancelledError:
            logger.info("Technician activity streaming cancelled")
    
    async def _stream_system_health(self):
        """Stream system health metrics"""
        try:
            while self.is_running:
                try:
                    # Get system health data
                    health_data = {
                        "timestamp": datetime.now().isoformat(),
                        "streams_active": len([s for s in self.streams.values() if s.is_active]),
                        "total_updates": sum(s.update_count for s in self.streams.values()),
                        "websocket_clients": len(self.websocket_clients),
                        "memory_usage": self._get_memory_usage(),
                        "cpu_usage": self._get_cpu_usage()
                    }
                    
                    self.streams["system_health"].add_data(health_data)
                    
                    await asyncio.sleep(self.config.update_interval)
                    
                except Exception as e:
                    logger.error(f"Error in system health streaming: {e}")
                    await asyncio.sleep(self.config.update_interval)
                    
        except asyncio.CancelledError:
            logger.info("System health streaming cancelled")
    
    async def _start_websocket_server(self):
        """Start WebSocket server for real-time data"""
        try:
            async def handle_client(websocket, path):
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
                finally:
                    self.websocket_clients.discard(websocket)
            
            # Start WebSocket server
            self.websocket_server = await websockets.serve(
                handle_client, 
                "localhost", 
                self.config.websocket_port
            )
            
            logger.info(f"WebSocket server started on port {self.config.websocket_port}")
            
            # Set up stream subscriptions for WebSocket broadcasting
            for stream in self.streams.values():
                stream.subscribe(self._broadcast_to_websockets)
            
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
            raise
    
    async def _handle_websocket_message(self, websocket, message: Dict[str, Any]):
        """Handle incoming WebSocket messages"""
        try:
            message_type = message.get("type")
            
            if message_type == "subscribe":
                stream_id = message.get("stream_id")
                if stream_id in self.streams:
                    # Send latest data for the stream
                    latest_data = self.streams[stream_id].get_latest_data(50)
                    await websocket.send(json.dumps({
                        "type": "subscription_data",
                        "stream_id": stream_id,
                        "data": latest_data
                    }))
            
            elif message_type == "get_latest":
                stream_id = message.get("stream_id")
                count = message.get("count", 10)
                
                if stream_id in self.streams:
                    latest_data = self.streams[stream_id].get_latest_data(count)
                    await websocket.send(json.dumps({
                        "type": "latest_data",
                        "stream_id": stream_id,
                        "data": latest_data
                    }))
            
            elif message_type == "ping":
                await websocket.send(json.dumps({"type": "pong"}))
                
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")
    
    async def _broadcast_to_websockets(self, data: Dict[str, Any]):
        """Broadcast data to all WebSocket clients"""
        if not self.websocket_clients:
            return
        
        try:
            message = json.dumps({
                "type": "stream_update",
                "data": data
            })
            
            # Send to all connected clients
            disconnected_clients = set()
            for websocket in self.websocket_clients:
                try:
                    await websocket.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected_clients.add(websocket)
                except Exception as e:
                    logger.error(f"Error broadcasting to WebSocket client: {e}")
                    disconnected_clients.add(websocket)
            
            # Remove disconnected clients
            self.websocket_clients -= disconnected_clients
            
        except Exception as e:
            logger.error(f"Error broadcasting to WebSocket clients: {e}")
    
    async def _send_webhook(self, stream_id: str, data: Dict[str, Any]):
        """Send data to webhook URL"""
        try:
            if not self.config.webhook_url:
                return
            
            webhook_data = {
                "stream_id": stream_id,
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.config.webhook_url,
                    json=webhook_data,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        logger.debug(f"Webhook sent successfully for stream {stream_id}")
                    else:
                        logger.warning(f"Webhook failed with status {response.status}")
                        
        except Exception as e:
            logger.error(f"Failed to send webhook: {e}")
    
    def get_stream_data(self, stream_id: str, count: int = 10) -> List[Dict[str, Any]]:
        """Get data from a specific stream"""
        if stream_id in self.streams:
            return self.streams[stream_id].get_latest_data(count)
        return []
    
    def get_all_streams_status(self) -> Dict[str, Any]:
        """Get status of all streams"""
        return {
            stream_id: {
                "is_active": stream.is_active,
                "update_count": stream.update_count,
                "last_update": stream.last_update.isoformat() if stream.last_update else None,
                "buffer_size": len(stream.buffer)
            }
            for stream_id, stream in self.streams.items()
        }
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage percentage"""
        try:
            import psutil
            return psutil.virtual_memory().percent
        except ImportError:
            return 0.0
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        try:
            import psutil
            return psutil.cpu_percent()
        except ImportError:
            return 0.0


# Factory function for creating streaming service
def create_streaming_service(config: StreamingConfig) -> RealTimeStreamingService:
    """Create real-time streaming service instance"""
    return RealTimeStreamingService(config)
