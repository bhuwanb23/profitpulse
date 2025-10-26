# Data Preprocessing Pipeline Documentation

## Overview

The Data Preprocessing Pipeline is a comprehensive suite of modules designed to clean, transform, and prepare raw data for machine learning models. This pipeline handles various data quality issues and transforms data into formats suitable for AI/ML analysis.

## Modules

### 1. Data Cleaning (`cleaning.py`)

#### Functions
- `remove_duplicates()`: Removes duplicate rows from DataFrame
- `clean_text_columns()`: Cleans text data by removing special characters and normalizing case
- `validate_data_types()`: Ensures columns have correct data types
- `remove_invalid_entries()`: Removes rows with invalid or corrupted data
- `clean_dataframe()`: Comprehensive cleaning pipeline combining all cleaning operations

#### Example Usage
```python
import pandas as pd
from src.data.preprocessing.cleaning import clean_dataframe

# Create sample data with issues
df = pd.DataFrame({
    'name': ['John Doe', 'Jane Smith', '  Bob Johnson  ', 'John Doe'],
    'age': [25, 30, 35, 25],
    'email': ['john@email.com', 'jane@email.com', 'bob@email.com', 'john@email.com']
})

# Clean the data
cleaned_df = clean_dataframe(df, text_columns=['name'], remove_duplicates_subset=['name', 'age'])
```

### 2. Missing Value Imputation (`imputation.py`)

#### Functions
- `mean_imputation()`: Imputes missing values using column mean
- `median_imputation()`: Imputes missing values using column median
- `mode_imputation()`: Imputes missing values using column mode
- `forward_fill_imputation()`: Forward fills missing values (useful for time series)
- `backward_fill_imputation()`: Backward fills missing values
- `knn_imputation()`: Uses K-Nearest Neighbors for imputation
- `custom_value_imputation()`: Imputes with a custom value
- `impute_missing_values()`: Comprehensive imputation pipeline

#### Example Usage
```python
import pandas as pd
from src.data.preprocessing.imputation import impute_missing_values

# Create sample data with missing values
df = pd.DataFrame({
    'numeric_col': [1.0, 2.0, None, 4.0, 5.0],
    'categorical_col': ['A', 'B', 'A', None, 'A']
})

# Define imputation strategy
strategy = {
    'mean_cols': ['numeric_col'],
    'mode_cols': ['categorical_col']
}

# Apply imputation
imputed_df = impute_missing_values(df, strategy)
```

### 3. Outlier Detection (`outlier_detection.py`)

#### Functions
- `zscore_outlier_detection()`: Detects outliers using Z-score method
- `iqr_outlier_detection()`: Detects outliers using Interquartile Range method
- `percentile_outlier_detection()`: Detects outliers using percentile thresholds
- `isolation_forest_outlier_detection()`: Uses Isolation Forest algorithm for outlier detection
- `remove_outliers()`: Comprehensive outlier detection and removal pipeline

#### Example Usage
```python
import pandas as pd
from src.data.preprocessing.outlier_detection import remove_outliers

# Create sample data with outliers
df = pd.DataFrame({
    'value': [1, 2, 3, 4, 100],  # 100 is an outlier
    'category': ['A', 'B', 'A', 'B', 'A']
})

# Define outlier detection strategy
strategy = {
    'zscore_cols': ['value']
}

# Remove outliers
cleaned_df, outliers_df = remove_outliers(df, strategy)
```

### 4. Data Standardization (`standardization.py`)

#### Functions
- `standardize_datetime_columns()`: Standardizes datetime formats
- `standardize_currency_columns()`: Converts currency strings to numeric values
- `standardize_categorical_values()`: Standardizes categorical value representations
- `standardize_text_columns()`: Standardizes text formatting
- `convert_units()`: Converts between different units of measurement
- `standardize_data()`: Comprehensive standardization pipeline

#### Example Usage
```python
import pandas as pd
from src.data.preprocessing.standardization import standardize_data

# Create sample data with various formats
df = pd.DataFrame({
    'date': ['2023-01-01', '01/02/2023', '2023-01-03'],
    'amount': ['$100.50', '€200.75', '£300.25'],
    'status': ['active', 'Inactive', 'Active']
})

# Define standardization configuration
config = {
    'datetime_columns': {'date': '%Y-%m-%d'},
    'currency_columns': ['amount'],
    'categorical_mappings': {'status': {'active': 'Active', 'inactive': 'Inactive', 'Active': 'Active'}}
}

# Apply standardization
standardized_df = standardize_data(df, config)
```

### 5. Data Normalization (`normalization.py`)

#### Functions
- `min_max_scaling()`: Applies Min-Max scaling to specified range
- `standard_scaling()`: Applies Z-score normalization
- `robust_scaling()`: Uses median and IQR for scaling
- `unit_vector_scaling()`: Normalizes vectors to unit length
- `custom_scaling()`: Applies custom scaling factor
- `normalize_data()`: Comprehensive normalization pipeline

#### Example Usage
```python
import pandas as pd
from src.data.preprocessing.normalization import normalize_data

# Create sample data
df = pd.DataFrame({
    'feature1': [1, 2, 3, 4, 5],
    'feature2': [10, 20, 30, 40, 50],
    'category': ['A', 'B', 'A', 'B', 'A']
})

# Define normalization configuration
config = {
    'min_max_cols': ['feature1'],
    'standard_cols': ['feature2']
}

# Apply normalization
normalized_df = normalize_data(df, config)
```

### 6. Feature Engineering (`feature_engineering.py`)

#### Functions
- `one_hot_encoding()`: Converts categorical variables to binary columns
- `label_encoding()`: Encodes categorical variables as integers
- `create_time_based_features()`: Extracts features from datetime columns
- `create_ratio_features()`: Creates ratio-based features
- `create_polynomial_features()`: Generates polynomial features
- `create_interaction_features()`: Creates interaction terms between features
- `create_binned_features()`: Creates binned/categorical versions of numerical features
- `engineer_features()`: Comprehensive feature engineering pipeline

#### Example Usage
```python
import pandas as pd
from src.data.preprocessing.feature_engineering import engineer_features

# Create sample data
df = pd.DataFrame({
    'category': ['A', 'B', 'A', 'C', 'B'],
    'date': pd.date_range('2023-01-01', periods=5),
    'value1': [1, 2, 3, 4, 5],
    'value2': [10, 20, 30, 40, 50]
})

# Define feature engineering configuration
config = {
    'one_hot_encode_cols': ['category'],
    'time_based_cols': ['date'],
    'ratio_cols': [('value1', 'value2')],
    'polynomial_cols': ['value1'],
    'interaction_cols': [('value1', 'value2')]
}

# Apply feature engineering
engineered_df = engineer_features(df, config)
```

### 7. Data Aggregation (`aggregation.py`)

#### Functions
- `groupby_aggregation()`: Performs groupby operations with custom aggregations
- `time_series_resampling()`: Resamples time series data to different frequencies
- `rolling_window_aggregation()`: Applies rolling window calculations
- `pivot_table_aggregation()`: Creates pivot tables from data
- `custom_aggregation()`: Applies custom aggregation functions
- `aggregate_data()`: Comprehensive aggregation pipeline

#### Example Usage
```python
import pandas as pd
from src.data.preprocessing.aggregation import aggregate_data

# Create sample data
df = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=100),
    'category': ['A', 'B'] * 50,
    'value': range(100),
    'quantity': range(100, 200)
})

# Define aggregation configuration
config = {
    'groupby_aggregations': [
        {
            'groupby_columns': ['category'],
            'aggregation_functions': {'value': 'mean', 'quantity': ['sum', 'count']}
        }
    ]
}

# Apply aggregation
aggregated_df = aggregate_data(df, config)
```

### 8. Data Validation (`validation.py`)

#### Functions
- `validate_data_schema()`: Validates DataFrame schema against expected structure
- `validate_data_ranges()`: Validates numerical value ranges
- `validate_data_completeness()`: Checks for data completeness
- `validate_cross_field_constraints()`: Validates relationships between columns
- `calculate_data_quality_score()`: Calculates overall data quality score
- `validate_data()`: Comprehensive data validation pipeline

#### Example Usage
```python
import pandas as pd
from src.data.preprocessing.validation import validate_data

# Create sample data
df = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'age': [25, 30, 35, 40, 45],
    'salary': [50000, 60000, 70000, 80000, 90000]
})

# Define validation configuration
config = {
    'expected_schema': {
        'id': 'int64',
        'age': 'int64',
        'salary': 'int64'
    },
    'range_validations': {
        'age': {'min': 0, 'max': 120},
        'salary': {'min': 0}
    },
    'completeness_requirements': ['id', 'age', 'salary']
}

# Apply validation
validation_results = validate_data(df, config)
```

## Integration with Existing System

The preprocessing pipeline can be integrated with the existing data ingestion system through the main orchestrator in `src/data/preprocessing.py`. This module provides a unified interface to all preprocessing functions.

## Best Practices

1. **Order of Operations**: Apply cleaning first, then imputation, followed by outlier detection, standardization, normalization, feature engineering, and finally validation.
2. **Data Quality**: Always validate your data after preprocessing to ensure quality.
3. **Parameter Tuning**: Adjust parameters based on your specific dataset characteristics.
4. **Memory Management**: For large datasets, consider processing in chunks to manage memory usage.

## Error Handling

All modules include comprehensive error handling and logging. Functions will log warnings for issues that don't prevent execution and raise exceptions for critical errors.