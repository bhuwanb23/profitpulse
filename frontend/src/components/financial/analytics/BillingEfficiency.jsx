export default function BillingEfficiency() {
	const metrics = { dsoDays: 32, collectionRate: 94 }
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Billing Efficiency</h2>
			<div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
				<div className="p-3 border border-gray-200 rounded-lg">
					<div className="text-xs text-gray-500">DSO (Days Sales Outstanding)</div>
					<div className="text-2xl font-semibold">{metrics.dsoDays} days</div>
					<div className="mt-2 h-2 w-full bg-gray-100 rounded-full"><div className="h-2 bg-amber-500 rounded-full" style={{ width: `${Math.min(metrics.dsoDays, 60) / 60 * 100}%` }} /></div>
				</div>
				<div className="p-3 border border-gray-200 rounded-lg">
					<div className="text-xs text-gray-500">Collection Rate</div>
					<div className="text-2xl font-semibold">{metrics.collectionRate}%</div>
					<div className="mt-2 h-2 w-full bg-gray-100 rounded-full"><div className="h-2 bg-emerald-500 rounded-full" style={{ width: `${metrics.collectionRate}%` }} /></div>
				</div>
			</div>
		</section>
	)
}
