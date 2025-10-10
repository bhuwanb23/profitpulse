import { Link } from 'react-router-dom'

const colorClasses = {
	blue: { bg: 'bg-blue-50', text: 'text-blue-700' },
	green: { bg: 'bg-green-50', text: 'text-green-700' },
	amber: { bg: 'bg-amber-50', text: 'text-amber-700' },
	purple: { bg: 'bg-purple-50', text: 'text-purple-700' },
}

const ActionButton = ({ onClick, icon, title, desc, color = 'blue' }) => {
	const c = colorClasses[color] || colorClasses.blue
	return (
		<button onClick={onClick} className="flex items-start gap-3 rounded-xl border border-gray-200 bg-white p-4 shadow-sm hover:shadow transition">
			<div className={`h-10 w-10 flex items-center justify-center rounded-lg ${c.bg} ${c.text} text-lg`}>{icon}</div>
			<div className="text-left">
				<div className="font-medium text-sm">{title}</div>
				<div className="text-xs text-gray-500">{desc}</div>
			</div>
		</button>
	)
}

export default function QuickActions() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold mb-3">Quick Actions</h2>
			<div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-3">
				<ActionButton icon="🎫" title="New Ticket" desc="Create a support ticket" color="blue" />
				<ActionButton icon="👤" title="Add Client" desc="Create a new client" color="green" />
				<ActionButton icon="💵" title="Create Invoice" desc="Bill for services" color="amber" />
				<ActionButton icon="⬆️" title="Import CSV" desc="Upload data file" color="purple" />
			</div>
		</section>
	)
}
