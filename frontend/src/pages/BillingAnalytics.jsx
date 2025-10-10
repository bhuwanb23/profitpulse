import RevenueTrends from '../components/financial/analytics/RevenueTrends'
import PaymentStatusCharts from '../components/financial/analytics/PaymentStatusCharts'
import OutstandingPayments from '../components/financial/analytics/OutstandingPayments'
import BillingEfficiency from '../components/financial/analytics/BillingEfficiency'
import PaymentMethodAnalytics from '../components/financial/analytics/PaymentMethodAnalytics'

export default function BillingAnalyticsPage() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Billing Analytics</h1>
				<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Export</button>
			</div>
			<RevenueTrends />
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<PaymentStatusCharts />
				<OutstandingPayments />
				<BillingEfficiency />
				<PaymentMethodAnalytics />
			</div>
		</div>
	)
}
