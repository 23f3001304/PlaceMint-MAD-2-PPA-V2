<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import * as studentApi from '../../api/endpoints/student'
import { openDoc } from '../../api/client'
import { setProfile } from '../../store/auth'
import { useAsync } from '../../composables/useAsync'
import { toastError, toastSuccess } from '../../store/ui'
import AppModal from '../../components/overlays/AppModal.vue'
import FormField from '../../components/forms/FormField.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import { BRANCHES, GRAD_YEARS } from '../../data/options'

const { run } = useAsync()
const profile = ref({})
const editing = ref(false)
const uploading = ref(false)
const form = reactive({ name: '', branch: '', degree: '', cgpa: '', grad_year: '', phone: '', skills: '', experience: '' })

const initial = computed(() => (profile.value.name || '?')[0].toUpperCase())

onMounted(async () => { profile.value = (await run(studentApi.profile)).data })

function openEdit() {
  const p = profile.value
  Object.assign(form, {
    name: p.name, branch: p.branch, degree: p.degree || '', cgpa: p.cgpa || '',
    grad_year: p.grad_year, phone: p.phone || '', skills: (p.skills || []).join(', '), experience: p.experience || '',
  })
  editing.value = true
}
async function save() {
  const p = (await run(() => studentApi.updateProfile({ ...form }))).data
  profile.value = p
  setProfile(p)
  editing.value = false
  toastSuccess('Profile updated')
}
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
  <div class="motion-fade-up" style="max-width: 820px">
    <PageHeader title="My profile" subtitle="How companies and the placement cell see you">
      <template #actions><button class="btn btn-3d-accent" @click="openEdit">Edit profile</button></template>
    </PageHeader>

    <div class="surface-card p-4 mb-3">
      <div class="d-flex align-items-center gap-3 mb-3">
        <span class="avatar-lg">{{ initial }}</span>
        <div>
          <h2 class="h4 mb-0">{{ profile.name }}</h2>
          <div class="text-mono small text-muted">{{ profile.roll_no }} · {{ profile.branch }} · {{ profile.degree || 'Degree not set' }}</div>
        </div>
        <span v-if="profile.id && !profile.profile_complete" class="status-badge st-pending ms-auto">Incomplete</span>
      </div>
      <div class="row g-3">
        <div class="col-4"><div class="stat-label">CGPA</div><div class="fw-semibold">{{ profile.cgpa || 'Not set' }}</div></div>
        <div class="col-4"><div class="stat-label">Grad year</div><div class="fw-semibold">{{ profile.grad_year }}</div></div>
        <div class="col-4"><div class="stat-label">Phone</div><div class="fw-semibold">{{ profile.phone || 'Not set' }}</div></div>
      </div>
    </div>

    <div class="surface-card p-4 mb-3">
      <h3 class="h6 mb-2">Skills</h3>
      <div v-if="(profile.skills || []).length">
        <span v-for="s in profile.skills" :key="s" class="badge text-bg-light me-1 mb-1">{{ s }}</span>
      </div>
      <p v-else class="text-muted mb-0">No skills added yet.</p>
    </div>

    <div class="surface-card p-4 mb-3">
      <h3 class="h6 mb-2">Experience</h3>
      <p class="mb-0" :class="{ 'text-muted': !profile.experience }" style="white-space: pre-line">
        {{ profile.experience || 'No experience added yet.' }}
      </p>
    </div>

    <div class="surface-card p-4">
      <h3 class="h6 mb-2">Resume</h3>
      <div class="d-flex gap-2 flex-wrap align-items-center">
        <label class="btn btn-outline-secondary mb-0">
          {{ uploading ? 'Uploading...' : (profile.has_resume ? 'Replace resume' : 'Upload resume') }}
          <input type="file" accept=".pdf,.doc,.docx" hidden @change="onResume" />
        </label>
        <button v-if="profile.has_resume" class="btn btn-outline-secondary" @click="viewResume">View resume</button>
        <span v-else class="text-muted small">No resume uploaded.</span>
      </div>
    </div>

    <AppModal v-model="editing" title="Edit profile" size="lg">
      <div class="row gx-3">
        <div class="col-md-8"><FormField id="ename" v-model="form.name" label="Full name" required /></div>
        <div class="col-md-4"><FormField id="ebranch" v-model="form.branch" label="Branch" type="select" :options="BRANCHES" /></div>
        <div class="col-md-4"><FormField id="edeg" v-model="form.degree" label="Degree" /></div>
        <div class="col-6 col-md-4"><FormField id="ecgpa" v-model="form.cgpa" label="CGPA" type="number" step="0.01" /></div>
        <div class="col-6 col-md-4"><FormField id="egy" v-model="form.grad_year" label="Grad year" type="select" :options="GRAD_YEARS" /></div>
        <div class="col-md-6"><FormField id="ephone" v-model="form.phone" label="Phone" /></div>
        <div class="col-md-6"><FormField id="eskills" v-model="form.skills" label="Skills" hint="Comma separated" /></div>
        <div class="col-12"><FormField id="eexp" v-model="form.experience" label="Experience" type="textarea" /></div>
      </div>
      <template #footer>
        <button class="btn btn-outline-secondary" @click="editing = false">Cancel</button>
        <button class="btn btn-3d-accent" @click="save">Save changes</button>
      </template>
    </AppModal>
  </div>
</template>

<style scoped>
.avatar-lg {
  width: 56px; height: 56px; border-radius: 50%; background: var(--ppa-accent); color: #fff;
  display: grid; place-items: center; font-weight: 700; font-size: 1.4rem; font-family: var(--ppa-font-display);
}
</style>
