const winston = require('winston');

/**
 * Revenue Leak Detection Data Mapper
 * Maps data between backend format and AI/ML service format for revenue leak detection
 */
class RevenueLeakMapper {
  /**
   * Map backend data to AI/ML service request format
   * @param {Object} data - Combined data from backend
   * @param {Object} options - Additional options
   * @returns {Object} - AI/ML service request format
   */
  static mapBackendToAIML(data, options = {}) {
    try {
      // Extract billing data
      const billingData = {
        invoices: (data.invoices || []).map(invoice => ({
          invoice_id: invoice.id,
          amount: parseFloat(invoice.total_amount) || 0,
          status: invoice.status,
          issue_date: invoice.invoice_date,
          due_date: invoice.due_date,
          paid_date: invoice.paid_date,
          client_id: invoice.client_id,
          services: invoice.services || []
        })),
        payment_patterns: data.paymentPatterns || {},
        billing_cycles: data.billingCycles || [],
        pricing_models: data.pricingModels || []
      };

      // Extract service delivery data
      const serviceDeliveryData = {
        services: (data.services || []).map(service => ({
          service_id: service.id,
          name: service.name,
          type: service.type,
          status: service.status,
          start_date: service.start_date,
          end_date: service.end_date,
          billable_hours: service.billable_hours || 0,
          actual_hours: service.actual_hours || 0,
          hourly_rate: service.hourly_rate || 0,
          client_id: service.client_id
        })),
        time_tracking: data.timeTracking || [],
        resource_utilization: data.resourceUtilization || {},
        project_margins: data.projectMargins || []
      };

      // Extract contract data
      const contractData = {
        contracts: (data.contracts || []).map(contract => ({
          contract_id: contract.id,
          client_id: contract.client_id,
          value: contract.value,
          start_date: contract.start_date,
          end_date: contract.end_date,
          terms: contract.terms || {},
          sla_requirements: contract.sla_requirements || {},
          pricing_structure: contract.pricing_structure || {}
        })),
        amendments: data.contractAmendments || [],
        renewals: data.contractRenewals || []
      };

      // Extract operational data
      const operationalData = {
        tickets: (data.tickets || []).map(ticket => ({
          ticket_id: ticket.id,
          client_id: ticket.client_id,
          priority: ticket.priority,
          status: ticket.status,
          created_date: ticket.created_at,
          resolved_date: ticket.resolved_at,
          hours_spent: ticket.hours_spent || 0,
          billable: ticket.billable !== false
        })),
        resource_costs: data.resourceCosts || {},
        overhead_allocation: data.overheadAllocation || {},
        efficiency_metrics: data.efficiencyMetrics || {}
      };

      // Build AI/ML request
      const aimlRequest = {
        organization_id: data.organizationId,
        analysis_period: {
          start_date: options.startDate || new Date(Date.now() - 90 * 24 * 60 * 60 * 1000).toISOString(),
          end_date: options.endDate || new Date().toISOString()
        },
        billing_data: billingData,
        service_delivery_data: serviceDeliveryData,
        contract_data: contractData,
        operational_data: operationalData,
        detection_options: {
          sensitivity_level: options.sensitivityLevel || 'medium',
          minimum_leak_threshold: options.minimumLeakThreshold || 1000,
          include_recommendations: options.includeRecommendations !== false,
          include_root_causes: options.includeRootCauses !== false
        }
      };

      winston.debug('Mapped backend data to AI/ML format for revenue leak detection', {
        organizationId: data.organizationId,
        invoicesCount: billingData.invoices.length,
        servicesCount: serviceDeliveryData.services.length,
        requestSize: JSON.stringify(aimlRequest).length
      });

      return aimlRequest;

    } catch (error) {
      winston.error('Error mapping backend data to AI/ML format for revenue leak:', error);
      throw new Error(`Revenue leak data mapping failed: ${error.message}`);
    }
  }

  /**
   * Map AI/ML service response to backend format
   * @param {Object} aimlResponse - Response from AI/ML service
   * @param {Object} options - Additional options
   * @returns {Object} - Backend response format
   */
  static mapAIMLToBackend(aimlResponse, options = {}) {
    try {
      if (!aimlResponse || !aimlResponse.data) {
        throw new Error('Invalid AI/ML revenue leak response format');
      }

      const data = aimlResponse.data;

      // Map detected leaks
      const detectedLeaks = (data.leaks_detected || []).map(leak => ({
        leakId: leak.leak_id || `leak_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        category: leak.category || 'unknown',
        description: leak.description || 'Revenue leak detected',
        estimatedAmount: leak.amount || 0,
        confidence: leak.confidence || 0.7,
        severity: this.calculateLeakSeverity(leak.amount),
        source: leak.source || 'unknown',
        timeframe: leak.timeframe || 'current',
        affectedClients: leak.affected_clients || [],
        affectedServices: leak.affected_services || []
      }));

      // Map leak categories
      const leakCategories = {
        unbilledHours: data.leak_categories?.unbilled_hours || { amount: 0, count: 0 },
        underpricedServices: data.leak_categories?.underpriced_services || { amount: 0, count: 0 },
        contractGaps: data.leak_categories?.contract_gaps || { amount: 0, count: 0 },
        inefficiencies: data.leak_categories?.inefficiencies || { amount: 0, count: 0 },
        writeOffs: data.leak_categories?.write_offs || { amount: 0, count: 0 },
        scopeCreep: data.leak_categories?.scope_creep || { amount: 0, count: 0 }
      };

      // Map root cause analysis
      const rootCauseAnalysis = {
        primaryCauses: data.root_causes?.primary || [],
        secondaryCauses: data.root_causes?.secondary || [],
        systemicIssues: data.root_causes?.systemic || [],
        processGaps: data.root_causes?.process_gaps || []
      };

      // Map recommendations
      const recommendations = (data.recommendations || []).map(rec => ({
        category: rec.category || 'general',
        priority: rec.priority || 'medium',
        description: rec.description || rec,
        estimatedSavings: rec.estimated_savings || 0,
        implementationEffort: rec.implementation_effort || 'medium',
        timeframe: rec.timeframe || 'short-term',
        requiredResources: rec.required_resources || [],
        successMetrics: rec.success_metrics || []
      }));

      // Map financial impact
      const financialImpact = {
        totalLeakAmount: data.total_leak_amount || 0,
        monthlyLeakRate: data.monthly_leak_rate || 0,
        annualizedImpact: data.annualized_impact || 0,
        recoveryPotential: data.recovery_potential || 0,
        preventionSavings: data.prevention_savings || 0,
        impactByCategory: data.impact_by_category || {}
      };

      // Map trends and patterns
      const trends = {
        leakTrends: data.trends?.leak_trends || [],
        seasonalPatterns: data.trends?.seasonal_patterns || [],
        clientPatterns: data.trends?.client_patterns || [],
        servicePatterns: data.trends?.service_patterns || []
      };

      // Build backend response
      const backendResponse = {
        success: true,
        detectedLeaks: detectedLeaks,
        leakCategories: leakCategories,
        rootCauseAnalysis: rootCauseAnalysis,
        recommendations: recommendations,
        financialImpact: financialImpact,
        trends: trends,
        summary: {
          totalLeaks: detectedLeaks.length,
          totalAmount: financialImpact.totalLeakAmount,
          highSeverityLeaks: detectedLeaks.filter(leak => leak.severity === 'high').length,
          recoverableAmount: financialImpact.recoveryPotential,
          confidenceScore: data.overall_confidence || 0.8
        },
        metadata: {
          modelVersion: data.model_version || 'v1.0',
          analysisDate: data.analysis_date || new Date().toISOString(),
          analysisPeriod: data.analysis_period || {},
          processingTime: data.processing_time || 0,
          dataQuality: data.data_quality || 'good',
          isFallback: data.is_fallback || false
        }
      };

      winston.debug('Mapped AI/ML response to backend format for revenue leak detection', {
        totalLeaks: detectedLeaks.length,
        totalAmount: financialImpact.totalLeakAmount,
        recommendationsCount: recommendations.length
      });

      return backendResponse;

    } catch (error) {
      winston.error('Error mapping AI/ML revenue leak response to backend format:', error);
      throw new Error(`Revenue leak response mapping failed: ${error.message}`);
    }
  }

  /**
   * Calculate leak severity based on amount
   * @param {number} amount - Leak amount
   * @returns {string} - Severity level
   */
  static calculateLeakSeverity(amount) {
    if (amount >= 50000) return 'critical';
    if (amount >= 20000) return 'high';
    if (amount >= 5000) return 'medium';
    return 'low';
  }

  /**
   * Validate backend data before mapping
   * @param {Object} data - Data to validate
   * @returns {Object} - Validation result
   */
  static validateBackendData(data) {
    const errors = [];
    const warnings = [];

    // Required fields
    if (!data.organizationId) {
      errors.push('Organization ID is required');
    }

    // Data quality checks
    if (!data.invoices || !Array.isArray(data.invoices)) {
      warnings.push('Invoice data is missing or invalid');
    }

    if (!data.services || !Array.isArray(data.services)) {
      warnings.push('Service data is missing or invalid');
    }

    if (data.invoices && data.invoices.length === 0) {
      warnings.push('No invoice data available for analysis');
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
      dataQuality: warnings.length === 0 ? 'excellent' : 
                   warnings.length <= 2 ? 'good' : 'poor'
    };
  }

  /**
   * Validate AI/ML response before mapping
   * @param {Object} aimlResponse - AI/ML response to validate
   * @returns {Object} - Validation result
   */
  static validateAIMLResponse(aimlResponse) {
    const errors = [];

    if (!aimlResponse) {
      errors.push('AI/ML revenue leak response is null or undefined');
      return { isValid: false, errors };
    }

    if (!aimlResponse.data) {
      errors.push('AI/ML revenue leak response data is missing');
    }

    if (aimlResponse.data && typeof aimlResponse.data.total_leak_amount !== 'number') {
      errors.push('Total leak amount is missing or invalid');
    }

    if (aimlResponse.data && aimlResponse.data.total_leak_amount < 0) {
      errors.push('Total leak amount cannot be negative');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  /**
   * Create cache key for revenue leak detection
   * @param {Object} data - Data
   * @param {Object} options - Options
   * @returns {string} - Cache key
   */
  static createCacheKey(data, options = {}) {
    const orgId = data.organizationId;
    const period = options.analysisPeriod || '90d';
    const timestamp = Math.floor(Date.now() / (1000 * 60 * 60 * 12)); // 12-hour caching
    
    return `revenue_leak_${orgId}_${period}_${timestamp}`;
  }
}

module.exports = RevenueLeakMapper;
