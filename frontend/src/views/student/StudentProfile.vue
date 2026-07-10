<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import * as studentApi from '../../api/endpoints/student'
import { openDoc } from '../../api/client'
import { setProfile } from '../../store/auth'
import { useAsync } from '../../composables/useAsync'
import { toastError, toastSuccess } from '../../store/ui'
import Icon from '../../components/Icon.vue'
import PageHeader from '../../components/layout/PageHeader.vue'

const { run } = useAsync()
const router = useRouter()
const profile = ref({})
const uploading = ref(false)

const initial = computed(() => (profile.value.name || '?')[0].toUpperCase())
const completeness = computed(() => {
  const p = profile.value
  const checks = [p.name, p.branch, p.degree, p.cgpa, p.grad_year, p.phone,
    (p.skills || []).length, p.experience, (p.links || []).length, p.has_resume]
  return Math.round((checks.filter(Boolean).length / checks.length) * 100)
})

onMounted(async () => { profile.value = (await run(studentApi.profile)).data })

function editProfile() { router.push({ name: 'student-onboarding', query: { edit: 1 } }) }

async function onResume(e) {
  const file = e.target.files[0]
  if (!file) return
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('resume', file)
    const { data } = await studentApi.uploadResume(fd)
    profile.value = data
    setProfile(data)
    toastSuccess('Resume uploaded')
  } catch (err) {
    toastError(err.message)
  } finally {
    uploading.value = false
  }
}
function viewResume() { openDoc(`/documents/resume/${profile.value.id}`) }
</script>

<template>
  <div class="motion-fade-up">
    <PageHeader title="My profile" subtitle="How companies and the placement cell see you">
      <template #actions><button class="btn btn-3d-accent" @click="editProfile">Edit profile</button></template>
    </PageHeader>

    <div class="surface-card profile-hero mb-3">
      <div class="hero-cover"></div>
      <div class="hero-body">
        <span class="avatar-xl">{{ initial }}</span>
        <div class="hero-heading">
          <div class="hero-id">
            <h2 class="h4 mb-1">{{ profile.name }}</h2>
            <div class="text-mono small text-muted">{{ profile.roll_no }} · {{ profile.branch }} · {{ profile.degree || 'Degree not set' }}</div>
          </div>
          <div class="ring" :style="{ '--pct': completeness }" :title="`Profile ${completeness}% complete`">
            <span>{{ completeness }}%</span>
          </div>
        </div>
        <div class="hero-stats">
          <div class="hstat"><span class="stat-label">CGPA</span><span class="hstat-v">{{ profile.cgpa || 'Not set' }}</span></div>
          <div class="hstat"><span class="stat-label">Grad year</span><span class="hstat-v">{{ profile.grad_year || 'Not set' }}</span></div>
          <div class="hstat"><span class="stat-label">Phone</span><span class="hstat-v">{{ profile.phone || 'Not set' }}</span></div>
        </div>
      </div>
    </div>

    <div class="surface-card p-4 mb-3">
      <h3 class="sec-head"><span class="sec-ico"><Icon name="award" :size="15" /></span>Skills</h3>
      <div v-if="(profile.skills || []).length" class="d-flex flex-wrap gap-2">
        <span v-for="s in profile.skills" :key="s" class="skill-pill">{{ s }}</span>
      </div>
      <div v-else class="empty-row">
        <span>No skills added yet</span>
        <button class="btn btn-sm btn-outline-secondary" @click="editProfile">Add skills</button>
      </div>
    </div>

    <div class="surface-card p-4 mb-3">
      <h3 class="sec-head"><span class="sec-ico"><Icon name="briefcase" :size="15" /></span>Experience</h3>
      <p v-if="profile.experience" class="mb-0" style="white-space: pre-line">{{ profile.experience }}</p>
      <div v-else class="empty-row">
        <span>No experience added yet</span>
        <button class="btn btn-sm btn-outline-secondary" @click="editProfile">Add experience</button>
      </div>
    </div>

    <div class="surface-card p-4 mb-3">
      <h3 class="sec-head"><span class="sec-ico"><Icon name="link" :size="15" /></span>Links</h3>
      <div v-if="(profile.links || []).length" class="d-flex flex-wrap gap-2">
        <a v-for="l in profile.links" :key="l.url" :href="l.url" target="_blank" rel="noopener" class="link-chip">
          <Icon name="link" :size="13" /> {{ l.label }}
        </a>
      </div>
      <div v-else class="empty-row">
        <span>No links added yet</span>
        <button class="btn btn-sm btn-outline-secondary" @click="editProfile">Add links</button>
      </div>
    </div>

    <div class="surface-card p-4">
      <h3 class="sec-head"><span class="sec-ico"><Icon name="file" :size="15" /></span>Resume</h3>
      <div v-if="profile.has_resume" class="resume-chip">
        <span class="sec-ico"><Icon name="file" :size="20" /></span>
        <div class="flex-grow-1">
          <div class="fw-semibold">Resume on file</div>
          <div class="small text-muted">PDF or Word document</div>
        </div>
        <button class="btn btn-sm btn-outline-secondary" @click="viewResume">View</button>
        <label class="btn btn-sm btn-outline-secondary mb-0">
          {{ uploading ? 'Uploading...' : 'Replace' }}
          <input type="file" accept=".pdf,.doc,.docx" hidden @change="onResume" />
        </label>
      </div>
      <label v-else class="resume-drop">
        <Icon name="download" :size="24" />
        <span class="fw-semibold">{{ uploading ? 'Uploading...' : 'Upload your resume' }}</span>
        <span class="small">PDF, DOC or DOCX</span>
        <input type="file" accept=".pdf,.doc,.docx" hidden @change="onResume" />
      </label>
    </div>
  </div>
</template>

<style scoped>
.profile-hero { padding: 0; overflow: hidden; }
.hero-cover {
  height: 96px; position: relative;
  background:
    radial-gradient(120% 200% at 100% 0, rgba(46, 138, 77, 0.85), transparent 55%),
    linear-gradient(120deg, var(--ppa-accent), var(--ppa-accent-shadow));
}
.hero-cover::after {
  content: ''; position: absolute; inset: 0;
  background-image: radial-gradient(rgba(255, 255, 255, 0.16) 1px, transparent 1px);
  background-size: 16px 16px;
}
.hero-body { position: relative; padding: 0 clamp(1.25rem, 3vw, 2rem) 1.5rem; }
.avatar-xl {
  position: absolute; top: -38px; left: clamp(1.25rem, 3vw, 2rem);
  width: 76px; height: 76px; border-radius: 50%; background: var(--ppa-accent); color: #fff;
  display: grid; place-items: center; font-weight: 800; font-size: 1.9rem; font-family: var(--ppa-font-display);
  border: 4px solid var(--ppa-surface); box-shadow: 0 8px 20px rgba(20, 17, 15, 0.16);
}
.hero-heading { display: flex; align-items: flex-end; justify-content: space-between; gap: 1rem; padding: 0.85rem 0 0 92px; }
.hero-id { min-width: 0; }
.ring {
  --pct: 0; width: 62px; height: 62px; border-radius: 50%; flex: none; position: relative;
  background: conic-gradient(var(--ppa-accent) calc(var(--pct) * 1%), var(--ppa-surface-sunk) 0);
  display: grid; place-items: center;
}
.ring::before { content: ''; position: absolute; inset: 5px; border-radius: 50%; background: var(--ppa-surface); }
.ring span { position: relative; font-family: var(--ppa-font-display); font-weight: 800; font-size: 0.8rem; }
.hero-stats { display: flex; margin-top: 1.25rem; border-top: 1px solid var(--ppa-border); }
.hstat { flex: 1; padding: 0.9rem 0.5rem 0; }
.hstat + .hstat { border-left: 1px solid var(--ppa-border); padding-left: 1rem; }
.hstat-v { display: block; margin-top: 0.15rem; font-family: var(--ppa-font-display); font-weight: 700; font-size: 1.1rem; }
</style>
