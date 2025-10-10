export default function AlertHistory() {
	const rows = [
		{ id: 'h1', at: '2025-10-10 08:30', text: 'SLA breach risk exceeded threshold' },
		{ id: 'h2', at: '2025-10-10 09:05', text: 'Outstanding payments crossed $10k' },
		{ id: 'h3', at: '2025-10-10 09:40', text: 'Ticket backlog above 50' },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Alert History</h2>
			<table className="mt-3 w-full text-sm">
				<thead className="text-left text-gray-500">
					<tr><th className="py-2">Time</th><th className="py-2">Event</th></tr>
				</thead>
				<tbody>
					{rows.map(r => (
						<tr key={r.id} className="border-t">
							<td className="py-2">{r.at}</td>
							<td className="py-2">{r.text}</td>
						</tr>
					))}
				</tbody>
			</table>
		</section>
	)
}
