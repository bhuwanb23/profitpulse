export default function Tickets() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Tickets</h1>
				<div className="flex gap-2">
					<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">+ New Ticket</button>
				</div>
			</div>
			
			{/* Ticket List Placeholder */}
			<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
				<h2 className="text-lg font-semibold mb-4">Support Tickets</h2>
				<div className="space-y-3">
					<div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
						<div>
							<h3 className="font-medium">Email server down</h3>
							<p className="text-sm text-gray-500">TKT-001 • Acme Corporation</p>
						</div>
						<span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">Resolved</span>
					</div>
					<div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
						<div>
							<h3 className="font-medium">VPN connection issues</h3>
							<p className="text-sm text-gray-500">TKT-002 • TechStart Inc</p>
						</div>
						<span className="px-2 py-1 bg-yellow-100 text-yellow-700 text-xs rounded">In Progress</span>
					</div>
					<div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
						<div>
							<h3 className="font-medium">Software installation request</h3>
							<p className="text-sm text-gray-500">TKT-003 • Global Solutions</p>
						</div>
						<span className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded">Open</span>
					</div>
				</div>
			</div>
		</div>
	)
}
