"""
Example of integrating the preprocessing pipeline with the data extraction system
"""

import asyncio
import pandas as pd
from datetime import datetime, timedelta

# Import the data extraction system
from src.data.ingestion.comprehensive_extractor import create_comprehensive_extractor, ExtractionConfig


async def example_integration():
    """Example showing how to integrate data extraction with preprocessing"""
    
    # Step 1: Extract data using the existing system
    print("Step 1: Extracting data...")
    
    # Configure data extraction
    config = ExtractionConfig(
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now(),
        include_superops=True,
        include_quickbooks=True,
        include_internal=True,
        max_records_per_source=100,
        parallel_extraction=True
    )
    
    # Extract data
    async with create_comprehensive_extractor(**config.__dict__) as extractor:
        raw_data = await extractor.extract_all_data()
    
    print(f"Extracted {raw_data['extraction_metadata']['total_records']} records")
    
    # Step 2: Convert extracted data to DataFrames for preprocessing
    print("\nStep 2: Converting to DataFrames...")
    
    # Convert ticket data to DataFrame (example)
    if 'superops_tickets' in raw_data:
        tickets_df = pd.DataFrame(raw_data['superops_tickets'])
        print(f"Created tickets DataFrame with {len(tickets_df)} rows")
    else:
        # Create sample data for demonstration
        tickets_df = pd.DataFrame({
            'ticket_id': [f'TICK-{i}' for i in range(1, 11)],
            'title': [f'Ticket {i}' for i in range(1, 11)],
            'status': ['Open', 'Closed', 'In Progress', 'Open', 'Closed'] * 2,
            'priority': ['High', 'Medium', 'Low', 'Critical', 'Medium'] * 2,
            'hours_logged': [1.5, 2.0, 3.5, 1.0, 4.0, 2.5, 1.0, 3.0, 2.0, 1.5],
            'billing_amount': [150.0, 200.0, 350.0, 100.0, 400.0, 250.0, 100.0, 300.0, 200.0, 150.0],
            'created_date': pd.date_range('2023-01-01', periods=10)
        })
        print("Created sample tickets DataFrame")
    
    # Step 3: Preprocess the data using our pipeline
    print("\nStep 3: Preprocessing ticket data...")
    
    try:
        # In a real implementation, you would use:
        # pipeline = DataPreprocessingPipeline()
        # processed_tickets_df, validation_results = pipeline.process_ticket_data(tickets_df)
        # For this example, we'll just show the concept
        processed_tickets_df = tickets_df  # Placeholder
        validation_results = {'is_valid': True, 'issues': []}
        
        print(f"Preprocessed DataFrame has {len(processed_tickets_df)} rows")
        print(f"Validation results: {validation_results}")
        
        # Show some sample processed data
        print("\nSample of processed data:")
        print(processed_tickets_df.head())
        
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return
    
    # Step 4: Example of using individual preprocessing modules
    print("\nStep 4: Using individual preprocessing modules...")
    
    # Example: Clean the data
    from src.data.preprocessing.cleaning import clean_dataframe
    cleaned_df = clean_dataframe(tickets_df, remove_duplicates_subset=['title'])
    print(f"Cleaned DataFrame has {len(cleaned_df)} rows")
    
    # Example: Handle missing values
    from src.data.preprocessing.imputation import impute_missing_values
    # Add some missing values for demonstration
    tickets_with_missing = tickets_df.copy()
    tickets_with_missing.loc[0, 'hours_logged'] = None
    tickets_with_missing.loc[2, 'billing_amount'] = None
    
    imputation_strategy = {
        'mean_cols': ['hours_logged', 'billing_amount']
    }
    imputed_df = impute_missing_values(tickets_with_missing, imputation_strategy)
    print("Missing values imputed using mean strategy")
    
    # Example: Remove outliers
    from src.data.preprocessing.outlier_detection import remove_outliers
    outlier_strategy = {
        'zscore_cols': ['hours_logged', 'billing_amount']
    }
    cleaned_df, outliers_df = remove_outliers(tickets_df, outlier_strategy)
    print(f"Removed {len(outliers_df)} outliers")
    
    print("\nIntegration example completed successfully!")


# Example usage in a real application
def integrate_with_ml_pipeline():
    """
    Example of how to integrate preprocessing with ML model training pipeline
    """
    
    async def ml_pipeline():
        # Extract and preprocess data
        config = ExtractionConfig(
            start_date=datetime.now() - timedelta(days=90),
            end_date=datetime.now(),
            include_superops=True,
            include_quickbooks=True,
            include_internal=True
        )
        
        async with create_comprehensive_extractor(**config.__dict__) as extractor:
            raw_data = await extractor.extract_all_data()
        
        # Process different types of data
        results = {}
        
        # Process ticket data
        if 'superops_tickets' in raw_data:
            tickets_df = pd.DataFrame(raw_data['superops_tickets'])
            # In a real implementation, you would use:
            # pipeline = DataPreprocessingPipeline()
            # processed_tickets, ticket_validation = pipeline.process_ticket_data(tickets_df)
            # For this example, we'll just show the concept
            processed_tickets = tickets_df  # Placeholder
            ticket_validation = {'is_valid': True, 'issues': []}
            results['tickets'] = {
                'data': processed_tickets,
                'validation': ticket_validation
            }
        
        # Process client data
        if 'superops_clients' in raw_data:
            clients_df = pd.DataFrame(raw_data['superops_clients'])
            # In a real implementation, you would use:
            # pipeline = DataPreprocessingPipeline()
            # processed_clients, client_validation = pipeline.process_client_data(clients_df)
            # For this example, we'll just show the concept
            processed_clients = clients_df  # Placeholder
            client_validation = {'is_valid': True, 'issues': []}
            results['clients'] = {
                'data': processed_clients,
                'validation': client_validation
            }
        
        # Process invoice data
        if 'quickbooks_invoices' in raw_data:
            invoices_df = pd.DataFrame(raw_data['quickbooks_invoices'])
            # In a real implementation, you would use:
            # pipeline = DataPreprocessingPipeline()
            # processed_invoices, invoice_validation = pipeline.process_invoice_data(invoices_df)
            # For this example, we'll just show the concept
            processed_invoices = invoices_df  # Placeholder
            invoice_validation = {'is_valid': True, 'issues': []}
            results['invoices'] = {
                'data': processed_invoices,
                'validation': invoice_validation
            }
        
        return results
    
    # Run the pipeline
    results = asyncio.run(ml_pipeline())
    
    # Use the processed data for ML model training
    # (This would be implemented based on specific model requirements)
    print("ML pipeline integration example:")
    for data_type, result in results.items():
        print(f"  - {data_type}: {len(result['data'])} records processed")
        print(f"    Validation passed: {result['validation'].get('is_valid', 'N/A')}")
    
    return results


if __name__ == "__main__":
    # Run the integration example
    asyncio.run(example_integration())
    
    print("\n" + "="*50)
    
    # Run the ML pipeline integration example
    integrate_with_ml_pipeline()