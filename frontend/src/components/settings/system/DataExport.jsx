export default function DataExport() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Data Export</h2>
			<div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
				<button className="p-3 border rounded bg-gray-50 hover:bg-gray-100">Export CSV</button>
				<button className="p-3 border rounded bg-gray-50 hover:bg-gray-100">Export JSON</button>
				<button className="p-3 border rounded bg-gray-50 hover:bg-gray-100">Export XLSX</button>
				<button className="p-3 border rounded bg-gray-50 hover:bg-gray-100">Export PDF</button>
			</div>
		</section>
	)
}
