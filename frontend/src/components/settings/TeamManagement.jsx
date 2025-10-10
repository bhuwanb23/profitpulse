export default function TeamManagement() {
	const members = [
		{ id: 'u1', name: 'Alex Carter', role: 'Admin', email: 'alex@example.com' },
		{ id: 'u2', name: 'Sam Lee', role: 'Manager', email: 'sam@example.com' },
		{ id: 'u3', name: 'Jamie Doe', role: 'Agent', email: 'jamie@example.com' },
	]
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Team Members</h2>
			<div className="mt-4">
				<table className="w-full text-sm">
					<thead className="text-left text-gray-500">
						<tr>
							<th className="py-2">Name</th>
							<th className="py-2">Email</th>
							<th className="py-2">Role</th>
							<th className="py-2 text-right">Actions</th>
						</tr>
					</thead>
					<tbody>
						{members.map(m => (
							<tr key={m.id} className="border-t">
								<td className="py-2">{m.name}</td>
								<td className="py-2">{m.email}</td>
								<td className="py-2">{m.role}</td>
								<td className="py-2 text-right">
									<button className="text-xs px-2 py-1 rounded bg-gray-100 hover:bg-gray-200">Edit</button>
								</td>
							</tr>
						))}
					</tbody>
				</table>
				<div className="mt-3">
					<button className="text-sm px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">Add member</button>
				</div>
			</div>
		</section>
	)
}
