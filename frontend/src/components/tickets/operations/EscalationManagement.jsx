import { useState } from 'react'

export default function EscalationManagement() {
	const [level, setLevel] = useState('none')
	const [priority, setPriority] = useState('medium')

	const save = () => {
		console.log('Escalation updated', { level, priority })
		alert('Escalation settings saved (mock).')
	}

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Escalation Management</h2>
			<div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
				<div>
					<label className="block text-gray-600 text-xs">Escalation Level</label>
					<select value={level} onChange={(e) => setLevel(e.target.value)} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
						<option value="none">None</option>
						<option value="l1">L1</option>
						<option value="l2">L2</option>
						<option value="l3">L3</option>
					</select>
				</div>
				<div>
					<label className="block text-gray-600 text-xs">Priority Override</label>
					<select value={priority} onChange={(e) => setPriority(e.target.value)} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
						<option value="low">low</option>
						<option value="medium">medium</option>
						<option value="high">high</option>
						<option value="critical">critical</option>
					</select>
				</div>
				<div className="flex items-end">
					<button onClick={save} className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Save</button>
				</div>
			</div>
		</section>
	)
}
