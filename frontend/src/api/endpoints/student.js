import { get, patch, post, qs } from '../client'

export const stats = () => get('/student/profile/stats')
export const profile = () => get('/student/profile')
export const updateProfile = (data) => patch('/student/profile', data)
export const uploadResume = (formData) => post('/student/profile/resume', formData)

export const drives = (params) => get('/student/drives' + qs(params))
export const driveDetail = (id) => get(`/student/drives/${id}`)
export const organizations = (params) => get('/student/drives/organizations' + qs(params))
export const organization = (id) => get(`/student/drives/organizations/${id}`)

export const apply = (driveId) => post('/student/applications', { drive_id: driveId })
export const applications = () => get('/student/applications')
export const placements = () => get('/student/applications/placements')
