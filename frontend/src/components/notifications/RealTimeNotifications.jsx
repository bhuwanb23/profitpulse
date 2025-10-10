import { useState } from 'react'

export default function RealTimeNotifications() {
	const [items] = useState([
		{ id: 'n1', at: '09:12', text: 'Ticket #1042 escalated to P2' },
		{ id: 'n2', at: '09:18', text: 'Invoice #2201 payment received' },
		{ id: 'n3', at: '09:22', text: 'Revenue forecast updated' },
	])
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Real-time Notifications</h2>
			<ul className="mt-3 space-y-2 text-sm">
				{items.map(i => (
					<li key={i.id} className="p-2 border rounded flex items-center justify-between">
						<span>{i.text}</span>
						<span className="text-xs text-gray-500">{i.at}</span>
					</li>
				))}
			</ul>
		</section>
	)
}
