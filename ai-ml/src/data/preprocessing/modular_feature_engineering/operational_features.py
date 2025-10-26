"""
Operational Features Engine
Module for extracting operational features from MSP data for AI/ML models
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


def calculate_ticket_resolution_time(df: pd.DataFrame,
                                   ticket_id_col: str = 'ticket_id',
                                   created_date_col: str = 'created_date',
                                   resolved_date_col: str = 'resolved_date') -> pd.DataFrame:
    """
    Calculate average ticket resolution time
    
    Args:
        df: Input DataFrame with ticket data
        ticket_id_col: Column name for ticket identifier
        created_date_col: Column name for ticket creation date
        resolved_date_col: Column name for ticket resolution date
    
    Returns:
        DataFrame with ticket_id and resolution_time_hours
    """
    df_resolution = df.copy()
    
    # Convert date columns to datetime
    df_resolution[created_date_col] = pd.to_datetime(df_resolution[created_date_col])
    df_resolution[resolved_date_col] = pd.to_datetime(df_resolution[resolved_date_col])
    
    # Calculate resolution time in hours
    df_resolution['resolution_time_hours'] = (
        df_resolution[resolved_date_col] - df_resolution[created_date_col]
    ).dt.total_seconds() / 3600
    
    # Group by ticket to get average resolution time
    resolution_times = df_resolution.groupby(ticket_id_col)['resolution_time_hours'].mean().reset_index()
    
    logger.info(f"Calculated ticket resolution times for {len(resolution_times)} tickets")
    return resolution_times


def calculate_sla_compliance(df: pd.DataFrame,
                           ticket_id_col: str = 'ticket_id',
                           sla_target_hours_col: str = 'sla_target_hours',
                           actual_resolution_hours_col: str = 'actual_resolution_hours') -> pd.DataFrame:
    """
    Calculate SLA compliance percentage
    
    Args:
        df: Input DataFrame with SLA data
        ticket_id_col: Column name for ticket identifier
        sla_target_hours_col: Column name for SLA target hours
        actual_resolution_hours_col: Column name for actual resolution hours
    
    Returns:
        DataFrame with SLA compliance metrics
    """
    df_sla = df.copy()
    
    # Determine if SLA was met
    df_sla['sla_met'] = df_sla[actual_resolution_hours_col] <= df_sla[sla_target_hours_col]
    
    # Calculate SLA compliance rate
    sla_compliance = df_sla.groupby(ticket_id_col).agg({
        'sla_met': 'mean',  # This gives the proportion of SLA met
        sla_target_hours_col: 'mean',
        actual_resolution_hours_col: 'mean'
    }).reset_index()
    
    sla_compliance = sla_compliance.rename(columns={'sla_met': 'sla_compliance_rate'})
    
    # Calculate SLA breach rate
    sla_compliance['sla_breach_rate'] = 1 - sla_compliance['sla_compliance_rate']
    
    logger.info(f"Calculated SLA compliance for {len(sla_compliance)} tickets")
    return sla_compliance


def calculate_technician_productivity(df: pd.DataFrame,
                                    technician_id_col: str = 'technician_id',
                                    tickets_handled_col: str = 'tickets_handled',
                                    total_hours_col: str = 'total_hours_worked',
                                    tickets_resolved_col: str = 'tickets_resolved') -> pd.DataFrame:
    """
    Calculate technician productivity scores
    
    Args:
        df: Input DataFrame with technician data
        technician_id_col: Column name for technician identifier
        tickets_handled_col: Column name for number of tickets handled
        total_hours_col: Column name for total hours worked
        tickets_resolved_col: Column name for tickets resolved
    
    Returns:
        DataFrame with technician productivity metrics
    """
    df_productivity = df.copy()
    
    # Calculate tickets per hour
    df_productivity['tickets_per_hour'] = np.where(
        df_productivity[total_hours_col] != 0,
        df_productivity[tickets_handled_col] / df_productivity[total_hours_col],
        np.nan
    )
    
    # Calculate resolution rate
    df_productivity['resolution_rate'] = np.where(
        df_productivity[tickets_handled_col] != 0,
        df_productivity[tickets_resolved_col] / df_productivity[tickets_handled_col],
        np.nan
    )
    
    # Calculate productivity score (weighted combination)
    df_productivity['productivity_score'] = (
        0.5 * df_productivity['tickets_per_hour'].fillna(0) +
        0.3 * df_productivity['resolution_rate'].fillna(0) +
        0.2 * (df_productivity[tickets_handled_col] / df_productivity[tickets_handled_col].max()).fillna(0)
    )
    
    # Group by technician
    productivity_scores = df_productivity.groupby(technician_id_col).agg({
        tickets_handled_col: 'sum',
        tickets_resolved_col: 'sum',
        total_hours_col: 'sum',
        'tickets_per_hour': 'mean',
        'resolution_rate': 'mean',
        'productivity_score': 'mean'
    }).reset_index()
    
    logger.info(f"Calculated technician productivity for {len(productivity_scores)} technicians")
    return productivity_scores


def assess_service_delivery_quality(df: pd.DataFrame,
                                 service_id_col: str = 'service_id',
                                 quality_score_col: str = 'quality_score',
                                 customer_rating_col: str = 'customer_rating',
                                 first_time_fix_col: str = 'first_time_fix') -> pd.DataFrame:
    """
    Assess service delivery quality metrics
    
    Args:
        df: Input DataFrame with service delivery data
        service_id_col: Column name for service identifier
        quality_score_col: Column name for quality scores
        customer_rating_col: Column name for customer ratings
        first_time_fix_col: Column name for first time fix indicator (boolean)
    
    Returns:
        DataFrame with service delivery quality metrics
    """
    df_quality = df.copy()
    
    # Calculate first time fix rate
    df_quality['first_time_fix_rate'] = df_quality[first_time_fix_col].astype(int)
    
    # Group by service to calculate quality metrics
    quality_metrics = df_quality.groupby(service_id_col).agg({
        quality_score_col: ['mean', 'std'],
        customer_rating_col: ['mean', 'std'],
        'first_time_fix_rate': 'mean'
    }).reset_index()
    
    # Flatten column names
    quality_metrics.columns = [
        service_id_col,
        'avg_quality_score', 'std_quality_score',
        'avg_customer_rating', 'std_customer_rating',
        'first_time_fix_rate'
    ]
    
    # Calculate overall quality index
    quality_metrics['quality_index'] = (
        0.4 * quality_metrics['avg_quality_score'] +
        0.4 * quality_metrics['avg_customer_rating'] +
        0.2 * quality_metrics['first_time_fix_rate'] * 10  # Scale to 0-10
    )
    
    logger.info(f"Assessed service delivery quality for {len(quality_metrics)} services")
    return quality_metrics


def calculate_client_satisfaction(df: pd.DataFrame,
                               client_id_col: str = 'client_id',
                               satisfaction_score_col: str = 'satisfaction_score',
                               feedback_count_col: str = 'feedback_count',
                               positive_feedback_col: str = 'positive_feedback_count') -> pd.DataFrame:
    """
    Calculate client satisfaction scores
    
    Args:
        df: Input DataFrame with client satisfaction data
        client_id_col: Column name for client identifier
        satisfaction_score_col: Column name for satisfaction scores
        feedback_count_col: Column name for total feedback count
        positive_feedback_col: Column name for positive feedback count
    
    Returns:
        DataFrame with client satisfaction metrics
    """
    df_satisfaction = df.copy()
    
    # Calculate satisfaction rate
    df_satisfaction['satisfaction_rate'] = np.where(
        df_satisfaction[feedback_count_col] != 0,
        df_satisfaction[positive_feedback_col] / df_satisfaction[feedback_count_col],
        np.nan
    )
    
    # Group by client to calculate satisfaction metrics
    satisfaction_metrics = df_satisfaction.groupby(client_id_col).agg({
        satisfaction_score_col: ['mean', 'std'],
        feedback_count_col: 'sum',
        positive_feedback_col: 'sum',
        'satisfaction_rate': 'mean'
    }).reset_index()
    
    # Flatten column names
    satisfaction_metrics.columns = [
        client_id_col,
        'avg_satisfaction_score', 'std_satisfaction_score',
        'total_feedback_count', 'positive_feedback_count',
        'satisfaction_rate'
    ]
    
    # Calculate net satisfaction score
    satisfaction_metrics['net_satisfaction_score'] = (
        satisfaction_metrics['avg_satisfaction_score'] * satisfaction_metrics['satisfaction_rate']
    )
    
    logger.info(f"Calculated client satisfaction for {len(satisfaction_metrics)} clients")
    return satisfaction_metrics


def analyze_ticket_frequency(df: pd.DataFrame,
                           client_id_col: str = 'client_id',
                           ticket_date_col: str = 'ticket_date',
                           ticket_type_col: str = 'ticket_type') -> pd.DataFrame:
    """
    Analyze support ticket frequency patterns
    
    Args:
        df: Input DataFrame with ticket data
        client_id_col: Column name for client identifier
        ticket_date_col: Column name for ticket date
        ticket_type_col: Column name for ticket type
    
    Returns:
        DataFrame with ticket frequency metrics
    """
    df_frequency = df.copy()
    
    # Convert date column to datetime
    df_frequency[ticket_date_col] = pd.to_datetime(df_frequency[ticket_date_col])
    
    # Extract time components
    df_frequency['year'] = df_frequency[ticket_date_col].dt.year
    df_frequency['month'] = df_frequency[ticket_date_col].dt.month
    df_frequency['week'] = df_frequency[ticket_date_col].dt.isocalendar().week
    
    # Calculate ticket frequency metrics
    # Tickets per month per client
    monthly_frequency = df_frequency.groupby([client_id_col, 'year', 'month']).size().to_frame('tickets_per_month').reset_index()
    
    # Tickets per week per client
    weekly_frequency = df_frequency.groupby([client_id_col, 'year', 'week']).size().to_frame('tickets_per_week').reset_index()
    
    # Ticket type distribution
    ticket_type_dist = df_frequency.groupby([client_id_col, ticket_type_col]).size().to_frame('ticket_count').reset_index()
    ticket_type_dist['ticket_type_percentage'] = ticket_type_dist.groupby(client_id_col)['ticket_count'].transform(lambda x: x / x.sum())
    
    # Calculate average tickets per period
    avg_metrics = df_frequency.groupby(client_id_col).size().to_frame('total_tickets').reset_index()
    avg_metrics['avg_tickets_per_month'] = avg_metrics['total_tickets'] / 12  # Assuming 12 months of data
    avg_metrics['avg_tickets_per_week'] = avg_metrics['total_tickets'] / 52   # Assuming 52 weeks of data
    
    logger.info(f"Analyzed ticket frequency patterns for {len(avg_metrics)} clients")
    return avg_metrics


def track_service_level_trends(df: pd.DataFrame,
                             service_id_col: str = 'service_id',
                             date_col: str = 'date',
                             performance_metric_col: str = 'performance_score') -> pd.DataFrame:
    """
    Track service level trends over time
    
    Args:
        df: Input DataFrame with service performance data
        service_id_col: Column name for service identifier
        date_col: Column name for date information
        performance_metric_col: Column name for performance metrics
    
    Returns:
        DataFrame with service level trends
    """
    df_trends = df.copy()
    
    # Convert date column to datetime
    df_trends[date_col] = pd.to_datetime(df_trends[date_col])
    
    # Extract time periods
    df_trends['year'] = df_trends[date_col].dt.year
    df_trends['month'] = df_trends[date_col].dt.month
    df_trends['quarter'] = df_trends[date_col].dt.quarter
    
    # Calculate performance trends by service and period
    monthly_trends = df_trends.groupby([service_id_col, 'year', 'month'])[performance_metric_col].mean().reset_index()
    quarterly_trends = df_trends.groupby([service_id_col, 'year', 'quarter'])[performance_metric_col].mean().reset_index()
    
    # Calculate trend indicators
    monthly_trends['prev_month_performance'] = monthly_trends.groupby(service_id_col)[performance_metric_col].shift(1)
    monthly_trends['monthly_trend'] = (
        monthly_trends[performance_metric_col] - monthly_trends['prev_month_performance']
    )
    
    quarterly_trends['prev_quarter_performance'] = quarterly_trends.groupby(service_id_col)[performance_metric_col].shift(1)
    quarterly_trends['quarterly_trend'] = (
        quarterly_trends[performance_metric_col] - quarterly_trends['prev_quarter_performance']
    )
    
    # Combine trends into a single DataFrame
    monthly_trends['period_type'] = 'monthly'
    quarterly_trends['period_type'] = 'quarterly'
    
    # Rename columns for consistency
    quarterly_trends = quarterly_trends.rename(columns={'quarter': 'month'})
    
    trends_analysis = pd.concat([monthly_trends, quarterly_trends], ignore_index=True)
    
    logger.info(f"Tracked service level trends for {len(trends_analysis)} service-period combinations")
    return trends_analysis


def calculate_resource_utilization(df: pd.DataFrame,
                                resource_id_col: str = 'resource_id',
                                allocated_hours_col: str = 'allocated_hours',
                                used_hours_col: str = 'used_hours',
                                capacity_hours_col: str = 'capacity_hours') -> pd.DataFrame:
    """
    Calculate resource utilization metrics
    
    Args:
        df: Input DataFrame with resource data
        resource_id_col: Column name for resource identifier
        allocated_hours_col: Column name for allocated hours
        used_hours_col: Column name for used hours
        capacity_hours_col: Column name for capacity hours
    
    Returns:
        DataFrame with resource utilization metrics
    """
    df_utilization = df.copy()
    
    # Calculate allocation rate
    df_utilization['allocation_rate'] = np.where(
        df_utilization[capacity_hours_col] != 0,
        df_utilization[allocated_hours_col] / df_utilization[capacity_hours_col],
        np.nan
    )
    
    # Calculate utilization rate
    df_utilization['utilization_rate'] = np.where(
        df_utilization[capacity_hours_col] != 0,
        df_utilization[used_hours_col] / df_utilization[capacity_hours_col],
        np.nan
    )
    
    # Calculate efficiency rate
    df_utilization['efficiency_rate'] = np.where(
        df_utilization[allocated_hours_col] != 0,
        df_utilization[used_hours_col] / df_utilization[allocated_hours_col],
        np.nan
    )
    
    # Group by resource to calculate overall metrics
    resource_utilization = df_utilization.groupby(resource_id_col).agg({
        allocated_hours_col: 'sum',
        used_hours_col: 'sum',
        capacity_hours_col: 'mean',
        'allocation_rate': 'mean',
        'utilization_rate': 'mean',
        'efficiency_rate': 'mean'
    }).reset_index()
    
    # Calculate resource utilization score
    resource_utilization['utilization_score'] = (
        0.4 * resource_utilization['utilization_rate'].fillna(0) +
        0.3 * resource_utilization['allocation_rate'].fillna(0) +
        0.3 * resource_utilization['efficiency_rate'].fillna(0)
    )
    
    logger.info(f"Calculated resource utilization for {len(resource_utilization)} resources")
    return resource_utilization