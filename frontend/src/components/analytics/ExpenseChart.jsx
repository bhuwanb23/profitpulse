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
						<PieChart>
							<Pie
								data={data}
								cx="50%"
								cy="50%"
								outerRadius={80}
								dataKey="amount"
								label={({ category, percentage }) => `${category}: ${percentage}%`}
								labelLine={false}
							>
								{data.map((entry, index) => (
									<Cell key={`cell-${index}`} fill={entry.fill} />
								))}
							</Pie>
							<Tooltip 
								formatter={(value) => [formatCurrency(value), 'Amount']}
							/>
						</PieChart>
					</ResponsiveContainer>
				</div>
			</CardContent>
		</Card>
	)
}
