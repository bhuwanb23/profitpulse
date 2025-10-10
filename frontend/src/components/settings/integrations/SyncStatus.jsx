export default function SyncStatus() {
	const items = [
		{ id: 's1', name: 'SuperOps', status: 'OK', last: '2m ago' },
		{ id: 's2', name: 'QuickBooks', status: 'OK', last: '5m ago' },
		{ id: 's3', name: 'Zapier', status: 'Error', last: '1m ago' },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Sync Status</h2>
			<ul className="mt-3 text-sm space-y-2">
				{items.map(i => (
					<li key={i.id} className="p-2 border rounded flex items-center justify-between">
						<span>{i.name}</span>
						<span className={`text-xs px-2 py-0.5 rounded ${i.status==='OK'?'bg-emerald-50 text-emerald-700':'bg-rose-50 text-rose-700'}`}>{i.status} — {i.last}</span>
					</li>
				))}
			</ul>
		</section>
	)
}
