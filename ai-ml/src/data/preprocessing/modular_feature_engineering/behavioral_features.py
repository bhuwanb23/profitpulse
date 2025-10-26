"""
Behavioral Features Engine
Module for extracting behavioral features from MSP client data for AI/ML models
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


def measure_client_engagement(df: pd.DataFrame,
                            client_id_col: str = 'client_id',
                            login_count_col: str = 'login_count',
                            support_request_count_col: str = 'support_request_count',
                            feature_usage_col: str = 'feature_usage_count') -> pd.DataFrame:
    """
    Measure client engagement levels
    
    Args:
        df: Input DataFrame with client engagement data
        client_id_col: Column name for client identifier
        login_count_col: Column name for login count
        support_request_count_col: Column name for support request count
        feature_usage_col: Column name for feature usage count
    
    Returns:
        DataFrame with client engagement metrics
    """
    df_engagement = df.copy()
    
    # Calculate engagement components
    df_engagement['login_frequency'] = df_engagement[login_count_col]
    df_engagement['support_request_frequency'] = df_engagement[support_request_count_col]
    df_engagement['feature_usage_frequency'] = df_engagement[feature_usage_col]
    
    # Normalize components (0-1 scale)
    df_engagement['normalized_logins'] = (
        df_engagement[login_count_col] / df_engagement[login_count_col].max()
    ).fillna(0)
    
    df_engagement['normalized_support_requests'] = (
        df_engagement[support_request_count_col] / df_engagement[support_request_count_col].max()
    ).fillna(0)
    
    df_engagement['normalized_feature_usage'] = (
        df_engagement[feature_usage_col] / df_engagement[feature_usage_col].max()
    ).fillna(0)
    
    # Calculate overall engagement score
    df_engagement['engagement_score'] = (
        0.4 * df_engagement['normalized_logins'] +
        0.3 * df_engagement['normalized_support_requests'] +
        0.3 * df_engagement['normalized_feature_usage']
    )
    
    # Group by client
    engagement_metrics = df_engagement.groupby(client_id_col).agg({
        login_count_col: 'sum',
        support_request_count_col: 'sum',
        feature_usage_col: 'sum',
        'engagement_score': 'mean'
    }).reset_index()
    
    # Categorize engagement levels
    engagement_metrics['engagement_level'] = pd.cut(
        engagement_metrics['engagement_score'],
        bins=[0, 0.33, 0.66, 1.0],
        labels=['Low', 'Medium', 'High']
    )
    
    logger.info(f"Measured client engagement for {len(engagement_metrics)} clients")
    return engagement_metrics


def analyze_communication_patterns(df: pd.DataFrame,
                                 client_id_col: str = 'client_id',
                                 communication_date_col: str = 'communication_date',
                                 communication_type_col: str = 'communication_type',
                                 response_time_col: str = 'response_time_hours') -> pd.DataFrame:
    """
    Analyze communication patterns
    
    Args:
        df: Input DataFrame with communication data
        client_id_col: Column name for client identifier
        communication_date_col: Column name for communication date
        communication_type_col: Column name for communication type
        response_time_col: Column name for response time in hours
    
    Returns:
        DataFrame with communication pattern metrics
    """
    df_communication = df.copy()
    
    # Convert date column to datetime
    df_communication[communication_date_col] = pd.to_datetime(df_communication[communication_date_col])
    
    # Extract time components
    df_communication['day_of_week'] = df_communication[communication_date_col].dt.dayofweek
    df_communication['hour_of_day'] = df_communication[communication_date_col].dt.hour
    df_communication['month'] = df_communication[communication_date_col].dt.month
    
    # Group by client to calculate communication metrics
    communication_metrics = df_communication.groupby(client_id_col).agg({
        communication_date_col: 'count',  # Total communications
        response_time_col: ['mean', 'std'],
        communication_type_col: lambda x: x.value_counts().to_dict(),  # Communication type distribution
        'day_of_week': lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,  # Most common day
        'hour_of_day': lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan   # Most common hour
    }).reset_index()
    
    # Flatten column names
    communication_metrics.columns = [
        client_id_col,
        'total_communications', 'avg_response_time', 'std_response_time',
        'communication_type_distribution', 'preferred_day', 'preferred_hour'
    ]
    
    # Calculate communication frequency scores
    communication_metrics['communication_frequency'] = communication_metrics['total_communications']
    communication_metrics['response_time_score'] = 1 / (1 + communication_metrics['avg_response_time'].fillna(0))
    
    logger.info(f"Analyzed communication patterns for {len(communication_metrics)} clients")
    return communication_metrics


def track_service_changes(df: pd.DataFrame,
                         client_id_col: str = 'client_id',
                         service_type_col: str = 'service_type',
                         change_type_col: str = 'change_type',
                         change_date_col: str = 'change_date') -> pd.DataFrame:
    """
    Track service upgrade/downgrade history
    
    Args:
        df: Input DataFrame with service change data
        client_id_col: Column name for client identifier
        service_type_col: Column name for service type
        change_type_col: Column name for change type (upgrade/downgrade)
        change_date_col: Column name for change date
    
    Returns:
        DataFrame with service change metrics
    """
    df_changes = df.copy()
    
    # Convert date column to datetime
    df_changes[change_date_col] = pd.to_datetime(df_changes[change_date_col])
    
    # Identify upgrade/downgrade patterns
    df_changes['is_upgrade'] = df_changes[change_type_col] == 'upgrade'
    df_changes['is_downgrade'] = df_changes[change_type_col] == 'downgrade'
    
    # Group by client to calculate change metrics
    change_metrics = df_changes.groupby(client_id_col).agg({
        change_date_col: 'count',  # Total changes
        'is_upgrade': 'sum',       # Upgrade count
        'is_downgrade': 'sum',     # Downgrade count
        service_type_col: lambda x: list(x.unique())  # Services changed
    }).reset_index()
    
    # Rename columns
    change_metrics = change_metrics.rename(columns={
        change_date_col: 'total_service_changes',
        'is_upgrade': 'upgrade_count',
        'is_downgrade': 'downgrade_count'
    })
    
    # Calculate change ratios
    change_metrics['upgrade_ratio'] = (
        change_metrics['upgrade_count'] / change_metrics['total_service_changes']
    ).fillna(0)
    
    change_metrics['downgrade_ratio'] = (
        change_metrics['downgrade_count'] / change_metrics['total_service_changes']
    ).fillna(0)
    
    # Calculate net change score
    change_metrics['net_change_score'] = (
        change_metrics['upgrade_ratio'] - change_metrics['downgrade_ratio']
    )
    
    # Categorize change behavior
    change_metrics['change_behavior'] = np.select(
        [
            change_metrics['net_change_score'] > 0.1,
            change_metrics['net_change_score'] < -0.1,
            (change_metrics['net_change_score'] >= -0.1) & (change_metrics['net_change_score'] <= 0.1)
        ],
        ['Expanding', 'Contracting', 'Stable'],
        default='Unknown'
    )
    
    logger.info(f"Tracked service changes for {len(change_metrics)} clients")
    return change_metrics


def predict_contract_renewal(df: pd.DataFrame,
                           client_id_col: str = 'client_id',
                           contract_end_date_col: str = 'contract_end_date',
                           renewal_probability_col: str = 'renewal_probability',
                           engagement_score_col: str = 'engagement_score') -> pd.DataFrame:
    """
    Predict contract renewal likelihood
    
    Args:
        df: Input DataFrame with contract data
        client_id_col: Column name for client identifier
        contract_end_date_col: Column name for contract end date
        renewal_probability_col: Column name for renewal probability
        engagement_score_col: Column name for engagement score
    
    Returns:
        DataFrame with contract renewal predictions
    """
    df_renewal = df.copy()
    
    # Convert date column to datetime
    df_renewal[contract_end_date_col] = pd.to_datetime(df_renewal[contract_end_date_col])
    
    # Calculate days until contract end
    df_renewal['days_until_end'] = (
        df_renewal[contract_end_date_col] - pd.Timestamp.now()
    ).dt.days
    
    # Calculate renewal risk factors
    df_renewal['time_pressure'] = np.where(
        df_renewal['days_until_end'] <= 30,
        1.0 - (df_renewal['days_until_end'] / 30),
        0
    )
    
    # Calculate renewal score (combination of existing probability and engagement)
    df_renewal['renewal_score'] = (
        0.6 * df_renewal[renewal_probability_col].fillna(0.5) +
        0.3 * df_renewal[engagement_score_col].fillna(0.5) +
        0.1 * (1 - df_renewal['time_pressure'].fillna(0))
    )
    
    # Categorize renewal likelihood
    df_renewal['renewal_likelihood'] = pd.cut(
        df_renewal['renewal_score'],
        bins=[0, 0.33, 0.66, 1.0],
        labels=['Low', 'Medium', 'High']
    )
    
    # Group by client
    renewal_predictions = df_renewal.groupby(client_id_col).agg({
        'days_until_end': 'min',
        renewal_probability_col: 'mean',
        engagement_score_col: 'mean',
        'renewal_score': 'mean',
        'renewal_likelihood': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown'
    }).reset_index()
    
    logger.info(f"Predicted contract renewal for {len(renewal_predictions)} clients")
    return renewal_predictions


def analyze_support_requests(df: pd.DataFrame,
                           client_id_col: str = 'client_id',
                           request_date_col: str = 'request_date',
                           request_type_col: str = 'request_type',
                           resolution_satisfaction_col: str = 'resolution_satisfaction') -> pd.DataFrame:
    """
    Analyze support request patterns
    
    Args:
        df: Input DataFrame with support request data
        client_id_col: Column name for client identifier
        request_date_col: Column name for request date
        request_type_col: Column name for request type
        resolution_satisfaction_col: Column name for resolution satisfaction score
    
    Returns:
        DataFrame with support request analysis metrics
    """
    df_requests = df.copy()
    
    # Convert date column to datetime
    df_requests[request_date_col] = pd.to_datetime(df_requests[request_date_col])
    
    # Extract time components
    df_requests['month'] = df_requests[request_date_col].dt.month
    df_requests['day_of_week'] = df_requests[request_date_col].dt.dayofweek
    
    # Group by client to calculate request metrics
    request_metrics = df_requests.groupby(client_id_col).agg({
        request_date_col: 'count',  # Total requests
        request_type_col: lambda x: x.value_counts().to_dict(),  # Request type distribution
        resolution_satisfaction_col: ['mean', 'std'],
        'month': lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,  # Peak month
        'day_of_week': lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan  # Peak day
    }).reset_index()
    
    # Flatten column names
    request_metrics.columns = [
        client_id_col,
        'total_requests', 'request_type_distribution',
        'avg_satisfaction', 'std_satisfaction',
        'peak_month', 'peak_day_of_week'
    ]
    
    # Calculate request frequency score
    request_metrics['request_frequency_score'] = request_metrics['total_requests']
    
    # Calculate satisfaction trend
    request_metrics['satisfaction_trend'] = request_metrics['avg_satisfaction'].fillna(0)
    
    logger.info(f"Analyzed support requests for {len(request_metrics)} clients")
    return request_metrics


def analyze_feedback_sentiment(df: pd.DataFrame,
                             client_id_col: str = 'client_id',
                             feedback_date_col: str = 'feedback_date',
                             sentiment_score_col: str = 'sentiment_score',
                             feedback_category_col: str = 'feedback_category') -> pd.DataFrame:
    """
    Analyze feedback sentiment
    
    Args:
        df: Input DataFrame with feedback data
        client_id_col: Column name for client identifier
        feedback_date_col: Column name for feedback date
        sentiment_score_col: Column name for sentiment score
        feedback_category_col: Column name for feedback category
    
    Returns:
        DataFrame with feedback sentiment metrics
    """
    df_feedback = df.copy()
    
    # Convert date column to datetime
    df_feedback[feedback_date_col] = pd.to_datetime(df_feedback[feedback_date_col])
    
    # Group by client to calculate sentiment metrics
    sentiment_metrics = df_feedback.groupby(client_id_col).agg({
        feedback_date_col: 'count',  # Total feedbacks
        sentiment_score_col: ['mean', 'std'],
        feedback_category_col: lambda x: x.value_counts().to_dict()  # Category distribution
    }).reset_index()
    
    # Flatten column names
    sentiment_metrics.columns = [
        client_id_col,
        'total_feedbacks', 'avg_sentiment', 'std_sentiment',
        'feedback_category_distribution'
    ]
    
    # Calculate sentiment trend
    sentiment_metrics['sentiment_trend'] = np.where(
        sentiment_metrics['avg_sentiment'] > 0,
        'Positive',
        np.where(sentiment_metrics['avg_sentiment'] < 0, 'Negative', 'Neutral')
    )
    
    # Calculate sentiment volatility
    sentiment_metrics['sentiment_volatility'] = sentiment_metrics['std_sentiment'].fillna(0)
    
    # Calculate overall sentiment score
    sentiment_metrics['overall_sentiment_score'] = sentiment_metrics['avg_sentiment'].fillna(0)
    
    logger.info(f"Analyzed feedback sentiment for {len(sentiment_metrics)} clients")
    return sentiment_metrics


def identify_usage_patterns(df: pd.DataFrame,
                          client_id_col: str = 'client_id',
                          usage_date_col: str = 'usage_date',
                          feature_name_col: str = 'feature_name',
                          usage_duration_col: str = 'usage_duration_minutes') -> pd.DataFrame:
    """
    Identify usage pattern analysis
    
    Args:
        df: Input DataFrame with usage data
        client_id_col: Column name for client identifier
        usage_date_col: Column name for usage date
        feature_name_col: Column name for feature name
        usage_duration_col: Column name for usage duration in minutes
    
    Returns:
        DataFrame with usage pattern metrics
    """
    df_usage = df.copy()
    
    # Convert date column to datetime
    df_usage[usage_date_col] = pd.to_datetime(df_usage[usage_date_col])
    
    # Extract time components
    df_usage['day_of_week'] = df_usage[usage_date_col].dt.dayofweek
    df_usage['hour_of_day'] = df_usage[usage_date_col].dt.hour
    df_usage['month'] = df_usage[usage_date_col].dt.month
    
    # Group by client to calculate usage metrics
    usage_metrics = df_usage.groupby(client_id_col).agg({
        usage_date_col: 'count',  # Total usage sessions
        usage_duration_col: ['sum', 'mean', 'std'],
        feature_name_col: lambda x: list(x.unique()),  # Features used
        'day_of_week': lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,  # Peak day
        'hour_of_day': lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan   # Peak hour
    }).reset_index()
    
    # Flatten column names
    usage_metrics.columns = [
        client_id_col,
        'total_sessions', 'total_usage_minutes', 'avg_session_duration', 'std_session_duration',
        'features_used', 'peak_day', 'peak_hour'
    ]
    
    # Calculate usage intensity
    usage_metrics['usage_intensity'] = (
        usage_metrics['total_usage_minutes'] / usage_metrics['total_sessions']
    ).fillna(0)
    
    # Calculate consistency score (lower std means more consistent)
    usage_metrics['consistency_score'] = 1 / (1 + usage_metrics['std_session_duration'].fillna(0))
    
    logger.info(f"Identified usage patterns for {len(usage_metrics)} clients")
    return usage_metrics


def calculate_churn_risk(df: pd.DataFrame,
                       client_id_col: str = 'client_id',
                       engagement_score_col: str = 'engagement_score',
                       support_ticket_count_col: str = 'support_ticket_count',
                       contract_renewal_likelihood_col: str = 'contract_renewal_likelihood',
                       payment_delinquency_col: str = 'payment_delinquency_rate') -> pd.DataFrame:
    """
    Calculate churn risk indicators
    
    Args:
        df: Input DataFrame with client data
        client_id_col: Column name for client identifier
        engagement_score_col: Column name for engagement score
        support_ticket_count_col: Column name for support ticket count
        contract_renewal_likelihood_col: Column name for contract renewal likelihood
        payment_delinquency_col: Column name for payment delinquency rate
    
    Returns:
        DataFrame with churn risk metrics
    """
    df_churn = df.copy()
    
    # Calculate churn risk factors
    # Low engagement is a risk factor
    df_churn['engagement_risk'] = np.where(
        df_churn[engagement_score_col] < 0.3,
        1.0,
        np.where(df_churn[engagement_score_col] < 0.6, 0.5, 0.0)
    )
    
    # High support ticket count is a risk factor
    df_churn['support_risk'] = np.where(
        df_churn[support_ticket_count_col] > df_churn[support_ticket_count_col].quantile(0.75),
        1.0,
        np.where(df_churn[support_ticket_count_col] > df_churn[support_ticket_count_col].quantile(0.5), 0.5, 0.0)
    )
    
    # Low contract renewal likelihood is a risk factor
    def map_renewal_risk(value):
        if value == 'High':
            return 0.0
        elif value == 'Medium':
            return 0.5
        elif value == 'Low':
            return 1.0
        else:
            return 0.5
    
    df_churn['renewal_risk'] = df_churn[contract_renewal_likelihood_col].apply(map_renewal_risk)
    
    # High payment delinquency is a risk factor
    df_churn['payment_risk'] = np.where(
        df_churn[payment_delinquency_col] > 0.2,
        1.0,
        np.where(df_churn[payment_delinquency_col] > 0.1, 0.5, 0.0)
    )
    
    # Calculate overall churn risk score (0-1 scale)
    df_churn['churn_risk_score'] = (
        0.3 * df_churn['engagement_risk'] +
        0.2 * df_churn['support_risk'] +
        0.3 * df_churn['renewal_risk'] +
        0.2 * df_churn['payment_risk']
    )
    
    # Categorize churn risk
    df_churn['churn_risk_level'] = pd.cut(
        df_churn['churn_risk_score'],
        bins=[0, 0.33, 0.66, 1.0],
        labels=['Low', 'Medium', 'High']
    )
    
    # Group by client
    churn_risk_metrics = df_churn.groupby(client_id_col).agg({
        engagement_score_col: 'mean',
        support_ticket_count_col: 'sum',
        contract_renewal_likelihood_col: lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown',
        payment_delinquency_col: 'mean',
        'churn_risk_score': 'mean',
        'churn_risk_level': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown'
    }).reset_index()
    
    logger.info(f"Calculated churn risk for {len(churn_risk_metrics)} clients")
    return churn_risk_metrics