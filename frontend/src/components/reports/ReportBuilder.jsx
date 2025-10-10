import { useState } from 'react'

export default function ReportBuilder() {
	const [dateRange, setDateRange] = useState('last_30')
	const [metrics, setMetrics] = useState({ revenue: true, tickets: true, profitability: false })
	const [groupBy, setGroupBy] = useState('month')

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Custom Report Builder</h2>
			<div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
				<label className="block">
					<span className="text-gray-600">Date Range</span>
					<select className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2" value={dateRange} onChange={(e)=>setDateRange(e.target.value)}>
						<option value="last_7">Last 7 days</option>
						<option value="last_30">Last 30 days</option>
						<option value="last_quarter">Last quarter</option>
						<option value="ytd">Year to date</option>
					</select>
				</label>
				<div>
					<span className="text-gray-600">Metrics</span>
					<div className="mt-1 grid grid-cols-2 gap-2">
						<label className="flex items-center gap-2"><input type="checkbox" checked={metrics.revenue} onChange={()=>setMetrics(m=>({ ...m, revenue: !m.revenue }))} /> Revenue</label>
						<label className="flex items-center gap-2"><input type="checkbox" checked={metrics.tickets} onChange={()=>setMetrics(m=>({ ...m, tickets: !m.tickets }))} /> Tickets</label>
						<label className="flex items-center gap-2"><input type="checkbox" checked={metrics.profitability} onChange={()=>setMetrics(m=>({ ...m, profitability: !m.profitability }))} /> Profitability</label>
					</div>
				</div>
				<label className="block">
					<span className="text-gray-600">Group By</span>
					<select className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2" value={groupBy} onChange={(e)=>setGroupBy(e.target.value)}>
						<option value="day">Day</option>
						<option value="week">Week</option>
						<option value="month">Month</option>
						<option value="quarter">Quarter</option>
					</select>
				</label>
			</div>
			<div className="mt-4 h-40 rounded border border-dashed grid place-items-center text-gray-500 text-sm">Preview (chart/table)</div>
			<div className="mt-3 flex gap-2">
				<button className="px-3 py-2 rounded bg-blue-600 text-white text-sm hover:bg-blue-700">Run</button>
				<button className="px-3 py-2 rounded bg-gray-100 text-sm hover:bg-gray-200">Save as Template</button>
			</div>
		</section>
	)
}
