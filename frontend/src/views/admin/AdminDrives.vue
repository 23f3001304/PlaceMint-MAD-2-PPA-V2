<script setup>
import { onMounted, reactive, ref, watch } from 'vue'

import * as adminApi from '../../api/endpoints/admin'
import { useAsync } from '../../composables/useAsync'
import { toastSuccess } from '../../store/ui'
import ConfirmDialog from '../../components/overlays/ConfirmDialog.vue'
import DataTable from '../../components/ui/DataTable.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import SearchBar from '../../components/forms/SearchBar.vue'
import SelectMenu from '../../components/inputs/SelectMenu.vue'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const { run, loading } = useAsync()
const rows = ref([])
const filters = reactive({ q: '', status: '' })
const confirm = reactive({ open: false, action: null, message: '' })

const STATUS_OPTIONS = [
  { value: '', label: 'All statuses' },
  { value: 'pending', label: 'Pending' },
  { value: 'approved', label: 'Approved' },
  { value: 'rejected', label: 'Rejected' },
  { value: 'closed', label: 'Closed' },
]

const columns = [
  { key: 'job_title', label: 'Role' },
  { key: 'company_name', label: 'Company' },
  { key: 'applicant_count', label: 'Applicants' },
  { key: 'status', label: 'Status' },
  { key: 'actions', label: '', class: 'text-end' },
]

async function load() {
  const res = await run(() => adminApi.drives({ q: filters.q, status: filters.status }))
  rows.value = res.data
}
onMounted(load)
let timer
watch(filters, () => { clearTimeout(timer); timer = setTimeout(load, 300) })

async function setApproval(d, status) {
  await run(() => adminApi.setDriveApproval(d.id, status))
  toastSuccess(`Drive ${status}`)
  load()
}
async function close(d) {
  await run(() => adminApi.closeDrive(d.id))
  toastSuccess('Drive closed')
  load()
}
function askDelete(d) {
  confirm.open = true
  confirm.message = `Delete "${d.job_title}"? This removes its applications.`
  confirm.action = async () => {
    await run(() => adminApi.deleteDrive(d.id))
    toastSuccess('Drive deleted')
    load()
  }
}
</script>

<template>
  <div class="motion-fade-up">
    <PageHeader title="Drives" subtitle="Approve and oversee placement drives">
      <template #actions>
        <SelectMenu v-model="filters.status" :options="STATUS_OPTIONS" placeholder="All statuses" />
        <SearchBar v-model="filters.q" placeholder="Search job title" />
      </template>
    </PageHeader>

    <DataTable :columns="columns" :rows="rows" :loading="loading" empty="No drives found.">
      <template #cell-job_title="{ row }">
        <div class="fw-semibold">{{ row.job_title }}</div>
        <div class="small text-muted">{{ row.drive_name || row.location }}</div>
      </template>
      <template #cell-status="{ row }"><StatusBadge :status="row.status" /></template>
      <template #cell-actions="{ row }">
        <div class="d-flex gap-1 justify-content-end flex-wrap">
          <button v-if="row.status === 'pending'" class="btn btn-sm btn-3d-accent" @click="setApproval(row, 'approved')">Approve</button>
          <button v-if="row.status === 'pending'" class="btn btn-sm btn-outline-secondary" @click="setApproval(row, 'rejected')">Reject</button>
          <button v-if="row.status === 'approved'" class="btn btn-sm btn-outline-secondary" @click="close(row)">Mark complete</button>
          <button class="btn btn-sm btn-outline-danger" @click="askDelete(row)">Delete</button>
        </div>
      </template>
    </DataTable>

    <ConfirmDialog
      v-model="confirm.open" title="Delete drive" :message="confirm.message"
      confirm-label="Delete" danger @confirm="confirm.action && confirm.action()"
    />
  </div>
</template>
