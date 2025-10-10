import { useState } from 'react'

export default function SLAMonitor() {
	const [targets, setTargets] = useState({ responseMins: 30, resolveHours: 4 })
	const [compliance, setCompliance] = useState({ response: 96, resolve: 92 })

	const update = () => {
		console.log('SLA targets updated', targets)
		alert('SLA targets saved (mock).')
	}

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">SLA Monitoring</h2>
			<div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
				<div>
					<label className="block text-gray-600 text-xs">Target Response (mins)</label>
					<input type="number" value={targets.responseMins} onChange={(e) => setTargets(prev => ({ ...prev, responseMins: Number(e.target.value) }))} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm" />
				</div>
				<div>
					<label className="block text-gray-600 text-xs">Target Resolve (hours)</label>
					<input type="number" value={targets.resolveHours} onChange={(e) => setTargets(prev => ({ ...prev, resolveHours: Number(e.target.value) }))} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm" />
				</div>
				<div className="flex items-end">
					<button onClick={update} className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Save</button>
				</div>
			</div>
			<div className="mt-4 grid grid-cols-2 gap-4">
				<div className="p-3 border border-gray-200 rounded-lg">
					<div className="text-xs text-gray-500">Response Compliance</div>
					<div className="text-lg font-semibold">{compliance.response}%</div>
					<div className="mt-1 h-2 w-full bg-gray-100 rounded-full"><div className="h-2 bg-emerald-500 rounded-full" style={{ width: `${compliance.response}%` }} /></div>
				</div>
				<div className="p-3 border border-gray-200 rounded-lg">
					<div className="text-xs text-gray-500">Resolve Compliance</div>
					<div className="text-lg font-semibold">{compliance.resolve}%</div>
					<div className="mt-1 h-2 w-full bg-gray-100 rounded-full"><div className="h-2 bg-emerald-500 rounded-full" style={{ width: `${compliance.resolve}%` }} /></div>
				</div>
			</div>
		</section>
	)
}
