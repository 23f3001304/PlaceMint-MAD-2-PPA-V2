// Read-only shareable profile lookups (any student or company by id).
import { get } from './client'

export const student = (id) => get(`/directory/students/${id}`)
export const company = (id) => get(`/directory/companies/${id}`)
