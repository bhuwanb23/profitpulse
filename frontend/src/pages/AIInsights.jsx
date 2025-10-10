import AIOverview from '../components/ai/AIOverview'
import LeakAlerts from '../components/ai/LeakAlerts'
import ProfitabilityScores from '../components/ai/ProfitabilityScores'
import AIRecommendationPanel from '../components/ai/AIRecommendationPanel'
import PredictiveAnalytics from '../components/ai/PredictiveAnalytics'
import ProfitabilityGenome from '../components/ai/ProfitabilityGenome'
import ServiceOptimization from '../components/ai/ServiceOptimization'
import PricingRecommendations from '../components/ai/PricingRecommendations'
import MarketInsights from '../components/ai/MarketInsights'

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
				<AIRecommendationPanel />
				<PredictiveAnalytics />
				<ProfitabilityGenome />
				<ServiceOptimization />
				<PricingRecommendations />
				<MarketInsights />
			</div>
		</div>
	)
}
