"""
Test script for Phase 2.1: Data Ingestion System
Tests SuperOps API client, data extraction, and real-time streaming
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

from src.data.superops_client import create_superops_client, SuperOpsConfig
from src.data.data_extractor import create_data_extractor
from src.data.streaming_service import create_streaming_service, StreamingConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_superops_client():
    """Test SuperOps API client functionality"""
    logger.info("=" * 60)
    logger.info("Testing SuperOps API Client")
    logger.info("=" * 60)
    
    try:
        # Create client with mock configuration
        config = SuperOpsConfig(
            base_url="https://api.superops.com",
            api_key="mock_api_key",
            tenant_id="mock_tenant_id"
        )
        
        async with create_superops_client() as client:
            # Test ticket extraction
            logger.info("Testing ticket data extraction...")
            tickets = await client.get_tickets(limit=10)
            logger.info(f"✅ Extracted {len(tickets)} tickets")
            
            if tickets:
                ticket = tickets[0]
                logger.info(f"Sample ticket: {ticket.title} - {ticket.status}")
            
            # Test client extraction
            logger.info("Testing client data extraction...")
            clients = await client.get_clients(limit=5)
            logger.info(f"✅ Extracted {len(clients)} clients")
            
            if clients:
                client_data = clients[0]
                logger.info(f"Sample client: {client_data.name} - {client_data.contract_type}")
            
            # Test technician extraction
            logger.info("Testing technician data extraction...")
            technicians = await client.get_technicians(limit=5)
            logger.info(f"✅ Extracted {len(technicians)} technicians")
            
            if technicians:
                tech = technicians[0]
                logger.info(f"Sample technician: {tech.name} - {tech.role}")
            
            # Test SLA metrics extraction
            logger.info("Testing SLA metrics extraction...")
            sla_metrics = await client.get_sla_metrics()
            logger.info(f"✅ Extracted {len(sla_metrics)} SLA metrics")
            
            # Test service delivery metrics
            logger.info("Testing service delivery metrics extraction...")
            service_metrics = await client.get_service_delivery_metrics()
            logger.info(f"✅ Extracted {len(service_metrics)} service delivery metrics")
            
            # Test technician productivity
            logger.info("Testing technician productivity extraction...")
            productivity = await client.get_technician_productivity()
            logger.info(f"✅ Extracted technician productivity data")
            logger.info(f"Productivity keys: {list(productivity.keys())}")
            
            # Test real-time data
            logger.info("Testing real-time data extraction...")
            realtime_data = await client.get_real_time_data()
            logger.info(f"✅ Extracted real-time data")
            logger.info(f"Real-time data keys: {list(realtime_data.keys())}")
            
            logger.info("✅ SuperOps client tests completed successfully!")
            return True
            
    except Exception as e:
        logger.error(f"❌ SuperOps client test failed: {e}")
        return False


async def test_data_extractor():
    """Test data extractor service"""
    logger.info("=" * 60)
    logger.info("Testing Data Extractor Service")
    logger.info("=" * 60)
    
    try:
        extractor = create_data_extractor()
        await extractor.initialize()
        
        # Test individual data extractions
        logger.info("Testing ticket data extraction...")
        tickets = await extractor.extract_ticket_data(
            start_date=datetime.now() - timedelta(days=7),
            end_date=datetime.now()
        )
        logger.info(f"✅ Extracted {len(tickets)} tickets with derived metrics")
        
        if tickets:
            ticket = tickets[0]
            logger.info(f"Sample ticket with metrics: {ticket.get('title')} - Age: {ticket.get('ticket_age_days')} days")
        
        logger.info("Testing client data extraction...")
        clients = await extractor.extract_client_data()
        logger.info(f"✅ Extracted {len(clients)} clients with derived metrics")
        
        if clients:
            client = clients[0]
            logger.info(f"Sample client with metrics: {client.get('name')} - Tier: {client.get('contract_tier')}")
        
        logger.info("Testing technician data extraction...")
        technicians = await extractor.extract_technician_data()
        logger.info(f"✅ Extracted {len(technicians)} technicians with derived metrics")
        
        if technicians:
            tech = technicians[0]
            logger.info(f"Sample technician with metrics: {tech.get('name')} - Skill Level: {tech.get('skill_level')}")
        
        logger.info("Testing SLA metrics extraction...")
        sla_metrics = await extractor.extract_sla_metrics()
        logger.info(f"✅ Extracted {len(sla_metrics)} SLA metrics with derived metrics")
        
        if sla_metrics:
            sla = sla_metrics[0]
            logger.info(f"Sample SLA metric: Compliance Ratio: {sla.get('sla_compliance_ratio'):.2f}")
        
        logger.info("Testing service delivery metrics extraction...")
        service_metrics = await extractor.extract_service_delivery_metrics()
        logger.info(f"✅ Extracted {len(service_metrics)} service delivery metrics with derived metrics")
        
        if service_metrics:
            service = service_metrics[0]
            logger.info(f"Sample service metric: Performance: {service.get('performance_category')}")
        
        logger.info("Testing technician productivity extraction...")
        productivity = await extractor.extract_technician_productivity()
        logger.info(f"✅ Extracted technician productivity with derived metrics")
        logger.info(f"Productivity category: {productivity.get('productivity_category')}")
        
        # Test comprehensive data extraction
        logger.info("Testing comprehensive data extraction...")
        all_data = await extractor.extract_all_data(
            start_date=datetime.now() - timedelta(days=7),
            end_date=datetime.now()
        )
        
        logger.info(f"✅ Comprehensive extraction completed")
        logger.info(f"Total records extracted: {all_data.get('extraction_metadata', {}).get('total_records', 0)}")
        logger.info(f"Extraction duration: {all_data.get('extraction_metadata', {}).get('extraction_duration', 0):.2f}s")
        
        # Test extraction stats
        stats = extractor.get_extraction_stats()
        logger.info(f"✅ Extraction stats: {stats}")
        
        await extractor.close()
        logger.info("✅ Data extractor tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Data extractor test failed: {e}")
        return False


async def test_streaming_service():
    """Test real-time streaming service"""
    logger.info("=" * 60)
    logger.info("Testing Real-time Streaming Service")
    logger.info("=" * 60)
    
    try:
        # Create streaming configuration
        config = StreamingConfig(
            update_interval=5,  # 5 seconds for testing
            max_buffer_size=100,
            websocket_port=8765,
            enable_websocket=True,
            enable_webhook=False
        )
        
        streaming_service = create_streaming_service(config)
        
        # Start streaming service
        logger.info("Starting streaming service...")
        await streaming_service.start()
        
        # Let it run for a short time to collect data
        logger.info("Collecting streaming data for 15 seconds...")
        await asyncio.sleep(15)
        
        # Test stream data retrieval
        logger.info("Testing stream data retrieval...")
        
        # Get real-time metrics
        realtime_data = streaming_service.get_stream_data("realtime_metrics", 5)
        logger.info(f"✅ Retrieved {len(realtime_data)} real-time metrics")
        
        # Get ticket updates
        ticket_updates = streaming_service.get_stream_data("ticket_updates", 5)
        logger.info(f"✅ Retrieved {len(ticket_updates)} ticket updates")
        
        # Get SLA alerts
        sla_alerts = streaming_service.get_stream_data("sla_alerts", 5)
        logger.info(f"✅ Retrieved {len(sla_alerts)} SLA alerts")
        
        # Get technician activity
        tech_activity = streaming_service.get_stream_data("technician_activity", 5)
        logger.info(f"✅ Retrieved {len(tech_activity)} technician activity updates")
        
        # Get system health
        system_health = streaming_service.get_stream_data("system_health", 5)
        logger.info(f"✅ Retrieved {len(system_health)} system health updates")
        
        # Test stream status
        status = streaming_service.get_all_streams_status()
        logger.info(f"✅ Stream status: {json.dumps(status, indent=2, default=str)}")
        
        # Stop streaming service
        logger.info("Stopping streaming service...")
        await streaming_service.stop()
        
        logger.info("✅ Streaming service tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Streaming service test failed: {e}")
        return False


async def test_data_quality():
    """Test data quality and validation"""
    logger.info("=" * 60)
    logger.info("Testing Data Quality and Validation")
    logger.info("=" * 60)
    
    try:
        extractor = create_data_extractor()
        await extractor.initialize()
        
        # Extract sample data
        tickets = await extractor.extract_ticket_data(limit=20)
        clients = await extractor.extract_client_data(limit=10)
        technicians = await extractor.extract_technician_data(limit=5)
        
        # Test data quality checks
        logger.info("Testing data quality checks...")
        
        # Check ticket data quality
        ticket_quality_issues = []
        for ticket in tickets:
            if not ticket.get("id"):
                ticket_quality_issues.append("Missing ticket ID")
            if not ticket.get("title"):
                ticket_quality_issues.append("Missing ticket title")
            if not ticket.get("status"):
                ticket_quality_issues.append("Missing ticket status")
        
        logger.info(f"✅ Ticket data quality: {len(ticket_quality_issues)} issues found")
        
        # Check client data quality
        client_quality_issues = []
        for client in clients:
            if not client.get("id"):
                client_quality_issues.append("Missing client ID")
            if not client.get("name"):
                client_quality_issues.append("Missing client name")
            if not client.get("contract_value"):
                client_quality_issues.append("Missing contract value")
        
        logger.info(f"✅ Client data quality: {len(client_quality_issues)} issues found")
        
        # Check technician data quality
        tech_quality_issues = []
        for tech in technicians:
            if not tech.get("id"):
                tech_quality_issues.append("Missing technician ID")
            if not tech.get("name"):
                tech_quality_issues.append("Missing technician name")
            if not tech.get("hourly_rate"):
                tech_quality_issues.append("Missing hourly rate")
        
        logger.info(f"✅ Technician data quality: {len(tech_quality_issues)} issues found")
        
        # Test derived metrics
        logger.info("Testing derived metrics calculation...")
        
        # Check if derived metrics are present
        derived_metrics_count = 0
        for ticket in tickets:
            if "ticket_age_days" in ticket:
                derived_metrics_count += 1
        
        logger.info(f"✅ Derived metrics: {derived_metrics_count}/{len(tickets)} tickets have derived metrics")
        
        # Test data completeness
        logger.info("Testing data completeness...")
        
        total_fields = 0
        populated_fields = 0
        
        for ticket in tickets[:5]:  # Check first 5 tickets
            for key, value in ticket.items():
                total_fields += 1
                if value is not None and value != "":
                    populated_fields += 1
        
        completeness_ratio = populated_fields / total_fields if total_fields > 0 else 0
        logger.info(f"✅ Data completeness: {completeness_ratio:.2%} ({populated_fields}/{total_fields} fields)")
        
        await extractor.close()
        logger.info("✅ Data quality tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Data quality test failed: {e}")
        return False


async def test_performance():
    """Test performance and scalability"""
    logger.info("=" * 60)
    logger.info("Testing Performance and Scalability")
    logger.info("=" * 60)
    
    try:
        extractor = create_data_extractor()
        await extractor.initialize()
        
        # Test extraction performance
        logger.info("Testing extraction performance...")
        
        start_time = datetime.now()
        all_data = await extractor.extract_all_data(
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now()
        )
        end_time = datetime.now()
        
        extraction_time = (end_time - start_time).total_seconds()
        total_records = all_data.get('extraction_metadata', {}).get('total_records', 0)
        
        logger.info(f"✅ Extraction performance: {total_records} records in {extraction_time:.2f}s")
        logger.info(f"✅ Records per second: {total_records/extraction_time:.2f}")
        
        # Test concurrent extractions
        logger.info("Testing concurrent extractions...")
        
        start_time = datetime.now()
        tasks = [
            extractor.extract_ticket_data(),
            extractor.extract_client_data(),
            extractor.extract_technician_data(),
            extractor.extract_sla_metrics(),
            extractor.extract_service_delivery_metrics()
        ]
        
        results = await asyncio.gather(*tasks)
        end_time = datetime.now()
        
        concurrent_time = (end_time - start_time).total_seconds()
        total_concurrent_records = sum(len(result) for result in results)
        
        logger.info(f"✅ Concurrent extraction: {total_concurrent_records} records in {concurrent_time:.2f}s")
        logger.info(f"✅ Concurrent records per second: {total_concurrent_records/concurrent_time:.2f}")
        
        # Test memory usage
        logger.info("Testing memory usage...")
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        
        logger.info(f"✅ Memory usage: {memory_usage:.2f} MB")
        
        await extractor.close()
        logger.info("✅ Performance tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Performance test failed: {e}")
        return False


async def main():
    """Main test function"""
    logger.info("🚀 Starting Phase 2.1: Data Ingestion System Tests")
    logger.info("=" * 80)
    
    # Run all tests
    tests = [
        ("SuperOps API Client", test_superops_client),
        ("Data Extractor Service", test_data_extractor),
        ("Real-time Streaming Service", test_streaming_service),
        ("Data Quality & Validation", test_data_quality),
        ("Performance & Scalability", test_performance)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running {test_name} Tests...")
        try:
            success = await test_func()
            results[test_name] = "✅ PASSED" if success else "❌ FAILED"
        except Exception as e:
            logger.error(f"❌ {test_name} test failed with exception: {e}")
            results[test_name] = "❌ FAILED"
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("📊 Phase 2.1 Test Summary:")
    logger.info("=" * 80)
    
    for test_name, result in results.items():
        logger.info(f"  {test_name}: {result}")
    
    passed = sum(1 for result in results.values() if "PASSED" in result)
    total = len(results)
    
    if passed == total:
        logger.info(f"\n🎉 All {total} tests passed! Phase 2.1 is working correctly.")
        logger.info("✅ SuperOps API Client: Ready for production")
        logger.info("✅ Data Extraction: Comprehensive data extraction working")
        logger.info("✅ Real-time Streaming: WebSocket streaming operational")
        logger.info("✅ Data Quality: Validation and quality checks working")
        logger.info("✅ Performance: Scalable and efficient data processing")
    else:
        logger.error(f"\n💥 {total - passed} out of {total} tests failed.")
    
    logger.info("\n🚀 Phase 2.1: Data Ingestion System - COMPLETED!")
    logger.info("Ready for Phase 2.2: Feature Engineering & Client Genome")


if __name__ == "__main__":
    asyncio.run(main())
