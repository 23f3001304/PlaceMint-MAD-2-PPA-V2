<script setup>
import { onMounted, reactive, ref, watch } from 'vue'

import * as companyApi from '../../api/endpoints/company'
import { useAsync } from '../../composables/useAsync'
import { useExport } from '../../composables/useExport'
import { toastSuccess } from '../../store/ui'
import AppModal from '../../components/overlays/AppModal.vue'
import DataTable from '../../components/ui/DataTable.vue'
import FormField from '../../components/forms/FormField.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const { run, loading } = useAsync()
const { exporting, runExport } = useExport()
const drives = ref([])
const selectedDrive = ref('')
const applicants = ref([])
const review = reactive({ open: false, app: null, status: '', remarks: '', interview_at: '', interview_mode: '' })

const STATUS_OPTIONS = ['shortlisted', 'interview', 'offer', 'rejected', 'placed']
const columns = [
  { key: 'student', label: 'Student' },
  { key: 'status', label: 'Status' },
  { key: 'interview', label: 'Interview' },
  { key: 'actions', label: '', class: 'text-end' },
]

onMounted(async () => {
  drives.value = (await run(companyApi.drives)).data
  if (drives.value.length) selectedDrive.value = drives.value[0].id
})
watch(selectedDrive, load)

async function load() {
  if (!selectedDrive.value) { applicants.value = []; return }
  applicants.value = (await run(() => companyApi.applicants(selectedDrive.value))).data
}

function openReview(a) {
  review.app = a
  review.status = a.status
  review.remarks = a.remarks || ''
  review.interview_at = a.interview_at ? a.interview_at.slice(0, 16) : ''
  review.interview_mode = a.interview_mode || ''
  review.open = true
}
async function saveReview() {
  await run(() => companyApi.updateApplication(review.app.id, {
    status: review.status, remarks: review.remarks,
    interview_at: review.interview_at || undefined, interview_mode: review.interview_mode,
  }))
  toastSuccess('Application updated')
  review.open = false
  load()
}
</script>

<template>
  <div class="motion-fade-up">
    <PageHeader title="Applicants" subtitle="Review, shortlist, interview and select">
      <template #actions>
        <select v-model="selectedDrive" class="form-select" style="width: auto">
          <option v-for="d in drives" :key="d.id" :value="d.id">{{ d.job_title }} ({{ d.applicant_count }})</option>
        </select>
        <button class="btn btn-outline-secondary" :disabled="exporting" @click="runExport">
          {{ exporting ? 'Exporting...' : 'Export CSV' }}
        </button>
      </template>
    </PageHeader>

    <DataTable :columns="columns" :rows="applicants" :loading="loading" empty="No applicants for this drive yet.">
      <template #cell-student="{ row }">
        <div class="fw-semibold">{{ row.student?.name }}</div>
        <div class="small text-muted">{{ row.student?.roll_no }} · {{ row.student?.branch }} · CGPA {{ row.student?.cgpa }}</div>
      </template>
      <template #cell-status="{ row }"><StatusBadge :status="row.status" /></template>
      <template #cell-interview="{ row }">
        <span v-if="row.interview_at" class="small">{{ row.interview_at.slice(0, 16).replace('T', ' ') }} · {{ row.interview_mode }}</span>
        <span v-else class="text-muted small">not scheduled</span>
      </template>
      <template #cell-actions="{ row }">
        <button class="btn btn-sm btn-3d-accent" @click="openReview(row)">Review</button>
      </template>
    </DataTable>

    <AppModal v-model="review.open" :title="review.app?.student?.name">
      <FormField v-model="review.status" label="Status" type="select" :options="STATUS_OPTIONS" />
      <div class="row gx-2">
        <div class="col-sm-7"><FormField v-model="review.interview_at" label="Interview date/time" type="datetime-local" /></div>
        <div class="col-sm-5"><FormField v-model="review.interview_mode" label="Mode" placeholder="In-person / Online" /></div>
      </div>
      <FormField v-model="review.remarks" label="Feedback / remarks" type="textarea" />
      <template #footer>
        <button class="btn btn-outline-secondary" @click="review.open = false">Cancel</button>
        <button class="btn btn-3d-accent" @click="saveReview">Save</button>
      </template>
    </AppModal>
  </div>
</template>
