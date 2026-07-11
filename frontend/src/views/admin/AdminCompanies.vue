<script setup>
import { onMounted, reactive, ref, watch } from 'vue'

import * as adminApi from '../../api/endpoints/admin'
import { useAsync } from '../../composables/useAsync'
import { toastSuccess } from '../../store/ui'
import AppModal from '../../components/overlays/AppModal.vue'
import ConfirmDialog from '../../components/overlays/ConfirmDialog.vue'
import DataTable from '../../components/ui/DataTable.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import SearchBar from '../../components/forms/SearchBar.vue'
import SelectMenu from '../../components/inputs/SelectMenu.vue'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const { run, loading } = useAsync()
const rows = ref([])
const filters = reactive({ q: '', status: '' })
const detail = reactive({ open: false, data: null })

const STATUS_OPTIONS = [
  { value: '', label: 'All statuses' },
  { value: 'pending', label: 'Pending' },
  { value: 'approved', label: 'Approved' },
  { value: 'rejected', label: 'Rejected' },
]
const confirm = reactive({ open: false, action: null, message: '' })

const columns = [
  { key: 'company_name', label: 'Company' },
  { key: 'industry', label: 'Industry' },
  { key: 'location', label: 'Location' },
  { key: 'drive_count', label: 'Drives' },
  { key: 'approval_status', label: 'Status' },
  { key: 'actions', label: '', class: 'text-end' },
]

async function load() {
  rows.value = (await run(() => adminApi.companies({ q: filters.q, status: filters.status }))).data
}
onMounted(load)
let timer
watch(filters, () => { clearTimeout(timer); timer = setTimeout(load, 300) })

async function openDetail(c) {
  detail.data = (await run(() => adminApi.companyDetail(c.id))).data
  detail.open = true
}
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
        <SelectMenu v-model="filters.status" :options="STATUS_OPTIONS" placeholder="All statuses" />
        <SearchBar v-model="filters.q" placeholder="Search name or industry" />
      </template>
    </PageHeader>

    <DataTable :columns="columns" :rows="rows" :loading="loading" empty="No companies found.">
      <template #cell-company_name="{ row }">
        <button class="btn btn-link p-0 fw-semibold text-start" @click="openDetail(row)">{{ row.company_name }}</button>
        <span v-if="row.is_blacklisted" class="status-badge st-rejected ms-2">blacklisted</span>
      </template>
      <template #cell-location="{ row }"><span class="text-muted">{{ row.location || 'Not set' }}</span></template>
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

    <AppModal v-model="detail.open" :title="detail.data?.company_name" size="lg">
      <div v-if="detail.data">
        <div class="d-flex align-items-center gap-2 mb-3">
          <StatusBadge :status="detail.data.approval_status" />
          <span class="text-muted small">{{ detail.data.industry }}<span v-if="detail.data.location"> · {{ detail.data.location }}</span></span>
        </div>
        <dl class="row small mb-3">
          <dt class="col-4 col-sm-3 text-muted">Login email</dt><dd class="col-8 col-sm-9">{{ detail.data.email }}</dd>
          <dt class="col-4 col-sm-3 text-muted">HR contact</dt><dd class="col-8 col-sm-9">{{ detail.data.hr_contact || 'Not set' }}</dd>
          <dt class="col-4 col-sm-3 text-muted">Website</dt>
          <dd class="col-8 col-sm-9">
            <a v-if="detail.data.website" :href="detail.data.website" target="_blank" rel="noopener">{{ detail.data.website }}</a>
            <span v-else>Not set</span>
          </dd>
        </dl>
        <p v-if="detail.data.description" class="text-muted">{{ detail.data.description }}</p>

        <h3 class="h6 mt-3">Drives ({{ (detail.data.drives || []).length }})</h3>
        <ul class="list-unstyled mb-0">
          <li v-for="d in detail.data.drives || []" :key="d.id" class="d-flex justify-content-between border-bottom py-2">
            <span>{{ d.job_title }}<span v-if="d.drive_name" class="text-muted small"> · {{ d.drive_name }}</span></span>
            <span class="d-flex gap-2 align-items-center">
              <span class="text-muted small">{{ d.applicant_count }} applicants</span>
              <StatusBadge :status="d.status" />
            </span>
          </li>
          <li v-if="!(detail.data.drives || []).length" class="text-muted py-2">No drives yet.</li>
        </ul>
      </div>
    </AppModal>

    <ConfirmDialog
      v-model="confirm.open" title="Remove company" :message="confirm.message"
      confirm-label="Remove" danger @confirm="confirm.action && confirm.action()"
    />
  </div>
</template>
