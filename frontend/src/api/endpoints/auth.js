import { get, post } from '../client'

export const login = (email, password) =>
  post('/auth/login', { email, password }, { auth: false })

export const register = (payload) => post('/auth/register', payload, { auth: false })

export const me = () => get('/auth/me')
