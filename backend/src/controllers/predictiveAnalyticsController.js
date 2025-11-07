const { AIAnalytics, AIRecommendation, Organization, Client, Invoice, Ticket, Service, Budget, Expense } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')
const aiClient = require('../services/ai-ml')
const ChurnMapper = require('../services/ai-ml/mappers/churnMapper')
const BudgetMapper = require('../services/ai-ml/mappers/budgetMapper')
const DemandMapper = require('../services/ai-ml/mappers/demandMapper')
const winston = require('winston')

// GET /api/ai/predictions/revenue - Revenue forecasting
const getRevenueForecasting = async (req, res) => {
  try {
    const { 
      organization_id,
      client_id,
      forecast_period = 12, // months
      confidence_level = 0.8,
      include_seasonality = true,
      include_trends = true
    } = req.query

    // Get historical revenue data
    const now = new Date()
    const startDate = new Date(now.getFullYear() - 2, now.getMonth(), now.getDate())
    
    const whereClause = {
      invoice_date: { [Op.between]: [startDate, now] },
      status: 'paid'
    }
    if (organization_id) whereClause.organization_id = organization_id
    if (client_id) whereClause.client_id = client_id

    // Get monthly revenue data
    const historicalData = await Invoice.findAll({
      where: whereClause,
      attributes: [
        [Invoice.sequelize.fn('strftime', '%Y-%m', Invoice.sequelize.col('invoice_date')), 'month'],
        [Invoice.sequelize.fn('SUM', Invoice.sequelize.col('total_amount')), 'revenue'],
        [Invoice.sequelize.fn('COUNT', Invoice.sequelize.col('id')), 'invoice_count']
      ],
      group: [Invoice.sequelize.fn('strftime', '%Y-%m', Invoice.sequelize.col('invoice_date'))],
      order: [[Invoice.sequelize.fn('strftime', '%Y-%m', Invoice.sequelize.col('invoice_date')), 'ASC']],
      raw: true
    })

    // Process historical data
    const processedData = historicalData.map(item => ({
      month: item.month,
      revenue: parseFloat(item.revenue || 0),
      invoice_count: parseInt(item.invoice_count)
    }))

    // Calculate trend analysis
    const revenues = processedData.map(item => item.revenue)
    const avgRevenue = revenues.length > 0 ? revenues.reduce((sum, rev) => sum + rev, 0) / revenues.length : 0
    
    // Simple linear regression for trend
    let trend = 0
    if (revenues.length > 1) {
      const n = revenues.length
      const sumX = (n * (n - 1)) / 2
      const sumY = revenues.reduce((sum, rev) => sum + rev, 0)
      const sumXY = revenues.reduce((sum, rev, index) => sum + (index * rev), 0)
      const sumXX = (n * (n - 1) * (2 * n - 1)) / 6
      
      trend = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX)
    }

    // Generate forecast
    const forecast = []
    const lastMonth = processedData.length > 0 ? processedData[processedData.length - 1] : null
    const baseRevenue = lastMonth ? lastMonth.revenue : avgRevenue

    for (let i = 1; i <= parseInt(forecast_period); i++) {
      const forecastDate = new Date()
      forecastDate.setMonth(forecastDate.getMonth() + i)
      const monthKey = `${forecastDate.getFullYear()}-${String(forecastDate.getMonth() + 1).padStart(2, '0')}`
      
      // Trend-based forecast
      let forecastedRevenue = Math.max(0, baseRevenue + (trend * i))
      
      // Add seasonality if enabled
      if (include_seasonality === 'true') {
        const seasonalityFactor = 1 + (0.15 * Math.sin((i * Math.PI) / 6)) // ±15% seasonal variation
        forecastedRevenue *= seasonalityFactor
      }
      
      // Add market trends if enabled
      if (include_trends === 'true') {
        const marketTrendFactor = 1 + (0.05 * Math.sin((i * Math.PI) / 12)) // ±5% market trend
        forecastedRevenue *= marketTrendFactor
      }

      const confidenceInterval = parseFloat(confidence_level)
      const margin = forecastedRevenue * (1 - confidenceInterval)

      forecast.push({
        month: monthKey,
        forecasted_revenue: Math.round(forecastedRevenue * 100) / 100,
        confidence_interval: {
          lower: Math.round((forecastedRevenue - margin) * 100) / 100,
          upper: Math.round((forecastedRevenue + margin) * 100) / 100
        },
        trend_factor: Math.round(trend * 100) / 100,
        seasonality_factor: include_seasonality === 'true' ? Math.round((1 + (0.15 * Math.sin((i * Math.PI) / 6))) * 100) / 100 : 1,
        market_trend_factor: include_trends === 'true' ? Math.round((1 + (0.05 * Math.sin((i * Math.PI) / 12))) * 100) / 100 : 1
      })
    }

    // Calculate forecast accuracy metrics
    let accuracyMetrics = null
    if (processedData.length >= 6) {
      const recentData = processedData.slice(-6)
      const avgRecentRevenue = recentData.reduce((sum, item) => sum + item.revenue, 0) / recentData.length
      const variance = recentData.reduce((sum, item) => sum + Math.pow(item.revenue - avgRecentRevenue, 2), 0) / recentData.length
      const standardDeviation = Math.sqrt(variance)
      
      accuracyMetrics = {
        historical_avg: Math.round(avgRecentRevenue * 100) / 100,
        standard_deviation: Math.round(standardDeviation * 100) / 100,
        coefficient_of_variation: Math.round((standardDeviation / avgRecentRevenue) * 100) / 100,
        confidence_level: parseFloat(confidence_level) * 100,
        forecast_accuracy: Math.round((1 - (standardDeviation / avgRecentRevenue)) * 100) / 100
      }
    }

    res.json({
      success: true,
      data: {
        forecast_period: parseInt(forecast_period),
        confidence_level: parseFloat(confidence_level),
        historical_data: processedData,
        forecast: forecast,
        trend_analysis: {
          trend: Math.round(trend * 100) / 100,
          trend_direction: trend > 0 ? 'increasing' : trend < 0 ? 'decreasing' : 'stable',
          base_revenue: Math.round(baseRevenue * 100) / 100
        },
        accuracy_metrics: accuracyMetrics,
        total_forecasted_revenue: Math.round(forecast.reduce((sum, item) => sum + item.forecasted_revenue, 0) * 100) / 100
      }
    })
  } catch (error) {
    console.error('Get revenue forecasting error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching revenue forecasting'
    })
  }
}

// GET /api/ai/predictions/churn - Client churn prediction
const getChurnPrediction = async (req, res) => {
  try {
    const { 
      organization_id,
      prediction_horizon = 90, // days
      risk_threshold = 0.7,
      include_factors = true
    } = req.query

    // Get client data for churn analysis
    const whereClause = {}
    if (organization_id) whereClause.organization_id = organization_id

    const clients = await Client.findAll({
      where: whereClause,
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name']
        },
        {
          model: Invoice,
          as: 'invoices',
          attributes: ['id', 'total_amount', 'status', 'invoice_date', 'due_date'],
          required: false
        },
        {
          model: Ticket,
          as: 'tickets',
          attributes: ['id', 'status', 'priority', 'created_at', 'resolved_at'],
          required: false
        },
        {
          model: Service,
          as: 'services',
          attributes: ['id', 'name', 'status', 'created_at'],
          required: false
        }
      ]
    })

    // Analyze churn risk for each client using AI/ML
    const churnPredictions = []
    
    for (const client of clients) {
      const invoices = client.invoices || []
      const tickets = client.tickets || []
      const services = client.services || []

      try {
        // Prepare client data for AI/ML analysis
        const clientData = prepareChurnClientData(client, invoices, tickets, services)
        
        // Validate data quality
        const validation = ChurnMapper.validateBackendData(clientData)
        if (!validation.isValid) {
          winston.warn('Client churn data validation failed, using fallback analysis', {
            clientId: client.id,
            errors: validation.errors
          })
          
          // Fall back to original analysis
          const fallbackResult = performFallbackChurnAnalysis(client, invoices, tickets, services, riskFactors, churnRiskScore)
          churnPredictions.push(fallbackResult)
          continue
        }

        // Try AI/ML service prediction
        let aiPredictionResult = null
        try {
          // Map to AI/ML format
          const aimlRequest = ChurnMapper.mapBackendToAIML(clientData, {
            predictionHorizon: prediction_horizon,
            includeConfidence: true,
            includeRiskFactors: include_factors === 'true',
            includeRetentionStrategies: true
          })

          // Call AI/ML service with fallback enabled
          const aimlResponse = await aiClient.predictChurn(aimlRequest, {
            useCircuitBreaker: true,
            useFallback: true,
            cacheKey: ChurnMapper.createCacheKey(clientData),
            cacheTTL: 300000 // 5 minutes
          })

          // Validate AI/ML response
          const responseValidation = ChurnMapper.validateAIMLResponse(aimlResponse)
          if (responseValidation.isValid) {
            // Map AI/ML response to backend format
            aiPredictionResult = ChurnMapper.mapAIMLToBackend(aimlResponse)
            
            winston.info('AI/ML churn prediction successful', {
              clientId: client.id,
              churnProbability: aiPredictionResult.churnPrediction.churnProbability,
              riskLevel: aiPredictionResult.churnPrediction.riskLevel,
              confidence: aiPredictionResult.churnPrediction.confidence,
              isFallback: aiPredictionResult.metadata.isFallback
            })
          } else {
            winston.warn('AI/ML churn response validation failed, using fallback', {
              clientId: client.id,
              errors: responseValidation.errors
            })
          }

        } catch (aiError) {
          winston.error('AI/ML churn prediction failed, using fallback', {
            clientId: client.id,
            error: aiError.message
          })
        }

        // Use AI prediction if available, otherwise fall back to original analysis
        if (aiPredictionResult && !aiPredictionResult.metadata.isFallback) {
          // Convert AI prediction to expected format
          const churnResult = convertAIChurnPrediction(aiPredictionResult, client)
          churnPredictions.push(churnResult)
        } else {
          // Fall back to original analysis
          const fallbackResult = performFallbackChurnAnalysis(client, invoices, tickets, services)
          churnPredictions.push(fallbackResult)
        }

      } catch (error) {
        winston.error('Error in churn analysis, using basic fallback', {
          clientId: client.id,
          error: error.message
        })
        
        // Basic fallback
        const basicResult = performFallbackChurnAnalysis(client, invoices, tickets, services)
        churnPredictions.push(basicResult)
      }
    }

    // Helper function to prepare client data for AI analysis
    function prepareChurnClientData(client, invoices, tickets, services) {
      const overdueInvoices = invoices.filter(inv => 
        inv.status !== 'paid' && new Date(inv.due_date) < new Date()
      )
      const recentTickets = tickets.filter(ticket => 
        new Date(ticket.created_at) > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
      )
      const unresolvedTickets = tickets.filter(ticket => 
        !['resolved', 'closed'].includes(ticket.status)
      )

      return {
        id: client.id,
        engagementScore: Math.max(0, 1 - (recentTickets.length / 10)),
        communicationFrequency: Math.max(0, 1 - (unresolvedTickets.length / 5)),
        ticketCount: tickets.length,
        responseTimeSatisfaction: 0.8, // Default
        featureAdoptionRate: services.length > 0 ? services.filter(s => s.status === 'active').length / services.length : 0.5,
        loginFrequency: 0.6, // Default
        paymentHistory: overdueInvoices.length === 0 ? 'good' : overdueInvoices.length < 3 ? 'fair' : 'poor',
        paymentDelays: overdueInvoices.length,
        contractValue: invoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount || 0), 0),
        priceSensitivity: 0.5, // Default
        billingDisputes: 0, // Default
        revenueTrend: 'stable', // Default
        serviceUtilization: services.length > 0 ? services.filter(s => s.status === 'active').length / services.length : 0.7,
        downtimeIncidents: 0, // Default
        slaCompliance: 0.95, // Default
        resolutionSatisfaction: 0.8, // Default
        escalationRate: unresolvedTickets.length / Math.max(tickets.length, 1),
        serviceAdoption: services.length > 0 ? services.filter(s => s.status === 'active').length / services.length : 0.7,
        relationshipDuration: client.created_at ? 
          Math.floor((Date.now() - new Date(client.created_at)) / (1000 * 60 * 60 * 24 * 30)) : 12,
        keyContactStability: 0.8, // Default
        stakeholderSatisfaction: 0.8, // Default
        renewalHistory: [], // Default
        expansionOpportunities: 0.5, // Default
        competitivePressure: 0.3 // Default
      }
    }

    // Helper function to convert AI prediction to expected format
    function convertAIChurnPrediction(aiResult, client) {
      return {
        client_id: client.id,
        client_name: client.name,
        client_company: client.company,
        organization_name: client.organization ? client.organization.name : 'Unknown',
        churn_probability: aiResult.churnPrediction.churnProbability,
        risk_level: aiResult.churnPrediction.riskLevel,
        confidence_score: aiResult.churnPrediction.confidence,
        time_to_churn: aiResult.churnPrediction.timeToChurn,
        risk_factors: aiResult.riskFactors,
        retention_strategies: aiResult.retentionStrategies,
        early_warning_indicators: aiResult.earlyWarningIndicators,
        interventions: aiResult.interventions,
        ai_powered: true
      }
    }

    // Helper function for fallback churn analysis
    function performFallbackChurnAnalysis(client, invoices, tickets, services) {
      const riskFactors = []
      let churnRiskScore = 0

      // 1. Payment behavior analysis
      const overdueInvoices = invoices.filter(inv => 
        inv.status !== 'paid' && new Date(inv.due_date) < new Date()
      )
      if (overdueInvoices.length > 0) {
        const paymentRisk = Math.min(overdueInvoices.length * 0.2, 0.8)
        churnRiskScore += paymentRisk
        riskFactors.push({
          factor: 'payment_delays',
          impact: paymentRisk,
          description: `${overdueInvoices.length} overdue invoices`,
          severity: paymentRisk > 0.5 ? 'high' : 'medium'
        })
      }

      // 2. Support ticket analysis
      const recentTickets = tickets.filter(ticket => 
        new Date(ticket.created_at) > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
      )
      const unresolvedTickets = tickets.filter(ticket => 
        !['resolved', 'closed'].includes(ticket.status)
      )
      
      if (recentTickets.length > 5) {
        const supportRisk = Math.min(recentTickets.length * 0.1, 0.6)
        churnRiskScore += supportRisk
        riskFactors.push({
          factor: 'high_support_volume',
          impact: supportRisk,
          description: `${recentTickets.length} tickets in last 30 days`,
          severity: supportRisk > 0.4 ? 'high' : 'medium'
        })
      }

      if (unresolvedTickets.length > 3) {
        const unresolvedRisk = Math.min(unresolvedTickets.length * 0.15, 0.7)
        churnRiskScore += unresolvedRisk
        riskFactors.push({
          factor: 'unresolved_issues',
          impact: unresolvedRisk,
          description: `${unresolvedTickets.length} unresolved tickets`,
          severity: unresolvedRisk > 0.5 ? 'high' : 'medium'
        })
      }

      // 3. Service utilization analysis
      const activeServices = services.filter(service => service.status === 'active')
      if (activeServices.length === 0) {
        churnRiskScore += 0.9
        riskFactors.push({
          factor: 'no_active_services',
          impact: 0.9,
          description: 'No active services',
          severity: 'critical'
        })
      }

      // 4. Revenue trend analysis
      const recentInvoices = invoices.filter(inv => 
        new Date(inv.invoice_date) > new Date(Date.now() - 90 * 24 * 60 * 60 * 1000)
      )
      if (recentInvoices.length > 0) {
        const recentRevenue = recentInvoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount), 0)
        const olderInvoices = invoices.filter(inv => 
          new Date(inv.invoice_date) > new Date(Date.now() - 180 * 24 * 60 * 60 * 1000) &&
          new Date(inv.invoice_date) <= new Date(Date.now() - 90 * 24 * 60 * 60 * 1000)
        )
        
        if (olderInvoices.length > 0) {
          const olderRevenue = olderInvoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount), 0)
          const revenueChange = (recentRevenue - olderRevenue) / olderRevenue
          
          if (revenueChange < -0.3) {
            const revenueRisk = Math.min(Math.abs(revenueChange), 0.8)
            churnRiskScore += revenueRisk
            riskFactors.push({
              factor: 'declining_revenue',
              impact: revenueRisk,
              description: `${Math.round(revenueChange * 100)}% revenue decline`,
              severity: revenueRisk > 0.5 ? 'high' : 'medium'
            })
          }
        }
      }

      // 5. Contract and engagement analysis
      const clientAge = client.createdAt ? 
        (Date.now() - new Date(client.created_at).getTime()) / (1000 * 60 * 60 * 24 * 365) : 0
      
      if (clientAge < 1) {
        churnRiskScore += 0.3
        riskFactors.push({
          factor: 'new_client',
          impact: 0.3,
          description: 'Client less than 1 year old',
          severity: 'medium'
        })
      }

      // Normalize churn risk score
      churnRiskScore = Math.min(churnRiskScore, 1.0)

      // Determine churn risk level
      let riskLevel = 'low'
      if (churnRiskScore >= 0.8) riskLevel = 'critical'
      else if (churnRiskScore >= 0.6) riskLevel = 'high'
      else if (churnRiskScore >= 0.4) riskLevel = 'medium'
      else if (churnRiskScore >= 0.2) riskLevel = 'low'

      // Generate recommendations
      const recommendations = []
      if (churnRiskScore > 0.6) {
        recommendations.push('Immediate client outreach and relationship review')
        recommendations.push('Address outstanding issues and improve service delivery')
        recommendations.push('Consider retention incentives or contract renegotiation')
      } else if (churnRiskScore > 0.4) {
        recommendations.push('Proactive client communication and satisfaction survey')
        recommendations.push('Monitor service usage and address any concerns')
      } else {
        recommendations.push('Maintain regular communication and service quality')
      }

      churnPredictions.push({
        client_id: client.id,
        client_name: client.name,
        client_company: client.company,
        organization_name: client.organization ? client.organization.name : 'Unknown',
        churn_risk_score: Math.round(churnRiskScore * 100) / 100,
        risk_level: riskLevel,
        prediction_horizon_days: parseInt(prediction_horizon),
        risk_factors: include_factors === 'true' ? riskFactors : [],
        recommendations: recommendations,
        client_metrics: {
          total_invoices: invoices.length,
          overdue_invoices: overdueInvoices.length,
          active_services: activeServices.length,
          recent_tickets: recentTickets.length,
          unresolved_tickets: unresolvedTickets.length,
          client_age_years: Math.round(clientAge * 100) / 100
        }
      })
    }

    // Sort by churn risk score
    churnPredictions.sort((a, b) => b.churn_risk_score - a.churn_risk_score)

    // Calculate summary statistics
    const totalClients = churnPredictions.length
    const highRiskClients = churnPredictions.filter(client => client.churn_risk_score >= parseFloat(risk_threshold)).length
    const avgChurnRisk = totalClients > 0 ? 
      churnPredictions.reduce((sum, client) => sum + client.churn_risk_score, 0) / totalClients : 0

    // Group by risk level
    const riskDistribution = {
      critical: churnPredictions.filter(client => client.risk_level === 'critical').length,
      high: churnPredictions.filter(client => client.risk_level === 'high').length,
      medium: churnPredictions.filter(client => client.risk_level === 'medium').length,
      low: churnPredictions.filter(client => client.risk_level === 'low').length
    }

    res.json({
      success: true,
      data: {
        prediction_horizon_days: parseInt(prediction_horizon),
        risk_threshold: parseFloat(risk_threshold),
        summary: {
          total_clients: totalClients,
          high_risk_clients: highRiskClients,
          avg_churn_risk: Math.round(avgChurnRisk * 100) / 100,
          risk_distribution: riskDistribution
        },
        churn_predictions: churnPredictions
      }
    })
  } catch (error) {
    console.error('Get churn prediction error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching churn prediction'
    })
  }
}

// GET /api/ai/predictions/demand - Service demand forecasting
const getDemandForecasting = async (req, res) => {
  try {
    const { 
      organization_id,
      service_id,
      forecast_period = 6, // months
      include_seasonality = true,
      include_growth_trends = true
    } = req.query

    // Get historical service demand data
    const now = new Date()
    const startDate = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate())
    
    const whereClause = {
      createdAt: { [Op.between]: [startDate, now] }
    }
    if (organization_id) whereClause.organization_id = organization_id
    if (service_id) whereClause.id = service_id

    // Get service data
    const services = await Service.findAll({
      where: whereClause,
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'company'],
          required: false
        }
      ]
    })

    // Analyze demand patterns for each service
    const demandForecasts = []
    
    for (const service of services) {
      // Simulate demand data for demonstration
      const now = new Date()
      const demandData = []
      
      // Generate simulated monthly demand data
      for (let i = 11; i >= 0; i--) {
        const monthStart = new Date(now.getFullYear(), now.getMonth() - i, 1)
        const monthKey = `${monthStart.getFullYear()}-${String(monthStart.getMonth() + 1).padStart(2, '0')}`
        const baseDemand = Math.floor(Math.random() * 20) + 5 // 5-25 demand per month
        demandData.push({ month: monthKey, demand: baseDemand })
      }

      // Calculate demand trend
      const demands = demandData.map(item => item.demand)
      const avgDemand = demands.length > 0 ? demands.reduce((sum, d) => sum + d, 0) / demands.length : 0
      
      let trend = 0
      if (demands.length > 1) {
        const n = demands.length
        const sumX = (n * (n - 1)) / 2
        const sumY = demands.reduce((sum, d) => sum + d, 0)
        const sumXY = demands.reduce((sum, d, index) => sum + (index * d), 0)
        const sumXX = (n * (n - 1) * (2 * n - 1)) / 6
        
        trend = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX)
      }

      // Generate demand forecast
      const forecast = []
      const lastDemand = demands.length > 0 ? demands[demands.length - 1] : avgDemand
      
      for (let i = 1; i <= parseInt(forecast_period); i++) {
        const forecastDate = new Date()
        forecastDate.setMonth(forecastDate.getMonth() + i)
        const monthKey = `${forecastDate.getFullYear()}-${String(forecastDate.getMonth() + 1).padStart(2, '0')}`
        
        // Base forecast with trend
        let forecastedDemand = Math.max(0, lastDemand + (trend * i))
        
        // Add seasonality if enabled
        if (include_seasonality === 'true') {
          const seasonalityFactor = 1 + (0.2 * Math.sin((i * Math.PI) / 6)) // ±20% seasonal variation
          forecastedDemand *= seasonalityFactor
        }
        
        // Add growth trends if enabled
        if (include_growth_trends === 'true') {
          const growthFactor = 1 + (0.1 * Math.sin((i * Math.PI) / 12)) // ±10% growth trend
          forecastedDemand *= growthFactor
        }

        forecast.push({
          month: monthKey,
          forecasted_demand: Math.round(forecastedDemand),
          trend_factor: Math.round(trend * 100) / 100,
          seasonality_factor: include_seasonality === 'true' ? Math.round((1 + (0.2 * Math.sin((i * Math.PI) / 6))) * 100) / 100 : 1,
          growth_factor: include_growth_trends === 'true' ? Math.round((1 + (0.1 * Math.sin((i * Math.PI) / 12))) * 100) / 100 : 1
        })
      }

      // Calculate demand metrics
      const peakDemand = Math.max(...demands, 0)
      const minDemand = Math.min(...demands, 0)
      const demandVolatility = demands.length > 1 ? 
        Math.sqrt(demands.reduce((sum, d) => sum + Math.pow(d - avgDemand, 2), 0) / demands.length) : 0

      demandForecasts.push({
        service_id: service.id,
        service_name: service.name,
        organization_name: service.organization ? service.organization.name : 'Unknown',
        client_name: service.client ? service.client.name : 'General',
        historical_demand: demandData,
        forecast: forecast,
        demand_metrics: {
          avg_monthly_demand: Math.round(avgDemand * 100) / 100,
          peak_demand: peakDemand,
          min_demand: minDemand,
          demand_volatility: Math.round(demandVolatility * 100) / 100,
          trend: Math.round(trend * 100) / 100,
          trend_direction: trend > 0 ? 'increasing' : trend < 0 ? 'decreasing' : 'stable'
        },
        total_forecasted_demand: Math.round(forecast.reduce((sum, item) => sum + item.forecasted_demand, 0))
      })
    }

    // Calculate overall summary
    const totalServices = demandForecasts.length
    const avgForecastedDemand = totalServices > 0 ? 
      demandForecasts.reduce((sum, service) => sum + service.total_forecasted_demand, 0) / totalServices : 0

    res.json({
      success: true,
      data: {
        forecast_period_months: parseInt(forecast_period),
        include_seasonality: include_seasonality === 'true',
        include_growth_trends: include_growth_trends === 'true',
        summary: {
          total_services: totalServices,
          avg_forecasted_demand: Math.round(avgForecastedDemand),
          total_forecasted_demand: Math.round(demandForecasts.reduce((sum, service) => sum + service.total_forecasted_demand, 0))
        },
        demand_forecasts: demandForecasts
      }
    })
  } catch (error) {
    console.error('Get demand forecasting error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching demand forecasting'
    })
  }
}

// GET /api/ai/predictions/budget - Budget optimization
const getBudgetOptimization = async (req, res) => {
  try {
    const { 
      organization_id,
      budget_id,
      optimization_horizon = 12, // months
      include_scenarios = true,
      risk_tolerance = 0.1
    } = req.query

    // Get budget data
    const whereClause = {}
    if (organization_id) whereClause.organization_id = organization_id
    if (budget_id) whereClause.id = budget_id

    const budgets = await Budget.findAll({
      where: whereClause,
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name']
        },
        {
          model: Expense,
          as: 'expenses',
          attributes: ['id', 'amount', 'category', 'expense_date'],
          required: false
        }
      ]
    })

    // Analyze budget optimization opportunities
    const budgetOptimizations = []
    
    for (const budget of budgets) {
      const expenses = budget.expenses || []
      
      // Analyze expense patterns
      const categoryAnalysis = {}
      expenses.forEach(expense => {
        const category = expense.category || 'Uncategorized'
        if (!categoryAnalysis[category]) {
          categoryAnalysis[category] = {
            total_amount: 0,
            count: 0,
            avg_amount: 0
          }
        }
        categoryAnalysis[category].total_amount += parseFloat(expense.amount)
        categoryAnalysis[category].count += 1
      })

      // Calculate averages
      Object.keys(categoryAnalysis).forEach(category => {
        const data = categoryAnalysis[category]
        data.avg_amount = data.count > 0 ? data.total_amount / data.count : 0
      })

      // Generate optimization scenarios
      const scenarios = []
      
      if (include_scenarios === 'true') {
        // Conservative scenario
        scenarios.push({
          name: 'Conservative',
          description: 'Minimal changes with focus on efficiency',
          budget_adjustment: -0.05, // 5% reduction
          risk_level: 'low',
          expected_savings: parseFloat(budget.total_amount) * 0.05,
          recommendations: [
            'Optimize existing processes',
            'Negotiate better vendor rates',
            'Implement cost controls'
          ]
        })

        // Moderate scenario
        scenarios.push({
          name: 'Moderate',
          description: 'Balanced approach with strategic cuts',
          budget_adjustment: -0.15, // 15% reduction
          risk_level: 'medium',
          expected_savings: parseFloat(budget.total_amount) * 0.15,
          recommendations: [
            'Reallocate budget categories',
            'Implement automation',
            'Review service levels'
          ]
        })

        // Aggressive scenario
        scenarios.push({
          name: 'Aggressive',
          description: 'Significant optimization with higher risk',
          budget_adjustment: -0.25, // 25% reduction
          risk_level: 'high',
          expected_savings: parseFloat(budget.total_amount) * 0.25,
          recommendations: [
            'Major process restructuring',
            'Technology investments',
            'Strategic partnerships'
          ]
        })
      }

      // Calculate optimization metrics
      const totalSpent = expenses.reduce((sum, expense) => sum + parseFloat(expense.amount), 0)
      const utilizationRate = parseFloat(budget.total_amount) > 0 ? 
        totalSpent / parseFloat(budget.total_amount) : 0
      
      const optimizationPotential = Math.max(0, utilizationRate - 0.8) * parseFloat(budget.total_amount)
      const efficiencyScore = utilizationRate > 0.9 ? 0.6 : utilizationRate > 0.7 ? 0.8 : 1.0

      budgetOptimizations.push({
        budget_id: budget.id,
        budget_name: budget.name,
        organization_name: budget.organization ? budget.organization.name : 'Unknown',
        current_status: {
          total_budget: parseFloat(budget.total_amount),
          total_spent: Math.round(totalSpent * 100) / 100,
          remaining_budget: Math.round((parseFloat(budget.total_amount) - totalSpent) * 100) / 100,
          utilization_rate: Math.round(utilizationRate * 100) / 100
        },
        category_analysis: Object.keys(categoryAnalysis).map(category => ({
          category,
          ...categoryAnalysis[category],
          total_amount: Math.round(categoryAnalysis[category].total_amount * 100) / 100,
          avg_amount: Math.round(categoryAnalysis[category].avg_amount * 100) / 100
        })),
        optimization_metrics: {
          optimization_potential: Math.round(optimizationPotential * 100) / 100,
          efficiency_score: Math.round(efficiencyScore * 100) / 100,
          risk_tolerance: parseFloat(risk_tolerance)
        },
        scenarios: scenarios,
        recommendations: [
          'Implement monthly budget reviews',
          'Set up automated alerts for overspending',
          'Regular vendor contract reviews',
          'Consider zero-based budgeting approach'
        ]
      })
    }

    // Calculate overall summary
    const totalBudgets = budgetOptimizations.length
    const totalOptimizationPotential = budgetOptimizations.reduce((sum, budget) => 
      sum + budget.optimization_metrics.optimization_potential, 0)
    const avgEfficiencyScore = totalBudgets > 0 ? 
      budgetOptimizations.reduce((sum, budget) => sum + budget.optimization_metrics.efficiency_score, 0) / totalBudgets : 0

    res.json({
      success: true,
      data: {
        optimization_horizon_months: parseInt(optimization_horizon),
        risk_tolerance: parseFloat(risk_tolerance),
        summary: {
          total_budgets: totalBudgets,
          total_optimization_potential: Math.round(totalOptimizationPotential * 100) / 100,
          avg_efficiency_score: Math.round(avgEfficiencyScore * 100) / 100
        },
        budget_optimizations: budgetOptimizations
      }
    })
  } catch (error) {
    console.error('Get budget optimization error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching budget optimization'
    })
  }
}

// GET /api/ai/predictions/market - Market trend analysis
const getMarketTrendAnalysis = async (req, res) => {
  try {
    const { 
      organization_id,
      analysis_period = 12, // months
      include_competitors = true,
      include_industry_trends = true
    } = req.query

    // Get organization data
    const whereClause = {}
    if (organization_id) whereClause.id = organization_id

    const organizations = await Organization.findAll({
      where: whereClause,
      include: [
        {
          model: Client,
          as: 'clients',
          attributes: ['id', 'name', 'company', 'created_at'],
          required: false
        },
        {
          model: Service,
          as: 'services',
          attributes: ['id', 'name', 'status', 'created_at'],
          required: false
        },
        {
          model: Invoice,
          as: 'invoices',
          attributes: ['id', 'total_amount', 'invoice_date', 'status'],
          required: false
        }
      ]
    })

    // Analyze market trends for each organization
    const marketTrends = []
    
    for (const organization of organizations) {
      const clients = organization.clients || []
      const services = organization.services || []
      const invoices = organization.invoices || []

      // Client growth analysis
      const clientGrowthData = []
      const now = new Date()
      for (let i = 11; i >= 0; i--) {
        const monthStart = new Date(now.getFullYear(), now.getMonth() - i, 1)
        const monthEnd = new Date(now.getFullYear(), now.getMonth() - i + 1, 0)
        
        const clientsInMonth = clients.filter(client => 
          new Date(client.created_at) >= monthStart && 
          new Date(client.created_at) <= monthEnd
        ).length
        
        clientGrowthData.push({
          month: `${monthStart.getFullYear()}-${String(monthStart.getMonth() + 1).padStart(2, '0')}`,
          new_clients: clientsInMonth
        })
      }

      // Service adoption analysis
      const serviceAdoptionData = []
      for (let i = 11; i >= 0; i--) {
        const monthStart = new Date(now.getFullYear(), now.getMonth() - i, 1)
        const monthEnd = new Date(now.getFullYear(), now.getMonth() - i + 1, 0)
        
        const servicesInMonth = services.filter(service => 
          new Date(service.created_at) >= monthStart && 
          new Date(service.created_at) <= monthEnd
        ).length
        
        serviceAdoptionData.push({
          month: `${monthStart.getFullYear()}-${String(monthStart.getMonth() + 1).padStart(2, '0')}`,
          new_services: servicesInMonth
        })
      }

      // Revenue trend analysis
      const revenueData = []
      for (let i = 11; i >= 0; i--) {
        const monthStart = new Date(now.getFullYear(), now.getMonth() - i, 1)
        const monthEnd = new Date(now.getFullYear(), now.getMonth() - i + 1, 0)
        
        const monthlyInvoices = invoices.filter(invoice => 
          new Date(invoice.invoice_date) >= monthStart && 
          new Date(invoice.invoice_date) <= monthEnd &&
          invoice.status === 'paid'
        )
        
        const monthlyRevenue = monthlyInvoices.reduce((sum, invoice) => 
          sum + parseFloat(invoice.total_amount), 0)
        
        revenueData.push({
          month: `${monthStart.getFullYear()}-${String(monthStart.getMonth() + 1).padStart(2, '0')}`,
          revenue: Math.round(monthlyRevenue * 100) / 100,
          invoice_count: monthlyInvoices.length
        })
      }

      // Calculate growth rates
      const clientGrowthRate = clientGrowthData.length > 1 ? 
        ((clientGrowthData[clientGrowthData.length - 1].new_clients - clientGrowthData[0].new_clients) / 
         Math.max(clientGrowthData[0].new_clients, 1)) * 100 : 0

      const revenueGrowthRate = revenueData.length > 1 ? 
        ((revenueData[revenueData.length - 1].revenue - revenueData[0].revenue) / 
         Math.max(revenueData[0].revenue, 1)) * 100 : 0

      // Market position analysis
      const marketPosition = {
        client_count: clients.length,
        service_count: services.length,
        total_revenue: Math.round(invoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount), 0) * 100) / 100,
        avg_revenue_per_client: clients.length > 0 ? 
          Math.round((invoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount), 0) / clients.length) * 100) / 100 : 0
      }

      // Industry trends (simulated)
      const industryTrends = include_industry_trends === 'true' ? [
        {
          trend: 'Cloud Migration',
          impact: 'high',
          description: 'Increasing demand for cloud-based services',
          opportunity_score: 0.8
        },
        {
          trend: 'Cybersecurity',
          impact: 'critical',
          description: 'Growing cybersecurity concerns driving service demand',
          opportunity_score: 0.9
        },
        {
          trend: 'Remote Work Support',
          impact: 'medium',
          description: 'Sustained remote work infrastructure needs',
          opportunity_score: 0.6
        },
        {
          trend: 'AI Integration',
          impact: 'high',
          description: 'AI-powered service delivery becoming standard',
          opportunity_score: 0.7
        }
      ] : []

      // Competitor analysis (simulated)
      const competitorAnalysis = include_competitors === 'true' ? {
        market_share: Math.random() * 0.3 + 0.1, // 10-40%
        competitive_position: Math.random() > 0.5 ? 'strong' : 'moderate',
        pricing_competitiveness: Math.random() * 0.4 + 0.6, // 60-100%
        service_differentiation: Math.random() * 0.3 + 0.7, // 70-100%
        recommendations: [
          'Focus on service quality differentiation',
          'Implement competitive pricing strategies',
          'Invest in customer relationship management',
          'Develop unique service offerings'
        ]
      } : null

      marketTrends.push({
        organization_id: organization.id,
        organization_name: organization.name,
        analysis_period_months: parseInt(analysis_period),
        client_growth: {
          data: clientGrowthData,
          growth_rate: Math.round(clientGrowthRate * 100) / 100,
          trend: clientGrowthRate > 10 ? 'growing' : clientGrowthRate < -10 ? 'declining' : 'stable'
        },
        service_adoption: {
          data: serviceAdoptionData,
          adoption_rate: Math.round(serviceAdoptionData.reduce((sum, item) => sum + item.new_services, 0) / 12 * 100) / 100
        },
        revenue_trends: {
          data: revenueData,
          growth_rate: Math.round(revenueGrowthRate * 100) / 100,
          trend: revenueGrowthRate > 15 ? 'growing' : revenueGrowthRate < -15 ? 'declining' : 'stable'
        },
        market_position: marketPosition,
        industry_trends: industryTrends,
        competitor_analysis: competitorAnalysis,
        market_insights: [
          'Client acquisition rate is ' + (clientGrowthRate > 0 ? 'positive' : 'negative'),
          'Revenue growth is ' + (revenueGrowthRate > 0 ? 'positive' : 'negative'),
          'Market position is ' + (marketPosition.avg_revenue_per_client > 10000 ? 'strong' : 'moderate'),
          'Service adoption is ' + (serviceAdoptionData.reduce((sum, item) => sum + item.new_services, 0) > 5 ? 'healthy' : 'low')
        ]
      })
    }

    // Calculate overall market summary
    const totalOrganizations = marketTrends.length
    const avgClientGrowth = totalOrganizations > 0 ? 
      marketTrends.reduce((sum, org) => sum + org.client_growth.growth_rate, 0) / totalOrganizations : 0
    const avgRevenueGrowth = totalOrganizations > 0 ? 
      marketTrends.reduce((sum, org) => sum + org.revenue_trends.growth_rate, 0) / totalOrganizations : 0

    res.json({
      success: true,
      data: {
        analysis_period_months: parseInt(analysis_period),
        include_competitors: include_competitors === 'true',
        include_industry_trends: include_industry_trends === 'true',
        summary: {
          total_organizations: totalOrganizations,
          avg_client_growth_rate: Math.round(avgClientGrowth * 100) / 100,
          avg_revenue_growth_rate: Math.round(avgRevenueGrowth * 100) / 100
        },
        market_trends: marketTrends
      }
    })
  } catch (error) {
    console.error('Get market trend analysis error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching market trend analysis'
    })
  }
}

// GET /api/ai/predictions/growth - Growth opportunities
const getGrowthOpportunities = async (req, res) => {
  try {
    const { 
      organization_id,
      opportunity_type,
      min_impact_score = 0.5,
      include_implementation_plan = true
    } = req.query

    // Get organization data
    const whereClause = {}
    if (organization_id) whereClause.id = organization_id

    const organizations = await Organization.findAll({
      where: whereClause,
      include: [
        {
          model: Client,
          as: 'clients',
          attributes: ['id', 'name', 'company', 'created_at'],
          required: false
        },
        {
          model: Service,
          as: 'services',
          attributes: ['id', 'name', 'status', 'created_at'],
          required: false
        },
        {
          model: Invoice,
          as: 'invoices',
          attributes: ['id', 'total_amount', 'invoice_date', 'status'],
          required: false
        },
        {
          model: Ticket,
          as: 'tickets',
          attributes: ['id', 'status', 'priority', 'created_at'],
          required: false
        }
      ]
    })

    // Analyze growth opportunities for each organization
    const growthOpportunities = []
    
    for (const organization of organizations) {
      const clients = organization.clients || []
      const services = organization.services || []
      const invoices = organization.invoices || []
      const tickets = organization.tickets || []

      // Calculate current metrics
      const currentMetrics = {
        total_clients: clients.length,
        total_services: services.length,
        total_revenue: Math.round(invoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount), 0) * 100) / 100,
        avg_revenue_per_client: clients.length > 0 ? 
          Math.round((invoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount), 0) / clients.length) * 100) / 100 : 0,
        service_utilization: services.length > 0 ? 
          Math.round((tickets.length / services.length) * 100) / 100 : 0
      }

      // Identify growth opportunities
      const opportunities = []

      // 1. Client Expansion Opportunities
      if (currentMetrics.total_clients > 0) {
        const clientExpansionScore = Math.min(currentMetrics.avg_revenue_per_client / 10000, 1.0)
        if (clientExpansionScore >= parseFloat(min_impact_score)) {
          opportunities.push({
            type: 'client_expansion',
            title: 'Expand Client Base',
            description: 'Opportunity to acquire new clients based on current performance',
            impact_score: clientExpansionScore,
            potential_revenue_increase: currentMetrics.total_revenue * 0.3,
            implementation_effort: 'medium',
            timeline_months: 6,
            success_probability: 0.7,
            key_metrics: {
              target_new_clients: Math.round(currentMetrics.total_clients * 0.3),
              expected_revenue_per_client: currentMetrics.avg_revenue_per_client,
              total_potential_revenue: currentMetrics.total_revenue * 0.3
            }
          })
        }
      }

      // 2. Service Diversification Opportunities
      if (currentMetrics.total_services > 0) {
        const serviceDiversificationScore = Math.min(currentMetrics.service_utilization / 10, 1.0)
        if (serviceDiversificationScore >= parseFloat(min_impact_score)) {
          opportunities.push({
            type: 'service_diversification',
            title: 'Diversify Service Portfolio',
            description: 'Add new services to existing client base',
            impact_score: serviceDiversificationScore,
            potential_revenue_increase: currentMetrics.total_revenue * 0.25,
            implementation_effort: 'high',
            timeline_months: 9,
            success_probability: 0.6,
            key_metrics: {
              target_new_services: Math.round(currentMetrics.total_services * 0.4),
              expected_revenue_per_service: currentMetrics.total_revenue / currentMetrics.total_services,
              total_potential_revenue: currentMetrics.total_revenue * 0.25
            }
          })
        }
      }

      // 3. Revenue Optimization Opportunities
      const revenueOptimizationScore = Math.min(currentMetrics.avg_revenue_per_client / 15000, 1.0)
      if (revenueOptimizationScore >= parseFloat(min_impact_score)) {
        opportunities.push({
          type: 'revenue_optimization',
          title: 'Optimize Revenue Streams',
          description: 'Increase revenue from existing clients through upselling and optimization',
          impact_score: revenueOptimizationScore,
          potential_revenue_increase: currentMetrics.total_revenue * 0.2,
          implementation_effort: 'low',
          timeline_months: 3,
          success_probability: 0.8,
          key_metrics: {
            target_revenue_increase: currentMetrics.total_revenue * 0.2,
            expected_client_retention: 0.9,
            total_potential_revenue: currentMetrics.total_revenue * 0.2
          }
        })
      }

      // 4. Market Penetration Opportunities
      const marketPenetrationScore = Math.min(currentMetrics.total_clients / 50, 1.0)
      if (marketPenetrationScore >= parseFloat(min_impact_score)) {
        opportunities.push({
          type: 'market_penetration',
          title: 'Market Penetration',
          description: 'Expand market presence in current geographic area',
          impact_score: marketPenetrationScore,
          potential_revenue_increase: currentMetrics.total_revenue * 0.4,
          implementation_effort: 'high',
          timeline_months: 12,
          success_probability: 0.5,
          key_metrics: {
            target_market_share: 0.15,
            expected_client_acquisition: Math.round(currentMetrics.total_clients * 0.5),
            total_potential_revenue: currentMetrics.total_revenue * 0.4
          }
        })
      }

      // 5. Technology Innovation Opportunities
      const technologyInnovationScore = 0.8 // High opportunity for technology innovation
      if (technologyInnovationScore >= parseFloat(min_impact_score)) {
        opportunities.push({
          type: 'technology_innovation',
          title: 'Technology Innovation',
          description: 'Implement cutting-edge technologies to differentiate services',
          impact_score: technologyInnovationScore,
          potential_revenue_increase: currentMetrics.total_revenue * 0.35,
          implementation_effort: 'high',
          timeline_months: 18,
          success_probability: 0.6,
          key_metrics: {
            target_technology_adoption: 0.8,
            expected_efficiency_gains: 0.3,
            total_potential_revenue: currentMetrics.total_revenue * 0.35
          }
        })
      }

      // Filter by opportunity type if specified
      const filteredOpportunities = opportunity_type ? 
        opportunities.filter(opp => opp.type === opportunity_type) : 
        opportunities

      // Add implementation plans if requested
      if (include_implementation_plan === 'true') {
        filteredOpportunities.forEach(opportunity => {
          opportunity.implementation_plan = generateImplementationPlan(opportunity)
        })
      }

      // Sort by impact score
      filteredOpportunities.sort((a, b) => b.impact_score - a.impact_score)

      growthOpportunities.push({
        organization_id: organization.id,
        organization_name: organization.name,
        current_metrics: currentMetrics,
        opportunities: filteredOpportunities,
        summary: {
          total_opportunities: filteredOpportunities.length,
          high_impact_opportunities: filteredOpportunities.filter(opp => opp.impact_score >= 0.8).length,
          total_potential_revenue: Math.round(filteredOpportunities.reduce((sum, opp) => sum + opp.potential_revenue_increase, 0) * 100) / 100,
          avg_impact_score: filteredOpportunities.length > 0 ? 
            Math.round(filteredOpportunities.reduce((sum, opp) => sum + opp.impact_score, 0) / filteredOpportunities.length * 100) / 100 : 0
        }
      })
    }

    // Calculate overall summary
    const totalOrganizations = growthOpportunities.length
    const totalOpportunities = growthOpportunities.reduce((sum, org) => sum + org.summary.total_opportunities, 0)
    const totalPotentialRevenue = growthOpportunities.reduce((sum, org) => sum + org.summary.total_potential_revenue, 0)

    res.json({
      success: true,
      data: {
        min_impact_score: parseFloat(min_impact_score),
        include_implementation_plan: include_implementation_plan === 'true',
        summary: {
          total_organizations: totalOrganizations,
          total_opportunities: totalOpportunities,
          total_potential_revenue: Math.round(totalPotentialRevenue * 100) / 100,
          avg_opportunities_per_organization: totalOrganizations > 0 ? 
            Math.round(totalOpportunities / totalOrganizations * 100) / 100 : 0
        },
        growth_opportunities: growthOpportunities
      }
    })
  } catch (error) {
    console.error('Get growth opportunities error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching growth opportunities'
    })
  }
}

// Helper function to generate implementation plan
const generateImplementationPlan = (opportunity) => {
  const plans = {
    client_expansion: [
      { phase: 'Phase 1', duration: '2 months', tasks: ['Market research', 'Lead generation setup', 'Sales team training'] },
      { phase: 'Phase 2', duration: '2 months', tasks: ['Outreach campaigns', 'Client meetings', 'Proposal development'] },
      { phase: 'Phase 3', duration: '2 months', tasks: ['Contract negotiations', 'Onboarding process', 'Service delivery'] }
    ],
    service_diversification: [
      { phase: 'Phase 1', duration: '3 months', tasks: ['Service gap analysis', 'Market research', 'Resource planning'] },
      { phase: 'Phase 2', duration: '3 months', tasks: ['Service development', 'Testing', 'Training'] },
      { phase: 'Phase 3', duration: '3 months', tasks: ['Launch', 'Client communication', 'Performance monitoring'] }
    ],
    revenue_optimization: [
      { phase: 'Phase 1', duration: '1 month', tasks: ['Client analysis', 'Upselling opportunities', 'Pricing review'] },
      { phase: 'Phase 2', duration: '1 month', tasks: ['Client outreach', 'Proposal development', 'Negotiations'] },
      { phase: 'Phase 3', duration: '1 month', tasks: ['Implementation', 'Monitoring', 'Optimization'] }
    ],
    market_penetration: [
      { phase: 'Phase 1', duration: '4 months', tasks: ['Market analysis', 'Competitive research', 'Strategy development'] },
      { phase: 'Phase 2', duration: '4 months', tasks: ['Marketing campaigns', 'Sales expansion', 'Partnership development'] },
      { phase: 'Phase 3', duration: '4 months', tasks: ['Market entry', 'Client acquisition', 'Performance optimization'] }
    ],
    technology_innovation: [
      { phase: 'Phase 1', duration: '6 months', tasks: ['Technology assessment', 'Vendor selection', 'Pilot planning'] },
      { phase: 'Phase 2', duration: '6 months', tasks: ['Pilot implementation', 'Testing', 'Training'] },
      { phase: 'Phase 3', duration: '6 months', tasks: ['Full deployment', 'Optimization', 'Scaling'] }
    ]
  }

  return plans[opportunity.type] || [
    { phase: 'Phase 1', duration: '3 months', tasks: ['Planning', 'Preparation', 'Initial implementation'] },
    { phase: 'Phase 2', duration: '3 months', tasks: ['Execution', 'Monitoring', 'Adjustments'] },
    { phase: 'Phase 3', duration: '3 months', tasks: ['Completion', 'Evaluation', 'Optimization'] }
  ]
}

module.exports = {
  getRevenueForecasting,
  getChurnPrediction,
  getDemandForecasting,
  getBudgetOptimization,
  getMarketTrendAnalysis,
  getGrowthOpportunities
}
