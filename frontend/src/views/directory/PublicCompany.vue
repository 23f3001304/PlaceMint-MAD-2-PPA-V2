<script setup>
// Shareable company page: about, website + links, key people, and open drives.
// Admins additionally get an Applicants tab (every student who applied here).
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import * as directoryApi from '../../api/directory'
import { useAsync } from '../../composables/useAsync'
import Icon from '../../components/Icon.vue'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const { run } = useAsync()
const route = useRoute()
const router = useRouter()
const bundle = ref(null)
const tab = ref('overview')

const p = computed(() => bundle.value?.profile || {})
const drives = computed(() => bundle.value?.drives || [])
const applicants = computed(() => bundle.value?.applicants)
const initial = computed(() => (p.value.company_name || '?')[0].toUpperCase())
const logoSrc = computed(() => `/api/documents/logo/${p.value.id}`)

onMounted(async () => { bundle.value = (await run(() => directoryApi.company(route.params.id))).data })
function fmtDate(s) { return s ? new Date(s).toLocaleDateString() : '' }
</script>

<template>
  <div v-if="bundle" class="motion-fade-up">
    <div class="mb-3">
      <button class="btn btn-sm btn-outline-secondary" @click="router.back()"><Icon name="chevron" :size="14" style="transform: rotate(90deg)" /> Back</button>
    </div>

    <div class="surface-card p-4 mb-3">
      <div class="d-flex align-items-center gap-3">
        <span class="avatar-lg" :class="{ 'has-logo': p.has_logo }">
          <img v-if="p.has_logo" :src="logoSrc" alt="" class="logo-img" />
          <template v-else>{{ initial }}</template>
        </span>
        <div class="flex-grow-1">
          <h1 class="h3 mb-1">{{ p.company_name }}</h1>
          <div class="small text-muted">{{ p.industry || 'Industry not set' }}<span v-if="p.location"> · {{ p.location }}</span></div>
        </div>
      </div>
      <div v-if="p.website || (p.links || []).length" class="d-flex flex-wrap gap-2 mt-3 pt-3 border-top">
        <a v-if="p.website" :href="p.website" target="_blank" rel="noopener" class="link-chip"><Icon name="globe" :size="13" /> Website</a>
        <a v-for="l in p.links" :key="l.url" :href="l.url" target="_blank" rel="noopener" class="link-chip"><Icon name="link" :size="13" /> {{ l.label }}</a>
      </div>
    </div>

    <div v-if="applicants" class="tabbar mb-3">
      <button :class="{ on: tab === 'overview' }" @click="tab = 'overview'">Overview</button>
      <button :class="{ on: tab === 'applicants' }" @click="tab = 'applicants'">Applicants ({{ applicants.length }})</button>
    </div>

    <template v-if="tab === 'overview'">
      <div v-if="(p.people || []).length" class="surface-card p-4 mb-3">
        <h3 class="sec-head"><span class="sec-ico"><Icon name="users" :size="15" /></span>Key people</h3>
        <div class="d-flex flex-wrap gap-3">
          <div v-for="person in p.people" :key="person.name" class="person-card">
            <span class="person-avatar">{{ (person.name || '?')[0].toUpperCase() }}</span>
            <div>
              <div class="fw-semibold">{{ person.name }}</div>
              <div class="small text-muted">{{ person.role }}</div>
              <a v-if="person.url" :href="person.url" target="_blank" rel="noopener" class="small">View profile</a>
            </div>
          </div>
        </div>
      </div>

      <div class="surface-card p-4 mb-3">
        <h3 class="sec-head"><span class="sec-ico"><Icon name="building" :size="15" /></span>About</h3>
        <p class="mb-0" :class="{ 'text-muted': !p.description }" style="white-space: pre-line">{{ p.description || 'No description provided.' }}</p>
      </div>

      <div class="surface-card p-4">
        <h3 class="sec-head"><span class="sec-ico"><Icon name="briefcase" :size="15" /></span>Open drives ({{ drives.length }})</h3>
        <div v-for="d in drives" :key="d.id" class="act-row">
          <div class="flex-grow-1"><div class="fw-semibold">{{ d.job_title }}</div><div class="small text-muted">{{ d.location || 'Location NA' }} · {{ d.package_lpa }} LPA</div></div>
          <span class="small text-muted">{{ d.applicant_count }} applied</span>
        </div>
        <p v-if="!drives.length" class="text-muted mb-0">No open drives right now.</p>
      </div>
    </template>

    <template v-else>
      <div class="surface-card p-4">
        <h3 class="sec-head"><span class="sec-ico"><Icon name="users" :size="15" /></span>Applicants ({{ applicants.length }})</h3>
        <div v-for="a in applicants" :key="a.id" class="act-row">
          <div class="flex-grow-1">
            <button class="btn btn-link p-0 fw-semibold text-start" @click="router.push(`/students/${a.student_id}`)">{{ a.student_name }}</button>
            <div class="small text-muted">{{ a.roll_no }} · {{ a.drive }} · Applied {{ fmtDate(a.applied_at) }}</div>
          </div>
          <StatusBadge :status="a.status" />
        </div>
        <p v-if="!applicants.length" class="text-muted mb-0">No applicants yet.</p>
      </div>
    </template>
  </div>
</template>

<style scoped>
.avatar-lg { width: 60px; height: 60px; border-radius: 50%; background: var(--ppa-accent); color: #fff; display: grid; place-items: center; font-weight: 800; font-size: 1.5rem; font-family: var(--ppa-font-display); flex: none; overflow: hidden; }
.avatar-lg.has-logo { background: #fff; border: 1px solid var(--ppa-border); }
.logo-img { width: 100%; height: 100%; object-fit: contain; padding: 4px; }
.tabbar { display: inline-flex; gap: 0.25rem; background: var(--ppa-surface-sunk); padding: 0.25rem; border-radius: 999px; }
.tabbar button { border: 0; background: transparent; padding: 0.4rem 1.15rem; border-radius: 999px; font-weight: 600; color: var(--ppa-muted); }
.tabbar button.on { background: var(--ppa-surface); color: var(--ppa-ink); box-shadow: 0 1px 4px rgba(20, 17, 15, 0.1); }
.act-row { display: flex; align-items: center; gap: 1rem; padding: 0.65rem 0; border-top: 1px solid var(--ppa-border); }
.act-row:first-of-type { border-top: 0; }
</style>
