export default function UserProfile() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Profile</h2>
			<div className="mt-4 grid grid-cols-1 gap-4">
				<div>
					<label className="text-sm text-gray-600">Name</label>
					<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="Your name" />
				</div>
				<div>
					<label className="text-sm text-gray-600">Email</label>
					<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="you@example.com" />
				</div>
				<div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
					<div>
						<label className="text-sm text-gray-600">Password</label>
						<input type="password" className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="••••••••" />
					</div>
					<div>
						<label className="text-sm text-gray-600">Confirm Password</label>
						<input type="password" className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="••••••••" />
					</div>
				</div>
				<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700 w-max">Save</button>
			</div>
		</section>
	)
}
