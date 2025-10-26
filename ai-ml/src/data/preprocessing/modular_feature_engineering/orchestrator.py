"""
Feature Engineering Orchestrator
Main orchestrator for the feature engineering pipeline that integrates all feature engines
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Any
import logging

# Import feature engine modules
from .financial_features import *
from .operational_features import *
from .behavioral_features import *

logger = logging.getLogger(__name__)


def extract_all_features(df: pd.DataFrame, 
                        feature_config: Dict[str, Any]) -> pd.DataFrame:
    """
    Extract all features from the three feature engines
    
    Args:
        df: Input DataFrame
        feature_config: Configuration dictionary specifying which features to extract
        
    Returns:
        DataFrame with all extracted features
    """
    logger.info("Starting feature extraction pipeline")
    df_features = df.copy()
    
    # Extract financial features if configured
    if feature_config.get('financial_features', False):
        financial_config = feature_config.get('financial_config', {})
        df_features = extract_financial_features(df_features, financial_config)
    
    # Extract operational features if configured
    if feature_config.get('operational_features', False):
        operational_config = feature_config.get('operational_config', {})
        df_features = extract_operational_features(df_features, operational_config)
    
    # Extract behavioral features if configured
    if feature_config.get('behavioral_features', False):
        behavioral_config = feature_config.get('behavioral_config', {})
        df_features = extract_behavioral_features(df_features, behavioral_config)
    
    logger.info("Feature extraction pipeline completed")
    return df_features


def extract_financial_features(df: pd.DataFrame, 
                             config: Dict[str, Any]) -> pd.DataFrame:
    """
    Extract financial features using the financial features engine
    
    Args:
        df: Input DataFrame
        config: Configuration for financial feature extraction
        
    Returns:
        DataFrame with financial features
    """
    logger.info("Extracting financial features")
    df_financial = df.copy()
    
    # Revenue per client
    if config.get('revenue_per_client', False):
        revenue_config = config.get('revenue_per_client_config', {})
        try:
            revenue_features = calculate_revenue_per_client(df_financial, **revenue_config)
            # Merge back with original data
            df_financial = df_financial.merge(revenue_features, on='client_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to calculate revenue per client: {e}")
    
    # Profit margins by service
    if config.get('profit_margins_by_service', False):
        margin_config = config.get('profit_margins_config', {})
        try:
            margin_features = calculate_profit_margins_by_service(df_financial, **margin_config)
            # Merge back with original data
            df_financial = df_financial.merge(margin_features, on='service_type', how='left')
        except Exception as e:
            logger.warning(f"Failed to calculate profit margins: {e}")
    
    # Billing efficiency
    if config.get('billing_efficiency', False):
        billing_config = config.get('billing_efficiency_config', {})
        try:
            billing_features = calculate_billing_efficiency(df_financial, **billing_config)
            df_financial = pd.concat([df_financial, billing_features], axis=1)
        except Exception as e:
            logger.warning(f"Failed to calculate billing efficiency: {e}")
    
    # Cost per ticket resolution
    if config.get('cost_per_ticket_resolution', False):
        cost_config = config.get('cost_per_ticket_config', {})
        try:
            cost_features = calculate_cost_per_ticket_resolution(df_financial, **cost_config)
            df_financial = df_financial.merge(cost_features, on='ticket_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to calculate cost per ticket resolution: {e}")
    
    # Service utilization rates
    if config.get('service_utilization_rates', False):
        utilization_config = config.get('service_utilization_config', {})
        try:
            utilization_features = calculate_service_utilization_rates(df_financial, **utilization_config)
            df_financial = df_financial.merge(utilization_features, on='service_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to calculate service utilization rates: {e}")
    
    # Payment behavior analysis
    if config.get('payment_behavior', False):
        payment_config = config.get('payment_behavior_config', {})
        try:
            payment_features = analyze_payment_behavior(df_financial, **payment_config)
            df_financial = df_financial.merge(payment_features, on='client_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to analyze payment behavior: {e}")
    
    # Revenue growth trends
    if config.get('revenue_growth_trends', False):
        growth_config = config.get('revenue_growth_config', {})
        try:
            growth_features = calculate_revenue_growth_trends(df_financial, **growth_config)
            # Merge back with original data
            df_financial = df_financial.merge(growth_features, on=['client_id', 'period'], how='left')
        except Exception as e:
            logger.warning(f"Failed to calculate revenue growth trends: {e}")
    
    # Profitability ratios
    if config.get('profitability_ratios', False):
        ratio_config = config.get('profitability_ratios_config', {})
        try:
            ratio_features = calculate_profitability_ratios(df_financial, **ratio_config)
            df_financial = pd.concat([df_financial, ratio_features], axis=1)
        except Exception as e:
            logger.warning(f"Failed to calculate profitability ratios: {e}")
    
    logger.info("Financial feature extraction completed")
    return df_financial


def extract_operational_features(df: pd.DataFrame, 
                               config: Dict[str, Any]) -> pd.DataFrame:
    """
    Extract operational features using the operational features engine
    
    Args:
        df: Input DataFrame
        config: Configuration for operational feature extraction
        
    Returns:
        DataFrame with operational features
    """
    logger.info("Extracting operational features")
    df_operational = df.copy()
    
    # Ticket resolution time
    if config.get('ticket_resolution_time', False):
        resolution_config = config.get('ticket_resolution_config', {})
        try:
            resolution_features = calculate_ticket_resolution_time(df_operational, **resolution_config)
            df_operational = df_operational.merge(resolution_features, on='ticket_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to calculate ticket resolution time: {e}")
    
    # SLA compliance
    if config.get('sla_compliance', False):
        sla_config = config.get('sla_compliance_config', {})
        try:
            sla_features = calculate_sla_compliance(df_operational, **sla_config)
            df_operational = df_operational.merge(sla_features, on='ticket_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to calculate SLA compliance: {e}")
    
    # Technician productivity
    if config.get('technician_productivity', False):
        productivity_config = config.get('technician_productivity_config', {})
        try:
            productivity_features = calculate_technician_productivity(df_operational, **productivity_config)
            df_operational = df_operational.merge(productivity_features, on='technician_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to calculate technician productivity: {e}")
    
    # Service delivery quality
    if config.get('service_delivery_quality', False):
        quality_config = config.get('service_delivery_quality_config', {})
        try:
            quality_features = assess_service_delivery_quality(df_operational, **quality_config)
            df_operational = df_operational.merge(quality_features, on='service_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to assess service delivery quality: {e}")
    
    # Client satisfaction
    if config.get('client_satisfaction', False):
        satisfaction_config = config.get('client_satisfaction_config', {})
        try:
            satisfaction_features = calculate_client_satisfaction(df_operational, **satisfaction_config)
            df_operational = df_operational.merge(satisfaction_features, on='client_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to calculate client satisfaction: {e}")
    
    # Ticket frequency analysis
    if config.get('ticket_frequency', False):
        frequency_config = config.get('ticket_frequency_config', {})
        try:
            frequency_features = analyze_ticket_frequency(df_operational, **frequency_config)
            df_operational = df_operational.merge(frequency_features, on='client_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to analyze ticket frequency: {e}")
    
    # Service level trends
    if config.get('service_level_trends', False):
        trends_config = config.get('service_level_trends_config', {})
        try:
            trends_analysis = track_service_level_trends(df_operational, **trends_config)
            df_operational = df_operational.merge(trends_analysis, on=['service_id', 'year', 'month'], how='left')
        except Exception as e:
            logger.warning(f"Failed to track service level trends: {e}")
    
    # Resource utilization
    if config.get('resource_utilization', False):
        utilization_config = config.get('resource_utilization_config', {})
        try:
            utilization_features = calculate_resource_utilization(df_operational, **utilization_config)
            df_operational = df_operational.merge(utilization_features, on='resource_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to calculate resource utilization: {e}")
    
    logger.info("Operational feature extraction completed")
    return df_operational


def extract_behavioral_features(df: pd.DataFrame, 
                              config: Dict[str, Any]) -> pd.DataFrame:
    """
    Extract behavioral features using the behavioral features engine
    
    Args:
        df: Input DataFrame
        config: Configuration for behavioral feature extraction
        
    Returns:
        DataFrame with behavioral features
    """
    logger.info("Extracting behavioral features")
    df_behavioral = df.copy()
    
    # Client engagement
    if config.get('client_engagement', False):
        engagement_config = config.get('client_engagement_config', {})
        try:
            engagement_features = measure_client_engagement(df_behavioral, **engagement_config)
            df_behavioral = df_behavioral.merge(engagement_features, on='client_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to measure client engagement: {e}")
    
    # Communication patterns
    if config.get('communication_patterns', False):
        communication_config = config.get('communication_patterns_config', {})
        try:
            communication_features = analyze_communication_patterns(df_behavioral, **communication_config)
            df_behavioral = df_behavioral.merge(communication_features, on='client_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to analyze communication patterns: {e}")
    
    # Service changes
    if config.get('service_changes', False):
        changes_config = config.get('service_changes_config', {})
        try:
            changes_features = track_service_changes(df_behavioral, **changes_config)
            df_behavioral = df_behavioral.merge(changes_features, on='client_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to track service changes: {e}")
    
    # Contract renewal prediction
    if config.get('contract_renewal', False):
        renewal_config = config.get('contract_renewal_config', {})
        try:
            renewal_features = predict_contract_renewal(df_behavioral, **renewal_config)
            df_behavioral = df_behavioral.merge(renewal_features, on='client_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to predict contract renewal: {e}")
    
    # Support request analysis
    if config.get('support_requests', False):
        requests_config = config.get('support_requests_config', {})
        try:
            requests_features = analyze_support_requests(df_behavioral, **requests_config)
            df_behavioral = df_behavioral.merge(requests_features, on='client_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to analyze support requests: {e}")
    
    # Feedback sentiment analysis
    if config.get('feedback_sentiment', False):
        sentiment_config = config.get('feedback_sentiment_config', {})
        try:
            sentiment_features = analyze_feedback_sentiment(df_behavioral, **sentiment_config)
            df_behavioral = df_behavioral.merge(sentiment_features, on='client_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to analyze feedback sentiment: {e}")
    
    # Usage patterns
    if config.get('usage_patterns', False):
        usage_config = config.get('usage_patterns_config', {})
        try:
            usage_features = identify_usage_patterns(df_behavioral, **usage_config)
            df_behavioral = df_behavioral.merge(usage_features, on='client_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to identify usage patterns: {e}")
    
    # Churn risk calculation
    if config.get('churn_risk', False):
        churn_config = config.get('churn_risk_config', {})
        try:
            churn_features = calculate_churn_risk(df_behavioral, **churn_config)
            df_behavioral = df_behavioral.merge(churn_features, on='client_id', how='left')
        except Exception as e:
            logger.warning(f"Failed to calculate churn risk: {e}")
    
    logger.info("Behavioral feature extraction completed")
    return df_behavioral