"""
Data Preprocessing Pipeline
Handles data cleaning, validation, and transformation
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer, KNNImputer
import warnings

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class DataPreprocessingError(Exception):
    """Custom exception for data preprocessing errors"""
    pass


class DataValidator:
    """Validates data quality and completeness"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.DataValidator")
    
    def validate_dataframe(self, df: pd.DataFrame, required_columns: List[str] = None) -> Dict[str, Any]:
        """Validate DataFrame quality and completeness"""
        validation_results = {
            "is_valid": True,
            "issues": [],
            "warnings": [],
            "stats": {}
        }
        
        try:
            # Basic validation
            if df.empty:
                validation_results["is_valid"] = False
                validation_results["issues"].append("DataFrame is empty")
                return validation_results
            
            # Check required columns
            if required_columns:
                missing_columns = set(required_columns) - set(df.columns)
                if missing_columns:
                    validation_results["is_valid"] = False
                    validation_results["issues"].append(f"Missing required columns: {missing_columns}")
            
            # Calculate statistics
            validation_results["stats"] = {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "missing_values": df.isnull().sum().sum(),
                "duplicate_rows": df.duplicated().sum(),
                "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024
            }
            
            # Check for high missing value percentage
            missing_percentage = (df.isnull().sum() / len(df)) * 100
            high_missing_cols = missing_percentage[missing_percentage > 50].index.tolist()
            if high_missing_cols:
                validation_results["warnings"].append(f"Columns with >50% missing values: {high_missing_cols}")
            
            # Check for duplicate rows
            if validation_results["stats"]["duplicate_rows"] > 0:
                validation_results["warnings"].append(f"Found {validation_results['stats']['duplicate_rows']} duplicate rows")
            
            self.logger.info(f"Data validation completed. Valid: {validation_results['is_valid']}")
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Error validating DataFrame: {e}")
            validation_results["is_valid"] = False
            validation_results["issues"].append(f"Validation error: {e}")
            return validation_results
    
    def validate_ticket_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate ticket-specific data"""
        validation_results = self.validate_dataframe(df)
        
        if not validation_results["is_valid"]:
            return validation_results
        
        try:
            # Ticket-specific validations
            ticket_issues = []
            
            # Check for valid status values
            valid_statuses = ["Open", "In Progress", "Closed", "Cancelled", "Pending"]
            invalid_status = df[~df['status'].isin(valid_statuses)]['status'].unique()
            if len(invalid_status) > 0:
                ticket_issues.append(f"Invalid status values: {invalid_status}")
            
            # Check for valid priority values
            valid_priorities = ["Low", "Medium", "High", "Critical"]
            invalid_priority = df[~df['priority'].isin(valid_priorities)]['priority'].unique()
            if len(invalid_priority) > 0:
                ticket_issues.append(f"Invalid priority values: {invalid_priority}")
            
            # Check for negative hours or billing amounts
            if 'hours_logged' in df.columns:
                negative_hours = df[df['hours_logged'] < 0]['hours_logged'].count()
                if negative_hours > 0:
                    ticket_issues.append(f"Found {negative_hours} records with negative hours")
            
            if 'billing_amount' in df.columns:
                negative_billing = df[df['billing_amount'] < 0]['billing_amount'].count()
                if negative_billing > 0:
                    ticket_issues.append(f"Found {negative_billing} records with negative billing amounts")
            
            validation_results["issues"].extend(ticket_issues)
            validation_results["is_valid"] = len(ticket_issues) == 0
            
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Error validating ticket data: {e}")
            validation_results["is_valid"] = False
            validation_results["issues"].append(f"Ticket validation error: {e}")
            return validation_results
    
    def validate_client_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate client-specific data"""
        validation_results = self.validate_dataframe(df)
        
        if not validation_results["is_valid"]:
            return validation_results
        
        try:
            # Client-specific validations
            client_issues = []
            
            # Check for valid email formats
            if 'email' in df.columns:
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                invalid_emails = df[~df['email'].str.match(email_pattern, na=False)]['email'].count()
                if invalid_emails > 0:
                    client_issues.append(f"Found {invalid_emails} records with invalid email formats")
            
            # Check for valid status values
            if 'status' in df.columns:
                valid_statuses = ["Active", "Inactive", "Suspended", "Prospect"]
                invalid_status = df[~df['status'].isin(valid_statuses)]['status'].unique()
                if len(invalid_status) > 0:
                    client_issues.append(f"Invalid status values: {invalid_status}")
            
            # Check for negative contract values
            if 'contract_value' in df.columns:
                negative_contracts = df[df['contract_value'] < 0]['contract_value'].count()
                if negative_contracts > 0:
                    client_issues.append(f"Found {negative_contracts} records with negative contract values")
            
            validation_results["issues"].extend(client_issues)
            validation_results["is_valid"] = len(client_issues) == 0
            
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Error validating client data: {e}")
            validation_results["is_valid"] = False
            validation_results["issues"].append(f"Client validation error: {e}")
            return validation_results


class DataCleaner:
    """Cleans and standardizes data"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.DataCleaner")
    
    def clean_dataframe(self, df: pd.DataFrame, 
                       remove_duplicates: bool = True,
                       handle_missing: str = "drop") -> pd.DataFrame:
        """Clean DataFrame by removing duplicates and handling missing values"""
        try:
            cleaned_df = df.copy()
            
            # Remove duplicates
            if remove_duplicates:
                initial_rows = len(cleaned_df)
                cleaned_df = cleaned_df.drop_duplicates()
                removed_duplicates = initial_rows - len(cleaned_df)
                if removed_duplicates > 0:
                    self.logger.info(f"Removed {removed_duplicates} duplicate rows")
            
            # Handle missing values
            if handle_missing == "drop":
                initial_rows = len(cleaned_df)
                cleaned_df = cleaned_df.dropna()
                removed_rows = initial_rows - len(cleaned_df)
                if removed_rows > 0:
                    self.logger.info(f"Removed {removed_rows} rows with missing values")
            elif handle_missing == "fill":
                cleaned_df = self._fill_missing_values(cleaned_df)
            
            self.logger.info(f"Data cleaning completed. Final rows: {len(cleaned_df)}")
            return cleaned_df
            
        except Exception as e:
            self.logger.error(f"Error cleaning DataFrame: {e}")
            raise DataPreprocessingError(f"Data cleaning failed: {e}")
    
    def _fill_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fill missing values using appropriate strategies"""
        try:
            filled_df = df.copy()
            
            for column in filled_df.columns:
                if filled_df[column].dtype in ['int64', 'float64']:
                    # Fill numeric columns with median
                    filled_df[column].fillna(filled_df[column].median(), inplace=True)
                elif filled_df[column].dtype == 'object':
                    # Fill categorical columns with mode
                    mode_value = filled_df[column].mode()
                    if not mode_value.empty:
                        filled_df[column].fillna(mode_value[0], inplace=True)
                    else:
                        filled_df[column].fillna('Unknown', inplace=True)
                elif filled_df[column].dtype == 'datetime64[ns]':
                    # Fill datetime columns with forward fill
                    filled_df[column].fillna(method='ffill', inplace=True)
            
            return filled_df
            
        except Exception as e:
            self.logger.error(f"Error filling missing values: {e}")
            return df
    
    def standardize_text(self, df: pd.DataFrame, text_columns: List[str]) -> pd.DataFrame:
        """Standardize text data (trim whitespace, lowercase, etc.)"""
        try:
            standardized_df = df.copy()
            
            for column in text_columns:
                if column in standardized_df.columns:
                    # Trim whitespace and convert to lowercase
                    standardized_df[column] = standardized_df[column].astype(str).str.strip().str.lower()
            
            self.logger.info(f"Standardized text in columns: {text_columns}")
            return standardized_df
            
        except Exception as e:
            self.logger.error(f"Error standardizing text: {e}")
            return df
    
    def clean_ticket_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean ticket-specific data"""
        try:
            cleaned_df = df.copy()
            
            # Standardize status and priority values
            if 'status' in cleaned_df.columns:
                status_mapping = {
                    'open': 'Open',
                    'in progress': 'In Progress',
                    'closed': 'Closed',
                    'cancelled': 'Cancelled',
                    'pending': 'Pending'
                }
                cleaned_df['status'] = cleaned_df['status'].str.lower().map(status_mapping).fillna(cleaned_df['status'])
            
            if 'priority' in cleaned_df.columns:
                priority_mapping = {
                    'low': 'Low',
                    'medium': 'Medium',
                    'high': 'High',
                    'critical': 'Critical'
                }
                cleaned_df['priority'] = cleaned_df['priority'].str.lower().map(priority_mapping).fillna(cleaned_df['priority'])
            
            # Clean numeric columns
            numeric_columns = ['hours_logged', 'billing_amount']
            for col in numeric_columns:
                if col in cleaned_df.columns:
                    # Remove negative values
                    cleaned_df[col] = cleaned_df[col].clip(lower=0)
                    # Remove outliers (values > 3 standard deviations)
                    mean_val = cleaned_df[col].mean()
                    std_val = cleaned_df[col].std()
                    upper_limit = mean_val + 3 * std_val
                    cleaned_df[col] = cleaned_df[col].clip(upper=upper_limit)
            
            self.logger.info("Ticket data cleaning completed")
            return cleaned_df
            
        except Exception as e:
            self.logger.error(f"Error cleaning ticket data: {e}")
            return df
    
    def clean_client_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean client-specific data"""
        try:
            cleaned_df = df.copy()
            
            # Clean email addresses
            if 'email' in cleaned_df.columns:
                cleaned_df['email'] = cleaned_df['email'].str.strip().str.lower()
            
            # Clean phone numbers (remove non-numeric characters)
            if 'phone' in cleaned_df.columns:
                cleaned_df['phone'] = cleaned_df['phone'].str.replace(r'[^\d+]', '', regex=True)
            
            # Standardize status values
            if 'status' in cleaned_df.columns:
                status_mapping = {
                    'active': 'Active',
                    'inactive': 'Inactive',
                    'suspended': 'Suspended',
                    'prospect': 'Prospect'
                }
                cleaned_df['status'] = cleaned_df['status'].str.lower().map(status_mapping).fillna(cleaned_df['status'])
            
            # Clean contract values
            if 'contract_value' in cleaned_df.columns:
                cleaned_df['contract_value'] = cleaned_df['contract_value'].clip(lower=0)
            
            self.logger.info("Client data cleaning completed")
            return cleaned_df
            
        except Exception as e:
            self.logger.error(f"Error cleaning client data: {e}")
            return df


class DataTransformer:
    """Transforms data for machine learning"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.DataTransformer")
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
    
    def encode_categorical(self, df: pd.DataFrame, categorical_columns: List[str]) -> pd.DataFrame:
        """Encode categorical variables"""
        try:
            encoded_df = df.copy()
            
            for column in categorical_columns:
                if column in encoded_df.columns:
                    # Use LabelEncoder for ordinal data
                    if column in ['priority', 'status']:
                        le = LabelEncoder()
                        encoded_df[column] = le.fit_transform(encoded_df[column].astype(str))
                        self.encoders[column] = le
                    else:
                        # Use one-hot encoding for nominal data
                        dummies = pd.get_dummies(encoded_df[column], prefix=column)
                        encoded_df = pd.concat([encoded_df, dummies], axis=1)
                        encoded_df = encoded_df.drop(column, axis=1)
            
            self.logger.info(f"Encoded categorical columns: {categorical_columns}")
            return encoded_df
            
        except Exception as e:
            self.logger.error(f"Error encoding categorical variables: {e}")
            return df
    
    def scale_numerical(self, df: pd.DataFrame, numerical_columns: List[str], 
                       method: str = "standard") -> pd.DataFrame:
        """Scale numerical variables"""
        try:
            scaled_df = df.copy()
            
            for column in numerical_columns:
                if column in scaled_df.columns:
                    if method == "standard":
                        scaler = StandardScaler()
                    elif method == "minmax":
                        scaler = MinMaxScaler()
                    else:
                        raise ValueError(f"Unknown scaling method: {method}")
                    
                    scaled_df[column] = scaler.fit_transform(scaled_df[[column]])
                    self.scalers[column] = scaler
            
            self.logger.info(f"Scaled numerical columns: {numerical_columns}")
            return scaled_df
            
        except Exception as e:
            self.logger.error(f"Error scaling numerical variables: {e}")
            return df
    
    def create_time_features(self, df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
        """Create time-based features from date columns"""
        try:
            feature_df = df.copy()
            
            for column in date_columns:
                if column in feature_df.columns:
                    # Convert to datetime
                    feature_df[column] = pd.to_datetime(feature_df[column], errors='coerce')
                    
                    # Create time features
                    feature_df[f'{column}_year'] = feature_df[column].dt.year
                    feature_df[f'{column}_month'] = feature_df[column].dt.month
                    feature_df[f'{column}_day'] = feature_df[column].dt.day
                    feature_df[f'{column}_weekday'] = feature_df[column].dt.weekday
                    feature_df[f'{column}_quarter'] = feature_df[column].dt.quarter
                    feature_df[f'{column}_is_weekend'] = feature_df[column].dt.weekday >= 5
                    
                    # Calculate days since/until
                    now = datetime.now()
                    feature_df[f'{column}_days_ago'] = (now - feature_df[column]).dt.days
                    feature_df[f'{column}_days_ago'] = feature_df[f'{column}_days_ago'].clip(lower=0)
            
            self.logger.info(f"Created time features for columns: {date_columns}")
            return feature_df
            
        except Exception as e:
            self.logger.error(f"Error creating time features: {e}")
            return df
    
    def create_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create derived features for analysis"""
        try:
            derived_df = df.copy()
            
            # Revenue per hour
            if 'billing_amount' in derived_df.columns and 'hours_logged' in derived_df.columns:
                derived_df['revenue_per_hour'] = derived_df['billing_amount'] / (derived_df['hours_logged'] + 1e-6)
            
            # Ticket age (if created_at exists)
            if 'created_at' in derived_df.columns:
                created_dates = pd.to_datetime(derived_df['created_at'], errors='coerce')
                derived_df['ticket_age_days'] = (datetime.now() - created_dates).dt.days
            
            # Resolution time (if both created_at and resolved_at exist)
            if 'created_at' in derived_df.columns and 'resolved_at' in derived_df.columns:
                created_dates = pd.to_datetime(derived_df['created_at'], errors='coerce')
                resolved_dates = pd.to_datetime(derived_df['resolved_at'], errors='coerce')
                derived_df['resolution_time_hours'] = (resolved_dates - created_dates).dt.total_seconds() / 3600
                derived_df['resolution_time_hours'] = derived_df['resolution_time_hours'].clip(lower=0)
            
            # Client value tier (if contract_value exists)
            if 'contract_value' in derived_df.columns:
                derived_df['client_value_tier'] = pd.cut(
                    derived_df['contract_value'],
                    bins=[0, 5000, 15000, 50000, float('inf')],
                    labels=['Bronze', 'Silver', 'Gold', 'Platinum']
                )
            
            self.logger.info("Created derived features")
            return derived_df
            
        except Exception as e:
            self.logger.error(f"Error creating derived features: {e}")
            return df


class DataPreprocessingPipeline:
    """Main data preprocessing pipeline"""
    
    def __init__(self):
        self.validator = DataValidator()
        self.cleaner = DataCleaner()
        self.transformer = DataTransformer()
        self.logger = logging.getLogger(__name__)
    
    def process_ticket_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process ticket data through the complete pipeline"""
        try:
            self.logger.info("Starting ticket data processing pipeline")
            
            # Validate data
            validation_results = self.validator.validate_ticket_data(df)
            if not validation_results["is_valid"]:
                self.logger.warning(f"Data validation issues: {validation_results['issues']}")
            
            # Clean data
            cleaned_df = self.cleaner.clean_ticket_data(df)
            cleaned_df = self.cleaner.clean_dataframe(cleaned_df)
            
            # Transform data
            # Encode categorical variables
            categorical_columns = ['status', 'priority']
            transformed_df = self.transformer.encode_categorical(cleaned_df, categorical_columns)
            
            # Create time features
            date_columns = ['created_at', 'resolved_at']
            transformed_df = self.transformer.create_time_features(transformed_df, date_columns)
            
            # Create derived features
            transformed_df = self.transformer.create_derived_features(transformed_df)
            
            # Scale numerical variables
            numerical_columns = ['hours_logged', 'billing_amount', 'revenue_per_hour', 'ticket_age_days']
            numerical_columns = [col for col in numerical_columns if col in transformed_df.columns]
            if numerical_columns:
                transformed_df = self.transformer.scale_numerical(transformed_df, numerical_columns)
            
            self.logger.info("Ticket data processing pipeline completed successfully")
            return transformed_df, validation_results
            
        except Exception as e:
            self.logger.error(f"Error processing ticket data: {e}")
            raise DataPreprocessingError(f"Ticket data processing failed: {e}")
    
    def process_client_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process client data through the complete pipeline"""
        try:
            self.logger.info("Starting client data processing pipeline")
            
            # Validate data
            validation_results = self.validator.validate_client_data(df)
            if not validation_results["is_valid"]:
                self.logger.warning(f"Data validation issues: {validation_results['issues']}")
            
            # Clean data
            cleaned_df = self.cleaner.clean_client_data(df)
            cleaned_df = self.cleaner.clean_dataframe(cleaned_df)
            
            # Transform data
            # Encode categorical variables
            categorical_columns = ['status']
            transformed_df = self.transformer.encode_categorical(cleaned_df, categorical_columns)
            
            # Create time features
            date_columns = ['created_at', 'last_contact']
            transformed_df = self.transformer.create_time_features(transformed_df, date_columns)
            
            # Create derived features
            transformed_df = self.transformer.create_derived_features(transformed_df)
            
            # Scale numerical variables
            numerical_columns = ['contract_value']
            numerical_columns = [col for col in numerical_columns if col in transformed_df.columns]
            if numerical_columns:
                transformed_df = self.transformer.scale_numerical(transformed_df, numerical_columns)
            
            self.logger.info("Client data processing pipeline completed successfully")
            return transformed_df, validation_results
            
        except Exception as e:
            self.logger.error(f"Error processing client data: {e}")
            raise DataPreprocessingError(f"Client data processing failed: {e}")
    
    def process_invoice_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process invoice data through the complete pipeline"""
        try:
            self.logger.info("Starting invoice data processing pipeline")
            
            # Validate data
            validation_results = self.validator.validate_dataframe(df)
            if not validation_results["is_valid"]:
                self.logger.warning(f"Data validation issues: {validation_results['issues']}")
            
            # Clean data
            cleaned_df = self.cleaner.clean_dataframe(df)
            
            # Transform data
            # Encode categorical variables
            categorical_columns = ['status', 'payment_method']
            transformed_df = self.transformer.encode_categorical(cleaned_df, categorical_columns)
            
            # Create time features
            date_columns = ['created_date', 'due_date', 'paid_date']
            transformed_df = self.transformer.create_time_features(transformed_df, date_columns)
            
            # Create derived features
            transformed_df = self.transformer.create_derived_features(transformed_df)
            
            # Scale numerical variables
            numerical_columns = ['amount', 'tax_amount', 'total_amount']
            numerical_columns = [col for col in numerical_columns if col in transformed_df.columns]
            if numerical_columns:
                transformed_df = self.transformer.scale_numerical(transformed_df, numerical_columns)
            
            self.logger.info("Invoice data processing pipeline completed successfully")
            return transformed_df, validation_results
            
        except Exception as e:
            self.logger.error(f"Error processing invoice data: {e}")
            raise DataPreprocessingError(f"Invoice data processing failed: {e}")


# Convenience function for easy usage
def preprocess_data(df: pd.DataFrame, data_type: str = "ticket") -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Preprocess data using the appropriate pipeline
    
    Args:
        df: DataFrame to preprocess
        data_type: Type of data ('ticket', 'client', 'invoice')
    
    Returns:
        Tuple of (processed_dataframe, validation_results)
    """
    pipeline = DataPreprocessingPipeline()
    
    if data_type == "ticket":
        return pipeline.process_ticket_data(df)
    elif data_type == "client":
        return pipeline.process_client_data(df)
    elif data_type == "invoice":
        return pipeline.process_invoice_data(df)
    else:
        raise ValueError(f"Unknown data type: {data_type}")
