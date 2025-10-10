export default function ReportTemplates() {
	const items = [
		{ id: 't1', name: 'Monthly Revenue Summary' },
		{ id: 't2', name: 'Ticket SLA Compliance' },
		{ id: 't3', name: 'Client Profitability Report' },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Report Templates</h2>
			<ul className="mt-3 space-y-2 text-sm">
				{items.map(i => (
					<li key={i.id} className="p-3 border rounded flex items-center justify-between">
						<span>{i.name}</span>
						<div className="flex gap-2">
							<button className="px-2 py-1 rounded bg-gray-100 hover:bg-gray-200 text-xs">Load</button>
							<button className="px-2 py-1 rounded bg-gray-100 hover:bg-gray-200 text-xs">Export</button>
						</div>
					</li>
				))}
			</ul>
		</section>
	)
}
