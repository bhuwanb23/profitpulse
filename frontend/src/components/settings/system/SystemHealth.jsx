export default function SystemHealth() {
	const items = [
		{ id: 'h1', name: 'API', status: 'OK', latency: '120ms' },
		{ id: 'h2', name: 'DB', status: 'OK', latency: '8ms' },
		{ id: 'h3', name: 'Queue', status: 'Degraded', latency: '450ms' },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">System Health</h2>
			<table className="mt-3 w-full text-sm">
				<thead className="text-left text-gray-500">
					<tr>
						<th className="py-2">Service</th>
						<th className="py-2">Status</th>
						<th className="py-2">Latency</th>
					</tr>
				</thead>
				<tbody>
					{items.map(s => (
						<tr key={s.id} className="border-t">
							<td className="py-2">{s.name}</td>
							<td className="py-2"><span className={`text-xs px-2 py-0.5 rounded ${s.status==='OK'?'bg-emerald-50 text-emerald-700': s.status==='Degraded'?'bg-amber-50 text-amber-700':'bg-rose-50 text-rose-700'}`}>{s.status}</span></td>
							<td className="py-2">{s.latency}</td>
						</tr>
					))}
				</tbody>
			</table>
		</section>
	)
}
