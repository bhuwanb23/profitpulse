import { Badge } from '../ui/Badge'
import { Button } from '../ui/Button'
import { PlusIcon, CurrencyDollarIcon } from '../ui/Icons'

export function ServiceCard({ service, onAddToClient, isAssigned = false }) {
	const getCategoryColor = (category) => {
		const colors = {
			support: 'blue',
			maintenance: 'green',
			consulting: 'purple',
			security: 'orange'
		}
		return colors[category] || 'default'
	}

	const getBillingIcon = (billing) => {
		switch (billing) {
			case 'per-user':
				return '👤'
			case 'per-device':
				return '💻'
			case 'hourly':
				return '⏰'
			case 'monthly':
				return '📅'
			default:
				return '💰'
		}
	}

	const formatPrice = (price) => {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD',
			minimumFractionDigits: 0
		}).format(price)
	}

	return (
		<div className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200 p-6">
			<div className="flex flex-col h-full">
				{/* Header */}
				<div className="flex items-start justify-between mb-4">
					<div className="flex-1">
						<h3 className="font-semibold text-gray-900 text-lg mb-2">{service.name}</h3>
						<div className="flex items-center gap-2 mb-3">
							<Badge variant={getCategoryColor(service.category)} size="sm">
								{service.category}
							</Badge>
							<span className="text-sm text-gray-500 flex items-center gap-1">
								{getBillingIcon(service.billing)}
								{service.billing.replace('-', ' ')}
							</span>
						</div>
					</div>
				</div>

				{/* Description */}
				<div className="mb-4 flex-1">
					<p className="text-sm text-gray-600 leading-relaxed">
						{getServiceDescription(service.name, service.category)}
					</p>
				</div>

				{/* Pricing */}
				<div className="mb-4 p-3 bg-gray-50 rounded-lg">
					<div className="flex items-center justify-between">
						<span className="text-sm text-gray-600">Base Price</span>
						<div className="flex items-center gap-1">
							<CurrencyDollarIcon className="h-4 w-4 text-gray-400" />
							<span className="font-semibold text-gray-900">
								{formatPrice(service.basePrice)}
							</span>
							<span className="text-xs text-gray-500">
								/{service.billing.split('-')[1] || 'unit'}
							</span>
						</div>
					</div>
				</div>

				{/* Action */}
				<div className="pt-2">
					{isAssigned ? (
						<Button variant="secondary" size="sm" className="w-full" disabled>
							Already Assigned
						</Button>
					) : (
						<Button 
							variant="primary" 
							size="sm" 
							className="w-full flex items-center justify-center gap-2"
							onClick={() => onAddToClient?.(service)}
						>
							<PlusIcon className="h-4 w-4" />
							Add to Client
						</Button>
					)}
				</div>
			</div>
		</div>
	)
}

function getServiceDescription(name, category) {
	const descriptions = {
		'24/7 Help Desk': 'Round-the-clock technical support for your team with priority ticket handling and expert assistance.',
		'Network Monitoring': 'Continuous monitoring of your network infrastructure with real-time alerts and performance optimization.',
		'Cloud Migration': 'Expert consultation and implementation for seamless cloud infrastructure migration and optimization.',
		'Security Assessment': 'Comprehensive security audits and vulnerability assessments to protect your digital assets.',
		'Backup & Recovery': 'Automated backup solutions with reliable disaster recovery planning and data protection.'
	}
	
	return descriptions[name] || `Professional ${category} service designed to enhance your IT operations and business efficiency.`
}
