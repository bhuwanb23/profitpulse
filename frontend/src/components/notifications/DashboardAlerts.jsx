export default function DashboardAlerts() {
	const cards = [
		{ id: 'd1', title: 'High SLA Breach Risk', level: 'High' },
		{ id: 'd2', title: 'Outstanding Payments Rising', level: 'Medium' },
		{ id: 'd3', title: 'High Ticket Backlog', level: 'Low' },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Dashboard Alerts</h2>
			<div className="mt-3 grid grid-cols-1 sm:grid-cols-3 gap-3">
				{cards.map(c => (
					<div key={c.id} className="p-3 border rounded">
						<div className="text-sm font-medium">{c.title}</div>
						<div className={`mt-1 text-xs px-2 py-0.5 rounded w-max ${c.level==='High'?'bg-rose-50 text-rose-700': c.level==='Medium'?'bg-amber-50 text-amber-700':'bg-gray-100'}`}>{c.level}</div>
					</div>
				))}
			</div>
		</section>
	)
}
