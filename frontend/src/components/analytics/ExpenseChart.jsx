import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import { CurrencyDollarIcon } from '../ui/Icons'

export function ExpenseChart({ data, formatCurrency }) {
	return (
		<Card className="bg-gradient-to-br from-rose-50 to-pink-50 border-rose-200">
			<CardHeader>
				<CardTitle className="flex items-center gap-2">
					<CurrencyDollarIcon className="h-5 w-5 text-rose-600" />
					<span className="bg-gradient-to-r from-rose-600 to-pink-600 bg-clip-text text-transparent font-bold">
						Expense Breakdown
					</span>
				</CardTitle>
			</CardHeader>
			<CardContent>
				<div className="h-64">
					<ResponsiveContainer width="100%" height="100%">
						<PieChart width={400} height={300}>
							<Pie
								data={data || []}
								cx="50%"
								cy="50%"
								outerRadius={80}
								dataKey="amount"
								nameKey="category"
								label={({ category, percentage }) => `${category}: ${percentage}%`}
								labelLine={false}
							>
								{(data || []).map((entry, index) => (
									<Cell key={`cell-${index}`} fill={entry.fill || '#8884d8'} />
								))}
							</Pie>
							<Tooltip 
								formatter={(value) => [formatCurrency ? formatCurrency(value) : `$${value}`, 'Amount']}
								contentStyle={{ 
									backgroundColor: 'rgba(255, 255, 255, 0.95)', 
									border: '1px solid #e5e7eb',
									borderRadius: '8px',
									backdropFilter: 'blur(8px)'
								}}
							/>
						</PieChart>
					</ResponsiveContainer>
				</div>
			</CardContent>
		</Card>
	)
}
