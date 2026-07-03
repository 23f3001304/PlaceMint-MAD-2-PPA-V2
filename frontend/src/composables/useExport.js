// Starts an async CSV export, polls until the job finishes, then downloads it.
import { ref } from 'vue'

import * as exportsApi from '../api/endpoints/exports'
import { toastError, toastInfo, toastSuccess } from '../store/ui'

const POLL_MS = 1200
const MAX_POLLS = 25

export function useExport() {
  const exporting = ref(false)

  async function runExport() {
    if (exporting.value) return
    exporting.value = true
    toastInfo('Preparing your export...')
    try {
      let job = (await exportsApi.start()).data
      for (let i = 0; i < MAX_POLLS && job.status !== 'done' && job.status !== 'failed'; i++) {
        await new Promise((resolve) => setTimeout(resolve, POLL_MS))
        job = (await exportsApi.status(job.id)).data
      }
      if (job.status === 'done') {
        toastSuccess(`Export ready (${job.row_count} rows)`)
        await exportsApi.downloadCsv(job.id, job.filename)
      } else {
        toastError('Export did not finish. Is the worker running?')
      }
    } catch (e) {
      toastError(e.message)
    } finally {
      exporting.value = false
    }
  }

  return { exporting, runExport }
}
