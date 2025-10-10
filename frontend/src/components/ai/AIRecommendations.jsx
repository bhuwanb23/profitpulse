export default function AIRecommendations() {
	const items = [
		{ title: 'Increase Help Desk Pricing', impact: 'High', confidence: 0.85 },
		{ title: 'Add Network Monitoring', impact: 'Medium', confidence: 0.75 },
		{ title: 'Optimize Software Licenses', impact: 'Low', confidence: 0.70 },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">AI Recommendations</h2>
			<ul className="mt-3 space-y-3">
				{items.map((rec) => (
					<li key={rec.title} className="p-3 border border-gray-200 rounded-lg">
						<div className="flex items-center justify-between">
							<div>
								<p className="font-medium text-sm">{rec.title}</p>
								<p className="text-xs text-gray-500">Impact: {rec.impact}</p>
							</div>
							<div className="text-xs text-gray-600">Confidence {(rec.confidence * 100).toFixed(0)}%</div>
						</div>
						<div className="mt-2 flex items-center gap-2">
							<button className="text-xs px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-700">Accept</button>
							<button className="text-xs px-3 py-1.5 rounded bg-gray-100 hover:bg-gray-200">Dismiss</button>
						</div>
					</li>
				))}
			</ul>
		</section>
	)
}
