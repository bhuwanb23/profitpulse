export default function ThemeCustomization() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Theme</h2>
			<div className="mt-3 grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
				<button className="p-3 border rounded bg-gray-50 hover:bg-gray-100">Light</button>
				<button className="p-3 border rounded bg-gray-900 text-white hover:bg-gray-800">Dark</button>
				<button className="p-3 border rounded bg-blue-50 hover:bg-blue-100">System</button>
			</div>
		</section>
	)
}
