export default function APIKeyManagement() {
	const keys = [
		{ id: 'k1', name: 'Backend Service', last4: '9f2a', created: '2025-09-04' },
		{ id: 'k2', name: 'CLI Tool', last4: '3c11', created: '2025-10-01' },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">API Keys</h2>
			<table className="mt-3 w-full text-sm">
				<thead className="text-left text-gray-500">
					<tr>
						<th className="py-2">Name</th>
						<th className="py-2">Key</th>
						<th className="py-2">Created</th>
						<th className="py-2 text-right">Actions</th>
					</tr>
				</thead>
				<tbody>
					{keys.map(k => (
						<tr key={k.id} className="border-t">
							<td className="py-2">{k.name}</td>
							<td className="py-2">•••• •••• •••• {k.last4}</td>
							<td className="py-2">{k.created}</td>
							<td className="py-2 text-right">
								<button className="text-xs px-2 py-1 rounded bg-gray-100 hover:bg-gray-200">Revoke</button>
							</td>
						</tr>
					))}
				</tbody>
			</table>
			<div className="mt-3">
				<button className="text-sm px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">Create API Key</button>
			</div>
		</section>
	)
}
