<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import * as adminApi from '../../api/endpoints/admin'
import { useAsync } from '../../composables/useAsync'
import { toastSuccess } from '../../store/ui'
import AppModal from '../../components/overlays/AppModal.vue'
import ConfirmDialog from '../../components/overlays/ConfirmDialog.vue'
import DataTable from '../../components/ui/DataTable.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import SearchBar from '../../components/forms/SearchBar.vue'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const { run, loading } = useAsync()
const router = useRouter()
const rows = ref([])
const q = ref('')
const detail = reactive({ open: false, data: null })
const confirm = reactive({ open: false, action: null, message: '' })

const columns = [
  { key: 'name', label: 'Name' },
  { key: 'roll_no', label: 'Roll no' },
  { key: 'branch', label: 'Branch' },
  { key: 'cgpa', label: 'CGPA' },
  { key: 'actions', label: '', class: 'text-end' },
]

async function load() {
  const res = await run(() => adminApi.students({ q: q.value }))
  rows.value = res.data
}
onMounted(load)
let timer
watch(q, () => { clearTimeout(timer); timer = setTimeout(load, 300) })

async function openDetail(s) {
  const res = await run(() => adminApi.studentDetail(s.id))
  detail.data = res.data
  detail.open = true
}
async function toggleBlacklist(s) {
  await run(() => adminApi.setBlacklist(s.user_id, !s.is_blacklisted))
  load()
}
function askDelete(s) {
  confirm.open = true
  confirm.message = `Remove ${s.name}? This deletes their applications.`
  confirm.action = async () => {
    await run(() => adminApi.deleteStudent(s.id))
    toastSuccess('Student removed')
    load()
  }
}
</script>

<template>
  <div class="motion-fade-up">
    <PageHeader title="Students" subtitle="Search and manage registered students">
      <template #actions><SearchBar v-model="q" placeholder="Search name or roll number" /></template>
    </PageHeader>

    <DataTable :columns="columns" :rows="rows" :loading="loading" empty="No students found.">
      <template #cell-name="{ row }">
        <button class="btn btn-link p-0 fw-semibold" @click="openDetail(row)">{{ row.name }}</button>
        <span v-if="row.is_blacklisted" class="status-badge st-rejected ms-2">blacklisted</span>
      </template>
      <template #cell-actions="{ row }">
        <div class="d-flex gap-1 justify-content-end flex-wrap">
          <button class="btn btn-sm btn-outline-secondary" @click="openDetail(row)">View</button>
          <button class="btn btn-sm btn-outline-secondary" @click="toggleBlacklist(row)">
            {{ row.is_blacklisted ? 'Un-blacklist' : 'Blacklist' }}
          </button>
          <button class="btn btn-sm btn-outline-danger" @click="askDelete(row)">Remove</button>
        </div>
      </template>
    </DataTable>

    <AppModal v-model="detail.open" :title="detail.data?.name" size="lg">
      <div v-if="detail.data" class="text-mono small text-muted mb-3">
        {{ detail.data.roll_no }} · {{ detail.data.branch }} · CGPA {{ detail.data.cgpa }} · {{ detail.data.email }}
      </div>
      <div v-if="detail.data?.skills?.length" class="mb-3">
        <span v-for="s in detail.data.skills" :key="s" class="badge text-bg-light me-1">{{ s }}</span>
      </div>
      <h3 class="h6">Applications</h3>
      <ul class="list-unstyled mb-0">
        <li v-for="a in detail.data?.applications || []" :key="a.id" class="d-flex justify-content-between border-bottom py-2">
          <span>{{ a.drive?.job_title }} · {{ a.drive?.company_name }}</span>
          <StatusBadge :status="a.status" />
        </li>
        <li v-if="!(detail.data?.applications || []).length" class="text-muted py-2">No applications yet.</li>
      </ul>
      <template #footer>
        <button class="btn btn-3d-accent" @click="router.push(`/students/${detail.data.id}`)">Open full profile</button>
      </template>
    </AppModal>

    <ConfirmDialog
      v-model="confirm.open" title="Remove student" :message="confirm.message"
      confirm-label="Remove" danger @confirm="confirm.action && confirm.action()"
    />
  </div>
</template>
