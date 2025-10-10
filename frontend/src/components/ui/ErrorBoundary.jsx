import { Component } from 'react'

export default class ErrorBoundary extends Component {
	constructor(props) {
		super(props)
		this.state = { hasError: false }
	}

	static getDerivedStateFromError() {
		return { hasError: true }
	}

	componentDidCatch(error, info) {
		// log to monitoring here
		console.error('ErrorBoundary caught', error, info)
	}

	render() {
		if (this.state.hasError) {
			return (
				<div className="min-h-[50vh] grid place-items-center">
					<div className="text-center">
						<h2 className="text-lg font-semibold">Something went wrong</h2>
						<p className="text-sm text-gray-500 mt-1">Please refresh the page or try again later.</p>
					</div>
				</div>
			)
		}
		return this.props.children
	}
}
