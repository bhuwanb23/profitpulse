import { useMemo } from 'react'
import { KPICard } from '../components/clients/KPICard'
import { Button } from '../components/ui/Button'
import { 
	DocumentTextIcon,
	ChartBarIcon,
	DocumentDownloadIcon,
	ClockIcon,
	TrendingUpIcon,
	EyeIcon,
	CalendarIcon,
	RefreshIcon
} from '../components/ui/Icons'

import ReportBuilder from '../components/reports/ReportBuilder'
import ReportTemplates from '../components/reports/ReportTemplates'
import ReportExports from '../components/reports/ReportExports'
import ReportVisualization from '../components/reports/ReportVisualization'
import ComparativeAnalysis from '../components/reports/ComparativeAnalysis'
import ReportScheduler from '../components/reports/ReportScheduler'

export default function Reports() {
	// Reports analytics data
	const reportsData = useMemo(() => {
		return {
			totalReports: 156,
			reportsThisMonth: 24,
			scheduledReports: 8,
			avgGenerationTime: 2.3,
			exportedReports: 89,
			templatesUsed: 12,
			recentActivity: [
				{ name: 'Monthly Revenue Report', generated: '2 hours ago', type: 'PDF' },
				{ name: 'Client Profitability Analysis', generated: '5 hours ago', type: 'Excel' },
				{ name: 'SLA Compliance Report', generated: '1 day ago', type: 'CSV' },
				{ name: 'Department Performance', generated: '2 days ago', type: 'PDF' }
			]
		}
	}, [])

	return (
		<div className="space-y-6">
			{/* Header */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold bg-gradient-to-r from-emerald-600 via-blue-600 to-purple-600 bg-clip-text text-transparent">
						📊 Reports & Analytics
					</h1>
					<p className="text-gray-600 mt-1">Generate, schedule, and export comprehensive business reports</p>
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<CalendarIcon className="h-4 w-4" />
						Schedule Report
					</Button>
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<DocumentDownloadIcon className="h-4 w-4" />
						Export All
					</Button>
					<Button variant="primary" size="sm" className="flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-blue-600">
						<RefreshIcon className="h-4 w-4" />
						Refresh Data
					</Button>
				</div>
			</div>

			{/* KPI Cards */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
				<KPICard
					title="Total Reports"
					value={reportsData.totalReports}
					change={12.5}
					changeType="positive"
					format="number"
					icon={DocumentTextIcon}
					iconColor="emerald"
				/>
				<KPICard
					title="This Month"
					value={reportsData.reportsThisMonth}
					change={8.3}
					changeType="positive"
					format="number"
					icon={TrendingUpIcon}
					iconColor="blue"
				/>
				<KPICard
					title="Scheduled Reports"
					value={reportsData.scheduledReports}
					change={2}
					changeType="positive"
					format="number"
					icon={ClockIcon}
					iconColor="purple"
				/>
				<KPICard
					title="Avg Generation Time"
					value={reportsData.avgGenerationTime}
					change={-15.2}
					changeType="positive"
					format="decimal"
					icon={ChartBarIcon}
					iconColor="orange"
					suffix="s"
				/>
				<KPICard
					title="Exported Reports"
					value={reportsData.exportedReports}
					change={18.7}
					changeType="positive"
					format="number"
					icon={DocumentDownloadIcon}
					iconColor="teal"
				/>
				<KPICard
					title="Templates Used"
					value={reportsData.templatesUsed}
					change={5.4}
					changeType="positive"
					format="number"
					icon={EyeIcon}
					iconColor="rose"
				/>
			</div>

			{/* Main Report Builder */}
			<div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
				<div className="xl:col-span-2">
					<ReportBuilder />
				</div>
				<div className="space-y-6">
					<ReportTemplates />
					<ReportExports />
				</div>
			</div>

			{/* Visualization and Analysis */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<ReportVisualization />
				<ComparativeAnalysis />
			</div>

			{/* Scheduler and Recent Activity */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<ReportScheduler />
				
				{/* Recent Activity */}
				<div className="bg-gradient-to-br from-gray-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
					<h2 className="text-lg font-semibold bg-gradient-to-r from-gray-700 to-gray-900 bg-clip-text text-transparent mb-4">
						Recent Report Activity
					</h2>
					<div className="space-y-3">
						{reportsData.recentActivity.map((activity, index) => (
							<div key={index} className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-100 hover:border-gray-200 transition-colors">
								<div className="flex items-center gap-3">
									<div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
										<DocumentTextIcon className="h-4 w-4 text-white" />
									</div>
									<div>
										<p className="font-medium text-gray-900">{activity.name}</p>
										<p className="text-sm text-gray-500">{activity.generated}</p>
									</div>
								</div>
								<span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
									{activity.type}
								</span>
							</div>
						))}
					</div>
				</div>
			</div>
		</div>
	)
}
