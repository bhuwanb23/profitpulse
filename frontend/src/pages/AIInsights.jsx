import AIOverview from '../components/ai/AIOverview'
import LeakAlerts from '../components/ai/LeakAlerts'
import ProfitabilityScores from '../components/ai/ProfitabilityScores'
import AIRecommendations from '../components/ai/AIRecommendations'
import PredictiveCharts from '../components/ai/PredictiveCharts'

export default function AIInsights() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">AI Intelligence</h1>
				<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Refresh</button>
			</div>

			<AIOverview />

			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<LeakAlerts />
				<ProfitabilityScores />
				<AIRecommendations />
				<PredictiveCharts />
			</div>
		</div>
	)
}
