const express = require('express')
const router = express.Router()
const {
  getBudgets,
  createBudget,
  getBudgetById,
  updateBudget,
  deleteBudget,
  getBudgetCategories,
  addBudgetCategory,
  getBudgetExpenses,
  getBudgetAlerts
} = require('../controllers/budgetController')
const {
  getBudgetsValidation,
  createBudgetValidation,
  getBudgetByIdValidation,
  updateBudgetValidation,
  deleteBudgetValidation,
  getBudgetCategoriesValidation,
  addBudgetCategoryValidation,
  getBudgetExpensesValidation,
  getBudgetAlertsValidation
} = require('../validators/budgetValidator')

// GET /api/budgets - List budgets
router.get('/', 
  getBudgetsValidation,
  getBudgets
)

// POST /api/budgets - Create budget
router.post('/', 
  createBudgetValidation,
  createBudget
)

// GET /api/budgets/:id - Get budget details
router.get('/:id', 
  getBudgetByIdValidation,
  getBudgetById
)

// PUT /api/budgets/:id - Update budget
router.put('/:id', 
  updateBudgetValidation,
  updateBudget
)

// DELETE /api/budgets/:id - Delete budget
router.delete('/:id', 
  deleteBudgetValidation,
  deleteBudget
)

// GET /api/budgets/:id/categories - Budget categories
router.get('/:id/categories', 
  getBudgetCategoriesValidation,
  getBudgetCategories
)

// POST /api/budgets/:id/categories - Add category
router.post('/:id/categories', 
  addBudgetCategoryValidation,
  addBudgetCategory
)

// GET /api/budgets/:id/expenses - Budget expenses
router.get('/:id/expenses', 
  getBudgetExpensesValidation,
  getBudgetExpenses
)

// GET /api/budgets/:id/alerts - Budget alerts
router.get('/:id/alerts', 
  getBudgetAlertsValidation,
  getBudgetAlerts
)

module.exports = router