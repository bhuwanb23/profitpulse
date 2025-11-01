"""
Market Analysis for Dynamic Pricing Engine
Handles market sensitivity analysis and competitive positioning
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class MarketTrendAnalyzer:
    """Analyzer for market trends and patterns"""
    
    def __init__(self):
        """Initialize market trend analyzer"""
        logger.info("Market Trend Analyzer initialized")
    
    def analyze_market_trends(self, market_data: pd.DataFrame, 
                            service_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Analyze market trends for different service types
        
        Args:
            market_data: DataFrame with market rate data
            service_types: List of service types to analyze (optional)
            
        Returns:
            Dictionary with trend analysis results
        """
        try:
            if market_data.empty:
                logger.warning("No market data available for trend analysis")
                return {}
            
            # Filter by service types if specified
            if service_types:
                market_data_filtered = market_data[market_data['service_type'].isin(service_types)]
                if isinstance(market_data_filtered, pd.DataFrame):
                    market_data = market_data_filtered
                else:
                    # If filtering returns a Series, convert back to DataFrame
                    market_data = pd.DataFrame([market_data_filtered]) if not market_data_filtered.empty else market_data
            
            trends = {}
            
            # Overall market trend
            overall_trend = self._calculate_trend(market_data, 'market_rate')
            trends['overall'] = {
                'trend_slope': overall_trend['slope'],
                'trend_direction': 'upward' if overall_trend['slope'] > 0 else 'downward' if overall_trend['slope'] < 0 else 'stable',
                'trend_strength': overall_trend['r_squared'],
                'current_rate': market_data['market_rate'].iloc[-1] if len(market_data) > 0 else 0,
                'average_rate': market_data['market_rate'].mean()
            }
            
            # Trends by service type
            for service_type in market_data['service_type'].unique():
                service_data_filtered = market_data[market_data['service_type'] == service_type]
                if isinstance(service_data_filtered, pd.DataFrame):
                    service_data = service_data_filtered
                else:
                    # If filtering returns a Series, convert back to DataFrame
                    service_data = pd.DataFrame([service_data_filtered]) if not service_data_filtered.empty else pd.DataFrame()
                
                if len(service_data) > 10:  # Need sufficient data points
                    service_trend = self._calculate_trend(service_data, 'market_rate')
                    current_rate_val = service_data['market_rate'].iloc[-1] if len(service_data) > 0 else 0
                    avg_rate_val = service_data['market_rate'].mean() if len(service_data) > 0 else 0
                    trends[service_type] = {
                        'trend_slope': service_trend['slope'],
                        'trend_direction': 'upward' if service_trend['slope'] > 0 else 'downward' if service_trend['slope'] < 0 else 'stable',
                        'trend_strength': service_trend['r_squared'],
                        'current_rate': float(current_rate_val),
                        'average_rate': float(avg_rate_val)
                    }
            
            logger.info(f"Analyzed market trends for {len(trends)} service types")
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing market trends: {e}")
            return {}
    
    def _calculate_trend(self, data: pd.DataFrame, column: str) -> Dict[str, float]:
        """
        Calculate trend using linear regression
        
        Args:
            data: DataFrame with time series data
            column: Column name to calculate trend for
            
        Returns:
            Dictionary with trend metrics
        """
        try:
            if len(data) < 2:
                return {'slope': 0.0, 'r_squared': 0.0}
            
            # Convert dates to numeric values for regression
            data = data.sort_values('date')
            x = np.arange(len(data)).astype(float)
            y = data[column].values.astype(float)
            
            # Calculate linear regression
            slope, intercept = np.polyfit(x, y, 1)
            
            # Calculate R-squared
            y_pred = slope * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            return {
                'slope': float(slope),
                'r_squared': float(r_squared)
            }
            
        except Exception as e:
            logger.error(f"Error calculating trend: {e}")
            return {'slope': 0.0, 'r_squared': 0.0}
    
    def detect_seasonality(self, market_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect seasonal patterns in market data
        
        Args:
            market_data: DataFrame with market rate data
            
        Returns:
            Dictionary with seasonality analysis
        """
        try:
            if market_data.empty or len(market_data) < 30:
                logger.warning("Insufficient data for seasonality detection")
                return {'seasonal_patterns': 'insufficient_data'}
            
            # Group by month to detect seasonal patterns
            market_data['month'] = market_data['date'].dt.month
            monthly_avg = market_data.groupby('month')['market_rate'].mean()
            
            # Convert to list for easier handling
            monthly_values = list(monthly_avg.values)
            monthly_indices = list(monthly_avg.index)
            
            # Find peak and trough months
            if monthly_values:
                peak_index = monthly_values.index(max(monthly_values))
                trough_index = monthly_values.index(min(monthly_values))
                peak_month = int(monthly_indices[peak_index])
                trough_month = int(monthly_indices[trough_index])
            else:
                peak_month = 1
                trough_month = 1
            
            # Calculate seasonal amplitude
            amplitude = monthly_avg.max() - monthly_avg.min()
            avg_rate = monthly_avg.mean()
            seasonal_strength = amplitude / avg_rate if avg_rate > 0 else 0
            
            seasonality = {
                'peak_month': int(peak_month),
                'trough_month': int(trough_month),
                'seasonal_amplitude': float(amplitude),
                'seasonal_strength': float(seasonal_strength),
                'monthly_averages': monthly_avg.to_dict()
            }
            
            logger.info(f"Detected seasonality with strength {seasonal_strength:.2f}")
            return seasonality
            
        except Exception as e:
            logger.error(f"Error detecting seasonality: {e}")
            return {'seasonal_patterns': 'error'}


class CompetitiveIntelligenceAnalyzer:
    """Analyzer for competitive intelligence and positioning"""
    
    def __init__(self):
        """Initialize competitive intelligence analyzer"""
        logger.info("Competitive Intelligence Analyzer initialized")
    
    def analyze_competitive_landscape(self, competitor_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze competitive landscape and positioning
        
        Args:
            competitor_data: DataFrame with competitor pricing data
            
        Returns:
            Dictionary with competitive analysis results
        """
        try:
            if competitor_data.empty:
                logger.warning("No competitor data available")
                return {'competitive_analysis': 'no_data'}
            
            # Overall market metrics
            total_competitors = competitor_data['competitor_name'].nunique()
            avg_market_price = competitor_data['avg_price'].mean()
            price_range = competitor_data['avg_price'].max() - competitor_data['avg_price'].min()
            
            # Market share analysis
            market_shares = competitor_data.groupby('competitor_name')['market_share'].mean()
            # Convert to dict and sort manually
            market_shares_dict = market_shares.to_dict()
            sorted_items = sorted(market_shares_dict.items(), key=lambda x: x[1], reverse=True)
            top_competitors = dict(sorted_items[:3])
            
            # Pricing strategy distribution
            strategy_counts = competitor_data['pricing_strategy'].value_counts()
            
            # Price range analysis
            price_ranges = {
                'min_price': float(competitor_data['price_range_min'].min()),
                'max_price': float(competitor_data['price_range_max'].max()),
                'avg_min_price': float(competitor_data['price_range_min'].mean()),
                'avg_max_price': float(competitor_data['price_range_max'].mean())
            }
            
            competitive_analysis = {
                'total_competitors': int(total_competitors),
                'average_market_price': float(avg_market_price),
                'price_range': float(price_range),
                'top_competitors': top_competitors,
                'pricing_strategies': strategy_counts.to_dict(),
                'price_ranges': price_ranges,
                'data_points': len(competitor_data)
            }
            
            logger.info(f"Analyzed competitive landscape with {total_competitors} competitors")
            return competitive_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing competitive landscape: {e}")
            return {'competitive_analysis': 'error'}
    
    def benchmark_against_competitors(self, our_pricing: Dict[str, Any], 
                                   competitor_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Benchmark our pricing against competitors
        
        Args:
            our_pricing: Dictionary with our pricing recommendations
            competitor_data: DataFrame with competitor pricing data
            
        Returns:
            Dictionary with benchmarking results
        """
        try:
            if competitor_data.empty or not our_pricing:
                logger.warning("Insufficient data for benchmarking")
                return {'benchmarking': 'insufficient_data'}
            
            # Calculate our average price
            our_prices = [rec['recommended_price'] for rec in our_pricing.values()]
            our_avg_price = np.mean(our_prices) if our_prices else 100
            
            # Competitor metrics
            competitor_avg_price = competitor_data['avg_price'].mean()
            competitor_min_price = competitor_data['avg_price'].min()
            competitor_max_price = competitor_data['avg_price'].max()
            
            # Positioning analysis
            price_difference = our_avg_price - competitor_avg_price
            price_difference_pct = (price_difference / competitor_avg_price) * 100 if competitor_avg_price > 0 else 0
            
            # Percentile ranking
            all_prices = list(competitor_data['avg_price']) + [our_avg_price]
            all_prices.sort()
            our_position = all_prices.index(our_avg_price) + 1
            percentile_rank = (our_position / len(all_prices)) * 100
            
            # Competitive positioning
            if price_difference_pct < -10:
                positioning = 'highly_competitive'
            elif price_difference_pct < -5:
                positioning = 'competitive'
            elif price_difference_pct < 5:
                positioning = 'market_aligned'
            elif price_difference_pct < 10:
                positioning = 'premium'
            else:
                positioning = 'highly_premium'
            
            benchmarking = {
                'our_average_price': float(our_avg_price),
                'competitor_average_price': float(competitor_avg_price),
                'competitor_price_range': {
                    'min': float(competitor_min_price),
                    'max': float(competitor_max_price)
                },
                'price_difference': float(price_difference),
                'price_difference_percentage': float(price_difference_pct),
                'percentile_rank': float(percentile_rank),
                'competitive_positioning': positioning,
                'recommendation': self._generate_benchmarking_recommendation(positioning, float(price_difference_pct))
            }
            
            logger.info(f"Benchmarked against competitors: {positioning} positioning")
            return benchmarking
            
        except Exception as e:
            logger.error(f"Error benchmarking against competitors: {e}")
            return {'benchmarking': 'error'}
    
    def _generate_benchmarking_recommendation(self, positioning: str, 
                                           price_difference_pct: float) -> str:
        """
        Generate recommendation based on benchmarking results
        
        Args:
            positioning: Competitive positioning
            price_difference_pct: Price difference percentage
            
        Returns:
            Recommendation string
        """
        if positioning == 'highly_competitive':
            return "Significantly underpriced - consider increasing prices to improve margins"
        elif positioning == 'competitive':
            return "Competitively priced - maintain current strategy with minor adjustments"
        elif positioning == 'market_aligned':
            return "Market-aligned pricing - focus on value differentiation"
        elif positioning == 'premium':
            return "Premium pricing - ensure value proposition justifies higher prices"
        else:
            return "Highly premium priced - monitor client retention and market share"


class DemandForecastAnalyzer:
    """Analyzer for demand forecasting and prediction"""
    
    def __init__(self):
        """Initialize demand forecast analyzer"""
        logger.info("Demand Forecast Analyzer initialized")
    
    def forecast_demand(self, pricing_history: pd.DataFrame, 
                       forecast_horizon_days: int = 30) -> Dict[str, Any]:
        """
        Forecast demand based on historical pricing and sales data
        
        Args:
            pricing_history: DataFrame with historical pricing and sales data
            forecast_horizon_days: Number of days to forecast
            
        Returns:
            Dictionary with demand forecast
        """
        try:
            if pricing_history.empty or len(pricing_history) < 30:
                logger.warning("Insufficient data for demand forecasting")
                return {'demand_forecast': 'insufficient_data'}
            
            # Sort data by date
            pricing_history = pricing_history.sort_values('date')
            
            # Calculate demand metrics
            avg_units_sold = float(pricing_history['units_sold'].mean())
            avg_acceptance_rate = float(pricing_history['client_acceptance_rate'].mean())
            
            # Trend analysis
            units_sold_trend = self._calculate_simple_trend(np.array(pricing_history['units_sold'].values))
            acceptance_rate_trend = self._calculate_simple_trend(np.array(pricing_history['client_acceptance_rate'].values))
            
            # Seasonal patterns (if available)
            pricing_history['day_of_week'] = pricing_history['date'].dt.dayofweek
            daily_patterns = pricing_history.groupby('day_of_week')['units_sold'].mean().to_dict()
            
            # Forecast future demand
            forecasted_units = self._forecast_simple(avg_units_sold, units_sold_trend, forecast_horizon_days)
            forecasted_acceptance = self._forecast_simple(avg_acceptance_rate, acceptance_rate_trend, forecast_horizon_days)
            
            demand_forecast = {
                'current_avg_units_sold': float(avg_units_sold),
                'current_avg_acceptance_rate': float(avg_acceptance_rate),
                'units_sold_trend': float(units_sold_trend),
                'acceptance_rate_trend': float(acceptance_rate_trend),
                'daily_patterns': daily_patterns,
                'forecast_horizon_days': forecast_horizon_days,
                'forecasted_units_sold': float(forecasted_units),
                'forecasted_acceptance_rate': float(forecasted_acceptance),
                'confidence_interval': self._calculate_confidence_interval(pricing_history)
            }
            
            logger.info(f"Generated demand forecast for {forecast_horizon_days} days")
            return demand_forecast
            
        except Exception as e:
            logger.error(f"Error forecasting demand: {e}")
            return {'demand_forecast': 'error'}
    
    def _calculate_simple_trend(self, values: np.ndarray) -> float:
        """
        Calculate simple trend using linear regression
        
        Args:
            values: Array of values
            
        Returns:
            Trend slope
        """
        try:
            if len(values) < 2:
                return 0.0
            
            x = np.arange(len(values))
            slope, _ = np.polyfit(x, values, 1)
            return float(slope)
        except Exception:
            return 0.0
    
    def _forecast_simple(self, current_value: float, trend: float, 
                        horizon: int) -> float:
        """
        Simple linear forecast
        
        Args:
            current_value: Current value
            trend: Trend slope
            horizon: Forecast horizon
            
        Returns:
            Forecasted value
        """
        return current_value + (trend * horizon)
    
    def _calculate_confidence_interval(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate confidence interval for forecast
        
        Args:
            data: DataFrame with historical data
            
        Returns:
            Dictionary with confidence interval bounds
        """
        try:
            units_std = data['units_sold'].std()
            acceptance_std = data['client_acceptance_rate'].std()
            
            return {
                'units_sold_lower_bound': float(data['units_sold'].mean() - (1.96 * units_std)),
                'units_sold_upper_bound': float(data['units_sold'].mean() + (1.96 * units_std)),
                'acceptance_rate_lower_bound': float(data['client_acceptance_rate'].mean() - (1.96 * acceptance_std)),
                'acceptance_rate_upper_bound': float(data['client_acceptance_rate'].mean() + (1.96 * acceptance_std))
            }
        except Exception:
            return {
                'units_sold_lower_bound': 0.0,
                'units_sold_upper_bound': 0.0,
                'acceptance_rate_lower_bound': 0.0,
                'acceptance_rate_upper_bound': 0.0
            }


# Global instances for easy access
market_trend_analyzer_instance = None
competitive_intelligence_analyzer_instance = None
demand_forecast_analyzer_instance = None


def get_market_trend_analyzer() -> MarketTrendAnalyzer:
    """Get singleton market trend analyzer instance"""
    global market_trend_analyzer_instance
    if market_trend_analyzer_instance is None:
        market_trend_analyzer_instance = MarketTrendAnalyzer()
    return market_trend_analyzer_instance


def get_competitive_intelligence_analyzer() -> CompetitiveIntelligenceAnalyzer:
    """Get singleton competitive intelligence analyzer instance"""
    global competitive_intelligence_analyzer_instance
    if competitive_intelligence_analyzer_instance is None:
        competitive_intelligence_analyzer_instance = CompetitiveIntelligenceAnalyzer()
    return competitive_intelligence_analyzer_instance


def get_demand_forecast_analyzer() -> DemandForecastAnalyzer:
    """Get singleton demand forecast analyzer instance"""
    global demand_forecast_analyzer_instance
    if demand_forecast_analyzer_instance is None:
        demand_forecast_analyzer_instance = DemandForecastAnalyzer()
    return demand_forecast_analyzer_instance