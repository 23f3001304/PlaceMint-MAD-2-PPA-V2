<script setup>
import { onMounted, reactive, ref } from 'vue'

import * as studentApi from '../../api/endpoints/student'
import { authState } from '../../store/auth'
import { useAsync } from '../../composables/useAsync'
import { toastSuccess } from '../../store/ui'
import AppModal from '../../components/overlays/AppModal.vue'
import DriveCard from '../../components/DriveCard.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import StatTile from '../../components/ui/StatTile.vue'

const { run } = useAsync()
const stats = ref({})
const orgs = ref([])
const org = reactive({ open: false, data: null })

onMounted(async () => {
  stats.value = (await studentApi.stats()).data
  orgs.value = (await studentApi.organizations()).data
})

async function openOrg(o) {
  org.data = (await run(() => studentApi.organization(o.id))).data
  org.open = true
}
async function apply(drive) {
  await run(() => studentApi.apply(drive.id))
  toastSuccess('Application submitted')
  org.open = false
}
</script>

<template>
  <div class="motion-fade-up">
    <PageHeader :title="`Hi ${authState.profile?.name || 'there'}`" subtitle="Your placement dashboard" />

    <div class="row g-3 mb-4">
      <div class="col-6 col-lg-3"><StatTile label="Applications" :value="stats.applications ?? 0" icon="file" /></div>
      <div class="col-6 col-lg-3"><StatTile label="In progress" :value="stats.in_progress ?? 0" icon="users" /></div>
      <div class="col-6 col-lg-3"><StatTile label="Placements" :value="stats.placements ?? 0" icon="award" /></div>
      <div class="col-6 col-lg-3"><StatTile label="Open drives" :value="stats.open_drives ?? 0" icon="briefcase" /></div>
    </div>

    <h2 class="h5 mb-3">Organizations</h2>
    <div class="row g-3">
      <div v-for="o in orgs" :key="o.id" class="col-md-6 col-xl-4">
        <button class="surface-card p-3 w-100 text-start org-card" @click="openOrg(o)">
          <div class="fw-semibold">{{ o.company_name }}</div>
          <div class="small text-muted">{{ o.industry }}<span v-if="o.location"> · {{ o.location }}</span></div>
          <div class="small mt-1 accent">{{ o.open_drives }} open drive(s)</div>
        </button>
      </div>
      <p v-if="!orgs.length" class="text-muted">No organizations are hiring yet.</p>
    </div>

    <AppModal v-model="org.open" :title="org.data?.company_name" size="lg">
      <p class="text-muted">{{ org.data?.description }}</p>
      <div class="row g-3">
        <div v-for="d in org.data?.drives || []" :key="d.id" class="col-md-6">
          <DriveCard :drive="d" @apply="apply" @view="() => {}" />
        </div>
        <p v-if="!(org.data?.drives || []).length" class="text-muted">No open drives right now.</p>
      </div>
    </AppModal>
  </div>
</template>

<style scoped>
.org-card { border: 1px solid var(--ppa-border); transition: transform 0.1s ease; }
.org-card:hover { transform: translateY(-2px); }
.accent { color: var(--ppa-accent); }
</style>
