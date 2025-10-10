export default function SecuritySettings() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Security</h2>
			<div className="mt-4 space-y-3 text-sm">
				<label className="flex items-center gap-2"><input type="checkbox" defaultChecked /> Enable 2FA</label>
				<label className="flex items-center gap-2"><input type="checkbox" /> Require strong passwords</label>
				<label className="flex items-center gap-2"><input type="checkbox" /> Session timeout after 20m</label>
				<button className="mt-2 text-sm px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 w-max">Save</button>
			</div>
		</section>
	)
}
