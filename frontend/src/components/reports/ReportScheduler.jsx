import { useState } from 'react'

export default function ReportScheduler() {
	const [frequency, setFrequency] = useState('weekly')
	const [recipients, setRecipients] = useState('')
	const [reportType, setReportType] = useState('revenue')

	const scheduledReports = [
		{ name: 'Weekly Revenue Report', frequency: 'Weekly', nextRun: 'Monday 9:00 AM', recipients: 3 },
		{ name: 'Monthly Analytics', frequency: 'Monthly', nextRun: '1st of month', recipients: 5 }
	]

	return (
		<section className="bg-gradient-to-br from-cyan-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<h2 className="text-lg font-semibold bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent mb-4">
				Report Scheduler
			</h2>
			
			{/* Schedule New Report */}
			<div className="bg-white rounded-lg border border-gray-200 p-4 mb-4">
				<h3 className="text-sm font-medium text-gray-700 mb-3">Schedule New Report</h3>
				<div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
					<label className="block">
						<span className="text-gray-600 font-medium">Report Type</span>
						<select 
							className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
							value={reportType}
							onChange={(e) => setReportType(e.target.value)}
						>
							<option value="revenue">Revenue Report</option>
							<option value="analytics">Analytics Summary</option>
							<option value="performance">Performance Report</option>
						</select>
					</label>
					<label className="block">
						<span className="text-gray-600 font-medium">Frequency</span>
						<select 
							className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
							value={frequency}
							onChange={(e) => setFrequency(e.target.value)}
						>
							<option value="daily">Daily</option>
							<option value="weekly">Weekly</option>
							<option value="monthly">Monthly</option>
							<option value="quarterly">Quarterly</option>
						</select>
					</label>
					<label className="block">
						<span className="text-gray-600 font-medium">Recipients</span>
						<input 
							className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-cyan-500 focus:border-transparent" 
							placeholder="email@example.com"
							value={recipients}
							onChange={(e) => setRecipients(e.target.value)}
						/>
					</label>
				</div>
				<div className="mt-4 flex gap-2">
					<button className="px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-600 to-blue-600 text-white text-sm font-medium hover:from-cyan-700 hover:to-blue-700 transition-all">
						Schedule Report
					</button>
					<button className="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 text-sm font-medium hover:bg-gray-50 transition-colors">
						Save as Draft
					</button>
				</div>
			</div>

			{/* Existing Scheduled Reports */}
			<div className="bg-white rounded-lg border border-gray-200 p-4">
				<h3 className="text-sm font-medium text-gray-700 mb-3">Active Schedules</h3>
				<div className="space-y-3">
					{scheduledReports.map((report, index) => (
						<div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
							<div>
								<p className="font-medium text-gray-900 text-sm">{report.name}</p>
								<p className="text-xs text-gray-500">
									{report.frequency} • Next: {report.nextRun} • {report.recipients} recipients
								</p>
							</div>
							<div className="flex gap-2">
								<button className="px-2 py-1 rounded bg-blue-100 text-blue-800 text-xs font-medium hover:bg-blue-200 transition-colors">
									Edit
								</button>
								<button className="px-2 py-1 rounded bg-red-100 text-red-800 text-xs font-medium hover:bg-red-200 transition-colors">
									Delete
								</button>
							</div>
						</div>
					))}
				</div>
			</div>
		</section>
	)
}
