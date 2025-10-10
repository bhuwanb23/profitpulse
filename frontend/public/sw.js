self.addEventListener('install', (event) => {
	self.skipWaiting()
})

self.addEventListener('activate', (event) => {
	clients.claim()
})

self.addEventListener('fetch', (event) => {
	// Placeholder: passthrough for now
	return
})
