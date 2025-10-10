import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { CONFIG } from './services/config'

const link = document.createElement('link')
link.rel = 'manifest'
link.href = '/manifest.webmanifest'
document.head.appendChild(link)

document.title = `${CONFIG.appName} — v${CONFIG.appVersion}`

if ('serviceWorker' in navigator) {
	window.addEventListener('load', () => {
		navigator.serviceWorker.register('/sw.js').catch(() => {})
	})
}

createRoot(document.getElementById('root')).render(
	<StrictMode>
		<App />
	</StrictMode>,
)
