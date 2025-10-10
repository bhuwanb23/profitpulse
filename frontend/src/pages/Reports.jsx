import ReportBuilder from '../components/reports/ReportBuilder'
import ReportTemplates from '../components/reports/ReportTemplates'
import ReportExports from '../components/reports/ReportExports'
import ReportVisualization from '../components/reports/ReportVisualization'
import ComparativeAnalysis from '../components/reports/ComparativeAnalysis'
import ReportScheduler from '../components/reports/ReportScheduler'

export default function Reports() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Reports</h1>
				<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Refresh</button>
			</div>
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<ReportBuilder />
				<ReportTemplates />
				<ReportVisualization />
				<ComparativeAnalysis />
				<ReportExports />
				<ReportScheduler />
			</div>
		</div>
	)
}
