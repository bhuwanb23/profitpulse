"""
Command Line Interface for SuperHack AI/ML System
"""

import asyncio
import argparse
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from data.ingestion import extract_data
from data.preprocessing import preprocess_data

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False):
    """Set up logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.getLogger().setLevel(level)


async def test_ingestion(args):
    """Test data ingestion"""
    logger.info("Testing data ingestion...")
    
    try:
        # Extract data from all sources
        all_data = await extract_data()
        
        logger.info("Data extraction results:")
        for source, df in all_data.items():
            logger.info(f"  {source}: {len(df)} rows, {len(df.columns)} columns")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in data ingestion: {e}")
        return False


def test_preprocessing(args):
    """Test data preprocessing"""
    logger.info("Testing data preprocessing...")
    
    try:
        # Import pandas here to avoid import issues
        import pandas as pd
        
        # Create sample data
        sample_data = {
            'ticket': {
                'id': [f'ticket_{i}' for i in range(1, 6)],
                'title': [f'Sample Ticket {i}' for i in range(1, 6)],
                'status': ['Open', 'In Progress', 'Closed', 'Open', 'Closed'],
                'priority': ['Low', 'Medium', 'High', 'Low', 'Critical'],
                'created_at': [(datetime.now() - timedelta(days=i)).isoformat() for i in range(1, 6)],
                'hours_logged': [2.5, 4.0, 1.5, 3.0, 6.0],
                'billing_amount': [150.0, 240.0, 90.0, 180.0, 360.0]
            },
            'client': {
                'id': [f'client_{i}' for i in range(1, 4)],
                'name': [f'Client Company {i}' for i in range(1, 4)],
                'email': [f'client{i}@company{i}.com' for i in range(1, 4)],
                'status': ['Active', 'Active', 'Inactive'],
                'contract_value': [5000.0, 12000.0, 8000.0],
                'created_at': [(datetime.now() - timedelta(days=i*30)).isoformat() for i in range(1, 4)]
            }
        }
        
        # Test each data type
        for data_type, data_dict in sample_data.items():
            logger.info(f"Processing {data_type} data...")
            df = pd.DataFrame(data_dict)
            
            processed_df, validation_results = preprocess_data(df, data_type)
            
            logger.info(f"  Original: {len(df)} rows, {len(df.columns)} columns")
            logger.info(f"  Processed: {len(processed_df)} rows, {len(processed_df.columns)} columns")
            logger.info(f"  Validation: {validation_results['is_valid']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in data preprocessing: {e}")
        return False


async def run_pipeline(args):
    """Run the complete data pipeline"""
    logger.info("Running complete data pipeline...")
    
    try:
        # Step 1: Extract data
        logger.info("Step 1: Extracting data...")
        all_data = await extract_data()
        
        # Step 2: Process each dataset
        logger.info("Step 2: Processing data...")
        processed_data = {}
        
        for source, df in all_data.items():
            if df.empty:
                continue
                
            # Determine data type based on source name
            if 'ticket' in source.lower():
                data_type = 'ticket'
            elif 'client' in source.lower():
                data_type = 'client'
            elif 'invoice' in source.lower():
                data_type = 'invoice'
            else:
                data_type = 'ticket'  # default
            
            logger.info(f"Processing {source} as {data_type} data...")
            processed_df, validation_results = preprocess_data(df, data_type)
            processed_data[source] = processed_df
            
            logger.info(f"  Processed: {len(processed_df)} rows, {len(processed_df.columns)} columns")
        
        logger.info(f"Pipeline completed. Processed {len(processed_data)} datasets.")
        return True
        
    except Exception as e:
        logger.error(f"Error in pipeline: {e}")
        return False


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="SuperHack AI/ML System CLI")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Test ingestion command
    test_ingestion_parser = subparsers.add_parser("test-ingestion", help="Test data ingestion")
    
    # Test preprocessing command
    test_preprocessing_parser = subparsers.add_parser("test-preprocessing", help="Test data preprocessing")
    
    # Run pipeline command
    run_pipeline_parser = subparsers.add_parser("run-pipeline", help="Run complete data pipeline")
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    if not args.command:
        parser.print_help()
        return
    
    # Import pandas here to avoid import issues
    import pandas as pd
    
    # Execute command
    if args.command == "test-ingestion":
        success = asyncio.run(test_ingestion(args))
    elif args.command == "test-preprocessing":
        success = test_preprocessing(args)
    elif args.command == "run-pipeline":
        success = asyncio.run(run_pipeline(args))
    else:
        logger.error(f"Unknown command: {args.command}")
        success = False
    
    if success:
        logger.info("✅ Command completed successfully")
        sys.exit(0)
    else:
        logger.error("❌ Command failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
