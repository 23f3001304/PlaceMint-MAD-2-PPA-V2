// Reactive auth session. Components read `authState`; guards and API calls read
// the token. No Pinia: Vue's own reactivity is enough for one small session.
import { reactive } from 'vue'

import * as authApi from '../api/endpoints/auth'
import { TOKEN_KEY } from '../api/client'

export const authState = reactive({
  token: localStorage.getItem(TOKEN_KEY) || null,
  user: null,
  profile: null,
  ready: false,
})

function setSession({ token, user, profile }) {
  authState.token = token
  authState.user = user
  authState.profile = profile
  localStorage.setItem(TOKEN_KEY, token)
}

export async function login(email, password) {
  const { data } = await authApi.login(email, password)
  setSession(data)
  return data.user
}

export async function register(payload) {
  const { data } = await authApi.register(payload)
  setSession(data)
  return data.user
}

export function logout() {
  authState.token = null
  authState.user = null
  authState.profile = null
  localStorage.removeItem(TOKEN_KEY)
}

export function setProfile(profile) {
  authState.profile = profile
}

// Validate a restored token by fetching the live session; drop it if invalid.
export async function loadSession() {
  if (!authState.token) {
    authState.ready = true
    return
  }
  try {
    const { data } = await authApi.me()
    authState.user = data.user
    authState.profile = data.profile
  } catch {
    logout()
  } finally {
    authState.ready = true
  }
}
