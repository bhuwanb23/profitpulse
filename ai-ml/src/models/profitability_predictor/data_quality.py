"""
Data Quality Assessment for Client Profitability Prediction
Assesses quality of prepared data for model training
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ProfitabilityDataQualityAssessor:
    """Assesses data quality for client profitability prediction models"""
    
    def __init__(self):
        """Initialize the data quality assessor"""
        pass
        
    def assess_missing_values(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Assess missing values in the dataset
        
        Args:
            data: DataFrame to assess
            
        Returns:
            Dictionary with missing value metrics
        """
        logger.info("Assessing missing values")
        
        try:
            missing_counts = data.isnull().sum()
            missing_percentages = (missing_counts / len(data)) * 100
            
            missing_report = {
                'total_records': len(data),
                'missing_counts': missing_counts.to_dict(),
                'missing_percentages': missing_percentages.to_dict(),
                'columns_with_missing': missing_counts[missing_counts > 0].to_dict()
            }
            
            logger.info(f"Missing value assessment completed - {len(missing_report['columns_with_missing'])} columns with missing values")
            return missing_report
            
        except Exception as e:
            logger.error(f"Error assessing missing values: {e}")
            raise
    
    def assess_duplicates(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Assess duplicate rows in the dataset
        
        Args:
            data: DataFrame to assess
            
        Returns:
            Dictionary with duplicate metrics
        """
        logger.info("Assessing duplicates")
        
        try:
            duplicate_count = data.duplicated().sum()
            
            duplicates_report = {
                'total_records': len(data),
                'duplicate_rows': duplicate_count,
                'duplicate_percentage': (duplicate_count / len(data)) * 100
            }
            
            logger.info(f"Duplicate assessment completed - {duplicate_count} duplicate rows")
            return duplicates_report
            
        except Exception as e:
            logger.error(f"Error assessing duplicates: {e}")
            raise
    
    def assess_data_types(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Assess data types in the dataset
        
        Args:
            data: DataFrame to assess
            
        Returns:
            Dictionary with data type metrics
        """
        logger.info("Assessing data types")
        
        try:
            data_types_report = {
                'total_columns': len(data.columns),
                'data_types': data.dtypes.to_dict(),
                'numerical_columns': data.select_dtypes(include=[np.number]).columns.tolist(),
                'categorical_columns': data.select_dtypes(include=['object']).columns.tolist(),
                'datetime_columns': data.select_dtypes(include=['datetime64']).columns.tolist()
            }
            
            logger.info(f"Data type assessment completed - {len(data_types_report['numerical_columns'])} numerical, {len(data_types_report['categorical_columns'])} categorical columns")
            return data_types_report
            
        except Exception as e:
            logger.error(f"Error assessing data types: {e}")
            raise
    
    def assess_outliers(self, data: pd.DataFrame, numerical_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Assess outliers in numerical columns
        
        Args:
            data: DataFrame to assess
            numerical_columns: List of numerical columns to check (if None, auto-detect)
            
        Returns:
            Dictionary with outlier metrics
        """
        logger.info("Assessing outliers")
        
        try:
            if numerical_columns is None:
                numerical_columns = data.select_dtypes(include=[np.number]).columns.tolist()
            
            outlier_report = {}
            total_outliers = 0
            
            for col in numerical_columns:
                if col in data.columns:
                    # Calculate IQR
                    Q1 = data[col].quantile(0.25)
                    Q3 = data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    
                    # Define outlier bounds
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    # Count outliers
                    outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
                    outlier_count = len(outliers)
                    outlier_percentage = (outlier_count / len(data)) * 100
                    
                    outlier_report[col] = {
                        'outlier_count': outlier_count,
                        'outlier_percentage': outlier_percentage,
                        'lower_bound': lower_bound,
                        'upper_bound': upper_bound,
                        'Q1': Q1,
                        'Q3': Q3,
                        'IQR': IQR
                    }
                    
                    total_outliers += outlier_count
            
            overall_report = {
                'total_outliers': total_outliers,
                'total_records': len(data),
                'outlier_percentage': (total_outliers / (len(data) * len(numerical_columns))) * 100 if numerical_columns else 0,
                'column_outliers': outlier_report
            }
            
            logger.info(f"Outlier assessment completed - {total_outliers} total outliers detected")
            return overall_report
            
        except Exception as e:
            logger.error(f"Error assessing outliers: {e}")
            raise
    
    def assess_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Complete data quality assessment
        
        Args:
            data: DataFrame to assess
            
        Returns:
            Dictionary with comprehensive quality metrics
        """
        logger.info("Starting complete data quality assessment")
        
        try:
            # Perform all quality assessments
            missing_report = self.assess_missing_values(data)
            duplicates_report = self.assess_duplicates(data)
            data_types_report = self.assess_data_types(data)
            outliers_report = self.assess_outliers(data)
            
            # Combine all reports
            quality_report = {
                'timestamp': datetime.now().isoformat(),
                'missing_values': missing_report,
                'duplicates': duplicates_report,
                'data_types': data_types_report,
                'outliers': outliers_report,
                'summary': {
                    'total_records': len(data),
                    'total_columns': len(data.columns),
                    'columns_with_missing': len(missing_report['columns_with_missing']),
                    'duplicate_rows': duplicates_report['duplicate_rows'],
                    'numerical_columns': len(data_types_report['numerical_columns']),
                    'categorical_columns': len(data_types_report['categorical_columns']),
                    'total_outliers': outliers_report['total_outliers']
                }
            }
            
            logger.info("Complete data quality assessment finished")
            return quality_report
            
        except Exception as e:
            logger.error(f"Error in complete data quality assessment: {e}")
            raise


# Convenience function for easy usage
def assess_profitability_data_quality(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Assess data quality for client profitability prediction
    
    Args:
        data: DataFrame to assess
        
    Returns:
        Dictionary with comprehensive quality metrics
    """
    assessor = ProfitabilityDataQualityAssessor()
    return assessor.assess_data_quality(data)