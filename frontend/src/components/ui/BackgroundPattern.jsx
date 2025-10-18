export default function BackgroundPattern() {
	return (
		<div className="fixed inset-0 -z-10 overflow-hidden">
			{/* Gradient Background */}
			<div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100"></div>
			
			{/* Animated Gradient Orbs */}
			<div className="absolute top-0 left-0 w-full h-full">
				{/* Large Orb 1 */}
				<div className="absolute -top-40 -left-40 w-80 h-80 bg-gradient-to-br from-blue-400/20 to-purple-600/20 rounded-full blur-3xl animate-pulse"></div>
				
				{/* Large Orb 2 */}
				<div className="absolute top-1/3 -right-40 w-96 h-96 bg-gradient-to-br from-indigo-400/20 to-pink-600/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }}></div>
				
				{/* Large Orb 3 */}
				<div className="absolute -bottom-40 left-1/4 w-72 h-72 bg-gradient-to-br from-cyan-400/20 to-blue-600/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '4s' }}></div>
				
				{/* Medium Orbs */}
				<div className="absolute top-1/4 left-1/3 w-48 h-48 bg-gradient-to-br from-violet-400/15 to-purple-600/15 rounded-full blur-2xl animate-pulse" style={{ animationDelay: '1s' }}></div>
				<div className="absolute bottom-1/4 right-1/3 w-56 h-56 bg-gradient-to-br from-emerald-400/15 to-teal-600/15 rounded-full blur-2xl animate-pulse" style={{ animationDelay: '3s' }}></div>
			</div>
			
			{/* Geometric Pattern Overlay */}
			<div className="absolute inset-0 opacity-[0.02]">
				<svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
					<defs>
						<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
							<path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1f2937" strokeWidth="1"/>
						</pattern>
						<pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse">
							<circle cx="10" cy="10" r="1" fill="#1f2937"/>
						</pattern>
					</defs>
					<rect width="100%" height="100%" fill="url(#grid)" />
					<rect width="100%" height="100%" fill="url(#dots)" />
				</svg>
			</div>
			
			{/* Floating Elements */}
			<div className="absolute inset-0 overflow-hidden">
				{/* Floating Shapes */}
				<div className="absolute top-1/4 left-1/4 w-4 h-4 bg-blue-400/20 rounded-full animate-bounce" style={{ animationDelay: '0s', animationDuration: '3s' }}></div>
				<div className="absolute top-1/3 right-1/4 w-3 h-3 bg-purple-400/20 rounded-full animate-bounce" style={{ animationDelay: '1s', animationDuration: '4s' }}></div>
				<div className="absolute bottom-1/3 left-1/3 w-5 h-5 bg-indigo-400/20 rounded-full animate-bounce" style={{ animationDelay: '2s', animationDuration: '5s' }}></div>
				<div className="absolute bottom-1/4 right-1/3 w-2 h-2 bg-cyan-400/20 rounded-full animate-bounce" style={{ animationDelay: '3s', animationDuration: '3.5s' }}></div>
				
				{/* Floating Icons */}
				<div className="absolute top-20 left-20 text-blue-400/10 text-4xl animate-pulse" style={{ animationDelay: '1s' }}>⚡</div>
				<div className="absolute top-40 right-32 text-purple-400/10 text-3xl animate-pulse" style={{ animationDelay: '2s' }}>🚀</div>
				<div className="absolute bottom-32 left-40 text-indigo-400/10 text-5xl animate-pulse" style={{ animationDelay: '3s' }}>✨</div>
				<div className="absolute bottom-20 right-20 text-cyan-400/10 text-3xl animate-pulse" style={{ animationDelay: '4s' }}>🎯</div>
				<div className="absolute top-1/2 left-16 text-emerald-400/10 text-4xl animate-pulse" style={{ animationDelay: '5s' }}>💎</div>
				<div className="absolute top-1/3 right-16 text-pink-400/10 text-3xl animate-pulse" style={{ animationDelay: '6s' }}>🌟</div>
			</div>
			
			{/* Subtle Noise Texture */}
			<div className="absolute inset-0 opacity-[0.015] mix-blend-overlay">
				<svg width="100%" height="100%">
					<filter id="noiseFilter">
						<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" stitchTiles="stitch"/>
						<feColorMatrix type="saturate" values="0"/>
					</filter>
					<rect width="100%" height="100%" filter="url(#noiseFilter)" />
				</svg>
			</div>
		</div>
	)
}
