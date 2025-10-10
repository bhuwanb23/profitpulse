export default function LeakAlerts() {
	const leaks = [
		{ title: 'Unbilled hours (TechStart)', amount: 1500, severity: 'high' },
		{ title: 'Underpriced service (Acme)', amount: 900, severity: 'medium' },
		{ title: 'Unused licenses (RetailMax)', amount: 450, severity: 'low' },
	]
	const badge = (sev) => sev === 'high' ? 'bg-red-50 text-red-700' : sev === 'medium' ? 'bg-amber-50 text-amber-700' : 'bg-gray-100'
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Revenue Leak Alerts</h2>
			<ul className="mt-3 space-y-3">
				{leaks.map((l) => (
					<li key={l.title} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
						<div>
							<p className="font-medium text-sm">{l.title}</p>
							<p className="text-xs text-gray-500">Potential recovery</p>
						</div>
						<div className="flex items-center gap-2">
							<span className="text-sm font-medium">${l.amount}</span>
							<span className={`text-[10px] px-2 py-0.5 rounded ${badge(l.severity)}`}>{l.severity}</span>
						</div>
					</li>
				))}
			</ul>
		</section>
	)
}
