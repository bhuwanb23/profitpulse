export default function AIOverview() {
	const cards = [
		{ title: 'Profitability Lift', value: '+12.5%', note: 'Projected', badge: '0.82' },
		{ title: 'Leak Reduction', value: '-23.0%', note: 'Estimated', badge: '0.88' },
		{ title: 'Budget Optimization', value: '15.0%', note: 'Potential', badge: '0.90' },
		{ title: 'Churn Risk', value: '3.2%', note: 'Current', badge: '0.79' },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">AI Analytics Overview</h2>
			<div className="mt-4 grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
				{cards.map((c) => (
					<div key={c.title} className="rounded-lg border border-gray-200 p-4">
						<div className="text-sm text-gray-500 flex items-center justify-between">
							<span>{c.title}</span>
							<span className="text-[10px] px-2 py-0.5 rounded bg-blue-50 text-blue-700">conf {c.badge}</span>
						</div>
						<div className="mt-2 text-xl font-semibold">{c.value}</div>
						<div className="text-xs text-gray-500">{c.note}</div>
					</div>
				))}
			</div>
		</section>
	)
}
