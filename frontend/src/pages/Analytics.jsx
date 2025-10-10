import RevenueAnalytics from '../components/analytics/RevenueAnalytics'
import ProfitabilityChart from '../components/analytics/ProfitabilityChart'
import BudgetUtilization from '../components/analytics/BudgetUtilization'
import ExpenseTracking from '../components/analytics/ExpenseTracking'
import ForecastingChart from '../components/analytics/ForecastingChart'
import RoiAnalysis from '../components/analytics/RoiAnalysis'

export default function Analytics() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Financial Analytics</h1>
				<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Export</button>
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<RevenueAnalytics />
				<ProfitabilityChart />
				<BudgetUtilization />
				<ForecastingChart />
				<RoiAnalysis />
				<ExpenseTracking />
			</div>
		</div>
	)
}
