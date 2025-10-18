import { useMemo } from 'react'
import { KPICard } from '../components/clients/KPICard'
import { Button } from '../components/ui/Button'
import { 
	CurrencyDollarIcon,
	ChartBarIcon,
	TrendingUpIcon,
	TrendingDownIcon,
	ExclamationTriangleIcon,
	CalendarIcon,
	DocumentTextIcon,
	PlusIcon,
	RefreshIcon
} from '../components/ui/Icons'

import BudgetOverview from '../components/financial/budgets/BudgetOverview'
import BudgetCreate from '../components/financial/budgets/BudgetCreate'
import ExpenseCategorization from '../components/financial/budgets/ExpenseCategorization'
import BudgetVsActual from '../components/financial/budgets/BudgetVsActual'
import CostCenterManagement from '../components/financial/budgets/CostCenterManagement'
import BudgetAlerts from '../components/financial/budgets/BudgetAlerts'

export default function BudgetManagementPage() {
	// Budget analytics data
	const budgetData = useMemo(() => {
		return {
			totalBudget: 2450000,
			spentAmount: 1876500,
			remainingBudget: 573500,
			utilizationRate: 76.6,
			monthlyBurn: 156780,
			projectedOverrun: -23400,
			activeBudgets: 12,
			budgetVariance: -8.3,
			recentTransactions: [
				{ description: 'Office Supplies Purchase', amount: -2340, category: 'Operations', date: '2 hours ago', status: 'Approved' },
				{ description: 'Marketing Campaign Budget', amount: -15000, category: 'Marketing', date: '5 hours ago', status: 'Pending' },
				{ description: 'Software License Renewal', amount: -8900, category: 'Technology', date: '1 day ago', status: 'Approved' },
				{ description: 'Travel Expense Reimbursement', amount: -3200, category: 'Travel', date: '1 day ago', status: 'Processing' },
				{ description: 'Equipment Purchase', amount: -12500, category: 'Operations', date: '2 days ago', status: 'Approved' }
			],
			budgetsByCategory: [
				{ category: 'Operations', allocated: 850000, spent: 645000, percentage: 75.9, color: '#3b82f6' },
				{ category: 'Marketing', allocated: 450000, spent: 367000, percentage: 81.6, color: '#10b981' },
				{ category: 'Technology', allocated: 380000, spent: 298000, percentage: 78.4, color: '#f59e0b' },
				{ category: 'Travel', allocated: 220000, spent: 156000, percentage: 70.9, color: '#8b5cf6' },
				{ category: 'HR', allocated: 350000, spent: 285000, percentage: 81.4, color: '#ef4444' },
				{ category: 'Facilities', allocated: 200000, spent: 125500, percentage: 62.8, color: '#06b6d4' }
			]
		}
	}, [])

	const getStatusColor = (status) => {
		const colors = {
			'Approved': 'bg-green-100 text-green-800',
			'Pending': 'bg-yellow-100 text-yellow-800',
			'Processing': 'bg-blue-100 text-blue-800',
			'Rejected': 'bg-red-100 text-red-800'
		}
		return colors[status] || 'bg-gray-100 text-gray-800'
	}

	const formatCurrency = (amount) => {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD',
			minimumFractionDigits: 0,
			maximumFractionDigits: 0
		}).format(Math.abs(amount))
	}

	return (
		<div className="space-y-6">
			{/* Header */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 bg-clip-text text-transparent">
						💰 Budget Management
					</h1>
					<p className="text-gray-600 mt-1">Monitor budgets, track expenses, and manage financial allocations</p>
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<DocumentTextIcon className="h-4 w-4" />
						Export Report
					</Button>
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<CalendarIcon className="h-4 w-4" />
						Budget Calendar
					</Button>
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<PlusIcon className="h-4 w-4" />
						New Budget
					</Button>
					<Button variant="primary" size="sm" className="flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600">
						<RefreshIcon className="h-4 w-4" />
						Refresh Data
					</Button>
				</div>
			</div>

			{/* KPI Cards - Primary Metrics */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
				<KPICard
					title="Total Budget"
					value={budgetData.totalBudget}
					change={12.5}
					changeType="positive"
					format="currency"
					icon={CurrencyDollarIcon}
					iconColor="emerald"
				/>
				<KPICard
					title="Amount Spent"
					value={budgetData.spentAmount}
					change={8.7}
					changeType="neutral"
					format="currency"
					icon={TrendingUpIcon}
					iconColor="blue"
				/>
				<KPICard
					title="Remaining Budget"
					value={budgetData.remainingBudget}
					change={-15.2}
					changeType="negative"
					format="currency"
					icon={TrendingDownIcon}
					iconColor="orange"
				/>
				<KPICard
					title="Utilization Rate"
					value={budgetData.utilizationRate}
					change={5.3}
					changeType="neutral"
					format="decimal"
					icon={ChartBarIcon}
					iconColor="purple"
					suffix="%"
				/>
			</div>

			{/* KPI Cards - Secondary Metrics */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
				<KPICard
					title="Monthly Burn"
					value={budgetData.monthlyBurn}
					change={-3.8}
					changeType="positive"
					format="currency"
					icon={TrendingUpIcon}
					iconColor="teal"
				/>
				<KPICard
					title="Projected Variance"
					value={budgetData.projectedOverrun}
					change={-12.1}
					changeType="positive"
					format="currency"
					icon={ExclamationTriangleIcon}
					iconColor="red"
				/>
				<KPICard
					title="Active Budgets"
					value={budgetData.activeBudgets}
					change={2}
					changeType="positive"
					format="number"
					icon={DocumentTextIcon}
					iconColor="indigo"
				/>
				<KPICard
					title="Budget Variance"
					value={budgetData.budgetVariance}
					change={-4.2}
					changeType="positive"
					format="decimal"
					icon={ChartBarIcon}
					iconColor="rose"
					suffix="%"
				/>
			</div>

			{/* Main Content Grid */}
			<div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
				{/* Left Column - Budget Overview & Analysis */}
				<div className="xl:col-span-2 space-y-6">
					{/* Enhanced Budget Overview */}
					<div className="bg-gradient-to-br from-emerald-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent mb-4">
							💰 Budget Overview & Analysis
						</h2>
						
						<div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
							<div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
								<div className="text-2xl font-bold text-emerald-600">{formatCurrency(budgetData.totalBudget)}</div>
								<div className="text-sm text-gray-500">Total Allocated</div>
							</div>
							<div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
								<div className="text-2xl font-bold text-blue-600">{formatCurrency(budgetData.spentAmount)}</div>
								<div className="text-sm text-gray-500">Amount Spent</div>
							</div>
							<div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
								<div className="text-2xl font-bold text-orange-600">{formatCurrency(budgetData.remainingBudget)}</div>
								<div className="text-sm text-gray-500">Remaining</div>
							</div>
						</div>

						{/* Budget Progress */}
						<div className="bg-white rounded-lg border border-gray-200 p-4">
							<div className="flex items-center justify-between mb-2">
								<span className="text-sm font-medium text-gray-700">Overall Budget Utilization</span>
								<span className="text-sm font-semibold text-gray-900">{budgetData.utilizationRate}%</span>
							</div>
							<div className="w-full bg-gray-200 rounded-full h-3 mb-2">
								<div 
									className="h-3 rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-300" 
									style={{ width: `${budgetData.utilizationRate}%` }}
								></div>
							</div>
							<div className="flex justify-between text-xs text-gray-500">
								<span>Spent: {formatCurrency(budgetData.spentAmount)}</span>
								<span>Budget: {formatCurrency(budgetData.totalBudget)}</span>
							</div>
						</div>
					</div>

					{/* Enhanced Budget vs Actual */}
					<div className="bg-gradient-to-br from-blue-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
							📊 Budget vs Actual by Category
						</h2>
						
						<div className="space-y-4">
							{budgetData.budgetsByCategory.map((budget, index) => (
								<div key={index} className="bg-white rounded-lg border border-gray-200 p-4">
									<div className="flex items-center justify-between mb-3">
										<div className="flex items-center gap-3">
											<div className="w-4 h-4 rounded-full" style={{ backgroundColor: budget.color }}></div>
											<span className="font-medium text-gray-900">{budget.category}</span>
										</div>
										<div className="text-right">
											<div className="text-sm font-semibold text-gray-900">{budget.percentage.toFixed(1)}%</div>
											<div className={`text-xs ${budget.percentage > 80 ? 'text-red-600' : budget.percentage > 60 ? 'text-yellow-600' : 'text-green-600'}`}>
												{budget.percentage > 80 ? 'Over Budget' : budget.percentage > 60 ? 'On Track' : 'Under Budget'}
											</div>
										</div>
									</div>
									<div className="w-full bg-gray-200 rounded-full h-2 mb-3">
										<div 
											className="h-2 rounded-full transition-all duration-300" 
											style={{ 
												width: `${budget.percentage}%`, 
												backgroundColor: budget.color 
											}}
										></div>
									</div>
									<div className="grid grid-cols-3 gap-4 text-xs text-gray-500">
										<div>
											<div className="font-medium">Allocated</div>
											<div>{formatCurrency(budget.allocated)}</div>
										</div>
										<div>
											<div className="font-medium">Spent</div>
											<div>{formatCurrency(budget.spent)}</div>
										</div>
										<div>
											<div className="font-medium">Remaining</div>
											<div>{formatCurrency(budget.allocated - budget.spent)}</div>
										</div>
									</div>
								</div>
							))}
						</div>
					</div>

					{/* Enhanced Expense Categorization */}
					<div className="bg-gradient-to-br from-purple-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
							🏷️ Recent Transactions
						</h2>
						
						<div className="space-y-3 max-h-80 overflow-y-auto">
							{budgetData.recentTransactions.map((transaction, index) => (
								<div key={index} className="flex items-center justify-between p-4 bg-white rounded-lg border border-gray-200 hover:border-purple-300 transition-all hover:shadow-sm">
									<div className="flex items-center gap-3">
										<div className="flex-shrink-0">
											<div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center">
												<CurrencyDollarIcon className="h-4 w-4 text-purple-600" />
											</div>
										</div>
										<div className="flex-1">
											<p className="font-medium text-gray-900 text-sm">{transaction.description}</p>
											<p className="text-xs text-gray-500">{transaction.category} • {transaction.date}</p>
										</div>
									</div>
									<div className="text-right">
										<p className="font-semibold text-red-600 text-sm">{formatCurrency(transaction.amount)}</p>
										<span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(transaction.status)}`}>
											{transaction.status}
										</span>
									</div>
								</div>
							))}
						</div>
					</div>
				</div>

				{/* Right Column - Management & Alerts */}
				<div className="space-y-6">
					{/* Enhanced Budget Creation */}
					<div className="bg-gradient-to-br from-green-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent mb-4">
							➕ Create New Budget
						</h2>
						
						<div className="space-y-4">
							<div className="bg-white rounded-lg border border-gray-200 p-4">
								<label className="text-sm font-medium text-gray-700 mb-2 block">Budget Name</label>
								<input type="text" className="w-full p-2 border border-gray-300 rounded-lg text-sm" placeholder="Enter budget name" />
							</div>
							
							<div className="bg-white rounded-lg border border-gray-200 p-4">
								<label className="text-sm font-medium text-gray-700 mb-2 block">Category</label>
								<select className="w-full p-2 border border-gray-300 rounded-lg text-sm">
									<option>Operations</option>
									<option>Marketing</option>
									<option>Technology</option>
									<option>Travel</option>
									<option>HR</option>
									<option>Facilities</option>
								</select>
							</div>
							
							<div className="bg-white rounded-lg border border-gray-200 p-4">
								<label className="text-sm font-medium text-gray-700 mb-2 block">Amount</label>
								<input type="number" className="w-full p-2 border border-gray-300 rounded-lg text-sm" placeholder="0.00" />
							</div>
							
							<div className="bg-white rounded-lg border border-gray-200 p-4">
								<label className="text-sm font-medium text-gray-700 mb-2 block">Period</label>
								<div className="grid grid-cols-2 gap-2">
									<input type="date" className="p-2 border border-gray-300 rounded-lg text-sm" />
									<input type="date" className="p-2 border border-gray-300 rounded-lg text-sm" />
								</div>
							</div>
							
							<button className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:from-green-700 hover:to-emerald-700 transition-all">
								Create Budget
							</button>
						</div>
					</div>

					{/* Enhanced Cost Center Management */}
					<div className="bg-gradient-to-br from-orange-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-4">
							🏢 Cost Centers
						</h2>
						
						<div className="space-y-3">
							{[
								{ name: 'Engineering', budget: 450000, spent: 367000, percentage: 81.6 },
								{ name: 'Sales', budget: 320000, spent: 245000, percentage: 76.6 },
								{ name: 'Marketing', budget: 280000, spent: 234000, percentage: 83.6 },
								{ name: 'Operations', budget: 180000, spent: 145000, percentage: 80.6 }
							].map((center, index) => (
								<div key={index} className="bg-white rounded-lg border border-gray-200 p-4">
									<div className="flex items-center justify-between mb-2">
										<span className="text-sm font-medium text-gray-700">{center.name}</span>
										<span className="text-xs text-gray-500">{center.percentage.toFixed(1)}%</span>
									</div>
									<div className="w-full bg-gray-200 rounded-full h-1.5 mb-2">
										<div 
											className={`h-1.5 rounded-full transition-all duration-300 ${
												center.percentage > 85 ? 'bg-red-500' : 
												center.percentage > 75 ? 'bg-yellow-500' : 'bg-green-500'
											}`}
											style={{ width: `${center.percentage}%` }}
										></div>
									</div>
									<div className="flex justify-between text-xs text-gray-500">
										<span>{formatCurrency(center.spent)}</span>
										<span>{formatCurrency(center.budget)}</span>
									</div>
								</div>
							))}
						</div>
					</div>

					{/* Enhanced Budget Alerts */}
					<div className="bg-gradient-to-br from-red-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-red-600 to-pink-600 bg-clip-text text-transparent mb-4">
							🚨 Budget Alerts
						</h2>
						
						<div className="space-y-3">
							{[
								{ message: 'Marketing budget 85% utilized', severity: 'warning', time: '2 hours ago' },
								{ message: 'Operations approaching limit', severity: 'critical', time: '4 hours ago' },
								{ message: 'Travel budget approved', severity: 'info', time: '1 day ago' },
								{ message: 'HR budget variance detected', severity: 'warning', time: '2 days ago' }
							].map((alert, index) => (
								<div key={index} className="flex items-start gap-3 p-3 bg-white rounded-lg border border-gray-200">
									<div className={`w-2 h-2 rounded-full mt-2 flex-shrink-0 ${
										alert.severity === 'critical' ? 'bg-red-500' :
										alert.severity === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
									}`}></div>
									<div className="flex-1">
										<p className="text-sm text-gray-900">{alert.message}</p>
										<p className="text-xs text-gray-500">{alert.time}</p>
									</div>
								</div>
							))}
						</div>
						
						<button className="w-full mt-4 bg-gradient-to-r from-red-600 to-pink-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:from-red-700 hover:to-pink-700 transition-all">
							Configure Alerts
						</button>
					</div>
				</div>
			</div>
		</div>
	)
}
