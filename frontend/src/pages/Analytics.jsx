export default function Analytics() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Financial Analytics</h1>
				<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Export</button>
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				{/* Revenue Analytics */}
				<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
					<h2 className="text-lg font-semibold mb-4">Revenue Analytics</h2>
					<div className="space-y-3">
						<div className="flex justify-between">
							<span className="text-gray-600">Monthly Revenue</span>
							<span className="font-semibold">$88,400</span>
						</div>
						<div className="flex justify-between">
							<span className="text-gray-600">Growth Rate</span>
							<span className="font-semibold text-green-600">+12.4%</span>
						</div>
					</div>
				</div>

				{/* Profitability Chart */}
				<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
					<h2 className="text-lg font-semibold mb-4">Profitability Analysis</h2>
					<div className="h-32 bg-gray-100 rounded flex items-center justify-center">
						<p className="text-gray-500">Chart Placeholder</p>
					</div>
				</div>

				{/* Budget Utilization */}
				<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
					<h2 className="text-lg font-semibold mb-4">Budget Utilization</h2>
					<div className="space-y-3">
						<div className="flex justify-between">
							<span className="text-gray-600">Used</span>
							<span className="font-semibold">$45,200</span>
						</div>
						<div className="flex justify-between">
							<span className="text-gray-600">Remaining</span>
							<span className="font-semibold text-green-600">$54,800</span>
						</div>
					</div>
				</div>

				{/* Forecasting Chart */}
				<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
					<h2 className="text-lg font-semibold mb-4">Revenue Forecasting</h2>
					<div className="h-32 bg-gray-100 rounded flex items-center justify-center">
						<p className="text-gray-500">Forecast Chart</p>
					</div>
				</div>
			</div>
		</div>
	)
}
