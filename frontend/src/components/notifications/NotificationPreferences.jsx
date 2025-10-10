export default function NotificationPreferences() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Notification Preferences</h2>
			<div className="mt-3 space-y-2 text-sm">
				<label className="flex items-center gap-2"><input type="checkbox" defaultChecked /> In-app notifications</label>
				<label className="flex items-center gap-2"><input type="checkbox" /> Email notifications</label>
				<label className="flex items-center gap-2"><input type="checkbox" /> Sound on new alerts</label>
			</div>
		</section>
	)
}
