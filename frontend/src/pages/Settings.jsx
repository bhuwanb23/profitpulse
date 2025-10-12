export default function Settings() {
	return (
		<div className="space-y-6">
			<h1 className="text-2xl font-semibold">Settings</h1>

			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				{/* User Management */}
				<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
					<h2 className="text-lg font-semibold mb-4">User Management</h2>
					<div className="space-y-3">
						<div className="flex items-center justify-between">
							<span className="text-gray-600">Total Users</span>
							<span className="font-semibold">3</span>
						</div>
						<div className="flex items-center justify-between">
							<span className="text-gray-600">Active Users</span>
							<span className="font-semibold text-green-600">3</span>
						</div>
						<button className="w-full bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Manage Users</button>
					</div>
				</div>

				{/* Organization Settings */}
				<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
					<h2 className="text-lg font-semibold mb-4">Organization</h2>
					<div className="space-y-3">
						<div className="flex items-center justify-between">
							<span className="text-gray-600">Name</span>
							<span className="font-semibold">TechWave MSP</span>
						</div>
						<div className="flex items-center justify-between">
							<span className="text-gray-600">Plan</span>
							<span className="font-semibold text-blue-600">Enterprise</span>
						</div>
						<button className="w-full bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Edit</button>
					</div>
				</div>

				{/* Security Settings */}
				<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
					<h2 className="text-lg font-semibold mb-4">Security</h2>
					<div className="space-y-3">
						<div className="flex items-center justify-between">
							<span className="text-gray-600">2FA</span>
							<span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">Enabled</span>
						</div>
						<div className="flex items-center justify-between">
							<span className="text-gray-600">Password Policy</span>
							<span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">Strong</span>
						</div>
						<button className="w-full bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Configure</button>
					</div>
				</div>

				{/* Integrations */}
				<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
					<h2 className="text-lg font-semibold mb-4">Integrations</h2>
					<div className="space-y-3">
						<div className="flex items-center justify-between">
							<span className="text-gray-600">SuperOps</span>
							<span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">Connected</span>
						</div>
						<div className="flex items-center justify-between">
							<span className="text-gray-600">QuickBooks</span>
							<span className="px-2 py-1 bg-yellow-100 text-yellow-700 text-xs rounded">Pending</span>
						</div>
						<button className="w-full bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Manage</button>
					</div>
				</div>
			</div>
		</div>
	)
}
