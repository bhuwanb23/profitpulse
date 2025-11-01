"""
Alert System for Revenue Leak Detection
Handles alert generation and tracking for detected revenue leaks
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
import json
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class AlertGenerator:
    """Generate alerts for detected revenue leaks"""
    
    def __init__(self):
        """Initialize alert generator"""
        self.alerts = []
        self.alert_rules = {
            'critical': {'threshold': 10000, 'frequency': 'immediate'},
            'high': {'threshold': 5000, 'frequency': 'hourly'},
            'medium': {'threshold': 1000, 'frequency': 'daily'},
            'low': {'threshold': 100, 'frequency': 'weekly'}
        }
        logger.info("Alert Generator initialized")
    
    def generate_alerts(self, classified_leaks: pd.DataFrame, 
                       recovery_estimates: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Generate alerts for classified revenue leaks
        
        Args:
            classified_leaks: DataFrame with classified leaks
            recovery_estimates: DataFrame with recovery estimates
            
        Returns:
            List of alert dictionaries
        """
        try:
            if classified_leaks.empty:
                logger.info("No classified leaks to generate alerts for")
                return []
            
            alerts = []
            
            for _, leak in classified_leaks.iterrows():
                alert = self._generate_leak_alert(leak, recovery_estimates)
                if alert:
                    alerts.append(alert)
                    self.alerts.append(alert)
            
            logger.info(f"Generated {len(alerts)} alerts for revenue leaks")
            return alerts
            
        except Exception as e:
            logger.error(f"Error generating alerts: {e}")
            return []
    
    def _generate_leak_alert(self, leak: pd.Series, 
                           recovery_estimates: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Generate alert for a single leak"""
        try:
            leak_id = leak.get('leak_id', '')
            client_id = leak.get('client_id', 'UNKNOWN')
            leak_type = leak.get('leak_type', 'unclassified')
            severity = leak.get('severity', 'medium')
            potential_loss = float(leak.get('potential_loss', 0) or 0)
            
            # Get recovery estimate for this leak
            estimate_row = recovery_estimates[recovery_estimates['leak_id'] == leak_id]
            if not estimate_row.empty and len(estimate_row) > 0:
                try:
                    # Safely extract recovery estimate
                    try:
                        if hasattr(estimate_row['adjusted_estimate'], 'iloc'):
                            recovery_estimate = float(list(estimate_row['adjusted_estimate'])[0] if hasattr(estimate_row['adjusted_estimate'], '__len__') and len(estimate_row['adjusted_estimate']) > 0 else potential_loss)
                        else:
                            recovery_estimate = float(list(estimate_row['adjusted_estimate'])[0] if hasattr(estimate_row['adjusted_estimate'], '__len__') and len(estimate_row['adjusted_estimate']) > 0 else potential_loss)
                    except:
                        recovery_estimate = potential_loss
                except:
                    recovery_estimate = potential_loss
            else:
                recovery_estimate = potential_loss
            
            # Determine alert level based on severity and potential loss
            alert_level = self._determine_alert_level(str(severity), potential_loss)
            
            # Check if alert should be generated based on rules
            if not self._should_generate_alert(alert_level, potential_loss):
                return None
            
            # Generate alert message
            alert_message = self._generate_alert_message(
                str(client_id), str(leak_type), potential_loss, recovery_estimate, str(severity)
            )
            
            # Determine alert channels
            alert_channels = self._determine_alert_channels(alert_level, str(client_id))
            
            alert = {
                'alert_id': f"ALERT-{len(self.alerts) + 1:04d}",
                'leak_id': leak_id,
                'client_id': client_id,
                'alert_level': alert_level,
                'alert_message': alert_message,
                'alert_channels': alert_channels,
                'potential_loss': potential_loss,
                'recovery_estimate': recovery_estimate,
                'leak_type': leak_type,
                'severity': severity,
                'timestamp': datetime.now(),
                'status': 'new',
                'assigned_to': self._determine_alert_owner(alert_level, str(leak_type)),
                'escalation_level': 1
            }
            
            return alert
            
        except Exception as e:
            logger.error(f"Error generating leak alert: {e}")
            return None
    
    def _determine_alert_level(self, severity: str, potential_loss: float) -> str:
        """Determine alert level based on severity and potential loss"""
        try:
            # Map severity to alert level
            severity_levels = {
                'critical': 'critical',
                'high': 'high',
                'medium': 'medium',
                'low': 'low'
            }
            
            base_level = severity_levels.get(severity.lower(), 'medium')
            
            # Adjust based on potential loss
            if potential_loss > 50000:
                return 'critical'
            elif potential_loss > 10000:
                return 'high'
            elif potential_loss > 1000:
                return 'medium'
            else:
                return base_level
                
        except Exception as e:
            logger.warning(f"Error determining alert level: {e}")
            return 'medium'
    
    def _should_generate_alert(self, alert_level: str, potential_loss: float) -> bool:
        """Determine if an alert should be generated based on rules"""
        try:
            rule = self.alert_rules.get(alert_level, {'threshold': 1000})
            threshold = rule.get('threshold', 1000)
            
            # Always generate alerts for critical and high severity
            if alert_level in ['critical', 'high']:
                return True
            
            # For medium and low, check against threshold
            return potential_loss >= threshold
            
        except Exception as e:
            logger.warning(f"Error checking alert generation: {e}")
            return True
    
    def _generate_alert_message(self, client_id: str, leak_type: str, 
                              potential_loss: float, recovery_estimate: float,
                              severity: str) -> str:
        """Generate alert message"""
        try:
            base_messages = {
                'unbilled_services': f"Unbilled services detected for client {client_id}. Potential loss: ${potential_loss:,.2f}",
                'underbilled_contracts': f"Underbilled contracts detected for client {client_id}. Potential loss: ${potential_loss:,.2f}",
                'overdue_invoices': f"Overdue invoices for client {client_id}. Potential loss: ${potential_loss:,.2f}",
                'unpaid_invoices': f"Unpaid invoices for client {client_id}. Potential loss: ${potential_loss:,.2f}",
                'duplicate_billing': f"Duplicate billing detected for client {client_id}. Potential recovery: ${recovery_estimate:,.2f}",
                'pricing_errors': f"Pricing errors detected for client {client_id}. Potential loss: ${potential_loss:,.2f}",
                'time_tracking_issues': f"Time tracking issues for client {client_id}. Potential loss: ${potential_loss:,.2f}",
                'service_delivery_gaps': f"Service delivery gaps for client {client_id}. Potential loss: ${potential_loss:,.2f}",
                'unclassified': f"Unclassified revenue leak for client {client_id}. Potential loss: ${potential_loss:,.2f}"
            }
            
            message = base_messages.get(leak_type, f"Revenue leak detected for client {client_id}. Potential loss: ${potential_loss:,.2f}")
            
            # Add severity indicator
            severity_indicator = severity.upper() if severity else "MEDIUM"
            return f"[{severity_indicator}] {message}"
            
        except Exception as e:
            logger.warning(f"Error generating alert message: {e}")
            return f"[MEDIUM] Revenue leak detected for client {client_id}. Potential loss: ${potential_loss:,.2f}"
    
    def _determine_alert_channels(self, alert_level: str, client_id: str) -> List[str]:
        """Determine which channels to send the alert to"""
        try:
            channels = ['email']
            
            # Add SMS for critical alerts
            if alert_level == 'critical':
                channels.append('sms')
            
            # Add dashboard notification for all alerts
            channels.append('dashboard')
            
            # Add ticketing system for high+ alerts
            if alert_level in ['critical', 'high']:
                channels.append('ticketing')
            
            return channels
            
        except Exception as e:
            logger.warning(f"Error determining alert channels: {e}")
            return ['email', 'dashboard']
    
    def _determine_alert_owner(self, alert_level: str, leak_type: str) -> str:
        """Determine who should own the alert"""
        try:
            # Map leak types to owners
            owners = {
                'unbilled_services': 'Billing Team',
                'underbilled_contracts': 'Account Management',
                'overdue_invoices': 'Collections Team',
                'unpaid_invoices': 'Collections Manager',
                'duplicate_billing': 'Billing Team',
                'pricing_errors': 'Account Management',
                'time_tracking_issues': 'Operations Team',
                'service_delivery_gaps': 'Service Delivery Team',
                'unclassified': 'Revenue Assurance Team'
            }
            
            owner = owners.get(leak_type, 'Revenue Assurance Team')
            
            # Escalate critical alerts
            if alert_level == 'critical':
                owner = 'Finance Director'
            elif alert_level == 'high':
                owner = 'Revenue Manager'
            
            return owner
            
        except Exception as e:
            logger.warning(f"Error determining alert owner: {e}")
            return 'Revenue Assurance Team'
    
    def get_alerts_by_client(self, client_id: str) -> List[Dict[str, Any]]:
        """Get all alerts for a specific client"""
        try:
            client_alerts = [alert for alert in self.alerts if alert.get('client_id') == client_id]
            return client_alerts
        except Exception as e:
            logger.error(f"Error getting alerts for client {client_id}: {e}")
            return []
    
    def get_alerts_by_level(self, alert_level: str) -> List[Dict[str, Any]]:
        """Get all alerts of a specific level"""
        try:
            level_alerts = [alert for alert in self.alerts if alert.get('alert_level') == alert_level]
            return level_alerts
        except Exception as e:
            logger.error(f"Error getting alerts for level {alert_level}: {e}")
            return []
    
    def update_alert_status(self, alert_id: str, status: str, 
                          assigned_to: Optional[str] = None) -> bool:
        """Update the status of an alert"""
        try:
            for alert in self.alerts:
                if alert.get('alert_id') == alert_id:
                    alert['status'] = status
                    if assigned_to:
                        alert['assigned_to'] = assigned_to
                    logger.info(f"Updated alert {alert_id} status to {status}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error updating alert {alert_id} status: {e}")
            return False


class RecoveryTracker:
    """Track recovery progress for detected revenue leaks"""
    
    def __init__(self):
        """Initialize recovery tracker"""
        self.recovery_records = []
        logger.info("Recovery Tracker initialized")
    
    def record_recovery_action(self, leak_id: str, client_id: str, 
                             action_taken: str, amount_recovered: float = 0.0,
                             action_owner: str = "Unknown") -> str:
        """
        Record a recovery action taken for a leak
        
        Args:
            leak_id: ID of the leak
            client_id: ID of the client
            action_taken: Description of action taken
            amount_recovered: Amount recovered (if any)
            action_owner: Who took the action
            
        Returns:
            Recovery record ID
        """
        try:
            record_id = f"REC-{len(self.recovery_records) + 1:04d}"
            
            record = {
                'record_id': record_id,
                'leak_id': leak_id,
                'client_id': client_id,
                'action_taken': action_taken,
                'amount_recovered': amount_recovered,
                'action_owner': action_owner,
                'timestamp': datetime.now(),
                'status': 'completed'
            }
            
            self.recovery_records.append(record)
            logger.info(f"Recorded recovery action {record_id} for leak {leak_id}")
            
            return record_id
            
        except Exception as e:
            logger.error(f"Error recording recovery action: {e}")
            return ""
    
    def get_recovery_summary(self, client_id: Optional[str] = None) -> Dict[str, Any]:
        """Get recovery summary statistics"""
        try:
            records = self.recovery_records
            if client_id:
                records = [record for record in records if record.get('client_id') == client_id]
            
            if not records:
                return {
                    'total_actions': 0,
                    'total_amount_recovered': 0.0,
                    'average_recovery_per_action': 0.0,
                    'recovery_rate': 0.0
                }
            
            total_actions = len(records)
            total_recovered = sum(record.get('amount_recovered', 0.0) for record in records)
            average_recovery = total_recovered / total_actions if total_actions > 0 else 0.0
            
            summary = {
                'total_actions': total_actions,
                'total_amount_recovered': total_recovered,
                'average_recovery_per_action': average_recovery,
                'recovery_rate': average_recovery,  # Simplified recovery rate
                'records': records[-10:]  # Last 10 records
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting recovery summary: {e}")
            return {
                'total_actions': 0,
                'total_amount_recovered': 0.0,
                'average_recovery_per_action': 0.0,
                'recovery_rate': 0.0
            }
    
    def get_recovery_by_leak(self, leak_id: str) -> List[Dict[str, Any]]:
        """Get all recovery actions for a specific leak"""
        try:
            leak_records = [record for record in self.recovery_records if record.get('leak_id') == leak_id]
            return leak_records
        except Exception as e:
            logger.error(f"Error getting recovery records for leak {leak_id}: {e}")
            return []
    
    def generate_recovery_report(self, period_days: int = 30) -> Dict[str, Any]:
        """Generate a recovery report for a specific period"""
        try:
            # Filter records by date
            cutoff_date = datetime.now() - timedelta(days=period_days)
            recent_records = [
                record for record in self.recovery_records 
                if record.get('timestamp', datetime.min) >= cutoff_date
            ]
            
            if not recent_records:
                return {
                    'period_days': period_days,
                    'total_actions': 0,
                    'total_amount_recovered': 0.0,
                    'average_recovery': 0.0,
                    'top_clients': [],
                    'top_leak_types': []
                }
            
            # Calculate statistics
            total_actions = len(recent_records)
            total_recovered = sum(record.get('amount_recovered', 0.0) for record in recent_records)
            average_recovery = total_recovered / total_actions if total_actions > 0 else 0.0
            
            # Group by client
            client_recovery = {}
            for record in recent_records:
                client_id = record.get('client_id', 'UNKNOWN')
                amount = record.get('amount_recovered', 0.0)
                if client_id in client_recovery:
                    client_recovery[client_id] += amount
                else:
                    client_recovery[client_id] = amount
            
            # Get top clients
            top_clients = sorted(client_recovery.items(), key=lambda x: x[1], reverse=True)[:5]
            
            report = {
                'period_days': period_days,
                'total_actions': total_actions,
                'total_amount_recovered': total_recovered,
                'average_recovery': average_recovery,
                'top_clients': [{'client_id': client, 'amount': amount} for client, amount in top_clients],
                'recent_records': recent_records[-20:]  # Last 20 records
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating recovery report: {e}")
            return {
                'period_days': period_days,
                'total_actions': 0,
                'total_amount_recovered': 0.0,
                'average_recovery': 0.0,
                'top_clients': [],
                'top_leak_types': []
            }


# Global instances for easy access
alert_generator_instance = None
recovery_tracker_instance = None


async def get_alert_generator() -> AlertGenerator:
    """Get singleton alert generator instance"""
    global alert_generator_instance
    if alert_generator_instance is None:
        alert_generator_instance = AlertGenerator()
    return alert_generator_instance


async def get_recovery_tracker() -> RecoveryTracker:
    """Get singleton recovery tracker instance"""
    global recovery_tracker_instance
    if recovery_tracker_instance is None:
        recovery_tracker_instance = RecoveryTracker()
    return recovery_tracker_instance