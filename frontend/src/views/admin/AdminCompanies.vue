<script setup>
import { onMounted, reactive, ref, watch } from 'vue'

import * as adminApi from '../../api/endpoints/admin'
import { useAsync } from '../../composables/useAsync'
import { toastSuccess } from '../../store/ui'
import ConfirmDialog from '../../components/overlays/ConfirmDialog.vue'
import DataTable from '../../components/ui/DataTable.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import SearchBar from '../../components/forms/SearchBar.vue'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const { run, loading } = useAsync()
const rows = ref([])
const filters = reactive({ q: '', status: '' })
const confirm = reactive({ open: false, action: null, message: '' })

const columns = [
  { key: 'company_name', label: 'Company' },
  { key: 'industry', label: 'Industry' },
  { key: 'approval_status', label: 'Status' },
  { key: 'actions', label: '', class: 'text-end' },
]

async function load() {
  const res = await run(() => adminApi.companies({ q: filters.q, status: filters.status }))
  rows.value = res.data
}
onMounted(load)
let timer
watch(filters, () => { clearTimeout(timer); timer = setTimeout(load, 300) })

async function setApproval(c, status) {
  await run(() => adminApi.setCompanyApproval(c.id, status))
  toastSuccess(`Company ${status}`)
  load()
}
async function toggleBlacklist(c) {
  await run(() => adminApi.setBlacklist(c.user_id, !c.is_blacklisted))
  load()
}
function askDelete(c) {
  confirm.open = true
  confirm.message = `Remove ${c.company_name}? This deletes its drives and applications.`
  confirm.action = async () => {
    await run(() => adminApi.deleteCompany(c.id))
    toastSuccess('Company removed')
    load()
  }
}
</script>

<template>
  <div class="motion-fade-up">
    <PageHeader title="Companies" subtitle="Approve, search and moderate companies">
      <template #actions>
        <select v-model="filters.status" class="form-select" style="width: auto">
          <option value="">All statuses</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
        </select>
        <SearchBar v-model="filters.q" placeholder="Search name or industry" />
      </template>
    </PageHeader>

    <DataTable :columns="columns" :rows="rows" :loading="loading" empty="No companies found.">
      <template #cell-approval_status="{ row }"><StatusBadge :status="row.approval_status" /></template>
      <template #cell-actions="{ row }">
        <div class="d-flex gap-1 justify-content-end flex-wrap">
          <button v-if="row.approval_status !== 'approved'" class="btn btn-sm btn-3d-accent" @click="setApproval(row, 'approved')">Approve</button>
          <button v-if="row.approval_status === 'pending'" class="btn btn-sm btn-outline-secondary" @click="setApproval(row, 'rejected')">Reject</button>
          <button class="btn btn-sm btn-outline-secondary" @click="toggleBlacklist(row)">
            {{ row.is_blacklisted ? 'Un-blacklist' : 'Blacklist' }}
          </button>
          <button class="btn btn-sm btn-outline-danger" @click="askDelete(row)">Remove</button>
        </div>
      </template>
    </DataTable>

    <ConfirmDialog
      v-model="confirm.open" title="Remove company" :message="confirm.message"
      confirm-label="Remove" danger @confirm="confirm.action && confirm.action()"
    />
  </div>
</template>
