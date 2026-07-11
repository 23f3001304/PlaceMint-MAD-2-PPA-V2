<script setup>
// Shareable company page: about, website + links, and open drives. Any signed-in
// user can open it (students from the org list, admins/companies from theirs).
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import * as directoryApi from '../../api/directory'
import { useAsync } from '../../composables/useAsync'
import Icon from '../../components/Icon.vue'

const { run } = useAsync()
const route = useRoute()
const router = useRouter()
const bundle = ref(null)

const p = computed(() => bundle.value?.profile || {})
const drives = computed(() => bundle.value?.drives || [])
const initial = computed(() => (p.value.company_name || '?')[0].toUpperCase())

onMounted(async () => { bundle.value = (await run(() => directoryApi.company(route.params.id))).data })
</script>

<template>
  <div v-if="bundle" class="motion-fade-up">
    <div class="mb-3">
      <button class="btn btn-sm btn-outline-secondary" @click="router.back()"><Icon name="chevron" :size="14" style="transform: rotate(90deg)" /> Back</button>
    </div>

    <div class="surface-card p-4 mb-3">
      <div class="d-flex align-items-center gap-3">
        <span class="avatar-lg">{{ initial }}</span>
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
  </div>
</template>

<style scoped>
.avatar-lg { width: 60px; height: 60px; border-radius: 50%; background: var(--ppa-accent); color: #fff; display: grid; place-items: center; font-weight: 800; font-size: 1.5rem; font-family: var(--ppa-font-display); flex: none; }
.act-row { display: flex; align-items: center; gap: 1rem; padding: 0.65rem 0; border-top: 1px solid var(--ppa-border); }
.act-row:first-of-type { border-top: 0; }
</style>
