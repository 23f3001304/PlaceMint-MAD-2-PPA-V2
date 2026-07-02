<script setup>
import { onMounted, ref } from 'vue'

import * as studentApi from '../../api/endpoints/student'
import { openDoc } from '../../api/client'
import { useAsync } from '../../composables/useAsync'
import { toastError } from '../../store/ui'
import DataTable from '../../components/ui/DataTable.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const { run, loading } = useAsync()
const apps = ref([])
const placements = ref([])

const columns = [
  { key: 'drive', label: 'Role' },
  { key: 'company', label: 'Company' },
  { key: 'status', label: 'Status' },
  { key: 'interview', label: 'Interview' },
  { key: 'remarks', label: 'Feedback' },
]

onMounted(async () => {
  apps.value = (await run(studentApi.applications)).data
  placements.value = (await studentApi.placements()).data
})

async function openOffer(p) {
  try {
    await openDoc(`/documents/offer-letter/${p.id}`)
  } catch (e) {
    toastError(e.message)
  }
}
</script>

<template>
  <div class="motion-fade-up">
    <PageHeader title="My applications" subtitle="Track status, interviews and feedback" />

    <div v-if="placements.length" class="surface-card p-3 mb-4">
      <h2 class="h6 mb-2">Placements</h2>
      <div
        v-for="p in placements" :key="p.id"
        class="d-flex justify-content-between align-items-center border-bottom py-2 flex-wrap gap-2"
      >
        <span>{{ p.position }} · {{ p.company_name }} · {{ p.salary_lpa }} LPA</span>
        <button class="btn btn-sm btn-3d-accent" @click="openOffer(p)">Offer letter</button>
      </div>
    </div>

    <DataTable :columns="columns" :rows="apps" :loading="loading" empty="You haven't applied to any drives yet.">
      <template #cell-drive="{ row }"><span class="fw-semibold">{{ row.drive?.job_title }}</span></template>
      <template #cell-company="{ row }">{{ row.drive?.company_name }}</template>
      <template #cell-status="{ row }"><StatusBadge :status="row.status" /></template>
      <template #cell-interview="{ row }">
        <span v-if="row.interview_at" class="small">{{ row.interview_at.slice(0, 16).replace('T', ' ') }} · {{ row.interview_mode }}</span>
        <span v-else class="text-muted small">not scheduled</span>
      </template>
      <template #cell-remarks="{ row }"><span class="small text-muted">{{ row.remarks || '' }}</span></template>
    </DataTable>
  </div>
</template>
