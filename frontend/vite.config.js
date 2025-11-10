import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  // Build-time validation for API URL in production builds
  if (mode === 'production' && !env.VITE_API_URL) {
    throw new Error('VITE_API_URL is required for production builds. Please set it in your environment.')
  }

  return {
    plugins: [react(), tailwindcss()],
    define: {
      __APP_ENV__: JSON.stringify(mode),
    },
  }
})
