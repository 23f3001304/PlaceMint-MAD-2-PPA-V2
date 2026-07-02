// Thin fetch wrapper around the Flask API. Reads the token straight from
// localStorage (not the store) to avoid an import cycle with the auth store.

const BASE = '/api'
const TOKEN_KEY = 'ppa_token'

export class ApiError extends Error {
  constructor(message, status, payload) {
    super(message)
    this.status = status
    this.payload = payload || {}
  }
}

async function request(path, { method = 'GET', body, auth = true, headers = {} } = {}) {
  const opts = { method, headers: { ...headers } }
  if (body instanceof FormData) {
    opts.body = body
  } else if (body !== undefined) {
    opts.headers['Content-Type'] = 'application/json'
    opts.body = JSON.stringify(body)
  }
  if (auth) {
    const token = localStorage.getItem(TOKEN_KEY)
    if (token) opts.headers.Authorization = `Bearer ${token}`
  }

  const res = await fetch(BASE + path, opts)
  const data = await res.json().catch(() => ({}))
  if (!res.ok || data.ok === false) {
    throw new ApiError(data.error || `Request failed (${res.status})`, res.status, data)
  }
  return data
}

export const get = (path, opts) => request(path, { ...opts, method: 'GET' })
export const post = (path, body, opts) => request(path, { ...opts, method: 'POST', body })
export const patch = (path, body, opts) => request(path, { ...opts, method: 'PATCH', body })
export const del = (path, opts) => request(path, { ...opts, method: 'DELETE' })
export { TOKEN_KEY }

// Build a query string from an object, dropping empty/null values.
export function qs(params) {
  if (!params) return ''
  const entries = Object.entries(params).filter(([, v]) => v !== '' && v != null)
  const encoded = new URLSearchParams(entries).toString()
  return encoded ? `?${encoded}` : ''
}
