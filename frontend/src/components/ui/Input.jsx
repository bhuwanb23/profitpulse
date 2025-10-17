export function Input({ 
	className = "", 
	type = "text",
	error = false,
	...props 
}) {
	const baseClasses = "block w-full rounded-lg border px-3 py-2 text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-0 transition-colors"
	const normalClasses = "border-gray-300 focus:border-blue-500 focus:ring-blue-500"
	const errorClasses = "border-red-300 focus:border-red-500 focus:ring-red-500"
	
	return (
		<input 
			type={type}
			className={`${baseClasses} ${error ? errorClasses : normalClasses} ${className}`}
			{...props}
		/>
	)
}

export function SearchInput({ 
	placeholder = "Search...", 
	value, 
	onChange, 
	className = "",
	...props 
}) {
	return (
		<div className={`relative ${className}`}>
			<div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
				<SearchIcon className="h-4 w-4 text-gray-400" />
			</div>
			<Input
				type="text"
				placeholder={placeholder}
				value={value}
				onChange={onChange}
				className="pl-10"
				{...props}
			/>
		</div>
	)
}

function SearchIcon({ className }) {
	return (
		<svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
		</svg>
	)
}
