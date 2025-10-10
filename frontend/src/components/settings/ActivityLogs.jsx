export default function ActivityLogs() {
	const logs = [
		{ id: 'a1', at: '2025-10-10 09:14', text: 'Login success' },
		{ id: 'a2', at: '2025-10-10 09:17', text: 'Updated pricing settings' },
		{ id: 'a3', at: '2025-10-10 09:25', text: 'Created invoice #1042' },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Activity Logs</h2>
			<ul className="mt-3 text-sm space-y-2">
				{logs.map(l => (
					<li key={l.id} className="p-2 border rounded">[{l.at}] {l.text}</li>
				))}
			</ul>
		</section>
	)
}
