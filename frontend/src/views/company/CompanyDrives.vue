<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import * as companyApi from '../../api/endpoints/company'
import { authState } from '../../store/auth'
import { useAsync } from '../../composables/useAsync'
import { toastSuccess } from '../../store/ui'
import AppModal from '../../components/overlays/AppModal.vue'
import ConfirmDialog from '../../components/overlays/ConfirmDialog.vue'
import DataTable from '../../components/ui/DataTable.vue'
import DriveForm from '../../components/forms/DriveForm.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const { run, loading } = useAsync()
const rows = ref([])
const approved = computed(() => authState.profile?.approval_status === 'approved')
const modal = reactive({ open: false, editing: null, form: emptyForm() })
const confirm = reactive({ open: false, action: null, message: '' })

const columns = [
  { key: 'job_title', label: 'Role' },
  { key: 'drive_name', label: 'Drive' },
  { key: 'applicant_count', label: 'Applicants' },
  { key: 'status', label: 'Status' },
  { key: 'actions', label: '', class: 'text-end' },
]

function emptyForm() {
  return {
    job_title: '', drive_name: '', job_description: '', location: '', package_lpa: '',
    min_experience: '', skills_required: '', eligible_branches: '', min_cgpa: '',
    eligible_years: '', benefits: '', deadline: '',
  }
}
function driveToForm(d) {
  return {
    ...d,
    skills_required: (d.skills_required || []).join(', '),
    eligible_branches: (d.eligible_branches || []).join(', '),
    eligible_years: (d.eligible_years || []).join(', '),
  }
}

async function load() { rows.value = (await run(companyApi.drives)).data }
onMounted(load)

function openCreate() { modal.editing = null; modal.form = emptyForm(); modal.open = true }
function openEdit(d) { modal.editing = d.id; modal.form = driveToForm(d); modal.open = true }

async function save() {
  const payload = { ...modal.form }
  if (modal.editing) await run(() => companyApi.updateDrive(modal.editing, payload))
  else await run(() => companyApi.createDrive(payload))
  toastSuccess(modal.editing ? 'Drive updated' : 'Drive submitted for approval')
  modal.open = false
  load()
}
async function toggle(d) {
  await run(() => companyApi.setDriveStatus(d.id, d.status === 'approved' ? 'closed' : 'approved'))
  load()
}
function askDelete(d) {
  confirm.open = true
  confirm.message = `Delete "${d.job_title}"?`
  confirm.action = async () => { await run(() => companyApi.deleteDrive(d.id)); toastSuccess('Deleted'); load() }
}
</script>

<template>
  <div class="motion-fade-up">
    <PageHeader title="Job drives" subtitle="Post and manage your placement drives">
      <template #actions>
        <button class="btn btn-3d-accent" :disabled="!approved" @click="openCreate">+ New drive</button>
      </template>
    </PageHeader>

    <p v-if="!approved" class="text-muted">Your company must be approved before posting drives.</p>

    <DataTable :columns="columns" :rows="rows" :loading="loading" empty="No drives yet.">
      <template #cell-status="{ row }"><StatusBadge :status="row.status" /></template>
      <template #cell-actions="{ row }">
        <div class="d-flex gap-1 justify-content-end flex-wrap">
          <button class="btn btn-sm btn-outline-secondary" @click="openEdit(row)">Edit</button>
          <button v-if="['approved', 'closed'].includes(row.status)" class="btn btn-sm btn-outline-secondary" @click="toggle(row)">
            {{ row.status === 'approved' ? 'Close' : 'Reopen' }}
          </button>
          <button class="btn btn-sm btn-outline-danger" @click="askDelete(row)">Delete</button>
        </div>
      </template>
    </DataTable>

    <AppModal v-model="modal.open" :title="modal.editing ? 'Edit drive' : 'New drive'" size="lg">
      <form novalidate @submit.prevent="save"><DriveForm :form="modal.form" /></form>
      <template #footer>
        <button class="btn btn-outline-secondary" @click="modal.open = false">Cancel</button>
        <button class="btn btn-3d-accent" @click="save">{{ modal.editing ? 'Save' : 'Submit for approval' }}</button>
      </template>
    </AppModal>

    <ConfirmDialog
      v-model="confirm.open" title="Delete drive" :message="confirm.message"
      confirm-label="Delete" danger @confirm="confirm.action && confirm.action()"
    />
  </div>
</template>
