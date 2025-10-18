export function CustomTooltip({ formatCurrency }) {
	return ({ active, payload, label }) => {
		if (active && payload && payload.length) {
			return (
				<div className="bg-white/95 backdrop-blur-sm p-4 border border-gray-200 rounded-xl shadow-xl">
					<p className="font-semibold text-gray-900 mb-2">{label}</p>
					{payload.map((entry, index) => (
						<div key={index} className="flex items-center gap-2 mb-1">
							<div 
								className="w-3 h-3 rounded-full" 
								style={{ backgroundColor: entry.color }}
							/>
							<span className="text-sm font-medium" style={{ color: entry.color }}>
								{entry.name}: {entry.name.includes('Growth') || entry.name.includes('Margin') ? 
									`${entry.value}%` : 
									entry.name.includes('Revenue') || entry.name.includes('Profit') || entry.name.includes('amount') ? 
									formatCurrency(entry.value) : entry.value}
							</span>
						</div>
					))}
				</div>
			)
		}
		return null
	}
}
