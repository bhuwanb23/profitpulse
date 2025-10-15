"""
Basic usage examples for SuperHack AI/ML system
Demonstrates common usage patterns and integration examples
"""

import asyncio
import logging
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data.data_extractor import create_data_extractor
from data.streaming_service import create_streaming_service, StreamingConfig
from utils.predictor import create_predictor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_data_extraction():
    """Example: Basic data extraction"""
    logger.info("🔍 Example: Data Extraction")
    logger.info("-" * 40)
    
    try:
        # Create data extractor
        extractor = create_data_extractor()
        await extractor.initialize()
        
        # Extract ticket data
        logger.info("Extracting ticket data...")
        tickets = await extractor.extract_ticket_data(
            start_date=datetime.now() - timedelta(days=7),
            end_date=datetime.now()
        )
        logger.info(f"✅ Extracted {len(tickets)} tickets")
        
        # Extract client data
        logger.info("Extracting client data...")
        clients = await extractor.extract_client_data()
        logger.info(f"✅ Extracted {len(clients)} clients")
        
        # Extract technician data
        logger.info("Extracting technician data...")
        technicians = await extractor.extract_technician_data()
        logger.info(f"✅ Extracted {len(technicians)} technicians")
        
        # Show sample data
        if tickets:
            sample_ticket = tickets[0]
            logger.info(f"Sample ticket: {sample_ticket.get('title', 'N/A')} - {sample_ticket.get('status', 'N/A')}")
        
        if clients:
            sample_client = clients[0]
            logger.info(f"Sample client: {sample_client.get('name', 'N/A')} - {sample_client.get('contract_tier', 'N/A')}")
        
        if technicians:
            sample_tech = technicians[0]
            logger.info(f"Sample technician: {sample_tech.get('name', 'N/A')} - {sample_tech.get('skill_level', 'N/A')}")
        
        # Close extractor
        await extractor.close()
        logger.info("✅ Data extraction completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Data extraction failed: {e}")


async def example_comprehensive_extraction():
    """Example: Comprehensive data extraction"""
    logger.info("\n🔍 Example: Comprehensive Data Extraction")
    logger.info("-" * 40)
    
    try:
        # Create data extractor
        extractor = create_data_extractor()
        await extractor.initialize()
        
        # Extract all data types
        logger.info("Extracting all data types...")
        all_data = await extractor.extract_all_data(
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now()
        )
        
        # Show results
        metadata = all_data.get('extraction_metadata', {})
        logger.info(f"✅ Comprehensive extraction completed")
        logger.info(f"Total records: {metadata.get('total_records', 0)}")
        logger.info(f"Extraction duration: {metadata.get('extraction_duration', 0):.2f}s")
        logger.info(f"Data types extracted:")
        
        for data_type, data_list in all_data.items():
            if isinstance(data_list, list):
                logger.info(f"  - {data_type}: {len(data_list)} records")
        
        # Close extractor
        await extractor.close()
        logger.info("✅ Comprehensive extraction completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Comprehensive extraction failed: {e}")


async def example_real_time_streaming():
    """Example: Real-time data streaming"""
    logger.info("\n🔍 Example: Real-time Data Streaming")
    logger.info("-" * 40)
    
    try:
        # Create streaming configuration
        config = StreamingConfig(
            update_interval=5,  # 5 seconds for demo
            max_buffer_size=50,
            websocket_port=8765,
            enable_websocket=True,
            enable_webhook=False
        )
        
        # Create streaming service
        streaming_service = create_streaming_service(config)
        
        # Start streaming service
        logger.info("Starting real-time streaming service...")
        await streaming_service.start()
        
        # Let it run for a short time
        logger.info("Collecting streaming data for 15 seconds...")
        await asyncio.sleep(15)
        
        # Get stream data
        logger.info("Retrieving stream data...")
        
        # Real-time metrics
        realtime_data = streaming_service.get_stream_data("realtime_metrics", 5)
        logger.info(f"✅ Retrieved {len(realtime_data)} real-time metrics")
        
        # Ticket updates
        ticket_updates = streaming_service.get_stream_data("ticket_updates", 5)
        logger.info(f"✅ Retrieved {len(ticket_updates)} ticket updates")
        
        # SLA alerts
        sla_alerts = streaming_service.get_stream_data("sla_alerts", 5)
        logger.info(f"✅ Retrieved {len(sla_alerts)} SLA alerts")
        
        # System health
        system_health = streaming_service.get_stream_data("system_health", 5)
        logger.info(f"✅ Retrieved {len(system_health)} system health updates")
        
        # Show stream status
        status = streaming_service.get_all_streams_status()
        logger.info("Stream status:")
        for stream_id, stream_status in status.items():
            logger.info(f"  - {stream_id}: {stream_status['update_count']} updates, buffer size: {stream_status['buffer_size']}")
        
        # Stop streaming service
        logger.info("Stopping streaming service...")
        await streaming_service.stop()
        logger.info("✅ Real-time streaming completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Real-time streaming failed: {e}")


async def example_predictions():
    """Example: Making predictions"""
    logger.info("\n🔍 Example: Making Predictions")
    logger.info("-" * 40)
    
    try:
        # Create predictor
        predictor = create_predictor()
        
        # Example client data for prediction
        client_data = {
            "client_id": "CLIENT-001",
            "features": {
                "monthly_spend": 5000.0,
                "service_tier": "premium",
                "contract_value": 60000.0,
                "ticket_count": 25,
                "avg_resolution_time": 2.5,
                "customer_satisfaction": 4.2
            }
        }
        
        # Make profitability prediction
        logger.info("Making profitability prediction...")
        profitability_result = await predictor.predict_profitability(client_data)
        logger.info(f"✅ Profitability prediction completed")
        logger.info(f"  Prediction value: {profitability_result.prediction_value:.3f}")
        logger.info(f"  Confidence: {profitability_result.confidence:.3f}")
        logger.info(f"  Explanation: {profitability_result.explanation}")
        
        # Make churn prediction
        logger.info("Making churn prediction...")
        churn_result = await predictor.predict_churn(client_data)
        logger.info(f"✅ Churn prediction completed")
        logger.info(f"  Prediction value: {churn_result.prediction_value:.3f}")
        logger.info(f"  Confidence: {churn_result.confidence:.3f}")
        logger.info(f"  Explanation: {churn_result.explanation}")
        
        # Make revenue leak detection
        logger.info("Making revenue leak detection...")
        leak_result = await predictor.detect_revenue_leak(client_data)
        logger.info(f"✅ Revenue leak detection completed")
        logger.info(f"  Prediction value: {leak_result.prediction_value:.3f}")
        logger.info(f"  Confidence: {leak_result.confidence:.3f}")
        logger.info(f"  Explanation: {leak_result.explanation}")
        
        # Make dynamic pricing recommendation
        logger.info("Making dynamic pricing recommendation...")
        pricing_result = await predictor.get_dynamic_pricing(client_data)
        logger.info(f"✅ Dynamic pricing recommendation completed")
        logger.info(f"  Prediction value: {pricing_result.prediction_value:.3f}")
        logger.info(f"  Confidence: {pricing_result.confidence:.3f}")
        logger.info(f"  Explanation: {pricing_result.explanation}")
        
        logger.info("✅ All predictions completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Predictions failed: {e}")


async def example_data_quality_check():
    """Example: Data quality validation"""
    logger.info("\n🔍 Example: Data Quality Validation")
    logger.info("-" * 40)
    
    try:
        # Create data extractor
        extractor = create_data_extractor()
        await extractor.initialize()
        
        # Extract sample data
        tickets = await extractor.extract_ticket_data(limit=20)
        clients = await extractor.extract_client_data(limit=10)
        technicians = await extractor.extract_technician_data(limit=5)
        
        # Check data quality
        logger.info("Performing data quality checks...")
        
        # Ticket data quality
        ticket_quality_issues = []
        for ticket in tickets:
            if not ticket.get("id"):
                ticket_quality_issues.append("Missing ticket ID")
            if not ticket.get("title"):
                ticket_quality_issues.append("Missing ticket title")
            if not ticket.get("status"):
                ticket_quality_issues.append("Missing ticket status")
        
        logger.info(f"✅ Ticket data quality: {len(ticket_quality_issues)} issues found")
        
        # Client data quality
        client_quality_issues = []
        for client in clients:
            if not client.get("id"):
                client_quality_issues.append("Missing client ID")
            if not client.get("name"):
                client_quality_issues.append("Missing client name")
            if not client.get("contract_value"):
                client_quality_issues.append("Missing contract value")
        
        logger.info(f"✅ Client data quality: {len(client_quality_issues)} issues found")
        
        # Technician data quality
        tech_quality_issues = []
        for tech in technicians:
            if not tech.get("id"):
                tech_quality_issues.append("Missing technician ID")
            if not tech.get("name"):
                tech_quality_issues.append("Missing technician name")
            if not tech.get("hourly_rate"):
                tech_quality_issues.append("Missing hourly rate")
        
        logger.info(f"✅ Technician data quality: {len(tech_quality_issues)} issues found")
        
        # Data completeness
        total_fields = 0
        populated_fields = 0
        
        for ticket in tickets[:5]:  # Check first 5 tickets
            for key, value in ticket.items():
                total_fields += 1
                if value is not None and value != "":
                    populated_fields += 1
        
        completeness_ratio = populated_fields / total_fields if total_fields > 0 else 0
        logger.info(f"✅ Data completeness: {completeness_ratio:.2%} ({populated_fields}/{total_fields} fields)")
        
        # Close extractor
        await extractor.close()
        logger.info("✅ Data quality validation completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Data quality validation failed: {e}")


async def main():
    """Main function to run all examples"""
    logger.info("🚀 SuperHack AI/ML System - Basic Usage Examples")
    logger.info("=" * 60)
    
    # Run examples
    examples = [
        ("Data Extraction", example_data_extraction),
        ("Comprehensive Extraction", example_comprehensive_extraction),
        ("Real-time Streaming", example_real_time_streaming),
        ("Predictions", example_predictions),
        ("Data Quality Check", example_data_quality_check)
    ]
    
    for example_name, example_func in examples:
        try:
            await example_func()
        except Exception as e:
            logger.error(f"❌ {example_name} example failed: {e}")
    
    logger.info("\n🎉 All examples completed!")
    logger.info("Check the logs above for detailed results.")


if __name__ == "__main__":
    asyncio.run(main())
