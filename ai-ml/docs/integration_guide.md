# Data Preprocessing Pipeline Integration Guide

## Overview

This guide explains how to integrate the Data Preprocessing Pipeline with the existing data extraction system in the SuperHack AI/ML layer.

## Integration Architecture

The preprocessing pipeline is designed to work seamlessly with the existing data extraction system. The typical data flow is:

1. **Data Extraction**: Use the `ComprehensiveDataExtractor` to extract raw data from all sources
2. **Data Conversion**: Convert extracted data to pandas DataFrames
3. **Preprocessing**: Apply the preprocessing pipeline to clean and transform the data
4. **Validation**: Validate the processed data quality
5. **ML Pipeline**: Feed the processed data to machine learning models

## Integration Examples

### Basic Integration

```python
import asyncio
import pandas as pd
from datetime import datetime, timedelta

# Import data extraction components
from src.data.ingestion.comprehensive_extractor import create_comprehensive_extractor, ExtractionConfig

# Import preprocessing components
from src.data.preprocessing import preprocess_data

async def basic_integration_example():
    # Step 1: Extract data
    config = ExtractionConfig(
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now(),
        include_superops=True,
        include_quickbooks=True,
        include_internal=True
    )
    
    async with create_comprehensive_extractor(**config.__dict__) as extractor:
        raw_data = await extractor.extract_all_data()
    
    # Step 2: Convert to DataFrames
    tickets_df = pd.DataFrame(raw_data['superops_tickets'])
    clients_df = pd.DataFrame(raw_data['superops_clients'])
    
    # Step 3: Preprocess data
    processed_tickets, ticket_validation = preprocess_data(tickets_df, "ticket")
    processed_clients, client_validation = preprocess_data(clients_df, "client")
    
    # Step 4: Use processed data for ML models
    print(f"Processed {len(processed_tickets)} tickets")
    print(f"Processed {len(processed_clients)} clients")
    
    return processed_tickets, processed_clients

# Run the example
# asyncio.run(basic_integration_example())
```

### Using Individual Preprocessing Modules

```python
import pandas as pd

# Import individual preprocessing modules
from src.data.preprocessing.cleaning import clean_dataframe
from src.data.preprocessing.imputation import impute_missing_values
from src.data.preprocessing.outlier_detection import remove_outliers
from src.data.preprocessing.standardization import standardize_data
from src.data.preprocessing.normalization import normalize_data
from src.data.preprocessing.feature_engineering import engineer_features
from src.data.preprocessing.validation import validate_data

def modular_preprocessing_example(df):
    """Example of using individual preprocessing modules"""
    
    # 1. Clean the data
    cleaned_df = clean_dataframe(df, remove_duplicates=True)
    
    # 2. Handle missing values
    imputation_config = {
        'mean_cols': ['numeric_column1', 'numeric_column2'],
        'mode_cols': ['categorical_column1']
    }
    imputed_df = impute_missing_values(cleaned_df, imputation_config)
    
    # 3. Remove outliers
    outlier_config = {
        'zscore_cols': ['numeric_column1', 'numeric_column2']
    }
    cleaned_df, outliers = remove_outliers(imputed_df, outlier_config)
    
    # 4. Standardize data formats
    standardization_config = {
        'datetime_columns': {'date_column': '%Y-%m-%d'},
        'currency_columns': ['price_column']
    }
    standardized_df = standardize_data(cleaned_df, standardization_config)
    
    # 5. Normalize numerical features
    normalization_config = {
        'standard_cols': ['numeric_column1', 'numeric_column2']
    }
    normalized_df = normalize_data(standardized_df, normalization_config)
    
    # 6. Engineer new features
    feature_config = {
        'one_hot_encode_cols': ['categorical_column1'],
        'time_based_features': {'date_column': '%Y-%m-%d'},
        'ratio_features': [('column1', 'column2', 'ratio_column')]
    }
    engineered_df = engineer_features(normalized_df, feature_config)
    
    # 7. Validate the processed data
    validation_config = {
        'expected_schema': {
            'id': 'int64',
            'numeric_column1': 'float64',
            'categorical_column1': 'object'
        },
        'range_validations': {
            'numeric_column1': {'min': 0, 'max': 100}
        }
    }
    validation_results = validate_data(engineered_df, validation_config)
    
    return engineered_df, validation_results
```

### Integration with ML Training Pipeline

```python
import asyncio
import pandas as pd
from datetime import datetime, timedelta

from src.data.ingestion.comprehensive_extractor import create_comprehensive_extractor, ExtractionConfig
from src.data.preprocessing import preprocess_data

class MLTrainingPipeline:
    """Example ML training pipeline integration"""
    
    def __init__(self):
        self.processed_data = {}
    
    async def prepare_training_data(self):
        """Extract and preprocess data for ML training"""
        
        # Extract raw data
        config = ExtractionConfig(
            start_date=datetime.now() - timedelta(days=365),  # 1 year of data
            end_date=datetime.now(),
            include_superops=True,
            include_quickbooks=True,
            include_internal=True
        )
        
        async with create_comprehensive_extractor(**config.__dict__) as extractor:
            raw_data = await extractor.extract_all_data()
        
        # Process different data types
        if 'superops_tickets' in raw_data:
            tickets_df = pd.DataFrame(raw_data['superops_tickets'])
            self.processed_data['tickets'], _ = preprocess_data(tickets_df, "ticket")
        
        if 'superops_clients' in raw_data:
            clients_df = pd.DataFrame(raw_data['superops_clients'])
            self.processed_data['clients'], _ = preprocess_data(clients_df, "client")
        
        if 'quickbooks_invoices' in raw_data:
            invoices_df = pd.DataFrame(raw_data['quickbooks_invoices'])
            self.processed_data['invoices'], _ = preprocess_data(invoices_df, "invoice")
        
        return self.processed_data
    
    def get_features_and_targets(self, data_type="tickets"):
        """Extract features and targets for ML models"""
        if data_type not in self.processed_data:
            raise ValueError(f"No processed data for {data_type}")
        
        df = self.processed_data[data_type]
        
        # Example feature extraction (customize based on your needs)
        if data_type == "tickets":
            # Features for ticket resolution time prediction
            feature_columns = ['priority', 'technician_id', 'service_type']
            target_column = 'resolution_time_hours'
        elif data_type == "clients":
            # Features for client churn prediction
            feature_columns = ['contract_value', 'service_utilization_rate', 'satisfaction_score']
            target_column = 'churn_probability'
        else:
            feature_columns = []
            target_column = None
        
        if target_column and target_column in df.columns:
            features = df[feature_columns]
            targets = df[target_column]
            return features, targets
        else:
            return df[feature_columns], None

# Usage example
async def run_ml_pipeline():
    pipeline = MLTrainingPipeline()
    processed_data = await pipeline.prepare_training_data()
    
    # Get features for ticket resolution prediction
    ticket_features, ticket_targets = pipeline.get_features_and_targets("tickets")
    
    print(f"Prepared {len(ticket_features)} ticket records for training")
    print(f"Feature columns: {list(ticket_features.columns)}")
    
    return processed_data

# asyncio.run(run_ml_pipeline())
```

## Best Practices for Integration

### 1. Error Handling

```python
from src.data.preprocessing import preprocess_data

def safe_preprocessing(df, data_type):
    """Safely preprocess data with proper error handling"""
    try:
        processed_df, validation_results = preprocess_data(df, data_type)
        
        if not validation_results.get('is_valid', True):
            print(f"Warning: Data validation issues found: {validation_results.get('issues', [])}")
        
        return processed_df, validation_results
    
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        # Return original data or handle error appropriately
        return df, {'is_valid': False, 'issues': [str(e)]}
```

### 2. Configuration Management

```python
import json

def load_preprocessing_config(config_file_path):
    """Load preprocessing configuration from file"""
    with open(config_file_path, 'r') as f:
        config = json.load(f)
    return config

def configurable_preprocessing(df, config):
    """Apply preprocessing based on configuration"""
    # Apply cleaning
    if 'cleaning' in config:
        from src.data.preprocessing.cleaning import clean_dataframe
        df = clean_dataframe(df, **config['cleaning'])
    
    # Apply imputation
    if 'imputation' in config:
        from src.data.preprocessing.imputation import impute_missing_values
        df = impute_missing_values(df, config['imputation'])
    
    # Continue with other steps...
    
    return df
```

### 3. Performance Optimization

```python
import pandas as pd

def batch_preprocessing(dataframes, batch_size=1000):
    """Process large datasets in batches to manage memory"""
    processed_batches = []
    
    for i in range(0, len(dataframes), batch_size):
        batch = dataframes[i:i+batch_size]
        # Process batch
        processed_batch, _ = preprocess_data(batch, "ticket")
        processed_batches.append(processed_batch)
    
    # Combine all batches
    final_df = pd.concat(processed_batches, ignore_index=True)
    return final_df
```

## Common Integration Scenarios

### 1. Real-time Data Processing

```python
async def real_time_preprocessing(streaming_data):
    """Process streaming data in real-time"""
    # Convert streaming data to DataFrame
    df = pd.DataFrame([streaming_data])
    
    # Apply lightweight preprocessing
    processed_df, validation = preprocess_data(df, "ticket")
    
    # Send to real-time ML model
    return processed_df
```

### 2. Batch Processing for Model Training

```python
def batch_training_preprocessing():
    """Comprehensive preprocessing for model training"""
    # Extract large historical dataset
    # Apply full preprocessing pipeline
    # Validate data quality
    # Save processed data for training
    pass
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the Python path includes the `src` directory
2. **Data Type Mismatches**: Check that DataFrame columns match expected types
3. **Memory Issues**: Use batch processing for large datasets
4. **Validation Failures**: Review data quality and adjust preprocessing parameters

### Debugging Tips

```python
import logging

# Enable detailed logging
logging.basicConfig(level=logging.INFO)

# Check data shapes and types
def debug_dataframe(df, name="DataFrame"):
    print(f"{name} shape: {df.shape}")
    print(f"{name} columns: {list(df.columns)}")
    print(f"{name} dtypes:\n{df.dtypes}")
    print(f"{name} sample:\n{df.head()}")
```

## Next Steps

1. Review the preprocessing pipeline documentation
2. Test integration with sample data
3. Customize preprocessing configurations for your specific use cases
4. Monitor data quality metrics
5. Iterate and improve the preprocessing pipeline based on ML model performance