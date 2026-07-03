import { downloadDoc, get, post } from '../client'

export const start = () => post('/exports')
export const status = (id) => get(`/exports/${id}`)
export const downloadCsv = (id, filename) => downloadDoc(`/exports/${id}/download`, filename)
