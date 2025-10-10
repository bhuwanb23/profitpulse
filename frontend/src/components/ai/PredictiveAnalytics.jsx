export default function PredictiveAnalytics() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Predictive Analytics</h2>
			<div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
				<div className="p-3 border rounded-lg">
					<h3 className="text-sm font-medium">Revenue Forecasting</h3>
					<div className="mt-2 h-28 bg-gradient-to-r from-blue-50 to-blue-100 rounded" />
					<p className="mt-2 text-xs text-gray-600">Projected next 6 months: +8.4% avg MoM</p>
				</div>
				<div className="p-3 border rounded-lg">
					<h3 className="text-sm font-medium">Client Churn Prediction</h3>
					<ul className="mt-2 text-xs text-gray-700 space-y-1">
						<li>Acme Co — 12% risk</li>
						<li>Globex — 9% risk</li>
						<li>Umbrella — 7% risk</li>
					</ul>
				</div>
				<div className="p-3 border rounded-lg">
					<h3 className="text-sm font-medium">Service Demand Forecasting</h3>
					<div className="mt-2 h-28 bg-gradient-to-r from-emerald-50 to-emerald-100 rounded" />
					<p className="mt-2 text-xs text-gray-600">Top rising: MDR, Cloud Backup</p>
				</div>
				<div className="p-3 border rounded-lg">
					<h3 className="text-sm font-medium">Budget Optimization</h3>
					<ul className="mt-2 text-xs text-gray-700 space-y-1">
						<li>Reduce unused SaaS seats (save ~$1.2k/mo)</li>
						<li>Consolidate RMM vendors (save ~$800/mo)</li>
					</ul>
				</div>
				<div className="p-3 border rounded-lg">
					<h3 className="text-sm font-medium">Market Trend Analysis</h3>
					<div className="mt-2 h-28 bg-gradient-to-r from-amber-50 to-amber-100 rounded" />
					<p className="mt-2 text-xs text-gray-600">SMB security spend → +14% YoY</p>
				</div>
				<div className="p-3 border rounded-lg">
					<h3 className="text-sm font-medium">Growth Opportunities</h3>
					<ul className="mt-2 text-xs text-gray-700 space-y-1">
						<li>Cross‑sell M365 Hardening to 11 clients</li>
						<li>Bundle NDR with MDR for 7 accounts</li>
					</ul>
				</div>
			</div>
		</section>
	)
}
