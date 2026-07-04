import { get } from '../client'

// Pre-login aggregated stats for the public landing page (no auth).
export const publicStats = () => get('/public/stats', { auth: false })
