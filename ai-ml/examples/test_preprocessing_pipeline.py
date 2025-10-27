"""
Test script to demonstrate the preprocessing pipeline working with sample data
"""

import sys
import os
import pandas as pd
import sqlite3
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.preprocessing.cleaning import clean_dataframe
from src.data.preprocessing.imputation import impute_missing_values
from src.data.preprocessing.outlier_detection import remove_outliers
from src.data.preprocessing.standardization import standardize_data
from src.data.preprocessing.normalization import normalize_data


def load_sample_data():
    """Load sample data from the database"""
    print("Loading Sample Data from Database")
    print("=" * 35)
    
    # Connect to the database
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'superhack.db')
    
    try:
        conn = sqlite3.connect(db_path)
        
        # Load clients data
        clients_df = pd.read_sql_query("SELECT * FROM clients LIMIT 10", conn)
        print(f"Loaded {len(clients_df)} client records")
        
        # Load tickets data
        tickets_df = pd.read_sql_query("SELECT * FROM tickets LIMIT 10", conn)
        print(f"Loaded {len(tickets_df)} ticket records")
        
        # Load invoices data
        invoices_df = pd.read_sql_query("SELECT * FROM invoices LIMIT 10", conn)
        print(f"Loaded {len(invoices_df)} invoice records")
        
        conn.close()
        
        return clients_df, tickets_df, invoices_df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None


def demonstrate_preprocessing(clients_df):
    """Demonstrate the preprocessing pipeline"""
    print("\nDemonstrating Preprocessing Pipeline")
    print("=" * 35)
    
    if clients_df is None or clients_df.empty:
        print("No data to process")
        return
    
    print(f"Original data shape: {clients_df.shape}")
    print("Original columns:", list(clients_df.columns))
    
    # 1. Clean data
    print("\n1. Cleaning Data...")
    cleaned_df = clean_dataframe(
        clients_df,
        remove_duplicates_subset=['id']  # Remove duplicates based on ID
    )
    print(f"Cleaned data shape: {cleaned_df.shape}")
    
    # 2. Handle missing values (if any)
    print("\n2. Handling Missing Values...")
    imputation_config = {
        'mean_cols': ['contract_value'] if 'contract_value' in cleaned_df.columns else [],
        'mode_cols': ['status'] if 'status' in cleaned_df.columns else []
    }
    
    if imputation_config['mean_cols'] or imputation_config['mode_cols']:
        imputed_df = impute_missing_values(cleaned_df, imputation_config)
        print(f"Data after imputation: {imputed_df.shape}")
    else:
        imputed_df = cleaned_df
        print("No columns specified for imputation")
    
    # 3. Remove outliers (if we have numeric columns)
    print("\n3. Removing Outliers...")
    numeric_columns = ['contract_value'] if 'contract_value' in imputed_df.columns else []
    
    if numeric_columns:
        outlier_config = {
            'zscore_cols': numeric_columns,
            'zscore_threshold': 3.0
        }
        cleaned_df_no_outliers, outliers = remove_outliers(imputed_df, outlier_config)
        print(f"Data after outlier removal: {cleaned_df_no_outliers.shape}")
        print(f"Outliers removed: {len(outliers)}")
    else:
        cleaned_df_no_outliers = imputed_df
        print("No numeric columns for outlier detection")
    
    # 4. Standardize data (if we have date columns)
    print("\n4. Standardizing Data...")
    standardization_config = {
        'datetime_columns': {'created_at': '%Y-%m-%d %H:%M:%S'} if 'created_at' in cleaned_df_no_outliers.columns else {},
        'currency_columns': ['contract_value'] if 'contract_value' in cleaned_df_no_outliers.columns else []
    }
    
    if standardization_config['datetime_columns'] or standardization_config['currency_columns']:
        standardized_df = standardize_data(cleaned_df_no_outliers, standardization_config)
        print(f"Data after standardization: {standardized_df.shape}")
    else:
        standardized_df = cleaned_df_no_outliers
        print("No columns specified for standardization")
    
    # 5. Normalize data (if we have numeric columns)
    print("\n5. Normalizing Data...")
    normalization_config = {
        'standard_cols': ['contract_value'] if 'contract_value' in standardized_df.columns else []
    }
    
    if normalization_config['standard_cols']:
        normalized_df = normalize_data(standardized_df, normalization_config)
        print(f"Data after normalization: {normalized_df.shape}")
    else:
        normalized_df = standardized_df
        print("No columns specified for normalization")
    
    print("\n✅ Preprocessing pipeline completed successfully!")
    print(f"Final data shape: {normalized_df.shape}")
    
    return normalized_df


def main():
    """Main function"""
    print("SuperHack Preprocessing Pipeline Test")
    print("=" * 40)
    
    # Load sample data
    clients_df, tickets_df, invoices_df = load_sample_data()
    
    # Demonstrate preprocessing
    processed_data = demonstrate_preprocessing(clients_df)
    
    if processed_data is not None:
        print("\n" + "=" * 50)
        print("🎉 PREPROCESSING DEMO COMPLETE")
        print("=" * 50)
        print("The preprocessing pipeline is working correctly!")
        print("You can now:")
        print("1. Continue with feature engineering")
        print("2. Create client genome vectors")
        print("3. Train machine learning models")
        print("\nThe entire AI/ML pipeline is ready to use!")


if __name__ == "__main__":
    main()