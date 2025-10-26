"""
Client Profitability Genome Package
Contains modules for creating and analyzing 50-dimensional client profitability vectors
"""

# Define the genome dimension structure
GENOME_DIMENSIONS = {
    # Financial Health Dimensions (0-9)
    'FinancialHealth': {
        'dimensions': list(range(0, 10)),
        'features': [
            'RevenueStability', 'ProfitMarginTrend', 'BillingEfficiency', 
            'PaymentBehavior', 'CostOptimization', 'FinancialGrowth',
            'ContractValueStability', 'RevenueDiversification', 
            'FinancialPredictability', 'CashFlowHealth'
        ]
    },
    
    # Operational Efficiency Dimensions (10-19)
    'OperationalEfficiency': {
        'dimensions': list(range(10, 20)),
        'features': [
            'SLACompliance', 'ResolutionTime', 'TechnicianProductivity',
            'ServiceQuality', 'ResourceUtilization', 'OperationalCostEfficiency',
            'ServiceConsistency', 'AutomationAdoption', 'ProcessOptimization',
            'OperationalScalability'
        ]
    },
    
    # Engagement Level Dimensions (20-29)
    'EngagementLevel': {
        'dimensions': list(range(20, 30)),
        'features': [
            'LoginFrequency', 'FeatureUsageDepth', 'SupportInteraction',
            'CommunicationResponsiveness', 'FeedbackParticipation', 'TrainingAdoption',
            'PortalEngagement', 'CommunityParticipation', 'AdvocacyIndicators',
            'RelationshipStrength'
        ]
    },
    
    # Growth Potential Dimensions (30-39)
    'GrowthPotential': {
        'dimensions': list(range(30, 40)),
        'features': [
            'ExpansionOpportunity', 'UpsellReadiness', 'MarketPosition',
            'InnovationAdoption', 'PartnershipPotential', 'CrossSellingOpportunities',
            'RevenueGrowthTrajectory', 'ServiceUtilizationTrends', 'MarketExpansion',
            'StrategicAlignment'
        ]
    },
    
    # Risk Factors Dimensions (40-49)
    'RiskFactors': {
        'dimensions': list(range(40, 50)),
        'features': [
            'ChurnProbability', 'PaymentDelinquencyRisk', 'ContractExpirationRisk',
            'ServiceQualityRisk', 'CompetitiveThreat', 'MarketVolatilityExposure',
            'DependencyRisk', 'ComplianceRisk', 'OperationalRisk',
            'FinancialStabilityRisk'
        ]
    }
}

# Define the complete 50-dimensional genome structure
GENOME_STRUCTURE = {}
for category, info in GENOME_DIMENSIONS.items():
    for i, feature in enumerate(info['features']):
        dimension_index = info['dimensions'][i]
        GENOME_STRUCTURE[dimension_index] = {
            'category': category,
            'feature': feature,
            'description': f"{category} - {feature}"
        }

__all__ = ['GENOME_DIMENSIONS', 'GENOME_STRUCTURE']