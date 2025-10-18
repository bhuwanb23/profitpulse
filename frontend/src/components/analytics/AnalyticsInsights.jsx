import { Button } from '../ui/Button'

export function AnalyticsInsights({ kpiData, formatCurrency }) {
	return (
		<div className="bg-gradient-to-r from-indigo-50 via-purple-50 to-pink-50 rounded-xl p-6 border border-indigo-200 shadow-sm">
			<div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
				<div>
					<h3 className="text-lg font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-1">
						🎯 Key Insights & Recommendations
					</h3>
					<p className="text-gray-600">
						Your business is showing strong growth with {formatCurrency(kpiData.totalRevenue)} in annual revenue. 
						Consider focusing on the high-performing departments and optimizing customer acquisition costs.
					</p>
				</div>
				<div className="flex flex-wrap gap-3">
					<Button variant="outline" size="sm" className="bg-white/50 backdrop-blur-sm">
						📊 Detailed Report
					</Button>
					<Button variant="outline" size="sm" className="bg-white/50 backdrop-blur-sm">
						🎯 Set Goals
					</Button>
					<Button variant="primary" size="sm" className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
						🚀 Get AI Insights
					</Button>
				</div>
			</div>
		</div>
	)
}
