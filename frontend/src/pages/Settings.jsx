export default function Settings() {
	return (
		<div className="space-y-6">
			<h1 className="text-2xl font-semibold">Settings</h1>

			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<h2 className="font-semibold">Profile</h2>
					<div className="mt-4 space-y-4">
						<div>
							<label className="text-sm text-gray-600">Name</label>
							<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="Your name" />
						</div>
						<div>
							<label className="text-sm text-gray-600">Email</label>
							<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="you@example.com" />
						</div>
						<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Save</button>
					</div>
				</section>

				<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<h2 className="font-semibold">Organization</h2>
					<div className="mt-4 space-y-4">
						<div>
							<label className="text-sm text-gray-600">Organization Name</label>
							<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="Company Inc" />
						</div>
						<div>
							<label className="text-sm text-gray-600">Plan</label>
							<select className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
								<option>Basic</option>
								<option>Pro</option>
								<option>Enterprise</option>
							</select>
						</div>
						<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Update</button>
					</div>
				</section>
			</div>
		</div>
	)
}
