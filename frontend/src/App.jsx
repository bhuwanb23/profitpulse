import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import './App.css'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import Clients from './pages/Clients'
import Tickets from './pages/Tickets'
import Invoices from './pages/Invoices'
import Analytics from './pages/Analytics'
import Settings from './pages/Settings'
import Login from './pages/Login'
import Register from './pages/Register'
import { AuthProvider } from './contexts/AuthContext'
import ProtectedRoute from './components/routing/ProtectedRoute'
import AIInsights from './pages/AIInsights'
import ClientServicesPage from './pages/ClientServices'
import ClientAnalyticsPage from './pages/ClientAnalytics'
import TicketAnalyticsPage from './pages/TicketAnalytics'
import TicketOperationsPage from './pages/TicketOperations'
import BillingAnalyticsPage from './pages/BillingAnalytics'
import BudgetManagementPage from './pages/BudgetManagement'
import Reports from './pages/Reports'
import Notifications from './pages/Notifications'

function App() {
	return (
		<BrowserRouter>
			<AuthProvider>
				<Routes>
					<Route path="/login" element={<Login />} />
					<Route path="/register" element={<Register />} />

					<Route element={<ProtectedRoute />}> 
						<Route element={<Layout />}> 
							<Route index element={<Dashboard />} />
							<Route path="dashboard" element={<Dashboard />} />
							<Route path="clients/*" element={<Clients />} />
							<Route path="client-services/:id?" element={<ClientServicesPage />} />
							<Route path="client-analytics/:id?" element={<ClientAnalyticsPage />} />
							<Route path="tickets/*" element={<Tickets />} />
							<Route path="ticket-analytics" element={<TicketAnalyticsPage />} />
							<Route path="ticket-operations" element={<TicketOperationsPage />} />
							<Route path="invoices/*" element={<Invoices />} />
							<Route path="analytics" element={<Analytics />} />
							<Route path="reports" element={<Reports />} />
							<Route path="billing-analytics" element={<BillingAnalyticsPage />} />
							<Route path="budget-management" element={<BudgetManagementPage />} />
							<Route path="ai" element={<AIInsights />} />
							<Route path="notifications" element={<Notifications />} />
							<Route path="settings" element={<Settings />} />
							<Route path="*" element={<Navigate to="/dashboard" replace />} />
						</Route>
					</Route>
				</Routes>
			</AuthProvider>
		</BrowserRouter>
	)
}

export default App
