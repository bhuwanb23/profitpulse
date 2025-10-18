import { useMemo } from 'react'
import { KPICard } from '../components/clients/KPICard'
import { Button } from '../components/ui/Button'
import { 
	ChartBarIcon,
	TrendingUpIcon,
	ExclamationTriangleIcon,
	CurrencyDollarIcon,
	UsersIcon,
	DocumentTextIcon,
	CalendarIcon,
	RefreshIcon,
	CheckIcon
} from '../components/ui/Icons'

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
	// AI analytics data
	const aiData = useMemo(() => {
		return {
			aiAccuracy: 94.8,
			predictionsGenerated: 1247,
			costSavings: 156780,
			profitabilityScore: 87.3,
			leaksDetected: 23,
			optimizationOpportunities: 15,
			aiRecommendations: [
				{ title: 'Optimize Service Pricing', impact: 'High', savings: '$45,000', confidence: 92 },
				{ title: 'Reduce Client Churn Risk', impact: 'Medium', savings: '$28,000', confidence: 87 },
				{ title: 'Improve Resource Allocation', impact: 'High', savings: '$38,000', confidence: 95 },
				{ title: 'Automate Routine Tasks', impact: 'Medium', savings: '$22,000', confidence: 89 }
			],
			predictiveInsights: [
				{ metric: 'Revenue Growth', prediction: '+12.5%', confidence: 94, trend: 'up' },
				{ metric: 'Client Satisfaction', prediction: '+5.2%', confidence: 89, trend: 'up' },
				{ metric: 'Operational Costs', prediction: '-8.7%', confidence: 91, trend: 'down' },
				{ metric: 'Market Share', prediction: '+3.1%', confidence: 86, trend: 'up' }
			],
			aiModels: [
				{ name: 'Profitability Predictor', status: 'Active', accuracy: 94.8, lastTrained: '2 hours ago' },
				{ name: 'Churn Prevention', status: 'Active', accuracy: 87.3, lastTrained: '6 hours ago' },
				{ name: 'Price Optimizer', status: 'Training', accuracy: 91.2, lastTrained: '1 day ago' },
				{ name: 'Resource Allocator', status: 'Active', accuracy: 89.6, lastTrained: '4 hours ago' }
			]
		}
	}, [])

	const formatCurrency = (amount) => {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD',
			minimumFractionDigits: 0,
			maximumFractionDigits: 0
		}).format(amount)
	}

	const getStatusColor = (status) => {
		const colors = {
			'Active': 'bg-green-100 text-green-800',
			'Training': 'bg-blue-100 text-blue-800',
			'Inactive': 'bg-gray-100 text-gray-800',
			'Error': 'bg-red-100 text-red-800'
		}
		return colors[status] || 'bg-gray-100 text-gray-800'
	}

	const getImpactColor = (impact) => {
		const colors = {
			'High': 'bg-red-100 text-red-800',
			'Medium': 'bg-yellow-100 text-yellow-800',
			'Low': 'bg-green-100 text-green-800'
		}
		return colors[impact] || 'bg-gray-100 text-gray-800'
	}

	return (
		<div className="space-y-6">
			{/* Header */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
						🤖 AI Intelligence & Insights
					</h1>
					<p className="text-gray-600 mt-1">Leverage artificial intelligence for business optimization and predictive analytics</p>
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<DocumentTextIcon className="h-4 w-4" />
						Export Insights
					</Button>
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<CalendarIcon className="h-4 w-4" />
						Schedule Analysis
					</Button>
					<Button variant="primary" size="sm" className="flex items-center gap-2 bg-gradient-to-r from-violet-600 to-purple-600">
						<RefreshIcon className="h-4 w-4" />
						Refresh AI Models
					</Button>
				</div>
			</div>

			{/* KPI Cards */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
				<KPICard
					title="AI Accuracy"
					value={aiData.aiAccuracy}
					change={2.3}
					changeType="positive"
					format="decimal"
					icon={ChartBarIcon}
					iconColor="violet"
					suffix="%"
				/>
				<KPICard
					title="Predictions Generated"
					value={aiData.predictionsGenerated}
					change={18.7}
					changeType="positive"
					format="number"
					icon={TrendingUpIcon}
					iconColor="purple"
				/>
				<KPICard
					title="Cost Savings"
					value={aiData.costSavings}
					change={25.4}
					changeType="positive"
					format="currency"
					icon={CurrencyDollarIcon}
					iconColor="emerald"
				/>
				<KPICard
					title="Profitability Score"
					value={aiData.profitabilityScore}
					change={4.8}
					changeType="positive"
					format="decimal"
					icon={TrendingUpIcon}
					iconColor="blue"
					suffix="%"
				/>
				<KPICard
					title="Leaks Detected"
					value={aiData.leaksDetected}
					change={-12.3}
					changeType="positive"
					format="number"
					icon={ExclamationTriangleIcon}
					iconColor="red"
				/>
				<KPICard
					title="Optimization Opportunities"
					value={aiData.optimizationOpportunities}
					change={8.9}
					changeType="positive"
					format="number"
					icon={CheckIcon}
					iconColor="teal"
				/>
			</div>

			{/* Main Content Grid */}
			<div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
				{/* Left Column - AI Insights & Recommendations */}
				<div className="space-y-6">
					{/* AI Recommendations */}
					<div className="bg-gradient-to-br from-violet-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent mb-4">
							🎯 AI Recommendations
						</h2>
						
						<div className="space-y-4 max-h-80 overflow-y-auto">
							{aiData.aiRecommendations.map((rec, index) => (
								<div key={index} className="bg-white rounded-lg border border-gray-200 p-4 hover:border-violet-300 transition-all hover:shadow-sm">
									<div className="flex items-start justify-between mb-3">
										<div className="flex-1">
											<h3 className="font-medium text-gray-900 text-sm">{rec.title}</h3>
											<p className="text-xs text-gray-500 mt-1">Potential savings: {rec.savings}</p>
										</div>
										<div className="flex items-center gap-2">
											<span className={`px-2 py-1 rounded-full text-xs font-medium ${getImpactColor(rec.impact)}`}>
												{rec.impact} Impact
											</span>
										</div>
									</div>
									<div className="flex items-center justify-between">
										<div className="flex items-center gap-2">
											<span className="text-xs text-gray-500">Confidence:</span>
											<div className="w-16 bg-gray-200 rounded-full h-1.5">
												<div 
													className="h-1.5 rounded-full bg-violet-500 transition-all duration-300" 
													style={{ width: `${rec.confidence}%` }}
												></div>
											</div>
											<span className="text-xs font-medium text-gray-700">{rec.confidence}%</span>
										</div>
										<button className="text-xs bg-violet-100 text-violet-700 px-2 py-1 rounded hover:bg-violet-200 transition-colors">
											Apply
										</button>
									</div>
								</div>
							))}
						</div>
					</div>

					{/* Enhanced AI Overview */}
					<div className="bg-gradient-to-br from-purple-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
							🧠 AI Model Performance
						</h2>
						
						<div className="space-y-4">
							{aiData.aiModels.map((model, index) => (
								<div key={index} className="bg-white rounded-lg border border-gray-200 p-4">
									<div className="flex items-center justify-between mb-3">
										<div className="flex items-center gap-3">
											<div className="w-2 h-2 bg-purple-500 rounded-full"></div>
											<span className="font-medium text-gray-900 text-sm">{model.name}</span>
										</div>
										<span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(model.status)}`}>
											{model.status}
										</span>
									</div>
									<div className="grid grid-cols-2 gap-4 text-xs text-gray-500">
										<div>
											<div className="font-medium">Accuracy</div>
											<div className="text-gray-900 font-semibold">{model.accuracy}%</div>
										</div>
										<div>
											<div className="font-medium">Last Trained</div>
											<div className="text-gray-900">{model.lastTrained}</div>
										</div>
									</div>
								</div>
							))}
						</div>
					</div>
				</div>

				{/* Right Column - Predictive Analytics & AI Components */}
				<div className="space-y-6">
					{/* Predictive Analytics */}
					<div className="bg-gradient-to-br from-blue-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
							📈 Predictive Insights
						</h2>
						
						<div className="grid grid-cols-1 gap-4">
							{aiData.predictiveInsights.map((insight, index) => (
								<div key={index} className="bg-white rounded-lg border border-gray-200 p-4">
									<div className="flex items-center justify-between mb-2">
										<span className="text-sm font-medium text-gray-700">{insight.metric}</span>
										<div className="flex items-center gap-1">
											{insight.trend === 'up' && <TrendingUpIcon className="h-4 w-4 text-green-500" />}
											{insight.trend === 'down' && <TrendingUpIcon className="h-4 w-4 text-red-500 rotate-180" />}
										</div>
									</div>
									<div className="flex items-center justify-between">
										<span className="text-lg font-bold text-gray-900">{insight.prediction}</span>
										<span className="text-xs text-gray-500">{insight.confidence}% confidence</span>
									</div>
								</div>
							))}
						</div>
					</div>

					{/* AI Components Integration */}
					<div className="grid grid-cols-1 gap-6">
						<LeakAlerts />
						<ProfitabilityScores />
					</div>
				</div>
			</div>

			{/* Enhanced AI Components Row */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<AIRecommendationPanel />
				<PredictiveAnalytics />
			</div>

			{/* Bottom Rows - Additional AI Components (2 per row) */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<ProfitabilityGenome />
				<ServiceOptimization />
			</div>
			
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<PricingRecommendations />
				<MarketInsights />
			</div>
		</div>
	)
}
