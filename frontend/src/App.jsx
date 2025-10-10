import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import './App.css'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import Clients from './pages/Clients'
import Tickets from './pages/Tickets'
import Invoices from './pages/Invoices'
import Analytics from './pages/Analytics'
import Settings from './pages/Settings'

function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route element={<Layout />}> 
					<Route index element={<Dashboard />} />
					<Route path="dashboard" element={<Dashboard />} />
					<Route path="clients" element={<Clients />} />
					<Route path="tickets" element={<Tickets />} />
					<Route path="invoices" element={<Invoices />} />
					<Route path="analytics" element={<Analytics />} />
					<Route path="settings" element={<Settings />} />
					<Route path="*" element={<Navigate to="/dashboard" replace />} />
				</Route>
			</Routes>
		</BrowserRouter>
	)
}

export default App
