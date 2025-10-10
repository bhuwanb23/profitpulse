export default function PricingRecommendations() {
	const items = [
		{ id: 'p1', title: 'Raise Help Desk per‑user from $35 → $42', impact: 'high' },
		{ id: 'p2', title: 'Add 10% uplift for 24/7 coverage', impact: 'medium' },
		{ id: 'p3', title: 'Bundle M365 hardening at $6/user', impact: 'medium' },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Pricing Recommendations</h2>
			<ul className="mt-3 space-y-2">
				{items.map(i => (
					<li key={i.id} className="p-3 border rounded-lg flex items-center justify-between">
						<span className="text-sm text-gray-700">{i.title}</span>
						<span className={`text-[10px] px-2 py-0.5 rounded ${i.impact==='high'?'bg-red-50 text-red-700': i.impact==='medium'?'bg-amber-50 text-amber-700':'bg-gray-100'}`}>{i.impact}</span>
					</li>
				))}
			</ul>
		</section>
	)
}
