import { useState } from 'react'
import { mockTicketCategories } from '../../../services/mockTickets'

export default function NewTicketForm() {
	const [form, setForm] = useState({ title: '', client: '', category: 'infrastructure', priority: 'medium', description: '' })
	const [errors, setErrors] = useState({})

	const validate = () => {
		const e = {}
		if (!form.title) e.title = 'Title is required'
		if (!form.client) e.client = 'Client is required'
		if (!form.description) e.description = 'Description is required'
		setErrors(e)
		return Object.keys(e).length === 0
	}

	const onSubmit = (ev) => {
		ev.preventDefault()
		if (!validate()) return
		console.log('Creating ticket (mock):', form)
		alert('Ticket created (mock).')
		setForm({ title: '', client: '', category: 'infrastructure', priority: 'medium', description: '' })
	}

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Create New Ticket</h2>
			<form onSubmit={onSubmit} className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
				<div>
					<label className="block text-gray-600 text-xs">Title</label>
					<input value={form.title} onChange={(e) => setForm(prev => ({ ...prev, title: e.target.value }))} className={`mt-1 w-full rounded-md border px-3 py-2 ${errors.title ? 'border-red-400' : 'border-gray-300'}`} placeholder="Issue title" />
					{errors.title && <p className="text-xs text-red-600 mt-1">{errors.title}</p>}
				</div>
				<div>
					<label className="block text-gray-600 text-xs">Client</label>
					<input value={form.client} onChange={(e) => setForm(prev => ({ ...prev, client: e.target.value }))} className={`mt-1 w-full rounded-md border px-3 py-2 ${errors.client ? 'border-red-400' : 'border-gray-300'}`} placeholder="Client name" />
					{errors.client && <p className="text-xs text-red-600 mt-1">{errors.client}</p>}
				</div>
				<div>
					<label className="block text-gray-600 text-xs">Category</label>
					<select value={form.category} onChange={(e) => setForm(prev => ({ ...prev, category: e.target.value }))} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2">
						{mockTicketCategories.map(c => <option key={c} value={c}>{c}</option>)}
					</select>
				</div>
				<div>
					<label className="block text-gray-600 text-xs">Priority</label>
					<select value={form.priority} onChange={(e) => setForm(prev => ({ ...prev, priority: e.target.value }))} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2">
						<option value="low">low</option>
						<option value="medium">medium</option>
						<option value="high">high</option>
						<option value="critical">critical</option>
					</select>
				</div>
				<div className="md:col-span-2">
					<label className="block text-gray-600 text-xs">Description</label>
					<textarea value={form.description} onChange={(e) => setForm(prev => ({ ...prev, description: e.target.value }))} className={`mt-1 w-full rounded-md border px-3 py-2 h-28 ${errors.description ? 'border-red-400' : 'border-gray-300'}`} placeholder="Describe the issue" />
					{errors.description && <p className="text-xs text-red-600 mt-1">{errors.description}</p>}
				</div>
				<div className="md:col-span-2">
					<button type="submit" className="bg-blue-600 text-white text-sm px-4 py-2 rounded-md hover:bg-blue-700">Create Ticket</button>
				</div>
			</form>
		</section>
	)
}
