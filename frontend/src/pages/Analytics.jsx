import { useMemo } from 'react'
import { KPICard } from '../components/clients/KPICard'
import { Button } from '../components/ui/Button'
import { 
	TrendingUpIcon, 
	CurrencyDollarIcon, 
	ChartBarIcon, 
	UserIcon,
	CalendarIcon,
	ArrowUpIcon
} from '../components/ui/Icons'

// Analytics Components
import { RevenueChart } from '../components/analytics/RevenueChart'
import { DepartmentChart } from '../components/analytics/DepartmentChart'
import { CustomerSegmentsChart } from '../components/analytics/CustomerSegmentsChart'
import { PerformanceMetricsChart } from '../components/analytics/PerformanceMetricsChart'
import { ExpenseChart } from '../components/analytics/ExpenseChart'
import { ForecastChart } from '../components/analytics/ForecastChart'
import { AnalyticsInsights } from '../components/analytics/AnalyticsInsights'
import { CustomTooltip } from '../components/analytics/CustomTooltip'
import BudgetUtilization from '../components/analytics/BudgetUtilization'
import ExpenseTracking from '../components/analytics/ExpenseTracking'
import RevenueAnalytics from '../components/analytics/RevenueAnalytics'
import RoiAnalysis from '../components/analytics/RoiAnalysis'
import ProfitabilityChart from '../components/analytics/ProfitabilityChart'
import ForecastingChart from '../components/analytics/ForecastingChart'

export default function Analytics() {
	// Comprehensive analytics data
	const analyticsData = useMemo(() => {
		// Revenue trends over 12 months
		const revenueData = [
			{ month: 'Jan', revenue: 88400, expenses: 52000, profit: 36400, target: 95000, growth: 15.2, customers: 145 },
			{ month: 'Feb', revenue: 92300, expenses: 54500, profit: 37800, target: 95000, growth: 4.4, customers: 152 },
			{ month: 'Mar', revenue: 87600, expenses: 51200, profit: 36400, target: 95000, growth: -5.1, customers: 148 },
			{ month: 'Apr', revenue: 105200, expenses: 58900, profit: 46300, target: 95000, growth: 20.1, customers: 167 },
			{ month: 'May', revenue: 98700, expenses: 55800, profit: 42900, target: 95000, growth: -6.2, customers: 159 },
			{ month: 'Jun', revenue: 112800, expenses: 62400, profit: 50400, target: 95000, growth: 14.3, customers: 178 },
			{ month: 'Jul', revenue: 118900, expenses: 65200, profit: 53700, target: 95000, growth: 5.4, customers: 185 },
			{ month: 'Aug', revenue: 124300, expenses: 68100, profit: 56200, target: 95000, growth: 4.5, customers: 192 },
			{ month: 'Sep', revenue: 119600, expenses: 66800, profit: 52800, target: 95000, growth: -3.8, customers: 188 },
			{ month: 'Oct', revenue: 135400, expenses: 72900, profit: 62500, target: 95000, growth: 13.2, customers: 205 },
			{ month: 'Nov', revenue: 142800, expenses: 76200, profit: 66600, target: 95000, growth: 5.5, customers: 218 },
			{ month: 'Dec', revenue: 158200, expenses: 82400, profit: 75800, target: 95000, growth: 10.8, customers: 235 }
		]

		// Department performance data
		const departmentData = [
			{ name: 'IT Services', revenue: 485200, expenses: 298400, profit: 186800, growth: 18.5, fill: '#3b82f6' },
			{ name: 'Consulting', revenue: 342800, expenses: 198600, profit: 144200, growth: 12.3, fill: '#10b981' },
			{ name: 'Support', revenue: 268900, expenses: 175400, profit: 93500, growth: 8.7, fill: '#f59e0b' },
			{ name: 'Training', revenue: 156400, expenses: 89200, profit: 67200, growth: 22.1, fill: '#ef4444' },
			{ name: 'Cloud Services', revenue: 298700, expenses: 167800, profit: 130900, growth: 35.2, fill: '#8b5cf6' },
			{ name: 'Security', revenue: 189600, expenses: 112300, profit: 77300, growth: 28.4, fill: '#06b6d4' }
		]

		// Customer segments
		const customerSegments = [
			{ name: 'Enterprise', value: 45, revenue: 892400, count: 23, fill: '#3b82f6' },
			{ name: 'Mid-Market', value: 32, revenue: 634800, count: 67, fill: '#10b981' },
			{ name: 'Small Business', value: 18, revenue: 356700, count: 145, fill: '#f59e0b' },
			{ name: 'Startups', value: 5, revenue: 98900, count: 89, fill: '#ef4444' }
		]

		// Monthly expenses breakdown
		const expenseData = [
			{ category: 'Salaries', amount: 285400, percentage: 42.3, fill: '#3b82f6' },
			{ category: 'Infrastructure', amount: 156800, percentage: 23.2, fill: '#10b981' },
			{ category: 'Marketing', amount: 89600, percentage: 13.3, fill: '#f59e0b' },
			{ category: 'Operations', amount: 67200, percentage: 9.9, fill: '#ef4444' },
			{ category: 'R&D', amount: 45300, percentage: 6.7, fill: '#8b5cf6' },
			{ category: 'Other', amount: 30700, percentage: 4.6, fill: '#6b7280' }
		]

		// Performance metrics
		const performanceMetrics = [
			{ name: 'Revenue Growth', value: 85, target: 90, fill: '#10b981' },
			{ name: 'Profit Margin', value: 72, target: 75, fill: '#3b82f6' },
			{ name: 'Customer Satisfaction', value: 91, target: 95, fill: '#f59e0b' },
			{ name: 'Market Share', value: 67, target: 70, fill: '#8b5cf6' },
			{ name: 'Operational Efficiency', value: 78, target: 85, fill: '#ef4444' },
			{ name: 'Employee Satisfaction', value: 83, target: 90, fill: '#06b6d4' }
		]

		// Forecast data
		const forecastData = [
			{ month: 'Jan 2025', predicted: 165000, optimistic: 185000, pessimistic: 145000 },
			{ month: 'Feb 2025', predicted: 172000, optimistic: 195000, pessimistic: 152000 },
			{ month: 'Mar 2025', predicted: 168000, optimistic: 188000, pessimistic: 148000 },
			{ month: 'Apr 2025', predicted: 185000, optimistic: 210000, pessimistic: 165000 },
			{ month: 'May 2025', predicted: 192000, optimistic: 218000, pessimistic: 172000 },
			{ month: 'Jun 2025', predicted: 198000, optimistic: 225000, pessimistic: 178000 }
		]

		return {
			revenueData,
			departmentData,
			customerSegments,
			expenseData,
			performanceMetrics,
			forecastData
		}
	}, [])

	// Calculate KPI data
	const kpiData = useMemo(() => {
		const currentMonth = analyticsData.revenueData[analyticsData.revenueData.length - 1]
		const previousMonth = analyticsData.revenueData[analyticsData.revenueData.length - 2]
		
		const totalRevenue = analyticsData.revenueData.reduce((sum, item) => sum + item.revenue, 0)
		const totalProfit = analyticsData.revenueData.reduce((sum, item) => sum + item.profit, 0)
		const totalCustomers = currentMonth.customers
		const avgRevenuePerCustomer = totalRevenue / totalCustomers / 12
		const profitMargin = (totalProfit / totalRevenue) * 100
		const revenueGrowth = ((currentMonth.revenue - previousMonth.revenue) / previousMonth.revenue) * 100

		return {
			totalRevenue,
			totalProfit,
			totalCustomers,
			avgRevenuePerCustomer,
			profitMargin,
			revenueGrowth,
			currentRevenue: currentMonth.revenue,
			currentProfit: currentMonth.profit
		}
	}, [analyticsData])

	const formatCurrency = (amount) => {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD',
			minimumFractionDigits: 0,
			maximumFractionDigits: 0
		}).format(amount)
	}

	// Create custom tooltip with currency formatting
	const customTooltip = CustomTooltip({ formatCurrency })

	return (
		<div className="space-y-6">
			{/* Header */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
						📊 Business Analytics Dashboard
					</h1>
					<p className="text-gray-600 mt-1">Comprehensive insights into your business performance</p>
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<CalendarIcon className="h-4 w-4" />
						Last 12 Months
					</Button>
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<ChartBarIcon className="h-4 w-4" />
						Export Report
					</Button>
					<Button variant="primary" size="sm" className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600">
						<TrendingUpIcon className="h-4 w-4" />
						View Insights
					</Button>
				</div>
			</div>

			{/* KPI Cards */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
				<KPICard
					title="Total Revenue"
					value={kpiData.totalRevenue}
					change={kpiData.revenueGrowth}
					changeType={kpiData.revenueGrowth > 0 ? "positive" : "negative"}
					format="currency"
					icon={CurrencyDollarIcon}
					iconColor="green"
				/>
				<KPICard
					title="Total Profit"
					value={kpiData.totalProfit}
					change={15.8}
					changeType="positive"
					format="currency"
					icon={TrendingUpIcon}
					iconColor="blue"
				/>
				<KPICard
					title="Profit Margin"
					value={kpiData.profitMargin / 100}
					change={2.3}
					changeType="positive"
					format="percentage"
					icon={ChartBarIcon}
					iconColor="purple"
				/>
				<KPICard
					title="Total Customers"
					value={kpiData.totalCustomers}
					change={8.7}
					changeType="positive"
					format="number"
					icon={UserIcon}
					iconColor="orange"
				/>
				<KPICard
					title="Avg Revenue/Customer"
					value={kpiData.avgRevenuePerCustomer}
					change={5.2}
					changeType="positive"
					format="currency"
					icon={CurrencyDollarIcon}
					iconColor="teal"
				/>
				<KPICard
					title="Monthly Growth"
					value={kpiData.revenueGrowth / 100}
					change={kpiData.revenueGrowth}
					changeType={kpiData.revenueGrowth > 0 ? "positive" : "negative"}
					format="percentage"
					icon={ArrowUpIcon}
					iconColor="green"
				/>
			</div>

			{/* Hero Chart - Revenue & Profit Trends */}
			<RevenueChart data={analyticsData.revenueData} customTooltip={customTooltip} />

			{/* Charts Grid */}
			<div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
				<DepartmentChart data={analyticsData.departmentData} customTooltip={customTooltip} />
				<CustomerSegmentsChart data={analyticsData.customerSegments} />
				<PerformanceMetricsChart data={analyticsData.performanceMetrics} customTooltip={customTooltip} />
			</div>

			{/* Secondary Charts Row */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<ExpenseChart data={analyticsData.expenseData} formatCurrency={formatCurrency} />
				<ForecastChart data={analyticsData.forecastData} customTooltip={customTooltip} />
			</div>

			{/* Additional Analytics Row */}
			<div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
				<RevenueAnalytics />
				<ProfitabilityChart />
				<RoiAnalysis />
			</div>

			{/* Budget & Forecasting Row */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<BudgetUtilization />
				<ForecastingChart />
			</div>

			{/* Expense Tracking Table */}
			<ExpenseTracking />

			{/* Insights & Actions */}
			<AnalyticsInsights kpiData={kpiData} formatCurrency={formatCurrency} />
		</div>
	)
}
