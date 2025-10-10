export default function RolesPermissions() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Roles & Permissions</h2>
			<div className="mt-4 space-y-3 text-sm">
				<div className="flex items-center justify-between p-3 border rounded">
					<div>
						<div className="font-medium">Admin</div>
						<div className="text-xs text-gray-500">Full access</div>
					</div>
					<button className="px-2 py-1 text-xs rounded bg-gray-100 hover:bg-gray-200">Edit</button>
				</div>
				<div className="flex items-center justify-between p-3 border rounded">
					<div>
						<div className="font-medium">Manager</div>
						<div className="text-xs text-gray-500">Limited admin</div>
					</div>
					<button className="px-2 py-1 text-xs rounded bg-gray-100 hover:bg-gray-200">Edit</button>
				</div>
				<div className="flex items-center justify-between p-3 border rounded">
					<div>
						<div className="font-medium">Agent</div>
						<div className="text-xs text-gray-500">Tickets & clients</div>
					</div>
					<button className="px-2 py-1 text-xs rounded bg-gray-100 hover:bg-gray-200">Edit</button>
				</div>
			</div>
		</section>
	)
}
