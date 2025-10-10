export default function EmailAlertSettings() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Email Alert Settings</h2>
			<div className="mt-3 space-y-2 text-sm">
				<label className="flex items-center gap-2"><input type="checkbox" defaultChecked /> Billing events</label>
				<label className="flex items-center gap-2"><input type="checkbox" /> Ticket escalations</label>
				<label className="flex items-center gap-2"><input type="checkbox" defaultChecked /> Weekly summaries</label>
			</div>
		</section>
	)
}
