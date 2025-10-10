import TicketVolumeTrends from '../components/tickets/analytics/TicketVolumeTrends'
import ResolutionTimeAnalytics from '../components/tickets/analytics/ResolutionTimeAnalytics'
import CategoryBreakdown from '../components/tickets/analytics/CategoryBreakdown'
import TechnicianPerformance from '../components/tickets/analytics/TechnicianPerformance'
import SLACompliance from '../components/tickets/analytics/SLACompliance'
import CSATScores from '../components/tickets/analytics/CSATScores'

export default function TicketAnalyticsPage() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Ticket Analytics</h1>
				<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Export</button>
			</div>
			<TicketVolumeTrends />
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<ResolutionTimeAnalytics />
				<CategoryBreakdown />
				<TechnicianPerformance />
				<SLACompliance />
				<CSATScores />
			</div>
		</div>
	)
}
