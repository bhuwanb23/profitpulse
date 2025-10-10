import BudgetOverview from '../components/financial/budgets/BudgetOverview'
import BudgetCreate from '../components/financial/budgets/BudgetCreate'
import ExpenseCategorization from '../components/financial/budgets/ExpenseCategorization'
import BudgetVsActual from '../components/financial/budgets/BudgetVsActual'
import CostCenterManagement from '../components/financial/budgets/CostCenterManagement'
import BudgetAlerts from '../components/financial/budgets/BudgetAlerts'

export default function BudgetManagementPage() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Budget Management</h1>
			</div>
			<BudgetOverview />
			<BudgetCreate />
			<BudgetVsActual />
			<ExpenseCategorization />
			<CostCenterManagement />
			<BudgetAlerts />
		</div>
	)
}
