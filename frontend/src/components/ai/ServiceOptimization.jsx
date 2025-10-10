export default function ServiceOptimization() {
	const suggestions = [
		{ id: 's1', text: 'Migrate legacy AV to MDR for top 5 clients' },
		{ id: 's2', text: 'Introduce tiered support SLAs to reduce overage' },
		{ id: 's3', text: 'Standardize backup vendor to lower costs' },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Service Optimization</h2>
			<ul className="mt-3 space-y-2 text-sm">
				{suggestions.map(s => (
					<li key={s.id} className="p-3 border rounded-lg text-gray-700">{s.text}</li>
				))}
			</ul>
		</section>
	)
}
