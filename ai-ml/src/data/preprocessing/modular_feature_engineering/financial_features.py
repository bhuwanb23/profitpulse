"""
Financial Features Engine
Module for extracting financial features from MSP data for AI/ML models
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


def calculate_revenue_per_client(df: pd.DataFrame, 
                               client_id_col: str = 'client_id',
                               revenue_col: str = 'revenue',
                               date_col: str = 'date',
                               frequency: str = 'monthly') -> pd.DataFrame:
    """
    Calculate revenue per client on monthly or quarterly basis
    
    Args:
        df: Input DataFrame with client, revenue, and date information
        client_id_col: Column name for client identifier
        revenue_col: Column name for revenue values
        date_col: Column name for date information
        frequency: 'monthly' or 'quarterly' aggregation
    
    Returns:
        DataFrame with client_id and revenue per period
    """
    df_financial = df.copy()
    
    # Convert date column to datetime
    df_financial[date_col] = pd.to_datetime(df_financial[date_col])
    
    # Extract period based on frequency
    if frequency == 'monthly':
        df_financial['period'] = df_financial[date_col].dt.to_period('M')
    elif frequency == 'quarterly':
        df_financial['period'] = df_financial[date_col].dt.to_period('Q')
    else:
        raise ValueError("Frequency must be 'monthly' or 'quarterly'")
    
    # Group by client and period, sum revenue
    revenue_per_client = df_financial.groupby([client_id_col, 'period'])[revenue_col].sum().reset_index()
    revenue_per_client = revenue_per_client.rename(columns={revenue_col: f'{frequency}_revenue'})
    
    logger.info(f"Calculated {frequency} revenue per client for {len(revenue_per_client)} records")
    return revenue_per_client


def calculate_profit_margins_by_service(df: pd.DataFrame,
                                      service_type_col: str = 'service_type',
                                      revenue_col: str = 'revenue',
                                      cost_col: str = 'cost') -> pd.DataFrame:
    """
    Calculate profit margins by service type
    
    Args:
        df: Input DataFrame with service type, revenue, and cost information
        service_type_col: Column name for service type
        revenue_col: Column name for revenue values
        cost_col: Column name for cost values
    
    Returns:
        DataFrame with service_type and profit_margin
    """
    df_margins = df.copy()
    
    # Calculate profit and margin for each record
    df_margins['profit'] = df_margins[revenue_col] - df_margins[cost_col]
    df_margins['profit_margin'] = np.where(
        df_margins[revenue_col] != 0,
        df_margins['profit'] / df_margins[revenue_col],
        0
    )
    
    # Group by service type and calculate average margin
    profit_margins = df_margins.groupby(service_type_col).agg({
        revenue_col: 'sum',
        cost_col: 'sum',
        'profit': 'sum',
        'profit_margin': 'mean'
    }).reset_index()
    
    logger.info(f"Calculated profit margins for {len(profit_margins)} service types")
    return profit_margins


def calculate_billing_efficiency(df: pd.DataFrame,
                              billed_amount_col: str = 'billed_amount',
                              actual_cost_col: str = 'actual_cost',
                              expected_amount_col: str = 'expected_amount') -> pd.DataFrame:
    """
    Calculate billing efficiency metrics
    
    Args:
        df: Input DataFrame with billing data
        billed_amount_col: Column name for billed amounts
        actual_cost_col: Column name for actual costs
        expected_amount_col: Column name for expected billing amounts
    
    Returns:
        DataFrame with billing efficiency metrics
    """
    df_efficiency = df.copy()
    
    # Calculate billing accuracy (how close billed amount is to expected)
    df_efficiency['billing_accuracy'] = np.where(
        df_efficiency[expected_amount_col] != 0,
        df_efficiency[billed_amount_col] / df_efficiency[expected_amount_col],
        np.nan
    )
    
    # Calculate cost recovery ratio (billed vs actual cost)
    df_efficiency['cost_recovery_ratio'] = np.where(
        df_efficiency[actual_cost_col] != 0,
        df_efficiency[billed_amount_col] / df_efficiency[actual_cost_col],
        np.nan
    )
    
    # Calculate billing efficiency score (0-1 scale)
    df_efficiency['billing_efficiency_score'] = np.clip(
        df_efficiency['billing_accuracy'] * df_efficiency['cost_recovery_ratio'],
        0, 1
    )
    
    logger.info(f"Calculated billing efficiency metrics for {len(df_efficiency)} records")
    return df_efficiency


def calculate_cost_per_ticket_resolution(df: pd.DataFrame,
                                       ticket_id_col: str = 'ticket_id',
                                       cost_col: str = 'cost',
                                       resolution_time_col: str = 'resolution_time_hours') -> pd.DataFrame:
    """
    Calculate cost per ticket resolution
    
    Args:
        df: Input DataFrame with ticket data
        ticket_id_col: Column name for ticket identifier
        cost_col: Column name for cost values
        resolution_time_col: Column name for resolution time in hours
    
    Returns:
        DataFrame with ticket_id and cost_per_hour metrics
    """
    df_cost = df.copy()
    
    # Calculate cost per hour of resolution
    df_cost['cost_per_hour'] = np.where(
        df_cost[resolution_time_col] != 0,
        df_cost[cost_col] / df_cost[resolution_time_col],
        np.nan
    )
    
    # Calculate average cost per ticket
    cost_per_ticket = df_cost.groupby(ticket_id_col).agg({
        cost_col: 'sum',
        resolution_time_col: 'sum'
    }).reset_index()
    
    cost_per_ticket['avg_cost_per_hour'] = np.where(
        cost_per_ticket[resolution_time_col] != 0,
        cost_per_ticket[cost_col] / cost_per_ticket[resolution_time_col],
        np.nan
    )
    
    logger.info(f"Calculated cost per ticket resolution for {len(cost_per_ticket)} tickets")
    return cost_per_ticket


def calculate_service_utilization_rates(df: pd.DataFrame,
                                      service_id_col: str = 'service_id',
                                      usage_col: str = 'usage_hours',
                                      available_hours_col: str = 'available_hours') -> pd.DataFrame:
    """
    Calculate service utilization rates
    
    Args:
        df: Input DataFrame with service usage data
        service_id_col: Column name for service identifier
        usage_col: Column name for actual usage hours
        available_hours_col: Column name for available hours
    
    Returns:
        DataFrame with service_id and utilization_rate
    """
    df_utilization = df.copy()
    
    # Calculate utilization rate
    df_utilization['utilization_rate'] = np.where(
        df_utilization[available_hours_col] != 0,
        df_utilization[usage_col] / df_utilization[available_hours_col],
        np.nan
    )
    
    # Group by service and calculate average utilization
    utilization_rates = df_utilization.groupby(service_id_col).agg({
        usage_col: 'sum',
        available_hours_col: 'sum',
        'utilization_rate': 'mean'
    }).reset_index()
    
    logger.info(f"Calculated service utilization rates for {len(utilization_rates)} services")
    return utilization_rates


def analyze_payment_behavior(df: pd.DataFrame,
                           client_id_col: str = 'client_id',
                           payment_date_col: str = 'payment_date',
                           payment_amount_col: str = 'payment_amount',
                           due_date_col: str = 'due_date') -> pd.DataFrame:
    """
    Analyze payment behavior patterns
    
    Args:
        df: Input DataFrame with payment data
        client_id_col: Column name for client identifier
        payment_date_col: Column name for payment date
        payment_amount_col: Column name for payment amount
        due_date_col: Column name for due date
    
    Returns:
        DataFrame with payment behavior metrics
    """
    df_payments = df.copy()
    
    # Convert date columns to datetime
    df_payments[payment_date_col] = pd.to_datetime(df_payments[payment_date_col])
    df_payments[due_date_col] = pd.to_datetime(df_payments[due_date_col])
    
    # Calculate days late (negative means early payment)
    df_payments['days_late'] = (df_payments[payment_date_col] - df_payments[due_date_col]).dt.days
    df_payments['is_late'] = df_payments['days_late'] > 0
    df_payments['is_early'] = df_payments['days_late'] < 0
    
    # Group by client to calculate payment behavior metrics
    payment_behavior = df_payments.groupby(client_id_col).agg({
        payment_amount_col: ['sum', 'mean', 'count'],
        'days_late': ['mean', 'std'],
        'is_late': 'sum',  # Count of late payments
        'is_early': 'sum'  # Count of early payments
    }).reset_index()
    
    # Flatten column names
    payment_behavior.columns = [
        client_id_col,
        'total_payments', 'avg_payment_amount', 'payment_count',
        'avg_days_late', 'std_days_late',
        'late_payment_count', 'early_payment_count'
    ]
    
    # Calculate additional metrics
    payment_behavior['late_payment_rate'] = (
        payment_behavior['late_payment_count'] / payment_behavior['payment_count']
    )
    payment_behavior['early_payment_rate'] = (
        payment_behavior['early_payment_count'] / payment_behavior['payment_count']
    )
    
    logger.info(f"Analyzed payment behavior for {len(payment_behavior)} clients")
    return payment_behavior


def calculate_revenue_growth_trends(df: pd.DataFrame,
                                  client_id_col: str = 'client_id',
                                  revenue_col: str = 'revenue',
                                  date_col: str = 'date',
                                  period: str = 'month') -> pd.DataFrame:
    """
    Calculate revenue growth trends
    
    Args:
        df: Input DataFrame with revenue data over time
        client_id_col: Column name for client identifier
        revenue_col: Column name for revenue values
        date_col: Column name for date information
        period: Time period for growth calculation ('month', 'quarter', 'year')
    
    Returns:
        DataFrame with revenue growth trends
    """
    df_growth = df.copy()
    
    # Convert date column to datetime
    df_growth[date_col] = pd.to_datetime(df_growth[date_col])
    
    # Extract period
    if period == 'month':
        df_growth['period'] = df_growth[date_col].dt.to_period('M')
    elif period == 'quarter':
        df_growth['period'] = df_growth[date_col].dt.to_period('Q')
    elif period == 'year':
        df_growth['period'] = df_growth[date_col].dt.to_period('Y')
    else:
        raise ValueError("Period must be 'month', 'quarter', or 'year'")
    
    # Calculate revenue by period and client
    period_revenue = df_growth.groupby([client_id_col, 'period'])[revenue_col].sum().reset_index()
    period_revenue = period_revenue.sort_values([client_id_col, 'period'])
    
    # Calculate growth rates
    period_revenue['prev_revenue'] = period_revenue.groupby(client_id_col)[revenue_col].shift(1)
    period_revenue['growth_rate'] = np.where(
        period_revenue['prev_revenue'] != 0,
        (period_revenue[revenue_col] - period_revenue['prev_revenue']) / period_revenue['prev_revenue'],
        np.nan
    )
    
    # Calculate cumulative growth
    period_revenue['cumulative_growth'] = period_revenue.groupby(client_id_col)['growth_rate'].cumsum()
    
    logger.info(f"Calculated revenue growth trends for {len(period_revenue)} client-period combinations")
    return period_revenue


def calculate_profitability_ratios(df: pd.DataFrame,
                                 revenue_col: str = 'revenue',
                                 cost_col: str = 'cost',
                                 expense_col: str = 'expenses',
                                 asset_col: str = 'total_assets') -> pd.DataFrame:
    """
    Calculate various profitability ratios
    
    Args:
        df: Input DataFrame with financial data
        revenue_col: Column name for revenue values
        cost_col: Column name for cost values
        expense_col: Column name for expense values
        asset_col: Column name for asset values (optional)
    
    Returns:
        DataFrame with profitability ratios
    """
    df_ratios = df.copy()
    
    # Calculate gross profit
    df_ratios['gross_profit'] = df_ratios[revenue_col] - df_ratios[cost_col]
    
    # Calculate gross profit margin
    df_ratios['gross_profit_margin'] = np.where(
        df_ratios[revenue_col] != 0,
        df_ratios['gross_profit'] / df_ratios[revenue_col],
        np.nan
    )
    
    # Calculate net profit (revenue - cost - expenses)
    df_ratios['net_profit'] = df_ratios[revenue_col] - df_ratios[cost_col] - df_ratios[expense_col]
    
    # Calculate net profit margin
    df_ratios['net_profit_margin'] = np.where(
        df_ratios[revenue_col] != 0,
        df_ratios['net_profit'] / df_ratios[revenue_col],
        np.nan
    )
    
    # Calculate return on assets (if asset data available)
    df_ratios['return_on_assets'] = np.where(
        df_ratios[asset_col] != 0,
        df_ratios['net_profit'] / df_ratios[asset_col],
        np.nan
    )
    
    # Calculate operating margin
    df_ratios['operating_margin'] = np.where(
        df_ratios[revenue_col] != 0,
        (df_ratios[revenue_col] - df_ratios[expense_col]) / df_ratios[revenue_col],
        np.nan
    )
    
    logger.info(f"Calculated profitability ratios for {len(df_ratios)} records")
    return df_ratios