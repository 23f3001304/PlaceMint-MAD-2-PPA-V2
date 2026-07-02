import { del, get, patch, post } from '../client'

export const stats = () => get('/company/stats')
export const profile = () => get('/company/profile')
export const updateProfile = (data) => patch('/company/profile', data)

export const drives = () => get('/company/drives')
export const createDrive = (data) => post('/company/drives', data)
export const updateDrive = (id, data) => patch(`/company/drives/${id}`, data)
export const setDriveStatus = (id, status) => post(`/company/drives/${id}/status`, { status })
export const deleteDrive = (id) => del(`/company/drives/${id}`)

export const applicants = (driveId) => get(`/company/applications/drive/${driveId}`)
export const updateApplication = (id, data) => patch(`/company/applications/${id}`, data)
