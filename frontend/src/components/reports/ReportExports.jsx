export default function ReportExports() {
	const exportOptions = [
		{ format: 'PDF', icon: '📄', color: 'from-red-500 to-red-600', description: 'Portable document' },
		{ format: 'Excel', icon: '📊', color: 'from-green-500 to-green-600', description: 'Spreadsheet format' },
		{ format: 'CSV', icon: '📋', color: 'from-blue-500 to-blue-600', description: 'Comma separated' },
		{ format: 'JSON', icon: '🔧', color: 'from-purple-500 to-purple-600', description: 'Data format' }
	]

	return (
		<section className="bg-gradient-to-br from-orange-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<h2 className="text-lg font-semibold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-4">
				Export Options
			</h2>
			<div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
				{exportOptions.map((option, index) => (
					<button 
						key={index}
						className="group bg-white rounded-lg border border-gray-200 p-4 hover:border-gray-300 transition-all hover:shadow-sm text-left"
					>
						<div className="flex items-center gap-3">
							<div className={`w-10 h-10 rounded-lg bg-gradient-to-r ${option.color} flex items-center justify-center text-white text-lg group-hover:scale-105 transition-transform`}>
								{option.icon}
							</div>
							<div>
								<p className="font-medium text-gray-900 text-sm">Export {option.format}</p>
								<p className="text-xs text-gray-500">{option.description}</p>
							</div>
						</div>
					</button>
				))}
			</div>
			
			{/* Quick Export Actions */}
			<div className="mt-4 pt-4 border-t border-gray-200">
				<div className="flex flex-wrap gap-2">
					<button className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-orange-600 to-red-600 text-white text-xs font-medium hover:from-orange-700 hover:to-red-700 transition-all">
						Export All
					</button>
					<button className="px-3 py-1.5 rounded-lg border border-gray-300 text-gray-700 text-xs font-medium hover:bg-gray-50 transition-colors">
						Schedule Export
					</button>
				</div>
			</div>
		</section>
	)
}
