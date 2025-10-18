export default function ReportTemplates() {
	const items = [
		{ id: 't1', name: 'Monthly Revenue Summary', type: 'Financial', color: 'from-blue-500 to-blue-600' },
		{ id: 't2', name: 'Ticket SLA Compliance', type: 'Operations', color: 'from-green-500 to-green-600' },
		{ id: 't3', name: 'Client Profitability Report', type: 'Analytics', color: 'from-purple-500 to-purple-600' },
		{ id: 't4', name: 'Department Performance', type: 'HR', color: 'from-orange-500 to-orange-600' },
		{ id: 't5', name: 'Customer Satisfaction', type: 'Quality', color: 'from-pink-500 to-pink-600' }
	]
	return (
		<section className="bg-gradient-to-br from-indigo-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<h2 className="text-lg font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-4">
				Report Templates
			</h2>
			<div className="space-y-3">
				{items.map(i => (
					<div key={i.id} className="bg-white rounded-lg border border-gray-200 p-4 hover:border-gray-300 transition-all hover:shadow-sm">
						<div className="flex items-center justify-between">
							<div className="flex items-center gap-3">
								<div className={`w-3 h-3 rounded-full bg-gradient-to-r ${i.color}`}></div>
								<div>
									<p className="font-medium text-gray-900 text-sm">{i.name}</p>
									<p className="text-xs text-gray-500">{i.type}</p>
								</div>
							</div>
							<div className="flex gap-2">
								<button className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-blue-600 to-blue-700 text-white text-xs font-medium hover:from-blue-700 hover:to-blue-800 transition-all">
									Load
								</button>
								<button className="px-3 py-1.5 rounded-lg border border-gray-300 text-gray-700 text-xs font-medium hover:bg-gray-50 transition-colors">
									Export
								</button>
							</div>
						</div>
					</div>
				))}
			</div>
		</section>
	)
}
