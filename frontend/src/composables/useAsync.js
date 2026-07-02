// Wraps an async call with loading/error state and surfaces failures as toasts.
import { ref } from 'vue'

import { toastError } from '../store/ui'

export function useAsync() {
  const loading = ref(false)
  const error = ref(null)

  async function run(fn) {
    loading.value = true
    error.value = null
    try {
      return await fn()
    } catch (e) {
      error.value = e.message
      toastError(e.message)
      throw e
    } finally {
      loading.value = false
    }
  }

  return { loading, error, run }
}
