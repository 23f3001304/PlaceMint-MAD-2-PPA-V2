<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import * as studentApi from '../../api/endpoints/student'
import { useAsync } from '../../composables/useAsync'
import { toastError, toastSuccess } from '../../store/ui'
import AppModal from '../../components/overlays/AppModal.vue'
import DriveCard from '../../components/DriveCard.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import SearchBar from '../../components/forms/SearchBar.vue'
import StatusBadge from '../../components/ui/StatusBadge.vue'
import CompleteProfileNotice from '../../components/CompleteProfileNotice.vue'
import { authState } from '../../store/auth'

const { run, loading } = useAsync()
const drives = ref([])
const filters = reactive({ q: '', eligible_only: false })
const detail = reactive({ open: false, drive: null })
const route = useRoute()

async function load() {
  if (!authState.profile?.profile_complete) return
  drives.value = (await run(() => studentApi.drives({
    q: filters.q,
    company: route.query.company || '',
    eligible_only: filters.eligible_only ? 'true' : '',
  }))).data
}
onMounted(load)
let timer
watch(filters, () => { clearTimeout(timer); timer = setTimeout(load, 300) })

async function apply(drive) {
  drive.applied = true // optimistic: flip the card immediately, no reload
  drive.applicant_count = (drive.applicant_count || 0) + 1
  detail.open = false
  try {
    await studentApi.apply(drive.id)
    toastSuccess('Application submitted')
  } catch (e) {
    drive.applied = false
    drive.applicant_count -= 1
    toastError(e.message)
  }
}
function view(drive) { detail.drive = drive; detail.open = true }
</script>

<template>
  <div class="motion-fade-up">
    <PageHeader title="Browse drives" subtitle="Approved openings you can apply to">
      <template v-if="authState.profile?.profile_complete" #actions>
        <div class="form-check d-flex align-items-center gap-2 me-2">
          <input id="elig" v-model="filters.eligible_only" class="form-check-input mt-0" type="checkbox" />
          <label for="elig" class="form-check-label small">Eligible only</label>
        </div>
        <SearchBar v-model="filters.q" placeholder="Search job title" />
      </template>
    </PageHeader>

    <CompleteProfileNotice v-if="!authState.profile?.profile_complete" />
    <template v-else>
      <p v-if="!loading && !drives.length" class="text-muted">No drives match your filters.</p>
      <div class="row g-3">
        <div v-for="d in drives" :key="d.id" class="col-md-6 col-xl-4">
          <DriveCard :drive="d" @apply="apply" @view="view" />
        </div>
      </div>
    </template>

    <AppModal v-model="detail.open" :title="detail.drive?.job_title" size="lg">
      <div v-if="detail.drive">
        <div class="text-muted mb-2">{{ detail.drive.company_name }}<span v-if="detail.drive.location"> · {{ detail.drive.location }}</span></div>
        <div class="d-flex gap-3 mb-3 text-mono small">
          <span v-if="detail.drive.package_lpa">{{ detail.drive.package_lpa }} LPA</span>
          <span>Min CGPA {{ detail.drive.min_cgpa }}</span>
          <span>Apply by {{ detail.drive.deadline }}</span>
        </div>
        <p style="white-space: pre-line">{{ detail.drive.job_description }}</p>
        <div v-if="(detail.drive.skills_required || []).length" class="mb-2">
          <span v-for="s in detail.drive.skills_required" :key="s" class="badge text-bg-light me-1">{{ s }}</span>
        </div>
        <div v-if="!detail.drive.eligible" class="mt-2">
          <StatusBadge status="rejected" /> {{ (detail.drive.ineligibility_reasons || []).join(', ') }}
        </div>
      </div>
      <template #footer>
        <button class="btn btn-outline-secondary" @click="detail.open = false">Close</button>
        <button
          v-if="detail.drive && !detail.drive.applied && detail.drive.eligible"
          class="btn btn-3d-accent" @click="apply(detail.drive)"
        >Apply</button>
        <button v-else-if="detail.drive?.applied" class="btn btn-outline-success" disabled>Applied</button>
      </template>
    </AppModal>
  </div>
</template>
