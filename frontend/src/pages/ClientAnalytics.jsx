import ClientAnalytics from '../components/clients/ClientAnalytics'
import { useParams } from 'react-router-dom'

export default function ClientAnalyticsPage() {
	useParams() // placeholder if needed later
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Client Analytics</h1>
			</div>
			<ClientAnalytics />
		</div>
	)
}
