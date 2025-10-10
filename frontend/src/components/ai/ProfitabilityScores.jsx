export default function ProfitabilityScores() {
	const items = [
		{ client: 'Acme', score: 0.85 },
		{ client: 'TechStart', score: 0.78 },
		{ client: 'RetailMax', score: 0.62 },
		{ client: 'HealthPlus', score: 0.80 },
		{ client: 'FinanceFirst', score: 0.74 },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Profitability Scores</h2>
			<ul className="mt-3 space-y-3">
				{items.map((it) => (
					<li key={it.client} className="flex items-center justify-between">
						<div className="w-40 text-sm">{it.client}</div>
						<div className="flex-1 mx-3 h-2 bg-gray-100 rounded-full">
							<div className="h-2 bg-emerald-500 rounded-full" style={{ width: `${it.score * 100}%` }} />
						</div>
						<div className="w-12 text-right text-sm">{Math.round(it.score * 100)}%</div>
					</li>
				))}
			</ul>
		</section>
	)
}
