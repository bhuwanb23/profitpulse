import { useState } from 'react'

export default function BudgetCreate() {
	const [form, setForm] = useState({ name: '', type: 'quarterly', total: '', start: '', end: '' })
	const [errors, setErrors] = useState({})
	const validate = () => {
		const e = {}
		if (!form.name) e.name = 'Name required'
		if (!form.total) e.total = 'Total required'
		if (!form.start) e.start = 'Start required'
		if (!form.end) e.end = 'End required'
		setErrors(e)
		return Object.keys(e).length === 0
	}
	const submit = (ev) => {
		ev.preventDefault()
		if (!validate()) return
		console.log('Create budget (mock)', form)
		alert('Budget created (mock).')
		setForm({ name: '', type: 'quarterly', total: '', start: '', end: '' })
	}
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Create Budget</h2>
			<form onSubmit={submit} className="mt-3 grid grid-cols-1 md:grid-cols-5 gap-3 text-sm">
				<div className="md:col-span-2">
					<label className="block text-gray-600 text-xs">Name</label>
					<input value={form.name} onChange={(e) => setForm(prev => ({ ...prev, name: e.target.value }))} className={`mt-1 w-full rounded-md border px-3 py-2 ${errors.name ? 'border-red-400' : 'border-gray-300'}`} placeholder="Budget name" />
				</div>
				<div>
					<label className="block text-gray-600 text-xs">Type</label>
					<select value={form.type} onChange={(e) => setForm(prev => ({ ...prev, type: e.target.value }))} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2">
						<option value="monthly">monthly</option>
						<option value="quarterly">quarterly</option>
						<option value="annual">annual</option>
					</select>
				</div>
				<div>
					<label className="block text-gray-600 text-xs">Total</label>
					<input type="number" min={0} value={form.total} onChange={(e) => setForm(prev => ({ ...prev, total: e.target.value }))} className={`mt-1 w-full rounded-md border px-3 py-2 ${errors.total ? 'border-red-400' : 'border-gray-300'}`} />
				</div>
				<div>
					<label className="block text-gray-600 text-xs">Start</label>
					<input value={form.start} onChange={(e) => setForm(prev => ({ ...prev, start: e.target.value }))} className={`mt-1 w-full rounded-md border px-3 py-2 ${errors.start ? 'border-red-400' : 'border-gray-300'}`} placeholder="YYYY-MM-DD" />
				</div>
				<div>
					<label className="block text-gray-600 text-xs">End</label>
					<input value={form.end} onChange={(e) => setForm(prev => ({ ...prev, end: e.target.value }))} className={`mt-1 w-full rounded-md border px-3 py-2 ${errors.end ? 'border-red-400' : 'border-gray-300'}`} placeholder="YYYY-MM-DD" />
				</div>
				<div className="md:col-span-5">
					<button type="submit" className="bg-blue-600 text-white text-sm px-4 py-2 rounded-md hover:bg-blue-700">Create Budget</button>
				</div>
			</form>
		</section>
	)
}
