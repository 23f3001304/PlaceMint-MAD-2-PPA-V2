// Minimal toast bus. `toast()` pushes a message; ToastHost renders the list.
import { reactive } from 'vue'

export const ui = reactive({ toasts: [] })
let seq = 0

export function toast(message, type = 'info', timeout = 3800) {
  const id = ++seq
  ui.toasts.push({ id, message, type })
  if (timeout) setTimeout(() => dismissToast(id), timeout)
  return id
}

export function dismissToast(id) {
  const index = ui.toasts.findIndex((t) => t.id === id)
  if (index !== -1) ui.toasts.splice(index, 1)
}

export const toastSuccess = (message) => toast(message, 'success')
export const toastError = (message) => toast(message, 'danger')
export const toastInfo = (message) => toast(message, 'info')
