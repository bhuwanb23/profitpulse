const { AIAnalytics, AIRecommendation, Organization, Client, Invoice, Ticket, Service, Budget, Expense } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')

// GET /api/ai/insights/profitability-genome - Profitability genome
const getProfitabilityGenome = async (req, res) => {
  try {
    const { 
      organization_id,
      client_id,
      include_dna_analysis = true,
      include_genetic_factors = true,
      include_evolution_tracking = true
    } = req.query

    // Get organization/client data
    const whereClause = {}
    if (organization_id) whereClause.organization_id = organization_id
    if (client_id) whereClause.client_id = client_id

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
          model: Service,
          as: 'services',
          attributes: ['id', 'name', 'status', 'created_at'],
          required: false
        },
        {
          model: Ticket,
          as: 'tickets',
          attributes: ['id', 'status', 'priority', 'created_at', 'resolved_at'],
          required: false
        }
      ]
    })

    // Analyze profitability genome for each client
    const profitabilityGenomes = []
    
    for (const client of clients) {
      const invoices = client.invoices || []
      const services = client.services || []
      const tickets = client.tickets || []

      // Calculate profitability DNA components
      const profitabilityDNA = {
        revenue_efficiency: 0,
        cost_optimization: 0,
        service_utilization: 0,
        payment_behavior: 0,
        growth_potential: 0,
        retention_stability: 0
      }

      // 1. Revenue Efficiency Analysis
      const paidInvoices = invoices.filter(inv => inv.status === 'paid')
      const totalRevenue = paidInvoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount), 0)
      const avgInvoiceValue = paidInvoices.length > 0 ? totalRevenue / paidInvoices.length : 0
      
      profitabilityDNA.revenue_efficiency = Math.min(avgInvoiceValue / 10000, 1.0) // Normalize to 0-1

      // 2. Cost Optimization Analysis
      const activeServices = services.filter(service => service.status === 'active')
      const serviceUtilizationRate = activeServices.length > 0 ? 
        Math.min(tickets.length / activeServices.length, 1.0) : 0
      
      profitabilityDNA.cost_optimization = serviceUtilizationRate

      // 3. Service Utilization Analysis
      const serviceAdoptionRate = services.length > 0 ? 
        Math.min(activeServices.length / services.length, 1.0) : 0
      
      profitabilityDNA.service_utilization = serviceAdoptionRate

      // 4. Payment Behavior Analysis
      const overdueInvoices = invoices.filter(inv => 
        inv.status !== 'paid' && new Date(inv.due_date) < new Date()
      )
      const paymentReliability = invoices.length > 0 ? 
        1 - (overdueInvoices.length / invoices.length) : 1
      
      profitabilityDNA.payment_behavior = Math.max(0, paymentReliability)

      // 5. Growth Potential Analysis
      const recentInvoices = invoices.filter(inv => 
        new Date(inv.invoice_date) > new Date(Date.now() - 90 * 24 * 60 * 60 * 1000)
      )
      const olderInvoices = invoices.filter(inv => 
        new Date(inv.invoice_date) > new Date(Date.now() - 180 * 24 * 60 * 60 * 1000) &&
        new Date(inv.invoice_date) <= new Date(Date.now() - 90 * 24 * 60 * 60 * 1000)
      )
      
      let growthRate = 0
      if (olderInvoices.length > 0 && recentInvoices.length > 0) {
        const recentRevenue = recentInvoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount), 0)
        const olderRevenue = olderInvoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount), 0)
        growthRate = (recentRevenue - olderRevenue) / olderRevenue
      }
      
      profitabilityDNA.growth_potential = Math.max(0, Math.min(1, (growthRate + 1) / 2))

      // 6. Retention Stability Analysis
      const clientAge = client.createdAt ? 
        (Date.now() - new Date(client.created_at).getTime()) / (1000 * 60 * 60 * 24 * 365) : 0
      const retentionStability = Math.min(clientAge / 3, 1.0) // 3 years = max stability
      
      profitabilityDNA.retention_stability = retentionStability

      // Calculate overall profitability score
      const profitabilityScore = Object.values(profitabilityDNA).reduce((sum, value) => sum + value, 0) / 6

      // Generate genetic factors analysis
      const geneticFactors = include_genetic_factors === 'true' ? {
        dominant_traits: Object.entries(profitabilityDNA)
          .sort(([,a], [,b]) => b - a)
          .slice(0, 3)
          .map(([trait, value]) => ({ trait, strength: Math.round(value * 100) / 100 })),
        recessive_traits: Object.entries(profitabilityDNA)
          .sort(([,a], [,b]) => a - b)
          .slice(0, 2)
          .map(([trait, value]) => ({ trait, weakness: Math.round(value * 100) / 100 })),
        genetic_markers: [
          { marker: 'REV_EFF', value: profitabilityDNA.revenue_efficiency, significance: 'high' },
          { marker: 'COST_OPT', value: profitabilityDNA.cost_optimization, significance: 'medium' },
          { marker: 'SERV_UTIL', value: profitabilityDNA.service_utilization, significance: 'high' },
          { marker: 'PAY_BEHAV', value: profitabilityDNA.payment_behavior, significance: 'critical' },
          { marker: 'GROWTH_POT', value: profitabilityDNA.growth_potential, significance: 'medium' },
          { marker: 'RET_STAB', value: profitabilityDNA.retention_stability, significance: 'high' }
        ]
      } : null

      // Generate evolution tracking
      const evolutionTracking = include_evolution_tracking === 'true' ? {
        current_generation: 'Gen-3',
        evolution_stage: profitabilityScore > 0.8 ? 'Advanced' : profitabilityScore > 0.6 ? 'Intermediate' : 'Basic',
        evolution_timeline: [
          { period: 'Q1 2024', score: Math.round((profitabilityScore - 0.1) * 100) / 100 },
          { period: 'Q2 2024', score: Math.round((profitabilityScore - 0.05) * 100) / 100 },
          { period: 'Q3 2024', score: Math.round(profitabilityScore * 100) / 100 },
          { period: 'Q4 2024', score: Math.round((profitabilityScore + 0.05) * 100) / 100 }
        ],
        next_evolution_target: Math.round((profitabilityScore + 0.1) * 100) / 100,
        evolution_recommendations: [
          'Optimize revenue efficiency through pricing strategies',
          'Improve service utilization through client engagement',
          'Enhance payment behavior through automated reminders',
          'Strengthen retention stability through value delivery'
        ]
      } : null

      // Generate DNA analysis
      const dnaAnalysis = include_dna_analysis === 'true' ? {
        dna_sequence: generateDNASequence(profitabilityDNA),
        mutation_probability: Math.round((1 - profitabilityScore) * 100) / 100,
        adaptation_capacity: Math.round(profitabilityScore * 100) / 100,
        survival_probability: Math.round((profitabilityScore * 0.8 + 0.2) * 100) / 100,
        fitness_score: Math.round(profitabilityScore * 100) / 100
      } : null

      profitabilityGenomes.push({
        client_id: client.id,
        client_name: client.name,
        client_company: client.company,
        organization_name: client.organization ? client.organization.name : 'Unknown',
        profitability_score: Math.round(profitabilityScore * 100) / 100,
        profitability_dna: profitabilityDNA,
        genetic_factors: geneticFactors,
        evolution_tracking: evolutionTracking,
        dna_analysis: dnaAnalysis,
        genome_classification: {
          category: profitabilityScore > 0.8 ? 'Elite' : profitabilityScore > 0.6 ? 'Premium' : profitabilityScore > 0.4 ? 'Standard' : 'Basic',
          tier: Math.ceil(profitabilityScore * 5),
          status: profitabilityScore > 0.7 ? 'Thriving' : profitabilityScore > 0.5 ? 'Stable' : 'At Risk'
        },
        recommendations: [
          'Focus on revenue efficiency optimization',
          'Improve service utilization rates',
          'Enhance payment behavior patterns',
          'Strengthen client retention strategies'
        ]
      })
    }

    // Calculate overall genome summary
    const totalClients = profitabilityGenomes.length
    const avgProfitabilityScore = totalClients > 0 ? 
      profitabilityGenomes.reduce((sum, genome) => sum + genome.profitability_score, 0) / totalClients : 0

    // Group by classification
    const classificationDistribution = {
      elite: profitabilityGenomes.filter(genome => genome.genome_classification.category === 'Elite').length,
      premium: profitabilityGenomes.filter(genome => genome.genome_classification.category === 'Premium').length,
      standard: profitabilityGenomes.filter(genome => genome.genome_classification.category === 'Standard').length,
      basic: profitabilityGenomes.filter(genome => genome.genome_classification.category === 'Basic').length
    }

    res.json({
      success: true,
      data: {
        include_dna_analysis: include_dna_analysis === 'true',
        include_genetic_factors: include_genetic_factors === 'true',
        include_evolution_tracking: include_evolution_tracking === 'true',
        summary: {
          total_clients: totalClients,
          avg_profitability_score: Math.round(avgProfitabilityScore * 100) / 100,
          classification_distribution: classificationDistribution
        },
        profitability_genomes: profitabilityGenomes
      }
    })
  } catch (error) {
    console.error('Get profitability genome error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching profitability genome'
    })
  }
}

// GET /api/ai/insights/service-optimization - Service optimization
const getServiceOptimization = async (req, res) => {
  try {
    const { 
      organization_id,
      service_id,
      optimization_focus = 'all', // efficiency, quality, cost, all
      include_automation = true,
      include_scaling = true
    } = req.query

    // Get service data
    const whereClause = {}
    if (organization_id) whereClause.organization_id = organization_id
    if (service_id) whereClause.id = service_id

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

    // Analyze service optimization opportunities
    const serviceOptimizations = []
    
    for (const service of services) {
      // Simulate service performance metrics
      const performanceMetrics = {
        efficiency_score: Math.random() * 0.4 + 0.6, // 0.6-1.0
        quality_score: Math.random() * 0.3 + 0.7, // 0.7-1.0
        cost_effectiveness: Math.random() * 0.5 + 0.5, // 0.5-1.0
        customer_satisfaction: Math.random() * 0.2 + 0.8, // 0.8-1.0
        utilization_rate: Math.random() * 0.4 + 0.6, // 0.6-1.0
        response_time: Math.random() * 2 + 1, // 1-3 hours
        resolution_rate: Math.random() * 0.2 + 0.8 // 0.8-1.0
      }

      // Generate optimization recommendations
      const optimizationRecommendations = []

      // Efficiency optimization
      if (optimization_focus === 'all' || optimization_focus === 'efficiency') {
        if (performanceMetrics.efficiency_score < 0.8) {
          optimizationRecommendations.push({
            category: 'efficiency',
            title: 'Process Automation',
            description: 'Implement automated workflows to improve service efficiency',
            impact_score: Math.round((0.9 - performanceMetrics.efficiency_score) * 100) / 100,
            implementation_effort: 'medium',
            estimated_improvement: Math.round((0.9 - performanceMetrics.efficiency_score) * 100) / 100,
            recommendations: [
              'Implement automated ticket routing',
              'Set up automated status updates',
              'Create automated reporting systems',
              'Implement workflow automation tools'
            ]
          })
        }
      }

      // Quality optimization
      if (optimization_focus === 'all' || optimization_focus === 'quality') {
        if (performanceMetrics.quality_score < 0.9) {
          optimizationRecommendations.push({
            category: 'quality',
            title: 'Quality Assurance Enhancement',
            description: 'Improve service quality through better processes and training',
            impact_score: Math.round((0.95 - performanceMetrics.quality_score) * 100) / 100,
            implementation_effort: 'high',
            estimated_improvement: Math.round((0.95 - performanceMetrics.quality_score) * 100) / 100,
            recommendations: [
              'Implement quality checkpoints',
              'Enhance staff training programs',
              'Create quality metrics dashboard',
              'Establish quality feedback loops'
            ]
          })
        }
      }

      // Cost optimization
      if (optimization_focus === 'all' || optimization_focus === 'cost') {
        if (performanceMetrics.cost_effectiveness < 0.8) {
          optimizationRecommendations.push({
            category: 'cost',
            title: 'Cost Optimization',
            description: 'Reduce service delivery costs while maintaining quality',
            impact_score: Math.round((0.9 - performanceMetrics.cost_effectiveness) * 100) / 100,
            implementation_effort: 'medium',
            estimated_improvement: Math.round((0.9 - performanceMetrics.cost_effectiveness) * 100) / 100,
            recommendations: [
              'Optimize resource allocation',
              'Implement cost tracking systems',
              'Negotiate better vendor rates',
              'Streamline service delivery processes'
            ]
          })
        }
      }

      // Automation opportunities
      const automationOpportunities = include_automation === 'true' ? [
        {
          area: 'Ticket Management',
          automation_level: 'high',
          potential_savings: Math.floor(Math.random() * 30) + 20, // 20-50%
          implementation_complexity: 'medium',
          description: 'Automate ticket creation, routing, and status updates'
        },
        {
          area: 'Reporting',
          automation_level: 'high',
          potential_savings: Math.floor(Math.random() * 40) + 30, // 30-70%
          implementation_complexity: 'low',
          description: 'Automate report generation and distribution'
        },
        {
          area: 'Client Communication',
          automation_level: 'medium',
          potential_savings: Math.floor(Math.random() * 25) + 15, // 15-40%
          implementation_complexity: 'medium',
          description: 'Automate client notifications and updates'
        }
      ] : []

      // Scaling opportunities
      const scalingOpportunities = include_scaling === 'true' ? [
        {
          type: 'Horizontal Scaling',
          description: 'Add more service instances to handle increased demand',
          scalability_score: Math.round(performanceMetrics.utilization_rate * 100) / 100,
          investment_required: 'medium',
          expected_roi: Math.round((performanceMetrics.utilization_rate * 0.3) * 100) / 100
        },
        {
          type: 'Vertical Scaling',
          description: 'Upgrade existing infrastructure for better performance',
          scalability_score: Math.round((1 - performanceMetrics.efficiency_score) * 100) / 100,
          investment_required: 'high',
          expected_roi: Math.round((1 - performanceMetrics.efficiency_score) * 0.4 * 100) / 100
        }
      ] : []

      // Calculate overall optimization score
      const optimizationScore = Object.values(performanceMetrics).reduce((sum, value) => sum + value, 0) / Object.keys(performanceMetrics).length

      serviceOptimizations.push({
        service_id: service.id,
        service_name: service.name,
        organization_name: service.organization ? service.organization.name : 'Unknown',
        client_name: service.client ? service.client.name : 'General',
        performance_metrics: performanceMetrics,
        optimization_score: Math.round(optimizationScore * 100) / 100,
        optimization_recommendations: optimizationRecommendations,
        automation_opportunities: automationOpportunities,
        scaling_opportunities: scalingOpportunities,
        optimization_roadmap: [
          { phase: 'Phase 1', duration: '3 months', focus: 'Process optimization', priority: 'high' },
          { phase: 'Phase 2', duration: '6 months', focus: 'Automation implementation', priority: 'medium' },
          { phase: 'Phase 3', duration: '9 months', focus: 'Scaling and growth', priority: 'low' }
        ],
        expected_improvements: {
          efficiency_gain: Math.round((0.9 - performanceMetrics.efficiency_score) * 100) / 100,
          quality_improvement: Math.round((0.95 - performanceMetrics.quality_score) * 100) / 100,
          cost_reduction: Math.round((0.9 - performanceMetrics.cost_effectiveness) * 100) / 100,
          customer_satisfaction_increase: Math.round((0.95 - performanceMetrics.customer_satisfaction) * 100) / 100
        }
      })
    }

    // Calculate overall summary
    const totalServices = serviceOptimizations.length
    const avgOptimizationScore = totalServices > 0 ? 
      serviceOptimizations.reduce((sum, service) => sum + service.optimization_score, 0) / totalServices : 0

    res.json({
      success: true,
      data: {
        optimization_focus,
        include_automation: include_automation === 'true',
        include_scaling: include_scaling === 'true',
        summary: {
          total_services: totalServices,
          avg_optimization_score: Math.round(avgOptimizationScore * 100) / 100,
          total_recommendations: serviceOptimizations.reduce((sum, service) => sum + service.optimization_recommendations.length, 0)
        },
        service_optimizations: serviceOptimizations
      }
    })
  } catch (error) {
    console.error('Get service optimization error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching service optimization'
    })
  }
}

// GET /api/ai/insights/pricing - Pricing recommendations
const getPricingRecommendations = async (req, res) => {
  try {
    const { 
      organization_id,
      service_id,
      pricing_strategy = 'all', // competitive, value_based, cost_plus, all
      include_market_analysis = true,
      include_client_segmentation = true
    } = req.query

    // Get service and invoice data
    const whereClause = {}
    if (organization_id) whereClause.organization_id = organization_id
    if (service_id) whereClause.id = service_id

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

    // Get invoice data for pricing analysis
    const invoices = await Invoice.findAll({
      where: organization_id ? { organization_id } : {},
      attributes: ['id', 'total_amount', 'invoice_date', 'status', 'client_id'],
      required: false
    })

    // Analyze pricing recommendations for each service
    const pricingRecommendations = []
    
    for (const service of services) {
      // Simulate current pricing data
      const currentPricing = {
        base_price: Math.floor(Math.random() * 500) + 100, // $100-$600
        hourly_rate: Math.floor(Math.random() * 100) + 50, // $50-$150/hour
        monthly_retainer: Math.floor(Math.random() * 2000) + 500, // $500-$2500
        setup_fee: Math.floor(Math.random() * 500) + 100 // $100-$600
      }

      // Generate pricing strategy recommendations
      const strategyRecommendations = []

      // Competitive pricing strategy
      if (pricing_strategy === 'all' || pricing_strategy === 'competitive') {
        const marketPosition = Math.random() * 0.4 + 0.3 // 0.3-0.7
        strategyRecommendations.push({
          strategy: 'competitive',
          title: 'Competitive Pricing Strategy',
          description: 'Price services based on market competition',
          current_position: Math.round(marketPosition * 100) / 100,
          recommended_adjustment: Math.round((0.5 - marketPosition) * 100) / 100,
          new_pricing: {
            base_price: Math.round(currentPricing.base_price * (1 + (0.5 - marketPosition))),
            hourly_rate: Math.round(currentPricing.hourly_rate * (1 + (0.5 - marketPosition))),
            monthly_retainer: Math.round(currentPricing.monthly_retainer * (1 + (0.5 - marketPosition)))
          },
          market_analysis: {
            competitor_avg_price: Math.round(currentPricing.base_price * (0.8 + Math.random() * 0.4)),
            market_share_potential: Math.round((0.5 - marketPosition) * 100) / 100,
            price_elasticity: Math.round((0.3 + Math.random() * 0.4) * 100) / 100
          }
        })
      }

      // Value-based pricing strategy
      if (pricing_strategy === 'all' || pricing_strategy === 'value_based') {
        const valueScore = Math.random() * 0.3 + 0.7 // 0.7-1.0
        strategyRecommendations.push({
          strategy: 'value_based',
          title: 'Value-Based Pricing Strategy',
          description: 'Price services based on delivered value',
          value_score: Math.round(valueScore * 100) / 100,
          recommended_adjustment: Math.round((valueScore - 0.5) * 100) / 100,
          new_pricing: {
            base_price: Math.round(currentPricing.base_price * (1 + (valueScore - 0.5))),
            hourly_rate: Math.round(currentPricing.hourly_rate * (1 + (valueScore - 0.5))),
            monthly_retainer: Math.round(currentPricing.monthly_retainer * (1 + (valueScore - 0.5)))
          },
          value_analysis: {
            client_satisfaction: Math.round((0.8 + Math.random() * 0.2) * 100) / 100,
            problem_solving_value: Math.round((0.7 + Math.random() * 0.3) * 100) / 100,
            time_savings_value: Math.round((0.6 + Math.random() * 0.4) * 100) / 100
          }
        })
      }

      // Cost-plus pricing strategy
      if (pricing_strategy === 'all' || pricing_strategy === 'cost_plus') {
        const costEfficiency = Math.random() * 0.4 + 0.6 // 0.6-1.0
        const marginTarget = 0.3 + Math.random() * 0.2 // 30-50%
        strategyRecommendations.push({
          strategy: 'cost_plus',
          title: 'Cost-Plus Pricing Strategy',
          description: 'Price services based on costs plus desired margin',
          cost_efficiency: Math.round(costEfficiency * 100) / 100,
          margin_target: Math.round(marginTarget * 100) / 100,
          recommended_adjustment: Math.round((marginTarget - 0.2) * 100) / 100,
          new_pricing: {
            base_price: Math.round(currentPricing.base_price * (1 + marginTarget)),
            hourly_rate: Math.round(currentPricing.hourly_rate * (1 + marginTarget)),
            monthly_retainer: Math.round(currentPricing.monthly_retainer * (1 + marginTarget))
          },
          cost_analysis: {
            direct_costs: Math.round(currentPricing.base_price * 0.6),
            indirect_costs: Math.round(currentPricing.base_price * 0.2),
            overhead_allocation: Math.round(currentPricing.base_price * 0.1),
            total_cost: Math.round(currentPricing.base_price * 0.9)
          }
        })
      }

      // Market analysis
      const marketAnalysis = include_market_analysis === 'true' ? {
        market_size: Math.floor(Math.random() * 1000000) + 500000, // $500K-$1.5M
        growth_rate: Math.round((Math.random() * 0.2 + 0.05) * 100) / 100, // 5-25%
        competitive_intensity: Math.round((Math.random() * 0.6 + 0.4) * 100) / 100, // 0.4-1.0
        price_sensitivity: Math.round((Math.random() * 0.5 + 0.3) * 100) / 100, // 0.3-0.8
        market_trends: [
          'Increasing demand for cloud services',
          'Growing emphasis on cybersecurity',
          'Rising automation requirements',
          'Shift towards subscription models'
        ]
      } : null

      // Client segmentation analysis
      const clientSegmentation = include_client_segmentation === 'true' ? [
        {
          segment: 'Enterprise',
          price_range: { min: 2000, max: 10000 },
          characteristics: ['Large organizations', 'Complex requirements', 'Long-term contracts'],
          recommended_pricing: Math.round(currentPricing.base_price * 1.5)
        },
        {
          segment: 'Mid-Market',
          price_range: { min: 500, max: 2000 },
          characteristics: ['Medium organizations', 'Standard requirements', 'Flexible contracts'],
          recommended_pricing: Math.round(currentPricing.base_price * 1.0)
        },
        {
          segment: 'SMB',
          price_range: { min: 100, max: 500 },
          characteristics: ['Small businesses', 'Basic requirements', 'Short-term contracts'],
          recommended_pricing: Math.round(currentPricing.base_price * 0.7)
        }
      ] : null

      // Calculate overall pricing score
      const pricingScore = Object.values(currentPricing).reduce((sum, value) => sum + value, 0) / Object.keys(currentPricing).length

      pricingRecommendations.push({
        service_id: service.id,
        service_name: service.name,
        organization_name: service.organization ? service.organization.name : 'Unknown',
        current_pricing: currentPricing,
        pricing_score: Math.round(pricingScore * 100) / 100,
        strategy_recommendations: strategyRecommendations,
        market_analysis: marketAnalysis,
        client_segmentation: clientSegmentation,
        pricing_insights: [
          'Current pricing is competitive in the market',
          'Opportunity for value-based pricing increase',
          'Consider tiered pricing for different client segments',
          'Monitor market trends for pricing adjustments'
        ],
        implementation_roadmap: [
          { phase: 'Analysis', duration: '1 month', tasks: ['Market research', 'Competitor analysis', 'Client feedback'] },
          { phase: 'Strategy', duration: '2 months', tasks: ['Pricing model design', 'Segmentation strategy', 'Value proposition'] },
          { phase: 'Implementation', duration: '3 months', tasks: ['Pricing rollout', 'Client communication', 'Performance monitoring'] }
        ]
      })
    }

    // Calculate overall summary
    const totalServices = pricingRecommendations.length
    const avgPricingScore = totalServices > 0 ? 
      pricingRecommendations.reduce((sum, service) => sum + service.pricing_score, 0) / totalServices : 0

    res.json({
      success: true,
      data: {
        pricing_strategy,
        include_market_analysis: include_market_analysis === 'true',
        include_client_segmentation: include_client_segmentation === 'true',
        summary: {
          total_services: totalServices,
          avg_pricing_score: Math.round(avgPricingScore * 100) / 100,
          total_recommendations: pricingRecommendations.reduce((sum, service) => sum + service.strategy_recommendations.length, 0)
        },
        pricing_recommendations: pricingRecommendations
      }
    })
  } catch (error) {
    console.error('Get pricing recommendations error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching pricing recommendations'
    })
  }
}

// GET /api/ai/insights/market - Market analysis
const getMarketAnalysis = async (req, res) => {
  try {
    const { 
      organization_id,
      analysis_depth = 'comprehensive', // basic, standard, comprehensive
      include_competitors = true,
      include_trends = true,
      include_opportunities = true
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

    // Analyze market for each organization
    const marketAnalyses = []
    
    for (const organization of organizations) {
      const clients = organization.clients || []
      const services = organization.services || []
      const invoices = organization.invoices || []

      // Calculate market position
      const marketPosition = {
        client_count: clients.length,
        service_count: services.length,
        total_revenue: Math.round(invoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount), 0) * 100) / 100,
        market_share: Math.random() * 0.3 + 0.1, // 10-40%
        growth_rate: Math.random() * 0.2 + 0.05, // 5-25%
        competitive_position: Math.random() > 0.5 ? 'strong' : 'moderate'
      }

      // Market size and trends
      const marketSize = {
        total_addressable_market: Math.floor(Math.random() * 50000000) + 10000000, // $10M-$60M
        serviceable_addressable_market: Math.floor(Math.random() * 10000000) + 2000000, // $2M-$12M
        serviceable_obtainable_market: Math.floor(Math.random() * 2000000) + 500000, // $500K-$2.5M
        market_growth_rate: Math.round((Math.random() * 0.15 + 0.05) * 100) / 100 // 5-20%
      }

      // Competitor analysis
      const competitorAnalysis = include_competitors === 'true' ? {
        direct_competitors: [
          {
            name: 'TechCorp Solutions',
            market_share: Math.round((Math.random() * 0.2 + 0.1) * 100) / 100,
            strengths: ['Strong brand recognition', 'Large client base', 'Comprehensive services'],
            weaknesses: ['High pricing', 'Slow innovation', 'Poor customer service'],
            threat_level: 'high'
          },
          {
            name: 'InnovateIT Services',
            market_share: Math.round((Math.random() * 0.15 + 0.05) * 100) / 100,
            strengths: ['Innovative solutions', 'Agile delivery', 'Competitive pricing'],
            weaknesses: ['Limited scale', 'New market presence', 'Resource constraints'],
            threat_level: 'medium'
          },
          {
            name: 'Enterprise Systems',
            market_share: Math.round((Math.random() * 0.25 + 0.15) * 100) / 100,
            strengths: ['Enterprise focus', 'Technical expertise', 'Long-term contracts'],
            weaknesses: ['Complex solutions', 'High costs', 'Slow adoption'],
            threat_level: 'medium'
          }
        ],
        competitive_landscape: {
          market_concentration: Math.round((Math.random() * 0.4 + 0.3) * 100) / 100, // 30-70%
          entry_barriers: Math.round((Math.random() * 0.5 + 0.5) * 100) / 100, // 50-100%
          competitive_intensity: Math.round((Math.random() * 0.6 + 0.4) * 100) / 100 // 40-100%
        }
      } : null

      // Market trends
      const marketTrends = include_trends === 'true' ? {
        technology_trends: [
          {
            trend: 'Cloud Migration',
            impact: 'high',
            adoption_rate: Math.round((Math.random() * 0.3 + 0.7) * 100) / 100,
            description: 'Increasing demand for cloud-based services and infrastructure'
          },
          {
            trend: 'AI Integration',
            impact: 'high',
            adoption_rate: Math.round((Math.random() * 0.4 + 0.6) * 100) / 100,
            description: 'Growing adoption of AI-powered solutions and automation'
          },
          {
            trend: 'Cybersecurity Focus',
            impact: 'critical',
            adoption_rate: Math.round((Math.random() * 0.2 + 0.8) * 100) / 100,
            description: 'Heightened focus on cybersecurity and data protection'
          },
          {
            trend: 'Remote Work Support',
            impact: 'medium',
            adoption_rate: Math.round((Math.random() * 0.3 + 0.7) * 100) / 100,
            description: 'Sustained demand for remote work infrastructure and support'
          }
        ],
        business_trends: [
          {
            trend: 'Subscription Models',
            impact: 'high',
            adoption_rate: Math.round((Math.random() * 0.4 + 0.6) * 100) / 100,
            description: 'Shift towards subscription-based service delivery'
          },
          {
            trend: 'Outsourcing Growth',
            impact: 'medium',
            adoption_rate: Math.round((Math.random() * 0.3 + 0.5) * 100) / 100,
            description: 'Increased outsourcing of IT services'
          },
          {
            trend: 'Digital Transformation',
            impact: 'high',
            adoption_rate: Math.round((Math.random() * 0.2 + 0.8) * 100) / 100,
            description: 'Accelerated digital transformation initiatives'
          }
        ]
      } : null

      // Market opportunities
      const marketOpportunities = include_opportunities === 'true' ? [
        {
          opportunity: 'SMB Market Expansion',
          market_size: Math.floor(Math.random() * 5000000) + 1000000, // $1M-$6M
          growth_potential: Math.round((Math.random() * 0.3 + 0.7) * 100) / 100,
          competition_level: 'medium',
          entry_barriers: 'low',
          description: 'Expand services to small and medium businesses',
          recommended_strategy: 'Develop cost-effective solutions for SMB market'
        },
        {
          opportunity: 'Vertical Specialization',
          market_size: Math.floor(Math.random() * 3000000) + 500000, // $500K-$3.5M
          growth_potential: Math.round((Math.random() * 0.4 + 0.6) * 100) / 100,
          competition_level: 'low',
          entry_barriers: 'medium',
          description: 'Specialize in specific industry verticals',
          recommended_strategy: 'Develop industry-specific expertise and solutions'
        },
        {
          opportunity: 'Geographic Expansion',
          market_size: Math.floor(Math.random() * 8000000) + 2000000, // $2M-$10M
          growth_potential: Math.round((Math.random() * 0.5 + 0.5) * 100) / 100,
          competition_level: 'high',
          entry_barriers: 'high',
          description: 'Expand services to new geographic markets',
          recommended_strategy: 'Partner with local providers and establish presence'
        }
      ] : null

      // Market insights and recommendations
      const marketInsights = [
        'Market is growing at a steady rate with increasing demand for cloud services',
        'Competition is intensifying, requiring differentiation strategies',
        'Opportunities exist in underserved market segments',
        'Technology trends are driving new service requirements',
        'Client expectations are evolving towards more integrated solutions'
      ]

      const strategicRecommendations = [
        'Focus on high-growth market segments',
        'Develop competitive differentiation strategies',
        'Invest in emerging technology capabilities',
        'Strengthen client relationships and retention',
        'Explore strategic partnerships and alliances'
      ]

      marketAnalyses.push({
        organization_id: organization.id,
        organization_name: organization.name,
        analysis_depth,
        market_position: marketPosition,
        market_size: marketSize,
        competitor_analysis: competitorAnalysis,
        market_trends: marketTrends,
        market_opportunities: marketOpportunities,
        market_insights: marketInsights,
        strategic_recommendations: strategicRecommendations,
        market_score: Math.round((marketPosition.market_share + marketPosition.growth_rate + marketPosition.competitive_position === 'strong' ? 0.8 : 0.5) * 100) / 100
      })
    }

    // Calculate overall summary
    const totalOrganizations = marketAnalyses.length
    const avgMarketScore = totalOrganizations > 0 ? 
      marketAnalyses.reduce((sum, analysis) => sum + analysis.market_score, 0) / totalOrganizations : 0

    res.json({
      success: true,
      data: {
        analysis_depth,
        include_competitors: include_competitors === 'true',
        include_trends: include_trends === 'true',
        include_opportunities: include_opportunities === 'true',
        summary: {
          total_organizations: totalOrganizations,
          avg_market_score: Math.round(avgMarketScore * 100) / 100,
          total_opportunities: marketAnalyses.reduce((sum, analysis) => sum + (analysis.market_opportunities ? analysis.market_opportunities.length : 0), 0)
        },
        market_analyses: marketAnalyses
      }
    })
  } catch (error) {
    console.error('Get market analysis error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching market analysis'
    })
  }
}

// GET /api/ai/insights/competitive - Competitive intelligence
const getCompetitiveIntelligence = async (req, res) => {
  try {
    const { 
      organization_id,
      competitor_focus = 'all', // direct, indirect, all
      analysis_type = 'comprehensive', // basic, detailed, comprehensive
      include_swot = true,
      include_positioning = true
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
          attributes: ['id', 'name', 'company'],
          required: false
        },
        {
          model: Service,
          as: 'services',
          attributes: ['id', 'name', 'status'],
          required: false
        },
        {
          model: Invoice,
          as: 'invoices',
          attributes: ['id', 'total_amount', 'status'],
          required: false
        }
      ]
    })

    // Analyze competitive intelligence for each organization
    const competitiveIntelligence = []
    
    for (const organization of organizations) {
      const clients = organization.clients || []
      const services = organization.services || []
      const invoices = organization.invoices || []

      // Calculate organization metrics
      const organizationMetrics = {
        client_count: clients.length,
        service_count: services.length,
        total_revenue: Math.round(invoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount), 0) * 100) / 100,
        market_share: Math.random() * 0.3 + 0.1, // 10-40%
        growth_rate: Math.random() * 0.2 + 0.05, // 5-25%
        client_retention: Math.random() * 0.2 + 0.8, // 80-100%
        service_quality: Math.random() * 0.3 + 0.7 // 70-100%
      }

      // Competitive landscape analysis
      const competitiveLandscape = {
        market_leaders: [
          {
            name: 'TechCorp Solutions',
            market_share: Math.round((Math.random() * 0.2 + 0.2) * 100) / 100, // 20-40%
            strengths: ['Market leadership', 'Brand recognition', 'Comprehensive portfolio'],
            weaknesses: ['High costs', 'Slow innovation', 'Complex solutions'],
            threat_level: 'high'
          },
          {
            name: 'Enterprise Systems',
            market_share: Math.round((Math.random() * 0.15 + 0.15) * 100) / 100, // 15-30%
            strengths: ['Enterprise focus', 'Technical expertise', 'Long-term relationships'],
            weaknesses: ['Limited flexibility', 'High complexity', 'Slow adoption'],
            threat_level: 'medium'
          }
        ],
        emerging_competitors: [
          {
            name: 'InnovateIT Services',
            market_share: Math.round((Math.random() * 0.1 + 0.05) * 100) / 100, // 5-15%
            strengths: ['Innovation', 'Agility', 'Competitive pricing'],
            weaknesses: ['Limited scale', 'New presence', 'Resource constraints'],
            threat_level: 'medium'
          },
          {
            name: 'CloudFirst Solutions',
            market_share: Math.round((Math.random() * 0.08 + 0.02) * 100) / 100, // 2-10%
            strengths: ['Cloud expertise', 'Modern architecture', 'Scalable solutions'],
            weaknesses: ['Limited experience', 'Small team', 'Narrow focus'],
            threat_level: 'low'
          }
        ],
        market_dynamics: {
          competitive_intensity: Math.round((Math.random() * 0.6 + 0.4) * 100) / 100, // 40-100%
          market_concentration: Math.round((Math.random() * 0.4 + 0.3) * 100) / 100, // 30-70%
          entry_barriers: Math.round((Math.random() * 0.5 + 0.5) * 100) / 100, // 50-100%
          price_competition: Math.round((Math.random() * 0.6 + 0.4) * 100) / 100 // 40-100%
        }
      }

      // SWOT analysis
      const swotAnalysis = include_swot === 'true' ? {
        strengths: [
          'Strong client relationships and retention',
          'Comprehensive service portfolio',
          'Experienced technical team',
          'Proven track record of delivery'
        ],
        weaknesses: [
          'Limited market presence in new segments',
          'Higher pricing compared to competitors',
          'Slow adoption of new technologies',
          'Limited marketing and brand awareness'
        ],
        opportunities: [
          'Growing demand for cloud services',
          'Expansion into underserved markets',
          'Partnership opportunities with technology vendors',
          'Increasing cybersecurity requirements'
        ],
        threats: [
          'Intensifying competition from established players',
          'Emerging competitors with innovative solutions',
          'Economic uncertainty affecting client spending',
          'Rapid technology changes requiring constant adaptation'
        ]
      } : null

      // Competitive positioning
      const competitivePositioning = include_positioning === 'true' ? {
        positioning_matrix: {
          price_position: Math.round((Math.random() * 0.6 + 0.2) * 100) / 100, // 20-80%
          quality_position: Math.round((Math.random() * 0.4 + 0.6) * 100) / 100, // 60-100%
          innovation_position: Math.round((Math.random() * 0.5 + 0.5) * 100) / 100, // 50-100%
          service_position: Math.round((Math.random() * 0.3 + 0.7) * 100) / 100 // 70-100%
        },
        competitive_advantages: [
          'Superior client service and support',
          'Deep technical expertise',
          'Flexible and customizable solutions',
          'Strong industry relationships'
        ],
        competitive_disadvantages: [
          'Higher pricing than some competitors',
          'Limited geographic presence',
          'Slower innovation cycle',
          'Smaller marketing budget'
        ],
        differentiation_strategy: [
          'Focus on client success and outcomes',
          'Emphasize technical expertise and quality',
          'Develop niche specializations',
          'Build strong partner ecosystem'
        ]
      } : null

      // Competitive intelligence insights
      const intelligenceInsights = [
        'Market leaders are focusing on enterprise clients and large-scale implementations',
        'Emerging competitors are gaining traction through innovation and competitive pricing',
        'Competition is intensifying in the mid-market segment',
        'Technology trends are creating new competitive dynamics',
        'Client expectations are evolving towards more integrated solutions'
      ]

      // Strategic recommendations
      const strategicRecommendations = [
        'Strengthen competitive differentiation through service quality',
        'Develop niche specializations to reduce direct competition',
        'Invest in innovation to match emerging competitors',
        'Build strategic partnerships to enhance market position',
        'Focus on client retention and relationship building'
      ]

      // Competitive threat assessment
      const threatAssessment = {
        immediate_threats: [
          {
            threat: 'Price competition from emerging competitors',
            severity: 'high',
            probability: 'medium',
            impact: 'financial',
            mitigation: 'Focus on value-based pricing and service differentiation'
          },
          {
            threat: 'Technology disruption from new entrants',
            severity: 'medium',
            probability: 'high',
            impact: 'strategic',
            mitigation: 'Invest in emerging technologies and innovation'
          }
        ],
        long_term_threats: [
          {
            threat: 'Market consolidation reducing opportunities',
            severity: 'medium',
            probability: 'low',
            impact: 'strategic',
            mitigation: 'Develop unique value propositions and market positioning'
          },
          {
            threat: 'Economic downturn affecting client spending',
            severity: 'high',
            probability: 'medium',
            impact: 'financial',
            mitigation: 'Diversify client base and service offerings'
          }
        ]
      }

      competitiveIntelligence.push({
        organization_id: organization.id,
        organization_name: organization.name,
        competitor_focus,
        analysis_type,
        organization_metrics: organizationMetrics,
        competitive_landscape: competitiveLandscape,
        swot_analysis: swotAnalysis,
        competitive_positioning: competitivePositioning,
        intelligence_insights: intelligenceInsights,
        strategic_recommendations: strategicRecommendations,
        threat_assessment: threatAssessment,
        competitive_score: Math.round((organizationMetrics.market_share + organizationMetrics.growth_rate + organizationMetrics.client_retention) * 100) / 100
      })
    }

    // Calculate overall summary
    const totalOrganizations = competitiveIntelligence.length
    const avgCompetitiveScore = totalOrganizations > 0 ? 
      competitiveIntelligence.reduce((sum, intelligence) => sum + intelligence.competitive_score, 0) / totalOrganizations : 0

    res.json({
      success: true,
      data: {
        competitor_focus,
        analysis_type,
        include_swot: include_swot === 'true',
        include_positioning: include_positioning === 'true',
        summary: {
          total_organizations: totalOrganizations,
          avg_competitive_score: Math.round(avgCompetitiveScore * 100) / 100,
          total_threats: competitiveIntelligence.reduce((sum, intelligence) => 
            sum + intelligence.threat_assessment.immediate_threats.length + intelligence.threat_assessment.long_term_threats.length, 0)
        },
        competitive_intelligence: competitiveIntelligence
      }
    })
  } catch (error) {
    console.error('Get competitive intelligence error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching competitive intelligence'
    })
  }
}

// POST /api/ai/insights/accept-recommendation - Accept recommendation
const acceptRecommendation = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const {
      recommendation_id,
      organization_id,
      acceptance_notes,
      implementation_plan,
      expected_outcomes
    } = req.body

    // Check if recommendation exists
    const recommendation = await AIRecommendation.findByPk(recommendation_id)
    if (!recommendation) {
      return res.status(404).json({
        success: false,
        message: 'Recommendation not found'
      })
    }

    // Check if organization matches
    if (recommendation.organization_id !== organization_id) {
      return res.status(400).json({
        success: false,
        message: 'Organization does not match recommendation'
      })
    }

    // Update recommendation status
    await recommendation.update({
      status: 'accepted',
      notes: acceptance_notes || recommendation.notes,
      implementation_plan: implementation_plan || null,
      expected_outcomes: expected_outcomes || null
    })

    // Create implementation tracking record
    const implementationRecord = {
      recommendation_id: recommendation.id,
      organization_id: organization_id,
      status: 'accepted',
      acceptance_date: new Date().toISOString(),
      acceptance_notes: acceptance_notes,
      implementation_plan: implementation_plan,
      expected_outcomes: expected_outcomes,
      next_steps: [
        'Review implementation plan with stakeholders',
        'Allocate resources for implementation',
        'Set up monitoring and tracking systems',
        'Begin implementation according to timeline'
      ]
    }

    res.json({
      success: true,
      message: 'Recommendation accepted successfully',
      data: {
        recommendation_id: recommendation.id,
        recommendation_type: recommendation.recommendation_type,
        title: recommendation.title,
        status: 'accepted',
        implementation_record: implementationRecord,
        next_steps: implementationRecord.next_steps
      }
    })
  } catch (error) {
    console.error('Accept recommendation error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while accepting recommendation'
    })
  }
}

// Helper function to generate DNA sequence
const generateDNASequence = (profitabilityDNA) => {
  const traits = Object.keys(profitabilityDNA)
  const sequence = traits.map(trait => {
    const value = profitabilityDNA[trait]
    if (value > 0.8) return 'A' // Strong
    if (value > 0.6) return 'T' // Good
    if (value > 0.4) return 'G' // Average
    return 'C' // Weak
  }).join('')
  
  return {
    sequence: sequence,
    length: sequence.length,
    composition: {
      A: (sequence.match(/A/g) || []).length,
      T: (sequence.match(/T/g) || []).length,
      G: (sequence.match(/G/g) || []).length,
      C: (sequence.match(/C/g) || []).length
    }
  }
}

module.exports = {
  getProfitabilityGenome,
  getServiceOptimization,
  getPricingRecommendations,
  getMarketAnalysis,
  getCompetitiveIntelligence,
  acceptRecommendation
}
