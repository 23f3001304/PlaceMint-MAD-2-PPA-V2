<script setup>
import { onMounted, ref } from 'vue'

import * as companyApi from '../../api/endpoints/company'
import { authState, setProfile } from '../../store/auth'
import PageHeader from '../../components/layout/PageHeader.vue'
import StatTile from '../../components/ui/StatTile.vue'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const stats = ref({})
const approved = ref(authState.profile?.approval_status === 'approved')

onMounted(async () => {
  const p = await companyApi.profile()
  setProfile(p.data)
  approved.value = p.data.approval_status === 'approved'
  stats.value = (await companyApi.stats()).data
})
</script>

<template>
  <div class="motion-fade-up">
    <PageHeader :title="authState.profile?.company_name" subtitle="Company dashboard" />

    <div v-if="!approved" class="surface-card p-4 mb-4 pending-note">
      <div class="d-flex align-items-center gap-2 mb-1">
        <span class="fw-semibold">Approval status</span>
        <StatusBadge :status="authState.profile?.approval_status" />
      </div>
      <p class="text-muted mb-0">You can post placement drives once the cell approves your company.</p>
    </div>

    <div class="row g-3">
      <div class="col-6 col-lg-3"><StatTile label="Drives" :value="stats.drives ?? 0" icon="briefcase" /></div>
      <div class="col-6 col-lg-3"><StatTile label="Active drives" :value="stats.active_drives ?? 0" icon="briefcase" /></div>
      <div class="col-6 col-lg-3"><StatTile label="Applications" :value="stats.applications ?? 0" icon="file" /></div>
      <div class="col-6 col-lg-3"><StatTile label="Shortlisted" :value="stats.shortlisted ?? 0" icon="users" /></div>
      <div class="col-6 col-lg-3"><StatTile label="Placed" :value="stats.placed ?? 0" icon="award" /></div>
    </div>
  </div>
</template>

<style scoped>
.pending-note { background: #fbecc8; border-color: #e6d3a3; }
</style>
