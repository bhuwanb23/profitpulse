"""
Comprehensive test for Phase 2.1: Complete Data Ingestion System
Tests all three data sources: SuperOps, QuickBooks, and Internal Database
"""

import asyncio
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.quickbooks_client import create_quickbooks_client
from data.internal_db_connector import create_internal_db_connector
from data.comprehensive_extractor import create_comprehensive_extractor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_quickbooks_client():
    """Test QuickBooks API client functionality"""
    logger.info("🧪 Testing QuickBooks API Client")
    logger.info("-" * 50)
    
    try:
        # Create QuickBooks client
        client = create_quickbooks_client()
        await client.initialize()
        
        # Test financial transactions extraction
        logger.info("Testing financial transactions extraction...")
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        transactions = await client.get_financial_transactions(start_date, end_date, limit=10)
        logger.info(f"✅ Extracted {len(transactions)} financial transactions")
        
        if transactions:
            sample_transaction = transactions[0]
            logger.info(f"Sample transaction: {sample_transaction.get('description', 'N/A')} - ${sample_transaction.get('amount', 0)}")
        
        # Test invoices and payments extraction
        logger.info("Testing invoices and payments extraction...")
        invoices_payments = await client.get_invoices_and_payments(start_date, end_date, limit=10)
        logger.info(f"✅ Extracted {len(invoices_payments.get('invoices', []))} invoices and {len(invoices_payments.get('payments', []))} payments")
        
        # Test expenses extraction
        logger.info("Testing expenses extraction...")
        expenses = await client.get_expenses_and_costs(start_date, end_date, limit=10)
        logger.info(f"✅ Extracted {len(expenses)} expenses")
        
        # Test customer profiles extraction
        logger.info("Testing customer profiles extraction...")
        profiles = await client.get_customer_financial_profiles(limit=10)
        logger.info(f"✅ Extracted {len(profiles)} customer profiles")
        
        if profiles:
            sample_profile = profiles[0]
            logger.info(f"Sample customer: {sample_profile.get('customer_name', 'N/A')} - ${sample_profile.get('financial_summary', {}).get('total_invoiced', 0)}")
        
        # Test real-time updates
        logger.info("Testing real-time financial updates...")
        update_count = 0
        async for update in client.get_real_time_financial_updates():
            update_count += 1
            logger.info(f"✅ Real-time update {update_count}: {update.get('type', 'N/A')}")
            if update_count >= 3:  # Test 3 updates
                break
        
        await client.close()
        logger.info("✅ QuickBooks client tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ QuickBooks client tests failed: {e}")
        return False


async def test_internal_db_connector():
    """Test internal database connector functionality"""
    logger.info("\n🧪 Testing Internal Database Connector")
    logger.info("-" * 50)
    
    try:
        # Create internal database connector
        connector = create_internal_db_connector()
        await connector.initialize()
        
        # Test client profiles extraction
        logger.info("Testing client profiles extraction...")
        profiles = await connector.get_client_profiles(limit=10)
        logger.info(f"✅ Extracted {len(profiles)} client profiles")
        
        if profiles:
            sample_profile = profiles[0]
            logger.info(f"Sample client: {sample_profile.get('name', 'N/A')} - {sample_profile.get('contract_tier', 'N/A')}")
        
        # Test service history extraction
        logger.info("Testing service history extraction...")
        service_history = await connector.get_service_history_and_preferences(limit=10)
        logger.info(f"✅ Extracted {len(service_history)} service history records")
        
        # Test satisfaction scores extraction
        logger.info("Testing satisfaction scores extraction...")
        satisfaction = await connector.get_satisfaction_scores(limit=10)
        logger.info(f"✅ Extracted {len(satisfaction)} satisfaction scores")
        
        if satisfaction:
            sample_score = satisfaction[0]
            logger.info(f"Sample satisfaction: {sample_score.get('overall_score', 0)}/5.0 - {sample_score.get('client_name', 'N/A')}")
        
        # Test communication engagement extraction
        logger.info("Testing communication engagement extraction...")
        communications = await connector.get_communication_engagement_data(limit=10)
        logger.info(f"✅ Extracted {len(communications)} communication records")
        
        # Test contract data extraction
        logger.info("Testing contract data extraction...")
        contracts = await connector.get_contract_and_renewal_data(limit=10)
        logger.info(f"✅ Extracted {len(contracts)} contract records")
        
        if contracts:
            sample_contract = contracts[0]
            logger.info(f"Sample contract: {sample_contract.get('contract_type', 'N/A')} - ${sample_contract.get('contract_value', 0)}")
        
        # Test comprehensive data extraction
        logger.info("Testing comprehensive internal data extraction...")
        all_data = await connector.get_all_internal_data()
        total_records = sum(len(data) for data in all_data.values() if isinstance(data, list))
        logger.info(f"✅ Extracted {total_records} total internal records across {len(all_data)} data types")
        
        await connector.close()
        logger.info("✅ Internal database connector tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Internal database connector tests failed: {e}")
        return False


async def test_comprehensive_extractor():
    """Test comprehensive data extractor functionality"""
    logger.info("\n🧪 Testing Comprehensive Data Extractor")
    logger.info("-" * 50)
    
    try:
        # Create comprehensive extractor
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        extractor = create_comprehensive_extractor(
            start_date=start_date,
            end_date=end_date,
            include_superops=True,
            include_quickbooks=True,
            include_internal=True,
            max_records_per_source=50,
            parallel_extraction=True
        )
        
        await extractor.initialize()
        
        # Test comprehensive data extraction
        logger.info("Testing comprehensive data extraction...")
        all_data = await extractor.extract_all_data()
        
        # Analyze results
        metadata = all_data.get("extraction_metadata", {})
        total_records = metadata.get("total_records", 0)
        duration = metadata.get("duration_seconds", 0)
        
        logger.info(f"✅ Comprehensive extraction completed in {duration:.2f}s")
        logger.info(f"✅ Total records extracted: {total_records}")
        
        # Show breakdown by source
        sources = ["superops", "quickbooks", "internal"]
        for source in sources:
            source_records = 0
            for key, value in all_data.items():
                if key.startswith(source) and isinstance(value, list):
                    source_records += len(value)
            logger.info(f"  - {source.capitalize()}: {source_records} records")
        
        # Test client-specific extraction
        logger.info("Testing client-specific data extraction...")
        client_data = await extractor.extract_client_specific_data("CLIENT-001")
        client_records = sum(len(data) for data in client_data.values() if isinstance(data, list))
        logger.info(f"✅ Client-specific extraction: {client_records} records for CLIENT-001")
        
        # Test real-time updates
        logger.info("Testing real-time updates...")
        update_count = 0
        async for update in extractor.get_real_time_updates():
            update_count += 1
            logger.info(f"✅ Real-time update {update_count}: {update.get('data', {}).get('type', 'N/A')}")
            if update_count >= 3:  # Test 3 updates
                break
        
        await extractor.close()
        logger.info("✅ Comprehensive extractor tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Comprehensive extractor tests failed: {e}")
        return False


async def test_data_quality_and_validation():
    """Test data quality and validation"""
    logger.info("\n🧪 Testing Data Quality and Validation")
    logger.info("-" * 50)
    
    try:
        # Test QuickBooks data quality
        logger.info("Testing QuickBooks data quality...")
        client = create_quickbooks_client()
        await client.initialize()
        
        transactions = await client.get_financial_transactions(
            datetime.now() - timedelta(days=7),
            datetime.now(),
            limit=20
        )
        
        # Validate transaction data
        quality_issues = []
        for transaction in transactions:
            if not transaction.get("id"):
                quality_issues.append("Missing transaction ID")
            if not transaction.get("amount"):
                quality_issues.append("Missing transaction amount")
            if not transaction.get("date"):
                quality_issues.append("Missing transaction date")
        
        logger.info(f"✅ QuickBooks data quality: {len(quality_issues)} issues found")
        
        await client.close()
        
        # Test internal database data quality
        logger.info("Testing internal database data quality...")
        connector = create_internal_db_connector()
        await connector.initialize()
        
        profiles = await connector.get_client_profiles(limit=20)
        
        # Validate profile data
        quality_issues = []
        for profile in profiles:
            if not profile.get("id"):
                quality_issues.append("Missing client ID")
            if not profile.get("name"):
                quality_issues.append("Missing client name")
            if not profile.get("contract_tier"):
                quality_issues.append("Missing contract tier")
        
        logger.info(f"✅ Internal database data quality: {len(quality_issues)} issues found")
        
        await connector.close()
        
        logger.info("✅ Data quality and validation tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Data quality and validation tests failed: {e}")
        return False


async def test_performance_and_scalability():
    """Test performance and scalability"""
    logger.info("\n🧪 Testing Performance and Scalability")
    logger.info("-" * 50)
    
    try:
        # Test parallel vs sequential extraction
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        
        # Parallel extraction
        logger.info("Testing parallel extraction...")
        parallel_extractor = create_comprehensive_extractor(
            start_date=start_date,
            end_date=end_date,
            max_records_per_source=100,
            parallel_extraction=True
        )
        
        await parallel_extractor.initialize()
        parallel_start = datetime.now()
        parallel_data = await parallel_extractor.extract_all_data()
        parallel_duration = (datetime.now() - parallel_start).total_seconds()
        await parallel_extractor.close()
        
        # Sequential extraction
        logger.info("Testing sequential extraction...")
        sequential_extractor = create_comprehensive_extractor(
            start_date=start_date,
            end_date=end_date,
            max_records_per_source=100,
            parallel_extraction=False
        )
        
        await sequential_extractor.initialize()
        sequential_start = datetime.now()
        sequential_data = await sequential_extractor.extract_all_data()
        sequential_duration = (datetime.now() - sequential_start).total_seconds()
        await sequential_extractor.close()
        
        # Compare performance
        speedup = sequential_duration / parallel_duration if parallel_duration > 0 else 1
        logger.info(f"✅ Parallel extraction: {parallel_duration:.2f}s")
        logger.info(f"✅ Sequential extraction: {sequential_duration:.2f}s")
        logger.info(f"✅ Speedup factor: {speedup:.2f}x")
        
        # Test memory usage
        import psutil
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        logger.info(f"✅ Memory usage: {memory_usage:.2f} MB")
        
        logger.info("✅ Performance and scalability tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Performance and scalability tests failed: {e}")
        return False


async def main():
    """Main test function"""
    logger.info("🚀 Starting Phase 2.1 Complete Data Ingestion System Tests")
    logger.info("=" * 80)
    
    test_results = []
    
    # Run all tests
    tests = [
        ("QuickBooks Client", test_quickbooks_client),
        ("Internal Database Connector", test_internal_db_connector),
        ("Comprehensive Extractor", test_comprehensive_extractor),
        ("Data Quality & Validation", test_data_quality_and_validation),
        ("Performance & Scalability", test_performance_and_scalability)
    ]
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            test_results.append((test_name, result))
        except Exception as e:
            logger.error(f"❌ {test_name} test failed with exception: {e}")
            test_results.append((test_name, False))
    
    # Generate summary
    logger.info("\n" + "=" * 80)
    logger.info("📊 Phase 2.1 Complete Test Summary:")
    logger.info("=" * 80)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"  {test_name}: {status}")
        if result:
            passed_tests += 1
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    logger.info(f"\n📈 Overall Results:")
    logger.info(f"  Total Tests: {total_tests}")
    logger.info(f"  Passed: {passed_tests}")
    logger.info(f"  Failed: {total_tests - passed_tests}")
    logger.info(f"  Success Rate: {success_rate:.1f}%")
    
    if passed_tests == total_tests:
        logger.info(f"\n🎉 All {total_tests} tests passed! Phase 2.1 Complete Data Ingestion System is working correctly.")
    else:
        logger.error(f"\n💥 {total_tests - passed_tests} out of {total_tests} tests failed.")
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
