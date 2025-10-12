const { Invoice, Client, Organization } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')

// GET /api/analytics/revenue-trends - Revenue trends
const getRevenueTrends = async (req, res) => {
  try {
    const { 
      organization_id,
      period = 'monthly', // daily, weekly, monthly, quarterly, yearly
      start_date,
      end_date,
      client_id
    } = req.query

    // Calculate date range
    const now = new Date()
    let startDate, endDate
    
    if (start_date && end_date) {
      startDate = new Date(start_date)
      endDate = new Date(end_date)
    } else {
      // Default to last 12 months
      endDate = now
      startDate = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate())
    }

    // Build where clause
    const whereClause = {
      invoice_date: { [Op.between]: [startDate, endDate] },
      status: 'paid'
    }
    if (organization_id) whereClause.organization_id = organization_id
    if (client_id) whereClause.client_id = client_id

    // Determine date grouping based on period
    let dateFormat, groupBy
    switch (period) {
      case 'daily':
        dateFormat = '%Y-%m-%d'
        groupBy = 'DATE(invoice_date)'
        break
      case 'weekly':
        dateFormat = '%Y-%u'
        groupBy = 'YEAR(invoice_date), WEEK(invoice_date)'
        break
      case 'monthly':
        dateFormat = '%Y-%m'
        groupBy = 'YEAR(invoice_date), MONTH(invoice_date)'
        break
      case 'quarterly':
        dateFormat = '%Y-%q'
        groupBy = 'YEAR(invoice_date), QUARTER(invoice_date)'
        break
      case 'yearly':
        dateFormat = '%Y'
        groupBy = 'YEAR(invoice_date)'
        break
      default:
        dateFormat = '%Y-%m'
        groupBy = 'YEAR(invoice_date), MONTH(invoice_date)'
    }

    // Get revenue trends - simplified for SQLite
    const revenueData = await Invoice.findAll({
      where: whereClause,
      attributes: [
        [Invoice.sequelize.fn('strftime', '%Y-%m', Invoice.sequelize.col('invoice_date')), 'period'],
        [Invoice.sequelize.fn('SUM', Invoice.sequelize.col('total_amount')), 'revenue'],
        [Invoice.sequelize.fn('COUNT', Invoice.sequelize.col('id')), 'invoice_count'],
        [Invoice.sequelize.fn('AVG', Invoice.sequelize.col('total_amount')), 'avg_invoice_value']
      ],
      group: [Invoice.sequelize.literal('strftime("%Y-%m", invoice_date)')],
      order: [[Invoice.sequelize.literal('strftime("%Y-%m", invoice_date)'), 'ASC']],
      raw: true
    })

    // Calculate growth rates
    const trends = revenueData.map((item, index) => {
      const previousRevenue = index > 0 ? parseFloat(revenueData[index - 1].revenue) : 0
      const currentRevenue = parseFloat(item.revenue)
      const growthRate = previousRevenue > 0 ? 
        ((currentRevenue - previousRevenue) / previousRevenue) * 100 : 0

      return {
        period: item.period,
        revenue: parseFloat(item.revenue),
        invoice_count: parseInt(item.invoice_count),
        avg_invoice_value: parseFloat(item.avg_invoice_value),
        growth_rate: Math.round(growthRate * 100) / 100,
        previous_revenue: previousRevenue
      }
    })

    // Calculate summary statistics
    const totalRevenue = trends.reduce((sum, item) => sum + item.revenue, 0)
    const totalInvoices = trends.reduce((sum, item) => sum + item.invoice_count, 0)
    const avgGrowthRate = trends.length > 1 ? 
      trends.slice(1).reduce((sum, item) => sum + item.growth_rate, 0) / (trends.length - 1) : 0

    res.json({
      success: true,
      data: {
        period,
        date_range: {
          start_date: startDate,
          end_date: endDate
        },
        summary: {
          total_revenue: Math.round(totalRevenue * 100) / 100,
          total_invoices: totalInvoices,
          avg_growth_rate: Math.round(avgGrowthRate * 100) / 100,
          periods_analyzed: trends.length
        },
        trends
      }
    })
  } catch (error) {
    console.error('Get revenue trends error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching revenue trends'
    })
  }
}

// GET /api/analytics/payment-status - Payment status charts
const getPaymentStatus = async (req, res) => {
  try {
    const { 
      organization_id,
      start_date,
      end_date,
      client_id
    } = req.query

    // Calculate date range
    const now = new Date()
    let startDate, endDate
    
    if (start_date && end_date) {
      startDate = new Date(start_date)
      endDate = new Date(end_date)
    } else {
      // Default to last 6 months
      endDate = now
      startDate = new Date(now.getFullYear(), now.getMonth() - 6, now.getDate())
    }

    // Build where clause
    const whereClause = {
      invoice_date: { [Op.between]: [startDate, endDate] }
    }
    if (organization_id) whereClause.organization_id = organization_id
    if (client_id) whereClause.client_id = client_id

    // Get payment status breakdown
    const statusData = await Invoice.findAll({
      where: whereClause,
      attributes: [
        'status',
        [Invoice.sequelize.fn('COUNT', Invoice.sequelize.col('id')), 'count'],
        [Invoice.sequelize.fn('SUM', Invoice.sequelize.col('total_amount')), 'total_amount']
      ],
      group: ['status'],
      raw: true
    })

    // Get overdue invoices (invoices past due date with status not 'paid')
    const overdueInvoices = await Invoice.findAll({
      where: {
        ...whereClause,
        due_date: { [Op.lt]: now },
        status: { [Op.notIn]: ['paid'] }
      },
      attributes: [
        [Invoice.sequelize.fn('COUNT', Invoice.sequelize.col('id')), 'count'],
        [Invoice.sequelize.fn('SUM', Invoice.sequelize.col('total_amount')), 'total_amount']
      ],
      raw: true
    })

    // Calculate percentages
    const totalInvoices = statusData.reduce((sum, item) => sum + parseInt(item.count), 0)
    const totalAmount = statusData.reduce((sum, item) => sum + parseFloat(item.total_amount || 0), 0)

    const statusBreakdown = statusData.map(item => ({
      status: item.status,
      count: parseInt(item.count),
      amount: parseFloat(item.total_amount || 0),
      percentage: totalInvoices > 0 ? Math.round((parseInt(item.count) / totalInvoices) * 100) : 0,
      amount_percentage: totalAmount > 0 ? Math.round((parseFloat(item.total_amount || 0) / totalAmount) * 100) : 0
    }))

    // Add overdue data
    const overdueData = {
      count: parseInt(overdueInvoices[0]?.count || 0),
      amount: parseFloat(overdueInvoices[0]?.total_amount || 0),
      percentage: totalInvoices > 0 ? Math.round((parseInt(overdueInvoices[0]?.count || 0) / totalInvoices) * 100) : 0
    }

    res.json({
      success: true,
      data: {
        date_range: {
          start_date: startDate,
          end_date: endDate
        },
        summary: {
          total_invoices: totalInvoices,
          total_amount: Math.round(totalAmount * 100) / 100,
          overdue_invoices: overdueData.count,
          overdue_amount: Math.round(overdueData.amount * 100) / 100
        },
        status_breakdown: statusBreakdown,
        overdue: overdueData
      }
    })
  } catch (error) {
    console.error('Get payment status error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching payment status'
    })
  }
}

// GET /api/analytics/outstanding-payments - Outstanding payments
const getOutstandingPayments = async (req, res) => {
  try {
    const { 
      organization_id,
      client_id,
      days_overdue,
      amount_min,
      amount_max,
      sort_by = 'due_date',
      sort_order = 'ASC'
    } = req.query

    // Build where clause for outstanding payments
    const whereClause = {
      status: { [Op.notIn]: ['paid'] }
    }
    if (organization_id) whereClause.organization_id = organization_id
    if (client_id) whereClause.client_id = client_id

    // Add overdue filter
    if (days_overdue) {
      const overdueDate = new Date()
      overdueDate.setDate(overdueDate.getDate() - parseInt(days_overdue))
      whereClause.due_date = { [Op.lt]: overdueDate }
    }

    // Add amount filters
    if (amount_min || amount_max) {
      whereClause.total_amount = {}
      if (amount_min) whereClause.total_amount[Op.gte] = parseFloat(amount_min)
      if (amount_max) whereClause.total_amount[Op.lte] = parseFloat(amount_max)
    }

    // Build order clause
    const orderClause = [[sort_by, sort_order.toUpperCase()]]

    const outstandingInvoices = await Invoice.findAll({
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
          attributes: ['id', 'name', 'email', 'company', 'contact_person', 'phone']
        }
      ],
      order: orderClause
    })

    // Calculate days overdue for each invoice
    const now = new Date()
    const processedInvoices = outstandingInvoices.map(invoice => {
      const dueDate = new Date(invoice.due_date)
      const daysOverdue = invoice.due_date ? 
        Math.ceil((now - dueDate) / (1000 * 60 * 60 * 24)) : null

      return {
        id: invoice.id,
        invoice_number: invoice.invoice_number,
        client_name: invoice.client ? invoice.client.name : 'Unknown',
        client_company: invoice.client ? invoice.client.company : 'Unknown',
        client_email: invoice.client ? invoice.client.email : null,
        client_phone: invoice.client ? invoice.client.phone : null,
        invoice_date: invoice.invoice_date,
        due_date: invoice.due_date,
        total_amount: parseFloat(invoice.total_amount),
        status: invoice.status,
        days_overdue: daysOverdue,
        is_overdue: daysOverdue > 0,
        organization_name: invoice.organization ? invoice.organization.name : 'Unknown'
      }
    })

    // Calculate summary statistics
    const totalOutstanding = processedInvoices.reduce((sum, invoice) => sum + invoice.total_amount, 0)
    const overdueCount = processedInvoices.filter(invoice => invoice.is_overdue).length
    const overdueAmount = processedInvoices
      .filter(invoice => invoice.is_overdue)
      .reduce((sum, invoice) => sum + invoice.total_amount, 0)

    // Group by client for client-level analysis
    const clientSummary = {}
    processedInvoices.forEach(invoice => {
      const clientId = invoice.client_name
      if (!clientSummary[clientId]) {
        clientSummary[clientId] = {
          client_name: invoice.client_name,
          client_company: invoice.client_company,
          invoice_count: 0,
          total_amount: 0,
          overdue_count: 0,
          overdue_amount: 0
        }
      }
      clientSummary[clientId].invoice_count++
      clientSummary[clientId].total_amount += invoice.total_amount
      if (invoice.is_overdue) {
        clientSummary[clientId].overdue_count++
        clientSummary[clientId].overdue_amount += invoice.total_amount
      }
    })

    res.json({
      success: true,
      data: {
        summary: {
          total_outstanding_amount: Math.round(totalOutstanding * 100) / 100,
          total_outstanding_invoices: processedInvoices.length,
          overdue_invoices: overdueCount,
          overdue_amount: Math.round(overdueAmount * 100) / 100,
          overdue_percentage: processedInvoices.length > 0 ? 
            Math.round((overdueCount / processedInvoices.length) * 100) : 0
        },
        invoices: processedInvoices,
        client_summary: Object.values(clientSummary)
      }
    })
  } catch (error) {
    console.error('Get outstanding payments error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching outstanding payments'
    })
  }
}

// GET /api/analytics/billing-efficiency - Billing efficiency
const getBillingEfficiency = async (req, res) => {
  try {
    const { 
      organization_id,
      start_date,
      end_date,
      client_id
    } = req.query

    // Calculate date range
    const now = new Date()
    let startDate, endDate
    
    if (start_date && end_date) {
      startDate = new Date(start_date)
      endDate = new Date(end_date)
    } else {
      // Default to last 12 months
      endDate = now
      startDate = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate())
    }

    // Build where clause
    const whereClause = {
      invoice_date: { [Op.between]: [startDate, endDate] }
    }
    if (organization_id) whereClause.organization_id = organization_id
    if (client_id) whereClause.client_id = client_id

    // Get billing efficiency metrics
    const efficiencyData = await Invoice.findAll({
      where: whereClause,
      attributes: [
        [Invoice.sequelize.fn('COUNT', Invoice.sequelize.col('id')), 'total_invoices'],
        [Invoice.sequelize.fn('SUM', Invoice.sequelize.col('total_amount')), 'total_amount'],
        [Invoice.sequelize.fn('AVG', Invoice.sequelize.col('total_amount')), 'avg_invoice_value'],
        [Invoice.sequelize.fn('COUNT', Invoice.sequelize.literal("CASE WHEN status = 'paid' THEN 1 END")), 'paid_invoices'],
        [Invoice.sequelize.fn('SUM', Invoice.sequelize.literal("CASE WHEN status = 'paid' THEN total_amount ELSE 0 END")), 'paid_amount'],
        [Invoice.sequelize.fn('AVG', Invoice.sequelize.literal("CASE WHEN status = 'paid' AND payment_date IS NOT NULL THEN (julianday(payment_date) - julianday(invoice_date)) END")), 'avg_payment_days']
      ],
      raw: true
    })

    const metrics = efficiencyData[0]
    const totalInvoices = parseInt(metrics.total_invoices)
    const totalAmount = parseFloat(metrics.total_amount || 0)
    const paidInvoices = parseInt(metrics.paid_invoices)
    const paidAmount = parseFloat(metrics.paid_amount || 0)
    const avgPaymentDays = parseFloat(metrics.avg_payment_days || 0)

    // Calculate efficiency metrics
    const collectionRate = totalInvoices > 0 ? (paidInvoices / totalInvoices) * 100 : 0
    const revenueCollectionRate = totalAmount > 0 ? (paidAmount / totalAmount) * 100 : 0
    const avgInvoiceValue = parseFloat(metrics.avg_invoice_value || 0)

    // Get payment timeline analysis
    const paymentTimeline = await Invoice.findAll({
      where: {
        ...whereClause,
        status: 'paid',
        payment_date: { [Op.not]: null }
      },
      attributes: [
        [Invoice.sequelize.literal('(julianday(payment_date) - julianday(invoice_date))'), 'payment_days'],
        [Invoice.sequelize.fn('COUNT', Invoice.sequelize.col('id')), 'count']
      ],
      group: [Invoice.sequelize.literal('(julianday(payment_date) - julianday(invoice_date))')],
      order: [[Invoice.sequelize.literal('payment_days'), 'ASC']],
      raw: true
    })

    // Categorize payment speed
    const paymentSpeedCategories = {
      '0-7 days': 0,
      '8-15 days': 0,
      '16-30 days': 0,
      '31-60 days': 0,
      '60+ days': 0
    }

    paymentTimeline.forEach(item => {
      const days = parseInt(item.payment_days)
      if (days <= 7) paymentSpeedCategories['0-7 days'] += parseInt(item.count)
      else if (days <= 15) paymentSpeedCategories['8-15 days'] += parseInt(item.count)
      else if (days <= 30) paymentSpeedCategories['16-30 days'] += parseInt(item.count)
      else if (days <= 60) paymentSpeedCategories['31-60 days'] += parseInt(item.count)
      else paymentSpeedCategories['60+ days'] += parseInt(item.count)
    })

    res.json({
      success: true,
      data: {
        date_range: {
          start_date: startDate,
          end_date: endDate
        },
        efficiency_metrics: {
          total_invoices: totalInvoices,
          total_amount: Math.round(totalAmount * 100) / 100,
          paid_invoices: paidInvoices,
          paid_amount: Math.round(paidAmount * 100) / 100,
          collection_rate: Math.round(collectionRate * 100) / 100,
          revenue_collection_rate: Math.round(revenueCollectionRate * 100) / 100,
          avg_invoice_value: Math.round(avgInvoiceValue * 100) / 100,
          avg_payment_days: Math.round(avgPaymentDays * 100) / 100
        },
        payment_speed_analysis: {
          categories: paymentSpeedCategories,
          total_paid_invoices: paidInvoices
        }
      }
    })
  } catch (error) {
    console.error('Get billing efficiency error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching billing efficiency'
    })
  }
}

// GET /api/analytics/payment-methods - Payment method analytics
const getPaymentMethods = async (req, res) => {
  try {
    const { 
      organization_id,
      start_date,
      end_date,
      client_id
    } = req.query

    // Calculate date range
    const now = new Date()
    let startDate, endDate
    
    if (start_date && end_date) {
      startDate = new Date(start_date)
      endDate = new Date(end_date)
    } else {
      // Default to last 12 months
      endDate = now
      startDate = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate())
    }

    // Build where clause
    const whereClause = {
      status: 'paid',
      payment_date: { [Op.between]: [startDate, endDate] }
    }
    if (organization_id) whereClause.organization_id = organization_id
    if (client_id) whereClause.client_id = client_id

    // Get payment method breakdown
    const paymentMethods = await Invoice.findAll({
      where: whereClause,
      attributes: [
        'payment_method',
        [Invoice.sequelize.fn('COUNT', Invoice.sequelize.col('id')), 'count'],
        [Invoice.sequelize.fn('SUM', Invoice.sequelize.col('total_amount')), 'total_amount'],
        [Invoice.sequelize.fn('AVG', Invoice.sequelize.col('total_amount')), 'avg_amount']
      ],
      group: ['payment_method'],
      order: [[Invoice.sequelize.fn('SUM', Invoice.sequelize.col('total_amount')), 'DESC']],
      raw: true
    })

    // Calculate totals
    const totalPayments = paymentMethods.reduce((sum, item) => sum + parseInt(item.count), 0)
    const totalAmount = paymentMethods.reduce((sum, item) => sum + parseFloat(item.total_amount || 0), 0)

    // Process payment methods with percentages
    const processedMethods = paymentMethods.map(method => ({
      payment_method: method.payment_method || 'Unknown',
      count: parseInt(method.count),
      total_amount: parseFloat(method.total_amount || 0),
      avg_amount: parseFloat(method.avg_amount || 0),
      count_percentage: totalPayments > 0 ? Math.round((parseInt(method.count) / totalPayments) * 100) : 0,
      amount_percentage: totalAmount > 0 ? Math.round((parseFloat(method.total_amount || 0) / totalAmount) * 100) : 0
    }))

    // Get payment method trends over time
    const monthlyTrends = await Invoice.findAll({
      where: whereClause,
      attributes: [
        [Invoice.sequelize.fn('strftime', '%Y-%m', Invoice.sequelize.col('payment_date')), 'month'],
        'payment_method',
        [Invoice.sequelize.fn('COUNT', Invoice.sequelize.col('id')), 'count'],
        [Invoice.sequelize.fn('SUM', Invoice.sequelize.col('total_amount')), 'amount']
      ],
      group: [
        Invoice.sequelize.fn('strftime', '%Y-%m', Invoice.sequelize.col('payment_date')),
        'payment_method'
      ],
      order: [
        [Invoice.sequelize.fn('strftime', '%Y-%m', Invoice.sequelize.col('payment_date')), 'ASC'],
        ['payment_method', 'ASC']
      ],
      raw: true
    })

    res.json({
      success: true,
      data: {
        date_range: {
          start_date: startDate,
          end_date: endDate
        },
        summary: {
          total_payments: totalPayments,
          total_amount: Math.round(totalAmount * 100) / 100,
          payment_methods_count: paymentMethods.length
        },
        payment_methods: processedMethods,
        monthly_trends: monthlyTrends.map(trend => ({
          month: trend.month,
          payment_method: trend.payment_method || 'Unknown',
          count: parseInt(trend.count),
          amount: parseFloat(trend.amount || 0)
        }))
      }
    })
  } catch (error) {
    console.error('Get payment methods error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching payment methods'
    })
  }
}

// GET /api/analytics/revenue-forecasting - Revenue forecasting
const getRevenueForecasting = async (req, res) => {
  try {
    const { 
      organization_id,
      forecast_months = 6,
      confidence_level = 0.8
    } = req.query

    // Get historical revenue data (last 24 months)
    const endDate = new Date()
    const startDate = new Date(endDate.getFullYear() - 2, endDate.getMonth(), endDate.getDate())

    const whereClause = {
      invoice_date: { [Op.between]: [startDate, endDate] },
      status: 'paid'
    }
    if (organization_id) whereClause.organization_id = organization_id

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

    for (let i = 1; i <= parseInt(forecast_months); i++) {
      const forecastDate = new Date()
      forecastDate.setMonth(forecastDate.getMonth() + i)
      const monthKey = `${forecastDate.getFullYear()}-${String(forecastDate.getMonth() + 1).padStart(2, '0')}`
      
      // Simple trend-based forecast
      const forecastedRevenue = Math.max(0, baseRevenue + (trend * i))
      
      // Add some seasonality (simplified)
      const seasonalityFactor = 1 + (0.1 * Math.sin((i * Math.PI) / 6)) // ±10% seasonal variation
      const adjustedRevenue = forecastedRevenue * seasonalityFactor

      forecast.push({
        month: monthKey,
        forecasted_revenue: Math.round(adjustedRevenue * 100) / 100,
        confidence_interval: {
          lower: Math.round(adjustedRevenue * (1 - parseFloat(confidence_level)) * 100) / 100,
          upper: Math.round(adjustedRevenue * (1 + parseFloat(confidence_level)) * 100) / 100
        },
        trend_factor: Math.round(trend * 100) / 100,
        seasonality_factor: Math.round(seasonalityFactor * 100) / 100
      })
    }

    // Calculate forecast accuracy metrics (if we have enough historical data)
    let accuracyMetrics = null
    if (processedData.length >= 6) {
      const recentData = processedData.slice(-6) // Last 6 months
      const avgRecentRevenue = recentData.reduce((sum, item) => sum + item.revenue, 0) / recentData.length
      const variance = recentData.reduce((sum, item) => sum + Math.pow(item.revenue - avgRecentRevenue, 2), 0) / recentData.length
      const standardDeviation = Math.sqrt(variance)
      
      accuracyMetrics = {
        historical_avg: Math.round(avgRecentRevenue * 100) / 100,
        standard_deviation: Math.round(standardDeviation * 100) / 100,
        coefficient_of_variation: Math.round((standardDeviation / avgRecentRevenue) * 100) / 100,
        confidence_level: parseFloat(confidence_level) * 100
      }
    }

    res.json({
      success: true,
      data: {
        forecast_period: parseInt(forecast_months),
        historical_data: processedData,
        forecast: forecast,
        trend_analysis: {
          trend: Math.round(trend * 100) / 100,
          trend_direction: trend > 0 ? 'increasing' : trend < 0 ? 'decreasing' : 'stable',
          base_revenue: Math.round(baseRevenue * 100) / 100
        },
        accuracy_metrics: accuracyMetrics
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

module.exports = {
  getRevenueTrends,
  getPaymentStatus,
  getOutstandingPayments,
  getBillingEfficiency,
  getPaymentMethods,
  getRevenueForecasting
}
