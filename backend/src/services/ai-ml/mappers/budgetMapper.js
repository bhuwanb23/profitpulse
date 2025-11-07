const winston = require('winston');

/**
 * Budget Optimization Data Mapper
 * Maps data between backend format and AI/ML service format for budget optimization
 */
class BudgetMapper {
  static mapBackendToAIML(data, options = {}) {
    try {
      const aimlRequest = {
        organization_id: data.organizationId,
        budget_data: {
          total_budget: data.totalBudget || 0,
          current_allocation: data.currentAllocation || {},
          budget_period: data.budgetPeriod || 'annual',
          budget_constraints: data.budgetConstraints || {}
        },
        department_data: (data.departments || []).map(dept => ({
          department_id: dept.id,
          name: dept.name,
          current_budget: dept.currentBudget || 0,
          spent_amount: dept.spentAmount || 0,
          performance_metrics: dept.performanceMetrics || {},
          priority_level: dept.priorityLevel || 'medium'
        })),
        historical_data: {
          spending_patterns: data.spendingPatterns || [],
          performance_history: data.performanceHistory || [],
          roi_metrics: data.roiMetrics || {},
          variance_analysis: data.varianceAnalysis || {}
        },
        optimization_options: {
          optimization_goal: options.optimizationGoal || 'maximize_roi',
          risk_tolerance: options.riskTolerance || 'medium',
          time_horizon: options.timeHorizon || 12,
          include_scenarios: options.includeScenarios !== false
        }
      };

      return aimlRequest;
    } catch (error) {
      winston.error('Error mapping budget data:', error);
      throw new Error(`Budget data mapping failed: ${error.message}`);
    }
  }

  static mapAIMLToBackend(aimlResponse, options = {}) {
    try {
      const data = aimlResponse.data;
      
      return {
        success: true,
        optimization: {
          optimizationScore: data.optimization_score || 0,
          potentialSavings: data.potential_savings || 0,
          recommendedAllocation: data.recommended_allocation || {},
          confidence: data.confidence || 0.7
        },
        optimizations: (data.optimizations || []).map(opt => ({
          category: opt.category,
          currentSpend: opt.current_spend,
          recommendedSpend: opt.recommended_spend,
          savings: opt.savings,
          rationale: opt.rationale,
          confidence: opt.confidence
        })),
        scenarios: {
          conservative: data.scenarios?.conservative || {},
          moderate: data.scenarios?.moderate || {},
          aggressive: data.scenarios?.aggressive || {}
        },
        recommendations: data.recommendations || [],
        riskAnalysis: {
          budgetRisks: data.risk_analysis?.budget_risks || [],
          mitigationStrategies: data.risk_analysis?.mitigation_strategies || []
        },
        metadata: {
          modelVersion: data.model_version || 'v1.0',
          optimizationDate: data.optimization_date || new Date().toISOString(),
          isFallback: data.is_fallback || false
        }
      };
    } catch (error) {
      winston.error('Error mapping budget response:', error);
      throw new Error(`Budget response mapping failed: ${error.message}`);
    }
  }

  static validateBackendData(data) {
    const errors = [];
    const warnings = [];
    
    if (!data.organizationId) errors.push('Organization ID is required');
    if (!data.totalBudget || data.totalBudget <= 0) warnings.push('Total budget is missing or invalid');
    if (!data.departments || !Array.isArray(data.departments)) warnings.push('Department data is missing');
    
    return {
      isValid: errors.length === 0,
      errors,
      warnings,
      dataQuality: warnings.length === 0 ? 'excellent' : warnings.length <= 2 ? 'good' : 'poor'
    };
  }

  static validateAIMLResponse(aimlResponse) {
    const errors = [];
    
    if (!aimlResponse?.data) errors.push('AI/ML budget response data is missing');
    if (aimlResponse.data && typeof aimlResponse.data.optimization_score !== 'number') {
      errors.push('Optimization score is missing or invalid');
    }
    
    return { isValid: errors.length === 0, errors };
  }

  static createCacheKey(data, options = {}) {
    const orgId = data.organizationId;
    const period = data.budgetPeriod || 'annual';
    const timestamp = Math.floor(Date.now() / (1000 * 60 * 60 * 24)); // Daily caching
    return `budget_${orgId}_${period}_${timestamp}`;
  }
}

module.exports = BudgetMapper;
