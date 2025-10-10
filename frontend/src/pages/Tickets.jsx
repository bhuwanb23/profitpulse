export default function Tickets() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Tickets</h1>
				<div className="flex gap-2">
					<select className="text-sm border border-gray-300 rounded-md px-2 py-1"><option>All Statuses</option></select>
					<select className="text-sm border border-gray-300 rounded-md px-2 py-1"><option>All Priorities</option></select>
					<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">+ New Ticket</button>
				</div>
			</div>

			<div className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
				<ul className="divide-y">
					{[
						{ id: 'TKT-001', title: 'Email server down', priority: 'High', status: 'Resolved' },
						{ id: 'TKT-002', title: 'VPN issues', priority: 'Medium', status: 'In Progress' },
						{ id: 'TKT-003', title: 'Software install', priority: 'Low', status: 'Open' },
					].map((t) => (
						<li key={t.id} className="py-3 flex items-center justify-between">
							<div>
								<p className="font-medium text-sm">{t.title}</p>
								<p className="text-xs text-gray-500">{t.id}</p>
							</div>
							<div className="flex items-center gap-2">
								<span className="text-xs px-2 py-1 rounded bg-gray-100">{t.priority}</span>
								<span className="text-xs px-2 py-1 rounded bg-gray-100">{t.status}</span>
								<button className="text-blue-600 hover:underline text-sm">View</button>
							</div>
						</li>
					))}
				</ul>
			</div>
		</div>
	)
}
