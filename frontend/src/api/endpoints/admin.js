import { del, get, post, qs } from '../client'

export const stats = () => get('/admin/stats')
export const charts = () => get('/admin/stats/charts')

export const companies = (params) => get('/admin/companies' + qs(params))
export const companyDetail = (id) => get(`/admin/companies/${id}`)
export const setCompanyApproval = (id, status) => post(`/admin/companies/${id}/approval`, { status })
export const deleteCompany = (id) => del(`/admin/companies/${id}`)

export const students = (params) => get('/admin/students' + qs(params))
export const studentDetail = (id) => get(`/admin/students/${id}`)
export const deleteStudent = (id) => del(`/admin/students/${id}`)

export const setBlacklist = (userId, blacklisted) => post(`/admin/users/${userId}/blacklist`, { blacklisted })
export const setActive = (userId, active) => post(`/admin/users/${userId}/active`, { active })

export const drives = (params) => get('/admin/drives' + qs(params))
export const setDriveApproval = (id, status) => post(`/admin/drives/${id}/approval`, { status })
export const closeDrive = (id) => post(`/admin/drives/${id}/close`)
export const deleteDrive = (id) => del(`/admin/drives/${id}`)

export const applications = (params) => get('/admin/applications' + qs(params))
