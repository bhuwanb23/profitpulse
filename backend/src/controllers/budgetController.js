const { Budget, Expense, Organization, User } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')

// GET /api/budgets - List budgets
const getBudgets = async (req, res) => {
  try {
    const { 
      page = 1, 
      limit = 10, 
      search, 
      budget_type,
      organization_id,
      is_active,
      start_date,
      end_date,
      sort_by = 'created_at',
      sort_order = 'DESC'
    } = req.query
    const offset = (page - 1) * limit

    // Build where clause
    const whereClause = {}
    if (search) {
      whereClause[Op.or] = [
        { name: { [Op.iLike]: `%${search}%` } },
        { description: { [Op.iLike]: `%${search}%` } }
      ]
    }
    if (budget_type) whereClause.budget_type = budget_type
    if (organization_id) whereClause.organization_id = organization_id
    if (is_active !== undefined) whereClause.is_active = is_active === 'true'
    
    // Date range filtering
    if (start_date || end_date) {
      whereClause.start_date = {}
      if (start_date) whereClause.start_date[Op.gte] = new Date(start_date)
      if (end_date) whereClause.start_date[Op.lte] = new Date(end_date)
    }

    // Build order clause
    const orderClause = [[sort_by, sort_order.toUpperCase()]]

    const { count, rows: budgets } = await Budget.findAndCountAll({
      where: whereClause,
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        }
      ],
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: orderClause
    })

    // Calculate budget utilization for each budget
    const budgetsWithUtilization = await Promise.all(budgets.map(async (budget) => {
      const expenses = await Expense.findAll({
        where: {
          budget_id: budget.id,
          expense_date: { [Op.between]: [budget.start_date, budget.end_date] }
        },
        attributes: [
          [Expense.sequelize.fn('SUM', Expense.sequelize.col('amount')), 'total_spent']
        ],
        raw: true
      })

      const totalSpent = parseFloat(expenses[0]?.total_spent || 0)
      const utilizationPercentage = budget.total_amount > 0 ? 
        (totalSpent / parseFloat(budget.total_amount)) * 100 : 0

      return {
        ...budget.toJSON(),
        utilization: {
          total_spent: totalSpent,
          remaining_amount: parseFloat(budget.total_amount) - totalSpent,
          utilization_percentage: Math.round(utilizationPercentage * 100) / 100,
          is_over_budget: totalSpent > parseFloat(budget.total_amount)
        }
      }
    }))

    res.json({
      success: true,
      data: {
        budgets: budgetsWithUtilization,
        pagination: {
          total: count,
          page: parseInt(page),
          limit: parseInt(limit),
          pages: Math.ceil(count / limit)
        }
      }
    })
  } catch (error) {
    console.error('Get budgets error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching budgets'
    })
  }
}

// POST /api/budgets - Create budget
const createBudget = async (req, res) => {
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
      organization_id,
      name,
      description,
      budget_type,
      total_amount,
      start_date,
      end_date,
      categories = [],
      alert_thresholds = {},
      created_by,
      notes
    } = req.body

    // Check if organization exists
    const organization = await Organization.findByPk(organization_id)
    if (!organization) {
      return res.status(400).json({
        success: false,
        message: 'Organization not found'
      })
    }

    // Validate date range
    const startDate = new Date(start_date)
    const endDate = new Date(end_date)
    if (startDate >= endDate) {
      return res.status(400).json({
        success: false,
        message: 'Start date must be before end date'
      })
    }

    const budget = await Budget.create({
      organization_id,
      name,
      description,
      budget_type,
      total_amount: parseFloat(total_amount),
      start_date: startDate,
      end_date: endDate,
      categories,
      alert_thresholds,
      created_by,
      notes,
      is_active: true
    })

    // Fetch the created budget with associations
    const createdBudget = await Budget.findByPk(budget.id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        }
      ]
    })

    res.status(201).json({
      success: true,
      message: 'Budget created successfully',
      data: { budget: createdBudget }
    })
  } catch (error) {
    console.error('Create budget error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while creating budget'
    })
  }
}

// GET /api/budgets/:id - Get budget details
const getBudgetById = async (req, res) => {
  try {
    const { id } = req.params

    const budget = await Budget.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        }
      ]
    })

    if (!budget) {
      return res.status(404).json({
        success: false,
        message: 'Budget not found'
      })
    }

    // Get expenses for this budget
    const expenses = await Expense.findAll({
      where: {
        budget_id: id,
        expense_date: { [Op.between]: [budget.start_date, budget.end_date] }
      },
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name']
        }
      ],
      order: [['expense_date', 'DESC']]
    })

    // Calculate budget utilization
    const totalSpent = expenses.reduce((sum, expense) => sum + parseFloat(expense.amount), 0)
    const utilizationPercentage = budget.total_amount > 0 ? 
      (totalSpent / parseFloat(budget.total_amount)) * 100 : 0

    res.json({
      success: true,
      data: {
        budget,
        expenses,
        utilization: {
          total_spent: totalSpent,
          remaining_amount: parseFloat(budget.total_amount) - totalSpent,
          utilization_percentage: Math.round(utilizationPercentage * 100) / 100,
          is_over_budget: totalSpent > parseFloat(budget.total_amount)
        }
      }
    })
  } catch (error) {
    console.error('Get budget by ID error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching budget'
    })
  }
}

// PUT /api/budgets/:id - Update budget
const updateBudget = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const { id } = req.params
    const updateData = req.body

    const budget = await Budget.findByPk(id)
    if (!budget) {
      return res.status(404).json({
        success: false,
        message: 'Budget not found'
      })
    }

    // Validate date range if dates are being updated
    if (updateData.start_date || updateData.end_date) {
      const startDate = new Date(updateData.start_date || budget.start_date)
      const endDate = new Date(updateData.end_date || budget.end_date)
      if (startDate >= endDate) {
        return res.status(400).json({
          success: false,
          message: 'Start date must be before end date'
        })
      }
    }

    // Update budget
    await budget.update(updateData)

    // Fetch updated budget with associations
    const updatedBudget = await Budget.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        }
      ]
    })

    res.json({
      success: true,
      message: 'Budget updated successfully',
      data: { budget: updatedBudget }
    })
  } catch (error) {
    console.error('Update budget error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while updating budget'
    })
  }
}

// DELETE /api/budgets/:id - Delete budget
const deleteBudget = async (req, res) => {
  try {
    const { id } = req.params

    const budget = await Budget.findByPk(id)
    if (!budget) {
      return res.status(404).json({
        success: false,
        message: 'Budget not found'
      })
    }

    // Check if budget has expenses
    const expenseCount = await Expense.count({
      where: { budget_id: id }
    })

    if (expenseCount > 0) {
      return res.status(400).json({
        success: false,
        message: 'Cannot delete budget with existing expenses. Please remove expenses first.'
      })
    }

    await budget.destroy()

    res.json({
      success: true,
      message: 'Budget deleted successfully'
    })
  } catch (error) {
    console.error('Delete budget error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while deleting budget'
    })
  }
}

// GET /api/budgets/:id/categories - Budget categories
const getBudgetCategories = async (req, res) => {
  try {
    const { id } = req.params

    const budget = await Budget.findByPk(id)
    if (!budget) {
      return res.status(404).json({
        success: false,
        message: 'Budget not found'
      })
    }

    const categories = budget.categories || []
    
    // Get expenses for each category to calculate spent amounts
    const categoryAnalysis = await Promise.all(categories.map(async (category) => {
      const expenses = await Expense.findAll({
        where: {
          budget_id: id,
          category: category.name,
          expense_date: { [Op.between]: [budget.start_date, budget.end_date] }
        },
        attributes: [
          [Expense.sequelize.fn('SUM', Expense.sequelize.col('amount')), 'total_spent'],
          [Expense.sequelize.fn('COUNT', Expense.sequelize.col('id')), 'expense_count']
        ],
        raw: true
      })

      const totalSpent = parseFloat(expenses[0]?.total_spent || 0)
      const expenseCount = parseInt(expenses[0]?.expense_count || 0)
      const utilizationPercentage = category.amount > 0 ? 
        (totalSpent / parseFloat(category.amount)) * 100 : 0

      return {
        ...category,
        spent_amount: totalSpent,
        remaining_amount: parseFloat(category.amount) - totalSpent,
        utilization_percentage: Math.round(utilizationPercentage * 100) / 100,
        expense_count: expenseCount,
        is_over_budget: totalSpent > parseFloat(category.amount)
      }
    }))

    res.json({
      success: true,
      data: {
        budget_id: id,
        budget_name: budget.name,
        categories: categoryAnalysis
      }
    })
  } catch (error) {
    console.error('Get budget categories error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching budget categories'
    })
  }
}

// POST /api/budgets/:id/categories - Add category
const addBudgetCategory = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const { id } = req.params
    const { name, amount, description } = req.body

    const budget = await Budget.findByPk(id)
    if (!budget) {
      return res.status(404).json({
        success: false,
        message: 'Budget not found'
      })
    }

    // Get existing categories
    const existingCategories = budget.categories || []
    
    // Check if category already exists
    const categoryExists = existingCategories.some(cat => cat.name === name)
    if (categoryExists) {
      return res.status(400).json({
        success: false,
        message: 'Category with this name already exists'
      })
    }

    // Add new category
    const newCategory = {
      name,
      amount: parseFloat(amount),
      description: description || '',
      created_at: new Date().toISOString()
    }

    const updatedCategories = [...existingCategories, newCategory]
    
    // Update budget with new categories
    await budget.update({ categories: updatedCategories })

    res.json({
      success: true,
      message: 'Category added successfully',
      data: {
        category: newCategory,
        total_categories: updatedCategories.length
      }
    })
  } catch (error) {
    console.error('Add budget category error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while adding budget category'
    })
  }
}

// GET /api/budgets/:id/expenses - Budget expenses
const getBudgetExpenses = async (req, res) => {
  try {
    const { id } = req.params
    const { 
      page = 1, 
      limit = 10, 
      category,
      start_date,
      end_date,
      sort_by = 'expense_date',
      sort_order = 'DESC'
    } = req.query
    const offset = (page - 1) * limit

    const budget = await Budget.findByPk(id)
    if (!budget) {
      return res.status(404).json({
        success: false,
        message: 'Budget not found'
      })
    }

    // Build where clause
    const whereClause = {
      budget_id: id
    }
    if (category) whereClause.category = category
    
    // Date range filtering
    if (start_date || end_date) {
      whereClause.expense_date = {}
      if (start_date) whereClause.expense_date[Op.gte] = new Date(start_date)
      if (end_date) whereClause.expense_date[Op.lte] = new Date(end_date)
    } else {
      // Default to budget date range
      whereClause.expense_date = { [Op.between]: [budget.start_date, budget.end_date] }
    }

    // Build order clause
    const orderClause = [[sort_by, sort_order.toUpperCase()]]

    const { count, rows: expenses } = await Expense.findAndCountAll({
      where: whereClause,
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name']
        }
      ],
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: orderClause
    })

    // Calculate summary statistics
    const totalExpenses = expenses.reduce((sum, expense) => sum + parseFloat(expense.amount), 0)
    const categoryBreakdown = {}
    expenses.forEach(expense => {
      const cat = expense.category || 'Uncategorized'
      if (!categoryBreakdown[cat]) {
        categoryBreakdown[cat] = { count: 0, total: 0 }
      }
      categoryBreakdown[cat].count++
      categoryBreakdown[cat].total += parseFloat(expense.amount)
    })

    res.json({
      success: true,
      data: {
        budget_id: id,
        budget_name: budget.name,
        summary: {
          total_expenses: expenses.length,
          total_amount: Math.round(totalExpenses * 100) / 100,
          remaining_budget: Math.round((parseFloat(budget.total_amount) - totalExpenses) * 100) / 100
        },
        category_breakdown: categoryBreakdown,
        expenses,
        pagination: {
          total: count,
          page: parseInt(page),
          limit: parseInt(limit),
          pages: Math.ceil(count / limit)
        }
      }
    })
  } catch (error) {
    console.error('Get budget expenses error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching budget expenses'
    })
  }
}

// GET /api/budgets/:id/alerts - Budget alerts
const getBudgetAlerts = async (req, res) => {
  try {
    const { id } = req.params

    const budget = await Budget.findByPk(id)
    if (!budget) {
      return res.status(404).json({
        success: false,
        message: 'Budget not found'
      })
    }

    // Get current expenses
    const expenses = await Expense.findAll({
      where: {
        budget_id: id,
        expense_date: { [Op.between]: [budget.start_date, budget.end_date] }
      },
      attributes: [
        [Expense.sequelize.fn('SUM', Expense.sequelize.col('amount')), 'total_spent']
      ],
      raw: true
    })

    const totalSpent = parseFloat(expenses[0]?.total_spent || 0)
    const totalBudget = parseFloat(budget.total_amount)
    const utilizationPercentage = (totalSpent / totalBudget) * 100

    // Generate alerts based on thresholds
    const alerts = []
    const alertThresholds = budget.alert_thresholds || {}

    // Budget utilization alerts
    if (utilizationPercentage >= (alertThresholds.utilization_warning || 80)) {
      alerts.push({
        type: 'utilization_warning',
        severity: utilizationPercentage >= (alertThresholds.utilization_critical || 95) ? 'critical' : 'warning',
        message: `Budget utilization is at ${Math.round(utilizationPercentage * 100) / 100}%`,
        current_value: Math.round(utilizationPercentage * 100) / 100,
        threshold: alertThresholds.utilization_warning || 80,
        recommendation: utilizationPercentage >= 100 ? 
          'Budget exceeded. Consider reviewing expenses or increasing budget.' :
          'Approaching budget limit. Monitor expenses closely.'
      })
    }

    // Over budget alert
    if (totalSpent > totalBudget) {
      alerts.push({
        type: 'over_budget',
        severity: 'critical',
        message: `Budget exceeded by $${Math.round((totalSpent - totalBudget) * 100) / 100}`,
        current_value: totalSpent,
        threshold: totalBudget,
        recommendation: 'Immediate action required. Review all expenses and consider budget adjustments.'
      })
    }

    // Category-specific alerts
    if (budget.categories && budget.categories.length > 0) {
      for (const category of budget.categories) {
        const categoryExpenses = await Expense.findAll({
          where: {
            budget_id: id,
            category: category.name,
            expense_date: { [Op.between]: [budget.start_date, budget.end_date] }
          },
          attributes: [
            [Expense.sequelize.fn('SUM', Expense.sequelize.col('amount')), 'total_spent']
          ],
          raw: true
        })

        const categorySpent = parseFloat(categoryExpenses[0]?.total_spent || 0)
        const categoryUtilization = (categorySpent / parseFloat(category.amount)) * 100

        if (categoryUtilization >= (alertThresholds.category_warning || 90)) {
          alerts.push({
            type: 'category_warning',
            severity: categoryUtilization >= 100 ? 'critical' : 'warning',
            message: `Category "${category.name}" utilization is at ${Math.round(categoryUtilization * 100) / 100}%`,
            current_value: Math.round(categoryUtilization * 100) / 100,
            threshold: alertThresholds.category_warning || 90,
            category: category.name,
            recommendation: categoryUtilization >= 100 ? 
              `Category "${category.name}" budget exceeded.` :
              `Category "${category.name}" approaching limit.`
          })
        }
      }
    }

    // Time-based alerts
    const now = new Date()
    const daysRemaining = Math.ceil((new Date(budget.end_date) - now) / (1000 * 60 * 60 * 24))
    const totalDays = Math.ceil((new Date(budget.end_date) - new Date(budget.start_date)) / (1000 * 60 * 60 * 24))
    const timeProgress = ((totalDays - daysRemaining) / totalDays) * 100

    if (daysRemaining <= (alertThresholds.time_warning_days || 7)) {
      alerts.push({
        type: 'time_warning',
        severity: daysRemaining <= 0 ? 'critical' : 'warning',
        message: `Budget period ends in ${daysRemaining} days`,
        current_value: daysRemaining,
        threshold: alertThresholds.time_warning_days || 7,
        recommendation: daysRemaining <= 0 ? 
          'Budget period has ended. Review final expenses.' :
          'Budget period ending soon. Complete pending expenses.'
      })
    }

    res.json({
      success: true,
      data: {
        budget_id: id,
        budget_name: budget.name,
        current_status: {
          total_budget: totalBudget,
          total_spent: Math.round(totalSpent * 100) / 100,
          remaining_amount: Math.round((totalBudget - totalSpent) * 100) / 100,
          utilization_percentage: Math.round(utilizationPercentage * 100) / 100,
          days_remaining: Math.max(0, daysRemaining),
          time_progress: Math.round(timeProgress * 100) / 100
        },
        alerts,
        alert_summary: {
          total_alerts: alerts.length,
          critical_alerts: alerts.filter(alert => alert.severity === 'critical').length,
          warning_alerts: alerts.filter(alert => alert.severity === 'warning').length
        }
      }
    })
  } catch (error) {
    console.error('Get budget alerts error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching budget alerts'
    })
  }
}

module.exports = {
  getBudgets,
  createBudget,
  getBudgetById,
  updateBudget,
  deleteBudget,
  getBudgetCategories,
  addBudgetCategory,
  getBudgetExpenses,
  getBudgetAlerts
}
