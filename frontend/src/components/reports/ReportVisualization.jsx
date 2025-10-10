import { useState } from 'react'

export default function ReportVisualization() {
	const [mode, setMode] = useState('chart')
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Visualization</h2>
			<div className="mt-3 flex gap-2 text-sm">
				<button onClick={()=>setMode('chart')} className={`px-3 py-1.5 rounded ${mode==='chart'?'bg-blue-600 text-white':'bg-gray-100 hover:bg-gray-200'}`}>Chart</button>
				<button onClick={()=>setMode('table')} className={`px-3 py-1.5 rounded ${mode==='table'?'bg-blue-600 text-white':'bg-gray-100 hover:bg-gray-200'}`}>Table</button>
				<button onClick={()=>setMode('both')} className={`px-3 py-1.5 rounded ${mode==='both'?'bg-blue-600 text-white':'bg-gray-100 hover:bg-gray-200'}`}>Both</button>
			</div>
			<div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
				{(mode==='chart' || mode==='both') && <div className="h-40 bg-gradient-to-r from-blue-50 to-blue-100 rounded" />}
				{(mode==='table' || mode==='both') && (
					<table className="w-full text-sm">
						<thead className="text-left text-gray-500">
							<tr><th className="py-2">Metric</th><th className="py-2">Value</th></tr>
						</thead>
						<tbody>
							<tr className="border-t"><td className="py-2">Revenue</td><td>$124k</td></tr>
							<tr className="border-t"><td className="py-2">Tickets</td><td>482</td></tr>
							<tr className="border-t"><td className="py-2">Profitability</td><td>17.2%</td></tr>
						</tbody>
					</table>
				)}
			</div>
		</section>
	)
}
