import { Routes, Route, useNavigate } from 'react-router-dom'
import ClientListTable from '../components/clients/ClientListTable'
import ClientDetail from '../components/clients/ClientDetail'

export default function Clients() {
	const navigate = useNavigate()
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Clients</h1>
				<div className="flex gap-2">
					<button onClick={() => navigate('/clients/new')} className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">+ New Client</button>
				</div>
			</div>
			<Routes>
				<Route index element={<ClientListTable />} />
				<Route path=":id" element={<ClientDetail />} />
			</Routes>
		</div>
	)
}

