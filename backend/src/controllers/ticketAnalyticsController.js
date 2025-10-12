const { Ticket, Client, User, Organization } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')

// GET /api/tickets/analytics/volume - Ticket volume trends
const getTicketVolumeTrends = async (req, res) => {
  try {
    const { 
      organization_id,
      period = '30d', // 7d, 30d, 90d, 1y
      start_date,
      end_date
    } = req.query

    // Calculate date range based on period
    let dateRange = {}
    const now = new Date()
    
    if (start_date && end_date) {
      dateRange = {
        [Op.gte]: new Date(start_date),
        [Op.lte]: new Date(end_date)
      }
    } else {
      const days = period === '7d' ? 7 : period === '30d' ? 30 : period === '90d' ? 90 : 365
      dateRange = {
        [Op.gte]: new Date(now.getTime() - (days * 24 * 60 * 60 * 1000))
      }
    }

    // Build where clause
    const whereClause = {
      created_at: dateRange
    }
    if (organization_id) whereClause.organization_id = organization_id

    // Get ticket counts by day
    const tickets = await Ticket.findAll({
      where: whereClause,
      attributes: [
        [Ticket.sequelize.fn('DATE', Ticket.sequelize.col('created_at')), 'date'],
        [Ticket.sequelize.fn('COUNT', '*'), 'count']
      ],
      group: [Ticket.sequelize.fn('DATE', Ticket.sequelize.col('created_at'))],
      order: [[Ticket.sequelize.fn('DATE', Ticket.sequelize.col('created_at')), 'ASC']],
      raw: true
    })

    // Get total counts by status
    const statusCounts = await Ticket.findAll({
      where: whereClause,
      attributes: [
        'status',
        [Ticket.sequelize.fn('COUNT', '*'), 'count']
      ],
      group: ['status'],
      raw: true
    })

    // Get total counts by priority
    const priorityCounts = await Ticket.findAll({
      where: whereClause,
      attributes: [
        'priority',
        [Ticket.sequelize.fn('COUNT', '*'), 'count']
      ],
      group: ['priority'],
      raw: true
    })

    // Calculate totals
    const totalTickets = tickets.reduce((sum, ticket) => sum + parseInt(ticket.count), 0)
    const avgTicketsPerDay = tickets.length > 0 ? totalTickets / tickets.length : 0

    // Calculate trends (comparing first half vs second half of period)
    const midPoint = Math.floor(tickets.length / 2)
    const firstHalf = tickets.slice(0, midPoint).reduce((sum, ticket) => sum + parseInt(ticket.count), 0)
    const secondHalf = tickets.slice(midPoint).reduce((sum, ticket) => sum + parseInt(ticket.count), 0)
    const trend = firstHalf > 0 ? ((secondHalf - firstHalf) / firstHalf * 100) : 0

    res.json({
      success: true,
      data: {
        period,
        date_range: {
          start: dateRange[Op.gte] || start_date,
          end: dateRange[Op.lte] || end_date || now
        },
        volume_trends: {
          daily_counts: tickets,
          total_tickets: totalTickets,
          avg_tickets_per_day: Math.round(avgTicketsPerDay * 100) / 100,
          trend_percentage: Math.round(trend * 100) / 100,
          trend_direction: trend > 0 ? 'increasing' : trend < 0 ? 'decreasing' : 'stable'
        },
        status_breakdown: statusCounts,
        priority_breakdown: priorityCounts
      }
    })
  } catch (error) {
    console.error('Get ticket volume trends error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching ticket volume trends'
    })
  }
}

// GET /api/tickets/analytics/resolution-time - Resolution time analytics
const getResolutionTimeAnalytics = async (req, res) => {
  try {
    const { 
      organization_id,
      period = '30d',
      start_date,
      end_date
    } = req.query

    // Calculate date range
    let dateRange = {}
    const now = new Date()
    
    if (start_date && end_date) {
      dateRange = {
        [Op.gte]: new Date(start_date),
        [Op.lte]: new Date(end_date)
      }
    } else {
      const days = period === '7d' ? 7 : period === '30d' ? 30 : period === '90d' ? 90 : 365
      dateRange = {
        [Op.gte]: new Date(now.getTime() - (days * 24 * 60 * 60 * 1000))
      }
    }

    // Build where clause for resolved tickets
    const whereClause = {
      created_at: dateRange,
      status: { [Op.in]: ['resolved', 'closed'] },
      resolved_at: { [Op.ne]: null }
    }
    if (organization_id) whereClause.organization_id = organization_id

    // Get resolution time data
    const resolvedTickets = await Ticket.findAll({
      where: whereClause,
      attributes: [
        'id',
        'created_at',
        'resolved_at',
        'priority',
        'category',
        'assigned_to'
      ]
    })

    // Calculate resolution times in hours
    const resolutionTimes = resolvedTickets.map(ticket => {
      const created = new Date(ticket.created_at)
      const resolved = new Date(ticket.resolved_at)
      const hours = (resolved - created) / (1000 * 60 * 60)
      return {
        ticket_id: ticket.id,
        hours: hours,
        priority: ticket.priority,
        category: ticket.category,
        technician: ticket.assigned_to ? 'Assigned' : 'Unassigned'
      }
    })

    // Calculate statistics
    const times = resolutionTimes.map(rt => rt.hours)
    const avgResolutionTime = times.length > 0 ? times.reduce((sum, time) => sum + time, 0) / times.length : 0
    const minResolutionTime = times.length > 0 ? Math.min(...times) : 0
    const maxResolutionTime = times.length > 0 ? Math.max(...times) : 0
    const medianResolutionTime = times.length > 0 ? times.sort((a, b) => a - b)[Math.floor(times.length / 2)] : 0

    // Group by priority
    const priorityStats = {}
    resolutionTimes.forEach(rt => {
      if (!priorityStats[rt.priority]) {
        priorityStats[rt.priority] = []
      }
      priorityStats[rt.priority].push(rt.hours)
    })

    const priorityAnalytics = Object.keys(priorityStats).map(priority => {
      const times = priorityStats[priority]
      return {
        priority,
        count: times.length,
        avg_hours: times.reduce((sum, time) => sum + time, 0) / times.length,
        min_hours: Math.min(...times),
        max_hours: Math.max(...times)
      }
    })

    // Group by category
    const categoryStats = {}
    resolutionTimes.forEach(rt => {
      if (!categoryStats[rt.category]) {
        categoryStats[rt.category] = []
      }
      categoryStats[rt.category].push(rt.hours)
    })

    const categoryAnalytics = Object.keys(categoryStats).map(category => {
      const times = categoryStats[category]
      return {
        category,
        count: times.length,
        avg_hours: times.reduce((sum, time) => sum + time, 0) / times.length,
        min_hours: Math.min(...times),
        max_hours: Math.max(...times)
      }
    })

    res.json({
      success: true,
      data: {
        period,
        date_range: {
          start: dateRange[Op.gte] || start_date,
          end: dateRange[Op.lte] || end_date || now
        },
        resolution_analytics: {
          total_resolved: resolvedTickets.length,
          avg_resolution_time_hours: Math.round(avgResolutionTime * 100) / 100,
          min_resolution_time_hours: Math.round(minResolutionTime * 100) / 100,
          max_resolution_time_hours: Math.round(maxResolutionTime * 100) / 100,
          median_resolution_time_hours: Math.round(medianResolutionTime * 100) / 100
        },
        priority_breakdown: priorityAnalytics,
        category_breakdown: categoryAnalytics,
        resolution_times: resolutionTimes
      }
    })
  } catch (error) {
    console.error('Get resolution time analytics error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching resolution time analytics'
    })
  }
}

// GET /api/tickets/analytics/categories - Category breakdown
const getCategoryBreakdown = async (req, res) => {
  try {
    const { 
      organization_id,
      period = '30d',
      start_date,
      end_date
    } = req.query

    // Calculate date range
    let dateRange = {}
    const now = new Date()
    
    if (start_date && end_date) {
      dateRange = {
        [Op.gte]: new Date(start_date),
        [Op.lte]: new Date(end_date)
      }
    } else {
      const days = period === '7d' ? 7 : period === '30d' ? 30 : period === '90d' ? 90 : 365
      dateRange = {
        [Op.gte]: new Date(now.getTime() - (days * 24 * 60 * 60 * 1000))
      }
    }

    // Build where clause
    const whereClause = {
      created_at: dateRange
    }
    if (organization_id) whereClause.organization_id = organization_id

    // Get category breakdown
    const categoryStats = await Ticket.findAll({
      where: whereClause,
      attributes: [
        'category',
        [Ticket.sequelize.fn('COUNT', '*'), 'count'],
        [Ticket.sequelize.fn('AVG', Ticket.sequelize.col('time_spent')), 'avg_time_spent']
      ],
      group: ['category'],
      order: [[Ticket.sequelize.fn('COUNT', '*'), 'DESC']],
      raw: true
    })

    // Get status breakdown by category
    const statusByCategory = await Ticket.findAll({
      where: whereClause,
      attributes: [
        'category',
        'status',
        [Ticket.sequelize.fn('COUNT', '*'), 'count']
      ],
      group: ['category', 'status'],
      raw: true
    })

    // Get priority breakdown by category
    const priorityByCategory = await Ticket.findAll({
      where: whereClause,
      attributes: [
        'category',
        'priority',
        [Ticket.sequelize.fn('COUNT', '*'), 'count']
      ],
      group: ['category', 'priority'],
      raw: true
    })

    // Calculate totals and percentages
    const totalTickets = categoryStats.reduce((sum, cat) => sum + parseInt(cat.count), 0)
    
    const categoryBreakdown = categoryStats.map(cat => {
      const percentage = totalTickets > 0 ? (parseInt(cat.count) / totalTickets * 100) : 0
      return {
        category: cat.category || 'Uncategorized',
        count: parseInt(cat.count),
        percentage: Math.round(percentage * 100) / 100,
        avg_time_spent: parseFloat(cat.avg_time_spent) || 0
      }
    })

    res.json({
      success: true,
      data: {
        period,
        date_range: {
          start: dateRange[Op.gte] || start_date,
          end: dateRange[Op.lte] || end_date || now
        },
        category_breakdown: categoryBreakdown,
        status_by_category: statusByCategory,
        priority_by_category: priorityByCategory,
        total_tickets: totalTickets
      }
    })
  } catch (error) {
    console.error('Get category breakdown error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching category breakdown'
    })
  }
}

// GET /api/tickets/analytics/technician-performance - Technician metrics
const getTechnicianPerformance = async (req, res) => {
  try {
    const { 
      organization_id,
      period = '30d',
      start_date,
      end_date
    } = req.query

    // Calculate date range
    let dateRange = {}
    const now = new Date()
    
    if (start_date && end_date) {
      dateRange = {
        [Op.gte]: new Date(start_date),
        [Op.lte]: new Date(end_date)
      }
    } else {
      const days = period === '7d' ? 7 : period === '30d' ? 30 : period === '90d' ? 90 : 365
      dateRange = {
        [Op.gte]: new Date(now.getTime() - (days * 24 * 60 * 60 * 1000))
      }
    }

    // Build where clause
    const whereClause = {
      created_at: dateRange,
      assigned_to: { [Op.ne]: null }
    }
    if (organization_id) whereClause.organization_id = organization_id

    // Get technician performance data
    const technicianStats = await Ticket.findAll({
      where: whereClause,
      attributes: [
        'assigned_to',
        [Ticket.sequelize.fn('COUNT', '*'), 'total_tickets'],
        [Ticket.sequelize.fn('SUM', Ticket.sequelize.col('time_spent')), 'total_time_spent'],
        [Ticket.sequelize.fn('AVG', Ticket.sequelize.col('time_spent')), 'avg_time_per_ticket']
      ],
      group: ['assigned_to'],
      order: [[Ticket.sequelize.fn('COUNT', '*'), 'DESC']],
      raw: true
    })

    // Get resolution rates by technician
    const resolutionStats = await Ticket.findAll({
      where: whereClause,
      attributes: [
        'assigned_to',
        'status',
        [Ticket.sequelize.fn('COUNT', '*'), 'count']
      ],
      group: ['assigned_to', 'status'],
      raw: true
    })

    // Calculate performance metrics
    const technicianPerformance = technicianStats.map(tech => {
      const technicianId = tech.assigned_to
      const resolved = resolutionStats
        .filter(rs => rs.assigned_to === technicianId && ['resolved', 'closed'].includes(rs.status))
        .reduce((sum, rs) => sum + parseInt(rs.count), 0)
      const total = resolutionStats
        .filter(rs => rs.assigned_to === technicianId)
        .reduce((sum, rs) => sum + parseInt(rs.count), 0)
      
      const resolutionRate = total > 0 ? (resolved / total * 100) : 0
      
      return {
        technician_id: technicianId,
        name: 'Technician',
        email: 'technician@example.com',
        role: 'technician',
        total_tickets: parseInt(tech.total_tickets),
        total_time_spent: parseFloat(tech.total_time_spent) || 0,
        avg_time_per_ticket: parseFloat(tech.avg_time_per_ticket) || 0,
        resolution_rate: Math.round(resolutionRate * 100) / 100,
        tickets_resolved: resolved,
        tickets_total: total
      }
    })

    res.json({
      success: true,
      data: {
        period,
        date_range: {
          start: dateRange[Op.gte] || start_date,
          end: dateRange[Op.lte] || end_date || now
        },
        technician_performance: technicianPerformance,
        summary: {
          total_technicians: technicianPerformance.length,
          avg_tickets_per_technician: technicianPerformance.length > 0 
            ? technicianPerformance.reduce((sum, tech) => sum + tech.total_tickets, 0) / technicianPerformance.length 
            : 0,
          avg_resolution_rate: technicianPerformance.length > 0
            ? technicianPerformance.reduce((sum, tech) => sum + tech.resolution_rate, 0) / technicianPerformance.length
            : 0
        }
      }
    })
  } catch (error) {
    console.error('Get technician performance error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching technician performance'
    })
  }
}

// GET /api/tickets/analytics/sla-compliance - SLA compliance
const getSLACompliance = async (req, res) => {
  try {
    const { 
      organization_id,
      period = '30d',
      start_date,
      end_date
    } = req.query

    // Calculate date range
    let dateRange = {}
    const now = new Date()
    
    if (start_date && end_date) {
      dateRange = {
        [Op.gte]: new Date(start_date),
        [Op.lte]: new Date(end_date)
      }
    } else {
      const days = period === '7d' ? 7 : period === '30d' ? 30 : period === '90d' ? 90 : 365
      dateRange = {
        [Op.gte]: new Date(now.getTime() - (days * 24 * 60 * 60 * 1000))
      }
    }

    // Build where clause
    const whereClause = {
      created_at: dateRange
    }
    if (organization_id) whereClause.organization_id = organization_id

    // Define SLA targets (in hours)
    const slaTargets = {
      critical: 4,    // 4 hours
      urgent: 8,      // 8 hours
      high: 24,       // 24 hours
      medium: 72,     // 72 hours
      low: 168        // 168 hours (7 days)
    }

    // Get all tickets with resolution data
    const tickets = await Ticket.findAll({
      where: whereClause,
      attributes: [
        'id',
        'priority',
        'status',
        'created_at',
        'resolved_at',
        'assigned_to'
      ]
    })

    // Calculate SLA compliance
    const slaAnalysis = tickets.map(ticket => {
      const created = new Date(ticket.created_at)
      const resolved = ticket.resolved_at ? new Date(ticket.resolved_at) : now
      const hoursToResolve = (resolved - created) / (1000 * 60 * 60)
      const slaTarget = slaTargets[ticket.priority] || slaTargets.medium
      const isCompliant = hoursToResolve <= slaTarget
      
      return {
        ticket_id: ticket.id,
        priority: ticket.priority,
        status: ticket.status,
        sla_target_hours: slaTarget,
        actual_hours: Math.round(hoursToResolve * 100) / 100,
        is_compliant: isCompliant,
        technician: ticket.assigned_to ? 'Assigned' : 'Unassigned'
      }
    })

    // Calculate compliance rates by priority
    const priorityCompliance = {}
    slaAnalysis.forEach(analysis => {
      if (!priorityCompliance[analysis.priority]) {
        priorityCompliance[analysis.priority] = {
          total: 0,
          compliant: 0,
          sla_target: analysis.sla_target_hours
        }
      }
      priorityCompliance[analysis.priority].total++
      if (analysis.is_compliant) {
        priorityCompliance[analysis.priority].compliant++
      }
    })

    const complianceRates = Object.keys(priorityCompliance).map(priority => {
      const data = priorityCompliance[priority]
      const complianceRate = data.total > 0 ? (data.compliant / data.total * 100) : 0
      return {
        priority,
        sla_target_hours: data.sla_target,
        total_tickets: data.total,
        compliant_tickets: data.compliant,
        compliance_rate: Math.round(complianceRate * 100) / 100
      }
    })

    // Overall compliance
    const totalTickets = slaAnalysis.length
    const compliantTickets = slaAnalysis.filter(a => a.is_compliant).length
    const overallComplianceRate = totalTickets > 0 ? (compliantTickets / totalTickets * 100) : 0

    res.json({
      success: true,
      data: {
        period,
        date_range: {
          start: dateRange[Op.gte] || start_date,
          end: dateRange[Op.lte] || end_date || now
        },
        sla_targets: slaTargets,
        overall_compliance: {
          total_tickets: totalTickets,
          compliant_tickets: compliantTickets,
          compliance_rate: Math.round(overallComplianceRate * 100) / 100
        },
        compliance_by_priority: complianceRates,
        sla_analysis: slaAnalysis
      }
    })
  } catch (error) {
    console.error('Get SLA compliance error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching SLA compliance'
    })
  }
}

// GET /api/tickets/analytics/satisfaction - Customer satisfaction
const getCustomerSatisfaction = async (req, res) => {
  try {
    const { 
      organization_id,
      period = '30d',
      start_date,
      end_date
    } = req.query

    // Calculate date range
    let dateRange = {}
    const now = new Date()
    
    if (start_date && end_date) {
      dateRange = {
        [Op.gte]: new Date(start_date),
        [Op.lte]: new Date(end_date)
      }
    } else {
      const days = period === '7d' ? 7 : period === '30d' ? 30 : period === '90d' ? 90 : 365
      dateRange = {
        [Op.gte]: new Date(now.getTime() - (days * 24 * 60 * 60 * 1000))
      }
    }

    // Build where clause for resolved tickets
    const whereClause = {
      created_at: dateRange,
      status: { [Op.in]: ['resolved', 'closed'] }
    }
    if (organization_id) whereClause.organization_id = organization_id

    // Get resolved tickets with client information
    const resolvedTickets = await Ticket.findAll({
      where: whereClause,
      attributes: [
        'id',
        'priority',
        'category',
        'created_at',
        'resolved_at',
        'time_spent',
        'assigned_to',
        'client_id'
      ],
      include: [
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company']
        }
      ]
    })

    // Simulate satisfaction scores based on resolution time and other factors
    // In a real application, this would come from actual customer feedback
    const satisfactionData = resolvedTickets.map(ticket => {
      const created = new Date(ticket.created_at)
      const resolved = new Date(ticket.resolved_at)
      const hoursToResolve = (resolved - created) / (1000 * 60 * 60)
      
      // Calculate satisfaction score based on resolution time and priority
      let baseScore = 5 // Start with 5/5
      
      // Penalize for long resolution times
      if (hoursToResolve > 72) baseScore -= 2
      else if (hoursToResolve > 24) baseScore -= 1
      else if (hoursToResolve > 8) baseScore -= 0.5
      
      // Bonus for quick resolution of high priority tickets
      if (ticket.priority === 'critical' && hoursToResolve <= 4) baseScore += 0.5
      if (ticket.priority === 'urgent' && hoursToResolve <= 8) baseScore += 0.5
      
      // Random variation to simulate real feedback
      const variation = (Math.random() - 0.5) * 0.5
      const satisfactionScore = Math.max(1, Math.min(5, baseScore + variation))
      
      return {
        ticket_id: ticket.id,
        client_name: ticket.client.name,
        client_company: ticket.client.company,
        priority: ticket.priority,
        category: ticket.category,
        resolution_time_hours: Math.round(hoursToResolve * 100) / 100,
        time_spent: parseFloat(ticket.time_spent) || 0,
        satisfaction_score: Math.round(satisfactionScore * 100) / 100,
        technician: ticket.assigned_to ? 'Assigned' : 'Unassigned'
      }
    })

    // Calculate satisfaction statistics
    const scores = satisfactionData.map(sd => sd.satisfaction_score)
    const avgSatisfaction = scores.length > 0 ? scores.reduce((sum, score) => sum + score, 0) / scores.length : 0
    
    // Categorize satisfaction levels
    const satisfactionLevels = {
      excellent: satisfactionData.filter(sd => sd.satisfaction_score >= 4.5).length,
      good: satisfactionData.filter(sd => sd.satisfaction_score >= 3.5 && sd.satisfaction_score < 4.5).length,
      average: satisfactionData.filter(sd => sd.satisfaction_score >= 2.5 && sd.satisfaction_score < 3.5).length,
      poor: satisfactionData.filter(sd => sd.satisfaction_score < 2.5).length
    }

    // Satisfaction by priority
    const satisfactionByPriority = {}
    satisfactionData.forEach(sd => {
      if (!satisfactionByPriority[sd.priority]) {
        satisfactionByPriority[sd.priority] = []
      }
      satisfactionByPriority[sd.priority].push(sd.satisfaction_score)
    })

    const prioritySatisfaction = Object.keys(satisfactionByPriority).map(priority => {
      const scores = satisfactionByPriority[priority]
      return {
        priority,
        count: scores.length,
        avg_satisfaction: scores.reduce((sum, score) => sum + score, 0) / scores.length
      }
    })

    res.json({
      success: true,
      data: {
        period,
        date_range: {
          start: dateRange[Op.gte] || start_date,
          end: dateRange[Op.lte] || end_date || now
        },
        satisfaction_analytics: {
          total_resolved_tickets: resolvedTickets.length,
          avg_satisfaction_score: Math.round(avgSatisfaction * 100) / 100,
          satisfaction_levels: satisfactionLevels,
          satisfaction_distribution: {
            excellent_percentage: Math.round((satisfactionLevels.excellent / resolvedTickets.length) * 100),
            good_percentage: Math.round((satisfactionLevels.good / resolvedTickets.length) * 100),
            average_percentage: Math.round((satisfactionLevels.average / resolvedTickets.length) * 100),
            poor_percentage: Math.round((satisfactionLevels.poor / resolvedTickets.length) * 100)
          }
        },
        satisfaction_by_priority: prioritySatisfaction,
        detailed_satisfaction: satisfactionData
      }
    })
  } catch (error) {
    console.error('Get customer satisfaction error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching customer satisfaction'
    })
  }
}

module.exports = {
  getTicketVolumeTrends,
  getResolutionTimeAnalytics,
  getCategoryBreakdown,
  getTechnicianPerformance,
  getSLACompliance,
  getCustomerSatisfaction
}
