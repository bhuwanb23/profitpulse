"""
Test script for data ingestion and preprocessing pipeline
"""

import asyncio
import logging
import pandas as pd
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our modules
from src.data.ingestion import DataIngestionManager, extract_data
from src.data.preprocessing import preprocess_data

async def test_data_ingestion():
    """Test data ingestion from all sources"""
    logger.info("Testing data ingestion...")
    
    try:
        # Test extracting all data
        all_data = await extract_data()
        
        logger.info("Data extraction results:")
        for source, df in all_data.items():
            logger.info(f"  {source}: {len(df)} rows, {len(df.columns)} columns")
            if not df.empty:
                logger.info(f"    Columns: {list(df.columns)}")
                logger.info(f"    Sample data:\n{df.head(2)}")
        
        return all_data
        
    except Exception as e:
        logger.error(f"Error in data ingestion test: {e}")
        return None

def test_data_preprocessing():
    """Test data preprocessing pipeline"""
    logger.info("Testing data preprocessing...")
    
    try:
        # Create sample ticket data
        sample_tickets = pd.DataFrame({
            'id': [f'ticket_{i}' for i in range(1, 11)],
            'title': [f'Sample Ticket {i}' for i in range(1, 11)],
            'status': ['Open', 'In Progress', 'Closed', 'Open', 'Closed', 'In Progress', 'Open', 'Closed', 'Open', 'Closed'],
            'priority': ['Low', 'Medium', 'High', 'Low', 'Critical', 'Medium', 'High', 'Low', 'Medium', 'High'],
            'created_at': [(datetime.now() - timedelta(days=i)).isoformat() for i in range(1, 11)],
            'resolved_at': [(datetime.now() - timedelta(days=i-1)).isoformat() if i % 2 == 0 else None for i in range(1, 11)],
            'client_id': [f'client_{i % 5}' for i in range(1, 11)],
            'hours_logged': [2.5, 4.0, 1.5, 3.0, 6.0, 2.0, 5.5, 1.0, 4.5, 3.5],
            'billing_amount': [150.0, 240.0, 90.0, 180.0, 360.0, 120.0, 330.0, 60.0, 270.0, 210.0]
        })
        
        logger.info(f"Original ticket data: {len(sample_tickets)} rows")
        logger.info(f"Original columns: {list(sample_tickets.columns)}")
        
        # Process ticket data
        processed_tickets, validation_results = preprocess_data(sample_tickets, "ticket")
        
        logger.info(f"Processed ticket data: {len(processed_tickets)} rows")
        logger.info(f"Processed columns: {list(processed_tickets.columns)}")
        logger.info(f"Validation results: {validation_results}")
        
        # Create sample client data
        sample_clients = pd.DataFrame({
            'id': [f'client_{i}' for i in range(1, 6)],
            'name': [f'Client Company {i}' for i in range(1, 6)],
            'email': [f'client{i}@company{i}.com' for i in range(1, 6)],
            'phone': [f'+1-555-{i:04d}' for i in range(1, 6)],
            'status': ['Active', 'Active', 'Inactive', 'Active', 'Active'],
            'contract_value': [5000.0, 12000.0, 8000.0, 15000.0, 25000.0],
            'created_at': [(datetime.now() - timedelta(days=i*30)).isoformat() for i in range(1, 6)],
            'last_contact': [(datetime.now() - timedelta(days=i*7)).isoformat() for i in range(1, 6)]
        })
        
        logger.info(f"Original client data: {len(sample_clients)} rows")
        logger.info(f"Original columns: {list(sample_clients.columns)}")
        
        # Process client data
        processed_clients, validation_results = preprocess_data(sample_clients, "client")
        
        logger.info(f"Processed client data: {len(processed_clients)} rows")
        logger.info(f"Processed columns: {list(processed_clients.columns)}")
        logger.info(f"Validation results: {validation_results}")
        
        return processed_tickets, processed_clients
        
    except Exception as e:
        logger.error(f"Error in data preprocessing test: {e}")
        return None, None

async def main():
    """Main test function"""
    logger.info("Starting SuperHack AI/ML Data Pipeline Test")
    logger.info("=" * 50)
    
    # Test data ingestion
    logger.info("\n1. Testing Data Ingestion")
    logger.info("-" * 30)
    all_data = await test_data_ingestion()
    
    if all_data:
        logger.info("✅ Data ingestion test passed")
    else:
        logger.error("❌ Data ingestion test failed")
    
    # Test data preprocessing
    logger.info("\n2. Testing Data Preprocessing")
    logger.info("-" * 30)
    processed_tickets, processed_clients = test_data_preprocessing()
    
    if processed_tickets is not None and processed_clients is not None:
        logger.info("✅ Data preprocessing test passed")
    else:
        logger.error("❌ Data preprocessing test failed")
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("Test Summary:")
    logger.info(f"  Data ingestion: {'✅ PASSED' if all_data else '❌ FAILED'}")
    logger.info(f"  Data preprocessing: {'✅ PASSED' if processed_tickets is not None else '❌ FAILED'}")
    
    if all_data and processed_tickets is not None:
        logger.info("\n🎉 All tests passed! Data pipeline is working correctly.")
    else:
        logger.error("\n💥 Some tests failed. Please check the logs above.")

if __name__ == "__main__":
    asyncio.run(main())
