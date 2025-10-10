export default function OrganizationSettings() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Organization</h2>
			<div className="mt-4 space-y-3 text-sm">
				<label className="block">
					<span className="text-sm text-gray-600">Organization Name</span>
					<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2" placeholder="Company Inc" />
				</label>
				<label className="block">
					<span className="text-sm text-gray-600">Plan</span>
					<select className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2">
						<option>Basic</option>
						<option>Pro</option>
						<option>Enterprise</option>
					</select>
				</label>
				<button className="text-sm px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 w-max">Update</button>
			</div>
		</section>
	)
}
