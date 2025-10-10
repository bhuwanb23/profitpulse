export default function AccessControl() {
	const resources = [
		{ id: 'r1', name: 'Clients', perms: ['read', 'write'] },
		{ id: 'r2', name: 'Tickets', perms: ['read', 'write'] },
		{ id: 'r3', name: 'Invoices', perms: ['read'] },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Access Control</h2>
			<table className="mt-4 w-full text-sm">
				<thead className="text-left text-gray-500">
					<tr>
						<th className="py-2">Resource</th>
						<th className="py-2">Read</th>
						<th className="py-2">Write</th>
					</tr>
				</thead>
				<tbody>
					{resources.map(r => (
						<tr key={r.id} className="border-t">
							<td className="py-2">{r.name}</td>
							<td className="py-2"><input type="checkbox" defaultChecked={r.perms.includes('read')} /></td>
							<td className="py-2"><input type="checkbox" defaultChecked={r.perms.includes('write')} /></td>
						</tr>
					))}
				</tbody>
			</table>
		</section>
	)
}
