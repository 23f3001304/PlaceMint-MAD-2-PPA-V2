<script setup>
// Shareable, resume-grade student page. Admins and companies can open it (from
// applicant lists or a shared link); admins additionally get an Activity tab.
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import * as directoryApi from '../../api/directory'
import { openDoc } from '../../api/client'
import { useAsync } from '../../composables/useAsync'
import Icon from '../../components/Icon.vue'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const { run } = useAsync()
const route = useRoute()
const router = useRouter()
const bundle = ref(null)
const tab = ref('profile')

const p = computed(() => bundle.value?.profile || {})
const activity = computed(() => bundle.value?.activity)
const initial = computed(() => (p.value.name || '?')[0].toUpperCase())
const photoSrc = computed(() => (p.value.has_photo ? `/api/documents/photo/${p.value.id}` : p.value.photo_url || ''))

onMounted(async () => { bundle.value = (await run(() => directoryApi.student(route.params.id))).data })

function viewResume() { openDoc(`/documents/resume/${p.value.id}`) }
function fmtDate(s) { return s ? new Date(s).toLocaleDateString() : '' }
</script>

<template>
  <div v-if="bundle" class="motion-fade-up">
    <div class="mb-3">
      <button class="btn btn-sm btn-outline-secondary" @click="router.back()"><Icon name="chevron" :size="14" style="transform: rotate(90deg)" /> Back</button>
    </div>

    <div class="surface-card p-4 mb-3">
      <div class="d-flex align-items-center gap-3">
        <span class="avatar-lg">
          <img v-if="photoSrc" :src="photoSrc" alt="" class="photo-img" />
          <template v-else>{{ initial }}</template>
        </span>
        <div class="flex-grow-1">
          <h1 class="h3 mb-1">{{ p.name }}</h1>
          <div class="text-mono small text-muted">{{ p.roll_no }} · {{ p.branch }} · {{ p.degree || 'Degree not set' }}</div>
        </div>
      </div>
      <div class="facts mt-3">
        <div><span class="stat-label">CGPA</span><b>{{ p.cgpa || 'NA' }}</b></div>
        <div><span class="stat-label">Grad year</span><b>{{ p.grad_year || 'NA' }}</b></div>
        <div><span class="stat-label">Email</span><b>{{ p.email || 'NA' }}</b></div>
        <div><span class="stat-label">Phone</span><b>{{ p.phone || 'NA' }}</b></div>
      </div>
    </div>

    <div v-if="activity" class="tabbar mb-3">
      <button :class="{ on: tab === 'profile' }" @click="tab = 'profile'">Profile</button>
      <button :class="{ on: tab === 'activity' }" @click="tab = 'activity'">Activity</button>
    </div>

    <template v-if="tab === 'profile'">
      <div class="surface-card p-4 mb-3">
        <h3 class="sec-head"><span class="sec-ico"><Icon name="award" :size="15" /></span>Skills</h3>
        <div v-if="(p.skills || []).length" class="d-flex flex-wrap gap-2">
          <span v-for="s in p.skills" :key="s" class="skill-pill">{{ s }}</span>
        </div>
        <p v-else class="text-muted mb-0">No skills listed.</p>
      </div>
      <div class="surface-card p-4 mb-3">
        <h3 class="sec-head"><span class="sec-ico"><Icon name="briefcase" :size="15" /></span>Experience</h3>
        <div v-if="(p.experiences || []).length" class="timeline">
          <div v-for="(x, i) in p.experiences" :key="i" class="tl-item">
            <div class="tl-dot"></div>
            <div class="tl-title">{{ x.title }}<span v-if="x.org" class="text-muted fw-normal"> · {{ x.org }}</span></div>
            <div v-if="x.period" class="small text-muted">{{ x.period }}</div>
            <p v-if="x.description" class="mb-0 mt-1" style="white-space: pre-line">{{ x.description }}</p>
          </div>
        </div>
        <p v-else class="text-muted mb-0">No experience listed.</p>
      </div>
      <div v-if="(p.projects || []).length" class="surface-card p-4 mb-3">
        <h3 class="sec-head"><span class="sec-ico"><Icon name="code" :size="15" /></span>Projects</h3>
        <div class="timeline">
          <div v-for="(x, i) in p.projects" :key="i" class="tl-item">
            <div class="tl-dot"></div>
            <div class="tl-title">{{ x.title }}<span v-if="x.period" class="text-muted fw-normal"> · {{ x.period }}</span></div>
            <a v-if="x.link" :href="x.link" target="_blank" rel="noopener" class="small d-inline-block">{{ x.link }}</a>
            <p v-if="x.description" class="mb-0 mt-1" style="white-space: pre-line">{{ x.description }}</p>
          </div>
        </div>
      </div>
      <div v-if="(p.links || []).length" class="surface-card p-4 mb-3">
        <h3 class="sec-head"><span class="sec-ico"><Icon name="link" :size="15" /></span>Links</h3>
        <div class="d-flex flex-wrap gap-2">
          <a v-for="l in p.links" :key="l.url" :href="l.url" target="_blank" rel="noopener" class="link-chip"><Icon name="link" :size="13" /> {{ l.label }}</a>
        </div>
      </div>
      <div class="surface-card p-4">
        <h3 class="sec-head"><span class="sec-ico"><Icon name="file" :size="15" /></span>Resume</h3>
        <button v-if="p.has_resume" class="btn btn-3d-accent btn-sm" @click="viewResume"><Icon name="download" :size="14" /> View resume</button>
        <p v-else class="text-muted mb-0">No resume uploaded.</p>
      </div>
    </template>

    <template v-else>
      <div class="surface-card p-4 mb-3">
        <h3 class="sec-head"><span class="sec-ico"><Icon name="file" :size="15" /></span>Applications ({{ activity.applications.length }})</h3>
        <div v-for="a in activity.applications" :key="a.id" class="act-row">
          <div class="flex-grow-1">
            <div class="fw-semibold">{{ a.drive?.job_title }}</div>
            <div class="small text-muted">{{ a.drive?.company_name }} · Applied {{ fmtDate(a.applied_at) }}<span v-if="a.interview_at"> · Interview {{ fmtDate(a.interview_at) }}</span></div>
          </div>
          <StatusBadge :status="a.status" />
        </div>
        <p v-if="!activity.applications.length" class="text-muted mb-0">No applications yet.</p>
      </div>
      <div class="surface-card p-4">
        <h3 class="sec-head"><span class="sec-ico"><Icon name="award" :size="15" /></span>Placements ({{ activity.placements.length }})</h3>
        <div v-for="pl in activity.placements" :key="pl.id" class="act-row">
          <div class="flex-grow-1"><div class="fw-semibold">{{ pl.position }}</div><div class="small text-muted">{{ pl.company_name }}</div></div>
          <span class="fw-semibold">{{ pl.salary_lpa }} LPA</span>
        </div>
        <p v-if="!activity.placements.length" class="text-muted mb-0">No placements yet.</p>
      </div>
    </template>
  </div>
</template>

<style scoped>
.avatar-lg { width: 60px; height: 60px; border-radius: 50%; background: var(--ppa-accent); color: #fff; display: grid; place-items: center; font-weight: 800; font-size: 1.5rem; font-family: var(--ppa-font-display); flex: none; overflow: hidden; }
.photo-img { width: 100%; height: 100%; object-fit: cover; }
.facts { display: flex; flex-wrap: wrap; gap: 1.75rem; border-top: 1px solid var(--ppa-border); padding-top: 1rem; }
.facts b { display: block; margin-top: 0.1rem; font-family: var(--ppa-font-display); font-size: 1.05rem; }
.tabbar { display: inline-flex; gap: 0.25rem; background: var(--ppa-surface-sunk); padding: 0.25rem; border-radius: 999px; }
.tabbar button { border: 0; background: transparent; padding: 0.4rem 1.15rem; border-radius: 999px; font-weight: 600; color: var(--ppa-muted); }
.tabbar button.on { background: var(--ppa-surface); color: var(--ppa-ink); box-shadow: 0 1px 4px rgba(20, 17, 15, 0.1); }
.act-row { display: flex; align-items: center; gap: 1rem; padding: 0.65rem 0; border-top: 1px solid var(--ppa-border); }
.act-row:first-of-type { border-top: 0; }
</style>
